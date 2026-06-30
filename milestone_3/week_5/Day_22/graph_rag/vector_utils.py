# vector_utils.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import COLLECTION_NAME, PERSIST_DIRECTORY

def create_chunks(text):
    docs = [Document(page_content=text)]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )
    return splitter.split_documents(docs)

def get_vectorstore(chunks=None):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    if chunks:
        vectorstore.add_documents(chunks)
    return vectorstore