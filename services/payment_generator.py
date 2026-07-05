"""
payment_generator.py

Generates a unified payment list by combining
payments from Patient Pay with payments inferred
from patient transactions.
"""

from models.payment import Payment


class PaymentGenerator:

    def generate(
        self,
        payments: list[Payment],
        transactions,
    ) -> list[Payment]:

        generated_payments = list(payments)

        seen = set()

        #
        # Register existing Patient Pay records
        #

        for payment in payments:

            key = (

                payment.patient_file_number,

                float(payment.amount),

                float(payment.discount),

                payment.payment_date,

            )

            seen.add(key)

        #
        # Generate payments from transactions
        #

        for transaction in transactions:

            #
            # Skip transactions that have
            # neither payment nor discount.
            #

            if (
                transaction.paid_amount <= 0
                and transaction.discount_value <= 0
            ):
                continue

            key = (

                transaction.patient_file_number,

                float(transaction.paid_amount),

                float(transaction.discount_value),

                transaction.entry_date,

            )

            #
            # Skip duplicate financial events
            #

            if key in seen:
                continue

            generated_payments.append(

                Payment(

                    patient_file_number=transaction.patient_file_number,

                    amount=transaction.paid_amount,

                    discount=transaction.discount_value,

                    payment_type=transaction.payment_type,

                    payment_date=transaction.entry_date,

                    notes="Generated from transaction",

                )

            )

            seen.add(key)

        return generated_payments