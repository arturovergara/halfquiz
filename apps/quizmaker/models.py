# Standard Libraries
import random
import uuid
from datetime import datetime
from pathlib import Path

# Django Imports
from django.db import models
from django.utils import timezone


def generate_image_path(instance, filename) -> str:
    upload_to = "images"
    now = timezone.now()
    new_filename = f"image_{datetime.timestamp(now)}.jpg"

    return Path(upload_to, new_filename).as_posix()


class GameManager(models.Manager):
    def create_random_game_by_topic(self, topic, number_of_questions, show_answer):
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
        game.show_answer = show_answer
        game.save()

        return game

    def create_all_possible_random_games(self):
        def split_list(source_list: list, size: int) -> list[list]:
            output = []

            while len(source_list) > size:
                pice = source_list[:size]
                output.append(pice)
                source_list = source_list[size:]

            output.append(source_list)

            return output

        # Standard Libraries
        from time import sleep

        topic = Topic.objects.first()
        questions = Question.objects.filter(topic=topic)
        questions_length = questions.count()
        random_numbers = random.sample(range(questions_length), questions_length)
        random_games = split_list(random_numbers, 35)

        for random_game in random_games:
            game = self.create()
            random_questions = [
                GameQuestion(question=questions[idx], order=i, game=game)
                for i, idx in enumerate(random_game, start=1)
            ]

            GameQuestion.objects.bulk_create(random_questions)
            game.current_question = GameQuestion.objects.get(order=1, game=game)
            game.show_answer = False
            game.save()

            sleep(1)

    def create_game_with_previous_wrong_questions(self):
        wrong_questions_idx = set(
            GameQuestion.objects.filter(
                models.Q(answer__is_right=False) | models.Q(answer__isnull=True)
            ).values_list("question__id", flat=True)
        )
        wrong_questions = Question.objects.filter(id__in=wrong_questions_idx)
        topic = Topic.objects.first()
        questions = Question.objects.filter(topic=topic).exclude(
            id__in=wrong_questions_idx
        )
        questions_length = questions.count()

        game = self.create()
        random_numbers = random.sample(
            range(questions_length), 35 - wrong_questions.count()
        )
        retry_questions = [
            GameQuestion(question=question, order=i, game=game)
            for i, question in enumerate(wrong_questions, start=1)
        ]
        random_questions = [
            GameQuestion(question=questions[idx], order=i, game=game)
            for i, idx in enumerate(random_numbers, start=wrong_questions.count() + 1)
        ]

        GameQuestion.objects.bulk_create(retry_questions + random_questions)
        game.current_question = GameQuestion.objects.get(order=1, game=game)
        game.show_answer = False
        game.save()


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    statement = models.CharField(max_length=1250)
    time = models.PositiveBigIntegerField(default=45000)
    explaination = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=generate_image_path, null=True, blank=True)
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

    @property
    def correct_option(self):
        try:
            correct_option = Option.objects.get(question=self, is_right=True)
        except Option.DoesNotExist:
            return None

        return correct_option


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
    show_answer = models.BooleanField(default=False)
    current_question = models.ForeignKey(
        "GameQuestion",
        related_name="game_answers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GameManager()

    @property
    def name(self) -> str:
        timestamp = timezone.localtime(self.created_at).strftime("%Y-%m-%d %H:%M:%S")

        return f"Test {timestamp}"

    @property
    def previous_question(self):
        order = (
            self.current_question.order
            if self.current_question is not None
            else GameQuestion.objects.filter(game=self).count()
        )
        try:
            question = GameQuestion.objects.get(game=self, order=order - 1)
        except GameQuestion.DoesNotExist:
            return None

        return question

    def answer_question(self) -> None:
        try:
            next_question = GameQuestion.objects.get(
                game=self, order=self.current_question.order + 1
            )
            self.current_question = next_question
        except GameQuestion.DoesNotExist:
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
