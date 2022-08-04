from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('auth/', include(("authentication.urls", "auth"))),
    path('', include(("frontend.urls", "frontend"))),
]
