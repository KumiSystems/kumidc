from ..models import TOTPSecret


def has_otp(user):
    try:
        return bool(len(TOTPSecret.objects.filter(user=user, active=True)))
    except TOTPSecret.DoesNotExist:
        return False