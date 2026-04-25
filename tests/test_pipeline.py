import pytest, asyncio, os

FIXTURE_REPO = "https://github.com/pallets/flask"

@pytest.fixture(scope="module")
def repo_data():
    from copilot.ingestion.cloner import clone_or_pull, walk_code_files, repo_id
    path = clone_or_pull(FIXTURE_REPO)
    files = walk_code_files(path)
    rid = repo_id(FIXTURE_REPO)
    return {"path": path, "files": files, "repo_id": rid}

def test_cloner_returns_files(repo_data):
    assert len(repo_data["files"]) > 0
    assert all("filepath" in f for f in repo_data["files"])

def test_chunker_produces_chunks(repo_data):
    from copilot.ingestion.chunker import chunk_file
    f = repo_data["files"][0]
    chunks = chunk_file(f)
    assert len(chunks) >= 1
    assert "text" in chunks[0]

def test_retriever_returns_results(repo_data):
    from copilot.retrieval.retriever import retrieve_sync
    results = retrieve_sync("routing", repo_data["repo_id"], top_k=3)
    assert len(results) > 0
    assert "filepath" in results[0]