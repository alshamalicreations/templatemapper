from pathlib import Path

# ==========================================
# PROJECT PATHS
# ==========================================

ROOT = Path(__file__).resolve().parent

SOURCE_FOLDER = ROOT / "source"
TEMPLATE_FOLDER = ROOT / "templates"
OUTPUT_FOLDER = ROOT / "output"
LOG_FOLDER = ROOT / "logs"
MAPPING_FOLDER = ROOT / "mappings"

# ==========================================
# DEFAULT FILES
# ==========================================

SOURCE_FILE = SOURCE_FOLDER / "Derma class.xlsx"

TEMPLATE_FILE = TEMPLATE_FOLDER / "Full_Backup_Template.xlsx"

OUTPUT_FILE = OUTPUT_FOLDER / "Full_Backup_Migrated.xlsx"

# ==========================================
# APP INFO
# ==========================================

APP_NAME = "Excel Migration Tool"

VERSION = "1.0.0"

AUTHOR = "Rayyan"

# ==========================================
# CREATE FOLDERS
# ==========================================

for folder in [

    SOURCE_FOLDER,

    TEMPLATE_FOLDER,

    OUTPUT_FOLDER,

    LOG_FOLDER,

    MAPPING_FOLDER

]:

    folder.mkdir(exist_ok=True)