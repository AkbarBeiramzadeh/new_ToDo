from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsTaskOwner
from .serializers import TaskSerializer
from ...models import Task
from .paginations import DefaultPagination
from rest_framework import filters


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTaskOwner]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state']
    ordering_fields = ['created_at']
    search_fields = ['title', 'state']
    pagination_class = DefaultPagination
