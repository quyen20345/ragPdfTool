import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = "AIzaSyDaOTajq9YRNRvNE7bIPYOv568CP4WNO0A"# getpass.getpass("Enter API key for Google Gemini: ")
  # AIzaSyDaOTajq9YRNRvNE7bIPYOv568CP4WNO0A
from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

print(model.invoke("Hello, world!"))
