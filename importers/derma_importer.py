"""
derma_importer.py

Reads data from a Derma workbook.
"""

from engine.excel_reader import ExcelReader
from importers.base_importer import BaseImporter

from mappings.derma_patient_mapping import PATIENT_MAPPING
from mappings.derma_transaction_mapping import TRANSACTION_MAPPING
from mappings.derma_payment_mapping import PAYMENT_MAPPING

from models.patient import Patient
from models.transaction import Transaction
from models.payment import Payment


class DermaImporter(BaseImporter):

    def __init__(
        self,
        workbook,
        tracker=None,
    ):

        super().__init__(
            workbook,
            tracker,
        )

        self.reader = ExcelReader(workbook)

    def read_patients(self) -> list[Patient]:

        rows = self.reader.read_sheet(
            "Patient",
            PATIENT_MAPPING,
        )

        patients = []

        patient_id = 1

        for row in rows:

            patients.append(

                Patient(

                    id=patient_id,

                    file_number=row.get("file_number"),

                    full_name=row.get("full_name", ""),

                    full_name_en=row.get("full_name_en", ""),

                    phone_number=str(
                        row.get("phone_number", "")
                    ),

                    gender=row.get("gender", ""),

                    birth_date=row.get("birth_date"),

                )

            )

            patient_id += 1

            self.advance_progress()

        return patients

    def read_transactions(self) -> list[Transaction]:

        rows = self.reader.read_sheet(
            "Patient Trans",
            TRANSACTION_MAPPING,
        )

        transactions = []

        for row in rows:

            transactions.append(

                Transaction(

                    patient_file_number=row.get(
                        "patient_file_number"
                    ),

                    treatment_name=row.get(
                        "treatment_name",
                        "",
                    ),

                    price=float(
                        row.get("price") or 0
                    ),

                    discount_rate=float(
                        row.get("discount_rate") or 0
                    ),

                    discount_value=float(
                        row.get("discount_value") or 0
                    ),

                    payment_type=row.get(
                        "payment_type",
                        "",
                    ),

                    paid_amount=float(
                        row.get("paid_amount") or 0
                    ),

                    entry_date=row.get(
                        "entry_date"
                    ),

                )

            )

            self.advance_progress()

        return transactions

    def read_payments(self) -> list[Payment]:

        rows = self.reader.read_sheet(
            "Patient Pay",
            PAYMENT_MAPPING,
        )

        payments = []

        for row in rows:

            payments.append(

                Payment(

                    patient_file_number=row.get(
                        "patient_file_number"
                    ),

                    amount=float(
                        row.get("amount") or 0
                    ),

                    payment_type=row.get(
                        "payment_type",
                        "",
                    ),

                    payment_date=row.get(
                        "payment_date"
                    ),

                    notes=row.get(
                        "notes",
                        "",
                    ),

                )

            )

            self.advance_progress()

        return payments