from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from allauth.socialaccount.providers.openid_connect.views import OpenIDConnectAdapter


class OIDCAdapter(OpenIDConnectAdapter):
    provider_id = "oidc"


oidc_login = OAuth2LoginView.adapter_view(OIDCAdapter)
oidc_callback = OAuth2CallbackView.adapter_view(OIDCAdapter)
