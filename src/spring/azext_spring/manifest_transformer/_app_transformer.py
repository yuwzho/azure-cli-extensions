# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
import re

from .base_transformer import Transformer
from .bicep_resource import BicepResource

class AppTransformer(Transformer):
    @property
    def parsable_attributes(self):
        return ['name']

    def _pcf_to_bicep(self, pcf, output, **__):
        for app in pcf.content.get('applications', []):
            spring = output.get_spring()
            app_resource = BicepResource(app.get('name'), 'Microsoft.AppPlatform/Spring/Apps', '2022-12-01', parent=spring)
            output.append(app_resource)
            deployment = BicepResource(app.get('name'), 'Microsoft.AppPlatform/Spring/Apps/Deployments', '2022-12-01', parent=app_resource)
            deployment.properties['active'] = True
            output.append(deployment)

    def _check_pcf_to_bicep_violation(self, pcf, **__):
        for app in pcf.content.get('applications', []):
            self._check_app_name(app.get('name'))
    
    def _check_app_name(self, name):
        pattern = r'^[a-z][a-z0-9-]*[a-z0-9]$'
        if not re.match(pattern, name):
            raise ValueError(f"Found invalid app name '{name}'. It must match the pattern '{pattern}'")