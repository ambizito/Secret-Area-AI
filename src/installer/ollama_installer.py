import subprocess
import platform
import os
import urllib.request
import ssl

def is_ollama_installed() -> bool:
    """
    Checks if Ollama is installed by using the 'where' command on Windows.
    This will return True if Ollama is found in the system PATH.
    """
    if platform.system() == "Windows":
        try:
            result = subprocess.run("where ollama", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode().strip()
            return bool(output)
        except Exception:
            return False
    else:
        return False

def install_ollama(callback=None) -> None:
    """
    Download and silently install Ollama on Windows.
    The callback, if provided, accepts (message: str, progress: int).
    """
    os_type = platform.system()
    print("Starting Ollama installation...")
    if os_type == "Windows":
        try:
            url = "https://ollama.com/download/OllamaSetup.exe"
            installer_path = os.path.join(os.getenv("TEMP"), "ollama_installer.exe")
            ssl._create_default_https_context = ssl._create_unverified_context

            def reporthook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
                if callback:
                    callback("Downloading Ollama...", min(percent, 100))

            urllib.request.urlretrieve(url, installer_path, reporthook)
            if callback:
                callback("Download complete. Installing...", 50)
            subprocess.run([installer_path, "/S"], check=True)
            if callback:
                callback("Ollama installed successfully on Windows.", 100)
            print("Ollama installed successfully on Windows.")
        except Exception as error:
            if callback:
                callback(f"Error installing Ollama on Windows: {error}", 0)
            print(f"Error installing Ollama on Windows: {error}")
    else:
        if callback:
            callback("OS not supported for automatic installation.", 0)
        print("OS not supported for automatic installation.")

def check_and_install_ollama():
    if not is_ollama_installed():
        print("Ollama not installed.")
        install_ollama()
    else:
        print("Ollama is already installed.")
