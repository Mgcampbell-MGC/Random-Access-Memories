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


def bandpass(img, s1=1.2, s2=5.0):
    g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    return cv2.GaussianBlur(g, (0, 0), s1) - cv2.GaussianBlur(g, (0, 0), s2)


class Checker:
    def __init__(self, approved_path):
        cut = cv2.imread(approved_path, cv2.IMREAD_UNCHANGED)
        if cut is None or cut.ndim != 3 or cut.shape[2] != 4:
            sys.exit("approved packshot must be a PNG with an alpha channel")
        self.ref = cut[..., :3]
        # Only judge the label interior: the edges of a cutout never match a new background.
        self.mask = cv2.erode((cut[..., 3] > 250).astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
        self.sift = cv2.SIFT_create(nfeatures=4000)
        self.matcher = cv2.BFMatcher()
        self.kr, self.dr = self.sift.detectAndCompute(cv2.cvtColor(self.ref, cv2.COLOR_BGR2GRAY), None)
        self.R = bandpass(self.ref.astype(np.float32))
        h, w = self.ref.shape[:2]
        # Textured tiles only: blank areas carry no text and would pass anything.
        self.tiles = [
            (y, x)
            for y in range(0, h - TILE + 1, TILE // 2)
            for x in range(0, w - TILE + 1, TILE // 2)
            if self.mask[y:y + TILE, x:x + TILE].mean() > 0.95 and self.R[y:y + TILE, x:x + TILE].std() > 4
        ]

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
        best = None
        for method, thr in ((cv2.RANSAC, 3.0), (cv2.USAC_MAGSAC, 2.0), (cv2.RANSAC, 1.5)):
            H, inliers = cv2.findHomography(src, dst, method, thr)
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
            hid = cv2.warpPerspective(hidden, H, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR) > 127
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
        return {
            "found": True,
            "tiles": len(s),
            "hidden_share": round(hidden_share, 3),
            "worst_tile": round(worst, 3),
            "p5_tile": round(p5, 3),
            "pass": worst >= MIN_TILE_PASS and p5 >= P5_TILE_PASS and hidden_share <= MAX_HIDDEN,
        }

def check_asset(checker, path, every, control=True):
    img = cv2.imread(path)
    if img is not None:
        hidden = cv2.imread(path.rsplit(".", 1)[0] + ".hidden.png", cv2.IMREAD_GRAYSCALE)
        r = checker.score(img, hidden)
        H = r.pop("_H", None)
        if control and H is not None and r.get("pass"):
            r.update(checker.control(img, H, hidden))
            if not r["control_caught"]:
                r["pass"] = False  # the check was not sensitive enough on this asset: a human must look
        return {"asset": path, "type": "image", **r, "pass": r.get("pass", False)}
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
                             and r["hidden_share"] <= MAX_HIDDEN)
            results.append(r)
        i += 1
    frames = i
    if not results:
        return {"asset": path, "type": "unreadable", "pass": False}
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
        "asset": path,
        "type": "video",
        **ctrl,
        "frames": frames,
        "frames_checked": len(results),
        "frames_without_label": len(results) - len(found),
        "worst_tile": worst,
        "worst_p5_tile": p5,
        "max_hidden_share": max((r.get("hidden_share", 0) for r in found), default=0.0),
        "pass": bool(found) and all(r["pass"] for r in found) and ctrl.get("control_caught", not control),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("approved")
    ap.add_argument("assets", nargs="+")
    ap.add_argument("--every", type=int, default=1, help="check every Nth video frame (1 = all; use 1 before delivery)")
    ap.add_argument("--json")
    ap.add_argument("--sem-controle", action="store_true", help="skip the planted-error control on stills")
    args = ap.parse_args()
    checker = Checker(args.approved)
    report = [check_asset(checker, a, args.every, not args.sem_controle) for a in args.assets]
    for r in report:
        print(f"{'APROVADA ' if r['pass'] else 'REPROVADA'}  {r['asset']}  {json.dumps({k: v for k, v in r.items() if k not in ('asset', 'pass')})}")
    if args.json:
        with open(args.json, "w") as f:
            json.dump(report, f, indent=1, ensure_ascii=False)
    sys.exit(0 if all(r["pass"] for r in report) else 1)


if __name__ == "__main__":
    main()
