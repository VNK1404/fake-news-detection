---
name: VeriNews AI
colors:
  surface: '#131315'
  surface-dim: '#131315'
  surface-bright: '#39393b'
  surface-container-lowest: '#0e0e10'
  surface-container-low: '#1c1b1d'
  surface-container: '#201f22'
  surface-container-high: '#2a2a2c'
  surface-container-highest: '#353437'
  on-surface: '#e5e1e4'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e5e1e4'
  inverse-on-surface: '#313032'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d3'
  on-secondary-container: '#00424e'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#131315'
  on-background: '#e5e1e4'
  surface-variant: '#353437'
typography:
  display:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
---

## Brand & Style
This design system embodies an authoritative, tech-forward aesthetic tailored for high-stakes information environments. It merges **Minimalism** with a **Futuristic** edge, focusing on clarity, precision, and trust. 

The visual narrative is inspired by high-end developer tools and intelligence interfaces—utilizing expansive whitespace (or "darkspace"), tactical use of vibrant accents, and a strict adherence to a systematic grid. The objective is to make complex AI-driven data feel accessible yet profoundly sophisticated. The UI should evoke a sense of calm under pressure, providing users with the clarity needed to distinguish truth from fabrication.

## Colors
The palette is anchored in a sophisticated "Obsidian" dark mode, providing a high-contrast foundation for data visualization and AI analysis.

- **Primary (Indigo):** Used for primary actions, active states, and brand presence. It signals intelligence and depth.
- **Secondary (Cyan):** Used for AI-driven insights, success states, and technical highlights. It provides the "futuristic" glow.
- **Neutral (Obsidian & Slate):** A scale of deep grays ensures hierarchy without pure black (#000) harshness.
- **Light Mode:** When toggled, the system flips to a "Gallery" white (#ffffff) with soft zinc borders (#e4e4e7), maintaining the same indigo/cyan accents for brand consistency.

## Typography
The typography system utilizes a dual-font approach to balance technical precision with extreme legibility.

- **Geist** is employed for headings, labels, and UI signals. Its mono-spaced heritage adds a "engineered" feel to the interface.
- **Inter** is used for all body copy and long-form analysis. It is optimized for readability, ensuring that "fake news" reports and data summaries are easy to digest.
- **Tracking:** Use tighter letter-spacing for large headlines to maintain a compact, premium feel. Use slightly increased tracking for small labels to improve scanning.

## Layout & Spacing
The layout follows a **Fluid Grid** model with strict adherence to an 8px spacing rhythm.

- **Desktop:** 12-column grid. Sidebars for navigation and filtering should be fixed (240px-280px) while the main content area remains fluid with a max-width of 1440px to prevent excessive line lengths.
- **Mobile:** 4-column grid with reduced margins.
- **Hierarchy:** Use larger vertical spacing (64px+) between distinct content sections to reinforce a minimalist, "uncluttered" feel.

## Elevation & Depth
Depth is created through **Tonal Layers** and **Subtle Glassmorphism** rather than traditional heavy shadows.

- **Surface Tiers:** Background is #09090b. Containers use #18181b. Floating elements (modals, tooltips) use #27272a.
- **Glassmorphism:** Navigation bars and side panels should use a 12px background blur with a 10% white (light mode) or 10% gray (dark mode) opacity.
- **Shadows:** Use a single "Ambient Glow" for active cards—a very soft, 20px blur indigo tint (#6366f1) at 10% opacity to suggest the element is powered by AI.
- **Borders:** Subtle 1px solid borders (#27272a) are the primary way to define structure.

## Shapes
The shape language is "Soft-Modern." Elements use a **Rounded** (0.5rem) base to feel approachable, but specialized components use larger radii.

- **Standard Elements:** Buttons, inputs, and small cards use 8px (0.5rem).
- **Large Containers:** Main content cards and feature sections use 16px (1rem).
- **Interactive Pill:** Search bars and status chips use full rounding (pill-shaped) to distinguish them from structural elements.

## Components
- **Buttons:** High-contrast Indigo fill for primary actions; "Ghost" borders for secondary. Use a subtle hover state that increases the Indigo saturation.
- **Cards:** No background color on primary cards; instead, use a 1px border. "Elevated" cards use a #18181b fill.
- **Inputs:** Minimalist bottom-border-only or subtle 1px outline. On focus, the border transitions to Cyan with a faint outer glow.
- **Status Chips:** Critical for fake news detection. Use "Verified" (Cyan), "Questionable" (Amber), and "False" (Red). Chips are always pill-shaped with low-opacity backgrounds.
- **AI Insight Panel:** A specialized component using a gradient border (Indigo to Cyan) to house AI-generated summaries.
- **Data Visualizations:** Use "Skeleton" loaders that pulse with a cyan tint to reinforce the technical nature of the platform.