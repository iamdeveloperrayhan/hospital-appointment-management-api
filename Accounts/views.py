from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.generics import (
        CreateAPIView,
    )
from .stabilizer import (
        RegisterSerializer,
        UserSerializer,
        ForgotPasswordSerializer,
        ResetPasswordSerializer,

    )
User = get_user_model()

# Create your views here.


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class ProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ForgotPasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_link = (f"http://localhost:3000/reset-password/?email={email}&token={token}")

        send_mail(
            subject="Password Reset Request",
            message=f"""Hello {user.full_name}, Click this link to reset your password: {reset_link} , If you want to reset your password so use this token {token} on your token field Or If you did not request this, ignore this email.""",
            from_email="noreply@example.com",
            recipient_list=[email],
        )

        return Response(
            {
                "message":"Password reset link sent to your email."
            }, status=status.HTTP_200_OK
        )



class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        return Response(
            {
                "message":"Password reset successfully."
            },status=status.HTTP_200_OK
        )
    
