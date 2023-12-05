# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

from .loader_factory import get_loader
from .transfomer_loader import get_transformers, init_transformed

def import_manifest(cmd, client, source, dest, source_type='pcf', dest_type='bicep'):
    raw = get_loader(source_type).load(source)
    feature_transformers = get_transformers(source_type, dest_type)
    transformed = init_transformed(dest_type)
    for transformer in feature_transformers:
        transformer.check_violation(raw)
        transformer.process(raw, transformed)
    transformed.dump(dest)