"""
transaction.py

Represents a treatment performed for a patient.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Transaction:

    patient_file_number: int

    treatment_name: str

    price: float

    discount_rate: float

    discount_value: float

    payment_type: str

    paid_amount: float

    entry_date: datetime | None