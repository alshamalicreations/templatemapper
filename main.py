"""
main.py

Application entry point.
"""

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    # Global application icon
    app.setWindowIcon(
        QIcon("assets/icons/app_icon.ico")
    )

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()