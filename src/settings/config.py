from os import getenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROD = getenv('PROD')
if PROD is None:
    import dotenv
    dotenv.load_dotenv(BASE_DIR / ".env")

LOG_LEVEL = int(getenv("LOG_LEVEL"))
BOT_TOKEN = getenv("BOT_TOKEN")
SQLITE_PATH = getenv("SQLITE_PATH", BASE_DIR / 'technesis.sqlite3')
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_DB = getenv("REDIS_DB")
SELENIUM_HOST = getenv("SELENIUM_HOST")
SELENIUM_PORT = getenv("SELENIUM_PORT")

EXCEL_EXTENSIONS = {".xlsx", ".xls"}
HTTP_SESSION_TIMEOUT = 15
