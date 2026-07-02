"""
payment_writer.py

Writes payments into the IonClinic
payments worksheet.
"""

from datetime import datetime
from uuid import uuid4


class PaymentWriter:

    def __init__(self, workbook, tracker=None):

        self.workbook = workbook
        self.sheet = workbook["payments"]
        self.tracker = tracker

    def write(self, patients):

        now = datetime.now()

        row = self.sheet.max_row + 1

        for patient in patients:

            for payment in patient.payments:

                self.sheet.cell(row=row, column=1).value = str(uuid4())

                self.sheet.cell(row=row, column=2).value = 1

                self.sheet.cell(row=row, column=3).value = patient.id

                self.sheet.cell(row=row, column=4).value = payment.amount

                self.sheet.cell(row=row, column=5).value = 0

                self.sheet.cell(row=row, column=6).value = payment.payment_type

                self.sheet.cell(row=row, column=7).value = payment.payment_date

                # appointment_id
                self.sheet.cell(row=row, column=8).value = None

                # session_id
                self.sheet.cell(row=row, column=9).value = None

                # doctor_id
                self.sheet.cell(row=row, column=10).value = None

                # department
                self.sheet.cell(row=row, column=11).value = None

                # status
                self.sheet.cell(row=row, column=12).value = "completed"

                row += 1

                if self.tracker:
                    self.tracker.advance()

        self._auto_fit()

    def _auto_fit(self):

        for column in self.sheet.columns:

            max_length = 0

            letter = column[0].column_letter

            for cell in column:

                if cell.value is not None:

                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

            self.sheet.column_dimensions[letter].width = min(
                max_length + 2,
                40,
            )