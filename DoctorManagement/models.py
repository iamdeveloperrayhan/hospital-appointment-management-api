from django.db import models
from Accounts.models import User
from django.core.validators import MinValueValidator
# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150)
    visiting_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.user.full_name