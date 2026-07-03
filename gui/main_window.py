"""
main_window.py

Main GUI window.
"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QVBoxLayout,
    QFrame,
)

from gui.styles import STYLE
from gui.migration_worker import MigrationWorker
from models.migration_request import MigrationRequest


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.worker = None

        self.setWindowTitle("TemplateMapper")

        self.setWindowIcon(
            QIcon("assets/icons/app_icon.ico")
        )

        self.resize(980, 720)

        self.setMinimumSize(900, 650)

        self.setStyleSheet(STYLE)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30,
            25,
            30,
            25,
        )

        layout.setSpacing(20)

        title = QLabel(
            "TemplateMapper"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            QLabel{
                font-size:30px;
                font-weight:bold;
            }
        """)

        subtitle = QLabel(
            "Universal Excel Migration Tool"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet("""
            QLabel{
                font-size:12px;
                color:#9AA0A6;
            }
        """)

        layout.addWidget(title)

        layout.addWidget(subtitle)

        line = QFrame()

        line.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(line)

        grid = QGridLayout()

        grid.setHorizontalSpacing(15)

        grid.setVerticalSpacing(15)

        self.source_edit = QLineEdit()
        self.source_edit.setReadOnly(True)

        self.template_edit = QLineEdit()
        self.template_edit.setReadOnly(True)

        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)

        self.source_button = QPushButton("Browse")
        self.template_button = QPushButton("Browse")
        self.output_button = QPushButton("Browse")

        self.source_button.clicked.connect(
            self.select_source
        )

        self.template_button.clicked.connect(
            self.select_template
        )

        self.output_button.clicked.connect(
            self.select_output
        )
        grid.addWidget(
            QLabel("Source Workbook"),
            0,
            0,
        )

        grid.addWidget(
            self.source_edit,
            0,
            1,
        )

        grid.addWidget(
            self.source_button,
            0,
            2,
        )

        grid.addWidget(
            QLabel("Template Workbook"),
            1,
            0,
        )

        grid.addWidget(
            self.template_edit,
            1,
            1,
        )

        grid.addWidget(
            self.template_button,
            1,
            2,
        )

        grid.addWidget(
            QLabel("Output Folder"),
            2,
            0,
        )

        grid.addWidget(
            self.output_edit,
            2,
            1,
        )

        grid.addWidget(
            self.output_button,
            2,
            2,
        )

        layout.addLayout(grid)

        self.start_button = QPushButton(
            "🚀 Start Migration"
        )

        self.start_button.setMinimumHeight(48)

        self.start_button.clicked.connect(
            self.start_migration
        )

        layout.addWidget(
            self.start_button
        )

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(separator)

        progress_title = QLabel(
            "Migration Progress"
        )

        progress_title.setStyleSheet("""
            QLabel{
                font-size:14px;
                font-weight:bold;
            }
        """)

        layout.addWidget(
            progress_title
        )

        self.progress = QProgressBar()

        self.progress.setValue(0)

        layout.addWidget(
            self.progress
        )

        stats = QGridLayout()

        stats.setHorizontalSpacing(50)

        stats.setVerticalSpacing(8)

        stats.addWidget(
            QLabel("Records Processed"),
            0,
            0,
        )

        self.records_label = QLabel(
            "0 / 0"
        )

        stats.addWidget(
            self.records_label,
            1,
            0,
        )

        stats.addWidget(
            QLabel("Current Status"),
            0,
            1,
        )

        self.status_label = QLabel(
            "Ready"
        )

        stats.addWidget(
            self.status_label,
            1,
            1,
        )

        stats.addWidget(
            QLabel("Estimated Time"),
            0,
            2,
        )

        self.eta_label = QLabel(
            "--:--"
        )

        stats.addWidget(
            self.eta_label,
            1,
            2,
        )

        layout.addLayout(stats)

        separator2 = QFrame()

        separator2.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(separator2)

        log_title = QLabel(
            "Migration Log"
        )

        log_title.setStyleSheet("""
            QLabel{
                font-size:14px;
                font-weight:bold;
            }
        """)

        layout.addWidget(
            log_title
        )

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        self.log.append(
            "Ready."
        )

        layout.addWidget(
            self.log,
            1,
        )

        self.setLayout(layout)
    def start_migration(self):

        source = self.source_edit.text().strip()
        template = self.template_edit.text().strip()
        output = self.output_edit.text().strip()

        if not source or not template or not output:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select all required paths.",
            )

            return

        request = MigrationRequest(
            source_file=source,
            template_file=template,
            output_folder=output,
        )

        self.start_button.setEnabled(False)
        self.start_button.setText("⏳ Migrating...")

        self.source_button.setEnabled(False)
        self.template_button.setEnabled(False)
        self.output_button.setEnabled(False)

        self.progress.setValue(0)

        self.records_label.setText("-- / --")
        self.status_label.setText("Starting migration...")
        self.eta_label.setText("--:--")

        self.log.clear()

        self.worker = MigrationWorker(request)

        self.worker.progress_changed.connect(
            self.update_progress
        )

        self.worker.log_message.connect(
            self.update_log
        )

        if hasattr(self.worker, "status_changed"):
            self.worker.status_changed.connect(
                self.status_label.setText
            )

        self.worker.migration_finished.connect(
            self.migration_finished
        )

        self.worker.migration_failed.connect(
            self.migration_failed
        )

        self.worker.start()

    def update_progress(self, value):

        self.progress.setValue(value)

    def update_log(self, message):

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        if message.startswith("="):

            self.log.append(message)

        elif message == "":

            self.log.append("")

        else:

            self.log.append(
                f"[{timestamp}] {message}"
            )

        scrollbar = self.log.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def migration_finished(self):

        self.progress.setValue(100)

        self.status_label.setText("Completed")

        self.eta_label.setText("00:00")

        self.start_button.setEnabled(True)
        self.start_button.setText("🚀 Start Migration")

        self.source_button.setEnabled(True)
        self.template_button.setEnabled(True)
        self.output_button.setEnabled(True)

        QMessageBox.information(
            self,
            "Migration Completed",
            "Migration completed successfully!",
        )

    def migration_failed(self, message):

        self.start_button.setEnabled(True)
        self.start_button.setText("🚀 Start Migration")

        self.source_button.setEnabled(True)
        self.template_button.setEnabled(True)
        self.output_button.setEnabled(True)

        self.status_label.setText("Failed")

        QMessageBox.critical(
            self,
            "Migration Failed",
            message,
        )

    def select_source(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Source Workbook",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if file:

            self.source_edit.setText(file)

    def select_template(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template Workbook",
            "",
            "Excel Files (*.xlsx)",
        )

        if file:

            self.template_edit.setText(file)

    def select_output(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
        )

        if folder:

            self.output_edit.setText(folder)