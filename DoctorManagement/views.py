from .models import Doctor
from DoctorManagement.stabilizer import DoctorSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Q

class DoctorListCreateAPIView(ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get("department")
        doctor_id = self.request.query_params.get("doctor")
        search = self.request.query_params.get("search")
        visiting_fee = self.request.query_params.get("ordering")

        if department:
            queryset = queryset.filter(department=department)

        if doctor_id:
            queryset = queryset.filter(id=doctor_id)
            
        if search:
            queryset = queryset.filter(Q(user__full_name__icontains=search))
                
        if visiting_fee:
            queryset = queryset.order_by(visiting_fee)

        return queryset
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


class DoctorDetailUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    