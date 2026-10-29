#!/usr/bin/env python3
"""
check_html.py - deterministic design and quality checks for a single HTML file.

Part of the Impeccable skill (Claude Chat edition). Standard library only.

Usage:
    python3 check_html.py page.html            # human-readable report
    python3 check_html.py page.html --json     # machine-readable output
    python3 check_html.py page.html --strict   # exit code 1 if any "issue" found

It reads the source only. It cannot see the rendered page, so treat the output
as evidence for a review, not as a verdict. A clean run does not mean the
design is good.
"""

import argparse
import colorsys
import json
import os
import re
import sys
from urllib.parse import unquote_plus, urlparse

# Fonts that are training-data defaults (see references/brand.md).
REFLEX_FONTS = [
    "Fraunces", "Newsreader", "Lora", "Crimson Pro", "Crimson Text", "Crimson",
    "Playfair Display", "Cormorant Garamond", "Cormorant", "Syne",
    "IBM Plex Mono", "IBM Plex Sans", "IBM Plex Serif", "Space Mono",
    "Space Grotesk", "Inter", "DM Sans", "DM Serif Display", "DM Serif Text",
    "Outfit", "Plus Jakarta Sans", "Instrument Sans", "Instrument Serif",
]

# Hosts a hosted Claude Chat page may load from.
ALLOWED_SCRIPT_HOSTS = {
    "cdnjs.cloudflare.com", "cdn.jsdelivr.net", "cdn.tailwindcss.com", "code.jquery.com",
}
ALLOWED_STYLE_HOSTS = {"fonts.googleapis.com"}

MAX_BYTES = 16 * 1024 * 1024

ISSUE, WARNING, NOTE = "issue", "warning", "note"
findings = []


def add(severity, rule, message, line=None, snippet=None):
    findings.append({
        "severity": severity,
        "rule": rule,
        "message": message,
        "line": line,
        "snippet": (snippet or "").strip()[:120] or None,
    })


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def mask_comments(text):
    """Blank out HTML and CSS/JS block comments but keep newlines so line numbers hold."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    return text


def hex_to_hue(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return None
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    if sat < 0.25:
        return None
    return hue * 360


def check(path):
    size = os.path.getsize(path)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    text = mask_comments(raw)
    lower = text.lower()

    if size > MAX_BYTES:
        add(ISSUE, "file-size", f"File is {size / 1024 / 1024:.1f} MB; hosted pages must stay under 16 MB.")

    # ---------- structure & accessibility ----------
    if not re.search(r"<html\b[^>]*\blang\s*=", text, re.I):
        add(ISSUE, "html-lang", "Missing lang attribute on <html>.")
    m = re.search(r"<title\b[^>]*>(.*?)</title>", text, re.I | re.S)
    if not m or not m.group(1).strip():
        add(ISSUE, "title", "Missing or empty <title>.")
    if not re.search(r'<meta\b[^>]*name\s*=\s*["\']viewport["\']', text, re.I):
        add(ISSUE, "viewport", "Missing viewport meta tag; the page won't be responsive on phones.")
    else:
        vm = re.search(r'<meta\b[^>]*name\s*=\s*["\']viewport["\'][^>]*>', text, re.I)
        tag = vm.group(0).lower()
        if "user-scalable=no" in tag.replace(" ", "") or re.search(r"maximum-scale\s*=\s*1(\.0)?\b", tag):
            add(ISSUE, "zoom-blocked", "Viewport blocks pinch zoom (user-scalable=no / maximum-scale=1).",
                line_of(text, vm.start()), vm.group(0))
        if "viewport-fit=cover" not in tag.replace(" ", "") and "safe-area-inset" in lower:
            add(WARNING, "viewport-fit", "Uses safe-area insets but the viewport lacks viewport-fit=cover.")
    h1s = re.findall(r"<h1\b", text, re.I)
    if len(h1s) == 0:
        add(WARNING, "h1", "No <h1> found.")
    elif len(h1s) > 1:
        add(WARNING, "h1", f"{len(h1s)} <h1> elements; use exactly one per page.")
    for m in re.finditer(r"<img\b(?![^>]*\balt\s*=)[^>]*>", text, re.I):
        add(ISSUE, "img-alt", "<img> without alt attribute (use alt=\"\" if decorative).",
            line_of(text, m.start()), m.group(0))
    for m in re.finditer(r"<(div|span)\b[^>]*\bonclick\s*=", text, re.I):
        add(ISSUE, "clickable-div", "Click handler on a non-semantic element; use <button> or <a>.",
            line_of(text, m.start()), m.group(0))
    n_hash = len(re.findall(r'href\s*=\s*["\']#["\']', text, re.I))
    if n_hash:
        add(WARNING, "dead-links", f"{n_hash} link(s) with href=\"#\" that go nowhere.")
    for m in re.finditer(r"lorem ipsum|dolor sit amet", lower):
        add(ISSUE, "lorem", "Placeholder lorem ipsum copy.", line_of(text, m.start()))
        break
    if re.search(r"<form\b", text, re.I) and not re.search(r"mailto:", lower):
        add(NOTE, "static-form",
            "A <form> was found. A static page cannot submit data anywhere; use a mailto: link or explain it needs a backend.")

    # focus handling
    has_focus_visible = ":focus-visible" in lower
    for m in re.finditer(r"outline\s*:\s*(none|0)\b", text, re.I):
        if not has_focus_visible:
            add(ISSUE, "outline-none", "outline removed with no :focus-visible replacement; keyboard users lose focus.",
                line_of(text, m.start()), m.group(0))
            break
    if not has_focus_visible and re.search(r"<(a|button|input|select|textarea)\b", text, re.I):
        add(WARNING, "focus-visible", "No :focus-visible styles; add a visible focus indicator for interactive elements.")

    # ---------- color ----------
    pure = re.compile(
        r"(#000(?:000)?\b(?![0-9a-f])|#fff(?:fff)?\b(?![0-9a-f])|"
        r"rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\)|"
        r"\b(?:color|background(?:-color)?|border-color|fill|stroke)\s*:\s*(?:black|white)\b)", re.I)
    hits = list(pure.finditer(text))
    if hits:
        first = hits[0]
        add(WARNING, "pure-black-white",
            f"{len(hits)} use(s) of pure black/white. Tint your neutrals toward the brand hue instead.",
            line_of(text, first.start()), first.group(0))
    if "oklch(" not in lower:
        add(NOTE, "no-oklch", "No OKLCH colors found; the skill recommends OKLCH tokens for perceptual consistency.")
    if "prefers-color-scheme" not in lower and not re.search(r"color-scheme\s*:", lower):
        add(NOTE, "no-color-scheme", "No dark-mode handling or color-scheme declaration.")

    # CSS rule blocks, for per-rule checks
    blocks = [(m.start(), m.group(0)) for m in re.finditer(r"[^{}]+\{[^{}]*\}", text)]
    for start, block in blocks:
        bl = block.lower()
        if re.search(r"background-clip\s*:\s*text", bl) or "-webkit-background-clip:text" in bl.replace(" ", ""):
            if "gradient" in bl:
                add(ISSUE, "gradient-text", "Gradient text. Use a solid color; gradient text hurts readability and reads as AI-generated.",
                    line_of(text, start + max(bl.find("background-clip"), 0)))
        for m in re.finditer(r"border-(left|right)\s*:\s*(\d+(?:\.\d+)?)px\s+solid", bl):
            if float(m.group(2)) >= 3:
                add(ISSUE, "side-stripe",
                    "Thick side-stripe border used as an accent. Use a full border, background tint, or leading icon instead.",
                    line_of(text, start + m.start()), m.group(0))
        for m in re.finditer(r"border-(left|right)-width\s*:\s*(\d+(?:\.\d+)?)px", bl):
            if float(m.group(2)) >= 3:
                add(ISSUE, "side-stripe", "Thick side-stripe border used as an accent.",
                    line_of(text, start + m.start()), m.group(0))

    # purple-blue gradient cliche (hex stops only)
    for m in re.finditer(r"(?:linear|radial|conic)-gradient\(([^;{}]*)\)", text, re.I):
        stops = re.findall(r"#[0-9a-fA-F]{3,6}\b", m.group(1))
        hues = [hex_to_hue(s) for s in stops]
        hues = [h for h in hues if h is not None]
        if len(hues) >= 2 and all(235 <= h <= 295 for h in hues):
            add(WARNING, "purple-gradient", "Purple/blue gradient: the most common AI-default look. Commit to a specific palette.",
                line_of(text, m.start()), m.group(0))
            break

    # ---------- typography ----------
    used = set()
    for m in re.finditer(r"font-family\s*:\s*([^;{}]+)", text, re.I):
        first = m.group(1).split(",")[0].strip().strip("'\"")
        for f in REFLEX_FONTS:
            if re.fullmatch(re.escape(f), first, re.I):
                used.add(f)
                add(WARNING, "reflex-font",
                    f"'{f}' is on the reflex-reject list (a training-data default). Look further.",
                    line_of(text, m.start()), m.group(0))
    for m in re.finditer(r"fonts\.googleapis\.com/css2?\?([^\"'>\s)]+)", text, re.I):
        for fam in re.findall(r"family=([^&:;]+)", m.group(1)):
            fam = unquote_plus(fam).strip()
            for f in REFLEX_FONTS:
                if re.fullmatch(re.escape(f), fam, re.I) and f not in used:
                    used.add(f)
                    add(WARNING, "reflex-font", f"Google Font '{f}' is on the reflex-reject list.",
                        line_of(text, m.start()))
    for m in re.finditer(r"\bbody\s*\{[^}]*font-size\s*:\s*(\d+(?:\.\d+)?)px", text, re.I):
        if float(m.group(1)) < 16:
            add(WARNING, "small-body", f"Body font-size is {m.group(1)}px; use at least 16px.", line_of(text, m.start()))

    # ---------- motion ----------
    for m in re.finditer(r"cubic-bezier\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)", text):
        y1, y2 = float(m.group(2)), float(m.group(4))
        if y1 > 1 or y2 > 1 or y1 < 0 or y2 < 0:
            add(WARNING, "bounce-easing", "Overshoot/bounce easing curve. Use smooth ease-out curves instead.",
                line_of(text, m.start()), m.group(0))
            break
    if re.search(r"(animation|transition)[^;{}]*\b(bounce|elastic)\b", lower) or re.search(r"@keyframes\s+\w*(bounce|elastic)", lower):
        add(WARNING, "bounce-easing", "Bounce/elastic animation found; real objects decelerate smoothly.")
    for m in re.finditer(r"transition\s*:\s*all\b", text, re.I):
        add(WARNING, "transition-all", "transition: all animates everything, including layout. List the exact properties.",
            line_of(text, m.start()), m.group(0))
        break
    for m in re.finditer(r"transition(?:-property)?\s*:[^;{}]*\b(width|height|top|left|right|bottom|margin|padding)\b", text, re.I):
        add(NOTE, "layout-animation", "Animating a layout property can cause jank; prefer transform and opacity.",
            line_of(text, m.start()), m.group(0))
        break
    has_motion = re.search(r"@keyframes|animation\s*:|transition\s*:|scroll-behavior\s*:\s*smooth", lower)
    if has_motion and "prefers-reduced-motion" not in lower:
        add(ISSUE, "reduced-motion", "Animations or smooth scrolling without a prefers-reduced-motion fallback.")

    # ---------- network & hosting ----------
    for m in re.finditer(r"<img\b[^>]*\bsrc\s*=\s*[\"'](https?:)?//[^\"']+", text, re.I):
        add(ISSUE, "remote-image", "Remote image; hosted pages block external images. Use inline SVG or a data: URI.",
            line_of(text, m.start()), m.group(0))
        break
    for m in re.finditer(r"url\(\s*[\"']?(https?:)?//[^)\"']+", text, re.I):
        if "fonts.gstatic.com" in m.group(0) or "fonts.googleapis.com" in m.group(0):
            continue
        add(ISSUE, "remote-css-url", "CSS url() points at an external host; it will not load in a hosted page.",
            line_of(text, m.start()), m.group(0))
        break
    for m in re.finditer(r"<script\b[^>]*\bsrc\s*=\s*[\"']((?:https?:)?//[^\"']+)[\"']", text, re.I):
        src = m.group(1)
        host = urlparse(src if src.startswith("http") else "https:" + src).hostname or ""
        if host not in ALLOWED_SCRIPT_HOSTS:
            add(ISSUE, "script-host", f"Script from '{host}' is blocked in hosted pages.", line_of(text, m.start()), src)
        else:
            if "@latest" in src or (host == "cdn.jsdelivr.net" and not re.search(r"@\d", src)) \
                    or (host == "cdn.tailwindcss.com" and not re.search(r"cdn\.tailwindcss\.com/\d", src)):
                add(WARNING, "unpinned-script", "CDN script without an exact pinned version.", line_of(text, m.start()), src)
    for m in re.finditer(r"<link\b[^>]*\bhref\s*=\s*[\"']((?:https?:)?//[^\"']+)[\"'][^>]*>", text, re.I):
        tag = m.group(0).lower()
        src = m.group(1)
        host = urlparse(src if src.startswith("http") else "https:" + src).hostname or ""
        is_style = "stylesheet" in tag
        if is_style and host not in ALLOWED_STYLE_HOSTS:
            add(ISSUE, "style-host", f"Stylesheet from '{host}' is blocked in hosted pages. Inline the CSS.",
                line_of(text, m.start()), src)
    if re.search(r"@import\s+(url\()?[\"']?https?:", text, re.I):
        add(WARNING, "css-import", "@import of an external stylesheet; only the Google Fonts stylesheet is allowed.")
    for m in re.finditer(r"\b(fetch|XMLHttpRequest)\b\s*\(?\s*[\"']?https?://", text):
        add(WARNING, "network-request", "Network request to an external host; hosted pages can't make them.",
            line_of(text, m.start()), m.group(0))
        break

    # storage safety
    if re.search(r"\b(localStorage|sessionStorage)\b", text) and not re.search(r"\btry\s*\{", text):
        add(WARNING, "storage-try", "Browser storage used without try/catch; it can be unavailable or empty.")

    return size


def main():
    ap = argparse.ArgumentParser(description="Static design and quality checks for one HTML file.")
    ap.add_argument("file", help="path to an .html file")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any 'issue' is found")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        print(f"error: file not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    size = check(args.file)
    order = {ISSUE: 0, WARNING: 1, NOTE: 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["line"] or 10**9))
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in (ISSUE, WARNING, NOTE)}

    if args.json:
        print(json.dumps({"file": args.file, "bytes": size, "counts": counts, "findings": findings}, indent=2))
    else:
        print(f"check_html: {args.file} ({size / 1024:.1f} KB)")
        print(f"  {counts[ISSUE]} issue(s), {counts[WARNING]} warning(s), {counts[NOTE]} note(s)\n")
        label = {ISSUE: "ISSUE  ", WARNING: "WARNING", NOTE: "NOTE   "}
        for f in findings:
            where = f"line {f['line']}" if f["line"] else "file"
            print(f"[{label[f['severity']]}] {f['rule']} ({where}): {f['message']}")
            if f["snippet"]:
                print(f"           > {f['snippet']}")
        if not findings:
            print("No findings. That is evidence, not proof: review the design yourself.")
        print("\nStatic source checks only. Layout, contrast in context, and overall quality need human judgment.")

    sys.exit(1 if (args.strict and counts[ISSUE]) else 0)


if __name__ == "__main__":
    main()
