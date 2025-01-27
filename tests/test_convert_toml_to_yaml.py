import unittest
import tempfile
import os
import toml
import yaml

from src.akmi_utils.convert_toml_yaml import convert_toml_to_yaml


class TestConvertTomlToYaml(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_conversion(self):
        # Define sample TOML content
        toml_content = {
            'title': 'Title Example',
            'owner': {
                'name': 'Eko Indarto',
                'orcid': '0000-0001-6208-6637'
            }
        }

        # Create a temporary TOML file
        input_toml_path = os.path.join(self.test_dir.name, 'test_input.toml')
        with open(input_toml_path, 'w') as toml_file:
            toml.dump(toml_content, toml_file)

        # Create a temporary YAML file path
        output_yaml_path = os.path.join(self.test_dir.name, 'test_output.yaml')

        # Perform the conversion
        convert_toml_to_yaml(input_toml_path, output_yaml_path)

        # Read the YAML file and verify its content
        with open(output_yaml_path, 'r') as yaml_file:
            yaml_content = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        self.assertEqual(toml_content, yaml_content)

if __name__ == '__main__':
    unittest.main()