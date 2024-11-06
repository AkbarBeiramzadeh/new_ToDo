import pytest
from rest_framework.test import APIClient
from accounts.models import User
from todo.models import Task


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="ab@ab.com", password="1020")
    return user


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestTaskModel:

    def test_create_task_with_valid_data(self, api_client, common_user):
        task = Task.objects.create(
            user=common_user,
            title="test",
            state="todo"
        )
        assert bool(Task.objects.filter(pk=task.id).exists())
        assert task.title == "test"

    def test_edit_task_with_valid_data(self, api_client, common_user):
        task = Task.objects.create(
            user=common_user,
            title="test",
            state="todo"
        )
        task.title = "edited"
        task.save()
        assert bool(Task.objects.filter(pk=task.id).exists())
        assert task.title == "edited"

    def test_delete_task(self, api_client, common_user):
        task = Task.objects.create(
            user=common_user,
            title="test",
            state="todo"
        )

        task.delete()
        assert not bool(Task.objects.filter(pk=task.id).exists())
