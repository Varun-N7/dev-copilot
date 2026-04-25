import hashlib, hmac, json, os, threading, asyncio
from django.http import HttpResponse
from rest_framework.views import APIView
from copilot.ingestion.cloner import clone_or_pull, walk_code_files, repo_id as get_repo_id, CLONE_ROOT
from copilot.ingestion.chunker import chunk_file
from copilot.ingestion.store import embed_and_store
from copilot.db import embeddings_col

WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb", ".rs"}

def verify_signature(payload: bytes, sig_header: str) -> bool:
    if not WEBHOOK_SECRET:
        return True
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, sig_header or "")

def _reindex_files(repo_url, changed_files):
    rid = get_repo_id(repo_url)
    local_path = clone_or_pull(repo_url)
    all_chunks = []
    for rel_path in changed_files:
        ext = os.path.splitext(rel_path)[1].lower()
        if ext not in CODE_EXTENSIONS:
            continue
        full = os.path.join(local_path, rel_path)
        if not os.path.exists(full):
            asyncio.run(embeddings_col.delete_many({"repo_id": rid, "filepath": rel_path}))
            continue
        content = open(full, encoding="utf-8", errors="ignore").read()
        file_obj = {"filepath": rel_path, "language": ext.lstrip("."), "content": content}
        asyncio.run(embeddings_col.delete_many({"repo_id": rid, "filepath": rel_path}))
        all_chunks.extend(chunk_file(file_obj))
    if all_chunks:
        asyncio.run(embed_and_store(rid, all_chunks))

class WebhookView(APIView):
    def post(self, request):
        sig = request.headers.get("X-Hub-Signature-256", "")
        if not verify_signature(request.body, sig):
            return HttpResponse("Forbidden", status=403)
        payload = json.loads(request.body)
        if request.headers.get("X-GitHub-Event") != "push":
            return HttpResponse("OK")
        repo_url = payload["repository"]["clone_url"]
        changed = list({f for commit in payload.get("commits", []) for f in commit.get("added", []) + commit.get("modified", []) + commit.get("removed", [])})
        threading.Thread(target=_reindex_files, args=(repo_url, changed), daemon=True).start()
        return HttpResponse("OK")