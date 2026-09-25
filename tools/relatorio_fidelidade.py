"""Relatório de Fidelidade — checks that a delivered asset shows the approved packaging exactly.

Usage:
    python3 relatorio_fidelidade.py APPROVED.png ASSET [ASSET ...] [--every N] [--json out.json]

APPROVED.png is the brand's approved packshot as a cutout with an alpha channel (the flat front
face works best). ASSET may be an image or a video. For each asset the label is located by SIFT
feature matching, warped back onto the approved packshot, and compared tile by tile on a band-pass
image, so a single misspelled word shows up as one bad tile instead of being averaged away.

Pass rule (calibrated 25 Sep 2026 on one real tube, see O_LANCAMENTO.md Part G):
    worst tile >= 0.80 AND 5th-percentile tile >= 0.95.
Exact composites scored 0.96/0.99 as stills and >=0.87/0.96 in every checked frame of a compressed
film; generated labels with 2 and 4 spelling errors scored 0.39/0.82 and 0.00/0.49.
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

    def score(self, img):
        k, d = self.sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
        if d is None:
            return {"found": False}
        good = [m for m, n in self.matcher.knnMatch(self.dr, d, k=2) if m.distance < 0.75 * n.distance]
        if len(good) < 12:
            return {"found": False, "matches": len(good)}
        src = np.float32([self.kr[m.queryIdx].pt for m in good])
        dst = np.float32([k[m.trainIdx].pt for m in good])
        H, inliers = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
        if H is None:
            return {"found": False, "matches": len(good)}
        h, w = self.ref.shape[:2]
        warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
        B = bandpass(warped.astype(np.float32))
        scores = []
        for y, x in self.tiles:
            a = self.R[y:y + TILE, x:x + TILE].ravel()
            b = B[y:y + TILE, x:x + TILE].ravel()
            a = a - a.mean()
            b = b - b.mean()
            scores.append(float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-9)))
        s = np.array(scores)
        worst = float(s.min())
        p5 = float(np.percentile(s, 5))
        return {
            "found": True,
            "inliers": int(inliers.sum()),
            "tiles": len(s),
            "worst_tile": round(worst, 3),
            "p5_tile": round(p5, 3),
            "pass": worst >= MIN_TILE_PASS and p5 >= P5_TILE_PASS,
        }


def check_asset(checker, path, every):
    img = cv2.imread(path)
    if img is not None:
        r = checker.score(img)
        return {"asset": path, "type": "image", **r, "pass": r.get("pass", False)}
    cap = cv2.VideoCapture(path)
    frames, results, i = 0, [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % every == 0:
            results.append(checker.score(fr))
        i += 1
    frames = i
    if not results:
        return {"asset": path, "type": "unreadable", "pass": False}
    found = [r for r in results if r.get("found")]
    worst = min((r["worst_tile"] for r in found), default=0.0)
    p5 = min((r["p5_tile"] for r in found), default=0.0)
    return {
        "asset": path,
        "type": "video",
        "frames": frames,
        "frames_checked": len(results),
        "frames_without_label": len(results) - len(found),
        "worst_tile": worst,
        "worst_p5_tile": p5,
        "pass": bool(found) and all(r["pass"] for r in found),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("approved")
    ap.add_argument("assets", nargs="+")
    ap.add_argument("--every", type=int, default=6, help="check every Nth video frame")
    ap.add_argument("--json")
    args = ap.parse_args()
    checker = Checker(args.approved)
    report = [check_asset(checker, a, args.every) for a in args.assets]
    for r in report:
        print(f"{'APROVADA ' if r['pass'] else 'REPROVADA'}  {r['asset']}  {json.dumps({k: v for k, v in r.items() if k not in ('asset', 'pass')})}")
    if args.json:
        with open(args.json, "w") as f:
            json.dump(report, f, indent=1, ensure_ascii=False)
    sys.exit(0 if all(r["pass"] for r in report) else 1)


if __name__ == "__main__":
    main()
