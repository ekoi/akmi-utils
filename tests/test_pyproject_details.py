import os

import toml

from src.akmi_utils.commons import get_project_details


def get_project_details_valid_keys(self):
    toml_content = {
        'project': {
            'name': 'akmi-utils',
            'version': '0.1.5.2',
            'description': 'A utility package for akmi'
        }
    }
    input_toml_path = os.path.join(self.test_dir.name, 'pyproject.toml')
    with open(input_toml_path, 'w') as toml_file:
        toml.dump(toml_content, toml_file)

    details = get_project_details(self.test_dir.name, ['name', 'version', 'description'])
    self.assertEqual(details, {
        'name': 'akmi-utils',
        'version': '0.1.5.2',
        'description': 'A utility package for akmi'
    })

def get_project_details_invalid_key(self):
    toml_content = {
        'project': {
            'name': 'akmi-utils',
            'version': '0.1.5.2'
        }
    }
    input_toml_path = os.path.join(self.test_dir.name, 'pyproject.toml')
    with open(input_toml_path, 'w') as toml_file:
        toml.dump(toml_content, toml_file)

    with self.assertRaises(KeyError):
        get_project_details(self.test_dir.name, ['nonexistent_key'])

def get_project_details_empty_keys(self):
    toml_content = {
        'project': {
            'name': 'akmi-utils',
            'version': '0.1.5.2'
        }
    }
    input_toml_path = os.path.join(self.test_dir.name, 'pyproject.toml')
    with open(input_toml_path, 'w') as toml_file:
        toml.dump(toml_content, toml_file)

    details = get_project_details(self.test_dir.name, [])
    self.assertEqual(details, {})