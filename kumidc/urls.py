from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    path('openid/', include('oidc_provider.urls', 'oidc_provider')),
    path('saml/', include('djangosaml2idp.urls', 'djangosaml2idp')),
    path('cas/', include('cas_server.urls', "cas_server")),

    path('admin/login/', RedirectView.as_view(url=reverse_lazy("auth:login"), query_string=True)),
    path('admin/', admin.site.urls),
    
    path('auth/', include(("authentication.urls", "auth"))),
    path('', include(("frontend.urls", "frontend"))),
]
