# Django Imports
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import Option, Question, Topic


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
