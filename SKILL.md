---
name: impeccable
description: Expert-level frontend design system for building and improving distinctive, production-quality static HTML websites and UI in Claude Chat. Use this skill whenever the user wants to design, build, redesign, review, polish, or improve a website, landing page, portfolio, one-page site, UI, or HTML/CSS component, or says things like "make this look better", "make it bolder", "make it feel more premium", "audit my site", "critique my design", or "build me a site". Handles the whole flow: gather the vibe, pick a register (brand or product), shape a design brief, build one self-contained HTML file, self-check it, and deliver it. Includes 19 commands (craft, shape, critique, audit, polish, bolder, quieter, distill, harden, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, onboard) and enforces design laws and anti-patterns so the result doesn't look AI-generated. Trigger even when the user doesn't say "design".
---

# Impeccable (Claude Chat edition)

A specialized design skill for turning generic AI output into committed, high-craft interfaces. This edition is built for Claude Chat: no project folder, no terminal required. The default deliverable is **one self-contained static HTML file**.

Based on [Impeccable](https://impeccable.style) by Paul Bakaus. See `NOTICE.md` for credits and changes.

## Workflow

### 1. Get the context and the vibe (in chat)

Before designing anything, know what you're making and how it should feel. Everything is gathered in conversation; there are no config files.

Find out, using what the user already said first:

- **What and who**: the subject, the audience, the one thing the page must do.
- **The vibe**: ask for three concrete, physical-object words (not "modern" or "clean") and two or three named references (a brand, a poster, a product, a building). If they have none, offer a few lanes to react to, for example:
  - "Brutalist and raw"
  - "Clean, Swiss-style minimalism"
  - "Playful, high-chroma pop"
  - "Sober, enterprise-grade reliability"
  - "Warm, tactile, small-batch craft"
- **Existing material**: pasted HTML, copy, brand colors, a logo, or screenshots. Treat any brand decision already made as fixed.

How to ask:
- **Sparse request** ("make me a portfolio"): ask 2 to 4 focused questions with concrete options, then stop and wait. If an options or buttons tool is available, use it; otherwise write short questions with lettered choices. Never invent a full brief from one line.
- **Clear request** (subject, audience, and some vibe are given): don't interrogate. State your assumptions in a line or two and build.
- If the vibe is unclear after that, infer it from the subject and audience, say what you inferred, and let the user override.

### 2. Identify the register

Decide whether the work is **Brand** or **Product**, then load the matching reference.

| Register | Use for | Load |
|---|---|---|
| **Brand** | Marketing sites, landing pages, portfolios, editorial and long-form pages, campaign pages. The design *is* the product. | [references/brand.md](references/brand.md) |
| **Product** | Apps, dashboards, tools, admin surfaces. Design serves the task. | [references/product.md](references/product.md) |

Most "make me a website" requests are Brand.

### 3. Route the command

Users don't need slash commands. They can say it plainly ("make it bolder", "audit this", "polish it") and you pick the right file. If no command is clear, use `craft` to build something new or `critique` to review something that exists.

| Command | Reference | What it does |
|---|---|---|
| `craft` | [craft.md](references/craft.md) | Full flow: shape, build one HTML file, review, deliver |
| `shape` | [shape.md](references/shape.md) | Discovery interview and design brief, no code |
| `critique` | [critique.md](references/critique.md) | Design-director review with scores and priorities |
| `audit` | [audit.md](references/audit.md) | Technical quality: accessibility, performance, responsive |
| `polish` | [polish.md](references/polish.md) | Final refinement pass before shipping |
| `bolder` | [bolder.md](references/bolder.md) | Amplify a design that is too safe |
| `quieter` | [quieter.md](references/quieter.md) | Tone down one that is too loud |
| `distill` | [distill.md](references/distill.md) | Strip to the essence |
| `harden` | [harden.md](references/harden.md) | Edge cases, states, error handling, long text |
| `animate` | [animate.md](references/animate.md) | Purposeful motion |
| `colorize` | [colorize.md](references/colorize.md) | Strategic color |
| `typeset` | [typeset.md](references/typeset.md) | Typography: fonts, scale, hierarchy |
| `layout` | [layout.md](references/layout.md) | Spacing, rhythm, composition |
| `delight` | [delight.md](references/delight.md) | Moments of personality |
| `overdrive` | [overdrive.md](references/overdrive.md) | Push past conventional limits (confirm direction first) |
| `clarify` | [clarify.md](references/clarify.md) | Clearer copy, labels, and messages |
| `adapt` | [adapt.md](references/adapt.md) | Adapt across screen sizes and contexts |
| `optimize` | [optimize.md](references/optimize.md) | Performance |
| `onboard` | [onboard.md](references/onboard.md) | First-run and empty-state experiences |

### 4. Build or revise

- **Always load [references/static-html.md](references/static-html.md) before writing code.** It lists what a self-contained hosted page can and can't load, and the responsive and theme foundations.
- For a new page, start from [templates/starter.html](templates/starter.html): it already has the tokens, dark mode, safe-area handling, focus styles, and reduced-motion fallback. Replace every token and every `REPLACE` with choices from the design direction. It is a foundation, not a look.
- Load the domain references that fit the work (see below).
- When revising a page the user supplied, read their HTML first and change only what the request calls for.

### 5. Self-check before delivering

You usually can't open the page in a browser, so check it by reading and by script:

```bash
python3 scripts/check_html.py path/to/page.html
```

The checker flags measurable problems (pure black or white, gradient text, side-stripe borders, reflex-reject fonts, bounce easing, missing viewport, language, alt text, focus styles, reduced-motion fallback, blocked external resources, and more). Fix real defects it finds. A clean result is evidence, not proof: still re-read the page against the brief like a designer. If you have no shell, do the same review by hand using the checklist in [static-html.md](references/static-html.md).

### 6. Deliver

- If an Artifact or publishing tool is available, publish the single HTML file so the user gets a live, shareable page.
- Otherwise, save it as an `.html` file and present it.
- Add a short note: the direction in one line, your assumptions, anything the user must replace (placeholder facts, image slots), and an honest limitation if there is one. End with "What's working? What isn't?"

## Design laws (always apply)

### Color and typography
- **OKLCH** for colors. Tint neutrals toward the brand hue. **Never use pure black (`#000`) or pure white (`#fff`).**
- Don't reach for blue or warm orange by reflex; pick the hue as a brand decision.
- Cap body line length at **65 to 75ch**. Use a modular scale with at least a **1.25** ratio between steps, and fluid `clamp()` sizes.
- Choose fonts on purpose, from a real catalog. **Reject the reflex list** in [brand.md](references/brand.md) (Inter, Fraunces, DM Sans, Space Grotesk, Playfair Display, and others).

### Layout and motion
- Spacing and alignment make grouping; don't wrap everything in cards. **Never nest cards inside cards.**
- Avoid the centered-stack default and the **hero-metric template** (big number, small label, stats, gradient).
- Animate `transform` and `opacity` with smooth ease-out curves. **No bounce or elastic easing.** Always respect `prefers-reduced-motion`.

### Absolute bans (anti-patterns)
- **No side-stripe borders**: no thick left or right border as a card or callout accent.
- **No gradient text**: use solid colors for readability.
- **No AI slop**: no generic SaaS template, no purple-to-blue gradients, no glassmorphism by default, no identical icon-heading-text card grids, no hero-metric clichés.

### The slop test
If someone could look at it and say "AI made that" without hesitation, it has failed. Before building, name the aesthetic lane and the reference. Then describe what you're about to build the way a competitor would; if that sentence fits the modal page in the category, start over.

## Domain references

Load these when the work touches the area:

- [typography.md](references/typography.md)
- [color-and-contrast.md](references/color-and-contrast.md)
- [spatial-design.md](references/spatial-design.md)
- [motion-design.md](references/motion-design.md)
- [interaction-design.md](references/interaction-design.md)
- [responsive-design.md](references/responsive-design.md)
- [ux-writing.md](references/ux-writing.md)
- [cognitive-load.md](references/cognitive-load.md), [heuristics-scoring.md](references/heuristics-scoring.md), [personas.md](references/personas.md): used by `critique` and `audit`
- [static-html.md](references/static-html.md): technical rules for the single-file page (always)

## Tools

- `scripts/check_html.py`: static design and quality checks for one HTML file (`--json` for machine-readable output, `--strict` to fail on issues).
- `templates/starter.html`: a neutral, correct foundation for a new single-file page.
