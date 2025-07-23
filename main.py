# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui import ModernResolutionChanger

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernResolutionChanger()
    window.show()
    sys.exit(app.exec())
