from django.urls import path

from .views.dashboard import IndexView, DashboardView
from .views.password import PasswordChangeView
from .views.otp import TOTPActivationView, TOTPDeactivationView, TOTPDispatcherView


urlpatterns = [
    path("", IndexView.as_view()),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/change_password/", PasswordChangeView.as_view(), name="change_password"),
    path("profile/totp/", TOTPDispatcherView.as_view(), name="totp"),
    path("profile/totp/activate/", TOTPActivationView.as_view(), name="activate_totp"),
    path("profile/totp/deactivate/", TOTPDeactivationView.as_view(), name="deactivate_totp"),
]