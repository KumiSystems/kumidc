from django.urls import path

from ..views.reverify import ReverifyView


urlpatterns = [
    path("reverify/", ReverifyView.as_view(), name="reverify"),
]