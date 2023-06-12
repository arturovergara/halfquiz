# Django Imports
from django.urls import reverse_lazy

# 3rd Party Libraries
import pytest

# Halfquiz Libraries
from apps.quizmaker.models import Option, Question, Topic

home_url = reverse_lazy("quizmaker:home")
pytestmark = pytest.mark.django_db


class TestTopicListView:
    url = reverse_lazy("quizmaker:topic_list")

    def test_home_view_redirect_to_topic_list_view(self, client):
        response = client.get(home_url)

        assert response.status_code == 302
        assert response["Location"] == self.url

    def test_get_method_without_data(self, client):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/topic_list.html"
        assert "<th>Name</th>" in response_content
        assert "<th>Description</th>" in response_content

    def test_get_method_display_rigth_data(self, client, topic_list):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")
        topics = Topic.objects.all()

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/topic_list.html"

        for topic in topics:
            assert topic.name in response_content
            assert topic.description in response_content


class TestTopicCreateView:
    url = reverse_lazy("quizmaker:topic_create")

    def test_get_method_renders_right_form(self, client):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/topic_form.html"

        assert 'name="name"' in response_content
        assert 'name="description"' in response_content

    def test_post_method_creates_a_topic(self, client):
        data = {
            "name": "A-new-excelent-topic",
            "description": "This-is-the-test-topic-hahaha",
        }
        response = client.post(self.url, data=data, follow=True)
        created_topic = Topic.objects.first()

        assert response.status_code == 200
        assert Topic.objects.count() == 1
        assert created_topic.name == data["name"]
        assert created_topic.description == data["description"]


class TestTopicDeleteView:
    def get_url(self, topic_id):
        return reverse_lazy("quizmaker:topic_delete", args=(topic_id,))

    def test_get_method_is_disable(self, client, topic):
        response = client.get(self.get_url(topic.id))

        assert response.status_code == 404
        assert response.context["exception"] == "Only POST method available"

    def test_post_method_delete_topic_model(self, client, topic_list):
        topic = Topic.objects.first()
        assert Topic.objects.count() == 3

        response = client.post(self.get_url(topic.id), follow=True)

        assert response.status_code == 200
        assert response.redirect_chain[0][1] == 302
        assert response.redirect_chain[0][0] == TestTopicListView.url

        assert Topic.objects.count() == 2
        assert Topic.objects.filter(id=topic.id).count() == 0


class TestTopicUpdateView:
    def get_url(self, topic_id):
        return reverse_lazy("quizmaker:topic_update", args=(topic_id,))

    def test_get_method_renders_right_form(self, client, topic):
        response = client.get(self.get_url(topic.id))
        response_content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/topic_form.html"
        assert 'name="name"' in response_content
        assert 'name="description"' in response_content

        assert topic.name in response_content
        assert topic.description in response_content

    def test_post_method_with_right_data_updates_a_topic(self, client, topic):
        data = {"name": "New-Topic-name", "description": topic.description}
        response = client.post(self.get_url(topic.id), data=data, follow=True)
        updated_topic = Topic.objects.first()

        assert response.status_code == 200
        assert response.redirect_chain[0][1] == 302
        assert response.redirect_chain[0][0] == TestTopicListView.url

        assert updated_topic.name == data["name"]
        assert updated_topic.description == data["description"]


class TestQuestionListView:
    url = reverse_lazy("quizmaker:question_list")

    def test_get_method_without_data(self, client):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/question_list.html"
        assert "<th>Statement</th>" in response_content
        assert "<th>Topic</th>" in response_content
        assert "<th>Time</th>" in response_content

    def test_get_method_display_rigth_data(self, client, question_list):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")
        questions = Question.objects.select_related("topic")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/question_list.html"

        for question in questions:
            assert question.statement in response_content
            assert question.topic.name in response_content
            assert f"{question.time_seconds}s" in response_content


class TestQuestionCreateView:
    url = reverse_lazy("quizmaker:question_create")

    def test_get_method_renders_right_form(self, client):
        response = client.get(self.url)
        response_content = response.content.decode("utf-8")

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/question_form.html"

        assert 'name="statement"' in response_content
        assert 'name="topic"' in response_content
        assert 'name="time"' in response_content

        for i in range(4):
            assert f'name="options-{i}-id"' in response_content
            assert f'name="options-{i}-text"' in response_content
            assert f'name="options-{i}-question"' in response_content
            assert f'name="options-{i}-is_right"' in response_content

    def test_post_method_with_right_data_creates_a_question(self, client, topic):
        data = {
            "statement": "Test Question",
            "topic": topic.id,
            "time": 45000,
            "options-TOTAL_FORMS": 4,
            "options-INITIAL_FORMS": 0,
            "options-0-text": "test",
            "options-0-is_right": True,
            "options-1-text": "test 2",
            "options-1-is_right": False,
            "options-2-text": "test 3",
            "options-2-is_right": False,
            "options-3-text": "test 4",
            "options-3-is_right": False,
        }
        response = client.post(self.url, data=data, follow=True)
        created_question = Question.objects.prefetch_related("options").first()
        created_options = created_question.options.all()

        assert response.status_code == 200
        assert Question.objects.count() == 1

        assert created_question.statement == data["statement"]
        assert created_question.topic == topic
        assert created_question.time == data["time"]

        for i, option in enumerate(created_options):
            assert option.text == data[f"options-{i}-text"]
            assert option.is_right == data[f"options-{i}-is_right"]


class TestQuestionDeleteView:
    def get_url(self, question_id):
        return reverse_lazy("quizmaker:question_delete", args=(question_id,))

    def test_get_method_is_disable(self, client, question):
        response = client.get(self.get_url(question.id))

        assert response.status_code == 404
        assert response.context["exception"] == "Only POST method available"

    def test_post_method_deletes_a_question_model(self, client, question):
        question = Question.objects.prefetch_related("options").first()
        options = question.options.all()

        assert Question.objects.count() == 1
        assert options.count() == 4

        response = client.post(self.get_url(question.id), follow=True)

        assert response.status_code == 200
        assert response.redirect_chain[0][1] == 302
        assert response.redirect_chain[0][0] == TestQuestionListView.url

        assert Question.objects.count() == 0
        assert Option.objects.count() == 0


class TestQuestionUpdateView:
    def get_url(self, question_id):
        return reverse_lazy("quizmaker:question_update", args=(question_id,))

    def test_get_method_renders_right_form(self, client, question):
        response = client.get(self.get_url(question.id))
        response_content = response.content.decode("utf-8")
        options = Option.objects.filter(question=question)

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/question_form.html"
        assert 'name="statement"' in response_content
        assert 'name="topic"' in response_content
        assert 'name="time"' in response_content

        assert question.statement in response_content
        assert question.topic.name in response_content
        assert f"{question.time_seconds}" in response_content

        for option in options:
            assert option.text in response_content

    def test_post_method_with_right_data_updates_a_question(self, client, question):
        data = {
            "statement": "New Test Statement",
            "topic": question.topic.id,
            "time": question.time,
            "options-TOTAL_FORMS": 4,
            "options-INITIAL_FORMS": 0,
            "options-0-text": "test",
            "options-0-is_right": True,
            "options-1-text": "test 2",
            "options-1-is_right": False,
            "options-2-text": "test 3",
            "options-2-is_right": False,
            "options-3-text": "test 4",
            "options-3-is_right": False,
        }
        response = client.post(self.get_url(question.id), data=data, follow=True)
        updated_question = Question.objects.first()

        assert response.status_code == 200
        assert response.redirect_chain[0][1] == 302
        assert response.redirect_chain[0][0] == TestQuestionListView.url

        assert updated_question.statement == data["statement"]
        assert updated_question.topic.id == data["topic"]
        assert updated_question.time == data["time"]
