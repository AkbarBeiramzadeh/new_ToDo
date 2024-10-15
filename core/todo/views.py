from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DeleteView, UpdateView, CreateView

from .models import Task


# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskEditView(UpdateView):
    pass


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskChangeStateView(UpdateView):
    pass


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title']
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
