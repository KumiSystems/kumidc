from django.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4

from ..helpers.session import session_expiry


class AuthSession(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    expiry = models.DateTimeField(default=session_expiry)