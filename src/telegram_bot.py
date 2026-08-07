import requests
from pathlib import Path

from config import BOT_TOKEN, CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(text):
    url = f"{BASE_URL}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
    )

    return response.json()


def send_document(file_path, caption=None):
    url = f"{BASE_URL}/sendDocument"

    with open(file_path, "rb") as document:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption,
                "parse_mode": "HTML"
            },
            files={
                "document": document
            }
        )

    return response.json()


def send_update(text, file_path=None):

    send_message(text)

    if file_path is not None:
        send_document(file_path)