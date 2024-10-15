from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # path('', views.TaskListView.as_view(), name='task_list'),
    # path('task-edit/<int:pk>/', views.TaskEditView.as_view(), name='task_edit'),
    # path('task-delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
    # path('task-update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
    # path('task-change-state/<int:pk>/<str:state>/', views.TaskChangeStateView.as_view(), name='task_change_state'),
]
