from django.urls import reverse, resolve
from todo.views import (
    TaskListView,
    TaskEditView,
    TaskDeleteView,
    TaskChangeStateView,
    TaskCreateView,
)


class TestTodoUrl:
    def test_todo_task_list_url_resolve(self):
        url = reverse("todo:task_list")
        assert resolve(url).func.view_class == TaskListView

    def test_todo_task_create_url_resolve(self):
        url = reverse("todo:task_create")
        assert resolve(url).func.view_class == TaskCreateView

    def test_todo_task_edit_url_resolve(self):
        url = reverse("todo:task_edit", kwargs={"pk": 1})
        assert resolve(url).func.view_class == TaskEditView

    def test_todo_task_delete_url_resolve(self):
        url = reverse("todo:task_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == TaskDeleteView

    def test_todo_task_change_state_url_resolve(self):
        url = reverse("todo:task_change_state", kwargs={"pk": 1, "state": "ToDo"})
        assert resolve(url).func.view_class == TaskChangeStateView
