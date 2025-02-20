# models/api_manager.py
import json
import os

class APIManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".chat_ollama_api_config.json")
        self.api_keys = self.load_api_keys()

    def load_api_keys(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_api_keys(self):
        with open(self.config_file, "w") as f:
            json.dump(self.api_keys, f, indent=4)

    def add_api_key(self, service_name, key):
        self.api_keys[service_name] = key
        self.save_api_keys()

    def edit_api_key(self, service_name, new_key):
        if service_name in self.api_keys:
            self.api_keys[service_name] = new_key
            self.save_api_keys()

    def get_api_key(self, service_name):
        return self.api_keys.get(service_name, None)

    def validate_api_key(self, service_name, key):
        # Simula a validação da chave de API
        return True

    def get_available_api_models(self):
        # Retorna uma lista de modelos disponíveis via API (simulação)
        return ["OpenAI - GPT-3", "Together AI", "Hugging Face"]
