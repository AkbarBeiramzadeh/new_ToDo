from rest_framework.test import APIClient
import pytest
from todo.forms import TaskEditForm


@pytest.fixture
def api_client():
    client = APIClient()
    return client


class TestTodoForm:
    def test_todo_edit_form_with_valid_data(self):
        form = TaskEditForm(
            data={
                "title": "test",
            }
        )
        assert form.is_valid() is True

    def test_todo_edit_form_with_no_data(self):
        form = TaskEditForm(data={})
        assert form.is_valid() is False
