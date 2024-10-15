from django import forms
from .models import Task


class TaskEditForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Task
        fields = ('title',)
