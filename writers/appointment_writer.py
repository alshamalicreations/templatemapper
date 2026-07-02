"""
appointment_writer.py

Writes patient transactions into the
IonClinic appointments worksheet.
"""

from datetime import datetime
from uuid import uuid4


class AppointmentWriter:

    def __init__(self, workbook, tracker=None):

        self.workbook = workbook
        self.sheet = workbook["appointments"]
        self.tracker = tracker

    def write(self, patients):

        now = datetime.now()

        row = self.sheet.max_row + 1

        for patient in patients:

            session_number = 1

            for transaction in patient.transactions:

                self.sheet.cell(row=row, column=1).value = str(uuid4())

                self.sheet.cell(row=row, column=2).value = 1

                self.sheet.cell(row=row, column=3).value = patient.id

                self.sheet.cell(row=row, column=4).value = transaction.entry_date

                self.sheet.cell(row=row, column=5).value = session_number

                self.sheet.cell(row=row, column=6).value = transaction.price

                self.sheet.cell(row=row, column=7).value = "completed"

                self.sheet.cell(row=row, column=8).value = transaction.treatment_name

                self.sheet.cell(row=row, column=9).value = False

                self.sheet.cell(row=row, column=10).value = now

                self.sheet.cell(row=row, column=11).value = now

                self.sheet.cell(row=row, column=12).value = ""

                self.sheet.cell(row=row, column=13).value = ""

                self.sheet.cell(row=row, column=14).value = transaction.treatment_name

                self.sheet.cell(row=row, column=15).value = None

                self.sheet.cell(row=row, column=16).value = None

                row += 1
                session_number += 1

                if self.tracker:
                    self.tracker.advance()

        self._auto_fit()

    def _auto_fit(self):

        for column in self.sheet.columns:

            max_length = 0

            column_letter = column[0].column_letter

            for cell in column:

                try:

                    if cell.value is not None:

                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                except Exception:

                    pass

            self.sheet.column_dimensions[column_letter].width = min(
                max_length + 2,
                40,
            )