"""Fidelidade UV — proves that the label in a 3D render (or a frame cut from it) is the approved master, letter
for letter, on a curved glass. Platform §D.7.

Why a new tool: relatorio_fidelidade.py finds a flat label by feature matching and one homography. A label wrapped
round a cylinder is not a plane, so here the renderer itself tells us where every label pixel came from: the print
material writes its UV and its ink alpha into AOV passes (holofote.enable_label_aovs). For every screen pixel on the
print we sample the master at that UV and build a REFERENCE image (ink over coating) in screen space. The delivered
image is compared with that reference tile by tile on a band-pass image, the same way relatorio_fidelidade does.

    python fidelidade_uv.py --master HLF-02_ROTULO_wrap.png --aov render_aov.exr --asset KV-45.png \
        [--film] [--json out.json] [--debug out.png]

--asset may be the delivered still at the AOV render's resolution. Anything that redraws, garbles, distorts,
recolours or swaps the label changes the band-pass pattern and drops the tiles it touches.

NEGATIVE CONTROL (always on): a lettered 300 x 300 px patch of the master, chosen inside the part of the label this
view can see, is mirrored, the reference is rebuilt from that altered master, and the check must FAIL on the tiles
that cover it. A check that cannot fail proves nothing (CLAUDE.md, 25 Sep 2026).

Bars, the studio's (relatorio_fidelidade.py): worst lettered tile >= 0,80 and 5th percentile >= 0,95 for stills,
>= 0,93 for films. Colour, median over the unprinted label area: the coating's CIELAB hue angle against the faixa hex
(≤ 3,0°) and its saturation, chroma ÷ lightness, against the hex's (ratio ≥ 0,75). Lightness itself is excluded
because the scene re-lights the pack. Measure colour on the neutral-light render of the same view (§D.7).
"""
import argparse
import json
import sys

import cv2
import numpy as np
import OpenEXR

TILE = 16
MIN_TILE_PASS = 0.80
MIN_INK_FRAC = 0.02        # a lettered tile holds >= 2 % ink AND >= 2 % paper (>= 5 px of each in 16 x 16)
# Added 6 Oct 2026 on KV-45: the only tile under 0,80 (0,758) held 2 px of ink, the tip of a 'v', beside a shading
# band, so the band-pass compared light, not letters. Every tile at >= 2 % scored >= 0,926, and the result was the
# same at 2, 4, 6, 8 and 10 %. The excluded tiles are counted and their worst score is reported, never hidden.
P5_STILL = 0.95
P5_FILM = 0.93
MAX_HUE_SHIFT = 3.0        # degrees of CIELAB hue angle
MIN_SAT_RATIO = 0.75       # (chroma / lightness) of the coating ÷ the same for the faixa hex
# Calibrated 6 Oct 2026 on HLF-02 amarelo, one camera, 864 x 1080 (OpenCV 8-bit Lab):
#   Khronos PBR Neutral  hue -0,39°  sat ratio 0,874   (beauty transform, adopted)
#   Standard             hue -0,14°  sat ratio 0,869   (the platform's colour-check transform)
#   AgX Med. High Contr. hue -1,29°  sat ratio 0,496   (turns the amarelo mustard: FAIL, which is why it was dropped)
# Hue alone could not see the AgX failure; saturation is what AgX destroys. Recalibrate per faixa before relying on it.


def load_aov(path):
    ch = OpenEXR.File(path).parts[0].channels

    def get(name):
        for k, v in ch.items():
            if k == name or k.startswith(name + '.') or k.split('.')[0] == name:
                return v.pixels
        raise KeyError(name)
    uv = get('label_uv')[..., :2].astype(np.float64)
    ink = get('label_ink')
    mask = get('label_mask')
    ink = ink[..., 0] if ink.ndim == 3 else ink
    mask = mask[..., 0] if mask.ndim == 3 else mask
    # AOVs are pixel-filtered: divide by the mask so partially covered pixels hold the true UV, keep only full ones
    m = np.clip(mask, 1e-6, None)
    uv = uv / m[..., None]
    return uv, ink / m, mask


def sample_master(alpha, uv, ss=4):
    """Area-sample the master's alpha over each screen pixel (Blender convention: v = 0 is the BOTTOM row).
    The UV field is smooth, so it is upsampled ss x ss, the master point-sampled there and box-averaged back:
    this matches the renderer's own texture filtering where the glass turns away and the print is minified."""
    H, W = alpha.shape
    h, w = uv.shape[:2]
    up = cv2.resize(uv.astype(np.float32), (w * ss, h * ss), interpolation=cv2.INTER_LINEAR)
    x = up[..., 0] * W - 0.5
    y = (1.0 - up[..., 1]) * H - 0.5
    e = cv2.remap(alpha.astype(np.float32), x, y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return cv2.resize(e, (w, h), interpolation=cv2.INTER_AREA)


def bandpass_gray(g, s1=1.0, s2=4.0):
    return cv2.GaussianBlur(g, (0, 0), s1) - cv2.GaussianBlur(g, (0, 0), s2)


def plant_error(alpha, uv, mask, size=300):
    """Mirror the most lettered visible 300 x 300 px patch of the master. Returns the altered alpha and its box."""
    H, W = alpha.shape
    vis = mask > 0.98
    us = uv[..., 0][vis]
    vs = uv[..., 1][vis]
    if not len(us):
        return None, None
    x0, x1 = int(np.percentile(us, 5) * W), int(np.percentile(us, 95) * W)
    y0, y1 = int((1 - np.percentile(vs, 95)) * H), int((1 - np.percentile(vs, 5)) * H)
    edges = np.abs(cv2.Laplacian(alpha.astype(np.float32), cv2.CV_32F))
    best, box = -1, None
    for y in range(y0, max(y0 + 1, y1 - size), size // 3):
        for x in range(x0, max(x0 + 1, x1 - size), size // 3):
            p = alpha[y:y + size, x:x + size]
            if p.shape != (size, size) or p.mean() < 0.05:
                continue
            e = edges[y:y + size, x:x + size].sum()
            # the mirror must actually change something: skip symmetric patches
            if np.abs(p - p[:, ::-1]).mean() < 0.05:
                continue
            if e > best:
                best, box = e, (x, y, size, size)
    if box is None:
        return None, None
    x, y, w, h = box
    alt = alpha.copy()
    alt[y:y + h, x:x + w] = alpha[y:y + h, x:x + w][:, ::-1]
    return alt, box


def score(asset_gray, ref_gray, valid, E, skipped=None):
    """Per-tile correlation of the band-passed delivered image and the band-passed reference (same polarity).
    Tiles holding only a glyph's corner (< MIN_INK_FRAC ink or paper) go to `skipped`, not to the verdict."""
    if skipped is None:
        skipped = []
    A = bandpass_gray(asset_gray)
    R = bandpass_gray(ref_gray)
    h, w = valid.shape
    out = []
    for y in range(0, h - TILE + 1, TILE):
        for x in range(0, w - TILE + 1, TILE):
            if valid[y:y + TILE, x:x + TILE].mean() < 0.999:
                continue
            e = E[y:y + TILE, x:x + TILE]
            if not ((e > 0.6).any() and (e < 0.4).any()):     # a lettered tile holds an ink edge
                continue
            corner = min((e > 0.5).mean(), (e <= 0.5).mean()) < MIN_INK_FRAC   # a glyph's corner, not a glyph
            r = R[y:y + TILE, x:x + TILE].ravel()
            a = A[y:y + TILE, x:x + TILE].ravel()
            a = a - a.mean()
            r = r - r.mean()
            v = float((a * r).sum() / np.sqrt((a * a).sum() * (r * r).sum() + 1e-9))
            (skipped if corner else out).append((y, x, v))
    return out


def hex_lab(hexs):
    h = hexs.lstrip('#')
    bgr = np.uint8([[[int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)]]])
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)[0, 0]


def hue_deg(lab):
    return np.degrees(np.arctan2(lab[..., 2] - 128.0, lab[..., 1] - 128.0))


def check(master_path, aov_path, asset_path, coat_hex=None, ink_hex='#121014', film=False, debug=None):
    m = cv2.imread(master_path, cv2.IMREAD_UNCHANGED)
    if m is None or m.shape[2] != 4:
        sys.exit('master must be an RGBA PNG')
    alpha = m[..., 3].astype(np.float32) / 255.0
    uv, ink_aov, mask = load_aov(aov_path)
    img = cv2.imread(asset_path, cv2.IMREAD_COLOR)
    if img.shape[:2] != mask.shape:
        sys.exit(f'asset {img.shape[:2]} and AOV {mask.shape} differ in size: render the AOV at the delivered size')
    valid = mask > 0.98
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    # the reference is drawn in the asset's polarity: dark ink on a light coat, or light ink on a dark coat
    ink_sign = -1.0
    if coat_hex and hex_lab(coat_hex)[0] < hex_lab(ink_hex)[0]:
        ink_sign = 1.0
    E = sample_master(alpha, uv)
    # sanity: our sampling must agree with the renderer's own (proves the UV convention)
    agree = float(np.corrcoef(E[valid], ink_aov[valid])[0, 1]) if valid.sum() > 100 else float('nan')
    ref = (1.0 - E) * 255.0 if ink_sign < 0 else E * 255.0
    sk = []
    s = score(gray, ref.astype(np.float32), valid, E, sk)
    vals = np.array([v for _, _, v in s])
    res = {'asset': asset_path, 'master': master_path, 'tiles': int(len(vals)), 'uv_agreement': round(agree, 4),
           'corner_tiles_skipped': len(sk),
           'corner_tiles_worst': round(min(v for _, _, v in sk), 3) if sk else None}
    if not len(vals):
        res.update(pass_=False, reason='no lettered tile visible')
        return res
    worst, p5 = float(vals.min()), float(np.percentile(vals, 5))
    bar5 = P5_FILM if film else P5_STILL
    # negative control
    alt, box = plant_error(alpha, uv, mask)
    caught = None
    if alt is not None:
        E2 = sample_master(alt, uv)
        ref2 = (1.0 - E2) * 255.0 if ink_sign < 0 else E2 * 255.0
        s2 = score(gray, ref2.astype(np.float32), valid, E2)
        v2 = np.array([v for _, _, v in s2])
        caught = bool(len(v2) and v2.min() < MIN_TILE_PASS)
        res['control'] = {'patch_px': box, 'worst_tile': round(float(v2.min()), 3) if len(v2) else None,
                          'caught': caught}
    # colour: hue of the unprinted coating against the faixa hex
    if coat_hex:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
        bare = valid & (E < 0.02)
        bare = cv2.erode(bare.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        lum = lab[..., 0]
        bare &= (lum > 40) & (lum < 250)      # skip shadow and blown specular
        if bare.sum() > 200:
            h_asset = hue_deg(lab[bare])
            h_ref = float(hue_deg(hex_lab(coat_hex)[None, :])[0])
            d = (h_asset - h_ref + 180) % 360 - 180
            res['hue_shift_deg'] = round(float(np.median(d)), 2)
            ref = hex_lab(coat_hex)
            s_ref = np.hypot(ref[1] - 128, ref[2] - 128) / max(ref[0], 1)
            px = lab[bare]
            s_asset = np.median(np.hypot(px[:, 1] - 128, px[:, 2] - 128) / np.maximum(px[:, 0], 1))
            res['sat_ratio'] = round(float(s_asset / s_ref), 3)
    ok = worst >= MIN_TILE_PASS and p5 >= bar5 and caught is True
    if 'hue_shift_deg' in res:
        ok = ok and abs(res['hue_shift_deg']) <= MAX_HUE_SHIFT and res['sat_ratio'] >= MIN_SAT_RATIO
    res.update(worst_tile=round(worst, 3), p5_tile=round(p5, 3), bar_p5=bar5, pass_=bool(ok))
    if debug:
        vis = img.copy()
        for y, x, v in s:
            col = (0, 200, 0) if v >= MIN_TILE_PASS else (0, 0, 255)
            cv2.rectangle(vis, (x, y), (x + TILE - 1, y + TILE - 1), col, 1)
        cv2.imwrite(debug, vis)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', required=True)
    ap.add_argument('--aov', required=True)
    ap.add_argument('--asset', required=True, nargs='+')
    ap.add_argument('--coat', default=None, help='faixa coating hex, e.g. #FFE81A')
    ap.add_argument('--ink', default='#121014')
    ap.add_argument('--film', action='store_true')
    ap.add_argument('--json')
    ap.add_argument('--debug')
    a = ap.parse_args()
    out = [check(a.master, a.aov, p, a.coat, a.ink, a.film, a.debug) for p in a.asset]
    for r in out:
        r['pass'] = r.pop('pass_')
    txt = json.dumps(out, indent=2, ensure_ascii=False)
    print(txt)
    if a.json:
        open(a.json, 'w').write(txt)
    sys.exit(0 if all(r['pass'] for r in out) else 1)


if __name__ == '__main__':
    main()
