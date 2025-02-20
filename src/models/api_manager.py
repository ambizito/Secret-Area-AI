# models/api_manager.py
import json
import os

class APIManager:
    """
    Handles API key storage and retrieval.
    """
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".chat_ollama_api_config.json")
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self) -> dict:
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {}

    def _save_api_keys(self) -> None:
        with open(self.config_file, "w") as f:
            json.dump(self.api_keys, f, indent=4)

    def add_api_key(self, service_name: str, key: str) -> None:
        self.api_keys[service_name] = key
        self._save_api_keys()

    def edit_api_key(self, service_name: str, new_key: str) -> None:
        if service_name in self.api_keys:
            self.api_keys[service_name] = new_key
            self._save_api_keys()

    def get_api_key(self, service_name: str) -> str:
        return self.api_keys.get(service_name, "")

    def validate_api_key(self, service_name: str, key: str) -> bool:
        # Here, simulate API key validation.
        return True

    def get_available_api_models(self) -> list:
        return ["OpenAI - GPT-3", "Together AI", "Hugging Face"]
