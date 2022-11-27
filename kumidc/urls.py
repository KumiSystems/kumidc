from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    re_path(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    
    re_path(r'^saml/', include('djangosaml2idp.urls')),

    path('admin/login/', RedirectView.as_view(url=reverse_lazy("auth:login"), query_string=True)),
    path('admin/', admin.site.urls),
    
    path('auth/', include(("authentication.urls", "auth"))),
    path('', include(("frontend.urls", "frontend"))),
]
