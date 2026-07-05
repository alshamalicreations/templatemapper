"""
appointment_writer.py

Writes patient appointments into the IonClinic
Simplified Import Template appointments worksheet.
"""


class AppointmentWriter:

    def __init__(
        self,
        workbook,
        tracker=None,
    ):

        self.workbook = workbook
        self.sheet = workbook["appointments"]

        self.tracker = tracker

    def write(self, patients):

        row = 2
        appointment_id = 1

        for patient in patients:

            session_number = 1

            for transaction in patient.transactions:

                # Calculate net price after discount
                appointment_price = (
                    transaction.price
                    - transaction.discount_value
                )

                # Prevent negative values
                if appointment_price < 0:
                    appointment_price = 0

                # id
                self.sheet.cell(row=row, column=1).value = appointment_id

                # patient_id
                self.sheet.cell(row=row, column=2).value = patient.id

                # appointment_datetime
                self.sheet.cell(row=row, column=3).value = (
                    transaction.entry_date
                )

                # session_number
                self.sheet.cell(row=row, column=4).value = session_number

                # price (after discount)
                self.sheet.cell(row=row, column=5).value = (
                    appointment_price
                )

                # status
                self.sheet.cell(row=row, column=6).value = "completed"

                # doctor_notes
                self.sheet.cell(row=row, column=7).value = (
                    transaction.treatment_name
                )

                row += 1
                appointment_id += 1
                session_number += 1

                if self.tracker:
                    self.tracker.advance()

        self._auto_fit()

    def _auto_fit(self):

        for column in self.sheet.columns:

            max_length = 0

            column_letter = column[0].column_letter

            for cell in column:

                if cell.value is None:
                    continue

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

            self.sheet.column_dimensions[column_letter].width = min(
                max_length + 2,
                40,
            )