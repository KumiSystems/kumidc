from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..forms.otp import TOTPLoginForm
from frontend.mixins.views import TitleMixin


class ReverifyView(TitleMixin, LoginView):
    template_name = "auth/reverify.html"
    form_class = TOTPLoginForm
    title = "Reverify"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["LastActivity"] = timezone.now().timestamp()
        return HttpResponseRedirect(self.get_success_url())