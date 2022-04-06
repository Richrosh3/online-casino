from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path("account/", views.account, name="account"),
    path("account/funds/add/bank/", views.add_funds_bank, name="add_funds_bank"),
    path("account/funds/add/crypto/", views.add_funds_crypto, name="add_funds_crypto"),
    path("account/funds/withdraw/", views.add_funds_crypto, name="withdraw_funds"),
]
