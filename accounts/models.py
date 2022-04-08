from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_private = models.BooleanField(default=False)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    def update_balance(self, update_amount):
        self.current_balance += update_amount
        self.save()