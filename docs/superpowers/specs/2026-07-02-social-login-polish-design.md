# Social Login Visual Polish Design

## Goal
Refine the third-party login area on the auth page so it reads as a secondary action. Keep the username/password card unchanged and only polish the social login section beneath it.

## Scope
- Only change the visual presentation of the social login area on the auth page.
- Keep the existing provider fetch and redirect behavior unchanged.
- Do not redesign the main login card.
- Do not introduce provider-specific icons or extra copy beyond a compact separator label.

## UX Direction
Use the minimal separator treatment instead of a boxed panel:
- Render a lightweight separator above the social login button.
- Place a short, low-emphasis label in the center of the separator.
- Keep the social login button full width.
- Restyle the button as a white surface with a subtle border and dark text so it reads as a secondary action.

## Component Changes
Update `frontend/components/auth/SocialLogin.vue` only.

Template changes:
- Do not render the component shell when no social providers are available.
- Add a separator row above the buttons.
- Keep support for one or more providers by rendering a button per provider.

Style changes:
- Add local scoped styles for the social login container.
- Reduce the top spacing relative to the login card.
- Style the separator with thin horizontal rules and centered helper text.
- Replace the current elevated colored button treatment with a white bordered button.
- Add a restrained hover state with a slight border and background shift.
- Preserve full-width layout on desktop and mobile.

## Content
Use a neutral helper label equivalent to "or continue with". Keep the existing button label format that interpolates the provider name.

## Non-Goals
- No changes to form validation, authentication flow, or callback handling.
- No changes to backend social login endpoints.
- No redesign of the surrounding auth page layout.

## Verification
- Auth page still loads when no providers are configured.
- Auth page renders the separator and white button when OIDC is configured.
- Clicking the button still navigates to the existing social login URL.
- Visual result reads as a secondary action beneath the primary login card.
