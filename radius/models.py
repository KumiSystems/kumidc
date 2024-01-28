from django.db import models
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta

from cidrfield.models import IPNetworkField


class RadiusChallengeChoice(models.TextChoices):
    NONE = "none", "None"
    TOTP = "totp", "Time-based One-time Password"
    WEB = "web", "Web-based"

class RadiusUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    challenge = models.CharField(
        max_length=255, choices=RadiusChallengeChoice.choices, default=RadiusChallengeChoice.NONE
    )

class RadiusNetwork(models.Model):
    name = models.CharField(max_length=255)
    network = IPNetworkField()


class RadiusUserIP(models.Model):
    user = models.ForeignKey(RadiusUser, on_delete=models.CASCADE)
    network = models.ForeignKey(RadiusNetwork, on_delete=models.CASCADE)
    ipv4_address = models.GenericIPAddressField(protocol="ipv4", null=True, blank=True)
    ipv6_prefix = models.GenericIPAddressField(protocol="ipv6", null=True, blank=True)

    class Meta:
        unique_together = ("user", "network")

    def save(self, *args, **kwargs):
        if not self.ip_address in self.network.network:
            raise ValueError(
                f"IPv4 address {self.ip_address} not in network {self.network.network}"
            )
        if not self.ipv6_prefix in self.network.network:
            raise ValueError(
                f"IPv6 prefix {self.ipv6_prefix} not in network {self.network.network}"
            )

        super().save(*args, **kwargs)


class RadiusAccountingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(RadiusUser, on_delete=models.CASCADE)
    ip = models.ForeignKey(RadiusUserIP, on_delete=models.CASCADE)

    start_time = models.DateTimeField(null=True, blank=True)
    stop_time = models.DateTimeField(null=True, blank=True)

    def start(self):
        self.start_time = datetime.now()
        self.save()

    def stop(self):
        self.stop_time = datetime.now()
        self.save()


class RadiusAccountingEvent(models.Model):
    session = models.ForeignKey(RadiusAccountingSession, on_delete=models.CASCADE)

    event_type = models.CharField(max_length=255)
    event_time = models.DateTimeField(auto_now_add=True)
    raw_data = models.TextField()


class RadiusWebAuthentication(models.Model):
    user = models.ForeignKey(RadiusUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    ip = models.IPAddressField()

    def save(self, *args, **kwargs):
        self.expiry = self.timestamp + timedelta(minutes=5)
        super().save(*args, **kwargs)