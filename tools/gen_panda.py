#!/usr/bin/env python3
"""Render the truecolor ANSI cowsay panda into GitHub-safe SVG (light + dark)."""
import re, os, textwrap

SRC   = r"C:\Users\aceso\Downloads\panda.txt"
OUT   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
MSG   = ["Hi there! I'm Abuma Hinsene.", "Software Engineering @ HiLCoE.", "Python / JavaScript / Dart."]

CW, LH, FS = 8.4, 16.0, 14.0          # char width, line height, font size
ANSI = re.compile(r"\x1b\[([0-9;]*)m")

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
    while out and not "".join(t for t, _ in out[-1]).strip():
        out.pop()
    return out

def bubble(msg):
    w = max(len(l) for l in msg)
    top = " " + "_" * (w + 2)
    bot = " " + "-" * (w + 2)
    if len(msg) == 1:
        body = ["< %s >" % msg[0].ljust(w)]
    else:
        body = []
        for i, l in enumerate(msg):
            lb, rb = ("/", "\\") if i == 0 else ("\\", "/") if i == len(msg) - 1 else ("|", "|")
            body.append("%s %s %s" % (lb, l.ljust(w), rb))
    return [top] + body + [bot]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

TOP = 34.0   # terminal title-bar height

def build(art, ink):
    lines = [[(l, ink)] for l in bubble(MSG)] + art
    cols  = max(sum(len(t) for t, _ in ln) for ln in lines)
    W, H  = cols * CW + 40, len(lines) * LH + TOP + 26
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
        'viewBox="0 0 %.0f %.0f" font-family="SFMono-Regular,Consolas,Menlo,monospace" '
        'font-size="%s" role="img" aria-label="cowsay panda saying: %s">'
        % (W, H, W, H, FS, esc(" ".join(MSG))),
        '<rect x="0.5" y="0.5" width="%.0f" height="%.0f" rx="10" fill="#0d1117" stroke="#30363d"/>' % (W-1, H-1),
        '<path d="M0.5 10.5a10 10 0 0 1 10-10h%.0f a10 10 0 0 1 10 10v23.5h-%.0f z" fill="#161b22"/>' % (W-21, W-1),
        '<circle cx="20" cy="17" r="5" fill="#ff5f56"/>',
        '<circle cx="38" cy="17" r="5" fill="#ffbd2e"/>',
        '<circle cx="56" cy="17" r="5" fill="#27c93f"/>',
        '<text x="%.1f" y="21.5" fill="#7d8590" font-size="11.5" text-anchor="middle">cowsay -f panda</text>' % (W/2),
    ]
    for i, runs in enumerate(lines):
        y, x, spans = TOP + 18 + i * LH, 20.0, []
        for text, colour in runs:
            if text:
                spans.append('<tspan x="%.1f" y="%.1f" fill="%s" xml:space="preserve">%s</tspan>'
                             % (x, y, colour or ink, esc(text)))
                x += len(text) * CW
        if spans:
            svg.append("<text>" + "".join(spans) + "</text>")
    svg.append("</svg>")
    return "\n".join(svg)

art = parse(SRC)
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "panda.svg")
open(p, "w", encoding="utf-8").write(build(art, "#e6edf3"))
print("wrote %s  (%d bytes)" % (p, os.path.getsize(p)))
print("art lines: %d" % len(art))
