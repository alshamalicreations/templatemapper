from openpyxl import load_workbook
from core.logger import get_logger

logger = get_logger()


class WorkbookLoader:

    def load(self, path):

        logger.info(f"Loading workbook: {path}")

        workbook = load_workbook(
            filename=path,
            data_only=False
        )

        logger.info("Workbook Loaded Successfully")

        return workbook