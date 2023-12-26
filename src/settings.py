from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COOKIE_DIR = BASE_DIR.parent / "cookies"
COOKIE_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR = BASE_DIR / "templates"

DEBUG = True
JSON_SORT_KEYS = True

SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
SQLALCHEMY_TRACK_MODIFICATIONS = True
