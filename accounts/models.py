import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
    monthly_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    monthly_deposit_left = Decimal(0.0)
    next_monthly_reset = models.DateTimeField(auto_now=False, null=True)

    def update_balance(self, update_amount: Decimal) -> None:
        """
        Updates a user's current account balance, incrementing it by the specified value.

        Args:
            update_amount:  Decimal value representing the amount by which to change the account balance. Use a negative
                            number to decrement the value.
        """
        self.current_balance = Decimal(update_amount) + Decimal(self.current_balance)
        if update_amount > Decimal(0.0):
            self.monthly_deposit_left -= update_amount
            print(self.monthly_deposit_left, self.next_monthly_reset)
        self.save()

    def update_monthly_limit(self) -> None:
        """
        Refreshes a user's monthly withdraw limit and defines the next month to reset monthly limit
        """

        if self.next_monthly_reset is None:
            print('Init monthly')
            self.next_monthly_reset = datetime.now() + relativedelta(months=1)
            self.monthly_deposit_left = Decimal(self.monthly_limit)

        elif self.next_monthly_reset < datetime.now():
            print('monthly reset', self.next_monthly_reset, datetime.now())
            self.monthly_deposit_left = Decimal(self.monthly_limit)

            while self.next_monthly_reset < datetime.now():
                self.next_monthly_reset += relativedelta(months=1)
                print(self.next_monthly_reset)
        self.save()
