"""Dielines and print-zone drawings for HOLOFOTE, as SVG in real millimetres (platform §C.1, §C.4–§C.9b).

    /home/user/venvs/web/bin/python _build/pack/facas.py

Writes 02_PRODUTO/facas/:
  FACA_COPO-200_zona-impressao.svg   O COPO DO SHOW unrolled (238,8 x 88 mm): print zone 18–82, panels, gaps, seam
  FACA_COPO-080_zona-impressao.svg   O SINGLE unrolled (182,2 x 66 mm): print zone 14–63
  FACA_CARTUCHO_96x96x98.svg         O INGRESSO reverse tuck end, SBS 400 g/m²
  FACA_CARTUCHO_74x74x76.svg         O INGRESSO SINGLE · FACA_CARTUCHO_74x74x82.svg  NOVA TEMPORADA (refil)
  FACA_CASE_base-130x130x102.svg     O CASE base tray wrap (black tolex paper over 2 mm greyboard) + EVA insert
  FACA_CASE_tampa-130x130x30.svg     O CASE lid wrap + the hasp tab with its slot
  FACA_SETLIST_105x400.svg           A SETLIST concertina: folds, ticket perforations, the x = 83 stub perforations
  FACA_PULSEIRA_selo-60x15.svg       the paper seal with its panel map along the strip (TOPO, BAIXO, sides, overlap)
  FACA_ETIQUETA-LOTE_40x12.svg / _32x10.svg the lot stickers
  FACA_TAMPA_90.svg / FACA_TAMPA_70.svg  the lid discs: print area, brim band, gasket footprint, X geometry
Layers (SVG <g id>): CORTE (cut, red), VINCO (crease, blue dashed), PICOTE (perforation, magenta dash-dot),
SANGRIA (3 mm bleed, green), ZONA (print zones, grey), COTA (dimensions and labels, black). Board thickness
allowances are NOT applied: these are flat geometry for art placement; the converter adds caliper and glue lines.
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import Line, run_cap, CAPS

OUT = os.path.dirname(K.out('facas', 'x'))
RED, BLUE, MAG, GREEN, GREY = '#E5004F', '#1A5CFF', '#C000C0', '#00A651', '#9A9A9A'


def f(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.')


# ------------------------------------------------------------------------------------------------- tuck-end carton
def tuck_end(W, D, H, glue=12.0, tongue=None, dust=None):
    """Reverse tuck end. Flat order left to right: glue | front | side 1 (right) | back | side 2 (left).
    Top tuck flap on the BACK panel (folds to the front), bottom tuck flap on the FRONT panel; dust flaps on the sides.
    Returns cut path, crease paths and panel rectangles (x, y, w, h) in mm, y down."""
    dust = dust or round(D * 0.42, 1)
    tongue = tongue or round(min(16.0, D * 0.2), 1)
    Tz = D + tongue                       # closure zone height (top and bottom)
    xg, xf, x1, xb, x2, xe = 0.0, glue, glue + W, glue + W + D, glue + 2 * W + D, glue + 2 * W + 2 * D
    y0, y1 = Tz, Tz + H
    Ht = 2 * Tz + H
    c = []
    # start at the glue flap, go round the outline clockwise
    c.append(f'M{f(xf)},{f(y0)}')
    c.append(f'L{f(xg)},{f(y0 + 5)} L{f(xg)},{f(y1 - 5)} L{f(xf)},{f(y1)}')
    # bottom: front panel carries the bottom tuck flap + tongue
    c += tuck_flap(xf, x1, y1, +1, D, tongue)
    # side 1 bottom dust flap
    c += dust_flap(x1, xb, y1, +1, dust, lead=True)
    # back panel bottom edge: straight
    c.append(f'L{f(x2)},{f(y1)}')
    c += dust_flap(x2, xe, y1, +1, dust, lead=False)
    c.append(f'L{f(xe)},{f(y0)}')
    # top, going back right to left
    c += dust_flap_rev(xe, x2, y0, dust)
    c += tuck_flap_rev(x2, xb, y0, D, tongue)
    c += dust_flap_rev2(xb, x1, y0, dust)
    c.append(f'L{f(xf)},{f(y0)} Z')
    cut = ' '.join(c)
    crease = [f'M{f(x)},{f(y0)} V{f(y1)}' for x in (xf, x1, xb, x2)]
    crease += [f'M{f(xf)},{f(y1)} H{f(x1)}', f'M{f(xb)},{f(y0)} H{f(x2)}',
               f'M{f(x1)},{f(y1)} H{f(xb)}', f'M{f(x2)},{f(y1)} H{f(xe)}',
               f'M{f(x1)},{f(y0)} H{f(xb)}', f'M{f(x2)},{f(y0)} H{f(xe)}',
               f'M{f(xf + 1.5)},{f(y1 + D)} H{f(x1 - 1.5)}', f'M{f(xb + 1.5)},{f(y0 - D)} H{f(x2 - 1.5)}']
    panels = dict(cola=(xg, y0, glue, H), frente=(xf, y0, W, H), lateral1=(x1, y0, D, H), verso=(xb, y0, W, H),
                  lateral2=(x2, y0, D, H), topo=(xb, y0 - D, W, D), fundo=(xf, y1, W, D))
    return dict(cut=cut, crease=crease, panels=panels, w=xe, h=Ht, dims=dict(W=W, D=D, H=H, glue=glue,
                                                                              tongue=tongue, dust=dust))


def tuck_flap(xa, xb_, y, s, D, tongue):
    """flap hanging below (s=+1) from (xa, y) to (xb_, y), drawn left to right."""
    r = min(8.0, tongue * 0.6)
    yb = y + s * D
    yt = yb + s * tongue
    return [f'L{f(xa)},{f(yb)}', f'L{f(xa + 1.5)},{f(yb)}', f'L{f(xa + 1.5)},{f(yt - s * r)}',
            f'Q{f(xa + 1.5)},{f(yt)} {f(xa + 1.5 + r)},{f(yt)}', f'L{f(xb_ - 1.5 - r)},{f(yt)}',
            f'Q{f(xb_ - 1.5)},{f(yt)} {f(xb_ - 1.5)},{f(yt - s * r)}', f'L{f(xb_ - 1.5)},{f(yb)}',
            f'L{f(xb_)},{f(yb)}', f'L{f(xb_)},{f(y)}']


def tuck_flap_rev(xa, xb_, y, D, tongue):
    """top flap above y, drawn right (xa) to left (xb_)."""
    r = min(8.0, tongue * 0.6)
    yb = y - D
    yt = yb - tongue
    return [f'L{f(xa)},{f(yb)}', f'L{f(xa - 1.5)},{f(yb)}', f'L{f(xa - 1.5)},{f(yt + r)}',
            f'Q{f(xa - 1.5)},{f(yt)} {f(xa - 1.5 - r)},{f(yt)}', f'L{f(xb_ + 1.5 + r)},{f(yt)}',
            f'Q{f(xb_ + 1.5)},{f(yt)} {f(xb_ + 1.5)},{f(yt + r)}', f'L{f(xb_ + 1.5)},{f(yb)}',
            f'L{f(xb_)},{f(yb)}', f'L{f(xb_)},{f(y)}']


def dust_flap(xa, xb_, y, s, dust, lead):
    """bottom dust flap (below y), left to right; the slope sits on the side away from the tuck flap's hinge."""
    if lead:
        return [f'L{f(xa + 2)},{f(y + dust)}', f'L{f(xb_ - 14)},{f(y + dust)}', f'L{f(xb_)},{f(y + 6)}',
                f'L{f(xb_)},{f(y)}']
    return [f'L{f(xa)},{f(y + 6)}', f'L{f(xa + 14)},{f(y + dust)}', f'L{f(xb_ - 2)},{f(y + dust)}',
            f'L{f(xb_)},{f(y)}']


def dust_flap_rev(xa, xb_, y, dust):
    """top dust flap of side 2 (rightmost), right to left."""
    return [f'L{f(xa - 2)},{f(y - dust)}', f'L{f(xb_ + 14)},{f(y - dust)}', f'L{f(xb_)},{f(y - 6)}',
            f'L{f(xb_)},{f(y)}']


def dust_flap_rev2(xa, xb_, y, dust):
    """top dust flap of side 1, right to left."""
    return [f'L{f(xa)},{f(y - 6)}', f'L{f(xa - 14)},{f(y - dust)}', f'L{f(xb_ + 2)},{f(y - dust)}',
            f'L{f(xb_)},{f(y)}']


# ------------------------------------------------------------------------------------------------- SVG writer
class Sheet:
    def __init__(self, w, h, margin=12.0, top=None):
        self.w, self.h, self.m = w, h, margin
        self.top = margin if top is None else top
        self.g = {k: [] for k in ('SANGRIA', 'ZONA', 'CORTE', 'VINCO', 'PICOTE', 'COTA')}

    def path(self, layer, d):
        self.g[layer].append(f'<path d="{d}"/>')

    def raw(self, layer, s):
        self.g[layer].append(s)

    def text(self, x, y, s, size=2.6, anchor='start', fill='#000'):
        """labels are set as outlines (Condensed One), so the file never depends on an installed font."""
        ln = Line([run_cap(s, K.CN, size, 40, CAPS)])
        if anchor == 'middle':
            p = K.place_center(ln, x, y)
        elif anchor == 'end':
            p = K.place_right(ln, x, y)
        else:
            p = K.place_left(ln, x, y)
        self.g['COTA'].append(f'<path d="{K.placed_paths(p)}" fill="{fill}"/>')

    def svg(self, title):
        m, mt = self.m, self.top
        W, H = self.w + 2 * m, self.h + mt + m + 10
        style = dict(SANGRIA=f'fill="none" stroke="{GREEN}" stroke-width="0.25" stroke-dasharray="1 1"',
                     ZONA=f'fill="none" stroke="{GREY}" stroke-width="0.2"',
                     CORTE=f'fill="none" stroke="{RED}" stroke-width="0.3"',
                     VINCO=f'fill="none" stroke="{BLUE}" stroke-width="0.3" stroke-dasharray="3 1.5"',
                     PICOTE=f'fill="none" stroke="{MAG}" stroke-width="0.3" stroke-dasharray="1.2 0.8"',
                     COTA='')
        body = ''.join(f'<g id="{k}" {style[k]}>{"".join(v)}</g>' for k, v in self.g.items() if v)
        head = Line([run_cap(title, K.CN, 3.4, 60, CAPS)])
        hp = K.place_left(head, 0, -4.0)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(W)}mm" height="{f(H)}mm" '
                f'viewBox="{f(-m)} {f(-mt - 10)} {f(W)} {f(H)}"><rect x="{f(-m)}" y="{f(-mt - 10)}" width="{f(W)}" '
                f'height="{f(H)}" fill="#fff"/><path d="{K.placed_paths(hp)}" fill="#000"/>{body}</svg>')

    def save(self, name, title):
        p = os.path.join(OUT, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(self.svg(title))
        return p


def rect(x, y, w, h):
    return f'M{f(x)},{f(y)} h{f(w)} v{f(h)} h{f(-w)} Z'


def circle(cx, cy, r):
    return K.circle_d(cx, cy, r)


# ------------------------------------------------------------------------------------------------- pieces
def copo(size):
    if size == '200':
        C, Hg, z0, z1, meas, coat_top, tag = 238.8, 88.0, 18.0, 82.0, 72.0, 87.0, 'COPO-200'
        title = 'O COPO DO SHOW · zona de impressão desenrolada · Ø76 × 88 mm · circunferência 238,8 mm'
    else:
        C, Hg, z0, z1, meas, coat_top, tag = 182.2, 66.0, 14.0, 63.0, 54.0, 65.0, 'COPO-080'
        title = 'O SINGLE · zona de impressão desenrolada · Ø58 × 66 mm · circunferência 182,2 mm'
    S = Sheet(C, Hg, margin=36.0)

    def Y(z):
        return Hg - z
    S.path('CORTE', rect(0, 0, C, Hg))                       # the unrolled glass (not a cut: the vessel outline)
    S.path('ZONA', rect(0, Y(coat_top), C, coat_top))        # coating, stops 1 mm under the rim
    S.path('ZONA', rect(0, Y(z1), C, z1 - z0))               # print zone
    for cx, nm in ((C * 0.25, 'FRENTE'), (C * 0.75, 'VERSO')):
        S.path('VINCO', rect(cx - meas / 2, Y(z1), meas, z1 - z0))
        S.path('ZONA', f'M{f(cx)},{f(Y(z1) - 2)} V{f(Y(z0) + 2)}')
        S.text(cx, Y(z1) - 1.5, f'{nm} · {meas:.1f} mm'.replace('.', ','), 2.4, 'middle')
    gap = (C - 2 * meas) / 2
    zm = Y((z0 + z1) / 2)
    S.text(gap / 4, zm, 'x = 0', 2.0, 'middle')
    S.text(gap / 4, zm + 3.4, 'emenda', 2.0, 'middle')
    S.text(C / 2, zm, f'lacuna lateral {gap:.1f} mm'.replace('.', ','), 2.0, 'middle')
    S.text(C / 2, zm + 3.4, 'sem tinta', 2.0, 'middle')
    S.text(C - gap / 4, zm, f'x = {C:.1f}'.replace('.', ','), 2.0, 'middle')
    S.text(C - gap / 4, zm + 3.4, '(= x 0)', 2.0, 'middle')
    S.text(C + 1, Y(z1) + 1.0, f'{z1:.1f} mm'.replace('.', ','), 2.0)
    S.text(C + 1, Y(z0) + 1.0, f'{z0:.1f} mm'.replace('.', ','), 2.0)
    S.text(-1.5, Y(coat_top) + 1.0, f'revestimento até {coat_top:.1f}'.replace('.', ','), 2.0, 'end')
    S.text(C / 2, Hg + 6, f'base 0 mm · faixa lisa 0–{z0:.0f} mm (plinto) · borda de vidro livre de 1,0 mm', 2.2,
           'middle')
    px = int(round(C * 40))
    S.text(C / 2, Hg + 10.5, f'mestre do rótulo: {px} × {int(round((z1 - z0) * 40))} px a 40 px/mm · y = ({z1:.1f} − b) × 40'
           .replace('.', ','), 2.2, 'middle')
    return S.save(f'FACA_{tag}_zona-impressao.svg', title)


def cartucho(W=96.0, D=96.0, H=98.0, title='O INGRESSO', relabel=None):
    net = tuck_end(W, D, H)
    S = Sheet(net['w'], net['h'])
    S.raw('SANGRIA', f'<path d="{net["cut"]}" stroke-width="6.25" stroke-opacity="0.25" stroke-dasharray="none"/>')
    S.path('CORTE', net['cut'])
    for c in net['crease']:
        S.path('VINCO', c)
    labels = dict(cola='COLA', frente='FRENTE (painel principal)', lateral1='LATERAL 1 · MODO DE USO', verso='VERSO · '
                  'MANIFESTO', lateral2='LATERAL 2 · holofote nela.', topo='TOPO (aba de fechamento)',
                  fundo='FUNDO (aba de fechamento)')
    labels.update(relabel or {})
    for k, (x, y, w, h) in net['panels'].items():
        if k == 'cola':
            continue
        S.text(x + w / 2, y + h / 2, labels[k], 2.6, 'middle', GREY)
    S.text(net['w'] / 2, net['h'] + 7.5, f'{title} · {W:.0f} × {D:.0f} × {H:.0f} mm · cartucho de fundo e topo invertidos '
           f'(RTE) · SBS 400 g/m² · espessura do cartão NÃO compensada', 2.4, 'middle')
    return S.save(f'FACA_CARTUCHO_{W:.0f}x{D:.0f}x{H:.0f}.svg', f'{title} · faca planificada')


def wrap_box(W, D, Hh, turn=15.0):
    """Cross-shaped wrap for a rigid set-up box: the face (W x D), four walls (height Hh) and a turn-in over the rim,
    with corner ears on the long walls."""
    ear = 12.0
    x0, y0 = turn + Hh, turn + Hh
    paths = []
    paths.append(f'M{f(x0)},{f(0)} H{f(x0 + W)} V{f(turn)} H{f(x0 + W + ear)} V{f(y0)} '
                 f'H{f(x0 + W + Hh)} V{f(y0 - ear)} H{f(x0 + W + Hh + turn)} V{f(y0 + D + ear)} '
                 f'H{f(x0 + W + Hh)} V{f(y0 + D)} H{f(x0 + W + ear)} V{f(y0 + D + Hh)} H{f(x0 + W)} '
                 f'V{f(y0 + D + Hh + turn)} H{f(x0)} V{f(y0 + D + Hh)} H{f(x0 - ear)} V{f(y0 + D)} '
                 f'H{f(x0 - Hh)} V{f(y0 + D + ear)} H{f(0)} V{f(y0 - ear)} H{f(x0 - Hh)} V{f(y0)} '
                 f'H{f(x0 - ear)} V{f(turn)} H{f(x0)} Z')
    crease = [rect(x0, y0, W, D), f'M{f(x0)},{f(turn)} H{f(x0 + W)}', f'M{f(x0)},{f(y0 + D + Hh)} H{f(x0 + W)}',
              f'M{f(turn)},{f(y0)} V{f(y0 + D)}', f'M{f(x0 + W + Hh)},{f(y0)} V{f(y0 + D)}']
    total = 2 * (turn + Hh) + W
    return paths, crease, (x0, y0), total


def case(which):
    if which == 'base':
        W, D, Hh, tag, title = 130.0, 130.0, 102.0, 'base-130x130x102', 'O CASE · bandeja base · forro tolex 120 g/m² sobre papelão cinza 2 mm'
    else:
        W, D, Hh, tag, title = 130.0, 130.0, 30.0, 'tampa-130x130x30', 'O CASE · tampa · forro tolex 120 g/m² sobre papelão cinza 2 mm'
    paths, crease, (x0, y0), total = wrap_box(W, D, Hh)
    extra = 0 if which == 'base' else 70.0
    S = Sheet(total + extra, total)
    for p in paths:
        S.path('CORTE', p)
        S.raw('SANGRIA', f'<path d="{p}" stroke-width="6.25" stroke-opacity="0.25" stroke-dasharray="none"/>')
    for c in crease:
        S.path('VINCO', c)
    lab = 'FUNDO (face de baixo)' if which == 'base' else 'TOPO DA TAMPA'
    S.text(x0 + W / 2, y0 + D / 2, lab, 3.0, 'middle', GREY)
    S.text(x0 + W / 2, y0 + D + Hh / 2, 'FRENTE', 3.0, 'middle', GREY)
    S.text(x0 + W / 2, y0 - Hh / 2, 'TRÁS (dobradiça)', 3.0, 'middle', GREY)
    S.text(x0 - Hh / 2, y0 + D / 2, 'ESQ.', 3.0, 'middle', GREY)
    S.text(x0 + W + Hh / 2, y0 + D / 2, 'DIR.', 3.0, 'middle', GREY)
    if which == 'base':
        # slot in the base front, behind the hasp
        sx = x0 + (W - 52.0) / 2 + 5.0
        sy = y0 + D + Hh - 8.0           # 8 mm below the base front's top edge (the wall is flipped in the net)
        S.path('CORTE', K.rrect_d(sx, sy - 1.5, 16.0, 3.0, 1.5))
        # EVA insert beside the net
        ex, ey = total + 20.0, 0.0
        S.w = total + 160.0
        S.path('CORTE', rect(ex, ey, 126.0, 126.0))
        S.path('CORTE', circle(ex + 63.0, ey + 63.0 + 4.0, 46.0))
        S.path('CORTE', rect(ex + 10.0, ey + 5.0, 106.0, 3.0))
        S.text(ex + 63.0, ey + 135.0, 'INSERTO EVA 126 × 126 · furo Ø92 × 86 · fenda do setlist 106 × 3', 2.4, 'middle')
    else:
        # the hasp tab: 52 x 16, R3, hangs from the lid front's lower edge; slot 16 x 3 at 8 mm
        tx, ty = total + 10.0, 10.0
        d = (f'M{f(tx)},{f(ty)} H{f(tx + 52)} V{f(ty + 13)} A3,3 0 0 1 {f(tx + 49)},{f(ty + 16)} H{f(tx + 3)} '
             f'A3,3 0 0 1 {f(tx)},{f(ty + 13)} Z')
        S.path('CORTE', d)
        S.path('VINCO', f'M{f(tx)},{f(ty)} H{f(tx + 52)}')
        S.path('CORTE', K.rrect_d(tx + 5.0, ty + 6.5, 16.0, 3.0, 1.5))
        S.text(tx + 26, ty + 24, 'ABA DO FECHO 52 × 16 · fenda 16 × 3', 2.2, 'middle')
    S.text(total / 2, total + 6, f'{title} · dobra de 15 mm para dentro · orelhas de canto 12 mm', 2.2, 'middle')
    return S.save(f'FACA_CASE_{tag}.svg', 'O CASE · ' + tag)


def setlist():
    S = Sheet(105.0, 400.0)
    S.path('CORTE', rect(0, 0, 105, 400))
    S.raw('SANGRIA', f'<path d="{rect(-3, -3, 111, 406)}"/>')
    for y in (100, 200, 300):
        S.path('VINCO', f'M0,{y} H105')
    for y in (325, 350, 375):
        S.path('PICOTE', f'M0,{y} H105')
    S.path('PICOTE', 'M83,300 V400')
    for i, nm in enumerate(['P1 · capa', 'P2 · setlist', 'P3 · setlist', 'P4 · BIS · 4 ingressos']):
        S.text(52.5, i * 100 + 52, nm, 3.0, 'middle', GREY)
    S.text(52.5, 407, 'A SETLIST · sanfona 105 × 400 · 4 painéis 105 × 100 · 300 g/m² · picote em x = 83 (canhoto 22 mm)',
           2.2, 'middle')
    return S.save('FACA_SETLIST_105x400.svg', 'A SETLIST · faca')


def seal_and_stickers():
    import pulseira as PU
    S = Sheet(60.0, 15.0, 26.0, top=6.0)
    S.path('CORTE', rect(0, 0, 60, 15))
    S.raw('SANGRIA', f'<path d="{rect(-3, -3, 66, 21)}"/>')
    a0, a1 = PU.AMARELO_S
    S.raw('ZONA', f'<path d="{rect(a0, 0, a1 - a0, 15)}" fill="{K.T.C["amarelo"]}" fill-opacity="0.35"/>')
    marks = sorted({v for s0, s1, *_ in PU.SEAL_PANELS for v in (s0, s1)})
    prev, low = None, False
    for v in marks:
        if 0 < v < 60:
            S.path('VINCO', f'M{f(v)},0 V15')
        low = (not low) if prev is not None and v - prev < 4.0 else False   # stagger crowded marks
        S.raw('COTA', f'<path d="M{f(v)},15.4 V{f(18.6 if not low else 20.8)}" fill="none" stroke="{GREY}" '
                      f'stroke-width="0.15"/>')
        S.text(v, 20.6 if not low else 22.8, f'{v:g}'.replace('.', ','), 1.5, 'middle', GREY)
        prev = v
    for s0, s1, name, where, vis in PU.SEAL_PANELS:
        if name in ('TOPO', 'BAIXO'):
            S.text((s0 + s1) / 2, 8.6, name, 2.4, 'middle')
    S.text(15.0, 8.4, 'colagem', 1.8, 'middle', GREY)
    S.text(15.0, 10.8, '(fica sob o BAIXO)', 1.4, 'middle', GREY)
    notes = ['SELO DE PAPEL 60 × 15 mm · impresso só por fora · vincos a cada mudança de face',
             'enrola no maço pulseira + ponta (≈16 × 2,5 mm) · volta de 37 mm + sobreposição de 23 mm por baixo',
             'TOPO 25,5–41,5: \u201cpode / rasgar.\u201d · BAIXO 44–60: \u201co que se guarda é a pulseira.\u201d',
             'amarelo de 23 a 44 (laterais + topo) · papel no BAIXO e na colagem (0–23)']
    for k, t in enumerate(notes):
        S.text(30, 28.0 + 3.0 * k, t, 1.7, 'middle')
    S.save('FACA_PULSEIRA_selo-60x15.svg', 'A PULSEIRA · selo de papel')
    for w, h in ((40.0, 12.0), (32.0, 10.0)):
        S = Sheet(w, h, 8.0)
        S.path('CORTE', K.rrect_d(0, 0, w, h, 1.0))
        S.text(w / 2, h + 6, f'etiqueta de lote · PP transparente fosco · {w:.0f} × {h:.0f} · cantos R1', 2.0, 'middle')
        S.save(f'FACA_ETIQUETA-LOTE_{w:.0f}x{h:.0f}.svg', 'ETIQUETA DE LOTE')


def tampa(Dm, gasket_o, glass_r, strip, tag):
    R_ = Dm / 2
    S = Sheet(Dm, Dm)
    S.path('CORTE', circle(R_, R_, R_))
    S.path('ZONA', circle(R_, R_, R_ - 0.6))
    S.path('ZONA', circle(R_, R_, glass_r))
    S.path('VINCO', circle(R_, R_, gasket_o / 2))
    L, Wd = strip
    for ang in (45, -45):
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        vx, vy = -uy, ux
        pts = [(R_ + sx * L / 2 * ux + sv * Wd / 2 * vx, R_ + sx * L / 2 * uy + sv * Wd / 2 * vy)
               for sx, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        S.path('ZONA', 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + ' Z')
    S.text(R_, Dm + 6, f'A TAMPA-PALCO Ø{Dm:.0f} · UV · área útil até R{R_ - 0.6:.1f} · aba de R{glass_r:.0f} a '
           f'R{R_ - 0.6:.1f} · fitas {Wd:.0f} × {L:.0f} a ±45° (nominal)'.replace('.', ','), 2.0, 'middle')
    S.save(f'FACA_TAMPA_{tag}.svg', f'A TAMPA-PALCO Ø{Dm:.0f}')


def main():
    copo('200')
    copo('080')
    cartucho()
    cartucho(74.0, 74.0, 76.0, 'O INGRESSO SINGLE')
    cartucho(74.0, 74.0, 82.0, 'NOVA TEMPORADA (refil)',
             dict(lateral1='LATERAL 1 · MODO DE USO', lateral2='LATERAL 2 · ADVERTÊNCIAS',
                  topo='TOPO · ESTE LADO PRA CIMA', fundo='FUNDO · código + descarte'))
    case('base')
    case('tampa')
    setlist()
    seal_and_stickers()
    tampa(90.0, 76.0, 38.0, (78.0, 18.0), '90')
    tampa(70.0, 58.0, 29.0, (60.0, 14.0), '70')
    print('facas written to', OUT)


if __name__ == '__main__':
    main()
