"""
migration_engine.py

Coordinates the migration workflow.
"""

from engine.patient_linker import PatientLinker
from engine.source_detector import SourceDetector
from engine.workbook_analyzer import WorkbookAnalyzer

from importers.derma_importer import DermaImporter

from models.migration_request import MigrationRequest

from services.workbook_service import WorkbookService


class MigrationEngine:

    def __init__(self):

        self.workbook_service = WorkbookService()
        self.analyzer = WorkbookAnalyzer()
        self.detector = SourceDetector()

    def run(self, request: MigrationRequest):

        print()

        print("Loading source workbook...")
        source = self.workbook_service.load(request.source_file)
        print("✓ Source workbook loaded")

        print()

        print("Loading template workbook...")
        self.workbook_service.load(request.template_file)
        print("✓ Template workbook loaded")

        print()

        workbook_type = self.detector.detect(source)

        print(f"Detected workbook: {workbook_type}")

        print()

        if workbook_type != "DERMA":
            print("Unsupported workbook.")
            return

        importer = DermaImporter(source)

        # ---------------------------------------
        # Import Data
        # ---------------------------------------

        patients = importer.read_patients()
        print(f"✓ Imported {len(patients)} patients")

        transactions = importer.read_transactions()
        print(f"✓ Imported {len(transactions)} transactions")

        payments = importer.read_payments()
        print(f"✓ Imported {len(payments)} payments")

        # ---------------------------------------
        # Link Data
        # ---------------------------------------

        linker = PatientLinker()

        linker.link_transactions(
            patients,
            transactions,
        )

        linker.link_payments(
            patients,
            payments,
        )

        # ---------------------------------------
        # Debug Information
        # ---------------------------------------

        print()
        print("=" * 60)
        print("Patients With Payments")
        print("=" * 60)

        found = 0

        for patient in patients:

            if len(patient.payments) == 0:
                continue

            print(f"Patient        : {patient.full_name}")
            print(f"File Number    : {patient.file_number}")
            print(f"Transactions   : {len(patient.transactions)}")
            print(f"Payments       : {len(patient.payments)}")
            print(f"Total Paid     : {patient.total_paid:.2f}")
            print(f"Treatments     : {patient.total_treatments:.2f}")
            print(f"Balance        : {patient.remaining_balance:.2f}")

            print("-" * 60)

            found += 1

            if found == 5:
                break

        if found == 0:
            print("No linked payments were found.")
            print()
            print("Debug:")
            print(
                f"First patient file number: {patients[0].file_number} ({type(patients[0].file_number).__name__})"
            )
            print(
                f"First payment file number: {payments[0].patient_file_number} ({type(payments[0].patient_file_number).__name__})"
            )

        print()
        print("Migration Engine Finished.")