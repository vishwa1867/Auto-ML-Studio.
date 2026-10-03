from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, logging
import pandas as pd
from process import process_file  # updated import

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

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    cleaned_file_link = None
    preview = None

    if request.method == "POST":
        if "file" not in request.files:
            message = "❌ No file uploaded"
        else:
            file = request.files["file"]
            if file.filename == "" or not allowed_file(file.filename):
                message = "❌ Only CSV files allowed"
            else:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                try:
                    # Use the new function name
                    cleaned_file_path = process_file(file_path)
                    if cleaned_file_path:
                        message = "✅ File cleaned successfully!"
                        cleaned_file_link = cleaned_file_path

                        # Optional: preview first 5 rows
                        df = pd.read_csv(cleaned_file_path)
                        preview = df.head().to_html(classes="table table-striped", index=False)
                    else:
                        message = "❌ Failed to clean file"
                except Exception as e:
                    logger.error("Error processing file:", exc_info=True)
                    message = f"❌ Error: {e}"

                # Optional: remove original uploaded file
                os.remove(file_path)

    return render_template("index.html", message=message, cleaned_file_link=cleaned_file_link, preview=preview)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
