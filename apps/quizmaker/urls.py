# Django Imports
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import (
    GameCreateView,
    GameDeleteView,
    GameListView,
    InGameFormView,
    QuestionBulkCreateView,
    QuestionCreateView,
    QuestionDeleteView,
    QuestionListView,
    QuestionUpdateView,
    TestView,
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
    path("questions/import/", QuestionBulkCreateView.as_view(), name="question_import"),
    path("questions/", QuestionListView.as_view(), name="question_list"),
    path("games/<int:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
    path("games/<uuid:game_uuid>/play/", InGameFormView.as_view(), name="game_play"),
    path("games/add/", GameCreateView.as_view(), name="game_create"),
    path("games/", GameListView.as_view(), name="game_list"),
    path("test/", TestView.as_view(), name="test_view"),
    path("", RedirectView.as_view(url=reverse_lazy("quizmaker:topic_list")), name="home"),
]
