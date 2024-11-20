from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = "api-v1"

router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")

urlpatterns = router.urls

urlpatterns += [
    path('weather/<str:lat>/<str:long>/<str:api_key>/', views.WeatherApi.as_view(), name='weather'),
]