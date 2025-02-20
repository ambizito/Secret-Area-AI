# tests/test_model_manager.py
import os
import unittest
from models.model_manager import ModelManager

class TestModelManager(unittest.TestCase):
    def setUp(self):
        self.manager = ModelManager()

    def test_get_installed_models_returns_list(self):
        models = self.manager.get_installed_models()
        self.assertIsInstance(models, list)

    def test_download_model_creates_directory(self):
        model_name = "test_model"
        success = self.manager.download_model(model_name)
        self.assertTrue(success)
        model_path = os.path.join(self.manager.local_model_dir, model_name)
        self.assertTrue(os.path.exists(model_path))
        # Cleanup
        if os.path.exists(model_path):
            os.rmdir(model_path)

if __name__ == '__main__':
    unittest.main()
