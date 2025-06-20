from flask import Blueprint, request, render_template, jsonify
from rag_model.src.qabot import llm_chain
import logging
logging.basicConfig(level=logging.DEBUG)

askpdf_bp = Blueprint('askpdf', __name__)

@askpdf_bp.route("/askpdf", methods=["GET", "POST"])
def askpdf():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            logging.debug(f"Question: {question}")
            response = llm_chain.invoke({"query": question})
            logging.debug(f"Response: {response}")
            answer = response["result"]
    return render_template("askpdf.html", answer=answer)
