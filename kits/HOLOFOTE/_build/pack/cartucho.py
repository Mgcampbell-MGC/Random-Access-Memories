"""The retail cartons of HOLOFOTE (platform §C.9, §C.9b), one parametrised generator for all three:

  INGRESSO  O INGRESSO, HLF-01…04-200, 96 x 96 x 98 mm
  SINGLE    O INGRESSO SINGLE, HLF-02-080, 74 x 74 x 76 mm (O SINGLE · PESO LÍQUIDO 80 g · aprox. 16 h)
  REFIL     NOVA TEMPORADA, HLF-REF-01…04, 74 x 74 x 82 mm

    /home/user/venvs/web/bin/python _build/pack/cartucho.py [--only HLF-02-080]

All are reverse-tuck-end cartons in SBS 400 g/m² with two inks: preto + the faixa colour (on ACÚSTICO the type knocks
out to the board, never preto on violeta). Panels at 20 px/mm in reading orientation:
  frente · lateral-1 (right) · verso · lateral-2 (left) · topo (ESTE LADO PRA CIMA ↑) · fundo

INGRESSO / SINGLE front: a giant ticket that repeats the copo's own lineup scaled to the carton's measure (MÃE over the
SKU's show name), so the carton and the glass inside always agree; the hero prints exactly MÃE AO VIVO / HOLOFOTE AO
VIVO. lateral-1 MODO DE USO + ADVERTÊNCIAS (cap 1,7), verso MANIFESTO ("ver lateral"), lateral-2 holofote nela. + the
"não precisava" line + bar block + disposal. The SINGLE's MANIFESTO takes the 80 g line.
REFIL front: NOVA TEMPORADA · faixa name · O copo fica. A turnê continua. · PESO LÍQUIDO 200 g; lateral-1 MODO DE USO,
lateral-2 ADVERTÊNCIAS, verso MANIFESTO (verbatim); the bar block and the disposal symbols go to the fundo.

Outputs in 02_PRODUTO/cartucho/ per SKU: <SKU>_CARTUCHO_<painel>.png/.svg, _ATLAS.png (4 x 3, candle_lib.box()
layout), _planificado.png (flat print sheet at 10 px/mm, 3 mm bleed, art in place, top flap turned 180°),
_planificado_preview.jpg (die lines over it) and _cartucho.json. The die lines themselves are written by facas.py.
"""
import os
import sys
import argparse

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, Placed, run_cap, run_xh, CAPS, FIG
import facas
from tipos import clear_accents, Glyph, glyph_path

PP = 20
ATLAS_PP = 16

# §C.9 / §C.9b strings that only the SINGLE and the refill carton use (exact)
SINGLE_NAME = 'HOLOFOTE AO VIVO · O SINGLE'        # §B.2 "Name (PT, as printed)"
SINGLE_NET = '80 g'
SINGLE_BURN = 'aprox. 16 h'
REF_LINE = ['O copo fica.', 'A turnê continua.']   # §A.8 line 17, one sentence per line
REF_TITLE = 'NOVA TEMPORADA'


class G:
    """Carton geometry: W (front width), D (depth), H (height), the type measure and the copo-poster scale."""

    def __init__(self, W, D, H, mar):
        self.W, self.D, self.H, self.MAR = W, D, H, mar
        self.X0, self.X1 = mar, W - mar
        self.MEAS = self.X1 - self.X0
        self.KS = self.MEAS / 72.0


KINDS = {
    'INGRESSO': dict(geo=G(96.0, 96.0, 98.0, 6.0), faixas=['01', '02', '03', '04'],
                     code=lambda f: f'HLF-{f}-200', net='200 g'),
    'SINGLE': dict(geo=G(74.0, 74.0, 76.0, 5.0), faixas=['02'], code=lambda f: 'HLF-02-080', net=SINGLE_NET),
    'REFIL': dict(geo=G(74.0, 74.0, 82.0, 5.0), faixas=['01', '02', '03', '04'], code=lambda f: f'HLF-REF-{f}',
                  net='200 g'),
}


class Panel:
    def __init__(self, g, name, w, h, flood, ink):
        self.g, self.name, self.w, self.h, self.flood, self.ink = g, name, w, h, flood, ink
        self.paths, self.log, self.dev = [], [], []

    def add(self, p, label, **meta):
        b = p.ink() if p.matrix is None and p.per_glyph is None else K.placed_ink_poly(p)
        m = self.g.MAR
        assert b[0] >= m - 0.6 and b[2] <= self.w - m + 0.6 and b[1] >= 2.0 and b[3] <= self.h - 2.0, \
            (self.name, label, b)
        self.paths.append(K.placed_paths(p))
        self.log.append(dict(label=label, ink_mm=[round(v, 2) for v in b],
                             text=''.join(r.text for r in p.line.runs), **meta))
        return p

    def raw(self, d):
        self.paths.append(d)


def colours(faixa):
    s = T.SKUS[faixa]
    flood = T.C[s['coating']]
    ink = T.C['papel'] if s['coating'] == 'violeta' else T.C['preto']
    return flood, ink


def split(P, lruns, rruns, y, label):
    g = P.g
    pl = K.place_left(Line(lruns), g.X0, y)
    pr = K.place_right(Line(rruns), g.X1, y)
    P.add(pl, label + ' L')
    P.add(pr, label + ' R')
    assert pr.ink()[0] - pl.ink()[2] > 3.0, label
    return pl, pr


REF_LOT = ('LOTE: ver base do copo', 'LOTE: marcado na cápsula')     # director's correction for the refill cartons

# director's decisions after the copy/compliance review, 6 Oct 2026 (recorded in every JSON they touch)
DD = T.DD
REF_MODO_FIRST = 'Retire o selo antes de usar. Encaixe a cápsula no copo HOLOFOTE limpo e frio.'
REF_MODO_USE = ('Use a cápsula sempre dentro do copo HOLOFOTE. Apoie o copo sobre a tampa virada ou sobre superfície '
                'plana, firme e resistente ao calor.')
REF_LAST = ('Modo de uso e advertências completas: ver lateral.', 'Modo de uso e advertências completas: ver laterais.')
SINGLE_CONTENT = 'CONTEÚDO: HOLOFOTE AO VIVO · O SINGLE — vela aromática · ODORIZANTE DE AMBIENTE'
BURN_200 = 'queima aprox. 40 h'                    # §B: 200 g ≈ 40 h (the setlist already states it)
WORDMARK_W = 30.0                                  # refill front wordmark, ink width (§D.3 minimum 18 mm)


def wordmark_mono(P, x0, baseline, ink_w=WORDMARK_W):
    """HOLOFOTE wordmark: the logo team's mono SVG (01_MARCA/logo, the lit O as a solid disc) in the carton's one
    type ink (§D.3 'Mono'; on amarelo it is the §D.3 colourway itself), ink width ink_w. Returns (ink box, cap)."""
    d, cap, box = K.logo_d(x0, baseline, ink_w)
    P.raw(d)
    P.log.append(dict(label='wordmark HOLOFOTE (logo SVG, mono)', ink_mm=[round(v, 2) for v in box],
                      cap_mm=round(cap, 3), source='01_MARCA/logo/HOLOFOTE_logo_mono-preto_transparente.svg'))
    return box, cap


def manifesto(faixa, net, refil=False, single=False):
    """The carton MANIFESTO lines, with every decision applied; returns (lines, deviation records)."""
    lines = T.manifesto(faixa, ver='carton')
    lines = [('PESO LÍQUIDO ' + net) if t == 'PESO LÍQUIDO 200 g' else t for t in lines]
    dev = [dict(panel='verso', **T.ALERG_FIX), dict(panel='verso', **T.INGREDIENT_BREAK)]

    def swap(old_prefix, new, why, whole=False):
        hits = [i for i, t in enumerate(lines) if t.startswith(old_prefix)]
        assert len(hits) == 1, (old_prefix, hits)
        i = hits[0]
        was = lines[i]
        lines[i] = new if whole else new + was[len(old_prefix):]
        dev.append(dict(panel='verso', kind=DD, platform=was, used=lines[i], reason=why))
    if refil:
        swap(REF_LOT[0], REF_LOT[1], "a refill's lot is laser-marked on the capsule band (director, as platform "
             "owner, 6 Oct 2026); the rest of the MANIFESTO is verbatim")
        show = T.SKUS[faixa]['show']
        swap('CONTEÚDO:', f'CONTEÚDO: HOLOFOTE {show} — vela aromática · refil · ODORIZANTE DE AMBIENTE',
             'the contents line names the refill', whole=True)
        swap(REF_LAST[0], REF_LAST[1], 'the refill carries MODO DE USO and ADVERTÊNCIAS on two sides', whole=True)
    if single:
        swap('CONTEÚDO:', SINGLE_CONTENT, 'the contents line names O SINGLE (the string as given by the director)',
             whole=True)
    return lines, dev


# ------------------------------------------------------------------------------------------------- fronts
def front_ticket(g, faixa, single=False):
    s = T.SKUS[faixa]
    flood, ink = colours(faixa)
    P = Panel(g, 'frente', g.W, g.H, flood, ink)
    KS = g.KS
    sc = g.W / 96.0                             # absolute spacings scale with the carton (INGRESSO = 1)
    cap1 = 2.6 * KS
    y = 7.0 * sc + cap1
    name = SINGLE_NAME if single else 'HOLOFOTE ' + s['show']
    split(P, [run_cap(T.CT_FRONT['ingresso'], K.CN, cap1, 100, CAPS)], [run_cap(name, K.CN, cap1, 80, CAPS)], y, 'L1')
    capm = 17.8 * KS
    ln, tr = K.fit_tracking([run_cap('MÃE', K.XP, capm, 0, CAPS)], g.MEAS, lo=-10, hi=200)
    y += 3.2 * sc + 0.315 * capm + capm
    p2 = P.add(K.place_left(ln, g.X0, y), 'MÃE', cap_mm=round(capm, 3), tracking=round(tr, 2))
    caps3 = 10.0 * KS
    ln, tr3 = K.fit_tracking([run_cap(s['show'], K.SG(700, s['wdth']), caps3, 0, CAPS)], g.MEAS)
    y += 2.4 * KS + caps3                       # the copo L2/L3 gap (2,4 mm), scaled
    p3 = K.place_left(ln, g.X0, y)
    obst = [(p2.x + b[0], p2.x + b[2], p2.y + b[3]) for b in (q.bounds() for q in p2.line.glyphs) if b]
    fix = clear_accents(p3, obst)
    P.add(p3, 'show', cap_mm=round(caps3, 3), wdth=s['wdth'], tracking=round(tr3, 2), accent_fix=fix or None)
    y += 4.0 * sc + 4.0 * KS
    # the date line keeps the copo's proportion unless it would crowd SETOR on a small carton: then its cap steps
    # down (never under 3,0 mm) until the L/R gap is at least 3,2 mm
    capd = 4.0 * KS
    wr = Line([run_cap(T.CT_FRONT['setor'], K.CN, cap1, 80, CAPS)]).ink_width()
    while capd > 3.0 and Line([run_cap(T.CT_FRONT['date'], K.CN, capd, 80, CAPS)]).ink_width() + wr + 3.2 > g.MEAS:
        capd -= 0.05
    if abs(capd - 4.0 * KS) > 1e-6:
        P.dev.append(dict(panel='frente', reason=f'L4 date cap {capd:.2f} mm instead of {4.0 * KS:.2f} (the copo '
                          f'proportion) so DOMINGO · 09.05 clears SETOR: PRIMEIRA FILA by 3,2 mm on the {g.W:.0f} mm front'))
    split(P, [run_cap(T.CT_FRONT['date'], K.CN, capd, 80, CAPS)],
          [run_cap(T.CT_FRONT['setor'], K.CN, cap1, 80, CAPS)], y, 'L4')
    y += 2.6 * sc
    P.raw(K.rect_d(g.X0, y - 0.15, g.MEAS, 0.3))
    y += 2.6 * sc + 4.0
    right5 = [run_cap(T.L6_RIGHT_CAPS, K.CN, cap1, 80, CAPS), run_cap(SINGLE_NET if single else T.L6_RIGHT_FIG,
                                                                     K.CN, 4.0, 0, FIG)]
    left = T.L6_LEFT + (' · ' + SINGLE_BURN if single else '')
    if not single:
        # optional (director, 6 Oct 2026): the 200 g burn time beside PESO LÍQUIDO, only if it fits with nothing moved
        cand = T.L6_LEFT + ' · ' + BURN_200
        gap = g.MEAS - Line([run_cap(cand, K.CN, cap1, 0, FIG)]).ink_width() - Line(right5).ink_width()
        if gap >= 6.0:
            left = cand
            P.dev.append(dict(panel='frente', kind=DD, added=BURN_200, line='L5', gap_to_right_mm=round(gap, 2),
                              reason='optional: the 200 g burn time near PESO LÍQUIDO (the setlist already states 40 h)'
                                     '; set on L5 after vela aromática, nothing else moved'))
        else:
            P.log.append(dict(label='L5 burn time not set', gap_mm=round(gap, 2)))
    split(P, [run_cap(left, K.CN, cap1, 0, FIG)], right5, y, 'L5')
    yp = y + 5.6 * sc
    perf_d, xx = [], 0.0
    while xx < g.W:
        perf_d.append(K.rect_d(xx, yp - 0.2, min(1.2, g.W - xx), 0.4))
        xx += 2.0
    P.raw(' '.join(perf_d))
    ln, cst = K.fit_size(lambda c: Line([run_cap(T.CT_FRONT['stub'], K.CN, c, 100, CAPS)]), g.MEAS, 1, 20)
    ys = yp + (g.H - yp) / 2 + cst / 2
    P.add(K.place_left(ln, g.X0, ys), 'stub', cap_mm=round(cst, 3))
    P.log.append(dict(label='perforation (printed)', y_mm=round(yp, 2), dash_mm=[1.2, 0.8], weight_mm=0.4))
    if single:
        P.dev.append(dict(panel='frente', reason='§C.9b gives the SINGLE carton the INGRESSO text "with PESO LÍQUIDO '
                          '80 g, aprox. 16 h and O SINGLE": O SINGLE joins the product name on L1 as the §B.2 printed '
                          'name "HOLOFOTE AO VIVO · O SINGLE"; aprox. 16 h follows vela aromática on L5'))
    return P


def front_refil(g, faixa):
    s = T.SKUS[faixa]
    flood, ink = colours(faixa)
    P = Panel(g, 'frente', g.W, g.H, flood, ink)
    wb, cw = wordmark_mono(P, g.X0, 6.0 + WORDMARK_W * 710 / 6318)    # brand on the principal display panel
    ln, c1 = K.fit_size(lambda c: Line([run_cap(REF_TITLE, K.CN, c, 100, CAPS)]), g.MEAS, 1, 30)
    y = wb[3] + cw + c1                                    # clear space below the wordmark = its O height
    P.add(K.place_left(ln, g.X0, y), REF_TITLE, cap_mm=round(c1, 3))
    P.dev.append(dict(panel='frente', kind=DD, added='HOLOFOTE wordmark', ink_w_mm=WORDMARK_W,
                      colourway='§D.3 mono: letters and the lit O in the type ink (a two-ink carton)',
                      reason='the brand must be on the principal display panel'))
    y += 2.4
    P.raw(K.rect_d(g.X0, y - 0.15, g.MEAS, 0.3))
    f = K.SG(700, s['wdth'])
    ln, c2 = K.fit_size(lambda c: Line([run_cap(s['show'], f, c, 0, CAPS)]), g.MEAS, 1, 40)
    acc = 0.34 * c2 if any(ch in s['show'] for ch in 'ÁÉÍÓÚÂÊÔÃÕ') else 0.0
    y += 4.4 + acc + c2
    P.add(K.place_left(ln, g.X0, y), 'faixa', cap_mm=round(c2, 3), wdth=s['wdth'])
    f2 = K.XP                                   # the Locutor: Expanded One, capitals (CCO review, round 3)
    ra, rb = REF_LINE[0].upper(), REF_LINE[1].upper()
    la, ca = K.fit_size(lambda c: Line([run_cap(ra, f2, c, 0, CAPS)]), g.MEAS, 1, 30)
    lb, cb = K.fit_size(lambda c: Line([run_cap(rb, f2, c, 0, CAPS)]), g.MEAS, 1, 30)
    P.dev.append(dict(panel='frente', platform=' '.join(REF_LINE), used=ra + ' ' + rb, font='Expanded One caps',
                      **T.LOCUTOR_CAPS))
    # bottom block first, then the Locutor line centred in the space left
    yb = g.H - 6.0
    pl = K.place_left(Line([run_cap(T.REF_LID[2], K.CN, 2.6, 0, FIG)]), g.X0, yb)
    pr = K.place_right(Line([run_cap(T.L6_RIGHT_CAPS, K.CN, 2.6, 80, CAPS), run_cap(T.L6_RIGHT_FIG, K.CN, 4.0, 0,
                                                                                    FIG)]), g.X1, yb)
    yr = yb - 4.0 - 2.4
    top = y + 0.9
    accb = 0.32 * cb                            # the circumflex of TURNÊ needs room above line b
    qh = ca + 2.4 + accb + cb
    ya = top + (yr - top - qh) / 2 + ca
    P.add(K.place_left(la, g.X0, ya), ra, cap_mm=round(ca, 3))
    P.add(K.place_left(lb, g.X0, ya + 2.4 + accb + cb), rb, cap_mm=round(cb, 3))
    P.raw(K.rect_d(g.X0, yr - 0.15, g.MEAS, 0.3))
    P.add(pl, 'vela aromática · refil')
    P.add(pr, 'PESO LÍQUIDO 200 g')
    P.dev.append(dict(panel='frente', reason='§C.9 lists the refill front as NOVA TEMPORADA · O copo fica. A turnê '
                      'continua. · faixa name · PESO LÍQUIDO 200 g; "vela aromática · refil" (the peel lid\'s own '
                      'string) is added beside the net weight so the main panel names the product'))
    return P


# ------------------------------------------------------------------------------------------------- the other panels
def legal(g, faixa, items, name):
    """Legal text: headings in Special Gothic wght 700 caps, cap 2,2; the body in Condensed One sentence case at
    tracking 0, cap 1,7 (the Produção: CCO review, round 3 allows lower case only there or in Shantell)."""
    flood, ink = colours(faixa)
    P = Panel(g, name, g.D, g.H, flood, ink)
    hb = K.SG(700, 100)
    bd = K.CN

    def run(top, write):
        y = top
        first = True
        for kind, t in items:
            if kind == 'h':
                y += (0 if first else 4.6)
                first = False
                if write:
                    P.add(K.place_left(Line([run_cap(t, hb, 2.2, 40, CAPS)]), g.X0, y), t, cap_mm=2.2)
                y += 0.5
            else:
                lines, texts = K.para(t, bd, 1.7, g.MEAS, 0)
                for ln, tx in zip(lines, texts):
                    y += 2.75
                    if write:
                        P.add(K.place_left(ln, g.X0, y), tx[:30], cap_mm=1.7)
        return y
    avail = g.H - 2 * 5.5
    end = run(0.0, False)
    assert end <= avail + 0.5, (name, end, avail)
    run((g.H - end) / 2 + 2.2 - 1.0, True)
    P.log.append(dict(label='legal body', font='Special Gothic Condensed One, tracking 0', cap_mm=1.7))
    P.dev.append(dict(panel=name, **T.BODY_PRODUCAO))
    return P


def back(g, faixa, net, refil=False, single=False):
    flood, ink = colours(faixa)
    P = Panel(g, 'verso', g.W, g.H, flood, ink)
    lines, dev = manifesto(faixa, net, refil, single)
    P.dev += dev

    def run(top, write):
        ln, cap = K.fit_size(lambda c: Line([run_cap(lines[0], K.CN, c, 100, CAPS)]), g.MEAS, 1, 20)
        y = top + cap
        if write:
            P.add(K.place_left(ln, g.X0, y), 'MANIFESTO head', cap_mm=round(cap, 3))
        y += 1.8
        if write:
            P.raw(K.rect_d(g.X0, y, g.MEAS, 0.3))
        y += 0.4
        for t in lines[1:]:
            if t == 'INDÚSTRIA BRASILEIRA':
                li = Line([run_cap(t, K.SG(700, 75), 3.0, 60, CAPS)])
                acc = -min(b[1] for b in (q.bounds() for q in li.glyphs) if b)        # Ú accent top over baseline
                dsc = max(b[3] for b in (q.bounds() for q in Line([run_cap('(gjpq@', K.CN, 1.7, 0, FIG)]).glyphs)
                          if b)                                                    # deepest 1,7 mm descender
                y += acc + dsc + 0.6                    # the Ú clears any descender above it by 0,6 mm
                if write:
                    P.add(K.place_left(li, g.X0, y), t, cap_mm=3.0)
                y += 0.6
                continue
            # "vela aromática · refil" is one name: no-break spaces keep it on one line
            ls, ts = K.para(t.replace('aromática · refil', 'aromática\u00a0·\u00a0refil'), K.CN, 1.7, g.MEAS, 0)
            for l2, tx in zip(ls, ts):
                y += 2.72
                if write:
                    P.add(K.place_left(l2, g.X0, y), tx[:30], cap_mm=1.7)
        return y
    end = run(0.0, False)
    run((g.H - end) / 2 - 0.5, True)
    return P


def bars_and_bins(P, by, lines=None):
    """The fictional bar block and, to its right, the disposal block (CCO review, round 3): one Condensed One caps line
    per material in the brand voice, the last baseline on the bar caption's baseline. On the 96 mm carton the bars are
    38 x 22 (as on O CASE); on the 74 mm cartons 30 x 20 (an EAN-13 at ~80%). The lines take cap 2,2 or the largest cap
    that fits the slot, never under 1,7 (the legal cap)."""
    g = P.g
    lines = lines or T.DISPOSAL_CT
    bw, bh = (38.0, 22.0) if g.W >= 90 else (30.0, 20.0)
    P.raw(K.bars_d(g.X0, by, bw, bh - 4.0))
    lnb, trb = K.fit_tracking([run_cap(T.BARCODE, K.CN, 2.0, 0, CAPS)], bw)
    P.add(K.place_left(lnb, g.X0, by + bh), 'barcode line', cap_mm=2.0)
    x0 = g.X0 + bw + 5.0
    slot = g.X1 - x0
    wid = max(Line([run_cap(t, K.CN, 1.0, 80, CAPS)]).ink_width() for t in lines)
    cap = min(2.2, slot / wid)
    assert cap >= 1.7, (cap, slot)
    pitch = 2.0 * cap
    for k, t in enumerate(lines):
        yb = by + bh - pitch * (len(lines) - 1 - k)
        P.add(K.place_left(Line([run_cap(t, K.CN, cap, 80, CAPS)]), x0, yb), t, cap_mm=round(cap, 3), tracking=80)
    P.log.append(dict(label='bar block', box_mm=[g.X0, by, bw, bh], scannable=False))
    P.log.append(dict(label='disposal block', lines=list(lines), cap_mm=round(cap, 3), x_mm=round(x0, 2)))
    P.dev.append(dict(panel=P.name, used=list(lines), **T.DISPOSAL_FIX))


def aspas(s):
    """ASCII double quotes to typographic aspas, opening then closing, in pairs."""
    out, open_ = [], True
    for ch in s:
        if ch == '"':
            out.append('\u201c' if open_ else '\u201d')
            open_ = not open_
        else:
            out.append(ch)
    assert open_, 'unpaired quote'
    return ''.join(out)


def side_tag(g, faixa):
    """Side 2: the wordmark (CCO review, round 3: the brand on every carton), the lockup holofote nela., the Locutor
    line in capitals, then the bar block and the disposal lines."""
    flood, ink = colours(faixa)
    P = Panel(g, 'lateral-2', g.D, g.H, flood, ink)
    top_m = 8.0 * g.H / 98.0
    ww = 30.0 * g.MEAS / 64.0                      # 30 mm on the 74 mm cartons, 39,4 on O INGRESSO (≥ 30 mm)
    wcap = ww * 710 / 6318
    wb, wcap = wordmark_mono(P, g.X0, top_m + wcap, ww)
    P.dev.append(dict(panel='lateral-2', kind=DD, added='HOLOFOTE wordmark (logo SVG, mono, carton ink)',
                      ink_w_mm=round(ww, 2), reason='the brand on side 2 of every 200 g and SINGLE carton'))
    ln, c1 = K.fit_size(lambda c: Line([run_cap(T.CT_SIDE2[0], K.XP, c, -10)]), g.MEAS, 1, 30)
    y = top_m + wcap + wcap + c1                   # clear space under the wordmark = its O height
    P.add(K.place_left(ln, g.X0, y), 'tagline', cap_mm=round(c1, 3), font='Expanded One lower case (the lockup)')
    q = T.CT_SIDE2[1]
    cut = q.index('. ') + 1
    qa, qb = q[:cut], q[cut + 1:]
    assert qa + ' ' + qb == q
    qa, qb = aspas(qa).upper(), qb.upper()          # the Locutor in capitals; ASCII " set as aspas “ ”
    P.dev.append(dict(panel='lateral-2', platform=q, used=qa + ' ' + qb, font='Expanded One caps',
                      **T.LOCUTOR_CAPS))
    f = K.XP
    la, ca = K.fit_size(lambda c: Line([run_cap(qa, f, c, 0, CAPS)]), g.MEAS, 1, 30)
    lb, cb = K.fit_size(lambda c: Line([run_cap(qb, f, c, 0, CAPS)]), g.MEAS, 1, 30)
    by = g.H - top_m - (22.0 if g.W >= 90 else 20.0)
    acc_a, acc_b = 0.32 * ca, 0.32 * cb            # Ã in NÃO, É in É
    qh = acc_a + ca + 2.6 + acc_b + cb
    ya = y + (by - y - qh) / 2 + acc_a + ca
    P.add(K.place_left(la, g.X0, ya), 'quote a', cap_mm=round(ca, 3))
    P.add(K.place_left(lb, g.X0, ya + 2.6 + acc_b + cb), 'quote b', cap_mm=round(cb, 3))
    bars_and_bins(P, by)
    return P


def top(g, faixa):
    flood, ink = colours(faixa)
    P = Panel(g, 'topo', g.W, g.D, flood, ink)
    ln, c = K.fit_size(lambda c: Line([run_cap(T.CT_TOP, K.CN, c, 100, CAPS)]), g.MEAS, 1, 30)
    P.add(K.place_left(ln, g.X0, g.D / 2 + c / 2), 'topo', cap_mm=round(c, 3))
    P.dev.append(dict(panel='topo', **T.CT_TOP_FIX))
    return P


def bottom(g, faixa, with_bars=False):
    flood, ink = colours(faixa)
    P = Panel(g, 'fundo', g.W, g.D, flood, ink)
    if with_bars:
        bars_and_bins(P, (g.D - 20.0) / 2, T.DISPOSAL_REF)
        P.dev.append(dict(panel='fundo', reason='§C.9 gives the refill carton\'s other panels as MODO DE USO, '
                          'ADVERTÊNCIAS and MANIFESTO; the fictional bar block and the disposal marks (side 2 on O '
                          'INGRESSO) go on the bottom, the one panel left free; the top keeps O INGRESSO\'s '
                          '"ESTE LADO PRA CIMA"'))
        P.dev.append(dict(panel='fundo', kind=DD, platform='papel · vidro · metal', used=' / '.join(T.DISPOSAL_REF),
                          reason='there is no glass in a refill'))
    return P


# ------------------------------------------------------------------------------------------------- raster and files
def render(P, pp=PP):
    hh, ww = int(round(P.h * pp)), int(round(P.w * pp))
    rgb = np.zeros((hh, ww, 3), np.float32)
    rgb[:] = K.hex01(P.flood)
    if P.paths:
        a, _ = K.raster_paths(P.w, P.h, pp, P.paths)
        rgb = rgb * (1 - a[..., None]) + K.hex01(P.ink)[None, None, :] * a[..., None]
    return np.clip(rgb, 0, 1)


def save_rgb(a, path, q=None):
    arr = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    if q:
        Image.fromarray(arr).save(path, quality=q, subsampling=0)
    else:
        Image.fromarray(arr).save(path, compress_level=6)


def write_panel_svg(P, path):
    doc = R.Doc(P.w, P.h, PP)
    doc.add(f'<rect width="{P.w}" height="{P.h}" fill="{P.flood}"/>')
    doc.add(f'<g id="TINTA" fill="{P.ink}">' + ''.join(f'<path d="{d}"/>' for d in P.paths) + '</g>')
    R.write_svg(doc, path)


def atlas(g, imgs, fill):
    cw, ch = int(g.W * ATLAS_PP), int(g.H * ATLAS_PP)
    A = np.zeros((3 * ch, 4 * cw, 3), np.float32)
    A[:] = fill
    cells = {'top': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2)}
    for k, im in imgs.items():
        c, r = cells[k]
        A[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] = cv2.resize(im, (cw, ch), interpolation=cv2.INTER_AREA)
    return A


def flat_sheet(g, imgs, flood, path_png, path_prev):
    """The flat print sheet at 10 px/mm: art on each panel, flood on flaps, 3 mm bleed, die lines on the preview."""
    pp = 10
    net = facas.tuck_end(g.W, g.D, g.H)
    bl = 3.0
    Wt, Ht = net['w'] + 2 * bl, net['h'] + 2 * bl

    def ras(el):
        doc = R.Doc(Wt, Ht, pp)
        doc.add(f'<g transform="translate({bl},{bl})">{el}</g>')
        return R.rasterise(doc)
    out_a = ras(f'<path d="{net["cut"]}"/>')
    grow = cv2.dilate((out_a > 0.5).astype(np.uint8), np.ones((int(bl * pp) * 2 + 1,) * 2, np.uint8)).astype(np.float32)
    sheet = np.ones((out_a.shape[0], out_a.shape[1], 3), np.float32)
    fl = K.hex01(flood)
    sheet = sheet * (1 - grow[..., None]) + fl[None, None, :] * grow[..., None]
    glue = net['panels']['cola']
    gx0, gy0, gw, gh = [int(round((v + bl) * pp)) for v in (glue[0], glue[1], glue[2], glue[3])]
    sheet[gy0:gy0 + gh, gx0:gx0 + gw] = 1.0                   # glue flap: unprinted board
    for key, (k2, rot) in dict(frente=('front', 0), lateral1=('right', 0), verso=('back', 0),
                               lateral2=('left', 0), topo=('top', 180), fundo=('bottom', 0)).items():
        x, y, w, h = net['panels'][key]
        im = cv2.resize(imgs[k2], (int(round(w * pp)), int(round(h * pp))), interpolation=cv2.INTER_AREA)
        if rot == 180:
            im = im[::-1, ::-1]
        xi, yi = int(round((x + bl) * pp)), int(round((y + bl) * pp))
        sheet[yi:yi + im.shape[0], xi:xi + im.shape[1]] = im
    sheet *= np.maximum(grow, 0)[..., None]
    sheet += (1 - grow)[..., None]
    save_rgb(sheet, path_png)
    cut_a = ras(f'<path d="{net["cut"]}" fill="none" stroke="#000" stroke-width="0.3"/>')
    prev = sheet * (1 - cut_a[..., None]) + np.array([0.86, 0.05, 0.2])[None, None, :] * cut_a[..., None]
    cr_a = ras(''.join(f'<path d="{c}" fill="none" stroke="#000" stroke-width="0.3" stroke-dasharray="3 1.5"/>'
                       for c in net['crease']))
    prev = prev * (1 - cr_a[..., None]) + np.array([0.1, 0.35, 0.9])[None, None, :] * cr_a[..., None]
    save_rgb(prev, path_prev, q=92)
    return net


def build(kind, faixa, od):
    K_ = KINDS[kind]
    g = K_['geo']
    code = K_['code'](faixa)
    flood, ink = colours(faixa)
    modo = [('h', T.MODO_DE_USO[0])] + [('b', t) for t in T.MODO_DE_USO[1:]]
    adv = [('h', T.ADVERTENCIAS[0])] + [('b', t) for t in T.ADVERTENCIAS[1:]]
    if kind == 'REFIL':
        assert T.MODO_DE_USO[-1] == T.MODO_FIX['used']
        modo_r = [('h', T.MODO_DE_USO[0]), ('b', REF_MODO_FIRST)] + [('b', t) for t in T.MODO_DE_USO[1:-1]] + \
                 [('b', REF_MODO_USE)]
        right = legal(g, faixa, modo_r, 'lateral-1')
        right.dev.append(dict(panel='lateral-1', kind=DD, added=REF_MODO_FIRST, position='first item of MODO DE USO',
                              reason='refill safety: the seal comes off and the capsule goes into a clean, cold glass'))
        right.dev.append(dict(panel='lateral-1', kind=DD, platform=T.MODO_FIX['platform'], used=REF_MODO_USE,
                              reason='the refill capsule is always used inside the HOLOFOTE glass'))
        panels = dict(front=front_refil(g, faixa), right=right, back=back(g, faixa, K_['net'], True),
                      left=legal(g, faixa, adv, 'lateral-2'), top=top(g, faixa), bottom=bottom(g, faixa, True))
    else:
        right = legal(g, faixa, modo + adv, 'lateral-1')
        right.dev.append(dict(panel='lateral-1', **T.MODO_FIX))
        panels = dict(front=front_ticket(g, faixa, kind == 'SINGLE'), right=right,
                      back=back(g, faixa, K_['net'], single=(kind == 'SINGLE')), left=side_tag(g, faixa),
                      top=top(g, faixa), bottom=bottom(g, faixa))
    names = dict(front='frente', right='lateral-1', back='verso', left='lateral-2', top='topo', bottom='fundo')
    meta = dict(sku=code, kind=kind, faixa=faixa, size_mm=[g.W, g.D, g.H], stock='SBS 400 g/m²',
                inks=['preto', T.SKUS[faixa]['coating']], flood=flood, type_ink=ink, knockout=(faixa == '04'),
                ppmm=PP, panels={}, deviations=[],
                atlas=dict(file=f'{code}_CARTUCHO_ATLAS.png', cell_px=[int(g.W * ATLAS_PP), int(g.H * ATLAS_PP)],
                           layout='[., top, ., .] / [left, front, right, back] / [., bottom, ., .] '
                                  '(candle_lib.box); top: image top = back; bottom: image top = front'),
                dieline=f'02_PRODUTO/facas/FACA_CARTUCHO_{g.W:.0f}x{g.D:.0f}x{g.H:.0f}.svg',
                generator='_build/pack/cartucho.py')
    imgs = {}
    for k, P in panels.items():
        rgb = render(P)
        imgs[k] = rgb
        save_rgb(rgb, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.png'))
        write_panel_svg(P, os.path.join(od, f'{code}_CARTUCHO_{names[k]}.svg'))
        meta['panels'][names[k]] = P.log
        meta['deviations'] += P.dev
    save_rgb(atlas(g, imgs, K.hex01(flood)), os.path.join(od, f'{code}_CARTUCHO_ATLAS.png'))
    flat_sheet(g, imgs, flood, os.path.join(od, f'{code}_CARTUCHO_planificado.png'),
               os.path.join(od, f'{code}_CARTUCHO_planificado_preview.jpg'))
    R.write_json(meta, os.path.join(od, f'{code}_cartucho.json'))
    print(code, 'done', [d['panel'] for d in meta['deviations']])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    od = os.path.dirname(K.out('cartucho', 'x'))
    for kind, K_ in KINDS.items():
        for f in K_['faixas']:
            code = K_['code'](f)
            if a.only and not code.startswith(a.only):
                continue
            build(kind, f, od)


if __name__ == '__main__':
    main()
