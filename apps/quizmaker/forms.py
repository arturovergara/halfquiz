# Django Imports
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import Game, GameQuestion, Option, Question, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("name", "description")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("statement", "topic", "time")


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ("text", "is_right")


class BaseOptionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        right_answers = []

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            is_right = form.cleaned_data.get("is_right")
            right_answers.append(is_right)

        if not any(right_answers):
            raise ValidationError("There must be at least one correct option")


OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    formset=BaseOptionFormSet,
    extra=4,
    max_num=4,
    min_num=2,
    validate_min=True,
)


class GameCreateForm(forms.Form):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    number_of_questions = forms.IntegerField(min_value=1)

    def create_game(self):
        topic = self.cleaned_data["topic"]
        number_of_questions = self.cleaned_data["number_of_questions"]
        game = Game.objects.create_random_game_by_topic(
            topic=topic, number_of_questions=number_of_questions
        )

        return game


class InGameQuestionForm(forms.ModelForm):
    class Meta:
        model = GameQuestion
        fields = ("answer",)
        widgets = {
            "answer": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super(InGameQuestionForm, self).__init__(*args, **kwargs)

        self.fields["answer"].empty_label = None
        self.fields["answer"].queryset = Option.objects.filter(
            question=self.instance.question
        )

    def save(self, commit=True):
        game_question = super(InGameQuestionForm, self).save(commit)
        print("Se llamo a save()")
        game_question.game.answer_question()

        return game_question.game
