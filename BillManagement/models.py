from django.db import models
from decimal import Decimal
from Accounts.models import User
from DoctorManagement.models import Doctor
from AppointmentManagement.models import Appointment
from django.core.exceptions import ValidationError
# Create your models here.

class Bill(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bills"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="bills"
    )
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="bill"
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )
    def clean(self):
        if self.discount > self.consultation_fee:
            raise ValidationError(
                "Discount cannot be greater than consultation fee."
            )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.consultation_fee - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.id}"