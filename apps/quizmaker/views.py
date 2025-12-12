# Django Imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from .forms import (
    GameCreateForm,
    InGameQuestionForm,
    OptionFormSet,
    QuestionBulkCreateForm,
    QuestionForm,
    TopicForm,
)
from .models import Game, Question, Topic


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.annotate(questions_number=Count("questions")).order_by("id")


class TopicCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was created successfully!"


class TopicDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was deleted successfully!"

    def get(self, request, *args, **kwargs):
        raise Http404("Only POST method available")


class TopicUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("quizmaker:topic_list")
    success_message = "Topic was updated successfully!"


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = "questions"


class QuestionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class QuestionBulkCreateView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = QuestionBulkCreateForm
    template_name = "quizmaker/question_bulk_form.html"
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question have been added successfully!"

    def form_valid(self, form):
        form.save()

        return super(QuestionBulkCreateView, self).form_valid(form)


class QuestionDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was deleted successfully!"

    def get(self, request, *args, **kwargs):
        raise Http404("Only POST method available")


class QuestionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy("quizmaker:question_list")
    success_message = "Question was updated successfully!"

    def get_context_data(self, **kwargs):
        context_data = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context_data["option_formset"] = (
            OptionFormSet(self.request.POST, instance=self.get_object())
            if self.request.POST
            else OptionFormSet(instance=self.get_object())
        )

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data(form=form)
        formset = context_data["option_formset"]

        if not formset.is_valid():
            return super(QuestionUpdateView, self).form_invalid(form)

        response = super(QuestionUpdateView, self).form_valid(form)
        formset.instance = self.get_object()
        formset.save()

        return response


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    context_object_name = "games"


class GameCreateView(LoginRequiredMixin, FormView):
    form_class = GameCreateForm
    template_name = "quizmaker/game_form.html"
    success_url = reverse_lazy("quizmaker:game_list")

    def form_valid(self, form):
        self.game = form.create_game()

        return super(GameCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quizmaker:game_play", args=(self.game.uuid,))


class GameDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("quizmaker:game_list")
    success_message = "Game was deleted successfully!"

    def get(self, request, *args, **kwargs):
        raise Http404("Only POST method available")


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    context_object_name = "game"

    def get_object(self):
        return Game.objects.prefetch_related("gamequestion_set").get(
            uuid=self.kwargs["game_uuid"], is_ready=True
        )

    def get_context_data(self, **kwargs):
        context_data = super(GameDetailView, self).get_context_data(**kwargs)
        correct_answers = self.object.gamequestion_set.filter(
            answer__is_right=True
        ).count()
        total_questions = self.object.gamequestion_set.count()
        correct_percentage = (correct_answers / total_questions) * 100

        context_data["score"] = correct_answers
        context_data["is_approved"] = (
            correct_percentage >= settings.MINIMUM_PASSING_PERCENTAGE
        )

        return context_data


class InGameFormView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = InGameQuestionForm
    template_name = "quizmaker/ingame_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, uuid=kwargs["game_uuid"], is_ready=False)

        return super(InGameFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(InGameFormView, self).get_form_kwargs()
        kwargs.update({"instance": self.game.current_question})

        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super(InGameFormView, self).get_context_data(**kwargs)
        context_data["question_number"] = self.game.current_question.order
        context_data["question_statement"] = self.game.current_question.question.statement
        context_data["question_image"] = self.game.current_question.question.image

        return context_data

    def form_valid(self, form):
        self.game = form.save()

        return super(InGameFormView, self).form_valid(form)

    def get_success_url(self):
        if not self.game.is_ready:
            return reverse_lazy("quizmaker:game_play", args=(self.game.uuid,))

        return reverse_lazy("quizmaker:game_review", args=(self.game.uuid,))

    def get_success_message(self, cleaned_data):
        if not self.game.show_answer:
            return None

        is_right = cleaned_data["answer"].is_right
        extra_tags = "correct" if is_right else "incorrect"
        message = f"Answer: {self.game.previous_question.question.correct_option.text}"

        return messages.success(self.request, message, extra_tags=extra_tags)
