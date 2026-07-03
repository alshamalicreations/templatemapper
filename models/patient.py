"""
patient.py

Patient domain model.
"""

from dataclasses import dataclass, field

from models.transaction import Transaction
from models.payment import Payment


@dataclass
class Patient:

    file_number: int

    full_name: str

    full_name_en: str

    phone_number: str

    gender: str

    birth_date: object

    # Assigned by the importer.
    # Default value is overwritten during import.
    id: int = 0

    transactions: list[Transaction] = field(default_factory=list)

    payments: list[Payment] = field(default_factory=list)

    @property
    def total_treatments(self):

        return sum(
            transaction.price
            for transaction in self.transactions
        )

    @property
    def total_paid(self):

        return sum(
            payment.amount
            for payment in self.payments
        )

    @property
    def remaining_balance(self):

        return self.total_treatments - self.total_paid