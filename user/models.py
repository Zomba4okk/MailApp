from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=20, unique=False)

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
