"""Relatório de Fidelidade — checks that a delivered asset shows the approved packaging exactly.

Usage:
    python3 relatorio_fidelidade.py APPROVED.png ASSET [ASSET ...] [--every N] [--json out.json]

APPROVED.png is the brand's approved packshot as a cutout with an alpha channel (the flat front
face works best). ASSET may be an image or a video. If ASSET has a sibling mask named
<asset>.hidden.png (white = packaging deliberately covered, e.g. by fingers), covered tiles are
excluded and reported: hidden is allowed, altered never. For a video the sibling is <asset>.hidden.mp4,
read frame by frame (compor.py and filme.py write both). For each asset the label is located by SIFT
feature matching, warped back onto the approved packshot, and compared tile by tile on a band-pass
image, so a single misspelled word shows up as one bad tile instead of being averaged away.

Every still that passes is also given a NEGATIVE CONTROL: one lettered patch of its label is mirrored in a copy
and re-checked, and the still passes only if the check catches the planted error ("control_caught").

Colour: the median hue+chroma shift across the visible label (lightness excluded, because the scene re-lights the
pack) must stay within --tolerancia-cor, default 2,0. Every film must be encoded BT.709-converted AND BT.709-tagged
(codificar.py): a film converted BT.601 but tagged BT.709 shows the pack's colours shifted on phones.

Pass rule (calibrated 25 Sep 2026 on one real tube, see O_LANCAMENTO.md Part G):
    worst tile >= 0.80 AND 5th-percentile tile >= 0.95.
Exact composites scored 0.96/0.99 as stills and >=0.87/0.96 in every checked frame of a compressed
film; generated labels with 2 and 4 spelling errors scored 0.39/0.82 and 0.00/0.49.
Films (recalibrated 25 Sep 2026): worst tile >= 0.80 in EVERY frame AND 5th-percentile >= 0.93. Five exact films of
the same tube, every frame checked, bottomed at a 5th percentile of 0.945-0.957 (resampling each frame softens fine
print a little); the worst-tile rule, which is the one a wrong letter trips (a planted one-patch error scored 0.28), is
unchanged. Each film also gets the planted-error control on its middle frame.
Recalibrate on each new packaging type before relying on the thresholds.
"""
import argparse
import json
import sys

import cv2
import numpy as np

TILE = 24
MIN_TILE_PASS = 0.80
P5_TILE_PASS = 0.95
P5_FILM_PASS = 0.93  # films resample the pack every frame; see the calibration note above
MAX_HIDDEN = 0.35  # above this share of the label covered, the asset needs a human look
# Colour: median shift of hue+chroma (ΔC in CIELAB a,b units) across the visible label, lightness excluded because
# the scene legitimately re-lights the pack. Calibrated 26 Sep 2026: exact stills 0,2–0,4, correctly encoded films
# ≈0,8, a film converted BT.601 but tagged BT.709 3,1–3,9, AI-regenerated labels 8–14.
MAX_COLOR_DRIFT = 2.0


def bandpass(img, s1=1.2, s2=5.0):
    g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    return cv2.GaussianBlur(g, (0, 0), s1) - cv2.GaussianBlur(g, (0, 0), s2)


class Checker:
    def __init__(self, approved_path=None, cut=None):
        if cut is None:
            cut = cv2.imread(approved_path, cv2.IMREAD_UNCHANGED)
            if cut is None or cut.ndim != 3 or cut.shape[2] != 4:
                sys.exit("approved packshot must be a PNG with an alpha channel")
        self.cut = cut
        self._scaled = {}
        self.ref = cut[..., :3]
        # Only judge the label interior: the edges of a cutout never match a new background.
        self.mask = cv2.erode((cut[..., 3] > 250).astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
        self.sift = cv2.SIFT_create(nfeatures=4000)
        self.matcher = cv2.BFMatcher()
        self.kr, self.dr = self.sift.detectAndCompute(cv2.cvtColor(self.ref, cv2.COLOR_BGR2GRAY), None)
        self.R = bandpass(self.ref.astype(np.float32))
        self.refLab = cv2.cvtColor(self.ref, cv2.COLOR_BGR2LAB).astype(np.float32)
        self.max_color = MAX_COLOR_DRIFT
        h, w = self.ref.shape[:2]
        # Colour is judged on every interior tile, flat ones included.
        self.ctiles = [
            (y, x)
            for y in range(0, h - TILE + 1, TILE // 2)
            for x in range(0, w - TILE + 1, TILE // 2)
            if self.mask[y:y + TILE, x:x + TILE].mean() > 0.95
        ]
        # Textured tiles only: blank areas carry no text and would pass anything.
        self.tiles = [
            (y, x)
            for y in range(0, h - TILE + 1, TILE // 2)
            for x in range(0, w - TILE + 1, TILE // 2)
            if self.mask[y:y + TILE, x:x + TILE].mean() > 0.95 and self.R[y:y + TILE, x:x + TILE].std() > 4
        ]

    def pack_scale(self, img):
        """How big the pack shows in img relative to the approved packshot (1.0 = same size), or None."""
        k, d = self.sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
        if d is None:
            return None
        good = [m for m, n in self.matcher.knnMatch(self.dr, d, k=2) if m.distance < 0.75 * n.distance]
        if len(good) < 12:
            return None
        src = np.float32([self.kr[m.queryIdx].pt for m in good])
        dst = np.float32([k[m.trainIdx].pt for m in good])
        A, _ = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
        return None if A is None else float(np.hypot(A[0, 0], A[1, 0]))

    def at_scale(self, s):
        """A checker whose approved packshot is shrunk to scale s.
        Why (measured 4 Oct 2026): the thresholds were calibrated with the pack shown at about the packshot's own
        size. A brand's packshot is usually far larger than the pack appears in a piece, and comparing in the
        packshot's resolution asks the piece for fine print it cannot hold: an exact composite at scale 0,51 scored
        a worst tile of 0,75 and failed. Shrinking the reference to the piece's scale restores the calibrated
        condition; it never enlarges, and it rounds DOWN so the reference is never sharper than the piece."""
        if s is None or s >= 0.85:
            return self
        b = max(0.10, np.floor(s * 20) / 20)
        if b not in self._scaled:
            h, w = self.cut.shape[:2]
            small = cv2.resize(self.cut, (max(1, int(round(w * b))), max(1, int(round(h * b)))),
                               interpolation=cv2.INTER_AREA)
            c = Checker(cut=small)
            c.max_color = self.max_color
            self._scaled[b] = c
        return self._scaled[b]

    def score(self, img, hidden=None):
        k, d = self.sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
        if d is None:
            return {"found": False}
        good = [m for m, n in self.matcher.knnMatch(self.dr, d, k=2) if m.distance < 0.75 * n.distance]
        if len(good) < 12:
            return {"found": False, "matches": len(good)}
        src = np.float32([self.kr[m.queryIdx].pt for m in good])
        dst = np.float32([k[m.trainIdx].pt for m in good])
        # Alignment can occasionally lock onto a wrong fit and fail a frame whose label is intact. A wrong fit can
        # only LOWER the scores, and a misspelled letter cannot be aligned away by one global homography, so
        # retrying stricter fits and keeping the best is safe.
        # A composited pack is placed by a similarity (compor.py, the film layer), so a full homography fitted
        # from label features alone can bend the far ends of the pack: measured 28 Sep 2026, a shelf composite
        # whose placement matched the master exactly failed on its base because the homography's perspective
        # terms, fitted on the label, drifted 10-15 px by the foot. Similarity and affine fits are tried too.
        fits = []
        for method, thr in ((cv2.RANSAC, 3.0), (cv2.USAC_MAGSAC, 2.0), (cv2.RANSAC, 1.5)):
            fits.append(cv2.findHomography(src, dst, method, thr))
        for est in (cv2.estimateAffinePartial2D, cv2.estimateAffine2D):
            A, inl = est(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
            fits.append((None if A is None else np.vstack([A, [0, 0, 1]]), inl))
        best = None
        for H, inliers in fits:
            if H is None:
                continue
            r = self._compare(img, H, hidden)
            r["inliers"] = int(inliers.sum())
            r["_H"] = H
            if best is None or (r["pass"], r.get("p5_tile", -1)) > (best["pass"], best.get("p5_tile", -1)):
                best = r
            if best["pass"]:
                break
        return best or {"found": False, "matches": len(good)}

    def control(self, img, H, hidden=None):
        """Negative control on THIS asset: mirror one lettered patch of the label in a copy, re-check, and
        report whether the check caught it. A pass that could not have failed proves nothing."""
        h, w = self.ref.shape[:2]
        free = [(y, x) for y, x in self.tiles]
        y, x = max(free, key=lambda t: self.R[t[0]:t[0] + TILE, t[1]:t[1] + TILE].std())
        warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
        patch = warped.copy()
        patch[y:y + TILE, x:x + TILE] = warped[y:y + TILE, x:x + TILE][:, ::-1]
        m = np.zeros((h, w), np.uint8)
        m[y:y + TILE, x:x + TILE] = 255
        back = cv2.warpPerspective(patch, H, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
        mb = cv2.warpPerspective(m, H, (img.shape[1], img.shape[0]), flags=cv2.INTER_NEAREST) > 0
        altered = img.copy()
        altered[mb] = back[mb]
        r = self.score(altered, hidden)
        # Caught means the WORST-TILE rule fired, the rule a single wrong letter must trip; failing only on the
        # 5th percentile would not show the check can see one letter.
        return {"control_caught": r.get("worst_tile", 1.0) < MIN_TILE_PASS, "control_worst_tile": r.get("worst_tile")}

    def _compare(self, img, H, hidden):
        h, w = self.ref.shape[:2]
        warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
        B = bandpass(warped.astype(np.float32))
        hid = None
        if hidden is not None:
            # A pixel even partly covered (a finger's soft edge) is covered: judging it would compare skin to label.
            hid = cv2.warpPerspective(hidden, H, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR) > 20
        scores, n_hidden = [], 0
        for y, x in self.tiles:
            if hid is not None and hid[y:y + TILE, x:x + TILE].mean() > 0.10:
                n_hidden += 1
                continue
            a = self.R[y:y + TILE, x:x + TILE].ravel()
            b = B[y:y + TILE, x:x + TILE].ravel()
            a = a - a.mean()
            b = b - b.mean()
            scores.append(float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-9)))
        s = np.array(scores)
        hidden_share = n_hidden / len(self.tiles)
        if not len(s):
            return {"found": True, "hidden_share": 1.0, "pass": False}
        worst = float(s.min())
        p5 = float(np.percentile(s, 5))
        lab = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB).astype(np.float32)
        drift = []
        for y, x in self.ctiles:
            if hid is not None and hid[y:y + TILE, x:x + TILE].mean() > 0.10:
                continue
            a = self.refLab[y:y + TILE, x:x + TILE].reshape(-1, 3).mean(0)
            b = lab[y:y + TILE, x:x + TILE].reshape(-1, 3).mean(0)
            drift.append(float(np.hypot(a[1] - b[1], a[2] - b[2])))
        color = float(np.median(drift)) if drift else 0.0
        return {
            "found": True,
            "tiles": len(s),
            "hidden_share": round(hidden_share, 3),
            "worst_tile": round(worst, 3),
            "p5_tile": round(p5, 3),
            "color_drift": round(color, 2),
            "pass": (worst >= MIN_TILE_PASS and p5 >= P5_TILE_PASS and hidden_share <= MAX_HIDDEN
                     and color <= self.max_color),
        }

def check_asset(checker, path, every, control=True):
    img = cv2.imread(path)
    if img is not None:
        hidden = cv2.imread(path.rsplit(".", 1)[0] + ".hidden.png", cv2.IMREAD_GRAYSCALE)
        s = checker.pack_scale(img)
        # First at the packshot's own size, exactly as calibrated; then, only if that fails and the pack shows
        # smaller, at the piece's own size (see Checker.at_scale). Each path carries its own planted-error control,
        # so a pass on either still had to catch a deliberately wrong patch. Measured 4 Oct 2026: on a small master
        # (Climate, 916 px) the full-size path passes a piece at scale 0,45 that the shrunk path cannot test; on a
        # large one (ORVALHA, 1.900 px) only the shrunk path passes exact pieces.
        r = None
        for c, ref_scale in ((checker, 1.0), (checker.at_scale(s), s)):
            if r is not None and c is checker:
                break  # no smaller reference to try
            q = c.score(img, hidden)
            H = q.pop("_H", None)
            if control and H is not None and q.get("pass"):
                q.update(c.control(img, H, hidden))
                if not q["control_caught"]:
                    q["pass"] = False  # the check was not sensitive enough here: try the other path, or a human looks
            q["ref_scale"] = None if ref_scale is None else round(ref_scale, 3)
            if r is None or (q.get("pass", False), q.get("p5_tile", -1)) > (r.get("pass", False), r.get("p5_tile", -1)):
                r = q
            if r.get("pass"):
                break
        return {"asset": path, "type": "image", **r, "pass": r.get("pass", False)}
    cap = cv2.VideoCapture(path)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    scales = []
    for i in (0, n // 2, max(n - 1, 0)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if ok:
            scales.append(checker.pack_scale(fr))
    scales = [s for s in scales if s is not None]
    s = min(scales) if scales else None
    # Same two paths as for stills: the packshot's own size first, then the film's own size.
    r = check_video(checker, path, every, control)
    r["ref_scale"] = 1.0
    small = checker.at_scale(s)
    if not r["pass"] and small is not checker:
        q = check_video(small, path, every, control)
        q["ref_scale"] = round(s, 3)
        if (q["pass"], q.get("worst_p5_tile", -1)) >= (r["pass"], r.get("worst_p5_tile", -1)):
            r = q
    return {"asset": path, "type": "video", **r}


def check_video(checker, path, every, control):
    cap = cv2.VideoCapture(path)
    # filme.py writes <film>.hidden.mp4 when a hand covers the packaging; read it in lockstep.
    hcap = cv2.VideoCapture(path.rsplit(".", 1)[0] + ".hidden.mp4")
    has_h = hcap.isOpened()
    frames, results, i = 0, [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        hid = None
        if has_h:
            okh, hf = hcap.read()
            hid = cv2.cvtColor(hf, cv2.COLOR_BGR2GRAY) if okh else None
        if i % every == 0:
            r = checker.score(fr, hid)
            r.pop("_H", None)
            if r.get("found"):
                r["pass"] = (r["worst_tile"] >= MIN_TILE_PASS and r["p5_tile"] >= P5_FILM_PASS
                             and r["hidden_share"] <= MAX_HIDDEN and r["color_drift"] <= checker.max_color)
            results.append(r)
        i += 1
    frames = i
    if not results:
        return {"type": "unreadable", "pass": False}
    found = [r for r in results if r.get("found")]
    worst = min((r["worst_tile"] for r in found), default=0.0)
    p5 = min((r["p5_tile"] for r in found), default=0.0)
    ctrl = {}
    if control and found:
        cap = cv2.VideoCapture(path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames // 2)
        ok, fr = cap.read()
        hid = None
        if has_h:
            hcap = cv2.VideoCapture(path.rsplit(".", 1)[0] + ".hidden.mp4")
            hcap.set(cv2.CAP_PROP_POS_FRAMES, frames // 2)
            okh, hf = hcap.read()
            hid = cv2.cvtColor(hf, cv2.COLOR_BGR2GRAY) if okh else None
        r = checker.score(fr, hid) if ok else {}
        if r.get("_H") is not None:
            ctrl = checker.control(fr, r["_H"], hid)
    return {
        **ctrl,
        "frames": frames,
        "frames_checked": len(results),
        "frames_without_label": len(results) - len(found),
        "worst_tile": worst,
        "worst_p5_tile": p5,
        "max_hidden_share": max((r.get("hidden_share", 0) for r in found), default=0.0),
        "max_color_drift": max((r.get("color_drift", 0) for r in found), default=0.0),
        "pass": bool(found) and all(r["pass"] for r in found) and ctrl.get("control_caught", not control),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("approved")
    ap.add_argument("assets", nargs="+")
    ap.add_argument("--every", type=int, default=1, help="check every Nth video frame (1 = all; use 1 before delivery)")
    ap.add_argument("--json")
    ap.add_argument("--sem-controle", action="store_true", help="skip the planted-error control on stills")
    ap.add_argument("--tolerancia-cor", type=float, default=MAX_COLOR_DRIFT,
                    help="max median colour shift (ΔC); set from the Ficha do Produto")
    args = ap.parse_args()
    checker = Checker(args.approved)
    checker.max_color = args.tolerancia_cor
    report = [check_asset(checker, a, args.every, not args.sem_controle) for a in args.assets]
    for r in report:
        print(f"{'APROVADA ' if r['pass'] else 'REPROVADA'}  {r['asset']}  {json.dumps({k: v for k, v in r.items() if k not in ('asset', 'pass')})}")
    if args.json:
        with open(args.json, "w") as f:
            json.dump(report, f, indent=1, ensure_ascii=False)
    sys.exit(0 if all(r["pass"] for r in report) else 1)


if __name__ == "__main__":
    main()
