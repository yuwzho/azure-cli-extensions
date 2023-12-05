# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

from .pcf_loader import PCF_Loader

def get_loader(manifest_type):
    if manifest_type.lower() == 'pcf':
        return PCF_Loader()