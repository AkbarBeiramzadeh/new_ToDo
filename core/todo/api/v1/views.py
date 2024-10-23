from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .serializers import TaskSerializer
from ...models import Task
from .permissions import IsOwner


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

