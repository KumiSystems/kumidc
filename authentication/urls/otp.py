from django.urls import path

from ..views.otp import TOTPLoginView


urlpatterns = [
    path('login/totp/', TOTPLoginView.as_view(), name="totplogin"),
]
