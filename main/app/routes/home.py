from flask import Blueprint, render_template, request, jsonify # request: lay du lieu tu client gui len, jsonify: chuyen du lieu thanh json
from rag_model.src.qabot import llm_chain # llm_chain: la ham tuong tac vs model de tra loi cau hoi

home_bp = Blueprint('main', __name__)


@home_bp.route("/askpdf", methods=["GET", "POST"])
def askpdf():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        answer = f"Bạn đã hỏi: {question}"  # hoặc gọi model tại đây
    return render_template("askpdf.html", answer=answer)


@home_bp.route("/ask", methods=["POST"])
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
    

@home_bp.route("/")
def base():
    return render_template("base.html")

@home_bp.route("/test")
def test():
    return render_template("test.html")