"""A TAMPA-PALCO, top print (platform §C.5; O SINGLE lid §C.9b).

    /home/user/venvs/web/bin/python _build/pack/tampa.py

UV print on the powder-coated preto steel disc. 40 px/mm, image centre = disc centre, image width = disc diameter,
image TOP = the BACK of the candle (+Y in Blender), so the brim line at 6 o'clock faces the front camera.
  · two amarelo gaffer strips (hero 18 x 78 mm, SINGLE 14 x 60 mm) at ±45°, woven cloth, torn ends (seed 0927), one end
    lifted 0,5 mm with its printed shadow (the tape is a UV-printed trompe-l'oeil, so the lift shadow is printed too);
  · "ela fica aqui." along the upper-left arm of the strip laid on top (Shantell 500, preto, x-height 2,4 / 1,8 mm);
  · "a tampa vira palco." on the brim at 6 o'clock, curved (Condensed One lower case, cap 2,0 mm, amarelo).

Writes 02_PRODUTO/tampa/HLF-TAMPA-90_* (hero, 3600 px) and HLF-TAMPA-70_* (O SINGLE, 2800 px):
  _topo.png        RGBA: tape + lift shadow + both inks — the file holofote.tampa(art=...) maps over the disc
  _fita.png        RGBA: tape + lift shadow only
  _tinta.png       RGBA: the two inks only (preto on the tape, amarelo on the brim) · _tinta.svg the inks as vectors
  _trama_altura.png 16-bit height of the woven tape (0 = steel, white = proud weave)
  _preview.png     the print on a preto disc, transparent outside the disc
  .json            geometry in mm (strips, lifted end, text placement)
"""
import os
import sys
import math
import json

import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as K
from comum import R, T, Line, run_xh, run_cap
import marca  # brand team's A MARCA functions (torn ends, weave, loose threads)

PPMM = 40
SEED = 927

SIZES = {
    '90': dict(D=90.0, W=18.0, L=78.0, xh=2.4, brim_cap=2.0, glass_r=38.0, sku='HLF-02-200 (e todos os 200 g)'),
    '70': dict(D=70.0, W=14.0, L=60.0, xh=1.8, brim_cap=2.0, glass_r=29.0, sku='HLF-02-080 O SINGLE'),
}


def mascara(s, t, tira, perfis, r):
    """Strip coverage: torn ends from the brand profiles (marca.perfis_pontas), but the long edges are FACTORY-SLIT —
    straight to within ~0,02 mm with a fibre fuzz, never wavy (marca's own edge noise reads hand-drawn at 40 px/mm)."""
    L, W = tira['L'], tira['W']
    n = len(perfis[0])
    tn = np.clip((t / W + 0.5) * (n - 1), 0, n - 1)
    e0 = np.interp(tn.ravel(), np.arange(n), perfis[0]).reshape(t.shape)
    e1 = np.interp(tn.ravel(), np.arange(n), perfis[1]).reshape(t.shape)
    fuzz = 0.5 * marca.ruido.valor(t.shape[0], t.shape[1], 3.0, r) + 0.35 * marca.ruido.valor(t.shape[0], t.shape[1],
                                                                                               60.0, r)
    dentro_t = W / 2 - np.abs(t) + 0.8 * fuzz
    d = np.minimum(dentro_t, np.minimum(s - (-L / 2 + e0), (L / 2 + e1) - s))
    return np.clip(d + 0.5, 0, 1).astype(np.float32)


def build(key):
    P = SIZES[key]
    D, Wm, Lm = P['D'], P['W'], P['L']
    S = int(round(D * PPMM))
    r = marca.ruido.rng(SEED)
    cx = cy = S / 2
    # strips: 0 rises to the right (+45°), 1 falls to the right (−45°). Hand-laid: ±1,0° and ±0,3 mm, never exact.
    tiras = []
    for ang in (45.0, -45.0):
        a = ang + r.uniform(-1.0, 1.0)
        dx, dy = r.uniform(-0.3, 0.3) * PPMM, r.uniform(-0.3, 0.3) * PPMM
        tiras.append(dict(cx=cx + dx, cy=cy + dy, ang=a, L=Lm * PPMM * r.uniform(0.985, 1.0), W=Wm * PPMM))
    topo = 1                        # the strip carrying "ela fica aqui." is laid last, on top
    ends = [(0, -1), (0, 1), (1, 1)]  # strip 1 end -1 is the upper-left arm (the text): it never lifts
    lev_t, lev_p = ends[int(r.integers(0, len(ends)))]
    fios = Wm / 0.45                # threads across the width: one every 0,45 mm

    N = S
    alfa = np.zeros((N, N), np.float32)
    rgb = np.zeros((N, N, 3), np.float32)
    altura = np.zeros((N, N), np.float32)
    sombra = np.zeros((N, N), np.float32)
    base = K.hex01('amarelo')
    masks = {}
    for i in (1 - topo, topo):
        tira = tiras[i]
        s, t = marca.coords(S, 1, tira)
        perf = marca.perfis_pontas(tira['W'], r)
        m = mascara(s, t, tira, perf, r)
        fio = marca.fios_soltos(N, 1, tira, perf, r) * (m < 0.5)
        v = marca.textura_tecido(s, t, tira, fios, r, 1)
        if i == lev_t:
            p = lev_p
            ini = p * tira['L'] / 2 - p * 0.13 * tira['L']
            dd = (s - ini) * p
            lev_m = np.clip(dd / (0.035 * tira['L']), 0, 1) * (dd > 0)
            # the bend where the tape leaves the steel: a thin highlight ridge, then a soft shade on the lifted part
            ridge = np.exp(-((dd + 0.15 * PPMM) / (0.12 * PPMM)) ** 2)
            shade = np.exp(-((dd - 0.35 * PPMM) / (0.45 * PPMM)) ** 2) * (dd > 0)
            v = v + 0.035 * lev_m + 0.06 * ridge - 0.035 * shade
            # 0,5 mm lift under a key at ~55° elevation from the front-left: the shadow falls 0,35 mm back-right
            sh = (m * lev_m).astype(np.float32)
            off = int(round(0.35 * PPMM))
            sh = np.roll(np.roll(sh, -off, 0), off, 1)
            k = int(0.45 * PPMM) | 1
            sombra = np.maximum(sombra, cv2.GaussianBlur(sh, (k, k), 0) * 0.55)
        if i == topo:
            s0, t0, W0 = masks[1 - topo]
            perto = np.exp(-((np.abs(t0) - W0 / 2) / (0.012 * W0 + 0.6)) ** 2)
            v = v + 0.06 * perto * np.sign(t0) * (np.abs(t0) < W0 * 0.6)
        tinta = base[None, None, :] * (1 + v[..., None])
        tinta = np.where(v[..., None] > 0, tinta + (1 - tinta) * v[..., None] * 0.35, tinta)
        creme = K.hex01('papel')[None, None, :] * 0.96
        tinta = np.where((fio > 0)[..., None], base[None, None, :] * 0.35 + creme * 0.65, tinta)
        m = np.maximum(m, fio)
        if i == topo:
            k = int(0.25 * PPMM) | 1
            shd = cv2.GaussianBlur(m, (k, k), 0)
            shd = np.roll(np.roll(shd, 3, 0), 3, 1)
            under = alfa > 0
            rgb = np.where(under[..., None], rgb * (1 - 0.16 * np.clip(shd - m, 0, 1))[..., None], rgb)
        rgb = rgb * (1 - m[..., None]) + tinta * m[..., None]
        h = np.clip(0.55 + 7.0 * v, 0, 1) * m
        altura = altura * (1 - m) + h
        alfa = alfa + m * (1 - alfa)
        masks[i] = (s, t, tira['W'])
        del s, t
    # contact: a faint printed shadow hugging the tape edge (tape is ~0,25 mm thick)
    k = int(0.2 * PPMM) | 1
    contato = cv2.GaussianBlur(np.roll(np.roll(alfa, 4, 0), 3, 1), (k, k), 0) * 0.12
    sombra = np.maximum(sombra, contato) * (1 - alfa)

    # ------------------------------------------------------------------ inks (vectors, mm)
    t1 = tiras[1]
    a1 = math.radians(t1['ang'])
    ux, uy = math.cos(a1), -math.sin(a1)
    vx, vy = -uy, ux
    c1 = (t1['cx'] / PPMM, t1['cy'] / PPMM)
    ln = Line([run_xh(T.LID_TAPE, K.SH, P['xh'])])
    tw = ln.ink_width()
    end_gap = 5.0 if key == '90' else 4.0
    s_start = -(Lm / 2) + end_gap               # ink-left of the text, measured from the strip centre (mm)
    s_end = s_start + tw
    xh = P['xh']
    ax = c1[0] + s_start * ux + (xh / 2) * vx
    ay = c1[1] + s_start * uy + (xh / 2) * vy
    p_tape = K.rotated(ln, ax, ay, -t1['ang'], anchor='left')
    R_ = D / 2
    brim_in, brim_out = P['glass_r'], R_ - 0.6
    cap = P['brim_cap']
    lb = Line([run_cap(T.LID_BRIM, K.CN, cap)])
    lbb = lb.ink()
    # centre the x-height band of the lower-case line in the visible brim band
    xhmm = K.CN.xh * lb.runs[0].em / 1000
    r_base = (brim_in + brim_out) / 2 + xhmm / 2 + 0.15
    p_brim = K.arc_bottom(lb, D / 2, D / 2, r_base)
    # inks raster
    d1 = K.placed_paths(p_tape)
    d2 = K.placed_paths(p_brim)
    a_tape_ink, doc1 = K.raster_paths(D, D, PPMM, [d1])
    a_brim_ink, doc2 = K.raster_paths(D, D, PPMM, [d2])
    # checks: the tape text sits inside the top strip, the brim line inside the brim band
    inside = (a_tape_ink > 0.5)
    m_top = np.zeros_like(alfa)
    s_, t_ = marca.coords(S, 1, t1)
    core = (np.abs(t_) < t1['W'] / 2 - 0.6 * PPMM) & (np.abs(s_) < t1['L'] / 2 - 1.5 * PPMM)
    del s_, t_
    leak = int((inside & ~core).sum())
    assert leak == 0, f'tape text leaves the strip core by {leak} px'
    yy, xx = np.mgrid[0:S, 0:S]
    rr = np.hypot(xx + 0.5 - S / 2, yy + 0.5 - S / 2) / PPMM
    bi = a_brim_ink > 0.02
    rmin, rmax = float(rr[bi].min()), float(rr[bi].max())
    assert rmin > brim_in + 0.3 and rmax < brim_out - 0.2, (rmin, rmax)
    assert (bi & (alfa > 0.02)).sum() == 0, 'brim line touches the tape'
    disc = np.clip((R_ - rr) * PPMM + 0.5, 0, 1).astype(np.float32)
    del xx, yy

    # ------------------------------------------------------------------ compose
    preto = K.hex01('preto')
    amarelo = K.hex01('amarelo')
    sombra_c = np.zeros(3, np.float32)               # a shadow on preto steel is near-black
    # layer stack over transparent: shadow -> tape -> preto ink (on the tape) -> amarelo brim ink
    def stack(layers):
        prem = np.zeros((N, N, 3), np.float32)
        acc = np.zeros((N, N), np.float32)
        for col, al in layers:
            c = col if col.ndim == 3 else col[None, None, :]
            prem = prem * (1 - al[..., None]) + c * al[..., None]
            acc = acc * (1 - al) + al
        rgb_s = prem / np.maximum(acc, 1e-6)[..., None]
        return rgb_s, acc
    tape_ink = a_tape_ink * alfa                      # the preto ink only exists where tape is
    rgb_f, a_f = stack([(sombra_c, sombra), (rgb, alfa)])
    rgb_t, a_t = stack([(sombra_c, sombra), (rgb, alfa), (preto, tape_ink), (amarelo, a_brim_ink)])
    rgb_i, a_i = stack([(preto, tape_ink), (amarelo, a_brim_ink)])
    a_f *= disc
    a_t *= disc
    a_i *= disc
    tag = f'HLF-TAMPA-{key}'
    od = K.out('tampa', tag)
    R.save_png(K.rgba_from(rgb_t, a_t), od + '_topo.png')
    R.save_png(K.rgba_from(rgb_f, a_f), od + '_fita.png')
    R.save_png(K.rgba_from(rgb_i, a_i), od + '_tinta.png')
    K.save16(altura * disc, od + '_trama_altura.png')
    # vector inks
    doc = R.Doc(D, D, PPMM)
    doc.path(d1, fill=T.C['preto'])
    doc.path(d2, fill=T.C['amarelo'])
    R.write_svg(doc, od + '_tinta.svg')
    # preview on the preto disc
    prev = np.zeros((N, N, 3), np.float32)
    prev[:] = preto
    prev = prev * (1 - a_t[..., None]) + rgb_t * a_t[..., None]
    R.save_png(K.rgba_from(prev, disc), od + '_preview.png')
    meta = dict(
        file=tag + '_topo.png', px=[S, S], ppmm=PPMM, disc_diameter_mm=D, seed=SEED, sku=P['sku'],
        mapping='planar from above; image centre = disc centre; image width = disc diameter; image top = back (+Y)',
        strips=[dict(centre_mm=[round(t['cx'] / PPMM, 3), round(t['cy'] / PPMM, 3)], angle_deg=round(t['ang'], 3),
                     length_mm=round(t['L'] / PPMM, 3), width_mm=Wm) for t in tiras],
        strip_on_top=topo, lifted_end=dict(strip=lev_t, end=lev_p, lift_mm=0.5),
        tape_text=dict(text=T.LID_TAPE, font='Shantell Sans 500 INFM 60 BNCE 0', x_height_mm=xh, colour='preto',
                       ink_width_mm=round(tw, 3), along_strip_mm=[round(s_start, 3), round(s_end, 3)],
                       note='upper-left arm of the strip on top, reading from the torn end toward the centre'),
        brim_text=dict(text=T.LID_BRIM, font='Special Gothic Condensed One', cap_mm=cap, colour='amarelo',
                       baseline_radius_mm=round(r_base, 3), ink_radius_mm=[round(rmin, 3), round(rmax, 3)],
                       visible_brim_mm=[brim_in, brim_out], position='6 o\'clock, curved, letters toward the centre'),
    )
    with open(od + '.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(tag, 'lifted', lev_t, lev_p, 'brim r', round(rmin, 2), round(rmax, 2), 'text', round(s_start, 1),
          round(s_end, 1))
    return od


def main():
    for k in ('90', '70'):
        build(k)


if __name__ == '__main__':
    main()
