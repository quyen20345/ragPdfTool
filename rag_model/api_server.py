from flask import Flask, request, jsonify
from qabot import QABot
import os

app = Flask(__name__)
qa_bot = QABot()

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    try:
        answer = qa_bot.get_answer(question)
        return jsonify({"answer": answer, "status": "success"})
    except Exception as e:
        return jsonify({"answer": str(e), "status": "error"}), 500

@app.route('/api/process_document', methods=['POST'])
def process_document():
    # Logic để xử lý tài liệu mới
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 