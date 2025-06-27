from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for
from rag_model.src.rag_utils import create_db_from_files
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

home_bp = Blueprint('home', __name__)
PDF_FOLDER = os.path.join("rag_model", "src", "data")
os.makedirs(PDF_FOLDER, exist_ok=True) 


def upload_pdf():
    if 'pdf_file' not in request.files:
        return redirect(url_for("home.home"))
    
    file = request.files['pdf_file']
    if file.filename == '':
        return redirect(url_for("home.home"))
    
    if file.filename.endswith('.pdf'):
        file.save(os.path.join(PDF_FOLDER, file.filename))

    return redirect(url_for("home.home"))


@home_bp.route("/pdfs/<path:filename>")
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)


@home_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return upload_pdf()

    # GET
    files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    return render_template("home.html", pdf_files=files)


@home_bp.route("/delete-pdf", methods=["POST"])
def delete_pdf():
    filename = request.form.get("filename")
    if not filename:
        return redirect(url_for("home.home"))

    file_path = os.path.join(PDF_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect(url_for("home.home"))

@home_bp.route("/prepare_vectordb", methods=["POST"])
def prepare_vectordb():
    try:
        # from rag_model.src.rag_utils import create_db_from_files
        create_db_from_files()
        logger.info("VectorDB đã được chuẩn bị thành công.")
    except Exception as e:
        logger.error(f"Lỗi khi chuẩn bị VectorDB: {e}")
    return redirect(url_for("home.home"))

