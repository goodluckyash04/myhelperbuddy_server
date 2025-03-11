import sys
from loguru import logger
from logtail import LogtailHandler
from pathlib import Path

from app.core.config import settings
from app.utils.date_and_time import date

# Create logs directory if it doesn't exist
LOG_DIR = Path("app/storage/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE_PATH = LOG_DIR / f"{date.get_today_date(include_time=False, as_string=True, date_format="%Y%m%d")}.log"
LOG_FORMAT = ("{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {extra[ip]} | {extra[mac]} | {module} "
              "| {function} | {message}")

LOG_FILE_SIZE = "5 MB"
LOG_FILE_RETENTION = "7 days"
LOG_FILE_LEVEL = "INFO"

LOGTAIL_FORMAT = "{extra}"
LOGTAIL_LOG_LEVEL = "INFO"


logger.remove()

logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                              "<level>{level}</level> | "
                              "<cyan>{module}</cyan> | <cyan>{function}</cyan> | "
                              "<level>{message}</level>",
           level="INFO")

# Send logs to Logtail
logtail_handler = LogtailHandler(source_token=settings.LOGTAIL_SOURCE_TOKEN, host=settings.LOGTAIL_HOST)
logger.add(logtail_handler, serialize=True, format=LOGTAIL_FORMAT, level=LOGTAIL_LOG_LEVEL)

# Save logs locally
# logger.add(LOG_FILE_PATH, format=LOG_FORMAT, rotation=LOG_FILE_SIZE, retention=LOG_FILE_RETENTION, level=LOG_FILE_LEVEL)
