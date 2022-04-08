from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_private = models.BooleanField(default=False)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    skill_level = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=200, blank=True)

    def update_balance(self, update_amount):
        self.current_balance += update_amount
        self.save()