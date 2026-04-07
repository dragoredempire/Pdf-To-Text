# Pdf-To-Text (Web OCR)

A simple Flask website that accepts one PDF file, runs OCR on each page, and shows extracted text in the browser.

## Features
- Upload one PDF from the web UI.
- OCR extraction using **Tesseract**.
- Page rendering from PDF using **PyMuPDF**.
- Extracted text is shown directly on the same page.

## Requirements
- Python 3.10+
- Tesseract OCR installed in your OS
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - macOS (Homebrew): `brew install tesseract`

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python server.py
```

Open: `http://127.0.0.1:5000`

## Notes
- This app performs OCR (image-based text extraction), so it works for scanned PDFs.
- Uploaded files are removed after processing.
