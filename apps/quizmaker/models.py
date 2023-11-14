# Standard Libraries
import random
import uuid

# Django Imports
from django.db import models


class GameManager(models.Manager):
    def create_random_game_by_topic(self, topic, number_of_questions):
        questions = Question.objects.filter(topic=topic)
        questions_length = questions.count()

        if number_of_questions > questions_length:
            number_of_questions = questions_length

        game = self.create()
        random_numbers = random.sample(range(questions_length), number_of_questions)
        random_questions = [
            GameQuestion(question=questions[idx], order=i, game=game)
            for i, idx in enumerate(random_numbers, start=1)
        ]

        GameQuestion.objects.bulk_create(random_questions)
        game.current_question = GameQuestion.objects.get(order=1, game=game)
        game.save()

        return game


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    statement = models.CharField(max_length=400)
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
    text = models.CharField(max_length=250)
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
        "GameQuestion",
        related_name="game_answers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = GameManager()

    def answer_question(self) -> None:
        try:
            next_question = GameQuestion.objects.get(
                game=self, order=self.current_question.order + 1
            )
            self.current_question = next_question
        except Exception:
            self.current_question = None
            self.is_ready = True

        self.save()


class GameQuestion(models.Model):
    order = models.PositiveSmallIntegerField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.ForeignKey(
        "Option",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
