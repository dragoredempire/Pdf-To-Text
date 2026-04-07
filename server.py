from flask import Flask, request, jsonify
import pytesseract
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Config for file uploads
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file: 
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Perform OCR on the uploaded PDF file
        text = pytesseract.image_to_string(file_path)  # Assuming Tesseract is set up for PDF to image conversion first
        return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)