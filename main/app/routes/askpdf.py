from flask import Blueprint, request, render_template, jsonify
from rag_model.src.qabot import llm_chain

askpdf_bp = Blueprint('askpdf', __name__)

@askpdf_bp.route("/askpdf", methods=["GET", "POST"])
def askpdf():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        answer = f"Bạn đã hỏi: {question}"  # hoặc gọi model tại đây
    return render_template("askpdf.html", answer=answer)


@askpdf_bp.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question' in request"}), 400

        question = data["question"]
        answer = llm_chain.run(question)  # hoặc invoke(question), tuỳ LLM bạn dùng
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
