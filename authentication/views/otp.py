from django.contrib.auth.views import LoginView
from django.utils import timezone

from ..forms.otp import TOTPLoginForm
from ..mixins.session import AuthSessionRequiredMixin
from frontend.mixins.views import TitleMixin


class TOTPLoginView(TitleMixin, AuthSessionRequiredMixin, LoginView):
    form_class = TOTPLoginForm
    title = "Verify"
    template_name = "auth/totplogin.html"

    def form_valid(self, form):
        self.request.session["LastActivity"] = timezone.now().timestamp()
        return super().form_valid(form)