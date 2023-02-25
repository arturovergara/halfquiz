# Django Imports
from django import forms

from .models import Question, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("name", "description")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("statement", "topic", "time")
