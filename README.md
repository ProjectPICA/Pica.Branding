# Pica Branding

Central repository for Project Pica's design guidelines, branding assets, and visual identity resources.

## Brand Overview

Pica is a modern platform designed to deliver exceptional user experiences. Our brand identity reflects innovation, reliability, and clarity.

### Brand Values

- **Innovation**: We embrace modern solutions and forward-thinking approaches
- **Reliability**: Consistent, dependable experiences our users can trust
- **Clarity**: Clear communication and intuitive design
- **Community**: Building connections and enabling collaboration

## Repository Structure

```
├── assets/
│   ├── logos/          # Logo files (light and dark mode variants)
│   ├── icons/          # Icon library
│   ├── colors/         # Color palette exports
│   ├── fonts/          # Typography files (if licensed for distribution)
│   └── images/         # Marketing and promotional images
├── guidelines/         # Brand and design guidelines
│   ├── COLORS.md       # Color palette documentation
│   ├── TYPOGRAPHY.md   # Typography guidelines
│   └── LOGO_USAGE.md   # Logo usage guidelines
└── templates/          # Design templates and POC examples
```

## Quick Links

### Guidelines
- [Color Palette](guidelines/COLORS.md) - Magpie Palette for light and dark modes
- [Typography](guidelines/TYPOGRAPHY.md) - Font families, type scale, and best practices
- [Logo Usage](guidelines/LOGO_USAGE.md) - Logo versions, clear space, and usage rules

### Templates
- [Light Mode Dashboard POC](templates/dashboard-light-poc.html)

## Voice and Tone

### General Principles
- Be clear and concise
- Use active voice
- Be helpful, not condescending
- Maintain professionalism while being approachable

### Writing Style
- Use sentence case for headings
- Avoid jargon when possible
- Be inclusive in language choices
- Prefer shorter sentences

## Visual Identity

### The Magpie Palette

Our color system is inspired by the magpie's distinctive plumage, available in both light and dark modes.

#### Light Mode
| Element | Color | HEX |
|---------|-------|-----|
| Primary Base | Cloud Mist | `#F8F9FC` |
| Secondary Base | Feather Gray | `#FFFFFF` |
| Accent 1 | Deep Teal | `#00838F` |
| Accent 2 | Vivid Indigo | `#3F51B5` |
| Text Primary | Obsidian Ink | `#1A1A2E` |

#### Dark Mode
| Element | Color | HEX |
|---------|-------|-----|
| Primary Base | Deep Obsidian | `#0D0D0D` |
| Secondary Base | Midnight Charcoal | `#1A1A1B` |
| Accent 1 | Iridescent Teal | `#005F6B` |
| Accent 2 | Royal Indigo | `#2E3192` |
| Text | Cloud White | `#F2F2F2` |

For complete color specifications, CSS variables, and usage guidelines, see the [Color Palette documentation](guidelines/COLORS.md).

### Logo Variants

| Mode | File | Usage |
|------|------|-------|
| Light | `assets/logos/pica-logo-primary.png` | White/light backgrounds |
| Dark | `assets/logos/pica-logo-dark-mode.png` | Dark backgrounds |

For detailed logo usage rules, clear space requirements, and approved backgrounds, see the [Logo Usage documentation](guidelines/LOGO_USAGE.md).

## Usage

### For Developers

When implementing UI components, refer to:
- [Color Palette](guidelines/COLORS.md) for color values and CSS variables
- [Typography](guidelines/TYPOGRAPHY.md) for font stacks and type scale
- Logo assets in `assets/logos/`
- POC templates in `templates/`

### For Designers

Design templates and examples can be found in the `templates/` directory. Refer to the [guidelines](guidelines/) folder for brand specifications.

## Do's and Don'ts

### Do
- Use official brand colors consistently
- Maintain proper logo spacing
- Follow typography guidelines
- Keep messaging clear and on-brand
- Use the correct logo variant for light/dark contexts

### Don't
- Alter logo proportions or colors
- Use unapproved color combinations
- Mix brand fonts with unapproved typefaces
- Use casual or overly informal language in official communications
- Use light mode logo on dark backgrounds (or vice versa)

## Contributing

When adding new assets or updating guidelines:
1. Ensure all assets are optimized for web use
2. Provide multiple formats where applicable (SVG + PNG for logos)
3. Update relevant documentation
4. Follow the existing naming conventions

## License

All brand assets are proprietary to Project Pica. Free to use for referential purposes only (identifying or linking to Project Pica). See [LICENSE](LICENSE) for full terms.
