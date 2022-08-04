from django.db import models
from django.contrib.auth import get_user_model

from annoying.fields import AutoOneToOneField
from pyotp import TOTP, random_base32


class TOTPSecret(models.Model):
    user = AutoOneToOneField(get_user_model(), models.CASCADE, primary_key=True)
    secret = models.CharField(max_length=32, default=random_base32)
    active = models.BooleanField(default=False)

    def verify(self, token):
        return TOTP(self.secret).verify(token)

    def get_uri(self):
        return TOTP(self.secret).provisioning_uri(name=self.user.email, issuer_name="KumiDC")

    def change_secret(self):
        self.secret = random_base32()
        self.save()
        return self.secret