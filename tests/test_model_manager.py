# tests/test_model_manager.py
import unittest
import os
from models.model_manager import ModelManager

class TestModelManager(unittest.TestCase):
    def setUp(self):
        self.manager = ModelManager()

    def test_get_installed_models(self):
        models = self.manager.get_installed_models()
        self.assertIsInstance(models, list)
        self.assertGreaterEqual(len(models), 0)

    def test_download_model(self):
        model_name = "teste_modelo"
        result = self.manager.download_model(model_name)
        self.assertTrue(result)
        model_path = os.path.join(self.manager.local_model_dir, model_name)
        self.assertTrue(os.path.exists(model_path))
        # Remove o diretório criado para o teste
        if os.path.exists(model_path):
            os.rmdir(model_path)

if __name__ == '__main__':
    unittest.main()
