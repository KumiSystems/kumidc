from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from frontend.mixins.views import TitleMixin
from ..mixins.session import OnlyLoggedOutMixin
from ..models.session import AuthSession
from ..helpers.otp import has_otp


class LoginView(OnlyLoggedOutMixin, TitleMixin, DjangoLoginView):
    template_name = "auth/login.html"
    title = "Login"

    def form_valid(self, form):
        if has_otp(user := form.get_user()):
            session = AuthSession.objects.create(user=user)
            self.request.session["AuthSession"] = str(session.id)
            return HttpResponseRedirect(reverse_lazy("auth:totplogin"))

        self.request.session["LastActivity"] = timezone.now().timestamp()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Could not log you in. Please check your email address and password, and try again.")
        return super().form_invalid(form)