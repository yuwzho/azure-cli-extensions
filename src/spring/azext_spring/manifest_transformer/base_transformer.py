# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
from enum import Enum
from abc import abstractmethod

class Transformer:
    def __init__(self, source_type, dest_type):
        if source_type.lower() == 'pcf' and dest_type.lower() == 'bicep':
            self.process = self._pcf_to_bicep
            self.check_violation = self._check_pcf_to_bicep_violation
        else:
            raise AttributeError('Cannot find transformer from {} to {}'.format(source_type, dest_type))

    def _pcf_to_bicep(self, *_, **__):
        pass

    def _check_pcf_to_bicep_violation(self, *_, **__):
        pass


class BicepResourceType(Enum):
    App = 'Microsoft.AppPlatform/Spring/Apps'
    Deployment = 'Microsoft.AppPlatform/Spring/Apps/Deployments'


class PCFToBicepAppTransformer(Transformer):
    @property
    @abstractmethod
    def _pcf_path(self):
        pass

    @property
    @abstractmethod
    def _bicep_path(self):
        pass

    @property
    @abstractmethod
    def _bicep_resource_type(self):
        pass

    def _check_pcf_to_bicep_violation(self, input, **__):
        for app in input.get('applications', []):
            value = self._find_value_from_pcf(app)
            self._check_app_violation(app, value)

    def _pcf_to_bicep(self, input, output, **__):
        for app in input.get('applications', []):
            resource = output.find(self._bicep_resource_type, app.get('name', ''))
            if not resource:
                raise KeyError(f'Cannot find {self._bicep_resource_type} resource {app.get("name")} in Bicep resources')
            value = self._find_value_from_pcf(app)
            value = self._convert_pcf_value_to_bicep_value(value)
            if value:
                self._add_to_bicep(resource, value)
    
    def _find_value_from_pcf(self, app):
        if not self._pcf_path:
            return None
        keys = self._pcf_path.split('.')
        tmp = app
        for k in keys[:-1]:
            tmp = tmp.get(k, {})
        return tmp.get(keys[-1], None)

    def _convert_pcf_value_to_bicep_value(self, pcf_value):
        return pcf_value

    def _add_to_bicep(self, resource, value):
        resource.put_properties(self._bicep_path, value)
    
    @abstractmethod
    def _check_app_violation(self, app, value):
        pass
