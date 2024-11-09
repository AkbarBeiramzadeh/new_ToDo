from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ActivationResendSerializer,
    PasswordResetRequestEmailSerializer,
    PasswordResetTokenVerificationSerializer,
    SetNewPasswordSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .. import utils

from rest_framework import mixins

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password change successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            # token = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_object = User.objects.get(pk=user_id)

        if user_object.is_verified:
            return Response({"details": "your account has already been verified."})
        user_object.is_verified = True
        user_object.save()

        return Response(
            {"details": "your account have been verified and activated successfully."}
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation email resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class PasswordResetRequestEmailApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token
        relativeLink = "/accounts/reset-password/set-password"  # reverse('accounts:password-reset-confirm')
        current_site = get_current_site(request=request).domain
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi '+user.email + \
        #         'Use the link below to reset your password \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #             'email_subject': 'Verify your email'}

        # Util.send_email(data)
        data = {"email": user.email, "link": absurl, "site": current_site}
        utils.Util.send_templated_email("email/reset_password_template.html", data)
        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordResetTokenValidateApiView(
    mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = PasswordResetTokenVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)


class PasswordResetSetNewApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"detail": "Password reset successfully"}, status=status.HTTP_200_OK
        )
