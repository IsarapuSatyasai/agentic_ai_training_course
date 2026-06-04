# vector_db.py
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import COLLECTION_NAME, PERSIST_DIRECTORY

def create_vectorstore(chunks):
    """Create and store documents in Chroma"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    vectorstore.add_documents(chunks)
    return vectorstore