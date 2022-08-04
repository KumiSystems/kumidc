from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.utils import timezone
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME, logout

from urllib.parse import urlparse

from ..models.otp import TOTPSecret


def authorize_hook(request, user, client):
    if request.session["LastActivity"] < (timezone.now() - timezone.timedelta(minutes=settings.REVERIFY_AFTER_INACTIVITY_MINUTES)).timestamp():
        try:
            assert user.totpsecret.active
            destination = reverse_lazy("auth:reverify")
        except (AssertionError, TOTPSecret.DoesNotExist):
            messages.error(request, "Your session has timed out, please login again.")
            logout(request)
            destination = reverse_lazy("auth:login")

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(destination)
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = request.get_full_path()     

        return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)
    else:
        return None