from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Task


# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'



class TaskEditView:
    pass


class TaskDeleteView:
    pass


class TaskUpdateView:
    pass


class TaskChangeStateView:
    pass
