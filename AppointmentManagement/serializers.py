from rest_framework import serializers
from .models import Appointment
from Accounts.stabilizer import UserSerializer
from DoctorManagement.stabilizer import DoctorSerializer
from DoctorManagement.models import Doctor
from datetime import date

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source="doctor",
        write_only=True
    )
    
    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_id",
            "appointment_date",
            "appointment_time",
            "status",
            "created_at"
        ]
    def validate_appointment_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Past dates are not allowed."
            )
        return value
    
    def create(self, validated_data):
        validated_data["patient"] = self.context["request"].user
        return super().create(validated_data)
        