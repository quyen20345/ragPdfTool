from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings

import os

# variable declaration
vector_db_path = "vectorstores/db_faiss"
pdf_data_path = "data"

try:
    if os.path.exists(pdf_data_path):
        print("the path is valid and existes.")
    else:
        print("the path does not exist or is not accessible.")
except OSError as e:
    print("An error accurred while checking the path: ")
    print(e)
    
# create a vector db from a text.
def create_db_from_text():
    raw_text = """Deeper neural networks are more difficult to train. We
present a residual learning framework to ease the training
of networks that are substantially deeper than those used
previously. We explicitly reformulate the layers as learn-
ing residual functions with reference to the layer inputs, in-
stead of learning unreferenced functions. We provide com-
prehensive empirical evidence showing that these residual
networks are easier to optimize, and can gain accuracy from
considerably increased depth. On the ImageNet dataset we
evaluate residual nets with a depth of up to 152 layers—8×
deeper than VGG nets [41] but still having lower complex-
ity. An ensemble of these residual nets achieves 3.57% error
on the ImageNet test set. This result won the 1st place on the
ILSVRC 2015 classification task. We also present analysis
on CIFAR-10 with 100 and 1000 layers."""
    
    # split text
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=512, # split text into chunks of 512 characters
        chunk_overlap=50, # overlap chunks by 50 characters
        length_function=len # use the len function to determine the length of the text
    )
    
    chunks = text_splitter.split_text(raw_text)
    
    # embedding
    embedding_model = GPT4AllEmbeddings(model_file="models/all-MiniLM-L6-v2-f16.gguf")

    # create a vector db
    db = FAISS.from_texts(texts=chunks, embedding=embedding_model)
    db.save_local(vector_db_path)
    return db

def create_db_from_files():
    # declare loader to scan entire data directory for pdf files
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls = PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Embeding
    embedding_model = GPT4AllEmbeddings(model_file="models/all-MiniLM-L6-v2-f16.gguf")
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db

if __name__ == "__main__":
    # create_db_from_text()
    create_db_from_files()
    print("preparing vectorDB done !!!")
