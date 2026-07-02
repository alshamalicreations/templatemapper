"""
main.py

Application entry point.
"""

from pathlib import Path

from controllers.migration_controller import MigrationController
from models.migration_request import MigrationRequest


def main():

    print("=" * 50)
    print("IonClinic Excel Tool")
    print("=" * 50)

    print()

    source = Path(
        input("Enter source workbook path: ").strip()
    )

    print()

    template = Path(
        input("Enter template workbook path: ").strip()
    )

    request = MigrationRequest(
        source_file=source,
        template_file=template,
    )

    controller = MigrationController()

    controller.migrate(request)


if __name__ == "__main__":
    main()