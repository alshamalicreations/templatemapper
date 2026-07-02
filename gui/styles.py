"""
styles.py

Application stylesheet.
"""

STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: white;
    font-size: 10pt;
    font-family: Segoe UI;
}

QLabel {
    font-size: 10pt;
}

QLineEdit {
    background: #2d2d30;
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    padding: 6px;
    color: white;
}

QPushButton {
    background-color: #0078D7;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2893ff;
}

QPushButton:pressed {
    background-color: #005fa3;
}

QProgressBar {
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #0078D7;
}

QTextEdit {
    background: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    color: white;
}
"""