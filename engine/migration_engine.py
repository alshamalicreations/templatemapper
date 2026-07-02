from engine.source_detector import SourceDetector
from engine.workbook_analyzer import WorkbookAnalyzer
from services.workbook_service import WorkbookService

from models.migration_request import MigrationRequest


class MigrationEngine:

    def __init__(self):

        self.workbook_service = WorkbookService()
        self.analyzer = WorkbookAnalyzer()
        self.detector = SourceDetector()

    def run(self, request: MigrationRequest):

        print()

        print("Loading source workbook...")

        source = self.workbook_service.load(
            request.source_file
        )

        print("✓ Source workbook loaded")

        print()

        print("Loading template workbook...")

        template = self.workbook_service.load(
            request.template_file
        )

        print("✓ Template workbook loaded")

        print()

        print("Analyzing source workbook...")

        report = self.analyzer.analyze(source)

        print("✓ Analysis complete")

        print()

        print("Detecting workbook type...")

        workbook_type = self.detector.detect(source)

        print(f"✓ Detected: {workbook_type}")

        print()

        print("=" * 60)
        print("Workbook Summary")
        print("=" * 60)

        for sheet, info in report.items():

            print()
            print(sheet)
            print("-" * 40)
            print(f"Rows     : {info['rows']}")
            print(f"Columns  : {info['columns']}")
            print(f"Headers  : {', '.join(map(str, info['headers']))}")

        print()
        print("Migration Engine Finished.")