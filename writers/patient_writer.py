"""
patient_writer.py

Writes Patient objects into the IonClinic
patients worksheet.
"""

from datetime import datetime


class PatientWriter:

    def __init__(self, workbook):

        self.workbook = workbook
        self.sheet = workbook["patients"]

    def write(self, patients):

        now = datetime.now()

        row = self.sheet.max_row + 1

        for patient in patients:

            self.sheet.cell(row=row, column=1).value = patient.id
            self.sheet.cell(row=row, column=2).value = 1
            self.sheet.cell(row=row, column=3).value = patient.full_name
            self.sheet.cell(row=row, column=4).value = patient.phone_number
            self.sheet.cell(row=row, column=5).value = patient.birth_date
            self.sheet.cell(row=row, column=6).value = ""
            self.sheet.cell(row=row, column=7).value = ""
            self.sheet.cell(row=row, column=8).value = None
            self.sheet.cell(row=row, column=9).value = patient.total_treatments
            self.sheet.cell(row=row, column=10).value = patient.remaining_balance
            self.sheet.cell(row=row, column=11).value = now
            self.sheet.cell(row=row, column=12).value = now
            self.sheet.cell(row=row, column=13).value = None

            row += 1

        self._auto_fit()

    def _auto_fit(self):

        for column in self.sheet.columns:

            length = 0

            letter = column[0].column_letter

            for cell in column:

                if cell.value is None:
                    continue

                length = max(length, len(str(cell.value)))

            self.sheet.column_dimensions[letter].width = min(
                length + 2,
                40,
            )