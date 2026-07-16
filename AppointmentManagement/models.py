from django.db import models
from DoctorManagement.models import Doctor
from Accounts.models import User
# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
        limit_choices_to={"user_type": "user"}
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor}"