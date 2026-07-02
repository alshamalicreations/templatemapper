"""
derma_importer.py

Reads patients from a Derma workbook.
"""

from models.patient import Patient
from importers.base_importer import BaseImporter
from engine.header_mapper import HeaderMapper
from mappings.derma_patient_mapping import PATIENT_MAPPING


class DermaImporter(BaseImporter):

    def __init__(self, workbook):

        super().__init__(workbook)

        self.mapper = HeaderMapper(PATIENT_MAPPING)

    def read_patients(self) -> list[Patient]:

        sheet = self.workbook["Patient"]

        patients: list[Patient] = []

        # Read the Excel header row
        headers = [cell.value for cell in sheet[1]]

        # Build the lookup table
        header_lookup = self.mapper.map_headers(headers)

        # Read every patient row
        for row in sheet.iter_rows(min_row=2, values_only=True):

            data = self.mapper.map_row(row, header_lookup)

            patient = Patient(

                file_number=data.get("file_number"),

                full_name=data.get("full_name", ""),

                full_name_en=data.get("full_name_en", ""),

                phone_number=str(data.get("phone_number", "")),

                gender=data.get("gender", ""),

                birth_date=data.get("birth_date"),

            )

            patients.append(patient)

        return patients