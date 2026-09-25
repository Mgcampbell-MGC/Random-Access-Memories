"""Compor — lays the brand's real packshot over the blank placeholder in a generated scene.

Usage:
    python3 compor.py CENA.png EMBALAGEM.png SAIDA.png [--matiz 210] [--tol 18] [--escala 1.0] [--dx 0] [--dy 0]

CENA.png is a generated scene in which the product is a BLANK PLACEHOLDER in one flat, saturated chroma colour
(default a pure blue, hue 210 degrees) that appears nowhere else in the scene: body AND cap, no text, no logo.
EMBALAGEM.png is the brand's approved packshot as a cutout with an alpha channel. The generator never sees it.

The script finds the placeholder, fits the packshot inside it (uniform scale, so the label is never stretched),
rotates it to the placeholder's tilt, re-lights it from the placeholder's own shading, puts anything that sat in
front of the placeholder (fingers, a leaf, a towel edge) back on top, and paints out leftover placeholder pixels.

Writes three files:
    SAIDA.png          the composite
    SAIDA.hidden.png   white where the packaging is covered (read by relatorio_fidelidade.py and filme.py)
    SAIDA.alpha.png    the packaging layer as placed (read by filme.py)

Only the scene's pixels are changed around the pack; the pack's own pixels are resampled once and re-lit with a
smooth brightness field, which the fidelity check tolerates by design. Tested 25 Sep 2026 on one real tube, in a
hand with fingers over the label (O_LANCAMENTO.md Part G2). Check every output with relatorio_fidelidade.py.
"""
import argparse
import sys

import cv2
import numpy as np


def placeholder_mask(scene, hue_deg, tol):
    hsv = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)
    h = hsv[..., 0].astype(np.int32) * 2  # OpenCV hue is 0-179
    d = np.minimum(np.abs(h - hue_deg), 360 - np.abs(h - hue_deg))
    m = ((d <= tol) & (hsv[..., 1] > 80) & (hsv[..., 2] > 30)).astype(np.uint8)
    # Wider net for painting out: the placeholder's own shadow side and soft edges.
    loose = ((d <= tol + 8) & (hsv[..., 1] > 45) & (hsv[..., 2] > 12)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        sys.exit("no placeholder found: check --matiz (hue in degrees) and that the placeholder is one flat colour")
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[i, cv2.CC_STAT_AREA] < 0.002 * m.size:
        sys.exit("placeholder too small or not found")
    body = (lab == i).astype(np.uint8)
    # Everything the placeholder would cover if nothing were in front of it: its convex hull.
    cnts, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros_like(body)
    cv2.fillPoly(hull, [cv2.convexHull(np.vstack(cnts))], 1)
    # Glare and deep shadow on the placeholder are not something in front of it.
    glare = ((hsv[..., 1] < 50) & (hsv[..., 2] > 170)) | ((d <= 2 * tol) & (hsv[..., 1] > 25)) | (hsv[..., 2] < 45)
    return body, hull, loose, glare


def axis(mask):
    """Centre, tilt (degrees, 0 = upright) and upright width/height of a blob, from its principal axis.

    A tube tapers, so a minimum-area rectangle tilts to hug the slanted side; the principal axis of a
    symmetric shape does not.
    """
    m = cv2.moments(mask.astype(np.uint8), binaryImage=True)
    cx, cy = m["m10"] / m["m00"], m["m01"] / m["m00"]
    th = 0.5 * np.degrees(np.arctan2(2 * m["mu11"], m["mu20"] - m["mu02"]))  # major axis vs x
    tilt = ((th - 90 + 90) % 180) - 90  # 0 when the major axis is vertical
    ys, xs = np.where(mask > 0)
    r = np.radians(tilt)
    u = (xs - cx) * np.cos(r) + (ys - cy) * np.sin(r)
    v = -(xs - cx) * np.sin(r) + (ys - cy) * np.cos(r)
    return cx + 0.5 * (u.max() + u.min()) * np.cos(r) - 0.5 * (v.max() + v.min()) * np.sin(r), \
        cy + 0.5 * (u.max() + u.min()) * np.sin(r) + 0.5 * (v.max() + v.min()) * np.cos(r), \
        tilt, u.max() - u.min() + 1, v.max() - v.min() + 1


def fit(hull, pack_alpha, escala, ajuste):
    cx, cy, tilt, w, h = axis(hull)
    ys, xs = np.where(pack_alpha > 0.5)
    pw, ph = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    k = {"largura": w / pw, "altura": h / ph}.get(ajuste, min(w / pw, h / ph)) * escala  # never stretch
    pcx, pcy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    A = cv2.getRotationMatrix2D((pcx, pcy), -tilt, k)
    A[:, 2] += (cx - pcx, cy - pcy)
    return A, k, tilt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cena")
    ap.add_argument("embalagem")
    ap.add_argument("saida")
    ap.add_argument("--matiz", type=float, default=210, help="placeholder hue in degrees (blue 210, green 120)")
    ap.add_argument("--tol", type=float, default=18)
    ap.add_argument("--escala", type=float, default=1.0, help="multiply the fitted size")
    ap.add_argument("--ajuste", default="dentro", choices=["dentro", "largura", "altura"],
                    help="fit inside the placeholder (default), or match its width or its height")
    ap.add_argument("--sem-oclusao", action="store_true", help="nothing is in front of the pack: skip occluders")
    ap.add_argument("--dx", type=float, default=0)
    ap.add_argument("--dy", type=float, default=0)
    a = ap.parse_args()

    scene = cv2.imread(a.cena)
    pack = cv2.imread(a.embalagem, cv2.IMREAD_UNCHANGED)
    if scene is None or pack is None or pack.ndim != 3 or pack.shape[2] != 4:
        sys.exit("need a scene image and a packshot PNG with an alpha channel")
    H, W = scene.shape[:2]
    body, hull, anychroma, glare = placeholder_mask(scene, a.matiz, a.tol)

    pa = pack[..., 3].astype(np.float32) / 255
    A, k, ang = fit(hull, pa, a.escala, a.ajuste)
    A[:, 2] += (a.dx, a.dy)
    prod = cv2.warpAffine(pack[..., :3].astype(np.float32), A, (W, H), flags=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC)
    alpha = np.clip(cv2.warpAffine(pa, A, (W, H), flags=cv2.INTER_LINEAR), 0, 1)

    # Re-light the pack from the placeholder's own low-frequency shading (normalised convolution: only
    # placeholder pixels are averaged, so a finger's shadow or the background never darkens the label).
    L = cv2.cvtColor(scene, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
    bm = body.astype(np.float32)
    s = max(4.0, 0.04 * max(H, W))
    low = cv2.GaussianBlur(L * bm, (0, 0), s) / np.maximum(cv2.GaussianBlur(bm, (0, 0), s), 1e-3)
    ratio = np.clip(low / np.median(L[body > 0]), 0.6, 1.35)
    lab = cv2.cvtColor(np.clip(prod, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 0] = np.clip(lab[..., 0] * np.where(alpha > 0, ratio, 1), 0, 255)
    prod = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    # Occluders: inside the placeholder's hull and the placed pack, but not placeholder-coloured.
    near = cv2.dilate(anychroma, np.ones((5, 5), np.uint8))
    occ = ((hull > 0) & (alpha > 0.1) & (near == 0) & ~glare).astype(np.uint8)
    if a.sem_oclusao:
        occ[:] = 0
    occ = cv2.morphologyEx(occ, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    occ = cv2.GaussianBlur(occ.astype(np.float32), (0, 0), 1.2)

    # Paint out placeholder pixels the real pack does not cover.
    rem = ((cv2.dilate(anychroma, np.ones((3, 3), np.uint8)) > 0) & (alpha < 0.5)).astype(np.uint8) * 255
    base = cv2.inpaint(scene, cv2.dilate(rem, np.ones((3, 3), np.uint8)), 5, cv2.INPAINT_TELEA).astype(np.float32)

    lay = alpha * (1 - occ)
    out = base * (1 - lay[..., None]) + prod * lay[..., None]
    stem = a.saida.rsplit(".", 1)[0]
    cv2.imwrite(a.saida, np.clip(out, 0, 255).astype(np.uint8))
    cv2.imwrite(stem + ".hidden.png", (np.clip(occ * (alpha > 0.1), 0, 1) * 255).astype(np.uint8))
    cv2.imwrite(stem + ".alpha.png", (alpha * 255).astype(np.uint8))
    left = int(((anychroma > 0) & (alpha < 0.5)).sum())
    print(f"escala {k:.3f}  inclinação {ang:.1f}°  pixels cobertos {int((occ > 0.5).sum())}  "
          f"placeholder pintado fora {left}")


if __name__ == "__main__":
    main()
