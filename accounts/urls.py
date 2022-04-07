from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Registration URLS
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset URLS
    path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Account URLS
    path("account/", views.account, name="account"),
    path("account/funds/add/bank/", views.add_funds_bank, name="add_funds_bank"),
    path("account/funds/add/crypto/", views.add_funds_crypto, name="add_funds_crypto"),
    path("account/funds/withdraw/", views.withdraw_funds, name="withdraw_funds"),
]
