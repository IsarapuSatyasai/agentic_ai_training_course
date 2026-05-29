import chromadb
from chromadb.utils import embedding_functions
from src.embeddings import get_embedding
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class FinancialPolicyRAG:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./vectorstore")
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="wef_financial_policy",
            embedding_function=self.openai_ef
        )

    def ingest_pdf(self, pdf_path: str):
        from src.utils import load_and_chunk_pdf
        documents = load_and_chunk_pdf(pdf_path)
        
        texts = [doc["text"] for doc in documents]
        ids = [doc["id"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)
        print(f"✅ Ingested {len(documents)} chunks into vector database")

    def retrieve(self, query: str, top_k: int = 4):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        return results['documents'][0], results['metadatas'][0]

    def generate_answer(self, query: str, context: str):
        prompt = f"""You are an expert assistant on the Water Environment Federation (WEF) Financial Policy.

Use ONLY the following context to answer the question. 
If the answer is not in the context, say "I don't have enough information from the policy document."

Context:
{context}

Question: {query}

Answer professionally and clearly, quoting specific policy sections when relevant.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful financial policy expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content