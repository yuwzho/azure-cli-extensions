# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import unittest
import os
import tempfile
import glob

from ...manifest_transformer.manifest_transformer import import_manifest

try:
    import unittest.mock as mock
except ImportError:
    from unittest import mock

from azure.cli.core.mock import DummyCli
from azure.cli.core import AzCommandsLoader
from azure.cli.core.commands import AzCliCommand

from knack.log import get_logger

logger = get_logger(__name__)
TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))

def _get_test_cmd():
    cli_ctx = DummyCli()
    cli_ctx.data['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    loader = AzCommandsLoader(cli_ctx, resource_type='Microsoft.AppPlatform')
    cmd = AzCliCommand(loader, 'test', None)
    cmd.command_kwargs = {'resource_type': 'Microsoft.AppPlatform'}
    cmd.cli_ctx = cli_ctx
    return cmd


# azdev test spring.test_asa_import_manifest --discover
class TestRoudtrip(unittest.TestCase):
    def test_roundtrip(self):
        # List all yaml files under the folder
        yaml_files = glob.glob(os.path.join(os.path.join(TEST_DIR, 'pcf_2_bicep'), '*.yml'))

        for yaml_file in yaml_files:
            bicep_file = os.path.splitext(yaml_file)[0] + '.bicep'
            self._compare_file(yaml_file, bicep_file)
            
    def _compare_file(self, yaml, bicep):
        _, tmp_file = tempfile.mkstemp()
        import_manifest(_get_test_cmd(), mock.MagicMock(), yaml, tmp_file)
        with open(tmp_file, 'r') as f:
            tmp_content = f.read()

        with open(bicep, 'r') as f:
            bicep_content = f.read()
        
        self.assertEqual(tmp_content, bicep_content,
                         f'Run command `az spring import-manifest -s {yaml} -d {bicep}` and check git diff.')
