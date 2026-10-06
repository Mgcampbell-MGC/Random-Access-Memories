"""A SETLIST (platform §C.8): the concertina insert, both sides, 105 x 400 mm flat at 20 px/mm, two inks (preto,
amarelo) on 300 g/m² uncoated papel-cartaz.

    /home/user/venvs/web/bin/python _build/pack/setlist.py

Side 1: P1 cover · P2–P3 the run of show · P4 BIS · 4 INGRESSOS (four 105 x 25 tickets, 22 mm stubs at x = 83).
Side 2 (the sheet turned over left to right, so P1' is behind P1 and the stub perforation sits at x = 22):
P1' REGRAS DA CASA · MODO DE USO · P2' ADVERTÊNCIAS · P3' DEPOIS DA TEMPORADA · P4' the four ticket backs.

Layout notes (forced by measurement, logged in the json):
  · the who-column "você (equipe técnica)" is 47 mm of Shantell: step 4's leader and who drop to a second line;
  · a ticket body is 64 mm wide and "INGRESSO 0n · <promise>" needs 80–99 mm: label and promise stack, the line
    break replacing the separator;
  · four 25 mm tickets fill P4, so its header "BIS · 4 INGRESSOS" runs up a 13 mm amarelo band on the left edge.
Outputs in 02_PRODUTO/setlist/: SETLIST_lado-1.png / _lado-2.png (print art, papel ground), _preto / _amarelo ink
layers (RGBA), _lado-n.svg (vectors), SETLIST_picote.png (die perforations and folds, white = cut), a flat-lay
preview, and SETLIST.json.
"""
import os
import sys
import math
import json

import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, Placed, run_cap, run_xh, CAPS, FIG
import marca

PP = 20
W, H = 105.0, 400.0
M0, M1 = 8.0, 97.0
MEAS = M1 - M0
PERF_X = 83.0
BAND = 13.0


class Side:
    def __init__(self, name):
        self.name = name
        self.L = {'preto': [], 'amarelo': []}
        self.tex = []
        self.log = []

    def add(self, p, label, layer='preto', **meta):
        self.L[layer].append(K.placed_paths(p))
        b = p.ink() if p.matrix is None and p.per_glyph is None else K.placed_ink_poly(p)
        self.log.append(dict(label=label, ink_mm=[round(v, 2) for v in b],
                             text=''.join(r.text for r in p.line.runs), **meta))
        assert b[0] >= 2.0 and b[2] <= W - 2.0, (label, b)
        return p


def leaders(S, x_from, x_to, y, cap=2.6, pitch=1.0, gap=1.0, grid0=M0):
    dot = Line([run_cap('.', K.CN, cap)])
    db = dot.ink()
    dw = db[2] - db[0]
    xs, k = [], 0
    while True:
        cx = grid0 + (k + 0.5) * pitch
        k += 1
        if cx - dw / 2 < x_from + gap:
            continue
        if cx + dw / 2 > x_to - gap:
            break
        xs.append(cx)
    for cx in xs:
        S.L['preto'].append(K.placed_paths(Placed(dot, cx - (db[0] + db[2]) / 2, y)))
    return (xs[-1] - xs[0] + dw) if xs else 0.0


def highlighter(S, b, seed=9):
    """an amarelo marker swipe behind a line (the safety line), slightly hand-laid: ragged ends, a 0,4° tilt"""
    r = np.random.default_rng(seed)
    x0, x1 = b[0] - 1.4, b[2] + 1.6
    y0, y1 = b[1] - 0.9, b[3] + 0.7
    tilt = math.tan(math.radians(-0.4))
    pts = []
    for t in np.linspace(0, 1, 6):
        pts.append((x0 + r.uniform(-0.35, 0.35), y0 + (y1 - y0) * t))
    top = [(x0 + (x1 - x0) * t, y0 + (x1 - x0) * t * tilt + r.uniform(-0.12, 0.12)) for t in np.linspace(0, 1, 12)]
    right = [(x1 + r.uniform(-0.45, 0.45), y0 + (y1 - y0) * t + (x1 - x0) * tilt) for t in np.linspace(0, 1, 6)]
    bot = [(x1 - (x1 - x0) * t, y1 + (x1 - x0) * (1 - t) * tilt + r.uniform(-0.12, 0.12)) for t in np.linspace(0, 1, 12)]
    poly = top + right + bot + list(reversed(pts))
    S.L['amarelo'].append('M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in poly) + ' Z')


# ------------------------------------------------------------------------------------------------- side 1
def side1():
    S = Side('lado-1')
    # P1 cover
    ln, tr = K.fit_tracking([run_cap(T.SETLIST_P1[0], K.CN, 22.0, 0, CAPS)], MEAS)
    S.add(K.place_left(ln, M0, 32.0), 'SETLIST', cap_mm=22.0, tracking=round(tr, 1))
    ln, c = K.fit_size(lambda c: Line([run_cap(T.SETLIST_P1[1], K.CN, c, 100, CAPS)]), MEAS, 1, 20)
    S.add(K.place_left(ln, M0, 32.0 + 6.0 + c), 'date', cap_mm=round(c, 3))
    S.add(K.place_left(Line([run_xh(T.SETLIST_P1[2], K.SH, 3.0)]), M0, 55.0), 'fã', xh_mm=3.0)
    img, meta, _ = marca.gerar(S=int(40 * PP), semente=927)
    S.tex.append((img.astype(np.float32), 79.0 - 20.0, 76.0 - 20.0))
    S.log.append(dict(label='A MARCA', centre_mm=[79.0, 76.0], strip_mm=[40.0, round(40 / 3.75, 2)], seed=927))
    # P2–P3: running header + steps
    who_line = {'7.': 0}
    steps = list(T.RUN_OF_SHOW)
    p2, p3 = steps[:5], steps[5:]
    for panel, items, bis in ((1, p2, False), (2, p3, True)):
        y0 = panel * 100.0
        hl = K.place_left(Line([run_cap(T.SETLIST_P1[0], K.CN, 2.2, 100, CAPS)]), M0, y0 + 10.0)
        hr = K.place_right(Line([run_cap(T.SETLIST_P1[1], K.CN, 2.2, 100, CAPS)]), M1, y0 + 10.0)
        S.add(hl, f'P{panel + 1} header L')
        S.add(hr, f'P{panel + 1} header R')
        S.L['preto'].append(K.rect_d(M0, y0 + 12.2, MEAS, 0.25))
        rows = []                      # (number or None, text or None, who or None, is_safety)
        TX = M0 + 6.2                  # text column (numbers hang left of it)
        for num, lines, who in items:
            # a line longer than the text column is re-broken (balanced, sentence-aware, no orphan)
            fitted = []
            for t in lines:
                if Line([run_cap(t, K.CN, 2.6, 0, FIG)]).ink_width() > M1 - TX:
                    fitted += K.para(t, K.CN, 2.6, M1 - TX, 0)[1]
                else:
                    fitted.append(t)
            lines = fitted
            wl = who_line.get(num, len(lines) - 1)
            for i, t in enumerate(lines):
                rows.append([num if i == 0 else None, t, who if i == wl else None, num == '9.'])
            rows.append(None)          # step gap
        if bis:
            rows.append('BIS')
        # measure, then centre the block between the header rule and the panel foot
        pitch, gap = 5.6, 1.9
        TX = M0 + 6.2                  # text column (numbers hang left of it)

        # rows whose who drops to a second line need an extra row: insert them now
        expanded = []
        for r in rows:
            expanded.append(r)
            if r not in (None, 'BIS') and r[2]:
                lw = Line([run_xh(r[2], K.SH, 2.2)]).ink_width()
                tw = Line([run_cap(r[1], K.CN, 2.6, 0, FIG)]).ink_width()
                if TX + tw + 6.0 + lw > M1:
                    who = r[2]
                    r[2] = None
                    expanded.append(['', '', who, False])
        rows[:] = expanded

        def layout2(ystart, write):
            y = ystart
            for r in rows:
                if r is None:
                    y += gap
                    continue
                if r == 'BIS':
                    y += 2.6
                    if write:
                        S.L['preto'].append(K.rect_d(M0, y - 0.125, MEAS, 0.25))
                    y += 6.2
                    if write:
                        S.add(K.place_left(Line([run_cap(T.SETLIST_BIS, K.CN, 2.8, 0, FIG)]), M0, y), 'BIS', cap_mm=2.8)
                    continue
                num, text, who, safety = r
                y += pitch
                if not write:
                    continue
                if num:
                    S.add(K.place_right(Line([run_cap(num, K.CN, 2.6, 0, FIG)]), TX - 1.6, y), f'step {num}')
                end = TX - 1.0
                if text:
                    p = S.add(K.place_left(Line([run_cap(text, K.CN, 2.6, 0, FIG)]), TX, y), f'step {text[:22]}',
                              cap_mm=2.6)
                    end = p.ink()[2]
                    if safety:
                        highlighter(S, p.ink())
                if who:
                    pw = S.add(K.place_right(Line([run_xh(who, K.SH, 2.2)]), M1, y), f'who {who}', xh_mm=2.2)
                    ld = leaders(S, end, pw.ink()[0], y)
                    assert ld >= 4.0, (who, ld)
            return y
        end = layout2(0.0, False)
        top = y0 + 12.2 + (100.0 - 12.2 - end) / 2 - 1.0
        layout2(top, True)
    # P4: four tickets
    y0 = 300.0
    S.L['amarelo'].append(K.rect_d(0, y0, BAND, 100.0))
    ln, c = K.fit_size(lambda c: Line([run_cap(T.P4_HEAD, K.CN, c, 140, CAPS)]), 94.0, 1, 20)
    cap_ok = c <= BAND - 4.4
    if not cap_ok:
        ln = Line([run_cap(T.P4_HEAD, K.CN, BAND - 4.4, 140, CAPS)])
        c = BAND - 4.4
        ln, trk = K.fit_tracking([run_cap(T.P4_HEAD, K.CN, c, 0, CAPS)], 94.0)
    # vertical, reading bottom to top, cap height centred in the band
    p = K.rotated(ln, BAND / 2 + c / 2, y0 + 50.0 + ln.ink_width() / 2, -90.0, anchor='left')
    S.add(p, 'BIS · 4 INGRESSOS (vertical)', cap_mm=round(c, 3))
    for i, (lab, prom) in enumerate(T.TICKETS):
        ty = y0 + 25.0 * i
        S.add(K.place_left(Line([run_cap(lab, K.CN, 3.0, 80, CAPS)]), BAND + 3.0, ty + 8.6), lab, cap_mm=3.0)
        if prom.startswith('_'):
            lnu, tru = K.fit_tracking([run_xh(prom, K.SH, 1.8)], PERF_X - 3.0 - (BAND + 3.0), lo=-200, hi=200)
            S.add(K.place_left(lnu, BAND + 3.0, ty + 18.0), 'write-in line', tracking=round(tru, 1))
        else:
            lines, texts = K.para(prom, K.SH, 1.8 * K.SH.cap / K.SH.xh, PERF_X - 3.0 - (BAND + 3.0))
            for j, ln2 in enumerate(lines):
                S.add(K.place_left(ln2, BAND + 3.0, ty + 14.4 + 5.0 * j), f'{lab} promise', xh_mm=1.8)
        st = Line([run_cap(T.STUB, K.CN, 2.6, 80, CAPS)])
        cx = PERF_X + (W - PERF_X) / 2
        S.add(K.rotated(st, cx + 2.6 / 2, ty + 12.5 + st.ink_width() / 2, -90.0, anchor='left'), 'stub', cap_mm=2.6)
    # printed tear lines along the perforations (fine dashes)
    d = []
    for y in (325.0, 350.0, 375.0):
        x = BAND
        while x < W:
            d.append(K.rect_d(x, y - 0.1, min(1.0, W - x), 0.2))
            x += 2.0
    y = y0
    while y < 400.0:
        d.append(K.rect_d(PERF_X - 0.1, y, 0.2, min(1.0, 400.0 - y)))
        y += 2.0
    S.L['preto'].append(' '.join(d))
    return S


# ------------------------------------------------------------------------------------------------- side 2
def side2():
    S = Side('lado-2')
    hb, bd = K.SG(700, 100), K.CN               # body in Condensed One at tracking 0 (the Produção; round 3)

    def panel(i, head, body, sub=None):
        y0 = i * 100.0

        def run(y, write):
            y += 3.4
            if write:
                S.add(K.place_left(Line([run_cap(head, hb, 3.4, 40, CAPS)]), M0, y), head, cap_mm=3.4)
            y += 2.2
            if write:
                S.L['preto'].append(K.rect_d(M0, y, MEAS, 0.3))
            y += 1.0
            if sub:
                y += 4.4
                if write:                       # a Locutor line: capitals (CCO review, round 3)
                    S.add(K.place_left(Line([run_cap(sub.upper(), hb, 2.6, 0, CAPS)]), M0, y), sub.upper(), cap_mm=2.6)
                y += 0.8
            for t in body:
                lines, texts = K.para(t, bd, 2.0, MEAS, 0)
                y += 0.9
                for ln, tx in zip(lines, texts):
                    y += 3.3
                    if write:
                        S.add(K.place_left(ln, M0, y), tx[:30], cap_mm=2.0)
            return y
        end = run(0.0, False)
        run(y0 + (100.0 - end) / 2, True)
    panel(0, T.P1B_HEAD, T.MODO_DE_USO[1:])
    panel(1, T.ADVERTENCIAS[0], T.ADVERTENCIAS[1:])
    panel(2, T.DEPOIS[0], T.DEPOIS[2:], sub=T.DEPOIS[1])
    # P4': four ticket backs (CCO review, round 3: each a small ticket, not a lone line). Turned over left to right,
    # the stub is x 0–22 (its perforation at x = 105 − 83 = 22) and the amarelo band's back is x 92–105.
    xb = W - PERF_X
    xr = W - BAND
    for i in range(4):
        ty = 300.0 + 25.0 * i
        S.add(K.place_left(Line([run_cap('Nº', K.CN, 2.0, 40, CAPS)]), 4.0, ty + 7.6), f'stub nº {i + 1}', cap_mm=2.0)
        S.add(K.place_left(Line([run_cap(f'{i + 1:02d}', K.CN, 7.0, 20, CAPS)]), 4.0, ty + 18.4), f'stub number {i + 1}',
              cap_mm=7.0)
        S.add(K.place_left(Line([run_cap(T.ADMITE_BACK, K.CN, 3.0, 80, CAPS)]), xb + 3.0, ty + 8.6), f'admite {i + 1}',
              cap_mm=3.0)
        # caps at +40, the lower-case close ("emitido por: você") at 0 tracking (the Produção rule)
        k = T.TICKET_BACK.index('emitido')
        avail = xr - xb - 6.0
        tr_c = 40
        while True:                                 # the caps tracking gives way first (never under 0)
            ln = Line([run_cap(T.TICKET_BACK[:k], K.CN, 1.6, tr_c, CAPS), run_cap(T.TICKET_BACK[k:], K.CN, 1.6, 0, FIG)])
            if ln.ink_width() <= avail or tr_c <= 0:
                break
            tr_c -= 2
        assert ln.ink_width() <= avail, (ln.ink_width(), avail)
        S.add(K.place_left(ln, xb + 3.0, ty + 14.4), f'ticket back {i + 1}', cap_mm=1.6)
    # the tear lines, mirrored from side 1: between the tickets (x 0–92) and along the stub (x = 22)
    d = []
    for y in (325.0, 350.0, 375.0):
        x = 0.0
        while x < xr:
            d.append(K.rect_d(x, y - 0.1, min(1.0, xr - x), 0.2))
            x += 2.0
    y = 300.0
    while y < 400.0:
        d.append(K.rect_d(xb - 0.1, y, 0.2, min(1.0, 400.0 - y)))
        y += 2.0
    S.L['preto'].append(' '.join(d))
    S.log.append(dict(label="P4' perforations (printed tear lines)", horizontal_y_mm=[325, 350, 375], vertical_x_mm=xb))
    return S


# ------------------------------------------------------------------------------------------------- raster
def render(S):
    a_p, _ = K.raster_paths(W, H, PP, S.L['preto'])
    a_a, _ = K.raster_paths(W, H, PP, S.L['amarelo'])
    hh, ww = a_p.shape
    rgb = np.zeros((hh, ww, 3), np.float32) + K.hex01('papel')
    rgb = rgb * (1 - a_a[..., None]) + K.hex01('amarelo') * a_a[..., None]
    tex_a = np.zeros((hh, ww), np.float32)
    for img, x, y in S.tex:
        x0, y0 = int(round(x * PP)), int(round(y * PP))
        h_, w_ = img.shape[:2]
        sub = rgb[y0:y0 + h_, x0:x0 + w_]
        al = img[..., 3:4]
        rgb[y0:y0 + h_, x0:x0 + w_] = sub * (1 - al) + img[..., :3] * al
        tex_a[y0:y0 + h_, x0:x0 + w_] = np.maximum(tex_a[y0:y0 + h_, x0:x0 + w_], img[..., 3])
    rgb = rgb * (1 - a_p[..., None]) + K.hex01('preto') * a_p[..., None]
    return np.clip(rgb, 0, 1), a_p, np.maximum(a_a, tex_a)


def perf_mask(side):
    """die information as a mask (white = cut/perforation, grey = fold crease)"""
    m = np.zeros((int(H * PP), int(W * PP)), np.float32)
    for y in (100, 200, 300):
        m[int(y * PP) - 1:int(y * PP) + 1, :] = 0.5
    for y in (325, 350, 375):
        yy = int(y * PP)
        for x in np.arange(0, W, 1.5):
            m[yy - 1:yy + 1, int(x * PP):int((x + 0.9) * PP)] = 1.0
    px = PERF_X if side == 1 else W - PERF_X
    xx = int(px * PP)
    for y in np.arange(300, 400, 1.5):
        m[int(y * PP):int((y + 0.9) * PP), xx - 1:xx + 1] = 1.0
    return m


def save_rgb(a, path, q=None):
    arr = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    if q:
        Image.fromarray(arr).save(path, quality=q, subsampling=0)
    else:
        Image.fromarray(arr).save(path, compress_level=6)


def flatlay(r1, r2, m1, m2, path):
    """review flat-lay: both sides of the unfolded card on a stage-grey floor, paper grain, fold creases, die slits."""
    s = 6 / PP
    pad = 60

    def prep(rgb, m, seed):
        im = cv2.resize(rgb, (int(W * 6), int(H * 6)), interpolation=cv2.INTER_AREA)
        mm = cv2.resize(m, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_AREA)
        g = K.paper_grain(im.shape[0], im.shape[1], 6, seed, 1.4)
        im = im * (1 + g[..., None])
        im = im * (1 - 0.55 * np.clip((mm >= 0.75) * mm, 0, 1))[..., None]
        crease = (mm > 0.3) & (mm < 0.75)
        im[crease] *= 0.86
        return np.clip(im, 0, 1)
    a, b = prep(r1, m1, 21), prep(r2, m2, 22)
    h, w = a.shape[:2]
    Wt, Ht = 2 * w + 3 * pad, h + 2 * pad
    canvas = np.zeros((Ht, Wt, 3), np.float32) + np.array([0.20, 0.20, 0.21])
    for i, im in enumerate((a, b)):
        x, y = pad + i * (w + pad), pad
        sh = np.zeros((Ht, Wt), np.float32)
        sh[y + 6:y + h + 6, x + 4:x + w + 4] = 1
        sh = cv2.GaussianBlur(sh, (0, 0), 6)
        canvas *= (1 - 0.45 * sh)[..., None]
        canvas[y:y + h, x:x + w] = im
    save_rgb(canvas, path, q=92)


def main():
    od = os.path.dirname(K.out('setlist', 'x'))
    s1, s2 = side1(), side2()
    meta = dict(size_mm=[W, H], ppmm=PP, panels='4 x 105 x 100 (folds at 100, 200, 300)', inks=['preto', 'amarelo'],
                stock='300 g/m² uncoated papel-cartaz', perforations=dict(tickets_y_mm=[325, 350, 375],
                                                                           stub_x_mm_side1=PERF_X,
                                                                           stub_x_mm_side2=W - PERF_X),
                side_2='turned over left to right (P1\' behind P1)', generator='_build/pack/setlist.py')
    out = {}
    for S, side in ((s1, 1), (s2, 2)):
        rgb, a_p, a_a = render(S)
        out[side] = rgb
        save_rgb(rgb, os.path.join(od, f'SETLIST_{S.name}.png'))
        R.save_png(R.ink_rgba(a_p, T.C['preto']), os.path.join(od, f'SETLIST_{S.name}_preto.png'))
        if a_a.max() > 0:
            R.save_png(R.ink_rgba(a_a, T.C['amarelo']), os.path.join(od, f'SETLIST_{S.name}_amarelo.png'))
        doc = R.Doc(W, H, PP)
        doc.add(f'<rect width="{W}" height="{H}" fill="{T.C["papel"]}"/>')
        doc.add(f'<g id="AMARELO" fill="{T.C["amarelo"]}">' + ''.join(f'<path d="{d}"/>' for d in S.L['amarelo']) + '</g>')
        doc.add(f'<g id="PRETO" fill="{T.C["preto"]}">' + ''.join(f'<path d="{d}"/>' for d in S.L['preto']) + '</g>')
        R.write_svg(doc, os.path.join(od, f'SETLIST_{S.name}.svg'))
        meta[S.name] = S.log
    m1, m2 = perf_mask(1), perf_mask(2)
    Image.fromarray((m1 * 255).astype(np.uint8), 'L').save(os.path.join(od, 'SETLIST_picote_lado-1.png'))
    flatlay(out[1], out[2], m1, m2, os.path.join(od, 'SETLIST_preview_aberto.jpg'))
    meta['note'] = ('A MARCA on the cover is textured for the render; its print separation is the flat amarelo '
                    'shape in SETLIST_lado-1_amarelo.png')
    meta['deviations'] = [dict(panel="P1' REGRAS DA CASA · MODO DE USO", **T.MODO_FIX),
                          dict(panel="P1' P2' P3' bodies", **T.BODY_PRODUCAO),
                          dict(panel="P3' sub-head", platform=T.DEPOIS[1], used=T.DEPOIS[1].upper(), **T.LOCUTOR_CAPS),
                          dict(panel="P4' ticket backs", kind=T.DD, added=['Nº 01–04 on the stub', T.ADMITE_BACK,
                                                                           'printed tear lines'],
                               reason='CCO review: each ticket back is a small ticket, not a lone 1,6 mm line')]
    R.write_json(meta, os.path.join(od, 'SETLIST.json'))
    print('setlist done')


if __name__ == '__main__':
    main()
