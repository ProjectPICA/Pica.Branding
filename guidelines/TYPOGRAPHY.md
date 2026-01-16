# Pica Typography

## Font Families

### Primary Font: Inter
Inter is our primary typeface for both headings and body text. It offers excellent readability across all sizes and devices.

**Font Stack:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
```

### Monospace Font: JetBrains Mono
Used for code snippets, technical content, and data displays.

**Font Stack:**
```css
font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
```

## Type Scale

| Name | Size | Weight | Line Height | Usage |
|------|------|--------|-------------|-------|
| Display | 48px / 3rem | 700 | 1.2 | Hero sections |
| H1 | 36px / 2.25rem | 700 | 1.25 | Page titles |
| H2 | 30px / 1.875rem | 600 | 1.3 | Section headers |
| H3 | 24px / 1.5rem | 600 | 1.35 | Subsection headers |
| H4 | 20px / 1.25rem | 600 | 1.4 | Card titles |
| H5 | 18px / 1.125rem | 600 | 1.4 | Small headers |
| H6 | 16px / 1rem | 600 | 1.5 | Minor headers |
| Body Large | 18px / 1.125rem | 400 | 1.6 | Lead paragraphs |
| Body | 16px / 1rem | 400 | 1.6 | Default body text |
| Body Small | 14px / 0.875rem | 400 | 1.5 | Secondary text |
| Caption | 12px / 0.75rem | 400 | 1.4 | Labels, captions |
| Code | 14px / 0.875rem | 400 | 1.5 | Code blocks |

## Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Regular | 400 | Body text, paragraphs |
| Medium | 500 | Emphasis, buttons |
| Semi-Bold | 600 | Subheadings, labels |
| Bold | 700 | Headings, important text |

## CSS Implementation

```css
/* Typography Variables */
:root {
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Font Sizes */
  --text-display: 3rem;
  --text-h1: 2.25rem;
  --text-h2: 1.875rem;
  --text-h3: 1.5rem;
  --text-h4: 1.25rem;
  --text-h5: 1.125rem;
  --text-h6: 1rem;
  --text-body-lg: 1.125rem;
  --text-body: 1rem;
  --text-body-sm: 0.875rem;
  --text-caption: 0.75rem;

  /* Font Weights */
  --font-regular: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.6;
}
```

## Best Practices

### Readability
- Maintain 60-80 characters per line for body text
- Use adequate line height (1.5-1.6 for body text)
- Ensure sufficient contrast between text and background

### Hierarchy
- Use font size and weight to establish visual hierarchy
- Limit the number of font sizes on a single page
- Maintain consistent heading structure (H1 > H2 > H3)

### Responsive Typography
- Consider fluid typography for responsive designs
- Adjust line lengths for different viewport sizes
- Test readability on various devices
