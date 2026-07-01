# Generic OIDC Login Design

## Summary

Add support for a single configurable OpenID Connect provider to doccano without changing the existing login page structure or the existing username/password and header-based SSO flows.

The implementation replaces the current Okta-specific social login wiring with a generic OIDC login path that can be configured against standards-compliant providers such as GitLab, Keycloak, Authentik, and Azure AD.

## Goals

- Support one configurable OIDC provider at a time.
- Keep the existing `/v1/social/links/` driven login button flow.
- Keep username/password login working unchanged.
- Keep header-based SSO working unchanged.
- Minimize frontend changes.
- Provide configuration that is provider-neutral rather than vendor-specific.

## Non-Goals

- Supporting multiple OIDC providers at the same time.
- Implementing provider-specific role or group synchronization in the first version.
- Preserving the old Okta-specific environment variable scheme.
- Building a custom OIDC flow outside the existing social login stack.

## Current State

The current codebase has an Okta-specific implementation:

- `allauth.socialaccount.providers.okta` is installed.
- `/social/complete/okta-oauth2/` is the only social login callback.
- `/v1/social/links/` returns a single hard-coded Okta entry.
- Documentation mentions OpenID Connect, but the corresponding code path is not actually wired as a complete generic OIDC implementation.

This creates a mismatch between documentation and actual capability, and it prevents reuse with non-Okta identity providers.

## Proposed Design

### Authentication Model

Replace the existing Okta-specific social login configuration with a single generic OIDC configuration. The system exposes one optional social login button when OIDC is enabled and fully configured.

The login flow remains:

1. Frontend requests `/v1/social/links/`.
2. Backend returns metadata for the configured social login option.
3. User clicks the provider button.
4. Browser is redirected to the provider authorization endpoint.
5. Provider redirects back to doccano callback endpoint.
6. Backend completes login and creates or reuses the local user.
7. User lands in the existing post-login destination.

### Configuration

Introduce provider-neutral settings:

- `OIDC_ENABLED`
- `OIDC_PROVIDER_NAME`
- `OIDC_ISSUER`
- `OIDC_CLIENT_ID`
- `OIDC_CLIENT_SECRET`
- `OIDC_SCOPES`
- `OIDC_USE_PKCE`

Defaults:

- `OIDC_ENABLED=false`
- `OIDC_PROVIDER_NAME=OpenID Connect`
- `OIDC_SCOPES=openid profile email`
- `OIDC_USE_PKCE=true`

The social login button is shown only when OIDC is enabled and the required values are present.

### URL Shape

Use a provider-neutral callback path:

- `/social/complete/oidc/`

This keeps the URL stable and avoids leaking vendor naming into the API surface.

### Backend Changes

#### Settings

Update `backend/config/settings/base.py` to:

- remove the Okta-only provider wiring
- read the new OIDC environment variables
- assemble a single internal OIDC configuration object used by views and adapters

#### Social Link API

Update `backend/social/views.py` so `/v1/social/links/` returns a generic provider entry instead of a hard-coded `okta` key.

Returned data should include:

- provider id
- display label
- authorize URL
- redirect path

If OIDC is disabled or incompletely configured, the API should return an empty result for social login instead of raising an error.

#### Login View

Replace the current Okta login view with a generic OIDC login view bound to the provider-neutral callback path.

The implementation should stay inside the existing social login stack rather than introducing a fully custom OIDC code flow.

#### User Identity Mapping

Do not assume all providers return the same claims. User creation and lookup should use a deterministic fallback chain:

1. `email`
2. `preferred_username`
3. `sub`

If the provider does not return an email, login should still succeed as long as a stable identifier is available.

### Frontend Changes

Frontend changes remain minimal:

- keep `frontend/pages/auth.vue` structure unchanged
- keep `frontend/components/auth/SocialLogin.vue` structure unchanged
- allow button label/provider name to come from API data rather than assuming Okta

No new frontend routes or views are required.

### Error Handling

The implementation should handle these cases explicitly:

- OIDC disabled: no social login button is shown
- partial configuration: no social login button is shown
- missing optional claims such as email: fallback to alternate identifiers
- provider-specific claim differences: tolerate them through fallback mapping

The implementation should not fail application startup merely because OIDC is not configured.

### Compatibility

Preserve:

- username/password authentication
- header-based SSO
- existing login page layout

Do not preserve:

- Okta-specific environment variable names
- Okta-specific callback path
- Okta-specific documentation as the primary path

### Documentation

Replace the current incomplete Okta OpenID Connect guidance with generic OIDC setup documentation that explains:

- required environment variables
- callback URL format
- example values
- how to use common providers such as GitLab or Keycloak through the same OIDC settings

### Testing

Add tests for:

- social link API when OIDC is disabled
- social link API when OIDC is fully configured
- login view identity mapping fallback behavior
- regression coverage for standard login path remaining unchanged

The repository should not include a real external IdP integration test. Tests should rely on mocked provider responses.

## Trade-Offs

### Why a Single Generic Provider

The current product shape exposes only one social login path. Supporting one configurable provider aligns with that shape and keeps the code small and predictable.

### Why Not Multiple Providers

Multiple providers would require a broader configuration model, richer frontend behavior, more callback management, and more test surface. That is unnecessary for the current requirement.

### Why Not a Custom OIDC Flow

Writing a custom authorization code flow would add avoidable authentication complexity and risk. Reusing the existing social login mechanism is safer and smaller in scope.

## Migration Plan

1. Introduce the new OIDC configuration and callback path.
2. Replace Okta-specific social link generation with generic OIDC link generation.
3. Update the social login backend view.
4. Update documentation to the generic OIDC model.
5. Add tests for configuration gating and identity mapping.

## Risks

- The currently pinned `django-allauth` version may limit which generic OIDC integration path is practical.
- Some providers may require claim mapping differences beyond the initial fallback chain.
- Existing users configured around Okta-specific environment variables will need to rename configuration during upgrade.

## Open Decisions Resolved

- Scope is one configurable OIDC provider, not multiple.
- The first version does not include group-to-admin synchronization.
- The login page remains API-driven and visually unchanged.

## Implementation Boundary

Implementation should stop after the repository supports one generic OIDC provider end-to-end, with updated documentation and automated tests. Multi-provider support and provider-specific authorization features remain out of scope.
