from django.urls import path

from .oidc import oidc_callback, oidc_login
from .views import Social

urlpatterns = [
    path("links/", Social.as_view()),
    path("login/oidc/", oidc_login, name="oidc_login"),
    path("complete/oidc/", oidc_callback, name="oidc_callback"),
]
