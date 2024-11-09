from django.urls import path, include
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("task-create/", views.TaskCreateView.as_view(), name="task_create"),
    path("task-edit/<int:pk>/", views.TaskEditView.as_view(), name="task_edit"),
    path("task-delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path(
        "task-change-state/<int:pk>/<str:state>/",
        views.TaskChangeStateView.as_view(),
        name="task_change_state",
    ),
    path("api/v1/", include("todo.api.v1.urls")),
]
