# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

import yaml
from knack.log import get_logger

logger = get_logger(__name__)


class PCFApp():
    def __init__(self, content):
        self.content = content
        self.name = content.get('name', '')
        self.parsed_attributes = []

    def find_value(self, path):
        if not path:
            return None
        keys = path.split('.')
        tmp = self.content
        for k in keys[:-1]:
            tmp = tmp.get(k, {})
        return tmp.get(keys[-1], None)

    def mark_parsed_attribute(self, path):
        if path:
            self.parsed_attributes.extend(path)

    def filter_unparsable_attributes(self):
        def traverse_dict(key, node):
            if key in self.parsed_attributes:
                return []
            if not isinstance(node, dict):
                return [key]
            unparsable = []
            for k, v in node.items():
                new_key = f"{key}.{k}" if key else k
                unparsable.extend(traverse_dict(new_key, v))
            return unparsable
        return traverse_dict(None, self.content)


class PCFFile():
    def __init__(self, content):
        self.content = content
        self.applications = [PCFApp(x) for x in content.get('applications', [])]

    @classmethod
    def load(cls, source):
        with open(source, 'r') as file:
            return cls(yaml.safe_load(file))
    
    def dump(self, *_):
        pass

    def mark_parsed_attribute(self, path):
        for app in self.applications:
            app.mark_parsed_attribute(path)

    def filter_unparsable_attributes(self):
        for app in self.applications:
            logger.warning('For application {}, the following attributes cannot be converted.\n  - {}'
                         .format(app.name, '\n  - '.join(app.filter_unparsable_attributes())))
