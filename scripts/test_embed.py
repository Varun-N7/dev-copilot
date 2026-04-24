import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from copilot.embeddings import embedder

vec = embedder.embed_query("hello world")
assert len(vec) == 384, f"unexpected dim: {len(vec)}"
print("Embedding OK, dim =", len(vec))