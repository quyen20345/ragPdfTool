from flask import Blueprint, render_template, request, jsonify # request: lay du lieu tu client gui len, jsonify: chuyen du lieu thanh json
from rag_model.src.qabot import llm_chain # llm_chain: la ham tuong tac vs model de tra loi cau hoi

home_bp = Blueprint('home', __name__)


@home_bp.route("/")
def home():
    return render_template("home.html")

@home_bp.route("/square", methods=["GET", "POST"])
def squarenumber():
    if request.method == "POST":
        num = request.form.get("num")  # get the input from the form
        if num.strip() == "": # Empty input
            return "<h1> Invalid input. Please enter a number.</h1>"
        square = int(num) ** 2
        return render_template('/caculation/answer.html', squareofnum=square, num=num)
    return render_template('/caculation/square.html')


# @home_bp.route("/ask", methods=["POST"])
# def ask():
#     try:
#         data = request.get_json()
#         if not data or "question" not in data:
#             return jsonify({"error": "Missing 'question' in request"}), 400

#         question = data["question"]
#         answer = llm_chain.run(question)  # hoặc invoke(question), tuỳ LLM bạn dùng
#         return jsonify({"answer": answer})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
