# AGENTS.md — Pica.Branding

The brand reference for PICA: design guidelines (the Magpie colour palette, typography, logo usage), logo files and
one HTML design proof-of-concept. Documentation and static assets only — no build, no package, no deploy. Nothing
imports this repository; other repositories copy values and files from it.

## Layout

```
README.md                    brand overview, palette summary, voice and tone, do's and don'ts
guidelines/COLORS.md         Magpie palette: light and dark tokens, CSS variables, usage
guidelines/TYPOGRAPHY.md     font families, type scale
guidelines/LOGO_USAGE.md     logo versions, clear space, approved backgrounds
assets/logos/                pica-logo-primary.png (light backgrounds), pica-logo-dark-mode.png (dark backgrounds)
assets/icons/, assets/images/  placeholders (.gitkeep)
templates/dashboard-light-poc.html   static light-mode dashboard proof-of-concept
LICENSE                      proprietary; referential use only
```

## Commands

None: there is nothing to build. Open `templates/*.html` in a browser to view a template.

## Verification ladder

1. Links between the Markdown files and to `assets/` resolve (relative paths, matching case).
2. A changed colour or font is changed in `README.md` and in the matching `guidelines/*.md` file, so the summary
   and the specification agree.
3. A new or changed asset opens and has both light and dark variants where the guidelines call for them.
4. Cannot verify (e.g. no way to render an image)? Say so.

## Conventions

- The guidelines are the single source of brand values; the README only summarises them and links there.
- Logos: provide SVG + PNG where possible, web-optimised, named `pica-logo-<variant>.<ext>`. Never alter logo
  proportions or colours.
- Colours are named tokens (Cloud Mist, Deep Teal, …) with HEX values for light and dark mode; keep both modes in
  step and meet WCAG AA contrast.
- `assets/logos/IMG_0784.PNG` is an unnamed source image; rename it or remove it once its use is known rather than
  referencing it.

## Commit hygiene

- Commit directly to `main` and push; no feature branches or PRs unless asked.
- Brief subject stating what was done. No `Co-Authored-By` lines or generated-with footers.

## This repo in the system

- The brand source for ProjectPICA's user-facing surfaces. Consumers copy from it by hand:
  - `PICA.WebApp` implements the Magpie palette as `--pica-*` design tokens in `src/styles.scss`;
  - `PICA.Infrastructure` holds the Entra External ID (CIAM) sign-in branding (`branding/ciam/`: CSS, logos, favicon);
  - `PICA.LandingPage` is meant to follow the same brand.
- Nothing updates automatically: a palette or logo change here is followed by a change in each consumer repository
  (tokens in `PICA.WebApp`, CIAM assets in `PICA.Infrastructure`), each verified there.
- The workspace repository `ProjectPICA/Pica.Claude` holds the cross-repo router (which repo owns what) and the
  release and TST-diagnostics procedures; read it when a change crosses this repository's boundary.
