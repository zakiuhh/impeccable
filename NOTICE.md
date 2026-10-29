# Notice

## This project

Impeccable (Claude Chat edition)
Modifications Copyright 2026 Zaki (@zakiuhh)

This is an adapted version of Impeccable for Claude Chat. It is not affiliated with or endorsed by the original authors.

## Original work: Impeccable

**Project:** Impeccable, https://impeccable.style and https://github.com/pbakaus/impeccable
**Author:** Paul Bakaus
**Copyright:** 2025-2026 Paul Bakaus
**License:** Apache License 2.0

## Upstream of the original: Anthropic frontend-design skill

The Impeccable skill builds on Anthropic's original frontend-design skill.

**Original work:** https://github.com/anthropics/skills/tree/main/skills/frontend-design
**License:** Apache License 2.0
**Copyright:** 2025 Anthropic, PBC

## Changes made in this edition

Under Section 4(b) of the Apache License 2.0, these are the modifications made to the original files:

- **Removed** parts that need a terminal, project folder, or browser harness: the `live` server and its scripts, the Node-based detector and critique-storage scripts, the `teach`, `document`, and `extract` commands, the Codex image-generation flow, and the `PRODUCT.md` / `DESIGN.md` setup.
- **Rewrote** `SKILL.md`, `references/craft.md`, and `references/critique.md` for a chat workflow that produces one self-contained static HTML file.
- **Edited** `references/shape.md` (removed the image-probe phase, added a chat-edition exception to its confirmation gate) and `references/polish.md`, and cleaned template placeholders and CLI-only passages from the remaining references.
- **Added** `references/static-html.md`, `scripts/check_html.py` (a dependency-free HTML checker), and `templates/starter.html`.
- **Unchanged in substance:** the domain references (typography, color, spatial, motion, interaction, responsive, UX writing, cognitive load, heuristics, personas, brand, product) and the remaining command references, apart from the cleanup above.

The full text of the Apache License 2.0 is in the `LICENSE` file.
