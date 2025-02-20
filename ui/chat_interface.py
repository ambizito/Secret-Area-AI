# ui/chat_interface.py
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QAction, QMenu, QToolBar, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from models.model_manager import ModelManager
from models.api_manager import APIManager

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatGPT + Ollama")
        self.resize(800, 600)
        self.model_manager = ModelManager()
        self.api_manager = APIManager()
        self.initUI()
    
    def initUI(self):
        # Cria o menu de seleção de modelos
        self.create_model_menu()

        # Interface principal: histórico do chat e área de entrada de mensagem
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Área de histórico de conversas
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        # Área de entrada e botão de envio
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)

        central_widget.setLayout(layout)

        # Toolbar para alternar entre modos de exibição
        toolbar = QToolBar("Configurações")
        self.addToolBar(toolbar)
        dark_mode_action = QAction("Modo Escuro", self)
        dark_mode_action.setCheckable(True)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        toolbar.addAction(dark_mode_action)

    def create_model_menu(self):
        menubar = self.menuBar()
        model_menu = menubar.addMenu("Modelos")

        # Submenu: Modelos Locais (Ollama)
        local_menu = QMenu("Modelos Locais (Ollama)", self)
        installed_models = self.model_manager.get_installed_models()
        for model in installed_models:
            action = QAction(model, self)
            action.triggered.connect(lambda checked, m=model: self.select_model(m))
            local_menu.addAction(action)
            
        # Submenu: Modelos Disponíveis para Download
        download_menu = QMenu("Modelos Disponíveis para Download", self)
        available_models = self.model_manager.get_available_models()
        for model in available_models:
            action = QAction(model, self)
            action.triggered.connect(lambda checked, m=model: self.download_model(m))
            download_menu.addAction(action)
            
        model_menu.addMenu(local_menu)
        model_menu.addMenu(download_menu)

        # Submenu: Modelos via API
        api_menu = QMenu("Modelos via API", self)
        api_models = self.api_manager.get_available_api_models()
        for model in api_models:
            action = QAction(model, self)
            action.triggered.connect(lambda checked, m=model: self.select_api_model(m))
            api_menu.addAction(action)
        model_menu.addMenu(api_menu)

        # Opção: Configuração de APIs
        config_api_action = QAction("Configurar APIs", self)
        config_api_action.triggered.connect(self.configure_api)
        model_menu.addAction(config_api_action)

    def send_message(self):
        message = self.chat_input.text()
        if message.strip() == "":
            return
        # Exibe a mensagem enviada
        self.chat_history.append(f"Você: {message}")
        # Aqui seria realizada a chamada real ao modelo selecionado
        response = self.process_message(message)
        self.chat_history.append(f"Modelo: {response}")
        self.chat_input.clear()

    def process_message(self, message):
        # Placeholder para integração com o modelo selecionado
        return f"Resposta simulada para '{message}'"

    def select_model(self, model_name):
        # Seleciona modelo local
        self.chat_history.append(f"[Sistema] Modelo local selecionado: {model_name}")

    def download_model(self, model_name):
        # Inicia o download do modelo
        success = self.model_manager.download_model(model_name)
        if success:
            self.chat_history.append(f"[Sistema] Modelo {model_name} baixado com sucesso!")
        else:
            self.chat_history.append(f"[Sistema] Falha ao baixar o modelo {model_name}.")

    def select_api_model(self, model_name):
        # Seleciona modelo via API
        self.chat_history.append(f"[Sistema] Modelo via API selecionado: {model_name}")

    def configure_api(self):
        # Abre a interface de configuração das APIs (pode ser uma nova janela)
        self.chat_history.append("[Sistema] Abrindo configurações de API...")

    def toggle_dark_mode(self, checked):
        if checked:
            # Aplica tema escuro
            self.setStyleSheet("background-color: #2e2e2e; color: #f0f0f0;")
        else:
            # Restaura tema padrão
            self.setStyleSheet("")
