"""
main_window.py

Main GUI window.
"""

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
)

from gui.styles import STYLE
from gui.migration_worker import MigrationWorker
from models.migration_request import MigrationRequest


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.worker = None

        self.setWindowTitle("IonClinic Migration Tool")

        self.resize(850, 600)

        self.setStyleSheet(STYLE)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        grid = QGridLayout()

        self.source_edit = QLineEdit()
        self.source_edit.setReadOnly(True)

        self.template_edit = QLineEdit()
        self.template_edit.setReadOnly(True)

        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)

        source_button = QPushButton("Browse")
        template_button = QPushButton("Browse")
        output_button = QPushButton("Browse")

        source_button.clicked.connect(self.select_source)
        template_button.clicked.connect(self.select_template)
        output_button.clicked.connect(self.select_output)

        grid.addWidget(QLabel("Source Workbook"), 0, 0)
        grid.addWidget(self.source_edit, 0, 1)
        grid.addWidget(source_button, 0, 2)

        grid.addWidget(QLabel("Template Workbook"), 1, 0)
        grid.addWidget(self.template_edit, 1, 1)
        grid.addWidget(template_button, 1, 2)

        grid.addWidget(QLabel("Output Folder"), 2, 0)
        grid.addWidget(self.output_edit, 2, 1)
        grid.addWidget(output_button, 2, 2)

        layout.addLayout(grid)

        self.start_button = QPushButton("Start Migration")
        self.start_button.clicked.connect(
            self.start_migration
        )

        layout.addWidget(self.start_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.append("Ready.")

        layout.addWidget(self.log)

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
        self.start_button.setText("Migrating...")

        self.progress.setValue(0)

        self.log.clear()

        self.worker = MigrationWorker(request)

        self.worker.progress_changed.connect(
            self.progress.setValue
        )

        self.worker.log_message.connect(
            self.log.append
        )

        self.worker.migration_finished.connect(
            self.migration_finished
        )

        self.worker.migration_failed.connect(
            self.migration_failed
        )

        self.worker.start()

    def migration_finished(self):

        self.start_button.setEnabled(True)

        self.start_button.setText(
            "Start Migration"
        )

        QMessageBox.information(
            self,
            "Success",
            "Migration completed successfully!",
        )

    def migration_failed(self, message):

        self.start_button.setEnabled(True)

        self.start_button.setText(
            "Start Migration"
        )

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