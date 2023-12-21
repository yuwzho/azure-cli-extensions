# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

import yaml
from knack.log import get_logger

logger = get_logger(__name__)

class PCFFile():
    def __init__(self, content):
        self.content = content

    @classmethod
    def load(cls, source):
        with open(source, 'r') as file:
            return cls(yaml.safe_load(file))
    
    def dump(self, *_):
        pass

    def filter_unparsable_attributes(self, parsable_attributes):
        def traverse_dict(prefix, d):
            unparsable = []
            for k, v in d.items():
                new_key = f"{prefix}.{k}" if prefix else k
                if new_key in parsable_attributes:
                    continue
                if isinstance(v, dict):
                    unparsable.extend(traverse_dict(new_key, v))
                else:
                    unparsable.append(new_key)
            return unparsable
        applications = self.content.get('applications', [])
        for app in applications:
            unparsable_attributes = traverse_dict(None, app)
            logger.warning('For application {}, the following attributes cannot be converted.\n  - {}'
                         .format(app.get('name', ''), '\n  - '.join(unparsable_attributes)))