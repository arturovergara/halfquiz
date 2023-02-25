# Django Imports
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import QuestionForm, TopicForm
from .models import Question, Topic


class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"


class TopicCreateView(SuccessMessageMixin, CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was created successfully!"


class TopicDeleteView(SuccessMessageMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was deleted successfully!"

    def get(self, request, *args, **kwargs):
        raise Http404("Only POST method available")


class TopicUpdateView(SuccessMessageMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was updated successfully!"


class QuestionListView(ListView):
    model = Question
    context_object_name = "questions"


class QuestionCreateView(SuccessMessageMixin, CreateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was created successfully!"


class QuestionUpdateView(SuccessMessageMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was updated successfully!"
