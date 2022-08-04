from django.urls import path

from .login import urlpatterns as loginpatterns
from .otp import urlpatterns as otppatterns
from .reverify import urlpatterns as reverifypatterns


urlpatterns = [] + loginpatterns + otppatterns + reverifypatterns
