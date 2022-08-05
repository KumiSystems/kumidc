from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url

from urllib.parse import urlparse

from ..models.otp import TOTPSecret


class TimeoutMixin:
    def dispatch(self, request, *args, **kwargs):
        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(settings.LOGIN_URL)
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = request.get_full_path()

        if request.user.is_authenticated:
            if not request.session.get("LastActivity"):
                messages.error(request, "Something went terribly wrong, please try logging in again.")
                logout(request)
            elif request.session["LastActivity"] < (timezone.now() - timezone.timedelta(minutes=settings.REVERIFY_AFTER_INACTIVITY_MINUTES)).timestamp():
                try:
                    assert request.user.totpsecret.active
                    return redirect_to_login(path, resolve_url("auth:reverify"), REDIRECT_FIELD_NAME)
                except (AssertionError, TOTPSecret.DoesNotExist):
                    messages.error(
                        request, "Your session has timed out, please login again.")
                    logout(request)
                except:
                    messages.error(
                        request, "Something went wrong, please try logging in again."
                    )

            else:
                request.session["LastActivity"] = timezone.now().timestamp()
                return super().dispatch(request, *args, **kwargs)

        else:
            messages.error(request, "You have to login to access this page.")

        return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)
