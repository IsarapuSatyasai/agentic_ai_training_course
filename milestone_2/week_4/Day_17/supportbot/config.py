import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configuration
MODELS = {
    'gpt-4o-mini': "Base Model (Fast & Cheap)",
    'gpt-4o': "Advanced Model (High Quality)"
}