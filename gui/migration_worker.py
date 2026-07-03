"""
migration_worker.py

Runs the migration in a background thread.
"""

from PySide6.QtCore import QThread, Signal

from engine.migration_engine import MigrationEngine
from models.migration_request import MigrationRequest


class MigrationWorker(QThread):

    progress_changed = Signal(int)

    log_message = Signal(str)

    status_changed = Signal(str)

    migration_finished = Signal()

    migration_failed = Signal(str)

    def __init__(self, request: MigrationRequest):

        super().__init__()

        self.request = request

    def run(self):

        try:

            engine = MigrationEngine(

                progress_callback=self.progress_changed.emit,

                log_callback=self.handle_log,

            )

            engine.run(self.request)

            self.migration_finished.emit()

        except Exception as error:

            self.migration_failed.emit(str(error))

    def handle_log(self, message):

        self.log_message.emit(message)

        self.status_changed.emit(message)