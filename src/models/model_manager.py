# models/model_manager.py
import os

class ModelManager:
    """
    Manages local and available models.
    """
    def __init__(self):
        self.local_model_dir = os.path.join(os.path.expanduser("~"), ".ollama", "models")
        self._ensure_model_dir()

    def _ensure_model_dir(self):
        if not os.path.exists(self.local_model_dir):
            os.makedirs(self.local_model_dir)

    def get_installed_models(self) -> list:
        """
        Returns list of installed local models.
        """
        self._ensure_model_dir()
        # In a real scenario, scan the folder. Here we simulate.
        return ["modelo_local_1", "modelo_local_2"]

    def get_available_models(self) -> list:
        """
        Returns list of models available for download.
        """
        return ["modelo_download_1", "modelo_download_2"]

    def download_model(self, model_name: str) -> bool:
        """
        Simulates downloading a model.
        """
        try:
            model_path = os.path.join(self.local_model_dir, model_name)
            os.makedirs(model_path, exist_ok=True)
            return True
        except Exception as error:
            print(f"Model download error: {error}")
            return False
