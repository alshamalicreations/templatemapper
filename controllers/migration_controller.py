"""
migration_controller.py

Receives commands from the GUI
and starts the migration.
"""

from engine.migration_engine import MigrationEngine
from models.migration_request import MigrationRequest


class MigrationController:

    def __init__(self):
        self.engine = MigrationEngine()

    def migrate(self, request: MigrationRequest):

        self.engine.run(request)