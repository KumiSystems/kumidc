from django.db import models
from django.contrib.auth import get_user_model

from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField
from annoying.fields import AutoOneToOneField


class Profile(models.Model):
    user = AutoOneToOneField(get_user_model(), models.CASCADE)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    middle_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    nickname = models.CharField(max_length=128, null=True, blank=True)
    preferred_username = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)
    zoneinfo = TimeZoneField(choices_display="WITH_GMT_OFFSET", null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email_verified = models.DateTimeField(null=True, blank=True)
    phone_number_verified = models.DateTimeField(null=True, blank=True)