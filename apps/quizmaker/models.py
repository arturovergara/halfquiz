# Standard Libraries
import uuid

# Django Imports
from django.db import models


class GameManager(models.Manager):
    def create_random_game_by_topic(self, topic, number_of_questions):
        pass


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

    @property
    def time_seconds(self):
        seconds = (self.time / 1000) % 60

        return int(seconds)


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


class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_ready = models.BooleanField(default=False)
    current_question = models.ForeignKey(
        "Answer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quiz = models.ForeignKey(
        "Quiz",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    topic = models.ForeignKey(
        "Topic",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = GameManager()

    @property
    def is_quiz(self):
        return self.quiz is not None


class Answer(models.Model):
    question_order = models.PositiveSmallIntegerField()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    option = models.ForeignKey(
        "Option",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
