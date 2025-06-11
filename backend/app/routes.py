from flask import Blueprint, request, jsonify
from app.rag_connector import RAGConnector

main = Blueprint('main', __name__)
rag = RAGConnector()

@main.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
            
        result = rag.ask_question(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}) 