from django.views.generic import TemplateView
from django.urls import reverse_lazy

from ..mixins.views import TitleMixin
from authentication.mixins.timeout import TimeoutMixin


class AuthorizationLogView(TimeoutMixin, TitleMixin, TemplateView):
    title = "My Authorizations"
    template_name = "frontend/authorization_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_url"] = reverse_lazy("frontend:authorization_log_data")
        return context