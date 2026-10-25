"""Write src/assets/vesl-labs-mark.svg: the vesl labs logo as inline SVG with one path per glyph, for the build-on.

Same geometry as public/vesl-labs.svg (F:\\VESL\\Assets\\Branding\\Logos\\outline_vesl_labs.py): two 248.8 squares,
type outlined from Geist Mono Regular. Classes: .mark-ground (the black, full width, so no seam), .mark-tile (mint square
and ++), .mark-glyph (each letter of vesl / labs, in writing order via --i).

    python scripts/vesl-labs-mark.py [path/to/GeistMono-Regular.ttf]
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\lindo\FontBase\GeistMono-Regular.ttf"
OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "vesl-labs-mark.svg"

MINT, INK = "#6dffc8", "#000000"
SQ = 248.8
DY = -1.0
RUNS = [("++", 13.75, 179.72, 178.68), ("vesl", 283.02, 108.37, 78.77), ("labs", 283.02, 188.17, 78.77)]

font = TTFont(FONT)
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
upm = font["head"].unitsPerEm


def glyphs(text, x, y, size):
    """One path per character: [(char, d)]."""
    s = size / upm
    out, pen_x = [], 0.0
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + pen_x, y + DY)))
        out.append((ch, pen.getCommands()))
        pen_x += hmtx[g][0] * s
    return out


plus = glyphs(*RUNS[0])
letters = glyphs(*RUNS[1]) + glyphs(*RUNS[2])

lines = [f'<svg class="mark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {2 * SQ:g} {SQ:g}" role="img" aria-label="vesl labs">',
         f'  <rect class="mark-ground" width="{2 * SQ:g}" height="{SQ:g}" fill="{INK}"/>',
         '  <g class="mark-tile">',
         f'    <rect width="{SQ:g}" height="{SQ:g}" fill="{MINT}"/>',
         f'    <path fill="{INK}" d="{" ".join(d for _, d in plus)}"/>',
         '  </g>']
lines += [f'  <path class="mark-glyph" style="--i:{i}" fill="{MINT}" d="{d}"/>' for i, (_, d) in enumerate(letters)]
lines.append("</svg>\n")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(OUT, len(letters), "letters")
