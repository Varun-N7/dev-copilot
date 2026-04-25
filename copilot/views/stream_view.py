import json, os
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from copilot.retrieval.retriever import retrieve_sync
from copilot.retrieval.qa_chain import build_context, SYSTEM_PROMPT
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.environ["GROQ_API_KEY"], streaming=True)

class StreamQueryView(APIView):
    def post(self, request):
        question = request.data.get("question")
        repo_id = request.data.get("repo_id")
        if not question or not repo_id:
            return StreamingHttpResponse("data: {\"error\": \"missing params\"}\n\n", content_type="text/event-stream")

        chunks = retrieve_sync(question, repo_id)
        context = build_context(chunks)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Codebase:\n\n{context}\n\nQuestion: {question}"),
        ]
        sources = [{"filepath": c["filepath"], "score": c["score"]} for c in chunks]

        def event_stream():
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
            for chunk in llm.stream(messages):
                token = chunk.content
                if token:
                    yield f"data: {json.dumps({'type': 'token', 'text': token})}\n\n"
            yield "data: {\"type\": \"done\"}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response