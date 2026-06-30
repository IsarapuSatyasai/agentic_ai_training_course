# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

COLLECTION_NAME = "rag_eval_demo"
PERSIST_DIRECTORY = "./chroma_db"