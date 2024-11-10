from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User
from todo.models import Task
import random

state_list = [
    "ToDo",
    "Done",
    "InProgress",
]


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # user = User.objects.get(email="admin@admin.com")
        user = User.objects.create_user(email=self.fake.email(), password="Test@123456")
        for _ in range(5):
            Task.objects.create(user=user,
                                title=self.fake.paragraph().split(" ")[0],
                                state=random.choice(state_list)
                                )
