from django.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4

from jwt import decode, InvalidTokenError

class AppKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    device = models.CharField(max_length=255)
    key = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.device}"

    def validateJWT(self, jwt):
        try:
            return decode(jwt, self.key, algorithms=['HS256'])
        except InvalidTokenError:
            return False

class AppSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    used = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    @property
    def valid(self):
        return self.created > timezone.now() - timezone.timedelta(minutes=5)
    
    @classmethod
    def get_for_user(cls, user, create = True):
        assert user

        if not user.appkey_set.filter(active=True).exists():
            return

        user_sessions = cls.objects.filter(user=user)

        for session in user_sessions:
            if session.valid and not session.used:
                return session

        if create:
            return cls.objects.create(user=user)
