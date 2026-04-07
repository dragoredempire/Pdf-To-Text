from __future__ import annotations

import io
import os
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from flask import Flask, jsonify, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_with_ocr(pdf_path: Path) -> str:
    """Render each PDF page as an image and run OCR with Tesseract."""
    extracted_pages: list[str] = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(image_bytes))
            page_text = pytesseract.image_to_string(image).strip()
            extracted_pages.append(page_text)

    return "\n\n".join(text for text in extracted_pages if text)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/upload")
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request."}), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400

    safe_name = secure_filename(uploaded_file.filename)
    save_path = Path(app.config["UPLOAD_FOLDER"]) / safe_name
    uploaded_file.save(save_path)

    try:
        text = extract_text_with_ocr(save_path)
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": f"OCR failed: {exc}"}), 500
    finally:
        if save_path.exists():
            os.remove(save_path)

    if not text:
        text = "No text detected by OCR."

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(debug=True)
