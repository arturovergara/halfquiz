# Django Imports
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import OptionFormSet, QuestionForm, TopicForm
from .models import Game, Question, Topic


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

    def get_context_data(self, **kwargs):
        context_data = super(QuestionCreateView, self).get_context_data(**kwargs)
        context_data["option_formset"] = (
            OptionFormSet(self.request.POST) if self.request.POST else OptionFormSet()
        )

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data(form=form)
        formset = context_data["option_formset"]

        if not formset.is_valid():
            return super(QuestionCreateView, self).form_invalid(form)

        response = super(QuestionCreateView, self).form_valid(form)
        formset.instance = self.object
        formset.save()

        return response


class QuestionDeleteView(SuccessMessageMixin, DeleteView):
    model = Question
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was deleted successfully!"

    def get(self, request, *args, **kwargs):
        raise Http404("Only POST method available")


class QuestionUpdateView(SuccessMessageMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was updated successfully!"

    def get_context_data(self, **kwargs):
        context_data = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context_data["option_formset"] = (
            OptionFormSet(self.request.POST, instance=self.object)
            if self.request.POST
            else OptionFormSet(instance=self.object)
        )

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data(form=form)
        formset = context_data["option_formset"]

        if not formset.is_valid():
            return super(QuestionUpdateView, self).form_invalid(form)

        response = super(QuestionUpdateView, self).form_valid(form)
        formset.instance = self.object
        formset.save()

        return response


class TestView(TemplateView):
    template_name = "quizmaker/test.html"

    def get_context_data(self, **kwargs):
        topic = Topic.objects.first()
        Game.objects.create_random_game_by_topic(topic=topic, number_of_questions=2)
        return super(TestView, self).get_context_data(**kwargs)
