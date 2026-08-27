#!/usr/bin/env python3
"""Render the truecolor ANSI panda art into a GitHub-safe SVG terminal card.

Reads tools/panda.txt (ANSI 24-bit colour), writes assets/panda.svg.
No speech bubble, no caption -- just the art in a terminal frame.
"""
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(HERE, "panda.txt")
OUT  = os.path.join(ROOT, "assets")

TITLE  = "Abuma Hinsene"
LABEL  = "Panda terminal art"
CW, LH, FS = 8.4, 16.0, 14.0          # char width, line height, font size
TOP    = 34.0                          # terminal title-bar height
INK    = "#e6edf3"
ACCENT = "#00f5d4"
ANSI   = re.compile(r"\x1b\[([0-9;]*)m")


def parse(path):
    """ANSI text -> list of lines, each a list of (text, '#rrggbb' or None)."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = raw.replace("\@", "@").replace("\r", "")
    out = []
    for line in raw.split("\n"):
        runs, colour, pos = [], None, 0
        for m in ANSI.finditer(line):
            if m.start() > pos:
                runs.append((line[pos:m.start()], colour))
            codes = [c for c in m.group(1).split(";") if c != ""]
            if not codes or codes[0] == "0":
                colour = None
            elif len(codes) >= 5 and codes[0] == "38" and codes[1] == "2":
                colour = "#%02x%02x%02x" % tuple(int(c) for c in codes[2:5])
            pos = m.end()
        if pos < len(line):
            runs.append((line[pos:], colour))
        out.append(runs)
    return out


def plain(runs):
    return "".join(t for t, _ in runs)


def trim(art):
    """Drop the leading connector lines and any blank rows top and bottom."""
    # the source art starts with stray "\" connector glyphs -- drop those rows
    art = [ln for ln in art if set(plain(ln).strip()) not in ({"\\"}, set())]
    # left-trim the shared indent so the panda sits flush in the frame
    indents = [len(plain(ln)) - len(plain(ln).lstrip()) for ln in art]
    pad = min(indents) if indents else 0
    if pad:
        for ln in art:
            for i, (t, c) in enumerate(ln):
                if t.strip() or len(t) > pad:
                    ln[i] = (t[pad:], c)
                    break
                pad -= len(t)
                ln[i] = ("", c)
    return art


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(art):
    cols = max(len(plain(ln)) for ln in art)
    W = cols * CW + 40
    H = len(art) * LH + TOP + 26
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
        'viewBox="0 0 %.0f %.0f" font-family="SFMono-Regular,Consolas,Menlo,monospace" '
        'font-size="%s" role="img" aria-label="%s">' % (W, H, W, H, FS, esc(LABEL)),
        '<rect x="0.5" y="0.5" width="%.0f" height="%.0f" rx="10" fill="#0d1117" stroke="#30363d"/>' % (W - 1, H - 1),
        '<path d="M0.5 10.5a10 10 0 0 1 10-10h%.0f a10 10 0 0 1 10 10v23.5h-%.0f z" fill="#161b22"/>' % (W - 21, W - 1),
        '<circle cx="20" cy="17" r="5" fill="#ff5f56"/>',
        '<circle cx="38" cy="17" r="5" fill="#ffbd2e"/>',
        '<circle cx="56" cy="17" r="5" fill="#27c93f"/>',
        '<text x="%.1f" y="21.5" fill="%s" font-size="11.5" text-anchor="middle" '
        'opacity="0.75">%s</text>' % (W / 2, ACCENT, esc(TITLE)),
    ]
    for i, runs in enumerate(art):
        y, x, spans = TOP + 18 + i * LH, 20.0, []
        for text, colour in runs:
            if text:
                spans.append('<tspan x="%.1f" y="%.1f" fill="%s" xml:space="preserve">%s</tspan>'
                             % (x, y, colour or INK, esc(text)))
                x += len(text) * CW
        if spans:
            svg.append("<text>" + "".join(spans) + "</text>")
    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    art = trim(parse(SRC))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "panda.svg")
    open(p, "w", encoding="utf-8").write(build(art))
    print("wrote %s  (%d bytes, %d art lines)" % (p, os.path.getsize(p), len(art)))
