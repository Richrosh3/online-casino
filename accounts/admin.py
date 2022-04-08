from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Class defining the Admin user, inheriting from Django's UserAdmin class and using our CustomUser model,
    as defined in models.py"""
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["email", "username", "skill_level", "bio", "birthday"]
    fieldsets = None
    fields = ["skill_level", "bio", "birthday"]


admin.site.register(CustomUser, CustomUserAdmin)
