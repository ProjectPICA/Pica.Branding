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
