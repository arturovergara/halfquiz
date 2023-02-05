# Django Imports
from django.urls import path

from .views import TestView, TopicListView

app_name = "quizmaker"
urlpatterns = [
    path("test/", TestView.as_view(), name="test"),
    path("topics/", TopicListView.as_view(), name="topic_list"),
]
