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

/* ---------------- Labels ---------------- */

QLabel {
    color: #E8EAED;
    font-size: 9pt;
}

/* ---------------- Line Edits ---------------- */

QLineEdit {
    background-color: #2B2D31;
    border: 1px solid #3C4043;
    border-radius: 8px;

    padding: 4px 10px;

    color: white;

    font-size: 9pt;

    selection-background-color: #4F8EF7;
}

QLineEdit:focus {
    border: 1px solid #4F8EF7;
}

/* ---------------- Buttons ---------------- */

QPushButton {

    background-color: #4F8EF7;

    color: white;

    border: none;

    border-radius: 8px;

    padding: 6px 14px;

    font-size: 9pt;

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

/* ---------------- CheckBox ---------------- */

QCheckBox {

    spacing: 8px;

    font-size: 9pt;

}

QCheckBox::indicator {

    width: 15px;

    height: 15px;

    border: 2px solid white;

    border-radius: 3px;

    background-color: transparent;

}

QCheckBox::indicator:hover {

    border: 2px solid #66A3FF;

}

QCheckBox::indicator:checked {

    background-color: white;

    border: 2px solid white;

}

/* ---------------- Text Edit ---------------- */

QTextEdit {

    background-color: #2B2D31;

    border: 1px solid #3C4043;

    border-radius: 8px;

    padding: 8px;

    color: white;

}

/* ---------------- Progress Bar ---------------- */

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

/* ---------------- Scroll Bars ---------------- */

QScrollBar:vertical {

    background: #2B2D31;

    width: 10px;

    margin: 0px;

    border-radius: 5px;

}

QScrollBar::handle:vertical {

    background: #4F8EF7;

    min-height: 30px;

    border-radius: 5px;

}

QScrollBar::handle:vertical:hover {

    background: #66A3FF;

}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {

    height: 0px;

}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {

    background: none;

}
"""