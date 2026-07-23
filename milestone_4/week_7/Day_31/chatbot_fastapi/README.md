



# Single AI Agent + FastAPI + Streamlit UI

A clean hierarchical project with:

- **FastAPI** backend (AI Agent powered by OpenAI)
- **Streamlit** frontend (beautiful chat UI)

## Folder Structure

```markdown
ai_agent_fastapi/
├── app/                          # Backend
│   ├── __init__.py
│   ├── main.py
│   ├── agent/
│   ├── core/
│   └── models/
├── frontend/                     # Frontend
│   ├── __init__.py
│   └── streamlit_app.py         
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Setup
```bash
cd ai_agent_fastapi
python -m venv .venv
# Windows → .venv\Scripts\activate
# Linux/macOS → source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure `.env`
```bash
cp .env.example .env
```
Add your **OpenAI** API key.

### 3. Run FastAPI (Terminal 1)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run Streamlit (Terminal 2)
```bash
streamlit run frontend/streamlit_app.py
```