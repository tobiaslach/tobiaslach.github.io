import logging
from io import BytesIO

import requests
from PyPDF2 import PdfReader, PdfWriter


URL = "https://www.barnim-gymnasium.de/fileadmin/schulen/barnim-gymnasium/Dokumente/Pl%C3%A4ne/splan.pdf"
PASSWORD = "schule"
DEST = "static/splan.pdf"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def download_schedule() -> bytes:
    """Download the schedule PDF with a user agent."""
    logging.info("Downloading schedule from %s", URL)
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
    logging.info("Download successful: %d bytes", len(resp.content))
    return resp.content


KEYWORDS = ["7/6", "Klassenleiter(in): Herz"]


def decrypt_and_filter(data: bytes) -> bytes:
    """Decrypt the PDF and keep only pages containing all KEYWORDS."""
    logging.info("Decrypting and filtering pages containing %s", KEYWORDS)

    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        reader.decrypt(PASSWORD)

    writer = PdfWriter()
    pages_added = 0
    for page in reader.pages:
        text = page.extract_text() or ""
        if all(k in text for k in KEYWORDS):
            writer.add_page(page)
            pages_added += 1

    output = BytesIO()
    writer.write(output)
    logging.info("Extracted %d page(s) matching keywords", pages_added)

    return output.getvalue()


def update_schedule():
    logging.info("Starting schedule update")

    data = download_schedule()
    filtered = decrypt_and_filter(data)
    with open(DEST, "wb") as f:
        f.write(filtered)
    logging.info("Saved filtered schedule to %s", DEST)

if __name__ == "__main__":
    update_schedule()
