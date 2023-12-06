# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

from ._app_transformer import AppTransformer
from ._resource_request_transformer import CPUResourceRequestTransformer, MemoryResourceRequestTransformer, SkuCapacityTransformer
from ._source_transformer import SourceTransformer
from ._public_endpoint_transformer import PublicEndpointTransformer
from .bicep_resource import BicepFile

def get_transformers(source_type, dest_type):
    if source_type.lower() == 'pcf' and dest_type.lower() == 'bicep':
        return [
            AppTransformer(source_type, dest_type),
            CPUResourceRequestTransformer(source_type, dest_type),
            MemoryResourceRequestTransformer(source_type, dest_type),
            SkuCapacityTransformer(source_type, dest_type),
            SourceTransformer(source_type, dest_type),
            PublicEndpointTransformer(source_type, dest_type)
        ]
    raise AttributeError('Cannot find transformers to transform from {} to {}'.format(source_type, dest_type))

def init_transformed(dest_type):
    return BicepFile()