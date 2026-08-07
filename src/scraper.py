from pathlib import Path
from datetime import datetime
import shutil

import requests
from bs4 import BeautifulSoup

from pdf_utils import sha256

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

    print("\nDownloaded newest PDF as temp.pdf")

    if not current_pdf.exists():

        shutil.move(temp_pdf, current_pdf)

        print("First PDF saved.")

        return True, current_pdf

    old_hash = sha256(current_pdf)
    new_hash = sha256(temp_pdf)

    print(f"\nOld Hash: {old_hash}")
    print(f"New Hash: {new_hash}")

    if old_hash == new_hash:

        temp_pdf.unlink()

        print("\n✅ PDF has NOT changed.")

        return False, current_pdf

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    archive_copy = ARCHIVE_FOLDER / f"{timestamp}_fmg_crmi_internship.pdf"

    shutil.copy2(current_pdf, archive_copy)

    shutil.move(temp_pdf, current_pdf)

    print("\n🚨 PDF HAS CHANGED!")

    return True, current_pdf