# 3rd Party Libraries
import pytest
from model_bakery import baker

# Halfquiz Libraries
from apps.quizmaker.models import Option, Question, Topic


@pytest.fixture
def topic():
    return baker.make(Topic)


@pytest.fixture
def topic_list():
    return baker.make(Topic, _quantity=3)


@pytest.fixture
def question():
    question = baker.make(Question)
    baker.make(Option, question=question, is_right=True)
    baker.make(Option, question=question, is_right=False, _quantity=3)

    return question


@pytest.fixture
def question_list():
    return baker.make(Question, _quantity=3)
