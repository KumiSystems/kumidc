from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from authentication.forms.otp import TOTPLoginForm
from authentication.mixins.timeout import TimeoutMixin
from ..mixins.views import TitleMixin


class TOTPActivationView(TitleMixin, TimeoutMixin, LoginView):
    authentication_form = TOTPLoginForm
    template_name = "frontend/activate_totp.html"
    title = "Activate Two-Factor Authentication"

    def form_valid(self, form):
        token = self.request.user.totpsecret
        token.active = True
        token.save()

        messages.success(self.request, "Two-factor authentication was enabled for your account.")

        return HttpResponseRedirect(self.get_success_url())


class TOTPDeactivationView(TitleMixin, TimeoutMixin, LoginView):
    authentication_form = TOTPLoginForm
    template_name = "frontend/deactivate_totp.html"
    title = "Disable Two-Factor Authentication"

    def form_valid(self, form):
        token = self.request.user.totpsecret
        token.active = False
        token.save()
        token.change_secret()

        messages.success(self.request, "Two-factor authentication was disabled for your account.")

        return HttpResponseRedirect(self.get_success_url())


class TOTPDispatcherView(TimeoutMixin, RedirectView):
    def get_redirect_url(self):
        if self.request.user.totpsecret.active:
            return reverse_lazy("frontend:deactivate_totp")
        return reverse_lazy("frontend:activate_totp")