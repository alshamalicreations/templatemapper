"""
payment_writer.py

Writes payments into the IonClinic
Simplified Import Template payments worksheet.
"""


PAYMENT_METHOD_MAP = {

    "كاش": "Cash",

    "فيزا": "Visa",

    "بطاقة": "Card",

    "تحويل": "Transfer",

}


class PaymentWriter:

    def __init__(
        self,
        workbook,
        tracker=None,
    ):

        self.workbook = workbook
        self.sheet = workbook["payments"]

        self.tracker = tracker

    def write(self, patients):

        row = 2
        payment_id = 1

        for patient in patients:

            for payment in patient.payments:

                payment_method = PAYMENT_METHOD_MAP.get(
                    str(payment.payment_type).strip(),
                    str(payment.payment_type).strip(),
                )

                # id
                self.sheet.cell(
                    row=row,
                    column=1,
                ).value = payment_id

                # patient_id
                self.sheet.cell(
                    row=row,
                    column=2,
                ).value = patient.id

                # amount
                self.sheet.cell(
                    row=row,
                    column=3,
                ).value = payment.amount

                # discount
                self.sheet.cell(
                    row=row,
                    column=4,
                ).value = payment.discount

                # payment_method
                self.sheet.cell(
                    row=row,
                    column=5,
                ).value = payment_method

                # payment_date
                self.sheet.cell(
                    row=row,
                    column=6,
                ).value = payment.payment_date

                row += 1
                payment_id += 1

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

            self.sheet.column_dimensions[
                letter
            ].width = min(
                max_length + 2,
                40,
            )