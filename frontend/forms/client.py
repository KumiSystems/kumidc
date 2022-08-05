from django import forms

from oidc_provider.models import Client
from oidc_provider.admin import ClientForm


class ClientEditForm(ClientForm):
    class Meta:
        model = Client
        fields = ['name', 'client_type', 'response_types', 'jwt_alg', '_redirect_uris', 'client_id', 'client_secret']


class ClientCreateForm(ClientForm):
    class Meta:
        model = Client
        fields = ['name', 'client_type', 'response_types', 'jwt_alg', '_redirect_uris']