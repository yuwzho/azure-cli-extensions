import os
import tarfile
import tempfile
import unittest
from ..._utils import _pack_source_code

class TestPackSourceCode(unittest.TestCase):
    def test_pack_source_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a node_modules folder and a .gitignore file
            source_path = os.path.join(temp_dir, 'source')
            os.makedirs(source_path)
            os.makedirs(os.path.join(source_path, 'node_modules'))
            with open(os.path.join(source_path, '.gitignore'), 'w') as f:
                f.write('node_modules')

            # Create a file under the node_modules folder
            with open(os.path.join(source_path, 'node_modules', 'test.txt'), 'w') as f:
                f.write('test')

            with open(os.path.join(source_path, 'exist.txt'), 'w') as f:
                f.write('test')

            # Call the _pack_source_code method
            archive_file = os.path.join(temp_dir, 'target') 
            _pack_source_code(source_path, archive_file)

            # Verify that the node_modules folder and its contents are not in the archive
            with tarfile.open(archive_file, 'r') as tf:
                self.assertNotIn('node_modules', tf.getnames())
                self.assertNotIn('node_modules/test.txt', tf.getnames())
                self.assertIn('exist.txt', tf.getnames())
