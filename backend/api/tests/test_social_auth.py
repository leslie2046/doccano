from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.adapter import OIDCSocialAccountAdapter


@override_settings(SOCIALACCOUNT_PROVIDERS={"openid_connect": {"SERVERS": []}})
class SocialLinksAPITest(APITestCase):
    def test_returns_empty_response_when_oidc_is_not_configured(self):
        response = self.client.get("/v1/social/links/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


@override_settings(
    SOCIALACCOUNT_PROVIDERS={
        "openid_connect": {
            "SERVERS": [
                {
                    "id": "oidc",
                    "name": "GitLab",
                    "server_url": "https://gitlab.example.com",
                    "APP": {"client_id": "client-id", "secret": "client-secret"},
                    "SCOPE": ["openid", "profile", "email"],
                    "OAUTH_PKCE_ENABLED": True,
                }
            ]
        }
    }
)
class ConfiguredSocialLinksAPITest(APITestCase):
    def test_returns_oidc_link_when_provider_is_configured(self):
        response = self.client.get("/v1/social/links/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "oidc": {
                    "type": "oidc",
                    "label": "GitLab",
                    "href": reverse("oidc_login"),
                }
            },
        )


class OIDCSocialAccountAdapterTest(TestCase):
    def setUp(self):
        self.adapter = OIDCSocialAccountAdapter()
        self.request = RequestFactory().get("/")

    def make_sociallogin(self, extra_data):
        user = get_user_model()()
        account = SimpleNamespace(provider="oidc", extra_data=extra_data)
        return SimpleNamespace(user=user, account=account)

    def test_populate_user_prefers_email_for_generated_username(self):
        sociallogin = self.make_sociallogin(
            {
                "sub": "subject-123",
                "email": "alice@example.com",
                "preferred_username": "alice-login",
            }
        )

        user = self.adapter.populate_user(
            self.request,
            sociallogin,
            {"email": "alice@example.com", "username": None, "name": None},
        )

        self.assertEqual(user.email, "alice@example.com")
        self.assertEqual(user.username, "alice")

    def test_populate_user_falls_back_to_subject_when_other_claims_are_missing(self):
        sociallogin = self.make_sociallogin({"sub": "subject-123"})

        user = self.adapter.populate_user(
            self.request,
            sociallogin,
            {"email": None, "username": None, "name": None},
        )

        self.assertEqual(user.username, "subject-123")
