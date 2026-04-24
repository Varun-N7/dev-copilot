import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from copilot.tools.file_search import file_search as _file_search
from copilot.tools.test_runner import run_tests as _run_tests
from copilot.retrieval.retriever import retrieve_sync
from copilot.retrieval.qa_chain import build_context

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.environ["GROQ_API_KEY"])

def make_agent(repo_url: str, repo_id: str):
    @tool
    def search_codebase(question: str) -> str:
        """Search the codebase using semantic embeddings. Use for 'where is X', 'how does Y work'."""
        chunks = retrieve_sync(question, repo_id)
        return build_context(chunks) if chunks else "No relevant code found."

    @tool
    def search_files(pattern: str) -> str:
        """Search code files by regex pattern. Use when you need exact text matches."""
        return _file_search(repo_url, pattern)

    @tool
    def run_tests(dummy: str = "") -> str:
        """Run the project test suite and return results. Ignore the dummy parameter."""
        return _run_tests(repo_url)

    tools = [search_codebase, search_files, run_tests]
    return create_react_agent(llm, tools)

def agent_answer(question: str, repo_url: str, repo_id: str) -> str:
    agent = make_agent(repo_url, repo_id)
    system = f"You are a developer assistant for the GitHub repo {repo_url}. Use tools to investigate the codebase before answering. Always cite file paths in your final answer."
    result = agent.invoke({"messages": [("system", system), ("human", question)]})
    return result["messages"][-1].content