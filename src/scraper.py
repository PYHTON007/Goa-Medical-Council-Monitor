from pathlib import Path
import shutil

import requests
from bs4 import BeautifulSoup

from pdf_utils import sha256
from state_manager import load_state, save_state

BASE_URL = "https://www.goamedicalcouncil.com"

DATA_FOLDER = Path("data")
PDF_FOLDER = DATA_FOLDER / "pdfs"
ARCHIVE_FOLDER = PDF_FOLDER / "archive"

DATA_FOLDER.mkdir(exist_ok=True)
PDF_FOLDER.mkdir(exist_ok=True)
ARCHIVE_FOLDER.mkdir(exist_ok=True)

homepage_file = DATA_FOLDER / "homepage.html"


def download_homepage():
    response = requests.get(BASE_URL, timeout=30)
    response.raise_for_status()

    homepage_file.write_text(
        response.text,
        encoding="utf-8"
    )

    return response.text


def find_pdf_link(html):
    soup = BeautifulSoup(html, "lxml")

    for link in soup.find_all("a"):

        text = link.get_text(strip=True)

        if text.lower() == "fmg crmi internship":

            href = link.get("href")

            if href.startswith("http"):
                return href

            return BASE_URL + "/" + href.lstrip("/")

    return None


def download_pdf(pdf_url):

    response = requests.get(pdf_url, timeout=30)
    response.raise_for_status()

    temp_pdf = PDF_FOLDER / "temp.pdf"
    current_pdf = PDF_FOLDER / "fmg_crmi_internship.pdf"

    temp_pdf.write_bytes(response.content)

    new_hash = sha256(temp_pdf)

    state = load_state()
    old_hash = state.get("last_hash", "")

    print(f"\nOld Hash : {old_hash}")
    print(f"New Hash : {new_hash}")

    # First ever run
    if old_hash == "":

        shutil.move(temp_pdf, current_pdf)

        state["last_hash"] = new_hash
        state["pdf_url"] = pdf_url

        save_state(state)

        print("\nFirst run completed.")

        return True, current_pdf

    # No changes
    if old_hash == new_hash:

        temp_pdf.unlink()

        print("\n✅ PDF has NOT changed.")

        return False, current_pdf

    # PDF changed

    if current_pdf.exists():

        archive_copy = ARCHIVE_FOLDER / current_pdf.name

        shutil.copy2(current_pdf, archive_copy)

    shutil.move(temp_pdf, current_pdf)

    state["last_hash"] = new_hash
    state["pdf_url"] = pdf_url

    save_state(state)

    print("\n🚨 PDF HAS CHANGED!")

    return True, current_pdf