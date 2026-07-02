"""
base_importer.py

Defines the contract that every importer must follow.
"""

from abc import ABC, abstractmethod

from openpyxl.workbook.workbook import Workbook

from models.patient import Patient
from models.transaction import Transaction
from models.payment import Payment


class BaseImporter(ABC):

    def __init__(self, workbook: Workbook):
        self.workbook = workbook

    @abstractmethod
    def read_patients(self) -> list[Patient]:
        raise NotImplementedError

    @abstractmethod
    def read_transactions(self) -> list[Transaction]:
        raise NotImplementedError

    @abstractmethod
    def read_payments(self) -> list[Payment]:
        raise NotImplementedError