"""
migration_request.py

Contains all information required to perform
a migration.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class MigrationRequest:

    source_file: Path

    template_file: Path

    output_file: Path | None = None

    validate_only: bool = False

    overwrite: bool = False