# Django Imports
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    statement = models.CharField(max_length=200)
    time = models.PositiveBigIntegerField(default=45000)
    explaination = models.TextField(null=True, blank=True)
    topic = models.ForeignKey(
        "Topic",
        on_delete=models.PROTECT,
        related_name="questions",
        help_text="Select a topic for this question",
    )

    def __str__(self):
        return f"{self.statement}"


class Option(models.Model):
    text = models.CharField(max_length=100)
    is_right = models.BooleanField(default=False)
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="options",
        help_text="Select a question for this option",
    )

    def __str__(self):
        return f"{self.text}"


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    questions = models.ManyToManyField(
        "Question", related_name="quizzes", help_text="Select questions for this quiz"
    )

    class Meta:
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"{self.title}"
