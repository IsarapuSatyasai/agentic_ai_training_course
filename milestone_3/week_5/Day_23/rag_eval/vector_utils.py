# vector_utils.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import COLLECTION_NAME, PERSIST_DIRECTORY

def create_sample_chunks():
    text = """
    Graph RAG combines knowledge graphs with vector search. It excels at multi-hop reasoning.
    Hybrid search uses both vector similarity and BM25 keyword matching.
    Reranking with cross-encoders significantly improves result quality.
    """
    docs = [Document(page_content=text)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
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