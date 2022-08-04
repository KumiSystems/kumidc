from django.utils import timezone


def session_expiry(start=timezone.now(), validity=timezone.timedelta(seconds=300)):
    return start + validity