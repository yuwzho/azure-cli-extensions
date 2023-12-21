# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
import re

from knack.log import get_logger

logger = get_logger(__name__)

def _format_resource_name(resource_type, resource_name):
    if isinstance(resource_name, BicepParam):
        resource_name = 'resource'
    return '{}_{}'.format(resource_type.split('/')[-1].lower(), resource_name.replace('-', '_'))


def _dict_to_str(d, indent=''):
    if not d:
        return ''
    items = []
    for k, v in d.items():
        if isinstance(v, dict):
            new_str = _dict_to_str(v, indent + '  ')
            items.append(indent + k + ' : {\n' + new_str + '\n' + indent + '}')
        elif isinstance(v, bool):
            items.append(f"{indent}{k} : {str(v).lower()}")
        elif isinstance(v, str):
            items.append(f"{indent}{k} : '{v}'")
        else:
            items.append(f"{indent}{k} : {v}")
    return '\n'.join(items)

class BicepResource:
    def __init__(self, resource_name, resource_type, api_version, is_existing=False, properties=None, parent=None):
        self.name = _format_resource_name(resource_type, resource_name)
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.api_version = api_version
        self.properties = properties or {}
        self.is_existing = is_existing
        self.parent = parent
        self.additional_properties = {}

    def put_properties(self, key, value):
        keys = key.split('.')
        temp = self.properties
        for k in keys[:-1]:
            temp = temp.setdefault(k, {})
        temp[keys[-1]] = value

    def get_property(self, key):
        keys = key.split('.')
        tmp = self.properties
        for k in keys[:-1]:
            tmp = tmp.get(k, {})
        return tmp.get(keys[-1], None)

    def put_additional_properties(self, key, value):
        keys = key.split('.')
        temp = self.additional_properties
        for k in keys[:-1]:
            temp = temp.setdefault(k, {})
        temp[keys[-1]] = value

    def _get_parent(self):
        return f'parent: {self.parent.name}' if self.parent else ''

    def _get_properties_str(self):
        properties = _dict_to_str(self.properties, indent='      ')
        if not properties:
            return ''
        return f"""
    properties: {'{'}
{properties}
    {'}'}"""

    def _get_resource_name(self):
        if isinstance(self.resource_name, BicepParam):
            return f'name: {self.resource_name.name}'
        return 'name: ' + '\'' + self.resource_name + '\''

    def __str__(self):
        result = f"""
resource {self.name} '{self.resource_type}@{self.api_version}' {'existing' if self.is_existing else ''} = {'{'}
    {self._get_resource_name()}
    {self._get_parent()}
    {self._get_properties_str()}
{_dict_to_str(self.additional_properties, indent='    ')}
{'}'}
"""
        return re.sub(r'\n([ ]*\n)+', '\n', result)


class BicepParam:
    def __init__(self, name, type, description=None):
        self.name = name
        self.type = type or 'string'
        self.description = description
    
    def __str__(self):
        param = f'param {self.name} {self.type}'
        if self.description:
            return f'@description(\'{self.description}\')\n{param}\n'
        return param

class BicepFile:
    def __init__(self):
        self.params = []
        self.resources = []
        self._init_spring()

    def _init_spring(self):
        param = BicepParam('name', 'string', 'Existing Azure Spring Apps instance name.')
        resource = BicepResource(param, 'Microsoft.AppPlatform/Spring', '2022-12-01', is_existing=True)
        self.resources.append(resource)
        self.params.append(param)

    def append(self, resource):
        if type(resource) is not BicepResource:
            raise AttributeError('resource should be type BicepResource')
        self.resources.append(resource)

    def find(self, resource_type, resource_name):
        target = _format_resource_name(resource_type, resource_name)
        return next(x for x in self.resources if x.name == target)

    def get_spring(self):
        return self.resources[0]

    def load(self, source):
        pass
    
    def dump(self, dest):
        with open(dest, 'w') as f:
            for x in self.params:
                f.writelines(str(x))
            for x in self.resources:
                f.writelines(str(x))
        logger.warning(f'Run `az deployment group create --template-file {dest} -g <Your-Resource-Group>` to deploy')