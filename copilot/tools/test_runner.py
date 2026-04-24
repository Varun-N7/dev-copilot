import os, subprocess
from copilot.ingestion.cloner import CLONE_ROOT, repo_id as get_repo_id

ALLOWED_TEST_COMMANDS = {
    "pytest": ["python", "-m", "pytest", "--tb=short", "-q", "--timeout=30"],
    "npm_test": ["npm", "test", "--", "--watchAll=false"],
}

def detect_test_command(local_path: str) -> list[str] | None:
    if os.path.exists(os.path.join(local_path, "pytest.ini")) or \
       os.path.exists(os.path.join(local_path, "setup.cfg")) or \
       os.path.exists(os.path.join(local_path, "pyproject.toml")) or \
       os.path.exists(os.path.join(local_path, "tests")) or \
       any(f.endswith("_test.py") or f.startswith("test_") for f in os.listdir(local_path)):
        return ALLOWED_TEST_COMMANDS["pytest"]
    if os.path.exists(os.path.join(local_path, "package.json")):
        return ALLOWED_TEST_COMMANDS["npm_test"]
    return None

def run_tests(repo_url: str) -> str:
    """Run tests in the cloned repo. Returns stdout/stderr output (max 4000 chars)."""
    rid = get_repo_id(repo_url)
    local_path = os.path.join(CLONE_ROOT, rid)
    if not os.path.exists(local_path):
        return "Error: repo not indexed."
    cmd = detect_test_command(local_path)
    if not cmd:
        return "Could not detect a test runner (looked for pytest, package.json)."
    try:
        result = subprocess.run(
            cmd,
            cwd=local_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = (result.stdout + result.stderr)[:4000]
        return output if output else "No output from test runner."
    except subprocess.TimeoutExpired:
        return "Tests timed out after 60 seconds."
    except FileNotFoundError as e:
        return f"Test runner not found: {e}"