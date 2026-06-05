import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

QUESTIONS_FILE = DATA_DIR / "questions.json"
WRONG_FILE = DATA_DIR / "wrong_questions.json"
FAVORITES_FILE = DATA_DIR / "favorites.json"
RECORDS_FILE = DATA_DIR / "records.json"


def ensure_data_files():
    """Create required data files if they do not exist.

    The project uses local JSON files instead of a database. This helper makes
    the CLI more robust when someone clones the repo and runs it directly.
    """
    DATA_DIR.mkdir(exist_ok=True)
    defaults = {
        QUESTIONS_FILE: [],
        WRONG_FILE: [],
        FAVORITES_FILE: [],
        RECORDS_FILE: [],
    }
    for path, value in defaults.items():
        if not path.exists():
            save_json(path, value)


def load_json(path, default=None):
    """Load JSON data from a file.

    Args:
        path: Target JSON file path.
        default: Value returned when the file is missing or invalid.
    """
    if default is None:
        default = []
    try:
        with Path(path).open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    """Save JSON data with readable formatting."""
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_questions():
    return load_json(QUESTIONS_FILE, [])


def load_wrong_questions():
    return load_json(WRONG_FILE, [])


def save_wrong_questions(data):
    save_json(WRONG_FILE, data)


def load_favorites():
    return load_json(FAVORITES_FILE, [])


def save_favorites(data):
    save_json(FAVORITES_FILE, data)


def load_records():
    return load_json(RECORDS_FILE, [])


def save_records(data):
    save_json(RECORDS_FILE, data)
