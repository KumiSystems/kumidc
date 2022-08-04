from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages

from ..models.session import AuthSession


class TOTPLoginForm(forms.Form):
    token = forms.IntegerField(max_value=10**9-1, min_value=0)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_token(self):
        token = str(self.cleaned_data.get('token')).zfill(6)

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            sessionid = self.request.session["AuthSession"]
            session = AuthSession.objects.get(sessionid)
            user = session.user

        if user.totpsecret.verify(token):
            self.user_cache = user
        else:
            messages.error(self.request, "The token you entered is incorrect. Please try again.")
            raise ValidationError("The token you entered is incorrect. Please try again.")

        return token