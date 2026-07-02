"""
ionclinic_exporter.py

Exports clinic data into an IonClinic Backup workbook.
"""

from pathlib import Path

from openpyxl import load_workbook

from writers.patient_writer import PatientWriter
from writers.appointment_writer import AppointmentWriter
from writers.payment_writer import PaymentWriter


class IonClinicExporter:

    def __init__(
        self,
        template_path: str,
        tracker=None,
    ):

        self.template_path = Path(template_path)

        self.workbook = load_workbook(self.template_path)

        self.tracker = tracker

    def export_patients(self, patients):

        PatientWriter(
            self.workbook,
            self.tracker,
        ).write(patients)

    def export_appointments(self, patients):

        AppointmentWriter(
            self.workbook,
            self.tracker,
        ).write(patients)

    def export_payments(self, patients):

        PaymentWriter(
            self.workbook,
            self.tracker,
        ).write(patients)

    def export(self, patients):

        print("Writing patients...")
        self.export_patients(patients)
        print("✓ Patients exported")

        print()

        print("Writing appointments...")
        self.export_appointments(patients)
        print("✓ Appointments exported")

        print()

        print("Writing payments...")
        self.export_payments(patients)
        print("✓ Payments exported")

    def save(self, output_path: str):

        self.workbook.save(output_path)