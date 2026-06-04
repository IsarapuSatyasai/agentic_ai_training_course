# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_CHUNK_SIZE = 300
DEFAULT_CHUNK_OVERLAP = 60
COLLECTION_NAME = "chunk_enrichment_demo"
PERSIST_DIRECTORY = "./chroma_db"