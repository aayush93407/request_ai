from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from io import BytesIO
from PyPDF2 import PdfReader

app = FastAPI()

class URLResponse(BaseModel):
    urls: list[str]

def extract_urls_from_pdf(pdf_file: BytesIO):
    """Extract URLs from the PDF."""
    reader = PdfReader(pdf_file)
    urls = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            for line in text.split("\n"):
                if line.startswith("http://") or line.startswith("https://"):
                    urls.append(line.strip())
    return urls

@app.post("/upload-pdf", response_model=URLResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Receive PDF, extract URLs, and send them back."""
    try:
        pdf_file = BytesIO(await file.read())
        urls = extract_urls_from_pdf(pdf_file)
        return URLResponse(urls=urls if urls else [])
    except Exception as e:
        return {"message": str(e)}