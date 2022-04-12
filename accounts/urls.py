from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    # Registration URLS
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset URLS
    path('password/reset/',
         auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm,
                                              email_template_name='registration/password_reset_email_c.html',
                                              template_name='registration/password_reset_form_c.html'),
         name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_c.html'),
         name='password_reset_confirm'),
    path('password/reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_c.html'),
         name='password_reset_done'),
    path('password/reset/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_c.html'),
         name='password_reset_complete'),

    # Account URLS
    path("account/", views.AccountView.as_view(), name="account"),
    path("account/funds/add/bank/", views.AddFundsBankView.as_view(), name="add_funds_bank"),
    path("account/funds/add/crypto/", views.AddFundsCryptoView.as_view(), name="add_funds_crypto"),
    path("account/funds/withdraw/", views.withdraw_funds, name="withdraw_funds"),
]
