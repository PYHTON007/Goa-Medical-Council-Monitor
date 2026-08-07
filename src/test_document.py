from pathlib import Path

from telegram_bot import send_update

pdf = Path("data/pdfs/fmg_crmi_internship.pdf")

send_update(
    "📄 Testing PDF upload from Goa Medical Council Monitor",
    pdf
)