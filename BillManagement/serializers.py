from rest_framework import serializers
from .models import Bill
from Accounts.stabilizer import UserSerializer
from DoctorManagement.stabilizer import DoctorSerializer

class BillSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = "__all__"
        read_only_fields = (
            "patient",
            "doctor",
            "total_amount",
        )

    def validate_appointment(self, value):
        if value.status != "Completed":
            raise serializers.ValidationError(
                "Bill can only be created for completed appointments."
            )

        if hasattr(value, "bill"):
            raise serializers.ValidationError(
                "This appointment already has a bill."
            )

        return value

    def create(self, validated_data):
        appointment = validated_data["appointment"]
        validated_data["patient"] = appointment.patient
        validated_data["doctor"] = appointment.doctor
        return super().create(validated_data)