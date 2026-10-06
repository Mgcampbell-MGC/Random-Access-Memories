"""HOLOFOTE · label fidelity on EVERY film frame where the label is visible (platform §D.7), using the studio checker
_build/tools/fidelidade_uv.py: its own functions (sample_master, score with the glyph-corner rule, plant_error, the
colour measure) and its own bars, applied frame by frame.

How each kind of frame is checked (compor.py writes the kind per frame in _quadros/<FILM>/manifest.json):
  label   the delivered frame against its view's label AOV. A 2D dolly push is a scale of the still, so the AOV's
          RAW (pixel-filtered) channels get the SAME affine transform as the picture before the reference is built:
          the check runs on the pushed frame itself, not on the pre-transform plate.
          3D frames (the F15 crane, f176–203) use their own per-frame AOV.
  albedo  flame-lit blackout frames (F15 f210–221): letters and geometry on the Cycles Diffuse Color pass of the
          blackout render (§D.7.3), with the planted error. The delivered pixels are reported too, for information.
Bars: worst lettered tile >= 0,80 in every frame, 5th percentile >= 0,93 (film), planted control caught.
Colour (hue and saturation of the coating, §D.7.2) is measured on the full-light frames only (warm-up and flame-lit
frames are not the neutral-light view).

    /home/user/venvs/web/bin/python _build/filmes/fidelidade_filmes.py FILM [FILM...]
-> 06_PRODUCAO/fidelidade/<NOME>.json (per-frame rows + summary)
"""
import os, sys, json, time
import numpy as np
import cv2
import OpenEXR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import comum as C                 # noqa: E402
import plano as P                 # noqa: E402
import fidelidade_uv as FU        # noqa: E402

COAT = '#FFE81A'
INK = '#121014'


def ler_aov(path):
    ch = OpenEXR.File(path).parts[0].channels

    def get(name):
        for k, v in ch.items():
            if k == name or k.startswith(name + '.') or k.split('.')[0] == name:
                return v.pixels
        raise KeyError(name)
    uv = get('label_uv')[..., :2].astype(np.float32)
    ink = get('label_ink').astype(np.float32)
    mask = get('label_mask').astype(np.float32)
    ink = ink[..., 0] if ink.ndim == 3 else ink
    mask = mask[..., 0] if mask.ndim == 3 else mask
    try:
        dc = get('DiffCol').astype(np.float32)[..., :3]
    except KeyError:
        dc = None
    return dict(uv=uv, ink=ink, mask=mask, diffcol=dc)


def transformar(aov, M):
    """Warp the raw, pixel-filtered AOV channels with the picture's affine (linear quantities: filter, then divide)."""
    if M is None:
        return aov
    h, w = aov['mask'].shape
    wa = lambda a: cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return dict(uv=np.dstack([wa(np.ascontiguousarray(aov['uv'][..., 0])), wa(np.ascontiguousarray(aov['uv'][..., 1]))]),
                ink=wa(aov['ink']), mask=wa(aov['mask']), diffcol=aov['diffcol'])


def checar(alpha, aov, img_bgr, film=True, coat=None):
    """fidelidade_uv.check(), on arrays (same functions, same bars, same polarity rule, same control)."""
    mask = aov['mask']
    m = np.clip(mask, 1e-6, None)
    uv = aov['uv'].astype(np.float64) / m[..., None]
    ink_aov = aov['ink'] / m
    valid = mask > 0.98
    if valid.sum() < 100:
        return dict(tiles=0, pass_=None, reason='label not visible')
    # crop to the label (tile grid kept: origin on a multiple of the tile)
    ys, xs = np.nonzero(mask > 0.02)
    T = FU.TILE
    y0, x0 = max(0, ys.min() // T * T - T), max(0, xs.min() // T * T - T)
    y1, x1 = min(mask.shape[0], ys.max() + 2 * T), min(mask.shape[1], xs.max() + 2 * T)
    sl = (slice(y0, y1), slice(x0, x1))
    uv, ink_aov, valid, mask = uv[sl], ink_aov[sl], valid[sl], mask[sl]
    img = img_bgr[sl]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ink_sign = -1.0
    E = FU.sample_master(alpha, uv)
    agree = float(np.corrcoef(E[valid], ink_aov[valid])[0, 1])
    ref = (1.0 - E) * 255.0 if ink_sign < 0 else E * 255.0
    sk = []
    s = FU.score(gray, ref.astype(np.float32), valid, E, sk)
    vals = np.array([v for _, _, v in s])
    res = dict(tiles=int(len(vals)), uv_agreement=round(agree, 4), corner_tiles_skipped=len(sk),
               corner_tiles_worst=round(min(v for _, _, v in sk), 3) if sk else None)
    if not len(vals):
        res.update(pass_=None, reason='no lettered tile visible')
        return res
    worst, p5 = float(vals.min()), float(np.percentile(vals, 5))
    wy, wx, _ = s[int(np.argmin(vals))]
    alt, box = FU.plant_error(alpha, uv, mask)
    caught = None
    if alt is not None:
        E2 = FU.sample_master(alt, uv)
        ref2 = (1.0 - E2) * 255.0
        s2 = FU.score(gray, ref2.astype(np.float32), valid, E2)
        v2 = np.array([v for _, _, v in s2])
        caught = bool(len(v2) and v2.min() < FU.MIN_TILE_PASS)
        res['control'] = dict(worst_tile=round(float(v2.min()), 3) if len(v2) else None, caught=caught)
    if coat:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
        bare = valid & (E < 0.02)
        bare = cv2.erode(bare.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        bare &= (lab[..., 0] > 40) & (lab[..., 0] < 250)
        if bare.sum() > 200:
            d = (FU.hue_deg(lab[bare]) - float(FU.hue_deg(FU.hex_lab(coat)[None, :])[0]) + 180) % 360 - 180
            r = FU.hex_lab(coat)
            s_ref = np.hypot(r[1] - 128, r[2] - 128) / max(r[0], 1)
            px = lab[bare]
            res['hue_shift_deg'] = round(float(np.median(d)), 2)
            res['sat_ratio'] = round(float(np.median(np.hypot(px[:, 1] - 128, px[:, 2] - 128) / np.maximum(px[:, 0], 1)) / s_ref), 3)
    bar5 = FU.P5_FILM if film else FU.P5_STILL
    ok = worst >= FU.MIN_TILE_PASS and p5 >= bar5 and caught is True
    if 'hue_shift_deg' in res:
        ok = ok and abs(res['hue_shift_deg']) <= FU.MAX_HUE_SHIFT and res['sat_ratio'] >= FU.MIN_SAT_RATIO
    res.update(worst_tile=round(worst, 3), worst_at=[int(wx + x0), int(wy + y0)], p5_tile=round(p5, 3), bar_p5=bar5,
               pass_=bool(ok))
    return res


def albedo_bgr(dc):
    s = C.l2s(np.clip(dc, 0, 1))
    return (np.clip(s, 0, 1) * 255 + 0.5).astype(np.uint8)[..., ::-1].copy()


def filme(film):
    t0 = time.time()
    od = os.path.join(C.QUADROS, film)
    man = json.load(open(os.path.join(od, 'manifest.json')))
    m = cv2.imread(C.MASTER, cv2.IMREAD_UNCHANGED)
    alpha = m[..., 3].astype(np.float32) / 255.0
    cache = {}
    rows = []
    albedo_res = {}
    for k in sorted(man, key=int):
        f, mf = int(k), man[k]
        if mf['check'] == 'none' or not mf['aov']:
            continue
        if mf['aov'] not in cache:
            cache.clear() if len(cache) > 2 else None
            cache[mf['aov']] = ler_aov(mf['aov'])
        aov = cache[mf['aov']]
        img = cv2.imread(os.path.join(od, 'q%04d.png' % f), cv2.IMREAD_COLOR)
        if mf['check'] == 'albedo':
            if mf['aov'] not in albedo_res:
                albedo_res[mf['aov']] = checar(alpha, aov, albedo_bgr(aov['diffcol']))
            r = dict(albedo_res[mf['aov']])
            r['method'] = 'albedo pass (Diffuse Color) of the blackout render, frame-invariant camera and pack'
            px = checar(alpha, aov, img)
            r['delivered_pixels'] = {k2: px.get(k2) for k2 in ('worst_tile', 'p5_tile', 'tiles', 'pass_')}
        else:
            M = None if abs(mf['push'] - 1) < 1e-9 else C.empurrar_M(mf['push'], tuple(mf['centro']))
            full = 'aquec' not in mf and _luz_plena(film, f)
            r = checar(alpha, transformar(aov, M), img, coat=COAT if full else None)
            r['method'] = ('label AOV, 2D push x%.4f applied to the AOV' % mf['push']) if M is not None else 'label AOV'
        r['frame'] = f
        r['pass'] = r.pop('pass_')
        rows.append(r)
    checked = [r for r in rows if r['pass'] is not None]
    worst = min(checked, key=lambda r: r['worst_tile']) if checked else None
    summ = dict(film=P.NOME[film], frames_total=P.DUR[film], frames_label_visible=len(checked),
                frames_pass=sum(1 for r in checked if r['pass']),
                frames_fail=[r['frame'] for r in checked if not r['pass']],
                worst_tile_min=worst['worst_tile'] if worst else None, worst_tile_frame=worst['frame'] if worst else None,
                p5_min=min(r['p5_tile'] for r in checked) if checked else None,
                controls_caught=sum(1 for r in checked if r.get('control', {}).get('caught')),
                colour_frames=sum(1 for r in checked if 'hue_shift_deg' in r),
                hue_shift_range=[min(r['hue_shift_deg'] for r in checked if 'hue_shift_deg' in r),
                                 max(r['hue_shift_deg'] for r in checked if 'hue_shift_deg' in r)] if any('hue_shift_deg' in r for r in checked) else None,
                sat_ratio_min=min((r['sat_ratio'] for r in checked if 'sat_ratio' in r), default=None),
                bars=dict(worst_tile=FU.MIN_TILE_PASS, p5=FU.P5_FILM, hue=FU.MAX_HUE_SHIFT, sat=FU.MIN_SAT_RATIO),
                tool='_build/tools/fidelidade_uv.py (functions and bars) via _build/filmes/fidelidade_filmes.py',
                seconds=round(time.time() - t0, 1))
    os.makedirs(C.FID, exist_ok=True)
    p = os.path.join(C.FID, P.NOME[film] + '.json')
    json.dump(dict(resumo=summ, quadros=rows), open(p, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(summ, ensure_ascii=False))
    return summ


def _luz_plena(film, f):
    """Frames under the full spot (not a warm-up frame, not flame-only): where the coating colour is measured."""
    warm = {'F15': (222, 223), 'F06A': (6, 7), 'F06B': (84, 85), 'F06C_07-05': (72, 73), 'F06C_08-05': (72, 73),
            'F06C_09-05': (72, 73)}[film]
    if film == 'F15' and f < 204:
        return True
    return f not in warm


if __name__ == '__main__':
    for film in sys.argv[1:] or list(P.DUR):
        filme(film)
