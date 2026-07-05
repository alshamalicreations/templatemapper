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

    discount: float = 0.0

    payment_type: str = ""

    payment_date: datetime | None = None

    notes: str = ""