from django.urls import path
from copilot.views.index_view import IndexRepoView
from copilot.views.query_view import QueryView

urlpatterns = [
    path("index", IndexRepoView.as_view()),
    path("query", QueryView.as_view()),
]