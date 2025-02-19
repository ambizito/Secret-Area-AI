import sys
from PyQt5.QtWidgets import QApplication
from ui.chat_interface import ChatInterface

def main():
    app = QApplication(sys.argv)
    window = ChatInterface()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
