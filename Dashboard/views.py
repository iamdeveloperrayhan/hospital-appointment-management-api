from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from DoctorManagement.models import Doctor
from AppointmentManagement.models import Appointment

User = get_user_model()

# Create your views here.

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_patients = User.objects.filter(
            user_type="user",
            patient_appointments__isnull=False,
        ).distinct().count()
        total_doctors = Doctor.objects.count()
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(
            status="Pending"
        ).count()
        completed_appointments = Appointment.objects.filter(
            status="Completed"
        ).count()
        data = {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "pending_appointments": pending_appointments,
            "completed_appointments": completed_appointments,
        }

        return Response(data)