from djangosaml2idp.views import ProcessMultiFactorView

from authentication.mixins.timeout import TimeoutMixin


class SAMLMultiFactorView(TimeoutMixin, ProcessMultiFactorView):
    pass
