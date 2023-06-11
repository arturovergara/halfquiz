# Django Imports
from django.urls import reverse_lazy

# 3rd Party Libraries
import pytest

# Halfquiz Libraries
from apps.quizmaker.models import Topic

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
        response_content = str(response.content)

        assert response.status_code == 200
        assert response.template_name[0] == "quizmaker/topic_list.html"
        assert "<th>Name</th>" in response_content
        assert "<th>Description</th>" in response_content

    def test_get_method_display_rigth_data(self, client, topic_list):
        response = client.get(self.url)
        response_content = str(response.content)
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
        response_content = str(response.content)

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
        response_content = str(response.content)

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
    pass


class TestQuestionCreateView:
    pass


class TestQuestionDeleteView:
    pass


class TestQuestionUpdateView:
    pass
