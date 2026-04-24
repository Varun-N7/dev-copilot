import os, re
from copilot.ingestion.cloner import CLONE_ROOT, repo_id as get_repo_id

def file_search(repo_url: str, pattern: str, max_results: int = 20) -> str:
    rid = get_repo_id(repo_url)
    local_path = os.path.join(CLONE_ROOT, rid)
    if not os.path.exists(local_path):
        return f"Error: repo not indexed. Call /api/index first."
    matches = []
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        return f"Invalid regex: {e}"
    for root, dirs, files in os.walk(local_path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        for fname in files:
            if not any(fname.endswith(ext) for ext in [".py", ".js", ".ts", ".java", ".go", ".rb"]):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, local_path)
            try:
                for i, line in enumerate(open(fpath, encoding="utf-8", errors="ignore"), 1):
                    if compiled.search(line):
                        matches.append(f"{rel}:{i}: {line.rstrip()}")
                        if len(matches) >= max_results:
                            return "\n".join(matches) + f"\n... (truncated at {max_results})"
            except Exception:
                continue
    return "\n".join(matches) if matches else "No matches found."