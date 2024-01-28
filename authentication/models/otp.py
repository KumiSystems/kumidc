from django.db import models
from django.contrib.auth import get_user_model

from annoying.fields import AutoOneToOneField
from pyotp import TOTP, random_base32

from datetime import datetime


class TOTPSecret(models.Model):
    """A secret for a user's TOTP device

    Attributes:
        user: The user to whom this secret belongs
        secret: The secret
        active: Whether this secret is currently active
    """

    user = AutoOneToOneField(get_user_model(), models.CASCADE, primary_key=True)
    secret = models.CharField(max_length=32, default=random_base32)
    active = models.BooleanField(default=False)

    def verify(self, token: str, window: int = 1, set_used=True) -> bool:
        """Verify a TOTP token

        Args:
            token (str): The token to verify
            window (int, optional): The number of tokens to check before and after the current token. Defaults to 1.

        Returns:
            bool: Whether the token was valid
        """

        if not self.active:
            return False

        if UsedTOTPToken.is_used(self, token):
            return False

        if TOTP(self.secret).verify(token, valid_window=window):
            if set_used:
                UsedTOTPToken.objects.create(secret=self, token=token)
            return True

        return False

    def get_uri(self) -> str:
        """Get the provisioning URI for this secret

        This is used to generate a QR code for the user to scan with their TOTP device.

        Returns:
            str: The provisioning URI
        """
        return TOTP(self.secret).provisioning_uri(
            name=self.user.email, issuer_name="KumiDC"
        )

    def change_secret(self) -> str:
        """Change the secret for this user

        This generates a new secret and saves it to the database.

        Returns:
            str: The new secret
        """

        self.secret = random_base32()
        self.save()
        return self.secret


class UsedTOTPToken(models.Model):
    """A TOTP token that has been used

    We log these so that we can prevent replay attacks.

    Attributes:
        secret: The secret that was used
        token: The token that was used
        timestamp: When the token was used
        expiry: How long we should keep this token for
    """
    secret = models.ForeignKey(TOTPSecret, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expiry = self.timestamp + timedelta(seconds=60)
        super().save(*args, **kwargs)

    @classmethod
    def is_used(cls, secret: TOTPSecret, token: str) -> bool:
        """Check whether a token has been used

        Args:
            secret (TOTPSecret): The secret that was used
            token (str): The token that was used

        Returns:
            bool: Whether the token has recently been used
        """
        return cls.objects.filter(secret=secret, token=token, expiry__gte=datetime.now()).exists()