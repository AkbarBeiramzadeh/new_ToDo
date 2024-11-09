from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from accounts.models import User
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="ab@ab.com", password="1020")
    return user


@pytest.fixture
def task_obj(common_user):
    task = Task.objects.create(user=common_user, title="test", state="ToDo")
    return task


@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_response_200_status(self, api_client, common_user):
        api_client.force_login(user=common_user)
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_401_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
            "state": "ToDo",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
            "state": "ToDo",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_task_without_login_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
            "state": "ToDo",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:task-list")
        data = {
            "state": "ToDo",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_get_task_detail_response_200_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        user = common_user
        api_client.force_authenticate(user=user)
        data = {
            "title": "test",
            "state": "ToDo",
        }
        api_client.post(url, data)

        url_detail = reverse("todo:api-v1:task-detail", kwargs={"pk": 1})
        response = api_client.get(url_detail)
        assert response.status_code == 200

    def test_get_task_detail_response_404_status(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        url_detail = reverse("todo:api-v1:task-detail", kwargs={"pk": 1})
        response = api_client.get(url_detail)
        assert response.status_code == 404

    def test_edit_task_detail_response_200_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        user = common_user
        api_client.force_authenticate(user=user)
        data = {
            "title": "test",
            "state": "ToDo",
        }
        api_client.post(url, data)

        new_data = {
            "title": "edited",
            "state": "done",
        }
        url_detail = reverse("todo:api-v1:task-detail", kwargs={"pk": 1})
        response = api_client.put(url_detail, data=new_data)

        assert response.status_code == 200
        assert response.data["title"] == "edited"
        assert response.data["state"] == "done"

    def test_delete_task(self, api_client, common_user, task_obj):
        api_client.force_authenticate(common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task_obj.pk})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Task.objects.filter(pk=task_obj.pk).exists() is False

    def test_delete_task_not_found(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)
        assert response.status_code == 404

    def test_delete_task_with_anonymous_user(self, api_client, common_user):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)
        assert response.status_code == 401
