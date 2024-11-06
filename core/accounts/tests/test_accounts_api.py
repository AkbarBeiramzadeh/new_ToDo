import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(
        email='test@example.com',
        password='AsAs1020',

    )
    user.is_verified = True
    return user


@pytest.fixture
def authed_client(api_client, user):
    client = api_client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestAccountsApi:
    def test_registration(self, api_client):
        url = reverse('accounts:api-v1:registration')
        data = {
            'email': 'newuser@example.com',
            'password': 'AsAs1020',
            'password1': 'AsAs1020'
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 201
        assert response.data["email"] == "newuser@example.com"

    def test_token_login_user_is_not_verified(self, api_client):
        data = {
            "email": "test@example.com",
            "password": "AsAs1020"
        }
        url = reverse('accounts:api-v1:token-login')
        response = api_client.post(url, data=data)
        assert response.status_code == 400


# def test_token_logout(authed_client):
#     url = reverse('token-logout')
#     response = client.post(url)
#     assert response.status_code == 204
#
#
# def test_jwt_create(authed_client):
#     url = reverse('jwt-create')
#     response = client.post(url)
#     assert response.status_code == 200
#     assert 'access' in response.data
#     assert 'refresh' in response.data
#
#
# def test_jwt_refresh(authed_client):
#     url = reverse('jwt-refresh')
#     refresh_token = RefreshToken.for_user(authed_client.user)
#     response = client.post(url, {'refresh': str(refresh_token)})
#     assert response.status_code == 200
#     assert 'access' in response.data
#
#
# def test_jwt_verify(authed_client):
#     url = reverse('jwt-verify')
#     access_token = RefreshToken.for_user(authed_client.user)
#     response = client.post(url, {'token': str(access_token)})
#     assert response.status_code == 200
#
#
# def test_change_password(authed_client):
#     url = reverse('change-password')
#     response = client.post(url, {'old_password': 'testpassword', 'new_password': 'newpassword123'})
#     assert response.status_code == 204
#
#
# def test_reset_password_request(client):
#     url = reverse('reset-password-request')
#     response = client.post(url, {'email': 'test@example.com'})
#     assert response.status_code == 204
#
#
# def test_reset_password_validate_token(client):
#     url = reverse('reset-password-validate')
#     response = client.post(url, {'token': 'some-valid-token'})
#     assert response.status_code == 200
#
#
# def test_reset_password_confirm(client):
#     url = reverse('reset-password-confirm')
#     response = client.post(url, {'token': 'some-valid-token', 'new_password': 'newpassword123'})
#     assert response.status_code == 204
#
#
# def test_activation(client):
#     url = reverse('activation', kwargs={'token': 'some-valid-token'})
#     response = client.post(url)
#     assert response.status_code == 204
#
#
# def test_activation_resend(client):
#     url = reverse('activation-resend')
#     response = client.post(url)
#     assert response.status_code == 204
