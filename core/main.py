# core/main.py

import sys
from PyQt5.QtWidgets import QApplication
from main_window import GUIApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUIApp()
    window.show()
    sys.exit(app.exec_())
