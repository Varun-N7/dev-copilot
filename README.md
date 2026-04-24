
# Dev Copilot
An AI-powered developer assistant that lets you chat with any GitHub codebase. Ask questions, search code, run tests, and get cited answers — all powered by local embeddings and RAG.

## What it does
- Clones any GitHub repo and indexes all code files
- Chunks and embeds code using HuggingFace (all-MiniLM-L6-v2)
- Stores vectors in MongoDB
- Retrieves relevant chunks and answers questions using LLM (Groq)
- AI Agent that can search files by regex and run the test suite
- Streams responses to the browser in real time

## Requirements
- Python 3.11+
- Docker
- MongoDB (via Docker)
- Groq API key (free at console.groq.com)

## Quick start
```bash
git clone https://github.com/Varun-N7/dev-copilot.git
cd dev-copilot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
sudo systemctl start docker
sudo docker compose up -d
python manage.py migrate
python manage.py runserver
```

## API reference

### POST /api/index
Index a GitHub repository.
**Request:**
```json
{
  "repo_url": "https://github.com/pallets/flask"
}
```
**Response:**
```json
{
  "status": "indexing_started",
  "repo_id": "7e3d4d9940b1"
}
```

### POST /api/query
Ask a question about an indexed repository.
**Request:**
```json
{
  "repo_id": "7e3d4d9940b1",
  "repo_url": "https://github.com/pallets/flask",
  "question": "Where is authentication handled?"
}
```
**Response:**
```json
{
  "answer": "Authentication is handled in `examples/tutorial/flaskr/auth.py`...",
  "sources": [
    {"filepath": "examples/tutorial/flaskr/auth.py", "score": 0.4157}
  ]
}
```

## Example curl commands

### Index a repo
```bash
curl -X POST http://localhost:8000/api/index \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/pallets/flask"}'
```

### Ask a question
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"repo_id": "7e3d4d9940b1", "repo_url": "https://github.com/pallets/flask", "question": "Where is authentication handled?"}'
```

### Run tests
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"repo_id": "7e3d4d9940b1", "repo_url": "https://github.com/pallets/flask", "question": "Run the tests and tell me if they pass"}'
```

## Running tests
```bash
pytest tests/ -v
```
