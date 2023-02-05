# Django Imports
from django.views.generic import ListView, TemplateView

from .models import Topic


class TestView(TemplateView):
    template_name = "quizmaker/example.html"


class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"
