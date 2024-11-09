from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        max_length=255,
        label="password",
        style={"input_type": "password"},
    )
    password1 = serializers.CharField(
        write_only=True,
        max_length=255,
        label="confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("email", "password", "password1")

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise ValidationError({"details": "Passwords do not match"})

        try:
            validate_password(attrs.get("password"))
        except ValidationError as e:
            raise ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "user is not verified."})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified."})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        try:
            validate_password(attrs.get("new_password"))
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": _("User does not exist")})

        if user_obj.is_verified:
            raise serializers.ValidationError({"detail": _("User is already verified")})
        attrs["user"] = user_obj
        return super().validate(attrs)


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise ValidationError({"detail": "There is no user with provided email"})
        attrs["user"] = user
        return super().validate(attrs)


class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ["token"]

    def validate(self, attrs):
        token = attrs["token"]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            return ValidationError({"detail": "Token expired"})
        except jwt.exceptions.DecodeError:
            raise ValidationError({"detail": "Token invalid"})

        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ["password", "password1", "token"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"details": "Passwords does not match"})
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            user.set_password(password)
            user.save()

            return super().validate(attrs)
        except Exception:
            raise AuthenticationFailed("The reset link is invalid", 401)
