from django.utils import timezone


def session_expiry(start=None, validity=timezone.timedelta(seconds=300)):
    start = start or timezone.now()
    return start + validity