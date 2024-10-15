from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# Create your views here.
class TaskListView(TemplateView):
    template_name = 'todo/task_list.html'


class TaskEditView:
    pass


class TaskDeleteView:
    pass


class TaskUpdateView:
    pass


class TaskChangeStateView:
    pass
