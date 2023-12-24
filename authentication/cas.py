from cas_server.auth import DjangoAuthUser

from django.contrib.auth import get_user_model

class KumiDCAuthUser(DjangoAuthUser):
    def __init__(self, username):
        User = get_user_model()
        try:
            self.user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            pass
        super(DjangoAuthUser, self).__init__(username)