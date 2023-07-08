from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url

from ..models.session import AuthSession

# Somewhat shamelessly copied from django.contrib.auth.views
#
# Original source:
# https://github.com/django/django/blob/main/django/contrib/auth/views.py
#
# License:
# BSD 3-Clause "New" or "Revised" License
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/main/LICENSE

class AuthSessionRequiredMixin(RedirectURLMixin):
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if not request.session["AuthSession"]:
            if request.user.is_authenticated and self.redirect_authenticated_user:
                redirect_to = self.request.POST.get(
                    self.redirect_field_name,
                    self.request.GET.get(self.redirect_field_name, '')
                )
                url_is_safe = url_has_allowed_host_and_scheme(
                    url=redirect_to,
                    allowed_hosts=self.get_success_url_allowed_hosts(),
                    require_https=self.request.is_secure(),
                )
                url = redirect_to if url_is_safe else resolve_url(
                    settings.LOGIN_REDIRECT_URL)

                if url == self.request.path:
                    raise ValueError(
                        "Redirection loop for authenticated user detected. Check that "
                        "your LOGIN_REDIRECT_URL doesn't point to a login page."
                    )
                return HttpResponseRedirect(url)

            if not request.user.is_authenticated:
                messages.error(
                    request, "Could not identify your login session, please try again.")
                url = resolve_url(settings.LOGIN_URL)
                if params := request.GET.urlencode():
                    url += f"?{params}"
                return HttpResponseRedirect(url)

        if request.user.is_authenticated:
            logout(request)
            messages.error(
                request, "This shouldn't happen. Looks like you are logged in *and* logging in. Logged you out, just to be sure. Please try logging in again. Sorry!")
            request.session["AuthSession"] = None
            url = resolve_url(settings.LOGIN_URL)
            if params := request.GET.urlencode():
                url += f"?{params}"
            return HttpResponseRedirect(url)

        try:
            session = AuthSession.objects.get(
                id=request.session["AuthSession"])
            if session.expiry < timezone.now():
                request.session["AuthSession"] = None
                messages.error(
                    request, "Your session has expired. Please try logging in again.")
                url = resolve_url(settings.LOGIN_URL)
                if params := request.GET.urlencode():
                    url += f"?{params}"
                return HttpResponseRedirect(url)

        except AuthSession.DoesNotExist:
            request.session["AuthSession"] = None
            messages.error(
                request, "You are trying to access a session that doesn't exist...? Please try logging in again.")
            url = resolve_url(settings.LOGIN_URL)
            if params := request.GET.urlencode():
                url += f"?{params}"
            return HttpResponseRedirect(url)

        return super().dispatch(request, *args, **kwargs)


class OnlyLoggedOutMixin:
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, '')
            )

            url_is_safe = url_has_allowed_host_and_scheme(
                url=redirect_to,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )

            url = redirect_to if url_is_safe else resolve_url(
                settings.LOGIN_REDIRECT_URL)

            if url == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )

            return HttpResponseRedirect(url)

        return super().dispatch(request, *args, **kwargs)
