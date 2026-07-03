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
    QCheckBox,
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

        #
        # Header
        #

        title = QLabel("TemplateMapper")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            QLabel{
                font-size:30px;
                font-weight:bold;
            }
        """)

        subtitle = QLabel(
            "Universal Excel Migration Tool"
        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            QLabel{
                font-size:12px;
                color:#9AA0A6;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)

        layout.addWidget(separator)

        #
        # Input Section
        #

        grid = QGridLayout()

        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)

        #
        # Labels
        #

        source_label = QLabel("Source Workbook")
        template_label = QLabel("Template Workbook")
        output_label = QLabel("Output Folder")

        source_label.setMinimumWidth(140)
        template_label.setMinimumWidth(140)
        output_label.setMinimumWidth(140)

        #
        # Textboxes
        #

        self.source_edit = QLineEdit()
        self.source_edit.setReadOnly(True)

        self.template_edit = QLineEdit()
        self.template_edit.setReadOnly(True)

        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)

        #
        # Browse Buttons
        #

        self.source_button = QPushButton("Browse")
        self.template_button = QPushButton("Browse")
        self.output_button = QPushButton("Browse")

        self.source_button.setFixedWidth(110)
        self.template_button.setFixedWidth(110)
        self.output_button.setFixedWidth(110)

        self.source_button.setMinimumHeight(36)
        self.template_button.setMinimumHeight(36)
        self.output_button.setMinimumHeight(36)

        self.source_button.clicked.connect(
            self.select_source
        )

        self.template_button.clicked.connect(
            self.select_template
        )

        self.output_button.clicked.connect(
            self.select_output
        )

        #
        # Source
        #

        grid.addWidget(
            source_label,
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

        #
        # Template
        #

        grid.addWidget(
            template_label,
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

        #
        # Output
        #

        grid.addWidget(
            output_label,
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

        #
        # Optional Clinic ID
        #

        self.use_clinic_id_checkbox = QCheckBox(
            "Specify Clinic ID"
        )

        self.use_clinic_id_checkbox.toggled.connect(
            self.toggle_clinic_id
        )

        grid.addWidget(
            self.use_clinic_id_checkbox,
            3,
            0,
            1,
            3,
        )

        self.clinic_id_label = QLabel(
            "Clinic ID"
        )

        self.clinic_id_edit = QLineEdit()

        self.clinic_id_edit.setPlaceholderText(
            "Enter Clinic ID"
        )

        self.clinic_id_label.hide()
        self.clinic_id_edit.hide()

        grid.addWidget(
            self.clinic_id_label,
            4,
            0,
        )

        grid.addWidget(
            self.clinic_id_edit,
            4,
            1,
            1,
            2,
        )

        layout.addLayout(grid)
                #
        # Start Button
        #

        self.start_button = QPushButton(
            "Start Migration"
        )

        self.start_button.setMinimumHeight(48)

        self.start_button.clicked.connect(
            self.start_migration
        )

        layout.addWidget(
            self.start_button
        )

        #
        # Separator
        #

        separator2 = QFrame()

        separator2.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(separator2)

        #
        # Progress
        #

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

        layout.addLayout(
            stats
        )

        #
        # Separator
        #

        separator3 = QFrame()

        separator3.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(separator3)

        #
        # Log
        #

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

    #
    # UI Helpers
    #

    def toggle_clinic_id(self, checked):

        self.clinic_id_label.setVisible(
            checked
        )

        self.clinic_id_edit.setVisible(
            checked
        )

        if not checked:

            self.clinic_id_edit.clear()

    #
    # Migration
    #

    def start_migration(self):

        source = self.source_edit.text().strip()

        template = self.template_edit.text().strip()

        output = self.output_edit.text().strip()

        clinic_id = None

        if self.use_clinic_id_checkbox.isChecked():

            clinic_id = self.clinic_id_edit.text().strip()

            if not clinic_id:

                QMessageBox.warning(
                    self,
                    "Missing Clinic ID",
                    "Please enter a Clinic ID or uncheck 'Specify Clinic ID'.",
                )

                return

        if not source or not template or not output:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select the source workbook, template workbook, and output folder.",
            )

            return

        request = MigrationRequest(

            source_file=source,

            template_file=template,

            output_folder=output,

            clinic_id=clinic_id,

        )

        self.start_button.setEnabled(False)

        self.start_button.setText(
            "Migrating..."
        )

        self.source_button.setEnabled(False)
        self.template_button.setEnabled(False)
        self.output_button.setEnabled(False)

        self.use_clinic_id_checkbox.setEnabled(
            False
        )

        self.clinic_id_edit.setEnabled(
            False
        )

        self.progress.setValue(0)

        self.records_label.setText(
            "-- / --"
        )

        self.status_label.setText(
            "Starting migration..."
        )

        self.eta_label.setText(
            "--:--"
        )

        self.log.clear()

        self.worker = MigrationWorker(
            request
        )

        self.worker.progress_changed.connect(
            self.update_progress
        )

        self.worker.log_message.connect(
            self.update_log
        )

        if hasattr(
            self.worker,
            "status_changed",
        ):

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
            #
    # Progress & Log
    #

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

    #
    # Migration Results
    #

    def migration_finished(self):

        self.progress.setValue(100)

        self.status_label.setText(
            "Completed"
        )

        self.eta_label.setText(
            "00:00"
        )

        self.start_button.setEnabled(True)

        self.start_button.setText(
            "Start Migration"
        )

        self.source_button.setEnabled(True)
        self.template_button.setEnabled(True)
        self.output_button.setEnabled(True)

        self.use_clinic_id_checkbox.setEnabled(
            True
        )

        if self.use_clinic_id_checkbox.isChecked():

            self.clinic_id_edit.setEnabled(
                True
            )

        QMessageBox.information(

            self,

            "Migration Completed",

            "Migration completed successfully!",

        )

    def migration_failed(self, message):

        self.start_button.setEnabled(True)

        self.start_button.setText(
            "Start Migration"
        )

        self.source_button.setEnabled(True)
        self.template_button.setEnabled(True)
        self.output_button.setEnabled(True)

        self.use_clinic_id_checkbox.setEnabled(
            True
        )

        if self.use_clinic_id_checkbox.isChecked():

            self.clinic_id_edit.setEnabled(
                True
            )

        self.status_label.setText(
            "Failed"
        )

        QMessageBox.critical(

            self,

            "Migration Failed",

            message,

        )

    #
    # Browse Dialogs
    #

    def select_source(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Select Source Workbook",

            "",

            "Excel Files (*.xlsx *.xls)",

        )

        if file:

            self.source_edit.setText(
                file
            )

    def select_template(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Select Template Workbook",

            "",

            "Excel Files (*.xlsx)",

        )

        if file:

            self.template_edit.setText(
                file
            )

    def select_output(self):

        folder = QFileDialog.getExistingDirectory(

            self,

            "Select Output Folder",

        )

        if folder:

            self.output_edit.setText(
                folder
            )