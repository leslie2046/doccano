from django.conf import settings
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView


class Social(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        providers = settings.SOCIALACCOUNT_PROVIDERS.get("openid_connect", {})
        servers = providers.get("SERVERS", [])
        if not servers:
            return Response({})

        oidc = servers[0]
        return Response(
            {
                "oidc": {
                    "type": "oidc",
                    "label": oidc.get("name", "OpenID Connect"),
                    "href": reverse("oidc_login"),
                }
            }
        )
