from django.db import models
from django.contrib.auth import get_user_model

from oidc_provider.models import Client


class AuthorizationLog(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    scope = models.TextField()
    granted = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)