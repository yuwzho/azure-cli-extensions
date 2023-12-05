# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

from knack.log import get_logger

from .base_transformer import Transformer

logger = get_logger(__name__)

class ResourceRequestTransformer(Transformer):

    def _pcf_to_bicep(self, input, output, **__):
        for app in input.get('applications', []):
            resource = output.find('Microsoft.AppPlatform/Spring/Apps/Deployments', app.get('name', ''))
            if not resource:
                raise KeyError(f'Cannot find deployment resource {app.get("name")} in Bicep resources')
            resource.put_properties('deploymentSettings.resourceRequests', {
                'cpu': app.get('cpu', '1'),
                'memory': self._convert_memory(app.get('memory', '1G'))
            })
            resource.put_additional_properties('sku', {
                'tier': 'Enterprise',
                'name': 'E0',
                'capacity': app.get('instances', 1)
            })

    def _check_pcf_to_bicep_violation(self, input, **__):
        for app in input.get('applications', []):
            self._check_cpu(app.get('name'), app.get('cpu'))
            self._check_memory(app.get('name'), app.get('memory'))
            self._check_instance_count(app.get('name'), app.get('instances'))

    def _convert_memory(self, memory):
        return f'{memory}i'

    def _check_cpu(self, name, cpu):
        if not cpu or cpu < 0:
            logger.warning(f'Invalid CPU value for app {name}. Expect a positive integer. Setting it to 1.')

    def _check_memory(self, name, memory):
        if not memory:
            logger.warning(f'Invalid memory value for app {name}. Expect a string. Setting it to 1Gi.')

    def _check_instance_count(self, name, instance):
        if not instance or instance < 0:
            logger.warning(f'Invalid instances value for app {name}. Expect a positive integer. Setting it to 1.')
