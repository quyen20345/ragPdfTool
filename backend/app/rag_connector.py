import requests
from app.config import Config

class RAGConnector:
    def __init__(self):
        self.base_url = Config.RAG_MODEL_URL

    def ask_question(self, question):
        """
        Gửi câu hỏi đến RAG model service
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/ask",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "error"}