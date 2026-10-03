from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os, logging
import pandas as pd
from ml_engine import train_model
from process import process_file  # your CSV cleaning function

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= CSV Upload & Clean =================
@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Only CSV files allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        cleaned_file_path = process_file(file_path)
        df = pd.read_csv(cleaned_file_path)
        preview_html = df.head().to_html(classes="table table-striped", index=False)

        # Remove original uploaded file
        os.remove(file_path)

        return jsonify({
            "message": "File cleaned successfully",
            "cleaned_file_link": cleaned_file_path,
            "preview": preview_html
        })
    except Exception as e:
        logger.error("Error cleaning file:", exc_info=True)
        return jsonify({"error": str(e)}), 500

# ================= Train ML Model =================
@app.route("/train-model", methods=["POST"])
def train_model_route():
    try:
        data = request.get_json()
        file_path = data.get("file_path")
        model_choice = data.get("model_choice")
        if not file_path or not model_choice:
            return jsonify({"error": "Missing parameters"}), 400

        metrics = train_model(file_path, model_choice)
        return jsonify(metrics), 200
    except Exception as e:
        logger.error("Error training model:", exc_info=True)
        return jsonify({"error": str(e)}), 500

# ================= Run Flask App =================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
