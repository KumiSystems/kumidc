from django.dispatch import receiver

from oidc_provider.signals import user_accept_consent, user_decline_consent

from ..models import AuthorizationLog


@receiver(user_accept_consent)
def consent_granted(sender, **kwargs):
    AuthorizationLog.objects.create(user=kwargs["user"], client=kwargs["client"], scope=kwargs["scope"], granted=True)


@receiver(user_decline_consent)
def consent_denied(sender, **kwargs):
    AuthorizationLog.objects.create(user=kwargs["user"], client=kwargs["client"], scope=kwargs["scope"], granted=False)