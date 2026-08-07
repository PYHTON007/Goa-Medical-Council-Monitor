import json
from pathlib import Path

STATE_FOLDER = Path("state")
STATE_FILE = STATE_FOLDER / "monitor_state.json"


def load_state():
    """
    Loads the monitor state.
    If it doesn't exist, returns a default state.
    """

    if not STATE_FILE.exists():
        return {
            "last_hash": "",
            "last_checked": "",
            "pdf_url": "",
            "version": "1.1"
        }

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    """
    Saves the monitor state.
    """

    STATE_FOLDER.mkdir(exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)