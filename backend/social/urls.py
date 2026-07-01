from django.urls import path

from .oidc import oidc_callback, oidc_login

urlpatterns = [
    path("login/oidc/", oidc_login),
    path("complete/oidc/", oidc_callback),
]
