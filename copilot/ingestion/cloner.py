import os, hashlib
from git import Repo

CLONE_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cloned_repos")
CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb", ".rs", ".cpp", ".c", ".h", ".cs", ".php", ".swift", ".kt"}

def repo_id(repo_url: str) -> str:
    return hashlib.md5(repo_url.encode()).hexdigest()[:12]

def clone_or_pull(repo_url: str) -> str:
    rid = repo_id(repo_url)
    local_path = os.path.join(CLONE_ROOT, rid)
    if os.path.exists(local_path):
        Repo(local_path).remotes.origin.pull()
    else:
        os.makedirs(CLONE_ROOT, exist_ok=True)
        Repo.clone_from(repo_url, local_path, depth=1)
    return local_path

def walk_code_files(local_path: str) -> list[dict]:
    files = []
    for root, dirs, filenames in os.walk(local_path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv", "venv"}]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in CODE_EXTENSIONS:
                full = os.path.join(root, fname)
                rel = os.path.relpath(full, local_path)
                try:
                    content = open(full, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                files.append({"filepath": rel, "language": ext.lstrip("."), "content": content})
    return files
