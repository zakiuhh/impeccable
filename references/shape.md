Shape the UX and UI for a feature before any code is written. This command produces a **design brief**: a structured artifact that guides implementation through discovery, not guesswork.

**Scope**: Design planning only. This command does NOT write code. It produces the thinking that makes code good.

**Output**: A design brief that can be handed off to `craft`, or used directly for freeform implementation.

## Philosophy

Most AI-generated UIs fail not because of bad code, but because of skipped thinking. They jump to "here's a card grid" without asking "what is the user trying to accomplish?" This command inverts that: understand deeply first, so implementation is precise.

## Phase 1: Discovery Interview

**Do NOT write any code or make any design decisions during this phase.** Your only job is to understand the feature deeply enough to make excellent design decisions later.

This is a required interaction, not optional guidance. Ask these questions in conversation, adapting based on answers. Don't dump them all at once; have a natural dialogue. Ask the user in chat.

### Interview cadence

Discovery includes at least one user-answer round unless the user's message or an already-confirmed brief directly answers the needed inputs. With a sparse prompt, do **not** synthesize a complete brief for confirmation on the first response.

- Use the harness's structured question tool when one exists. Otherwise, ask directly in chat and stop.
- Ask **2-3 questions per round**, then wait for answers.
- Treat anything the user already told you as an anchor; it reduces repeated questions but does **not** replace shape for craft. Shape is task-specific.
- One round is the default. Add a second only if the first answers leave material gaps. Don't run a second round just to feel thorough.
- Round 1 should clarify purpose, audience/context, content/scope, and (for brand) visual direction.
- Round 2, when needed, fills in whatever's still genuinely missing.

**Assert-then-confirm, not menu-with-escape.** When the user's message and the context so far make one option obvious, name it and ask the user to confirm or override. Don't enumerate "Restrained / Committed / Or something else?" as a real choice; "This reads as Restrained, confirm?" beats a four-option menu when the answer is already clear.

### Purpose & Context
- What is this feature for? What problem does it solve?
- Who specifically will use it? (Not "users"; be specific: role, context, frequency)
- What does success look like? How will you know this feature is working?
- What's the user's state of mind when they reach this feature? (Rushed? Exploring? Anxious? Focused?)

### Content & Data
- What content or data does this feature display or collect?
- What are the realistic ranges? (Minimum, typical, maximum, e.g., 0 items, 5 items, 500 items)
- What are the edge cases? (Empty state, error state, first-time use, power user)
- Is any content dynamic? What changes and how often?
- What visual assets are real content here? Note required images, product shots, illustrations, maps, textures, diagrams, generated objects, or existing project assets.

### Design Direction

Force a visual decision on three fronts. Skip anything the context so far already answers; ask only what's missing.

- **Color strategy for this surface.** Pick one: Restrained / Committed / Full palette / Drenched. Can override the project default if the surface earns it (e.g. a drenched hero inside an otherwise Restrained product).
- **Theme via scene sentence.** Write one sentence of physical context for this surface: who uses it, where, under what ambient light, in what mood. The sentence forces dark vs light. If it doesn't, add detail until it does.
- **Two or three named anchor references.** Specific products, brands, objects. Not adjectives like "modern" or "clean."

### Scope

Always ask. Sketch quality and shipped quality are different outputs; don't guess between them.

- **Fidelity.** Sketch / mid-fi / high-fi / production-ready?
- **Breadth.** One screen / a flow / a whole surface?
- **Interactivity.** Static visual / interactive prototype / shipped-quality component?
- **Time intent.** Quick exploration, or polish until it ships?

Scope answers are task-scoped; carry them through the design brief only.

### Constraints
- Are there technical constraints? (performance budget, browser support, must it work offline or print well?)
- Are there content constraints? (Localization, dynamic text length, user-generated content)
- Mobile/responsive requirements?
- Accessibility requirements beyond WCAG AA?

### Anti-Goals
- What should this NOT be? What would be a wrong direction?
- What's the biggest risk of getting this wrong?

## Phase 2: Design Brief

After the interview, present a brief and **end your response**. The user must confirm before any implementation runs. Do not present a brief and then continue to code in the same response, even if the brief feels obvious to you. The user's confirmation is the gate.

**Chat edition exception:** this strict pause applies whenever `shape` runs on its own, and whenever the request was sparse. When `craft` runs shape for a *clear* request (subject, audience, and vibe already given), the compact brief ends with your stated assumptions and `craft` continues straight into the build in the same turn. See [craft.md](craft.md), Step 1. The user can still override afterward.

**Choose the brief shape based on how clear the answers are:**

- **Compact form (3-5 bullets)** when discovery was crisp and the original prompt + the context so far already pinned scope, content, and direction. State what you're building, the visual lane, and end with one or two specific questions or a clear "confirm or override?" prompt. This is the default for typical craft requests with a clear prompt.
- **Full structured form (sections below)** when the task is genuinely ambiguous, multi-screen, or when the user asked for shape as a standalone step. Use this when the discipline of structure earns its weight.

Don't pad a clear brief into a long one to look thorough. A 70-line brief restating answers the user just gave is noise, not rigor. Equally, don't skip the confirmation pause to look efficient: the pause is the point.

Present the brief, then **stop and wait for explicit confirmation**. You are not the judge of whether the user already approved. Even when the brief feels obviously right, ask once and wait. The pause is what separates shape from premature implementation.

### Brief Structure

**1. Feature Summary** (2-3 sentences)
What this is, who it's for, what it needs to accomplish.

**2. Primary User Action**
The single most important thing a user should do or understand here.

**3. Design Direction**
Color strategy (Restrained / Committed / Full palette / Drenched) + the theme scene sentence + 2–3 named anchor references. Reference the context so far where they already answer, and note any per-surface overrides.

If you ran the Visual Direction Probe step, name which probe direction won and what changed in the brief because of it.

**4. Scope**
Fidelity, breadth, interactivity, and time intent from the Scope section of the interview. Task-scoped; these don't persist beyond the brief.

**5. Layout Strategy**
High-level spatial approach: what gets emphasis, what's secondary, how information flows. Describe the visual hierarchy and rhythm, not specific CSS.

**6. Key States**
List every state the feature needs: default, empty, loading, error, success, edge cases. For each, note what the user needs to see and feel.

**7. Interaction Model**
How users interact with this feature. What happens on click, hover, scroll? What feedback do they get? What's the flow from entry to completion?

**8. Content Requirements**
What copy, labels, empty state messages, error messages, and microcopy are needed. Note any dynamic content and its realistic ranges. For image-led surfaces, also list the required image/media roles and their likely source (project asset, generated raster, semantic SVG/CSS, canvas/WebGL, icon library, or accepted omission).

**9. Recommended References**
Based on the brief, list which impeccable reference files would be most valuable during implementation (e.g., spatial-design.md for complex layouts, motion-design.md for animated features, interaction-design.md for form-heavy features).

**10. Open Questions**
Anything genuinely unresolved. Don't list "open questions" you've already recommended a default for; assert the default and move on. If you'd write `Recommend: X` next to a question, just decide X.

---

Ask for explicit confirmation of the brief before finishing.

If the user disagrees with any part, revisit the relevant discovery questions. A shape run is incomplete until the user confirms direction.

Once confirmed, the brief is complete. The user can now hand it to `craft`, or use it to guide any other implementation approach. (If the user wants the full discovery-then-build flow in one step, they should use craft instead, which runs this command internally.)
