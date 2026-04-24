import asyncio, threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from copilot.ingestion.cloner import clone_or_pull, walk_code_files, repo_id
from copilot.ingestion.chunker import chunk_all_files
from copilot.ingestion.store import embed_and_store

def _run_ingestion(repo_url):
    rid = repo_id(repo_url)
    local_path = clone_or_pull(repo_url)
    files = walk_code_files(local_path)
    chunks = chunk_all_files(files)
    asyncio.run(embed_and_store(rid, chunks))

class IndexRepoView(APIView):
    def post(self, request):
        repo_url = request.data.get("repo_url")
        if not repo_url:
            return Response({"error": "repo_url required"}, status=status.HTTP_400_BAD_REQUEST)
        rid = repo_id(repo_url)
        t = threading.Thread(target=_run_ingestion, args=(repo_url,), daemon=True)
        t.start()
        return Response({"status": "indexing_started", "repo_id": rid})
