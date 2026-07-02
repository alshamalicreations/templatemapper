"""
payment.py

Represents a payment made by a patient.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Payment:

    patient_file_number: int

    amount: float

    payment_type: str

    payment_date: datetime | None

    notes: str