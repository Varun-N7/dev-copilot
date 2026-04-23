# Dev Copilot

An AI-powered developer assistant that lets you chat with any GitHub codebase. Ask questions, search code, and get cited answers — all powered by local embeddings and RAG.

## What it does

- Clones any GitHub repo and indexes all code files
- Chunks and embeds code using HuggingFace (all-MiniLM-L6-v2)
- Stores vectors in MongoDB
- Retrieves relevant chunks and answers questions using LLM
- Streams responses to the browser in real time

## Requirements

- Python 3.11+
- Docker
- MongoDB (via Docker)

## Quick start

```bash
git clone https://github.com/Varun-N7/dev-copilot.git
cd dev-copilot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
docker-compose up -d
python manage.py migrate
python manage.py runserver
```

## Environment variables

| Variable | Description | Required |
|----------|-------------|----------|
| DJANGO_SECRET_KEY | Django secret key | Yes |
| DEBUG | Debug mode (True/False) | No |
| OPENAI_API_KEY | OpenAI API key | No |
| GITHUB_TOKEN | GitHub personal access token | Yes |
| MONGO_URI | MongoDB connection URI | Yes |
| MONGO_DB_NAME | MongoDB database name | Yes |

## Progress

- Day 1 — Foundation & ingestion pipeline ✅
- Day 2 — RAG retrieval + Django API 🔜
- Day 3 — Tool calling + agent executor 🔜
- Day 4 — Streaming, UI, webhooks & tests 🔜
