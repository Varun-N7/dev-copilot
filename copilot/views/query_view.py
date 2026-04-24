from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from copilot.retrieval.retriever import retrieve_sync
from copilot.retrieval.qa_chain import answer

class QueryView(APIView):
    def post(self, request):
        question = request.data.get("question")
        repo_id = request.data.get("repo_id")
        if not question or not repo_id:
            return Response({"error": "question and repo_id required"}, status=status.HTTP_400_BAD_REQUEST)
        chunks = retrieve_sync(question, repo_id)
        if not chunks:
            return Response({"error": "No indexed data found for this repo_id."}, status=status.HTTP_404_NOT_FOUND)
        response_text = answer(question, chunks)
        return Response({
            "answer": response_text,
            "sources": [{"filepath": c["filepath"], "score": c["score"]} for c in chunks],
        })