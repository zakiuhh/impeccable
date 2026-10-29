# Static HTML in Claude Chat

Technical rules for building a **single, self-contained HTML page** that works when Claude Chat hosts or previews it. The design thinking lives in the other references; this file keeps the page from silently breaking.

These rules reflect how hosted pages in Claude Chat behave. If your environment is more permissive (you're only saving a file for download), you may relax the network rules, but the accessibility and responsive rules always apply.

## 1. One file, nothing else

- Everything lives in one `.html` file: markup, CSS in a `<style>` tag, JS in a `<script>` tag.
- Keep it **under 16 MB**, including anything embedded as a data URI. Most pages should be a small fraction of that.
- No local file references (`./img/photo.jpg`, `styles.css`). They won't resolve.

## 2. What can load from outside

Hosted pages run under a strict content-security policy. Anything outside the allowlist fails **silently**, so a page can look fine in your head and be broken for the viewer.

| Resource | Allowed | Notes |
|---|---|---|
| Scripts | `cdnjs.cloudflare.com` (preferred), `cdn.jsdelivr.net/npm/`, `cdn.tailwindcss.com`, `code.jquery.com` | Nothing else, including unpkg and esm.sh |
| Stylesheets | `fonts.googleapis.com` only | Fonts download from `fonts.gstatic.com` |
| Images | **Inline only** (inline SVG or `data:` URIs) | Remote `<img src="https://...">` will not load |
| Network requests | None | No `fetch` or form posts to other sites |

Consequences for design:

- **Images**: draw with inline SVG and CSS, or embed small `data:` URIs. Don't reference stock photo URLs; they won't render.
- **Libraries**: a library's own CSS or web fonts won't load. Prefer libraries that work as a script alone, or skip libraries. Most static pages need none.
- **Version pinning**: if you load a script, pin an exact version (never `latest` or a bare name), and choose a release at least two weeks old.
- **Contact forms**: a static page can't submit data anywhere. Use a `mailto:` link, or tell the user honestly that a form needs a backend and offer a mailto-based alternative.
- **Downloads**: plain download links and script-triggered saves may do nothing in a hosted page. Don't depend on them.

## 3. Fonts

- Load at most two families from Google Fonts with a single `<link>` and `display=swap`.
- Choose fonts on purpose: check the reflex-reject list in [brand.md](brand.md) before settling.
- Always give a **real fallback stack** (for example a serif or sans-serif system stack with sensible metrics), because the page must look right if the font stylesheet is slow or blocked.
- Only request the weights and styles you actually use.

## 4. Theme, color, and responsive foundation

Define colors as tokens on `:root`, then redefine them for dark mode:

```css
:root {
  color-scheme: light dark;
  --bg: oklch(98% 0.008 85);
  --text: oklch(24% 0.02 260);
  --accent: oklch(58% 0.19 35);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: oklch(18% 0.015 260);
    --text: oklch(92% 0.01 85);
  }
}
:root[data-theme="dark"] {
  --bg: oklch(18% 0.015 260);
  --text: oklch(92% 0.01 85);
}
body { background: var(--bg); color: var(--text); }
```

- Give `body` an explicit background, and make every text color and the surface behind it come from tokens.
- Use relative units, flexbox, and grid. Images and SVG get `max-width: 100%`.
- Wide content (tables, code, diagrams) scrolls inside its own `overflow-x: auto` wrapper so the page itself never scrolls sideways.
- A deliberately single-theme design is fine, but then set `color-scheme` to match so form controls and scrollbars agree.

## 5. Phones and safe areas

Declare the viewport so the page can draw edge to edge, then keep content clear of the system bars:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
:root {
  box-sizing: border-box;
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
html { scroll-padding-top: env(safe-area-inset-top, 0px); }
```

- Elements fixed to the top or bottom add the matching `env(safe-area-inset-*)` to their padding.
- A sticky header uses `top: env(safe-area-inset-top, 0px)` instead of `0`.
- Size one-screen layouts with `height: 100%` on `html` and `body`, not `100vh`.

## 6. Storage and state

- `localStorage`, `sessionStorage`, and IndexedDB work, but they are private to that viewer's browser and are never shared between visitors.
- **Wrap every read and write in `try/catch`** and render correctly when storage is empty or unavailable.
- Use storage only for per-viewer conveniences (a remembered tab, a theme choice, an unsent draft). Don't build features that assume shared data on a static page.

## 7. Navigation inside the page

- Same-page anchors (`#about`) are fine and recommended for single-page sites. Smooth scrolling must respect `prefers-reduced-motion`.
- For multiple views, use plain hash names made of ASCII letters, digits, and hyphens (for example `#pricing`). Avoid `#/path` style routes, query strings, and key-value hashes.
- Show the view named in `location.hash` on load and on `hashchange`; show the start view if there is none.

## 8. Details that make it feel finished

- Add a favicon as an inline SVG emoji or mark:
  `<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✦</text></svg>">`
- Write a real `<title>` and a `<meta name="description">`.
- Use typographic punctuation in all visible text: ’ for apostrophes and the proper quotation marks for the text's language (“ ” in English). Keep straight quotes in HTML, CSS, JS, and JSON syntax.
- Use real en and em dashes where they belong, and non-breaking spaces to avoid awkward line breaks in short headings.

## 9. Pre-delivery checklist

- [ ] One file, no local references, under the size limit
- [ ] No remote images; no scripts or stylesheets from disallowed hosts
- [ ] Every library version pinned; font fallbacks present
- [ ] Colors are tokens; dark mode (or a committed `color-scheme`) handled
- [ ] Viewport meta with `viewport-fit=cover`; safe-area padding applied
- [ ] No sideways page scroll at 360px wide
- [ ] `lang`, `<title>`, one `<h1>`, landmarks, labeled controls, visible `:focus-visible`
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Storage reads and writes wrapped in `try/catch`
- [ ] No fake forms, dead links, or placeholder copy
