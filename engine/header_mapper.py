"""
header_mapper.py

Maps Excel rows into internal dictionaries
using a configurable column mapping.
"""


class HeaderMapper:

    def __init__(self, mapping: dict[str, str]):

        self.mapping = mapping

    def map_headers(self, headers: list) -> dict[int, str]:
        """
        Build a lookup table from column index
        to internal field name.
        """

        lookup = {}

        for index, header in enumerate(headers):

            if header in self.mapping:

                lookup[index] = self.mapping[header]

        return lookup

    def map_row(
        self,
        row: tuple,
        header_lookup: dict[int, str],
    ) -> dict:

        data = {}

        for index, value in enumerate(row):

            if index in header_lookup:

                field = header_lookup[index]

                data[field] = value

        return data