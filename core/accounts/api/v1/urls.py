from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # login token
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # JWT
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    # change password
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password')

    # activation
    path('activation/confirm/<str:token>', views.ActivationApiView.as_view(), name='activation'),

    # resend activation
    path('activation/resend/', views.ActivationResendApiView.as_view(), name='activation-resend'),

]
