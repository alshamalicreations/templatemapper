from pathlib import Path
from loguru import logger

LOG_FILE = Path("logs/migration.log")

logger.remove()

logger.add(

    LOG_FILE,

    rotation="5 MB",

    retention=10,

    level="INFO",

    encoding="utf-8"

)

logger.add(

    lambda msg: print(msg, end=""),

    level="INFO"

)

def get_logger():

    return logger