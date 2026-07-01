# Generic OIDC setup

This document explains how to configure a single OpenID Connect provider for doccano.

## Supported model

The current implementation supports one configurable OIDC provider at a time. You can point it at standards-compliant providers such as GitLab, Keycloak, Authentik, and Azure AD.

## Environment variables

Set these environment variables for the backend:

```bash
export OIDC_ENABLED=true
export OIDC_PROVIDER_NAME="GitLab"
export OIDC_ISSUER="https://gitlab.example.com"
export OIDC_CLIENT_ID="YOUR_CLIENT_ID"
export OIDC_CLIENT_SECRET="YOUR_CLIENT_SECRET"
export OIDC_SCOPES="openid,profile,email"
export OIDC_USE_PKCE=true
```

Optional:

```bash
export OIDC_TOKEN_AUTH_METHOD="client_secret_post"
```

If `OIDC_TOKEN_AUTH_METHOD` is omitted, django-allauth will use the provider metadata to decide whether `client_secret_basic` should be used.

## Callback URL

Configure your provider callback URL as:

```text
{DOCCANO_URL}/v1/social/complete/oidc/
```

Examples:

- `https://example.com/v1/social/complete/oidc/`
- `http://127.0.0.1:3000/v1/social/complete/oidc/` when the frontend dev server proxies `/v1` to the backend

## Login flow

When OIDC is configured, the login page shows one additional provider button. Clicking it starts the OIDC authorization code flow and returns the browser to doccano after authentication completes.

## Claim handling

doccano uses the provider `sub` claim as the social account UID. For local username creation, the implementation falls back in this order:

1. `email`
2. `preferred_username`
3. `sub`

This allows login to succeed even when the provider does not return an email address.

## Notes

- Username/password login still works.
- Header-based SSO still works.
- Only one OIDC provider is supported at a time in this version.
