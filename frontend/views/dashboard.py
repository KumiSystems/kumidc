from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy

from ..mixins.views import TitleMixin
from authentication.mixins.timeout import TimeoutMixin


class IndexView(RedirectView):
    url = reverse_lazy("frontend:dashboard")

class DashboardView(TimeoutMixin, TitleMixin, TemplateView):
    title = "Dashboard"
    template_name = "frontend/dashboard.html"