from pypdf import PdfReader

def load_and_chunk_pdf(pdf_path: str, chunk_size: int = 1000):
    reader = PdfReader(pdf_path)
    documents = []
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text().strip()
        if text:
            # Simple chunking
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size]
                documents.append({
                    "id": f"page_{page_num+1}_chunk_{i//chunk_size}",
                    "text": chunk,
                    "metadata": {
                        "source": "WEF_Financial_Policy",
                        "page": page_num + 1
                    }
                })
    return documents