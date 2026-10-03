from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os, logging
from datetime import datetime
from openai import OpenAI

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# OpenAI client
client = OpenAI(api_key="h26wxiLz3ETEw-K8r7HOnRROphhdup4_kLxW6r-m2Mya-RKgH4sxMwbNx3UT3BlbkFJ30lCoA9i6ejtTuY2NOi1VUecpPzWphqO3GrV3fvrKkT-v9bonRGI4xm85eJWSJlOPuHyhNzg4A")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400
        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Only CSV allowed"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        from data_extractor import data_extraction
        result = data_extraction(file_path)

        os.remove(file_path)
        return jsonify({"success": True, "filename": filename, "data": result})
    return render_template("index.html")

@app.route("/ask-gpt", methods=["POST"])
def ask_gpt():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"success": False, "error": "No text"}), 400

    # Truncate prompt to avoid hitting token limit
    if len(text) > 2000:
        text = text[:2000] + "... (truncated)"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an ML assistant. Summarize dataset features briefly, recommend the best model, and provide hyperparameters in separate sections with short answers."},
            {"role": "user", "content": text}
        ],
        max_tokens=500
    )
    reply = response.choices[0].message.content.strip()
    return jsonify({"success": True, "reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
