import datetime
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Class representing the model for a user of the Online Casino. Associated with each user is a username, password,
    first and last name, email address, account type (public or private), birthday, skill level, bio, as well as the
    current account balance and total earnings over time
    """

    is_private = models.BooleanField(default=False)
    current_balance = models.FloatField(default=0.0)
    total_earnings = models.FloatField(default=0.0)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    skill_level = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    monthly_limit = models.FloatField(default=-1)
    monthly_deposit_left = models.FloatField(default=0.0)
    next_monthly_reset = models.DateTimeField(auto_now=False, null=True)

    def withdraw(self, withdraw_amount: float) -> bool:
        """
        Withdraws the specified amount from user's account into linked bank account

        Args:
            withdraw_amount - float amount of money to withdraw from user's account

        Returns:
            boolean value indicating if transaction was successful
        """
        if withdraw_amount <= self.current_balance:
            self.current_balance = round(self.current_balance - withdraw_amount, 2)
            self.save()
            return True

        return False

    def deposit(self, deposit_amount: float) -> bool:
        """
        Deposits a certain amount of money from a crypto or bank account into user's account. Returns false if deposit
        exceeds monthly deposit limit. Returns true if deposit is successful. Will also check the next date for
        resetting monthly deposit limit and adjust it to one month in advance and refresh monthly deposit limit if
        current date exceeds next month's reset date.

        Args:
            deposit_amount - float amount of money to deposit into user's account

        Returns:
            boolean value indicating if transaction was successful
        """
        if self.monthly_limit > 0:
            if datetime.now(timezone.utc) >= self.next_monthly_reset:
                self.monthly_deposit_left = self.monthly_limit
                self.next_monthly_reset = datetime.now(timezone.utc) + relativedelta(months=1)
                self.save()

            if deposit_amount <= self.monthly_deposit_left:
                self.monthly_deposit_left -= deposit_amount
                self.current_balance = round(self.current_balance + deposit_amount, 2)
                self.save()
                return True

            return False

        else:
            self.current_balance = round(self.current_balance + deposit_amount, 2)
            self.save()
            return True

    def update_balance(self, update_amount: float) -> bool:
        """
        Updates a user's current account balance, incrementing it by the specified value.

        Args:
            update_amount:  Value representing the amount by which to change the account balance. Use a negative
                            number to decrement the value.

        Returns:
            true if the update succeeded, false otherwise
        """
        if update_amount >= 0 or self.current_balance >= -1 * update_amount:
            self.current_balance = round(self.current_balance + update_amount, 2)
            self.total_earnings = round(self.total_earnings + update_amount, 2)
            self.save()
            return True

        return False
