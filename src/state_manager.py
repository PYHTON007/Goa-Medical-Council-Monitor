import json
import os

STATE_FILE = "state/monitor_state.json"
HISTORY_FILE = "state/monitor_history.json"


def load_state():
    """Load the saved monitor state."""

    if not os.path.exists(STATE_FILE):
        return {
            "last_hash": None
        }

    try:

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:

        return {
            "last_hash": None
        }


def save_state(state):
    """Save monitor state."""

    os.makedirs(
        os.path.dirname(STATE_FILE),
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )


def load_history():
    """Load monitor history."""

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            history = json.load(f)

            if isinstance(history, list):
                return history

            return []

    except Exception:

        return []


def save_history(history):
    """Save monitor history."""

    os.makedirs(
        os.path.dirname(HISTORY_FILE),
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )