import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROVIDER = 'openai'
    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    
    TEMPERATURE = 0.7