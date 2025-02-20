# ui/chat_interface.py
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QAction, QMenu,
    QToolBar, QHBoxLayout, QPushButton, QLabel, QProgressBar, QListWidget,
    QListWidgetItem, QStackedWidget, QFrame, QDialog, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from models.model_manager import ModelManager
from models.api_manager import APIManager
from installer.ollama_installer import is_ollama_installed, install_ollama

class InstallOllamaThread(QThread):
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    
    def run(self):
        def callback(message, progress):
            self.update_status.emit(message)
            self.update_progress.emit(progress)
        install_ollama(callback=callback)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setFixedSize(300, 200)  # increased height for API link input
        layout = QVBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setChecked(True)
        layout.addWidget(self.dark_mode_checkbox)
        # API Link input field
        self.api_link_label = QLabel("API Link:")
        layout.addWidget(self.api_link_label)
        self.api_link_input = QLineEdit()
        layout.addWidget(self.api_link_input)
        # Install Ollama button
        self.install_btn = QPushButton("Install Ollama")
        layout.addWidget(self.install_btn)
        self.setLayout(layout)

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set default dark theme
        self.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        self.setWindowTitle("ChatGPT + Ollama")
        self.resize(1000, 700)
        self.model_manager = ModelManager()
        self.api_manager = APIManager()
        self.selected_model = None
        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        self._create_sidebar(main_layout)
        self._create_chat_stack(main_layout)

        central_widget.setLayout(main_layout)

        # Menu for configuration
        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.configure_api)
        self.menuBar().addAction(config_action)
        
        self.update_placeholder()

    def _create_sidebar(self, layout):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        sidebar_layout.setSpacing(5)
        
        new_chat_btn = QPushButton("New Chat")
        new_chat_btn.setStyleSheet("text-align: left; padding: 10px;")
        new_chat_btn.clicked.connect(self.new_chat)
        sidebar_layout.addWidget(new_chat_btn)
        
        history_label = QLabel("Chat History")
        history_label.setStyleSheet("padding: 10px;")
        sidebar_layout.addWidget(history_label)
        self.sidebar_chat_list = QListWidget()
        for chat in ["Chat 1", "Chat 2", "Chat 3"]:
            QListWidgetItem(chat, self.sidebar_chat_list)
        sidebar_layout.addWidget(self.sidebar_chat_list)
        
        proj_layout = QHBoxLayout()
        proj_label = QLabel("Projects")
        proj_label.setStyleSheet("font-size: 10pt; padding: 5px;")
        proj_layout.addWidget(proj_label)
        add_proj_btn = QPushButton("+")
        add_proj_btn.setFixedWidth(30)
        add_proj_btn.clicked.connect(self.add_project)
        proj_layout.addWidget(add_proj_btn)
        sidebar_layout.addLayout(proj_layout)
        self.projetos_list = QListWidget()
        for proj in ["Project A"]:
            QListWidgetItem(proj, self.projetos_list)
        sidebar_layout.addWidget(self.projetos_list)
        
        config_btn = QPushButton("Configuration")
        config_btn.setStyleSheet("text-align: left; padding: 10px;")
        config_btn.clicked.connect(self.configure_api)
        sidebar_layout.addWidget(config_btn)
        
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)
        layout.addWidget(sidebar)

    def _create_chat_stack(self, layout):
        self.chat_stack = QStackedWidget()
        
        # Placeholder page
        self.placeholder = QWidget()
        ph_layout = QVBoxLayout()
        self.instr_label = QLabel("")
        self.instr_label.setAlignment(Qt.AlignCenter)
        ph_layout.addWidget(self.instr_label)
        self.option_layout = QHBoxLayout()
        ph_layout.addLayout(self.option_layout)
        self.placeholder.setLayout(ph_layout)
        self.chat_stack.addWidget(self.placeholder)
        
        # Chat page
        self.chat_area = QWidget()
        chat_layout = QVBoxLayout()
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        chat_layout.addWidget(self.chat_history)
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(send_btn)
        chat_layout.addLayout(input_layout)
        # Installation progress (hidden by default)
        self.install_progress = QProgressBar()
        self.install_progress.setVisible(False)
        self.install_status = QLabel("Installation status: Waiting...")
        self.install_status.setVisible(False)
        chat_layout.addWidget(self.install_progress)
        chat_layout.addWidget(self.install_status)
        self.chat_area.setLayout(chat_layout)
        self.chat_stack.addWidget(self.chat_area)
        
        layout.addWidget(self.chat_stack)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_placeholder(self):
        # Show installation option if Ollama is missing; else allow model selection.
        if not is_ollama_installed():
            self.instr_label.setText("Ollama is not installed.\nClick below to install:")
            self.clear_layout(self.option_layout)
            install_btn = QPushButton("Install Ollama")
            install_btn.clicked.connect(self.install_ollama)
            self.option_layout.addWidget(install_btn)
        else:
            # Ollama installed. Check if models are available.
            models = self.model_manager.get_installed_models()
            if not models:  # No models installed
                self.instr_label.setText("Ollama is installed but not initialized.\nPlease initialize Ollama:")
                self.clear_layout(self.option_layout)
                init_btn = QPushButton("Initialize Ollama")
                init_btn.clicked.connect(self.initialize_ollama)
                self.option_layout.addWidget(init_btn)
            else:
                self.instr_label.setText("Select a model to start:")
                self.clear_layout(self.option_layout)
                self.model_list = QListWidget()
                for model in models:
                    item = QListWidgetItem(model)
                    self.model_list.addItem(item)
                self.model_list.itemClicked.connect(self.select_model)
                self.option_layout.addWidget(self.model_list)
                # Also add API linking option
                api_btn = QPushButton("Link API")
                api_btn.clicked.connect(lambda: self.chat_history.append("[System] Opening API connection..."))
                self.option_layout.addWidget(api_btn)

    def initialize_ollama(self):
        """
        Dummy function to prompt user to manually initialize Ollama.
        In a real app, this should guide the user to complete Ollama initialization.
        """
        self.chat_history.append("[System] Please start Ollama manually to finish initialization.")

    def new_chat(self):
        if not self.selected_model:
            self.chat_stack.setCurrentIndex(0)
            self.update_placeholder()
        else:
            self.chat_stack.setCurrentIndex(1)
            self.chat_history.clear()
            self.chat_history.append(f"[System] New chat started with model: {self.selected_model}")

    def send_message(self):
        message = self.chat_input.text().strip()
        if not message:
            return
        self.chat_history.append(f"You: {message}")
        response = self.process_message(message)
        self.chat_history.append(f"Model ({self.selected_model}): {response}")
        self.chat_input.clear()

    def process_message(self, message: str) -> str:
        return f"Simulated response for '{message}'"

    def select_model(self, item):
        self.selected_model = item.text()
        self.chat_history.append(f"[System] Selected model: {self.selected_model}")
        self.chat_stack.setCurrentIndex(1)
        self.chat_history.append(f"[System] New chat initiated with {self.selected_model}")

    def configure_api(self):
        dlg = ConfigDialog(self)
        dlg.dark_mode_checkbox.stateChanged.connect(self.apply_dark_mode)
        dlg.install_btn.clicked.connect(self.install_ollama)
        dlg.exec_()

    def apply_dark_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        else:
            self.setStyleSheet("")

    def install_ollama(self):
        if is_ollama_installed():
            self.chat_history.append("[System] Ollama is already installed.")
            self.update_placeholder()
        else:
            self.chat_history.append("[System] Installing Ollama...")
            self.install_progress.setVisible(True)
            self.install_status.setVisible(True)
            self.install_progress.setValue(0)
            self.install_thread = InstallOllamaThread()
            self.install_thread.update_status.connect(self.update_installation_status)
            self.install_thread.update_progress.connect(self.install_progress.setValue)
            self.install_thread.start()

    def update_installation_status(self, message):
        self.chat_history.append(f"[System] {message}")
        self.install_status.setText(f"Installation status: {message}")
        if "installed successfully" in message or "Error" in message:
            self.install_progress.setVisible(False)
            self.install_status.setVisible(False)
            self.update_placeholder()

    def add_project(self):
        new_proj = f"Project {self.projetos_list.count() + 1}"
        QListWidgetItem(new_proj, self.projetos_list)
