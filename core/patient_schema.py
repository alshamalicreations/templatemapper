from openpyxl.worksheet.worksheet import Worksheet


def print_patient_schema(sheet: Worksheet):

    print()
    print("=" * 70)
    print("PATIENTS DESTINATION SCHEMA")
    print("=" * 70)

    headers = []

    for cell in sheet[1]:
        headers.append(cell.value)

    for index, header in enumerate(headers, start=1):
        print(f"{index:02d}. {header}")