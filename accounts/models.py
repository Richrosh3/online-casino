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
    current_session = models.TextField(default='')
    total_earnings = models.FloatField(default=0.0)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    skill_level = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    monthly_limit = models.FloatField(default=-1)
    monthly_deposit_left = models.FloatField(default=0.0)
    next_monthly_reset = models.DateTimeField(auto_now=False, null=True)
    friends = models.ManyToManyField("CustomUser", blank=True)
    friend_requests = models.TextField(blank=True, max_length=None, default='')

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

    @staticmethod
    def check_username_exists(username: str) -> bool:
        """
        checks if the username exists
        Args:
            username: username of the user that is being checked

        Returns:
            true if the user exists, false if not
        """
        return CustomUser.objects.filter(username=username).exists()

    def send_friend_request(self, other_username: str) -> bool:
        """
        Sends a friend request to the user with the given username
        Args:
            other_username: username to which the friend request is being sent

        Returns:
            true if the friend request is sent, false otherwise
        """
        if self.check_username_exists(other_username):
            other_user = CustomUser.objects.get(username=other_username)
            already_friends = self.friends.filter(username=other_username).exists()
            already_requested = self.username in other_user.friend_requests.__str__().split("\n")

            if not already_friends and not already_requested and other_user.username != self.username:

                if other_user.friend_requests != "":
                    other_user.friend_requests += "\n"
                other_user.friend_requests += self.username

                other_user.save()
                self.save()
                return True
        return False

    def accept_friend_request(self, other_username: str) -> bool:
        """
        Accepts a friend request to the user with the given username
        Args:
            other_username: username of the friend request to accept

        Returns:
            true if the friend request is accepted, false otherwise
        """
        friend_requests = self.friend_requests.__str__().split("\n")
        if self.check_username_exists(other_username) and other_username in friend_requests:
            other_user = CustomUser.objects.get(username=other_username)
            self.friends.add(other_user)
            other_user.friends.add(self)

            friend_requests.remove(other_user.username)
            separator = "\n"
            self.friend_requests = separator.join(friend_requests)

            other_user.save()
            self.save()
            return True

        return False

    def remove_friend(self, other_username: str) -> bool:
        """
        Removes a friend with the username provided
        Args:
            other_username: username of the friend that should be removed

        Returns:
            true if the friend is removed, false otherwise
        """
        if self.check_username_exists(other_username):
            user_to_remove = CustomUser.objects.get(username=other_username)
            if self.friends.filter(username=user_to_remove.username).exists():
                self.friends.remove(user_to_remove)
                user_to_remove.friends.remove(self)
                return True
        return False

