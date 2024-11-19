from django.db import models
# from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=20, default="ToDo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_relative_api_url(self):
        return reverse("todo:api-v1:task-detail", kwargs={"pk": self.pk})
