# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

class Transformer:
    def __init__(self, source_type, dest_type):
        if source_type.lower() == 'pcf' and dest_type.lower() == 'bicep':
            self.process = self._pcf_to_bicep
            self.check_violation = self._check_pcf_to_bicep_violation
        else:
            raise AttributeError('Cannot find transformer from {} to {}'.format(source_type, dest_type))

    def _pcf_to_bicep(self, *_, **__):
        pass

    def _check_pcf_to_bicep_violation(self, *_, **__):
        pass
