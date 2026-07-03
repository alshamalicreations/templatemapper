"""
patient_writer.py

Writes Patient objects into the IonClinic
Simplified Import Template patients worksheet.
"""


class PatientWriter:

    def __init__(
        self,
        workbook,
        tracker=None,
    ):

        self.workbook = workbook
        self.sheet = workbook["patients"]

        self.tracker = tracker

    def write(self, patients):

        row = 2

        for patient in patients:

            self.sheet.cell(row=row, column=1).value = patient.id
            self.sheet.cell(row=row, column=2).value = patient.full_name
            self.sheet.cell(row=row, column=3).value = patient.phone_number
            self.sheet.cell(row=row, column=4).value = patient.birth_date
            self.sheet.cell(row=row, column=5).value = getattr(patient, "notes", "")
            self.sheet.cell(row=row, column=6).value = getattr(patient, "treatment_plan", "")

            row += 1

            if self.tracker:
                self.tracker.advance()

        self._auto_fit()

    def _auto_fit(self):

        for column in self.sheet.columns:

            max_length = 0

            letter = column[0].column_letter

            for cell in column:

                if cell.value is None:
                    continue

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

            self.sheet.column_dimensions[letter].width = min(
                max_length + 2,
                40,
            )