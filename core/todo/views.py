from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.shortcuts import redirect

from .forms import TaskEditForm
from .models import Task

from .tasks import delete_done_tasks
from django.http import HttpResponse


# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskEditView(UpdateView):
    model = Task
    template_name = "todo/update_task.html"
    success_url = reverse_lazy("todo:task_list")
    form_class = TaskEditForm


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskChangeStateView(UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.state = kwargs.get("state")
        object.save()
        return redirect(self.success_url)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


def task_delete_done(request):
    delete_done_tasks.delay()
    return HttpResponse("<h1>Delete done tasks</h1>")
