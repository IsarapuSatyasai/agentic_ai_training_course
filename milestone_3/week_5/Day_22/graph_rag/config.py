# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

DEFAULT_CHUNK_SIZE = 400
DEFAULT_CHUNK_OVERLAP = 80

COLLECTION_NAME = "graph_rag_demo"
PERSIST_DIRECTORY = "./chroma_db"