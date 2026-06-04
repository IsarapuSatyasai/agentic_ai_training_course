# enrichment.py
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_document():
    with open("sample_document.txt", "r", encoding="utf-8") as f:
        return f.read()

def enrich_chunks(text, chunk_size=300, chunk_overlap=60):
    """Split and enrich document with metadata"""
    docs = [Document(page_content=text)]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = splitter.split_documents(docs)
    
    # Enrichment
    for chunk in chunks:
        chunk.metadata = {
            "source": "sample_document.txt",
            "date": "2025-05-20",
            "category": "employee_onboarding",
            "entities": ["Satyasai Esarapu", "Hyderabad", "xAI Solutions", "Bangalore", "Pune"],
            "summary": "Employee identity submission and company expansion plans.",
            "has_pii": True,
            "domain": "AI_Engineering"
        }
    return chunks