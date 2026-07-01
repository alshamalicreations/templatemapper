from config import *
from core.workbook import WorkbookLoader
from core.logger import get_logger
from core.patient_schema import print_patient_schema
from core.patient_migrator import PatientMigrator

logger = get_logger()


def banner():
    print()
    print("=" * 60)
    print(APP_NAME)
    print(f"Version : {VERSION}")
    print("=" * 60)
    print()


def main():

    banner()

    loader = WorkbookLoader()

    source = loader.load(SOURCE_FILE)
    template = loader.load(TEMPLATE_FILE)

    print("\nSource Sheets")
    for sheet in source.sheetnames:
        print(f" • {sheet}")

    print("\nTemplate Sheets")
    for sheet in template.sheetnames:
        print(f" • {sheet}")

    patient_sheet = template["patients"]

    print_patient_schema(patient_sheet)

    migrator = PatientMigrator(
        source,
        template
    )

    patient_map = migrator.migrate()

    template.save(OUTPUT_FILE)

    logger.info("Workbook Saved Successfully")

    logger.info(
        f"Migration Complete ({len(patient_map)} patients)"
    )


if __name__ == "__main__":
    main()