# Django Imports
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import (
    QuestionCreateView,
    QuestionDeleteView,
    QuestionListView,
    QuestionUpdateView,
    TopicCreateView,
    TopicDeleteView,
    TopicListView,
    TopicUpdateView,
)

app_name = "quizmaker"
urlpatterns = [
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic_delete"),
    path("topics/<int:pk>/edit/", TopicUpdateView.as_view(), name="topic_update"),
    path("topics/add/", TopicCreateView.as_view(), name="topic_create"),
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path(
        "questions/<int:pk>/delete/",
        QuestionDeleteView.as_view(),
        name="question_delete",
    ),
    path(
        "questions/<int:pk>/edit/", QuestionUpdateView.as_view(), name="question_update"
    ),
    path("questions/add/", QuestionCreateView.as_view(), name="question_create"),
    path("questions/", QuestionListView.as_view(), name="question_list"),
    path(
        "", RedirectView.as_view(url=reverse_lazy("quizmaker:topic_list")), name="home"
    ),
]
