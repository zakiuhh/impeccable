<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.png">
    <img alt="Impeccable logo" src="assets/logo-light.png" width="140">
  </picture>
</p>

<h1 align="center">Impeccable <sub>Chat Edition</sub></h1>

<p align="center">
  A Claude skill for building and improving distinctive, production-quality
  static HTML websites, so they don't look AI-generated.
</p>

---

## What it does

Describe a site, or paste one you already have, and Claude gathers the vibe, picks a design direction, builds **one self-contained HTML file**, checks it, and delivers it. It also reviews, polishes, and fixes existing pages.

It enforces real design laws and bans the tells of generic AI output: pure black and white, gradient text, side-stripe borders, bounce easing, nested cards, reflex fonts, and purple-gradient SaaS templates.

This edition adapts [Impeccable](https://impeccable.style) for Claude Chat. There is no project folder, terminal, or browser harness required.

## How it works

| Step | What happens |
|---|---|
| **1. Context and vibe** | Asks only what it needs: what, who, three physical-object vibe words, two or three named references |
| **2. Register** | Brand (marketing, portfolio, editorial) or Product (app, dashboard) |
| **3. Route** | Picks the right command from plain language ("make it bolder") |
| **4. Build** | Starts from a correct foundation and follows the design laws and hosting rules |
| **5. Self-check** | Runs a bundled HTML checker and re-reads the page against the brief |
| **6. Deliver** | Publishes or saves one `.html` file, with assumptions and anything to replace |

## Commands

You don't need slash commands. Just say what you want.

| Command | What it does |
|---|---|
| `craft` | Full flow: shape, build, review, deliver |
| `shape` | Discovery interview and design brief, no code |
| `critique` | Design-director review with scores and priorities |
| `audit` | Accessibility, performance, and responsive checks |
| `polish` | Final refinement pass |
| `bolder` / `quieter` | Amplify a timid design / calm a loud one |
| `distill` | Strip to the essence |
| `harden` | Edge cases, states, long text, errors |
| `animate` | Purposeful motion |
| `colorize` | Strategic color |
| `typeset` | Fonts, scale, hierarchy |
| `layout` | Spacing, rhythm, composition |
| `delight` | Moments of personality |
| `overdrive` | Push past conventional limits |
| `clarify` | Clearer copy and labels |
| `adapt` | Work across screen sizes |
| `optimize` | Performance |
| `onboard` | First-run and empty states |

## What's different from the original

| Original (CLI) | This edition (Chat) |
|---|---|
| Reads `PRODUCT.md` and `DESIGN.md` from your project | Gathers context in the conversation |
| Node detector and live-mode server | `scripts/check_html.py`, a dependency-free Python checker |
| Builds into a framework and build pipeline | One self-contained `.html` file |
| Browser and screenshot loop | Code review plus checker, and screenshots when a tool is available |
| Codex image-generation flow | Inline SVG and CSS; clear image slots instead of fake photos |

Also new: `references/static-html.md` (what a hosted, self-contained page can and can't load) and `templates/starter.html` (tokens, dark mode, safe areas, focus styles, reduced motion).

## The checker

```bash
python3 scripts/check_html.py page.html          # readable report
python3 scripts/check_html.py page.html --json   # machine-readable
python3 scripts/check_html.py page.html --strict # exit 1 if any issue
```

It reads the source only, so it can't judge the rendered result. It catches things like pure black and white, gradient text, side-stripe borders, reflex-reject fonts, bounce easing, `transition: all`, missing viewport, language, alt text, focus styles, reduced-motion fallbacks, remote images, and blocked script or stylesheet hosts.

## Example prompts

- "Build me a portfolio site for a ceramics studio. Warm, tactile, a bit imperfect."
- "Make a landing page for my open-source CLI tool. Sober and fast."
- "Critique this page" (paste your HTML)
- "Make it bolder, but keep the layout"
- "Audit the accessibility of this and fix what you find"

## Install

### Claude (web and apps)

1. Download this repo as a ZIP (or zip the `impeccable` folder yourself). Make sure `SKILL.md` sits at the top level of the folder inside the ZIP.
2. Open Claude's settings and find the Skills section.
3. Upload the ZIP and turn the skill on.

### Claude Code

Copy the folder into your skills directory:

```bash
git clone https://github.com/zakiuhh/impeccable.git
cp -r impeccable ~/.claude/skills/
```

(Change the clone URL if your repo lives somewhere else.) For serious project work in a codebase, the [original Impeccable](https://impeccable.style) is the better fit; this edition is tuned for chat.

## Repo structure

```
impeccable/
├── assets/
│   ├── logo-dark.png        # for dark backgrounds
│   └── logo-light.png       # for light backgrounds
├── references/              # commands and design domains (32 files)
├── scripts/
│   └── check_html.py        # static HTML checker
├── templates/
│   └── starter.html         # neutral single-file foundation
├── LICENSE                  # Apache-2.0
├── NOTICE.md                # credits and list of changes
├── README.md
└── SKILL.md                 # the actual skill
```

## Customizing

All the behavior lives in `SKILL.md` and `references/`. Edit the design laws, the command table, or the checker rules to fit your taste. Keep the `name` in the frontmatter the same as the folder name.

## Credits and license

This is a modified version of **Impeccable** by Paul Bakaus (2025-2026), which itself builds on Anthropic's **frontend-design** skill. Both are licensed under the **Apache License 2.0**, and so is this edition. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for the attribution and the list of changes. This project is not affiliated with or endorsed by the original authors.
