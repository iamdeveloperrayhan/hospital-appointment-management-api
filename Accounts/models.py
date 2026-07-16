from django.db import models
from django.contrib.auth.models import AbstractUser
from Accounts.managers import UserManager
# Create your models here.

class User(AbstractUser):
    username = None

    USER_TYPE_CHOICES = (
        ("user", "User"),
        ("doctor", "Doctor"),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="user"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return self.email