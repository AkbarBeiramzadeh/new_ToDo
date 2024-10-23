from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from .filters import IsOwnerFilterBackend
from .permissions import IsTaskOwner
from .serializers import TaskSerializer
from ...models import Task


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTaskOwner]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [IsOwnerFilterBackend]




