# backend/app/services/llm_service.py
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.vector_service import VectorService
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.7,
        )
        self.vector_service = VectorService()
    
    def create_rag_chain(self, temperature: float = 0.7):
        """Create RAG chain with Vietnamese prompt"""
        prompt_template = """
        Bạn là một trợ lý AI thông minh và hữu ích. Hãy sử dụng thông tin từ các tài liệu được cung cấp để trả lời câu hỏi một cách chính xác và chi tiết.

        Ngữ cảnh từ tài liệu:
        {context}

        Câu hỏi: {question}

        Hướng dẫn:
        - Trả lời dựa trên thông tin có trong tài liệu
        - Nếu không tìm thấy thông tin liên quan, hãy nói rằng bạn không tìm thấy thông tin trong tài liệu
        - Trả lời bằng tiếng Việt một cách tự nhiên và dễ hiểu
        - Có thể trích dẫn thông tin cụ thể từ tài liệu nếu cần

        Trả lời:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.llm.temperature = temperature
        vectorstore = self.vector_service.get_vectorstore()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        return qa_chain
    
    def query(self, question: str, temperature: float = 0.7):
        """Query documents using RAG"""
        # Check if there are any documents
        search_results = self.vector_service.search_similar(question, k=1)
        if not search_results:
            return {
                "result": "Không tìm thấy tài liệu nào trong cơ sở dữ liệu. Vui lòng upload tài liệu trước khi đặt câu hỏi.",
                "source_documents": []
            }
        
        qa_chain = self.create_rag_chain(temperature)
        result = qa_chain({"query": question})
        return result
    
    def test_connection(self):
        """Test Ollama connection"""
        try:
            response = self.llm.invoke("Hello")
            return True, response[:50] + "..." if len(response) > 50 else response
        except Exception as e:
            return False, str(e)
