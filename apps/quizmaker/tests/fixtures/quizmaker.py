# 3rd Party Libraries
import pytest
from model_bakery import baker

# Halfquiz Libraries
from apps.quizmaker.models import Topic


@pytest.fixture
def topic():
    return baker.make(Topic)


@pytest.fixture
def topic_list():
    return baker.make(Topic, _quantity=3)
