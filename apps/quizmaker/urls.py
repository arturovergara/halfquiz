# Django Imports
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import TopicListView

app_name = "quizmaker"
urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path(
        "", RedirectView.as_view(url=reverse_lazy("quizmaker:topic_list")), name="home"
    ),
]
