from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsTaskOwner
from .serializers import TaskSerializer
from ...models import Task
from .paginations import DefaultPagination
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
import requests
from rest_framework.response import Response


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTaskOwner]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["state"]
    ordering_fields = ["created_at"]
    search_fields = ["title", "state"]
    pagination_class = DefaultPagination


class WeatherApi(APIView):
    """
    Current weather and forecast
    """
    @method_decorator(cache_page(timeout=20 * 60))
    def get(self, request, lat, long, api_key):
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}')
        return Response({"message": "GET request", "response": response.json()})
