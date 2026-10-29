# Critique Flow

### Purpose

Review a page or design the way a design director would: honest, specific, prioritized. Give the user a scored critique and ask what they want improved next. The chat response is the deliverable.

### Setup

1. **Identify the target.** It is one of: HTML the user pasted or uploaded, a page you built earlier in this chat, a screenshot, or a description. Read the HTML or look at the image closely before judging anything.
2. **Know the intent.** Use what the user already told you (audience, vibe, goal). If a critical piece is missing and changes the verdict, ask one short question; otherwise state your assumption in a line and continue.

### Assessment A: Design Review (do this first)

Think like a design director. Read the source (or study the screenshot) and evaluate:
- **AI slop**: Would someone believe "AI made this" immediately? Check all the DON'T guidance from the main skill and the reflex-reject lists in [brand.md](brand.md).
- **Holistic design**: hierarchy, IA, emotional fit, discoverability, composition, typography, color, accessibility, states, copy, and edge cases.
- **Cognitive load**: consult [cognitive-load](cognitive-load.md); report checklist failures and decision points with >4 visible options.
- **Emotional journey**: peak-end rule, emotional valleys, reassurance at high-stakes moments.
- **Nielsen heuristics**: consult [heuristics-scoring](heuristics-scoring.md); score all 10 heuristics 0-4.

Form your verdict before running any script, so automated output doesn't anchor your judgment.

### Assessment B: Deterministic check (optional)

If you have the HTML as a file and a shell, run:

```bash
python3 scripts/check_html.py path/to/page.html
```

It reports static, measurable issues only: pure black or white, gradient text, side-stripe borders, reflex-reject fonts, bounce easing, `transition: all`, missing viewport, language, alt text, focus styles, reduced-motion handling, and more. It cannot see the rendered layout, so treat results as evidence rather than a verdict, and call out false positives. If you can't run it, skip it and say so.

### Generate Combined Critique Report

Combine your design review with any deterministic check results into a single report. Do NOT simply concatenate. Weave the findings together, noting where the check agrees with your review, where it caught something you missed, and where its findings are false positives.

The chat response is the deliverable. Present the full structured critique below in chat; do not replace it with a short summary.

Structure your feedback as a design director would:

#### Design Health Score
> *Consult [heuristics-scoring](heuristics-scoring.md)*

Present the Nielsen's 10 heuristics scores as a table:

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | ? | [specific finding or "n/a" if solid] |
| 2 | Match System / Real World | ? | |
| 3 | User Control and Freedom | ? | |
| 4 | Consistency and Standards | ? | |
| 5 | Error Prevention | ? | |
| 6 | Recognition Rather Than Recall | ? | |
| 7 | Flexibility and Efficiency | ? | |
| 8 | Aesthetic and Minimalist Design | ? | |
| 9 | Error Recovery | ? | |
| 10 | Help and Documentation | ? | |
| **Total** | | **??/40** | **[Rating band]** |

Be honest with scores. A 4 means genuinely excellent. Most real interfaces score 20-32.

#### Anti-Patterns Verdict

**Start here.** Does this look AI-generated?

**LLM assessment**: Your own evaluation of AI slop tells. Cover overall aesthetic feel, layout sameness, generic composition, missed opportunities for personality.

**Deterministic scan** (only if you ran `scripts/check_html.py`): Summarize what it found, with counts and line numbers. Note any issues it caught that you missed, and flag any false positives. If you couldn't run it, say so in one line.

#### Overall Impression
A brief gut reaction: what works, what doesn't, and the single biggest opportunity.

#### What's Working
Highlight 2-3 things done well. Be specific about why they work.

#### Priority Issues
The 3-5 most impactful design problems, ordered by importance.

For each issue, tag with **P0-P3 severity** (consult [heuristics-scoring](heuristics-scoring.md) for severity definitions):
- **[P?] What**: Name the problem clearly
- **Why it matters**: How this hurts users or undermines goals
- **Fix**: What to do about it (be concrete)
- **Suggested command**: Which command could address this (from: craft, shape, critique, audit, polish, adapt, animate, bolder, clarify, colorize, delight, distill, harden, layout, onboard, optimize, overdrive, quieter, typeset)

#### Persona Red Flags
> *Consult [personas](personas.md)*

Auto-select 2-3 personas most relevant to this interface type (use the selection table in the reference). If the user has described their audience or brand, also generate 1-2 project-specific personas from that.

For each selected persona, walk through the primary user action and list specific red flags found:

**Alex (Power User)**: No keyboard shortcuts detected. Form requires 8 clicks for primary action. Forced modal onboarding. High abandonment risk.

**Jordan (First-Timer)**: Icon-only nav in sidebar. Technical jargon in error messages ("404 Not Found"). No visible help. Will abandon at step 2.

Be specific. Name the exact elements and interactions that fail each persona. Don't write generic persona descriptions; write what broke for them.

#### Minor Observations
Quick notes on smaller issues worth addressing.

#### Questions to Consider
Provocative questions that might unlock better solutions:
- "What if the primary action were more prominent?"
- "Does this need to feel this complex?"
- "What would a confident version of this look like?"

**Remember**:
- Be direct. Vague feedback wastes everyone's time.
- Be specific. "The submit button," not "some elements."
- Say what's wrong AND why it matters to users.
- Give concrete suggestions. Cut "consider exploring..." entirely.
- Prioritize ruthlessly. If everything is important, nothing is.
- Don't soften criticism. Developers need honest feedback to ship great design.

### Ask the User

**After presenting findings**, use targeted questions based on what was actually found. These answers will shape the action plan.

Ask questions along these lines (adapt to the specific findings; do NOT ask generic questions):

1. **Priority direction**: Based on the issues found, ask which category matters most to the user right now. For example: "I found problems with visual hierarchy, color usage, and information overload. Which area should we tackle first?" Offer the top 2-3 issue categories as options.

2. **Design intent**: If the critique found a tonal mismatch, ask whether it was intentional. For example: "The interface feels clinical and corporate. Is that the intended tone, or should it feel warmer/bolder/more playful?" Offer 2-3 tonal directions as options based on what would fix the issues found.

3. **Scope**: Ask how much the user wants to take on. For example: "I found N issues. Want to address everything, or focus on the top 3?" Offer scope options like "Top 3 only", "All issues", "Critical issues only".

4. **Constraints** (optional; only ask if relevant): If the findings touch many areas, ask if anything is off-limits. For example: "Should any sections stay as-is?" This prevents the plan from touching things the user considers done.

**Rules for questions**:
- Every question must reference specific findings from the report. Never ask generic "who is your audience?" questions.
- Keep it to 2-4 questions maximum. Respect the user's time.
- Offer concrete options, not open-ended prompts.
- If findings are straightforward (e.g., only 1-2 clear issues), skip questions and go directly to Recommended Actions.

### Recommended Actions

**After receiving the user's answers**, present a prioritized action summary reflecting the user's priorities and scope from Ask the User.

#### Action Summary

List recommended commands in priority order, based on the user's answers:

1. **`command-name`**: Brief description of what to fix (specific context from critique findings)
2. **`command-name`**: Brief description (specific context)
...

**Rules for recommendations**:
- Only recommend commands from: craft, shape, critique, audit, polish, adapt, animate, bolder, clarify, colorize, delight, distill, harden, layout, onboard, optimize, overdrive, quieter, typeset
- Order by the user's stated priorities first, then by impact
- Each item's description should carry enough context that the command knows what to focus on
- Map each Priority Issue to the appropriate command
- Skip commands that would address zero issues
- If the user chose a limited scope, only include items within that scope
- If the user marked areas as off-limits, exclude commands that would touch those areas
- End with `polish` as the final step if any fixes were recommended

After presenting the summary, tell the user:

> You can ask me to run these one at a time, all at once, or in any order you prefer.
>
> Ask me to re-run `critique` after fixes to see your score improve.
