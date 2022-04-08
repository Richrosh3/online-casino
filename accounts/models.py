from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Class representing the model for a user of the Online Casino. Associated with each user is a username, password,
    first and last name, email address, account type (public or private), birthday, skill level, bio, as well as the
    current account balance and total earnings over time
    """

    is_private = models.BooleanField(default=False)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    skill_level = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=200, blank=True)

    def update_balance(self, update_amount: Decimal) -> None:
        """
        Updates a user's current account balance, incrementing it by the specified value.

        Args:
            update_amount:  Decimal value representing the amount by which to change the account balance. Use a negative
                            number to decrement the value.
        """
        self.current_balance += update_amount
        self.save()
