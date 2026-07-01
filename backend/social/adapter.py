from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class OIDCSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if sociallogin.account.provider != "oidc":
            return user

        username = getattr(user, "username", "")
        if username:
            return user

        extra_data = sociallogin.account.extra_data or {}
        email = data.get("email") or extra_data.get("email")
        preferred_username = data.get("username") or extra_data.get("preferred_username")
        subject = extra_data.get("sub")
        username_candidates = [email, preferred_username, subject, "user"]
        user.username = get_account_adapter(request).generate_unique_username(username_candidates)
        return user
