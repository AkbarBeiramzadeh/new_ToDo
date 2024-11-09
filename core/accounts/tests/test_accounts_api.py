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
def user(api_client):
    user = User.objects.create_user(
        email="test@example.com",
        password="AsAs1020",
    )
    user.is_verified = True
    user.save()
    api_client.force_authenticate(user=user)
    return user


@pytest.mark.django_db
class TestAccountsApi:
    def test_registration(self, api_client):
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "newuser@example.com",
            "password": "AsAs1020",
            "password1": "AsAs1020",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 201
        assert response.data["email"] == "newuser@example.com"

    def test_token_login_user_is_not_verified(self, api_client):
        data = {"email": "test@example.com", "password": "AsAs1020"}
        url = reverse("accounts:api-v1:token-login")
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    def test_token_logout(self, api_client):
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "newuser@example.com",
            "password": "AsAs1020",
            "password1": "AsAs1020",
        }
        register_response = api_client.post(url, data=data)
        assert register_response.status_code == 201

        url_token_login = reverse("accounts:api-v1:token-login")
        user_obj = User.objects.get(email="newuser@example.com")
        user_obj.is_verified = True
        user_obj.save()
        token_login_response = api_client.post(
            url_token_login,
            data={"email": data.get("email"), "password": data.get("password")},
        )

        assert token_login_response.status_code == 200

        api_client.force_authenticate(user=user_obj)
        url_token_logout = reverse("accounts:api-v1:token-logout")
        response = api_client.post(url_token_logout)
        assert response.status_code == 204

    def test_jwt_create(self, api_client, user):
        url = reverse("accounts:api-v1:jwt-create")
        response = api_client.post(
            url, data={"email": user.email, "password": "AsAs1020"}
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_jwt_refresh(self, api_client, user):
        url = reverse("accounts:api-v1:jwt-refresh")
        refresh_token = RefreshToken.for_user(user)
        response = api_client.post(url, {"refresh": str(refresh_token)})
        assert response.status_code == 200
        assert "access" in response.data

    def test_jwt_verify(self, api_client, user):
        url = reverse("accounts:api-v1:jwt-verify")
        access_token = RefreshToken.for_user(user)
        response = api_client.post(url, {"token": str(access_token)})
        assert response.status_code == 200

    def test_change_password(self, api_client, user):
        url = reverse("accounts:api-v1:change-password")
        response = api_client.put(
            url,
            {
                "old_password": "AsAs1020",
                "new_password": "newpassword123",
                "new_password1": "newpassword123",
            },
        )
        assert response.status_code == 200

    def test_reset_password_request(self, api_client, user):
        url = reverse("accounts:api-v1:reset-password-request")
        response = api_client.post(url, {"email": "test@example.com"})
        assert response.status_code == 200

    def test_reset_password_validate_token_with_invalid_token(self, api_client):
        url = reverse("accounts:api-v1:reset-password-validate")
        response = api_client.post(url, {"token": "invalid-token"})
        assert response.status_code == 400

    def test_reset_password_confirm(self, api_client, user):
        api_client.force_authenticate(user=user)
        url_get_jwt_token = reverse("accounts:api-v1:jwt-create")
        data = {"email": user.email, "password": "AsAs1020"}
        response = api_client.post(url_get_jwt_token, data=data)

        assert "access" in response.data

        url = reverse("accounts:api-v1:reset-password-confirm")
        response = api_client.patch(
            url,
            {
                "token": response.data["access"],
                "password": "newPassword123",
                "password1": "newPassword123",
            },
        )
        assert response.status_code == 200

    def test_activation(self, api_client, user):
        url_get_jwt_token = reverse("accounts:api-v1:jwt-create")
        data = {"email": user.email, "password": "AsAs1020"}
        response = api_client.post(url_get_jwt_token, data=data)

        url = reverse(
            "accounts:api-v1:activation", kwargs={"token": response.data["access"]}
        )
        response = api_client.get(url)
        assert response.status_code == 200

    def test_activation_resend(self, api_client):
        User.objects.create_user(email="a1@email.com", password="123")
        url = reverse("accounts:api-v1:activation-resend")
        data = {"email": "a1@email.com"}
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_activation_resend_with_anonymous_user(self, api_client):
        url = reverse("accounts:api-v1:activation-resend")
        data = {"email": "anonymouse_user@email.com"}
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    def test_activation_resend_with_user_verified_already(self, api_client):
        user = User.objects.create_user(email="a1@email.com", password="123")
        user.is_verified = True
        user.save()
        url = reverse("accounts:api-v1:activation-resend")
        data = {"email": "a1@email.com"}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
