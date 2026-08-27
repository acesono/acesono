#!/usr/bin/env python3
"""Render the truecolor ANSI panda art into a GitHub-safe SVG.

Reads tools/panda.txt (ANSI 24-bit colour), writes assets/panda.svg.
Art only -- no window chrome, no title bar, no caption. The art is cropped
tight to its own bounds and sits on a flat rounded dark panel, which the
white glyphs of the panda's face need in order to stay visible on GitHub's
light theme.
"""
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(HERE, "panda.txt")
OUT  = os.path.join(ROOT, "assets")

LABEL = "Panda ASCII art"
BG    = "#0d1117"     # panel fill; set to None for a transparent background
PAD   = 18.0          # padding around the art, in px
RADIUS = 12.0
CW, LH, FS = 8.4, 16.0, 14.0          # char width, line height, font size
INK   = "#e6edf3"
ANSI  = re.compile(r"\x1b\[([0-9;]*)m")


def parse(path):
    """ANSI text -> list of lines, each a list of (char, '#rrggbb' or None)."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = raw.replace("\@", "@").replace("\r", "")
    lines = []
    for line in raw.split("\n"):
        chars, colour, pos = [], None, 0
        for m in ANSI.finditer(line):
            chars += [(c, colour) for c in line[pos:m.start()]]
            codes = [c for c in m.group(1).split(";") if c != ""]
            if not codes or codes[0] == "0":
                colour = None
            elif len(codes) >= 5 and codes[0] == "38" and codes[1] == "2":
                colour = "#%02x%02x%02x" % tuple(int(c) for c in codes[2:5])
            pos = m.end()
        chars += [(c, colour) for c in line[pos:]]
        lines.append(chars)
    return lines


def crop(lines):
    """Drop the stray leading connector glyphs, then crop to the art's bounds."""
    lines = [ln for ln in lines if set("".join(c for c, _ in ln).strip()) != {"\\"}]

    def bounds(ln):
        cols = [i for i, (c, _) in enumerate(ln) if c.strip()]
        return (cols[0], cols[-1]) if cols else None

    box = [b for b in map(bounds, lines) if b]
    if not box:
        return lines
    left  = min(b[0] for b in box)
    right = max(b[1] for b in box)

    out = [ln[left:right + 1] for ln in lines]
    while out and not "".join(c for c, _ in out[0]).strip():
        out.pop(0)
    while out and not "".join(c for c, _ in out[-1]).strip():
        out.pop()
    return out


def runs(line):
    """Regroup a char list into (text, colour) runs so the SVG stays small."""
    out = []
    for ch, col in line:
        if out and out[-1][1] == col:
            out[-1][0] += ch
        else:
            out.append([ch, col])
    return [(t, c) for t, c in out]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(art):
    cols = max(len(ln) for ln in art)
    W = cols * CW + PAD * 2
    H = len(art) * LH + PAD * 2
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
           'viewBox="0 0 %.0f %.0f" font-family="SFMono-Regular,Consolas,Menlo,monospace" '
           'font-size="%s" role="img" aria-label="%s">' % (W, H, W, H, FS, esc(LABEL))]
    if BG:
        svg.append('<rect width="%.0f" height="%.0f" rx="%.0f" fill="%s"/>' % (W, H, RADIUS, BG))
    for i, line in enumerate(art):
        y, x, spans = PAD + 12 + i * LH, PAD, []
        for text, colour in runs(line):
            if text.strip():
                spans.append('<tspan x="%.1f" y="%.1f" fill="%s" xml:space="preserve">%s</tspan>'
                             % (x, y, colour or INK, esc(text)))
            x += len(text) * CW
        if spans:
            svg.append("<text>" + "".join(spans) + "</text>")
    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    art = crop(parse(SRC))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "panda.svg")
    open(p, "w", encoding="utf-8").write(build(art))
    print("wrote %s  (%d bytes, %d rows x %d cols)"
          % (p, os.path.getsize(p), len(art), max(len(l) for l in art)))
