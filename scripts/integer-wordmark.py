"""Write public/integer-wordmark.svg: the INTEGER wordmark with its carbon copy, as integer.run draws it.

The letters come from integer.run's generated wordmark.js (Syncopate Bold outlines, font units, baseline y = 0, y down);
the copy is offset 0.07 em down and right in carbon (#3f3d40, 0.6) with the same grain filter as the live page.

    python scripts/integer-wordmark.py [path/to/wordmark.js]
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else r"F:\Integer\landing\site\wordmark.js")
OUT = Path(__file__).resolve().parent.parent / "public" / "integer-wordmark.svg"

INK, CARBON = "#221e1b", "#3f3d40"
WIDTH = 300.0                        # nominal px width of the letters; the grain is tuned to this size

wm = json.loads(re.search(r"=\s*(\{.*\})\s*;?\s*$", SRC.read_text(encoding="utf-8"), re.S).group(1))
k = WIDTH / wm["width"]
off = 0.07 * wm["upem"] * k
cap = wm["cap"] * k
desc = 40 * k                        # G dips just below the baseline

letters = "".join(f'<path transform="translate({l["x"]} 0)" d="{l["d"]}"/>' for l in wm["letters"])
glyphs = f'<g transform="translate(0 {cap:.3f}) scale({k:.6f})">{letters}</g>'

w, h = WIDTH + off, cap + desc + off
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}" height="{h:.2f}">
<title>INTEGER</title>
<defs>
<filter id="carbon" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="1" seed="11" result="grain"/>
<feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -1.1 0 0 0 1.45" result="speck"/>
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="23" result="cloud"/>
<feColorMatrix in="cloud" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -0.7 0 0 0 1.2" result="mottle"/>
<feComposite in="SourceGraphic" in2="speck" operator="in" result="tex0"/>
<feComposite in="tex0" in2="mottle" operator="in"/>
</filter>
</defs>
<g filter="url(#carbon)" opacity="0.6"><g fill="{CARBON}" transform="translate({off:.3f} {off:.3f})">{glyphs}</g></g>
<g fill="{INK}">{glyphs}</g>
</svg>
"""
OUT.write_text(svg, encoding="utf-8", newline="\n")
print(OUT, f"{w:.1f}x{h:.1f}", len(svg), "bytes")
