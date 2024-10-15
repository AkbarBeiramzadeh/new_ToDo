from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DeleteView, UpdateView

from .models import Task


# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'


class TaskEditView(UpdateView):
    pass


class TaskDeleteView(DeleteView):
    pass


class TaskChangeStateView(UpdateView):
    pass
