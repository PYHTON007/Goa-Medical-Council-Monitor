from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SEND_STATUS_IF_NO_CHANGE = True
SEND_PDF_ON_CHANGE = True
SEND_SUMMARY = True 