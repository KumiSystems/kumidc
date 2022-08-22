from djangosaml2idp.processors import BaseProcessor


class SAMLProcessor(BaseProcessor):
    def enable_multifactor(self, user):
        return user.totpsecret.exists() and user.totpsecret.active