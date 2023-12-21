# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
from .base_transformer import PCFToBicepAppTransformer, BicepResourceType

from knack.log import get_logger

logger = get_logger(__name__)

class EnvTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['env'] 

    @property
    def _pcf_path(self):
        return 'env' 

    @property
    def _bicep_path(self):
        return 'deploymentSettings.environmentVariables'

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.Deployment.value
