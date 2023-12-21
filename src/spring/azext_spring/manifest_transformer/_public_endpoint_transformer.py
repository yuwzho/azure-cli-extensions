# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
from .base_transformer import PCFToBicepAppTransformer, BicepResourceType

from knack.log import get_logger

logger = get_logger(__name__)

class PublicEndpointTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['no-route'] 

    @property
    def _pcf_path(self):
        return 'no-route' 

    @property
    def _bicep_path(self):
        return 'public'

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.App.value

    def _convert_pcf_value_to_bicep_value(self, value):
        if value: # if no-route is True, do nothing, else expose
            return None
        else:
            return True
