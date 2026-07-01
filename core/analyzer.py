from collections import Counter


class WorkbookAnalyzer:

    def __init__(self, workbook):
        self.workbook = workbook

    def analyze(self):

        report = {}

        for sheet in self.workbook.sheetnames:

            ws = self.workbook[sheet]

            headers = []

            if ws.max_row >= 1:
                headers = [cell.value for cell in ws[1]]

            non_empty_rows = 0

            data_types = Counter()

            for row in ws.iter_rows(min_row=2, values_only=True):

                if any(cell is not None for cell in row):
                    non_empty_rows += 1

                for cell in row:

                    if cell is not None:
                        data_types[type(cell).__name__] += 1

            report[sheet] = {
                "rows": non_empty_rows,
                "columns": ws.max_column,
                "headers": headers,
                "types": dict(data_types),
            }

        return report