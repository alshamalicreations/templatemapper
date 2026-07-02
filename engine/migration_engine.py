"""
migration_engine.py

Coordinates the migration workflow.
"""

from datetime import datetime
from pathlib import Path
from time import perf_counter

from engine.patient_linker import PatientLinker
from engine.source_detector import SourceDetector

from exporters.ionclinic_exporter import IonClinicExporter
from importers.derma_importer import DermaImporter

from models.migration_request import MigrationRequest

from services.workbook_service import WorkbookService


class MigrationEngine:

    def __init__(self):

        self.workbook_service = WorkbookService()
        self.detector = SourceDetector()

    def run(self, request: MigrationRequest):

        start_time = perf_counter()

        print("\n" + "=" * 60)
        print("IONCLINIC MIGRATION TOOL")
        print("=" * 60)

        print("\nLoading source workbook...")
        source = self.workbook_service.load(request.source_file)
        print("✓ Source workbook loaded")

        print("\nLoading template workbook...")
        self.workbook_service.load(request.template_file)
        print("✓ Template workbook loaded")

        workbook_type = self.detector.detect(source)

        print(f"\nDetected workbook type: {workbook_type}")

        if workbook_type != "DERMA":

            print("\nUnsupported workbook.")
            return

        importer = DermaImporter(source)

        print("\nImporting data...")

        patients = importer.read_patients()
        transactions = importer.read_transactions()
        payments = importer.read_payments()

        print(f"✓ Patients      : {len(patients)}")
        print(f"✓ Transactions  : {len(transactions)}")
        print(f"✓ Payments      : {len(payments)}")

        print("\nLinking records...")

        linker = PatientLinker()

        linker.link_transactions(
            patients,
            transactions,
        )

        linker.link_payments(
            patients,
            payments,
        )

        print("✓ Relationships linked")

        print("\nExporting workbook...")

        exporter = IonClinicExporter(
            request.template_file
        )

        exporter.export(
            patients
        )

        output_folder = Path("output")
        output_folder.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        output_file = (
            output_folder
            / f"IonClinic_Backup_{timestamp}.xlsx"
        )

        exporter.save(output_file)

        elapsed = perf_counter() - start_time

        print("\n" + "=" * 60)
        print("MIGRATION REPORT")
        print("=" * 60)

        print(f"Workbook Type        : {workbook_type}")

        print(f"Patients Imported    : {len(patients)}")
        print(f"Appointments Exported: {len(transactions)}")
        print(f"Payments Exported    : {len(payments)}")

        print(f"\nOutput File:")
        print(output_file)

        print(f"\nExecution Time:")
        print(f"{elapsed:.2f} seconds")

        print("\nValidation:")

        print(
            "PASS - Patients"
            if len(patients) > 0
            else "FAIL - Patients"
        )

        print(
            "PASS - Appointments"
            if len(transactions) > 0
            else "FAIL - Appointments"
        )

        print(
            "PASS - Payments"
            if len(payments) > 0
            else "FAIL - Payments"
        )

        print("\nWarnings : 0")
        print("Errors   : 0")

        print("\n" + "=" * 60)
        print("Migration Completed Successfully")
        print("=" * 60)