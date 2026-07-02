"""
Detects the source software.
"""


class SourceDetector:

    def detect(self, workbook):

        sheets = set(workbook.sheetnames)

        if {
            "Patient",
            "Patient Trans",
            "Patient Pay",
        }.issubset(sheets):

            return "DERMA"

        return "UNKNOWN"