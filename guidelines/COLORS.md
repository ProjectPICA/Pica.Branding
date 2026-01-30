# Pica Color Palette

## Primary Colors

### Pica Blue
The primary brand color representing trust and innovation.

| Format | Value |
|--------|-------|
| HEX | `#0066CC` |
| RGB | `rgb(0, 102, 204)` |
| HSL | `hsl(210, 100%, 40%)` |

### Pica Dark
Used for primary text and dark UI elements.

| Format | Value |
|--------|-------|
| HEX | `#1A1A2E` |
| RGB | `rgb(26, 26, 46)` |
| HSL | `hsl(240, 28%, 14%)` |

## Secondary Colors

### Success Green
| Format | Value |
|--------|-------|
| HEX | `#28A745` |
| RGB | `rgb(40, 167, 69)` |

### Warning Orange
| Format | Value |
|--------|-------|
| HEX | `#FFC107` |
| RGB | `rgb(255, 193, 7)` |

### Error Red
| Format | Value |
|--------|-------|
| HEX | `#DC3545` |
| RGB | `rgb(220, 53, 69)` |

### Info Cyan
| Format | Value |
|--------|-------|
| HEX | `#17A2B8` |
| RGB | `rgb(23, 162, 184)` |

## Neutral Colors

| Name | HEX | Usage |
|------|-----|-------|
| White | `#FFFFFF` | Backgrounds, cards |
| Gray 100 | `#F8F9FA` | Light backgrounds |
| Gray 200 | `#E9ECEF` | Borders, dividers |
| Gray 300 | `#DEE2E6` | Disabled states |
| Gray 400 | `#CED4DA` | Placeholder text |
| Gray 500 | `#ADB5BD` | Secondary text |
| Gray 600 | `#6C757D` | Muted text |
| Gray 700 | `#495057` | Body text |
| Gray 800 | `#343A40` | Headings |
| Gray 900 | `#212529` | Primary text |
| Black | `#000000` | Rare use only |

## Usage Guidelines

### Accessibility
- Ensure sufficient contrast ratios (WCAG 2.1 AA minimum)
- Primary text should have at least 4.5:1 contrast ratio
- Large text (18px+) should have at least 3:1 contrast ratio

### Color Combinations
- Primary Blue on White: Approved
- White on Primary Blue: Approved
- Primary Blue on Gray 100: Approved
- Avoid: Error Red on Warning Orange
- Avoid: Low contrast text/background combinations

## CSS Variables

```css
:root {
  /* Primary */
  --pica-blue: #0066CC;
  --pica-dark: #1A1A2E;

  /* Semantic */
  --pica-success: #28A745;
  --pica-warning: #FFC107;
  --pica-error: #DC3545;
  --pica-info: #17A2B8;

  /* Neutrals */
  --pica-white: #FFFFFF;
  --pica-gray-100: #F8F9FA;
  --pica-gray-200: #E9ECEF;
  --pica-gray-300: #DEE2E6;
  --pica-gray-400: #CED4DA;
  --pica-gray-500: #ADB5BD;
  --pica-gray-600: #6C757D;
  --pica-gray-700: #495057;
  --pica-gray-800: #343A40;
  --pica-gray-900: #212529;
  --pica-black: #000000;
}
```

---

## Light Mode: The Magpie Palette

A clean, airy light theme inspired by the magpie's white plumage and the sky it soars through.

### Color Definitions

| Element | Color Description | HEX | RGB | Usage in UI |
|---------|-------------------|-----|-----|-------------|
| Primary Base | Cloud Mist (The open sky) | `#F8F9FC` | `rgb(248, 249, 252)` | Main background color |
| Secondary Base | Feather Gray (The soft down) | `#FFFFFF` | `rgb(255, 255, 255)` | Card backgrounds, elevated surfaces |
| Accent 1 | Deep Teal (The wing sheen) | `#00838F` | `rgb(0, 131, 143)` | Primary buttons, active states |
| Accent 2 | Vivid Indigo (The tail tips) | `#3F51B5` | `rgb(63, 81, 181)` | Links, icons, subtle gradients |
| Text Primary | Obsidian Ink (The dark plumage) | `#1A1A2E` | `rgb(26, 26, 46)` | Main body text, headers |
| Text Secondary | Slate Gray (The shadows) | `#64748B` | `rgb(100, 116, 139)` | Secondary text, captions |
| Border/Divider | Silver Mist | `#E2E8F0` | `rgb(226, 232, 240)` | Borders, dividers, subtle lines |

### Detailed Specifications

#### Cloud Mist (Primary Base)
A subtle off-white with a cool undertone for comfortable extended viewing.

| Format | Value |
|--------|-------|
| HEX | `#F8F9FC` |
| RGB | `rgb(248, 249, 252)` |
| HSL | `hsl(225, 33%, 98%)` |

#### Feather Gray (Secondary Base)
Pure white for elevated surfaces, creating depth through shadow rather than color.

| Format | Value |
|--------|-------|
| HEX | `#FFFFFF` |
| RGB | `rgb(255, 255, 255)` |
| HSL | `hsl(0, 0%, 100%)` |

#### Deep Teal (Accent 1)
A richer, more saturated teal optimized for visibility on light backgrounds.

| Format | Value |
|--------|-------|
| HEX | `#00838F` |
| RGB | `rgb(0, 131, 143)` |
| HSL | `hsl(185, 100%, 28%)` |

#### Vivid Indigo (Accent 2)
A brighter indigo that maintains vibrancy on light surfaces.

| Format | Value |
|--------|-------|
| HEX | `#3F51B5` |
| RGB | `rgb(63, 81, 181)` |
| HSL | `hsl(231, 48%, 48%)` |

#### Obsidian Ink (Text Primary)
Deep, rich text color for optimal readability.

| Format | Value |
|--------|-------|
| HEX | `#1A1A2E` |
| RGB | `rgb(26, 26, 46)` |
| HSL | `hsl(240, 28%, 14%)` |

#### Slate Gray (Text Secondary)
Softer gray for secondary information and captions.

| Format | Value |
|--------|-------|
| HEX | `#64748B` |
| RGB | `rgb(100, 116, 139)` |
| HSL | `hsl(215, 16%, 47%)` |

### Light Mode CSS Variables

```css
:root {
  /* Magpie Palette - Light Mode */
  --magpie-primary-base: #F8F9FC;      /* Cloud Mist */
  --magpie-secondary-base: #FFFFFF;    /* Feather Gray */
  --magpie-accent-1: #00838F;          /* Deep Teal */
  --magpie-accent-2: #3F51B5;          /* Vivid Indigo */
  --magpie-text-primary: #1A1A2E;      /* Obsidian Ink */
  --magpie-text-secondary: #64748B;    /* Slate Gray */
  --magpie-border: #E2E8F0;            /* Silver Mist */

  /* Semantic mappings */
  --pica-background: var(--magpie-primary-base);
  --pica-surface: var(--magpie-secondary-base);
  --pica-primary: var(--magpie-accent-1);
  --pica-secondary: var(--magpie-accent-2);
  --pica-text-primary: var(--magpie-text-primary);
  --pica-text-secondary: var(--magpie-text-secondary);
  --pica-border: var(--magpie-border);
}
```

### Light Mode Usage Guidelines

#### Contrast & Accessibility
- Obsidian Ink (#1A1A2E) on Cloud Mist (#F8F9FC): **15.8:1** contrast ratio ✓
- Obsidian Ink (#1A1A2E) on Feather Gray (#FFFFFF): **16.4:1** contrast ratio ✓
- Deep Teal (#00838F) on Feather Gray (#FFFFFF): **4.6:1** contrast ratio ✓
- All text combinations exceed WCAG AA requirements

#### Layering Hierarchy
1. **Base layer**: Cloud Mist (#F8F9FC) - Page background
2. **Elevated surfaces**: Feather Gray (#FFFFFF) - Cards, modals, dropdowns (with shadow)
3. **Interactive elements**: Deep Teal (#00838F) - Buttons, active states
4. **Secondary interactions**: Vivid Indigo (#3F51B5) - Links, secondary buttons

#### Approved Combinations
- ✅ Obsidian Ink text on Cloud Mist/Feather Gray background
- ✅ Deep Teal buttons on Cloud Mist/Feather Gray
- ✅ Vivid Indigo links on Cloud Mist/Feather Gray
- ✅ Deep Teal to Vivid Indigo gradients
- ✅ Silver Mist borders on Feather Gray cards

#### Avoid
- ❌ Slate Gray text for important/primary content
- ❌ Deep Teal text on colored backgrounds (use on white only)
- ❌ Mixing dark mode colors with light mode palette

---

## Dark Mode: The Magpie Palette

A refined dark theme inspired by the magpie's distinctive plumage—from deep obsidian blacks to iridescent teal sheens.

### Color Definitions

| Element | Color Description | HEX | RGB | Usage in UI |
|---------|-------------------|-----|-----|-------------|
| Primary Base | Deep Obsidian (The head/neck) | `#0D0D0D` | `rgb(13, 13, 13)` | Main background color |
| Secondary Base | Midnight Charcoal (The wing shadows) | `#1A1A1B` | `rgb(26, 26, 27)` | Card backgrounds, section dividers |
| Accent 1 | Iridescent Teal (The wing sheen) | `#005F6B` | `rgb(0, 95, 107)` | Primary buttons, active states |
| Accent 2 | Royal Indigo (The tail/wing tips) | `#2E3192` | `rgb(46, 49, 146)` | Links, icons, subtle gradients |
| Text/Highlight | Cloud White (The belly) | `#F2F2F2` | `rgb(242, 242, 242)` | Main body text, headers |

### Detailed Specifications

#### Deep Obsidian (Primary Base)
The foundation of the dark theme, representing the magpie's distinctive black plumage.

| Format | Value |
|--------|-------|
| HEX | `#0D0D0D` |
| RGB | `rgb(13, 13, 13)` |
| HSL | `hsl(0, 0%, 5%)` |

#### Midnight Charcoal (Secondary Base)
A slightly elevated surface color for layering and visual hierarchy.

| Format | Value |
|--------|-------|
| HEX | `#1A1A1B` |
| RGB | `rgb(26, 26, 27)` |
| HSL | `hsl(240, 2%, 10%)` |

#### Iridescent Teal (Accent 1)
The primary accent color capturing the magpie's iridescent wing sheen.

| Format | Value |
|--------|-------|
| HEX | `#005F6B` |
| RGB | `rgb(0, 95, 107)` |
| HSL | `hsl(187, 100%, 21%)` |

#### Royal Indigo (Accent 2)
A secondary accent for depth and visual interest.

| Format | Value |
|--------|-------|
| HEX | `#2E3192` |
| RGB | `rgb(46, 49, 146)` |
| HSL | `hsl(238, 52%, 38%)` |

#### Cloud White (Text/Highlight)
The primary text color providing optimal readability on dark surfaces.

| Format | Value |
|--------|-------|
| HEX | `#F2F2F2` |
| RGB | `rgb(242, 242, 242)` |
| HSL | `hsl(0, 0%, 95%)` |

### Dark Mode CSS Variables

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* Magpie Palette - Dark Mode */
    --magpie-primary-base: #0D0D0D;      /* Deep Obsidian */
    --magpie-secondary-base: #1A1A1B;    /* Midnight Charcoal */
    --magpie-accent-1: #005F6B;          /* Iridescent Teal */
    --magpie-accent-2: #2E3192;          /* Royal Indigo */
    --magpie-text: #F2F2F2;              /* Cloud White */

    /* Semantic mappings */
    --pica-background: var(--magpie-primary-base);
    --pica-surface: var(--magpie-secondary-base);
    --pica-primary: var(--magpie-accent-1);
    --pica-secondary: var(--magpie-accent-2);
    --pica-text-primary: var(--magpie-text);
  }
}

/* Manual dark mode toggle class */
.dark-mode,
[data-theme="dark"] {
  --magpie-primary-base: #0D0D0D;
  --magpie-secondary-base: #1A1A1B;
  --magpie-accent-1: #005F6B;
  --magpie-accent-2: #2E3192;
  --magpie-text: #F2F2F2;

  --pica-background: var(--magpie-primary-base);
  --pica-surface: var(--magpie-secondary-base);
  --pica-primary: var(--magpie-accent-1);
  --pica-secondary: var(--magpie-accent-2);
  --pica-text-primary: var(--magpie-text);
}
```

### Dark Mode Usage Guidelines

#### Contrast & Accessibility
- Cloud White (#F2F2F2) on Deep Obsidian (#0D0D0D): **18.1:1** contrast ratio ✓
- Cloud White (#F2F2F2) on Midnight Charcoal (#1A1A1B): **15.5:1** contrast ratio ✓
- Iridescent Teal (#005F6B) on Deep Obsidian (#0D0D0D): **3.8:1** - Use for large text/icons only
- All text combinations exceed WCAG AAA requirements

#### Layering Hierarchy
1. **Base layer**: Deep Obsidian (#0D0D0D) - Page background
2. **Elevated surfaces**: Midnight Charcoal (#1A1A1B) - Cards, modals, dropdowns
3. **Interactive elements**: Iridescent Teal (#005F6B) - Buttons, active states
4. **Secondary interactions**: Royal Indigo (#2E3192) - Links, secondary buttons

#### Approved Combinations
- ✅ Cloud White text on Deep Obsidian background
- ✅ Cloud White text on Midnight Charcoal background
- ✅ Iridescent Teal buttons on Deep Obsidian/Midnight Charcoal
- ✅ Royal Indigo links on Deep Obsidian/Midnight Charcoal
- ✅ Iridescent Teal to Royal Indigo gradients

#### Avoid
- ❌ Iridescent Teal text on Deep Obsidian (insufficient contrast for body text)
- ❌ Royal Indigo text on Deep Obsidian (insufficient contrast)
- ❌ Mixing light mode grays with dark mode palette
