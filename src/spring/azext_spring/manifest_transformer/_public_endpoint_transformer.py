# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines
from .base_transformer import Transformer

from knack.log import get_logger

logger = get_logger(__name__)

class PublicEndpointTransformer(Transformer):
    def _pcf_to_bicep(self, input, output, **__):
        for app in input.get('applications', []):
            if app.get('no-route', True):
                resource = output.find('Microsoft.AppPlatform/Spring/Apps', app.get('name', ''))
                if not resource:
                    raise KeyError(f'Cannot find App resource {app.get("name")} in Bicep resources')
                resource.put_properties('public', True)

    # do nothing for violation check
    def _check_pcf_to_bicep_violation(self, *_, **__):
        pass