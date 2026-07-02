"""
patient.py

Represents a patient independently of any
Excel workbook or clinic system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from models.transaction import Transaction
from models.payment import Payment


@dataclass(slots=True)
class Patient:
    """
    Represents one patient.
    """

    file_number: int
    full_name: str
    full_name_en: str
    phone_number: str
    gender: str
    birth_date: Optional[date]

    transactions: list[Transaction] = field(default_factory=list)
    payments: list[Payment] = field(default_factory=list)

    @property
    def total_paid(self) -> float:
        return sum(payment.amount for payment in self.payments)

    @property
    def total_treatments(self) -> float:
        return sum(transaction.price for transaction in self.transactions)

    @property
    def remaining_balance(self) -> float:
        return self.total_treatments - self.total_paid