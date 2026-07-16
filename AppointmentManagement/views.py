from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from core.permissions import AppointmentPermission

from django.db.models import Q

class AppointmentListCreateAPIView(ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = Appointment.objects.all()

        elif user.user_type == "user":
            queryset = Appointment.objects.filter(patient=user)

        elif user.user_type == "doctor":
            queryset = Appointment.objects.filter(doctor__user=user)

        else:
            queryset = Appointment.objects.none()


        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status__iexact=status)


        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(Q(patient__full_name__icontains=search))


        ordering = self.request.query_params.get("ordering")
        if ordering in ["appointment_date", "-appointment_date"]:
            queryset = queryset.order_by(ordering)

        return queryset


class AppointmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated,AppointmentPermission]
    