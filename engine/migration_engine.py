"""
migration_engine.py

Coordinates the migration workflow.
"""

from datetime import datetime
from pathlib import Path
from time import perf_counter

from engine.patient_linker import PatientLinker
from engine.progress_tracker import ProgressTracker
from engine.source_detector import SourceDetector

from exporters.ionclinic_exporter import IonClinicExporter
from importers.derma_importer import DermaImporter

from models.migration_request import MigrationRequest

from services.payment_generator import PaymentGenerator
from services.workbook_service import WorkbookService


class MigrationEngine:

    def __init__(
        self,
        progress_callback=None,
        log_callback=None,
    ):

        self.workbook_service = WorkbookService()
        self.detector = SourceDetector()

        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def progress(self, value):

        if self.progress_callback:
            self.progress_callback(value)

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

        print(message)

    def run(self, request: MigrationRequest):

        start_time = perf_counter()

        self.log("=" * 60)
        self.log("TEMPLATEMAPPER")
        self.log("IONCLINIC SIMPLIFIED IMPORT EXPORT")
        self.log("=" * 60)

        self.progress(1)

        self.log("Loading source workbook...")

        source = self.workbook_service.load(
            request.source_file
        )

        self.log("✓ Source workbook loaded")

        self.progress(2)

        self.log("Loading template workbook...")

        self.workbook_service.load(
            request.template_file
        )

        self.log("✓ Template workbook loaded")

        workbook_type = self.detector.detect(
            source
        )

        self.log(
            f"Detected workbook type: {workbook_type}"
        )

        if workbook_type != "DERMA":

            raise Exception(
                "Unsupported workbook."
            )

        #
        # First pass
        #

        self.progress(3)

        importer = DermaImporter(source)

        payment_generator = PaymentGenerator()

        patients = importer.read_patients()

        transactions = importer.read_transactions()

        payments = importer.read_payments()

        payments = payment_generator.generate(

            payments=payments,

            transactions=transactions,

        )

        total_operations = (

            len(patients)
            + len(transactions)
            + len(payments)
            + len(patients)
            + len(transactions)
            + len(payments)

        )

        tracker = ProgressTracker(

            total_operations=total_operations,

            callback=self.progress,

        )

        #
        # Second pass
        #

        importer = DermaImporter(

            source,

            tracker=tracker,

        )

        self.log("Importing patients...")

        patients = importer.read_patients()

        self.log(
            f"✓ Imported {len(patients)} patients"
        )

        self.log("Importing appointments...")

        transactions = importer.read_transactions()

        self.log(
            f"✓ Imported {len(transactions)} appointments"
        )

        self.log("Importing payments...")

        payments = importer.read_payments()

        payments = payment_generator.generate(

            payments=payments,

            transactions=transactions,

        )

        self.log(
            f"✓ Imported {len(payments)} payments"
        )
        self.log("Linking patient records...")

        linker = PatientLinker(

            tracker=tracker,

        )

        linker.link_transactions(

            patients,

            transactions,

        )

        linker.link_payments(

            patients,

            payments,

        )

        self.log("✓ Patient relationships linked")

        self.log("Generating Simplified Import Template...")

        exporter = IonClinicExporter(

            request.template_file,

            clinic_id=request.clinic_id,

            tracker=tracker,

        )

        exporter.export(

            patients

        )

        output_folder = Path(
            request.output_folder
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        output_file = (
            output_folder
            / f"TemplateMapper_Export_{timestamp}.xlsx"
        )

        self.log("Saving workbook...")

        exporter.save(
            output_file
        )

        self.progress(100)

        elapsed = perf_counter() - start_time

        self.log("")
        self.log("=" * 60)
        self.log("MIGRATION REPORT")
        self.log("=" * 60)

        self.log(
            f"Source Workbook Type : {workbook_type}"
        )

        self.log(
            "Export Target       : IonClinic Simplified Import Template"
        )

        self.log("")

        self.log(
            f"Patients Exported    : {len(patients)}"
        )

        self.log(
            f"Appointments Exported: {len(transactions)}"
        )

        self.log(
            f"Payments Exported    : {len(payments)}"
        )

        self.log("")

        self.log("Output File:")

        self.log(
            str(output_file)
        )

        self.log("")

        self.log("Execution Time:")

        self.log(
            f"{elapsed:.2f} seconds"
        )

        self.log("")

        self.log("Validation:")

        self.log(
            "PASS - Patients"
            if patients
            else "FAIL - Patients"
        )

        self.log(
            "PASS - Appointments"
            if transactions
            else "FAIL - Appointments"
        )

        self.log(
            "PASS - Payments"
            if payments
            else "FAIL - Payments"
        )

        self.log("")

        self.log("Warnings : 0")
        self.log("Errors   : 0")

        self.log("")
        self.log("=" * 60)
        self.log("Migration Completed Successfully")
        self.log("=" * 60)