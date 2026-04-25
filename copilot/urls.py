from django.urls import path
from copilot.views.index_view import IndexRepoView
from copilot.views.query_view import QueryView
from copilot.views.stream_view import StreamQueryView
from copilot.views.webhook_view import WebhookView

urlpatterns = [
    path("index", IndexRepoView.as_view()),
    path("query", QueryView.as_view()),
    path("query/stream", StreamQueryView.as_view()),
    path("webhook", WebhookView.as_view()),
]