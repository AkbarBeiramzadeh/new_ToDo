from celery import shared_task
from django.apps import apps


@shared_task
def delete_done_tasks():
    Task = apps.get_model('todo', 'Task')
    tasks = Task.objects.filter(state="Done")
    if tasks:
        tasks.delete()
