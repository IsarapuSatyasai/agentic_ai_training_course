from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Simple AI Chatbot API")

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Local database file
DB_FILE = "conversations.json"

# --- JSON Database Helper Functions ---
def read_db() -> Dict[str, List[Dict]]:
    """Reads the JSON file and returns the data as a dictionary."""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def write_db(data: Dict[str, List[Dict]]):
    """Writes the dictionary back to the JSON file."""
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# --- Pydantic Models ---
class MessageRequest(BaseModel):
    message: str

# --- CRUD Endpoints ---

# 1. CREATE a new chat session
@app.post("/chats/")
def create_chat():
    db = read_db()
    chat_id = str(uuid.uuid4())[:8] # Generate a short, readable ID
    db[chat_id] = []
    write_db(db)
    return {"chat_id": chat_id}

# 2. READ all available chat sessions
@app.get("/chats/")
def get_all_chats():
    db = read_db()
    return {"chat_ids": list(db.keys())}

# 3. READ the history of a specific chat session
@app.get("/chats/{chat_id}")
def get_chat(chat_id: str):
    db = read_db()
    if chat_id not in db:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id, "messages": db[chat_id]}

# 4. UPDATE a chat session (Send a message and get AI response)
@app.post("/chats/{chat_id}/message")
def send_message(chat_id: str, req: MessageRequest):
    db = read_db()
    if chat_id not in db:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Append user message
    user_msg = {"role": "user", "content": req.message}
    db[chat_id].append(user_msg)
    
    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=db[chat_id]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Append AI message
    ai_msg = {"role": "assistant", "content": ai_reply}
    db[chat_id].append(ai_msg)
    
    # Save back to JSON
    write_db(db)
    return {"user_message": user_msg, "ai_message": ai_msg}

# 5. DELETE a chat session
@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: str):
    db = read_db()
    if chat_id in db:
        del db[chat_id]
        write_db(db)
        return {"detail": "Chat deleted"}
    raise HTTPException(status_code=404, detail="Chat not found")