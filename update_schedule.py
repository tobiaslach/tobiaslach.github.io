import requests
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

URL = "https://www.barnim-gymnasium.de/fileadmin/schulen/barnim-gymnasium/Dokumente/Pl%C3%A4ne/splan.pdf"
PASSWORD = "schule"
DEST = "static/splan.pdf"

def download_and_decrypt():
    response = requests.get(URL)
    response.raise_for_status()
    reader = PdfReader(BytesIO(response.content))
    if reader.is_encrypted:
        reader.decrypt(PASSWORD)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(DEST, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    download_and_decrypt()
