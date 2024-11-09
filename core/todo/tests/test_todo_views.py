import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="ab@ab.com", password="1020")
    return user


@pytest.mark.django_db
class TestToDoView:

    def test_todo_index_view_with_logged_in_user_response(
        self, api_client, common_user
    ):
        url = reverse("todo:task_list")
        user = common_user
        api_client.force_login(user=user)
        response = api_client.get(url)
        assert response.status_code == 200
        assert bool(str(response.content).find("index")) is True
        assert "todo/task_list.html" in response.template_name

    def test_todo_index_view_with_anonymous_user_response(self, api_client):
        url = reverse("todo:task_list")
        response = api_client.get(url)
        assert response.status_code == 302
        assert bool(str(response.content).find("Task"))
        target_url = reverse("todo:task_list")
        assert response.url.startswith(
            target_url
        ), f"Expected redirect to {target_url}, but got {response.url}"
