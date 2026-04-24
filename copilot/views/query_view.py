from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from copilot.retrieval.retriever import retrieve_sync
from copilot.retrieval.agent import agent_answer

class QueryView(APIView):
    def post(self, request):
        question = request.data.get("question")
        repo_id = request.data.get("repo_id")
        repo_url = request.data.get("repo_url")
        if not question or not repo_id or not repo_url:
            return Response({"error": "question, repo_id and repo_url required"}, status=status.HTTP_400_BAD_REQUEST)
        chunks = retrieve_sync(question, repo_id)
        if not chunks:
            return Response({"error": "No indexed data found for this repo_id."}, status=status.HTTP_404_NOT_FOUND)
        response_text = agent_answer(question, repo_url, repo_id)
        return Response({
            "answer": response_text,
            "sources": [{"filepath": c["filepath"], "score": c["score"]} for c in chunks],
        })