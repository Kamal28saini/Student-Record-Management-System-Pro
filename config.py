
from pathlib import Path

APP_NAME = "Student Record Management System Pro"
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "students.db"

LOG_DIRECTORY = BASE_DIR / "logs"
SCREENSHOT_DIRECTORY = BASE_DIR / "screenshots"

DATABASE_DIR.mkdir(exist_ok=True)
LOG_DIRECTORY.mkdir(exist_ok=True)
SCREENSHOT_DIRECTORY.mkdir(exist_ok=True)

DEFAULT_SEMESTER = 1
MAX_MARKS = 100

MIN_STUDENT_AGE = 16
MAX_STUDENT_AGE = 100

APP_THEME = "clam"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

TABLE_ROW_HEIGHT = 30
