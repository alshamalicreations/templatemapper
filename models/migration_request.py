"""
migration_request.py

Contains the information required
to perform a migration.
"""

from dataclasses import dataclass


@dataclass
class MigrationRequest:

    source_file: str

    template_file: str

    output_folder: str