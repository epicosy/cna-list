# tests/test_loader.py

import unittest
from unittest.mock import patch
from pathlib import Path
from cna_list.loader import CNALoader
from cna_list.models import CNA
from pydantic import ValidationError

cna1 = {
    'id': "cna1",
    'name': "CNA 1",
    'root': "root1@org.com",
    'email': "security@apache.org",
    'scope': {
        "external": True,
        "third_party": False,
        "organizations": ["cna1_org"]
    }
}

cna2 = {
    'id': "adobe",
    'name': "Adobe Systems Incorporated",
    'root': "cve@mitre.org",
    'email': "psirt@adobe.com",
    'scope': {
        "external": False,
        "third_party": False,
        "organizations": ["adobe"]
    }
}

invalid_cna = {
    "id": "invalid",
    "name": "Invalid CNA",
    "root": "",
    "email": "",
    "scope": {
        "external": False,
        "third_party": False,
        "organizations": ["invalid"]
    }
}


class TestCNALoader(unittest.TestCase):
    @patch('cna_list.loader.json.load')
    @patch('cna_list.loader.Path.open')  # Mock the open method for the Path object
    @patch('cna_list.loader.Path.exists', return_value=True)  # Mocking file existence
    @patch('cna_list.loader.get_external_path', return_value=Path('tests/mock_data'))  # Mocking path retrieval
    @patch('cna_list.loader.Path.iterdir', return_value=[
        Path('tests/mock_data/cna1.json'),  # Mocking paths to files
        Path('tests/mock_data/cna2.json')
    ])
    def test_load_cna_data(self, mock_iterdir, mock_get_external_path, mock_exists, mock_open, mock_json_load):
        mock_json_load.side_effect = [cna1, cna2]

        # Act
        loader = CNALoader()

        # Assert
        self.assertIn('security@apache.org', loader.records)
        self.assertIn('psirt@adobe.com', loader.records)

    @patch('cna_list.loader.Path.exists', return_value=False)
    def test_invalid_path(self, mock_exists):
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            CNALoader(Path('/invalid/path'))

    @patch('cna_list.loader.get_external_path', return_value=Path('tests/mock_data'))
    @patch('cna_list.loader.Path.exists', return_value=True)
    @patch.object(CNALoader, 'load', side_effect=lambda x: CNA(**cna2))  # Mock load method
    @patch('cna_list.loader.Path.open')  # Mock the open method for the Path object
    def test_load_specific_file(self, mock_open, mock_json_load, mock_exists, mock_get_external_path):
        # Setup
        mock_json_load.return_value = cna2

        # Act
        cna = CNALoader.load_from_external('cna2.json')

        # Assert
        self.assertEqual(cna.id, 'adobe')
        self.assertEqual(cna.email, 'psirt@adobe.com')

    @patch('cna_list.loader.get_external_path', return_value=Path('tests/mock_data'))
    @patch('cna_list.loader.Path.exists', return_value=True)
    @patch('cna_list.loader.Path.iterdir', return_value=[Path('tests/mock_data/invalid_cna.json')])
    @patch('cna_list.loader.Path.open')  # Mock the open method for the Path object
    @patch('cna_list.loader.json.load')
    def test_invalid_json_format(self, mock_json_load, mock_open, mock_iterdir, mock_exists, mock_get_external_path):
        mock_json_load.side_effect = [invalid_cna]

        # Act & Assert: Validate that a ValidationError is raised
        with self.assertRaises(ValidationError):
            CNALoader()  # This should now raise a ValidationError because of invalid data in the CNA model

#    @patch.object(CNALoader, 'load', side_effect=lambda x: CNA(**invalid_cna))  # Mock load method

    @patch('cna_list.loader.get_external_path', return_value=Path('tests/mock_data'))
    @patch('cna_list.loader.Path.open')  # Mock the open method for the Path object
    @patch('cna_list.loader.Path.exists', return_value=True)
    @patch('cna_list.loader.Path.iterdir', return_value=[Path('tests/mock_data/cna1.json')])
    @patch('cna_list.loader.json.load')
    def test_load_with_validation(self, mock_json_load, mock_iterdir, mock_exists, mock_open, mock_get_external_path):
        # Setup
        mock_json_load.side_effect = [cna1]

        # Act
        loader = CNALoader()
        cna = loader['security@apache.org']

        # Assert
        self.assertIsInstance(cna, CNA)  # Check if the loaded object is an instance of CNA


if __name__ == "__main__":
    unittest.main()
