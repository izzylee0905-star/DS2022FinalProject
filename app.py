from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"ok": False, "error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"ok": False, "error": "No file selected"})
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}-{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    url = f"/{file_path}"  # relative URL for static file
    return jsonify({"ok": True, "url": url})

@app.route('/api/v1/gallery', methods=['GET'])
def gallery():
    files = sorted(os.listdir(UPLOAD_FOLDER))
    urls = [f"/{UPLOAD_FOLDER}/{file}" for file in files]
    return jsonify({"ok": True, "gallery": urls})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

