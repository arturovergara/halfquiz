# Django Imports
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import TopicForm
from .models import Topic


class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"


class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was created successfully!"
