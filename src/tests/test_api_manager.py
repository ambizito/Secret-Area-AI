import os
import json
import unittest
from models.api_manager import APIManager

class TestAPIManager(unittest.TestCase):
    def setUp(self):
        self.api_manager = APIManager()
        # Backup config if exists
        self.backup = None
        if os.path.exists(self.api_manager.config_file):
            with open(self.api_manager.config_file, "r") as f:
                self.backup = json.load(f)
            os.remove(self.api_manager.config_file)

    def tearDown(self):
        if self.backup is not None:
            with open(self.api_manager.config_file, "w") as f:
                json.dump(self.backup, f)

    def test_add_and_get_api_key(self):
        self.api_manager.add_api_key("TestService", "ABC123")
        key = self.api_manager.get_api_key("TestService")
        self.assertEqual(key, "ABC123")

    def test_edit_api_key(self):
        self.api_manager.add_api_key("TestService", "ABC123")
        self.api_manager.edit_api_key("TestService", "XYZ789")
        key = self.api_manager.get_api_key("TestService")
        self.assertEqual(key, "XYZ789")

if __name__ == '__main__':
    unittest.main()
