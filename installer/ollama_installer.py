# installer/ollama_installer.py
import subprocess
import platform
import os

def is_ollama_installed():
    try:
        # Tenta executar "ollama --version" para verificar a instalação
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def install_ollama():
    # Lógica para instalação automática do Ollama (exemplo, a ser aprimorada)
    os_type = platform.system()
    print("Iniciando instalação do Ollama...")
    if os_type == "Windows":
        print("Instalação automática para Windows não implementada. Por favor, instale manualmente.")
    elif os_type == "Linux":
        print("Tentando instalar Ollama no Linux...")
        # Exemplo: executar comandos de instalação (ex.: apt-get)
    elif os_type == "Darwin":
        print("Tentando instalar Ollama no macOS...")
        # Exemplo: utilizar brew para instalação
    else:
        print("Sistema operacional não suportado para instalação automática do Ollama.")

def check_and_install_ollama():
    if not is_ollama_installed():
        print("Ollama não está instalado.")
        install_ollama()
    else:
        print("Ollama já está instalado.")
