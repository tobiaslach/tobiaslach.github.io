import requests
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

URL = "https://www.barnim-gymnasium.de/fileadmin/schulen/barnim-gymnasium/Dokumente/Pl%C3%A4ne/splan.pdf"
PASSWORD = "schule"
DEST = "static/splan.pdf"

def download_schedule() -> bytes:
    """Download the schedule PDF with a user agent."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
    return resp.content


def decrypt_and_filter(data: bytes, keyword: str = "7/6") -> bytes:
    """Decrypt the PDF and keep only pages containing the keyword."""
    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        reader.decrypt(PASSWORD)

    writer = PdfWriter()
    for page in reader.pages:
        text = page.extract_text() or ""
        if keyword in text:
            writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def update_schedule():
    data = download_schedule()
    filtered = decrypt_and_filter(data)
    with open(DEST, "wb") as f:
        f.write(filtered)

if __name__ == "__main__":
    update_schedule()
