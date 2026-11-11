#!/usr/bin/env python3
"""Generates assets/brand/*.svg + *.png (logo mark, wordmark lockup and stacked logo in color, white, black;
the stacked logo also has a color-on-dark variant).
Dev-time only; outputs are committed. Needs fonttools (venv) and rsvg-convert.
Usage: python3 _build/brand_assets.py /path/to/Inter[opsz,wght].ttf"""
import os, sys, subprocess
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "brand")
os.makedirs(OUT, exist_ok=True)

font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 400, "opsz": 14})
gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
hmtx = font["hmtx"]

# Palette: "color" is for light backgrounds
COLOR = dict(c1="#40916C", c2="#6AB58E", c4="#2D6A4F", gold="#D4A63C", t1="#0B1F16", t2="#2D6A4F")
WHITE = dict(c1="#fff", c2="#fff", c4="#fff", gold="#fff", t1="#fff", t2="#fff")
BLACK = dict(c1="#000", c2="#000", c4="#000", gold="#000", t1="#000", t2="#000")
VARIANTS = {"color": COLOR, "white": WHITE, "black": BLACK}
# Stacked only: color mark with light text, for deep green or black backgrounds
COLOR_DARK = dict(COLOR, t1="#F5F2EA", t2=COLOR["c2"])
STACKED = {"color": COLOR, "color-dark": COLOR_DARK, "white": WHITE, "black": BLACK}

def mark_body(p):
    return (f'<rect x="2" y="2" width="46" height="46" rx="12" fill="{p["c1"]}"/>'
            f'<rect x="52" y="2" width="46" height="46" rx="12" fill="{p["c2"]}"/>'
            f'<rect x="52" y="52" width="46" height="46" rx="12" fill="{p["c4"]}"/>'
            f'<rect x="8" y="58" width="34" height="34" rx="8" transform="rotate(45 25 75)" fill="{p["gold"]}"/>')

def text_paths(text, size, x0, baseline, colors):
    """Outline text with Inter; returns (svg paths, end x). colors: fill per word index."""
    s = size / upm
    x, out, word = x0, [], 0
    for ch in text:
        if ch == " ":
            x += hmtx[cmap[32]][0] * s; word += 1; continue
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        out.append(f'<path d="{pen.getCommands()}" fill="{colors[word]}"/>')
        x += hmtx[g][0] * s
    return "".join(out), x

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}">{body}</svg>\n'

H = 100
for name, p in VARIANTS.items():
    mark = svg(100, 100, mark_body(p))
    # wordmark lockup: mark (100 tall) + text sized to sit beside it (cap-height-ish, x-height centered)
    size = 74
    baseline = 50 + 0.36 * size  # optical vertical centre for lowercase text with descender (y)
    gap = 28
    paths, end = text_paths("oddly sunny", size, 100 + gap, baseline, [p["t1"], p["t2"]])
    w = round(end + 2, 1)
    lock = svg(w, H, mark_body(p) + paths)
    for stem, data in (("logo", mark), ("wordmark", lock)):
        base = os.path.join(OUT, f"{stem}-{name}")
        open(base + ".svg", "w").write(data)
        wpx = 1024 if stem == "logo" else 2048
        subprocess.run(["rsvg-convert", "-w", str(wpx), base + ".svg", "-o", base + ".png"], check=True)

def stacked(p):
    """Mark above the name, name centred. Mark is 100 wide; text is ~1.7x that, as in the approved stacked art."""
    size, baseline = 29.5, 135.2  # baseline puts the ascender ~15 below the mark
    paths, end = text_paths("oddly sunny", size, 0, baseline, [p["t1"], p["t2"]])
    w = max(100, end)
    body = f'<g transform="translate({(w - 100) / 2:.2f} 0)">{mark_body(p)}</g>' + paths
    pad = 8  # breathing room so the text never touches the edge
    vw, vh = round(w + 2 * pad, 1), 160
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {vw:g} {vh}" width="{vw:g}" height="{vh}">{body}</svg>\n'

for name, p in STACKED.items():
    base = os.path.join(OUT, f"stacked-{name}")
    open(base + ".svg", "w").write(stacked(p))
    subprocess.run(["rsvg-convert", "-w", "1536", base + ".svg", "-o", base + ".png"], check=True)
print(sorted(os.listdir(OUT)))
