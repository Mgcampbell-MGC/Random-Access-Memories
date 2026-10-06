"""HOLOFOTE wordmark and O FOCO symbol as exact SVG outlines (platform §D.3).

Wordmark: Special Gothic Expanded One caps, tracking -10/1000 em, shaped with HarfBuzz (kerning on).
The THIRD O (the O of "FO") is the lit lamp: its outer contour filled solid, counter removed.
Outputs SVG + PNG in every colourway into 01_MARCA/logo/.
"""
import os, sys, subprocess
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
FONT = os.path.join(HERE, 'fonts', 'SpecialGothicExpandedOne-Regular.ttf')
OUT = os.path.join(KIT, '01_MARCA', 'logo')
os.makedirs(OUT, exist_ok=True)
C = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A', rosa='#FF4FA0', laranja='#FF6A1A', violeta='#8424F5')

tt = TTFont(FONT)
gs = tt.getGlyphSet()
UPM = tt['head'].unitsPerEm
CAP = tt['OS/2'].sCapHeight


def shape(text, tracking=-10):
    blob = hb.Blob.from_file_path(FONT)
    face = hb.Face(blob)
    font = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': False})
    x = 0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = tt.getGlyphName(info.codepoint)
        out.append((name, x + pos.x_offset, pos.y_offset))
        x += pos.x_advance + tracking
    return out, x - tracking


def contours(name, dx, dy):
    """Return list of SVG path strings, one per contour, in font units with y flipped (y down)."""
    rec = RecordingPen()
    gs[name].draw(rec)
    paths, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op in ('closePath', 'endPath'):
            paths.append(cur)
            cur = []
    res = []
    for p in paths:
        sp = SVGPathPen(gs)
        tp = TransformPen(sp, (1, 0, 0, -1, dx, CAP - dy))
        for op, args in p:
            getattr(tp, op)(*args)
        bp = BoundsPen(gs)
        for op, args in p:
            getattr(bp, op)(*args)
        res.append((sp.getCommands(), bp.bounds))
    return res


def wordmark_paths():
    glyphs, width = shape('HOLOFOTE')
    letters, lit = [], None
    o_count = 0
    for name, x, y in glyphs:
        cs = contours(name, x, y)
        if name == 'O':
            o_count += 1
            if o_count == 3:
                # outer contour = the one with the largest bbox
                outer = max(cs, key=lambda c: (c[1][2] - c[1][0]) * (c[1][3] - c[1][1]))
                lit = outer[0]
                continue
        letters.append(' '.join(c[0] for c in cs))
    return letters, lit, width


def svg_wordmark(ink, lamp, bg=None, pad=None):
    letters, lit, width = wordmark_paths()
    o_h = CAP  # clear space = O height on every side
    pad = o_h if pad is None else pad
    W, H = width + 2 * pad, CAP + 2 * pad
    rect = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ''
    body = ''.join(f'<path d="{d}" fill="{ink}" fill-rule="nonzero"/>' for d in letters)
    body += f'<path d="{lit}" fill="{lamp}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{rect}'
            f'<g transform="translate({pad},{pad})">{body}</g></svg>'), W, H


def svg_foco(color, bg=None):
    """O FOCO: the lit disc (d) over a flat floor ellipse (2.4d x 0.8d), gap 0.5d."""
    d = 400
    W = 2.4 * d + 2 * 0.25 * d
    H = d + 0.5 * d + 0.8 * d + 2 * 0.25 * d
    cx = W / 2
    top = 0.25 * d
    rect = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{rect}'
            f'<circle cx="{cx}" cy="{top + d / 2}" r="{d / 2}" fill="{color}"/>'
            f'<ellipse cx="{cx}" cy="{top + d + 0.5 * d + 0.4 * d}" rx="{1.2 * d}" ry="{0.4 * d}" fill="{color}"/></svg>')


def main():
    ways = {
        'HOLOFOTE_logo_preto-sobre-papel': (C['preto'], C['amarelo'], C['papel']),
        'HOLOFOTE_logo_papel-sobre-preto': (C['papel'], C['amarelo'], C['preto']),
        'HOLOFOTE_logo_preto-sobre-amarelo': (C['preto'], C['preto'], C['amarelo']),
        'HOLOFOTE_logo_preto-sobre-rosa': (C['preto'], C['amarelo'], C['rosa']),
        'HOLOFOTE_logo_preto-sobre-laranja': (C['preto'], C['preto'], C['laranja']),   # §D.1: amarelo never touches laranja
        'HOLOFOTE_logo_papel-sobre-violeta': (C['papel'], C['amarelo'], C['violeta']),
        'HOLOFOTE_logo_mono-preto_transparente': (C['preto'], C['preto'], None),
        'HOLOFOTE_logo_papel_transparente': (C['papel'], C['amarelo'], None),
        'HOLOFOTE_logo_preto_transparente': (C['preto'], C['amarelo'], None),
    }
    for name, (ink, lamp, bg) in ways.items():
        svg, W, H = svg_wordmark(ink, lamp, bg)
        p = os.path.join(OUT, name + '.svg')
        open(p, 'w').write(svg)
    for name, col, bg in [('O_FOCO_amarelo-sobre-preto', C['amarelo'], C['preto']), ('O_FOCO_preto', C['preto'], None),
                          ('O_FOCO_amarelo', C['amarelo'], None)]:
        open(os.path.join(OUT, name + '.svg'), 'w').write(svg_foco(col, bg))
    letters, lit, width = wordmark_paths()
    print('wordmark width/cap =', round(width / CAP, 3), '(platform says 9,273)')


if __name__ == '__main__':
    main()
