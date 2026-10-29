# Craft Flow

Build a complete static HTML page with impeccable UX and UI quality: shape the design, commit to a visual direction, build one self-contained HTML file, review it honestly, and deliver it. The exit bar is "defensible in a high-end studio review".

Before writing code you need: the register identified (and its reference loaded), and a confirmed or clearly stated design direction for this task, from [shape.md](shape.md) or supplied by the user.

Treat the approved direction as a contract for composition, hierarchy, density, atmosphere, signature motifs, and distinctive visual moves. If the finished page lacks the major ingredients of the direction, the implementation is wrong.

## Step 0: Foundation (single file by default)

In Claude Chat the deliverable is **one self-contained `.html` file**: HTML, CSS, and JS inline, no framework, no build step. Don't ask which framework to use.

- **Multi-section site** (home, about, work, contact): build it as one long page with anchored sections, or a single file with hash-based views, unless the user explicitly wants separate downloadable pages. If they do, make several linked `.html` files with relative links and shared inline-free CSS repeated per file.
- **Existing HTML the user pasted**: read it first. Keep their content, structure, and any brand decisions already made, and improve from there.
- Read [static-html.md](static-html.md) before writing code. It covers what a hosted, self-contained page can and cannot load.

## Step 1: Shape the design

Run [shape.md](shape.md) and pass along whatever the user described.

How strict the pause is depends on how much you know:

- **Sparse request** ("make me a portfolio site"): do the discovery interview. Ask 2 to 4 focused questions in chat, with concrete options, then **stop and wait**. Do not invent a full brief from a one-line prompt.
- **Clear request** (subject, audience, and some sense of vibe are all given): write a **compact brief** of 3 to 5 bullets covering what you're building, the audience, the visual lane, the color strategy, and your key assumptions, then **build in the same turn**. The user can override afterward. Say "assumptions: ..." so they know what to challenge.
- **User says "just build it"**: treat it as a clear request, state assumptions in one line, and build.
- **Brief already confirmed** earlier in the chat: use it and skip this step.

Don't pad a clear brief into a long one to look thorough, and don't skip questions on a sparse prompt to look efficient.

## Step 2: Load references

Always consult:
- [spatial-design.md](spatial-design.md) for layout and spacing
- [typography.md](typography.md) for type hierarchy
- [brand.md](brand.md) or [product.md](product.md), whichever matches the register
- [static-html.md](static-html.md) for the technical rules of a single-file page

Then add by need:
- Complex interactions or forms: [interaction-design.md](interaction-design.md)
- Animation or transitions: [motion-design.md](motion-design.md)
- Color-heavy or themed: [color-and-contrast.md](color-and-contrast.md)
- Responsive requirements: [responsive-design.md](responsive-design.md)
- Heavy on copy, labels, or errors: [ux-writing.md](ux-writing.md)

## Step 3: Visual direction without image generation

There is no native image generation here, and remote images usually can't load in a hosted page. Say that in one line, then lean on what a static page does best:

- **Type, color, layout, and rhythm** carry the design. Make deliberate choices there first.
- **Inline SVG** for illustrations, marks, diagrams, patterns, and icons. Draw them with intent, not as generic blobs.
- **CSS** for texture, gradients (never on text), shapes, masks, and atmosphere.
- **Embedded data URIs** only for small assets; keep the whole file well under the size limit.
- **Image-led briefs** (restaurants, hotels, photography, travel, food, fashion): don't fake photography with generic cards, emoji, or decorative gray boxes. Build a strong typographic and graphic composition, and put clearly labeled, well-proportioned image slots (with real alt text) where the user will drop their own photos. Tell them where the slots are.

Never ship a broken `<img>`, a guessed stock-photo URL, or a placeholder that says "image here" in the final page unless the user asked for a template.

## Step 4: Build to production quality

Build in passes so structure, visual system, states, motion, and responsive behavior each get deliberate attention. The list below is the definition of done, not inspiration.

### Production bar

- **Real content.** No lorem ipsum, placeholder copy, dead links (`href="#"` that go nowhere), fake controls, or unused scaffold. Write believable, specific copy for the subject. If you lack facts (prices, addresses, testimonials), keep them honestly generic or mark them for the user to replace, and say which ones.
- **Preserve the approved direction's major ingredients.** Missing hero treatment, signature motifs, section structure, or CTA/nav treatment are blocking defects unless the user accepted the change.
- **Semantic first.** One `<h1>`, a logical heading order, landmarks (`header`, `nav`, `main`, `footer`), real `<button>` and `<a>`, labeled form fields, accessible names for icon-only controls, `lang` on `<html>`.
- **Design tokens.** Colors, spacing, type scale, radii, and easing live as CSS variables on `:root`. Use OKLCH for color; no pure `#000` or `#fff`.
- **Deliberate spacing and alignment.** No default gaps, arbitrary margins, unbalanced whitespace, or accidental optical misalignment. Use a spacing scale.
- **Intentional typography.** A considered font pairing (not from the reflex-reject list), fluid sizes with `clamp()`, readable measure (65 to 75ch), stable line breaks, no overflow at any width.
- **Realistic state coverage.** Default, hover, `:focus-visible`, active, disabled, loading, error, success, empty, long and short text.
- **Finished interaction quality.** Keyboard paths, touch targets of at least 44px, no hover-only functionality, clear feedback timing.
- **Coherent icon set.** One style of icon throughout: inline SVG with consistent stroke and size, or accessible text. Don't mix styles, and don't use emoji as UI icons.
- **Premium motion with restraint.** Animate `transform` and `opacity`, ease out with exponential or quart curves, no bounce or elastic. Always honor `prefers-reduced-motion`. Don't animate layout properties casually, and don't block task completion with choreography.
- **Responsive by composition.** It re-flows and re-prioritizes at mobile, tablet, and desktop widths; it doesn't just shrink. Test mentally at roughly 360, 768, and 1280px.
- **Light and dark.** Provide both color schemes via `prefers-color-scheme` unless the design deliberately commits to one theme, in which case set `color-scheme` to match.
- **Self-contained and fast.** No render-blocking external requests beyond the allowed font stylesheet, no needless libraries, under the file size limit, no layout shift.
- **Ask when uncertain.** If something materially changes the brief or approved direction, stop and ask instead of guessing.

## Step 5: Review before you deliver

You usually can't open the page in a browser, so review by reading and reasoning, and use tools when you do have them.

1. **Re-read the code like a designer**, section by section, against the brief and the DON'Ts in the main skill: hierarchy, spacing rhythm, contrast, type scale, responsive behavior, state coverage, motion, and copy.
2. **Run the checker if you have a shell:**

   ```bash
   python3 scripts/check_html.py path/to/page.html
   ```

   Fix real defects it finds. A clean result is evidence, never proof the design is good.
3. **If a rendering tool is available** (a headless browser or screenshot tool), capture mobile, tablet, and desktop widths and actually look at them. A screenshot you didn't look at doesn't count.
4. **Patch material defects once.** Don't invent defects to demonstrate iteration. A confident "first pass clean, delivering" beats a fake fix.

## Step 6: Deliver

Deliver the page in the way the environment supports:

- If an **Artifact** or publishing tool is available, write the single HTML file and publish it so the user gets a live, shareable page.
- Otherwise, save it as an `.html` file in the outputs folder and present it to the user.

Then add a short message (not a long essay):
- The direction in one line (the lane, the color strategy, the type choices)
- The assumptions you made, so they can override them
- Anything they need to replace (placeholder facts, image slots, contact details)
- Honest limitations or follow-up risks
- Close with: "What's working? What isn't?"
