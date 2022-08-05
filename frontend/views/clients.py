from django.views.generic import TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from oidc_provider.models import Client

from ..mixins.views import TitleMixin
from ..forms.client import ClientEditForm, ClientCreateForm
from authentication.mixins.timeout import TimeoutMixin


class ClientView(TimeoutMixin, TitleMixin, TemplateView):
    title = "My Apps"
    template_name = "frontend/client_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_url"] = reverse_lazy("frontend:client_list_data")
        return context


class ClientEditView(TimeoutMixin, TitleMixin, UpdateView):
    model = Client
    form_class = ClientEditForm
    template_name = "frontend/client_edit.html"
    title = "Edit App"

    def get_object(self, queryset=None):
        return get_object_or_404(Client, owner=self.request.user, client_id=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("frontend:client_edit", args=(self.object.client_id,))


class ClientCreateView(TimeoutMixin, TitleMixin, CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = "frontend/client_edit.html"
    title = "Edit App"

    def get_object(self, queryset=None):
        return get_object_or_404(Client, owner=self.request.user, client_id=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("frontend:client_edit", args=(self.object.client_id,))