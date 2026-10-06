"""A PULSEIRA (platform §C.6): the woven jacquard band and its paper seal.

    /home/user/venvs/web/bin/python _build/pack/pulseira.py

Band: black woven polyester 15 x 350 mm, jacquard text in amarelo, repeating and NEVER cut mid-word:
  ACESSO TOTAL · ATRAÇÃO · 09.05.27 · HOLOFOTE ·
The woven zone runs from 14 mm (clear of the one-way clasp) to 340 mm (10 mm heat-sealed tail). It holds exactly
two whole repeats between two O FOCO marks (§D.3: O FOCO is the woven band's symbol); the size is solved so the
zone is filled exactly, so nothing is ever truncated. Type: Special Gothic wght 700 wdth 75 caps (a jacquard needs
the sturdy cut; Condensed One's hairline joins would break up at a 0,2 mm thread pitch).
Seal (re-set 6 Oct 2026, director's decision, a deviation from §C.6 recorded in the json): a 60 x 15 mm strip of
uncoated papel-cartaz wrapped round the band-and-tail stack (≈16 x 2,5 mm), printed on the outside only. Only a
~15 x 16 mm face shows on top, so the front "pode rasgar." is set in two lines "pode / rasgar." (Expanded One lower
case, the longer line filling 13,5 mm) on the TOP panel, amarelo; the back "o que se guarda é a pulseira." sits on the
outer UNDERSIDE panel in Shantell 500, papel, as many lines as fit 13,5 mm. The 23 mm overlap lies under the stack.

Outputs in 02_PRODUTO/pulseira/ at 20 px/mm: PULSEIRA_padrao.png (the two-colour jacquard design, 7000 x 300),
PULSEIRA_padrao.svg, PULSEIRA_tecido.png (woven render: weft floats, warp ground, selvedges), PULSEIRA_tecido_altura16.png,
PULSEIRA_SELO_faixa.png / .svg (the flat 60 x 15 strip as printed), PULSEIRA_SELO_face-topo.png / -baixo.png (each
visible face in reading orientation, 15 x 16 mm), PULSEIRA.json (panel map along the strip).
"""
import os
import sys
import math

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, Placed, run_cap, run_xh, CAPS

PP = 20
L, Wb = 350.0, 15.0
Z0, Z1 = 14.0, 340.0
REPEATS = 2
TRACK = 60
WEFT, WARP = 0.25, 0.20          # thread pitch (mm): weft across the band, warp along it


def layout(cap):
    f = K.SG(700, 75)
    ln = Line([run_cap(' '.join([T.BAND] * REPEATS), f, cap, TRACK, CAPS)])
    d = cap * 0.52                                      # O FOCO: the whole mark (2,2 d) is 1,15 x the cap height
    fw = 2.4 * d
    gap = Line([run_cap(' · ', f, cap, TRACK, CAPS)]).advance * 0.5
    total = fw + gap + ln.ink_width() + gap + fw
    return ln, d, fw, gap, total


def band():
    lo, hi = 2.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if layout(mid)[4] > Z1 - Z0:
            hi = mid
        else:
            lo = mid
    cap = lo
    ln, d, fw, gap, total = layout(cap)
    assert cap <= 6.5, cap
    yb = Wb / 2 + cap / 2
    x = Z0
    paths = []
    foco1, fwid, fh = K.foco_d(x + fw / 2, Wb / 2 - 1.1 * d, d)
    paths.append(foco1)
    x += fw + gap
    p = K.place_left(ln, x, yb)
    paths.append(K.placed_paths(p))
    x = p.ink()[2] + gap
    foco2, _, _ = K.foco_d(x + fw / 2, Wb / 2 - 1.1 * d, d)
    paths.append(foco2)
    end = x + fw
    assert abs(end - Z1) < 0.05, end
    a, _ = K.raster_paths(L, Wb, PP, paths)
    # check: whole repeats only (count each word, every one complete)
    words = ' '.join([T.BAND] * REPEATS).split(' ')
    assert words.count('ACESSO') == REPEATS and words.count('HOLOFOTE') == REPEATS
    return a, paths, dict(cap_mm=round(cap, 3), tracking=TRACK, repeats=REPEATS, zone_mm=[Z0, Z1],
                          foco_disc_mm=round(d, 3), text_ink_mm=[round(p.ink()[0], 3), round(p.ink()[2], 3)],
                          baseline_mm_from_edge=round(yb, 3))


def woven(a):
    """Jacquard render: the design is quantised to the thread grid (that is what a loom does), amarelo weft floats
    where the pattern is, a black warp-faced twill elsewhere, a 0,6 mm selvedge on each edge."""
    hh, ww = a.shape
    pw, ph = WEFT * PP, WARP * PP                  # 5 x 4 px cells
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    ci = np.floor(xx / pw).astype(int)
    cj = np.floor(yy / ph).astype(int)
    # sample the design at each cell centre
    cx = np.clip(((ci + 0.5) * pw).astype(int), 0, ww - 1)
    cy = np.clip(((cj + 0.5) * ph).astype(int), 0, hh - 1)
    m = (a[cy, cx] > 0.5).astype(np.float32)
    fx = (xx / pw) - ci                              # 0..1 inside a weft cell
    fy = (yy / ph) - cj
    weft_shape = np.sin(np.pi * fx) ** 0.7           # a weft float is round across its width
    warp_shape = np.sin(np.pi * fy) ** 0.7
    twill = ((ci + cj) % 3 == 0).astype(np.float32)  # 2/1 twill on the black ground
    am = K.hex01('amarelo')
    bk = np.array([0.055, 0.05, 0.06], np.float32)
    rnd = np.random.default_rng(927)
    jitter = rnd.normal(0, 0.035, (cj.max() + 2, ci.max() + 2)).astype(np.float32)[cj, ci]
    lum_a = 0.80 + 0.26 * weft_shape + jitter
    lum_b = 0.75 + 0.55 * (warp_shape * (1 - twill) + weft_shape * twill) + jitter * 2
    rgb = m[..., None] * am[None, None, :] * lum_a[..., None] + (1 - m)[..., None] * bk[None, None, :] * lum_b[..., None]
    hgt = m * (0.55 + 0.45 * weft_shape) + (1 - m) * (0.35 + 0.35 * (warp_shape * (1 - twill) + weft_shape * twill))
    # selvedges
    sel = ((yy < 0.6 * PP) | (yy > hh - 0.6 * PP)).astype(np.float32)
    rgb = rgb * (1 - sel[..., None]) + sel[..., None] * bk[None, None, :] * (0.8 + 0.5 * warp_shape)[..., None]
    hgt = hgt * (1 - sel) + sel * (0.5 + 0.3 * warp_shape)
    return np.clip(rgb, 0, 1), np.clip(hgt, 0, 1)


# The paper seal wraps the band-and-tail stack (≈16 x 2,5 mm, perimeter 37 mm): the 60 mm strip goes round once and
# overlaps itself by 23 mm. The overlap is put UNDER the stack so nothing printed is ever covered. Along the strip
# (s = 0 is the end laid down first, against the stack):
STACK_W, STACK_T = 16.0, 2.5
SEAL_L, SEAL_W = 60.0, 15.0
SEAL_PANELS = [  # (s0, s1, name, where, visible)
    (0.0, 4.5, 'interna-topo', 'inner layer, under the top panel', False),
    (4.5, 7.0, 'interna-lado', 'inner layer, under the right side', False),
    (7.0, 23.0, 'interna-baixo', 'inner layer, under the underside panel (glue zone)', False),
    (23.0, 25.5, 'lado-esquerdo', 'left side of the stack', True),
    (25.5, 41.5, 'TOPO', 'top face: the front, "pode / rasgar."', True),
    (41.5, 44.0, 'lado-direito', 'right side of the stack (outer layer)', True),
    (44.0, 60.0, 'BAIXO', 'underside: "o que se guarda é a pulseira."', True),
]
AMARELO_S = (23.0, 44.0)          # amarelo from the left side over the top to the right side; the rest is bare papel
FACE_MARGIN = 0.75                # (15 - 13,5) / 2


def face_front():
    """'pode / rasgar.' — Expanded One lower case, two lines, flush left, the longer line ('rasgar.') filling 13,5 mm
    of the 15 mm face; the block centred on the 15 x 16 face. Coordinates in FACE mm: x along the line (15), y across
    the stack (16)."""
    words = T.SEAL_FRONT.split(' ')
    assert len(words) == 2 and ' '.join(words) == T.SEAL_FRONT
    ln2, cap = K.fit_size(lambda c: Line([run_cap(words[1], K.XP, c, 0)]), SEAL_W - 2 * FACE_MARGIN, 0.5, 10)
    ln1 = Line([run_cap(words[0], K.XP, cap, 0)])
    b1, b2 = ln1.ink(), ln2.ink()
    lead = b1[3] - b2[1] + 0.22 * cap              # line 1's descender to line 2's x-height, plus air
    top, bot = b1[1], lead + b2[3]
    y1 = STACK_W / 2 - (top + bot) / 2
    x = FACE_MARGIN
    lines = [(ln1, x - b1[0], y1), (ln2, x - b2[0], y1 + lead)]
    return lines, dict(text=T.SEAL_FRONT, lines=words, font='Special Gothic Expanded One lower case',
                       cap_mm=round(cap, 3), longer_line_mm=round(b2[2] - b2[0], 3), lead_mm=round(lead, 3),
                       alignment='flush left, block centred on the face')


def face_back():
    """'o que se guarda é a pulseira.' — Shantell 500, the largest x-height whose lines (no hyphenation, balanced,
    centred) fit 13,5 mm and stack inside the face with margins."""
    words = T.SEAL_BACK.split(' ')
    best = None
    xh = 1.8
    while xh > 0.9:
        cap = xh * K.SH.cap / K.SH.xh

        def wf(ws):
            return Line([run_cap(' '.join(ws), K.SH, cap, 0)]).ink_width()
        ls = K.break_words(words, wf, SEAL_W - 2 * FACE_MARGIN, 1)
        if all(wf(l) <= SEAL_W - 2 * FACE_MARGIN for l in ls):
            lead = 2.15 * xh
            lns = [Line([run_cap(' '.join(l), K.SH, cap, 0)]) for l in ls]
            top = lns[0].ink()[1]
            bot = lead * (len(lns) - 1) + lns[-1].ink()[3]
            if bot - top <= STACK_W - 2 * 1.2:
                best = (xh, lns, [' '.join(l) for l in ls], lead, top, bot)
                break
        xh = round(xh - 0.02, 3)
    xh, lns, texts, lead, top, bot = best
    y1 = STACK_W / 2 - (top + bot) / 2
    lines = [(ln, SEAL_W / 2 - (ln.ink()[0] + ln.ink()[2]) / 2, y1 + i * lead) for i, ln in enumerate(lns)]
    return lines, dict(text=T.SEAL_BACK, lines=texts, font='Shantell Sans 500 INFM 60 BNCE 0', x_height_mm=xh,
                       lead_mm=round(lead, 3), alignment='centred lines, block centred on the face')


def seal():
    """The strip is printed on ONE side (the outside). Text lines run along the strip's 15 mm width, i.e. parallel to
    the band, stacked across the 16 mm face. In the flat file (s along x, width along y) each line is turned 90°
    clockwise: it reads top to bottom, and the first line sits toward the higher s."""
    pan = {p[2]: p for p in SEAL_PANELS}
    out_paths, faces, info = {'front': [], 'back': []}, {}, {}
    for key, fn, panel in (('front', face_front, 'TOPO'), ('back', face_back, 'BAIXO')):
        lines, inf = fn()
        s0, s1 = pan[panel][0], pan[panel][1]
        fpaths = []
        for ln, x, y in lines:
            fpaths.append(K.placed_paths(Placed(ln, x, y)))
            # face (x along the line, y across) -> strip (s = s1 - y, w = x), rotated +90°
            b = ln.ink()
            p = K.rotated(ln, s1 - y, x + b[0], 90.0, anchor='left')
            out_paths[key].append(K.placed_paths(p))
            q = K.placed_ink_poly(p)
            assert q[0] > s0 + 0.9 and q[2] < s1 - 0.9 and q[1] > FACE_MARGIN - 0.05 and q[3] < SEAL_W - FACE_MARGIN + 0.05, \
                (key, q)
        faces[key] = fpaths
        info[key] = dict(panel=panel, s_mm=[s0, s1], **inf)
    a, _ = K.raster_paths(SEAL_L, SEAL_W, PP, out_paths['front'] + out_paths['back'])
    yel, _ = K.raster_paths(SEAL_L, SEAL_W, PP, [K.rect_d(AMARELO_S[0], 0, AMARELO_S[1] - AMARELO_S[0], SEAL_W)])
    fa, _ = K.raster_paths(SEAL_W, STACK_W, PP, faces['front'])
    ba, _ = K.raster_paths(SEAL_W, STACK_W, PP, faces['back'])
    return a, yel, fa, ba, out_paths, info


def main():
    od = os.path.dirname(K.out('pulseira', 'x'))
    a, paths, info = band()
    hh, ww = a.shape
    rgb = np.zeros((hh, ww, 3), np.float32) + K.hex01('preto')
    rgb = rgb * (1 - a[..., None]) + K.hex01('amarelo') * a[..., None]
    R.save_png(K.rgba_from(rgb, np.ones_like(a)), os.path.join(od, 'PULSEIRA_padrao.png'))
    doc = R.Doc(L, Wb, PP)
    doc.add(f'<rect width="{L}" height="{Wb}" fill="{T.C["preto"]}"/>')
    doc.add(f'<g id="AMARELO-JACQUARD" fill="{T.C["amarelo"]}">' + ''.join(f'<path d="{d}"/>' for d in paths) + '</g>')
    R.write_svg(doc, os.path.join(od, 'PULSEIRA_padrao.svg'))
    wv, hg = woven(a)
    R.save_png(K.rgba_from(wv, np.ones_like(a)), os.path.join(od, 'PULSEIRA_tecido.png'))
    K.save16(hg, os.path.join(od, 'PULSEIRA_tecido_altura16.png'))
    a2, yel, fa, ba, sp, sinfo = seal()
    strip = np.zeros(a2.shape + (3,), np.float32) + K.hex01('papel')
    strip = strip * (1 - yel[..., None]) + K.hex01('amarelo') * yel[..., None]
    strip = strip * (1 - a2[..., None]) + K.hex01('preto') * a2[..., None]
    R.save_png(K.rgba_from(strip, np.ones_like(a2)), os.path.join(od, 'PULSEIRA_SELO_faixa.png'))
    d2 = R.Doc(SEAL_L, SEAL_W, PP)
    d2.add(f'<rect width="{SEAL_L}" height="{SEAL_W}" fill="{T.C["papel"]}"/>')
    d2.add(f'<rect id="AMARELO" x="{AMARELO_S[0]}" width="{AMARELO_S[1] - AMARELO_S[0]}" height="{SEAL_W}" '
           f'fill="{T.C["amarelo"]}"/>')
    d2.add(f'<g id="PRETO" fill="{T.C["preto"]}">' + ''.join(f'<path d="{d}"/>' for d in sp['front'] + sp['back'])
           + '</g>')
    R.write_svg(d2, os.path.join(od, 'PULSEIRA_SELO_faixa.svg'))
    for al, flood, nm in ((fa, 'amarelo', 'topo'), (ba, 'papel', 'baixo')):
        r_ = np.zeros(al.shape + (3,), np.float32) + K.hex01(flood)
        r_ = r_ * (1 - al[..., None]) + K.hex01('preto') * al[..., None]
        R.save_png(K.rgba_from(r_, np.ones_like(al)), os.path.join(od, f'PULSEIRA_SELO_face-{nm}.png'))
    for old_f in ('PULSEIRA_SELO_frente.png', 'PULSEIRA_SELO_verso.png', 'PULSEIRA_SELO_frente.svg',
                  'PULSEIRA_SELO_verso.svg'):
        if os.path.exists(os.path.join(od, old_f)):
            os.remove(os.path.join(od, old_f))
    seal_meta = dict(size_mm=[SEAL_L, SEAL_W], ppmm=PP, stock='uncoated papel-cartaz, printed one side (outside)',
                     stack_mm=[STACK_W, STACK_T], perimeter_mm=2 * (STACK_W + STACK_T), overlap_mm=SEAL_L - 2 *
                     (STACK_W + STACK_T),
                     panels=[dict(s_mm=[a_, b_], name=n, where=w, visible=v) for a_, b_, n, w, v in SEAL_PANELS],
                     amarelo_s_mm=list(AMARELO_S), front=sinfo['front'], back=sinfo['back'],
                     orientation='flat file: x = s along the 60 mm strip (s = 0 is the end laid first), y = the '
                                 '15 mm width (parallel to the band); lines are turned 90° clockwise',
                     face_files=['PULSEIRA_SELO_face-topo.png', 'PULSEIRA_SELO_face-baixo.png'],
                     deviation=dict(platform='§C.6: front "pode rasgar." Expanded One lower case cap 4,0 mm; back '
                                             '"o que se guarda é a pulseira." Shantell x-height 1,8 on the reverse',
                                    used=f'front in two lines at cap {sinfo["front"]["cap_mm"]} mm on the top '
                                         f'panel; back on the outer underside panel in '
                                         f'{len(sinfo["back"]["lines"])} lines at x-height '
                                         f'{sinfo["back"]["x_height_mm"]} mm',
                                    reason='wrapped round the band and tail (≈16 x 2,5 mm) the seal shows only a '
                                           '~15 x 16 mm top face; at cap 4,0 "pode rasgar." is 41,6 mm wide and read '
                                           '"…de ras…" (3D team); director\'s decision 6 Oct 2026, exact strings '
                                           'kept'))
    R.write_json(dict(band=dict(size_mm=[Wb, L], ppmm=PP, px=[ww, hh], text=T.BAND, font='Special Gothic wght 700 '
                                'wdth 75 caps', colours=dict(ground='preto (black polyester)', jacquard='amarelo'),
                                thread_pitch_mm=dict(weft=WEFT, warp=WARP), **info,
                                orientation='x = along the band from the clasp end; y = across (15 mm)'),
                     seal=seal_meta,
                     generator='_build/pack/pulseira.py'), os.path.join(od, 'PULSEIRA.json'))
    print('pulseira', info)


if __name__ == '__main__':
    main()
