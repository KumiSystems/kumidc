from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..forms.otp import TOTPLoginForm
from ..models.app import AppSession
from frontend.mixins.views import TitleMixin


class ReverifyView(TitleMixin, LoginView):
    template_name = "auth/reverify.html"
    form_class = TOTPLoginForm
    title = "Reverify"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["LastActivity"] = timezone.now().timestamp()

        try:
            app_session = AppSession.objects.get(id=self.request.session["AppSession"])
            app_session.used = True
            app_session.save()
        except AppSession.DoesNotExist:
            pass

        return HttpResponseRedirect(self.get_success_url())