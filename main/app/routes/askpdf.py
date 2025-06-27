from flask import Blueprint, request, render_template, jsonify
from rag_model.src.vinallamaQA import llm_chain
from rag_model.src.geminiQA import ask_with_gemini
import logging
logging.basicConfig(level=logging.DEBUG)

askpdf_bp = Blueprint('askpdf', __name__)

@askpdf_bp.route("/askpdf", methods=["GET", "POST"])
def askpdf():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        model = request.form.get("model")
        if question:
            logging.debug(f"Question: {question}")
            if model == "vinallama-7b":
                logging.debug(f"Question: {model}")
                response = llm_chain.invoke({"query": question})
                logging.debug(f"Response: {response}")
            elif model == "gemini-2.0":
                logging.debug(f"Question: {model}")
                response = ask_with_gemini(question)
                logging.debug(f"Response: {response}")
            answer = response["result"]
    return render_template("askpdf.html", answer=answer)
