"""
excel_reader.py

Reads Excel worksheets and converts rows into
mapped dictionaries.
"""

from openpyxl.workbook.workbook import Workbook

from engine.header_mapper import HeaderMapper


class ExcelReader:

    def __init__(self, workbook: Workbook):

        self.workbook = workbook

    def read_sheet(
        self,
        sheet_name: str,
        mapping: dict[str, str],
    ) -> list[dict]:

        sheet = self.workbook[sheet_name]

        headers = [
            cell.value
            for cell in sheet[1]
        ]

        mapper = HeaderMapper(mapping)

        lookup = mapper.map_headers(headers)

        rows = []

        for row in sheet.iter_rows(
            min_row=2,
            values_only=True,
        ):

            rows.append(
                mapper.map_row(
                    row,
                    lookup,
                )
            )

        return rows