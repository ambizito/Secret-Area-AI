# models/model_manager.py
import os

class ModelManager:
    def __init__(self):
        # Diretório onde os modelos do Ollama são armazenados
        self.local_model_dir = os.path.join(os.path.expanduser("~"), ".ollama", "models")
    
    def get_installed_models(self):
        # Retorna uma lista de modelos instalados localmente (exemplo de simulação)
        if not os.path.exists(self.local_model_dir):
            os.makedirs(self.local_model_dir)
        return ["modelo_local_1", "modelo_local_2"]

    def get_available_models(self):
        # Retorna uma lista de modelos disponíveis para download (simulação)
        return ["modelo_download_1", "modelo_download_2"]

    def download_model(self, model_name):
        # Simula o download do modelo (integração real deve se comunicar com o Ollama)
        try:
            model_path = os.path.join(self.local_model_dir, model_name)
            os.makedirs(model_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Erro ao baixar modelo: {e}")
            return False
