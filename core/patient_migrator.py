import uuid
from datetime import datetime

from core.logger import get_logger

logger = get_logger()


class PatientMigrator:

    def __init__(self, source_workbook, template_workbook):

        self.source = source_workbook
        self.template = template_workbook

        self.patient_sheet = self.source["Patient"]
        self.destination_sheet = self.template["patients"]

        self.patient_id_map = {}

    # ---------------------------------------------------
    # Helpers
    # ---------------------------------------------------

    def clean_text(self, value):

        if value is None:
            return ""

        value = str(value)

        # Remove illegal XML characters
        value = value.replace("\x00", "")
        value = value.replace("\x01", "")
        value = value.replace("\x02", "")
        value = value.replace("\x03", "")
        value = value.replace("\x04", "")
        value = value.replace("\x05", "")
        value = value.replace("\x06", "")
        value = value.replace("\x07", "")
        value = value.replace("\x08", "")

        value = value.replace("\t", " ")
        value = value.replace("\n", " ")
        value = value.replace("\r", " ")

        value = value.strip()

        # Prevent Excel Formula Injection
        if value.startswith("="):
            value = "'" + value

        return value

    def clean_phone(self, phone):

        phone = self.clean_text(phone)

        # Limit size
        if len(phone) > 30:
            phone = phone[:30]

        return phone

    # ---------------------------------------------------

    def migrate(self):

        logger.info("Starting Patient Migration...")

        inserted = 0

        now = datetime.now()

        for row in self.patient_sheet.iter_rows(
            min_row=2,
            values_only=True
        ):

            file_number = row[0]

            patient_name = self.clean_text(row[1])

            patient_name_en = self.clean_text(row[2])

            phone = self.clean_phone(row[3])

            sex = self.clean_text(row[4])

            birth_date = row[5]

            if patient_name == "":
                continue

            patient_uuid = str(uuid.uuid4())

            self.patient_id_map[file_number] = patient_uuid

            notes = ""

            if patient_name_en:
                notes += f"English Name: {patient_name_en}"

            if sex:

                if notes:
                    notes += " | "

                notes += f"Gender: {sex}"

            self.destination_sheet.append([

                patient_uuid,                 # id
                1,                            # clinic_id
                patient_name,                 # full_name
                phone,                        # phone_number
                birth_date,                   # birth_date
                notes,                        # notes
                "",                           # treatment_plan
                1,                            # department_id
                0,                            # total_amount
                0,                            # remaining_amount
                now,                          # created_at
                now,                          # updated_at
                1                             # doctor_id

            ])

            inserted += 1

            if inserted % 500 == 0:

                logger.info(
                    f"{inserted} patients migrated..."
                )

        logger.info(
            f"Finished. {inserted} patients inserted."
        )

        return self.patient_id_map