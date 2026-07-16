from rest_framework import serializers
from .models import Doctor
from Accounts.models import User

class DoctorSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email")
    full_name = serializers.CharField(source="user.full_name")
    phone_number = serializers.CharField(source="user.phone_number")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "password",
            "department",
            "specialization",
            "visiting_fee"
        ]

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", {})
        user = instance.user
        user.email = user_data.get("email", user.email)
        user.full_name = user_data.get("full_name", user.full_name)
        user.phone_number = user_data.get("phone_number", user.phone_number)

        if "password" in validated_data:
            user.set_password(validated_data.pop("password"))
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            email=user_data["email"],
            full_name=user_data["full_name"],
            phone_number=user_data["phone_number"],
            password=validated_data.pop("password"),
            user_type="doctor"
        )

        doctor = Doctor.objects.create(
            user=user,
            **validated_data
        )

        return doctor