"""
styles.py

Application stylesheet.
"""

STYLE = """
QWidget {
    background-color: #202124;
    color: #E8EAED;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QLabel {
    color: #E8EAED;
    font-size: 10pt;
}

QLineEdit {
    background-color: #2B2D31;
    border: 1px solid #3C4043;
    border-radius: 8px;
    padding: 8px;
    color: white;
    selection-background-color: #4F8EF7;
}

QLineEdit:focus {
    border: 1px solid #4F8EF7;
}

QPushButton {
    background-color: #4F8EF7;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    font-size: 10pt;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #66A3FF;
}

QPushButton:pressed {
    background-color: #3D78D8;
}

QPushButton:disabled {
    background-color: #555555;
    color: #BBBBBB;
}

QTextEdit {
    background-color: #2B2D31;
    border: 1px solid #3C4043;
    border-radius: 8px;
    padding: 8px;
    color: white;
}

QProgressBar {
    border: 1px solid #3C4043;
    border-radius: 8px;
    text-align: center;
    background-color: #2B2D31;
    height: 22px;
}

QProgressBar::chunk {
    border-radius: 8px;
    background-color: #4F8EF7;
}
"""