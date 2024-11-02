from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # login token
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    # path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

]
