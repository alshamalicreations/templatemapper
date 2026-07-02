"""
patient_linker.py

Links transactions and payments to patients.
"""

from models.patient import Patient
from models.transaction import Transaction
from models.payment import Payment


class PatientLinker:

    def _normalize_key(self, value):

        if value is None:
            return None

        return str(value).strip()

    def build_index(
        self,
        patients: list[Patient],
    ) -> dict[str, Patient]:

        index = {}

        for patient in patients:

            key = self._normalize_key(patient.file_number)

            index[key] = patient

        return index

    def link_transactions(
        self,
        patients: list[Patient],
        transactions: list[Transaction],
    ):

        index = self.build_index(patients)

        for transaction in transactions:

            key = self._normalize_key(
                transaction.patient_file_number
            )

            patient = index.get(key)

            if patient:

                patient.transactions.append(transaction)

    def link_payments(
        self,
        patients: list[Patient],
        payments: list[Payment],
    ):

        index = self.build_index(patients)

        for payment in payments:

            key = self._normalize_key(
                payment.patient_file_number
            )

            patient = index.get(key)

            if patient:

                patient.payments.append(payment)