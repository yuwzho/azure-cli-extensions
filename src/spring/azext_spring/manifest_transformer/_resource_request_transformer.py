# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

from knack.log import get_logger

from .base_transformer import PCFToBicepAppTransformer, BicepResourceType

logger = get_logger(__name__)

class CPUResourceRequestTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['cpu'] 

    @property
    def _pcf_path(self):
        return 'cpu' 

    @property
    def _bicep_path(self):
        return 'deploymentSettings.resourceRequests.cpu'

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.Deployment.value
    
    def _convert_pcf_value_to_bicep_value(self, value):
        return value or '1'
    
    def _check_app_violation(self, app, cpu):
        if not cpu or cpu < 0:
            logger.warning(f'Invalid CPU value for app {app.get("name")}. Expect a positive integer. Setting it to 1.')
  

class MemoryResourceRequestTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['memory'] 

    @property
    def _pcf_path(self):
        return 'memory' 

    @property
    def _bicep_path(self):
        return 'deploymentSettings.resourceRequests.memory'

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.Deployment.value

    def _convert_pcf_value_to_bicep_value(self, value):
        return '{}i'.format(value or '1G')

    def _check_app_violation(self, app, memory):
        if not memory:
            logger.warning(f'Invalid memory value for app {app.get("name")}. Expect a string. Setting it to 1Gi.')


class SkuCapacityTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['instances'] 

    @property
    def _pcf_path(self):
        return 'instances' 

    @property
    def _bicep_path(self):
        return 'sku.capacity'

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.Deployment.value

    def _add_to_bicep(self, resource, value):
        resource.put_additional_properties('sku', {
            'tier': 'Enterprise',
            'name': 'E0',
            'capacity': value
        })

    def _convert_pcf_value_to_bicep_value(self, value):
        return value or 1

    def _check_app_violation(self, app, instance):
        if not instance or instance < 0:
            logger.warning(f'Invalid instances value for app {app.get("name")}. Expect a positive integer. Setting it to 1.')
