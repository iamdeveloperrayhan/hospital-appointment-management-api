from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "phone_number",
            "address",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "address",
            "date_joined",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist."
            )

        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate(self, attrs):
        email = attrs.get("email")
        token = attrs.get("token")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid user."
            )
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                "Invalid or expired token."
            )
        attrs["user"] = user
        return attrs
