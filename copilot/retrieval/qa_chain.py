import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = """You are a developer assistant with deep knowledge of the codebase provided.
Answer questions using ONLY the code excerpts below. 
Always cite the file path (e.g. `src/auth.py`) when referencing code.
If the answer isn't in the provided excerpts, say so clearly — do not guess.
Format code references as inline code with backticks."""

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.environ["GROQ_API_KEY"],
)

def build_context(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        parts.append(f"### {c['filepath']}\n```\n{c['text']}\n```")
    return "\n\n".join(parts)

def answer(question: str, chunks: list[dict]) -> str:
    context = build_context(chunks)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Codebase excerpts:\n\n{context}\n\n---\n\nQuestion: {question}"),
    ]
    response = llm.invoke(messages)
    return response.content