#!/usr/bin/env python
"""HOLOFOTE · onsets.py — the exact transient times of an audio file, for snapping type slams to sound.

Method: librosa onset detection (spectral flux, hop 128 samples = 2,7 ms at 48 kHz) finds each event; each one is
then refined to the SAMPLE: inside a −35/+15 ms window around librosa's estimate, on a causal 1,5 ms peak-hold envelope of
the signal high-passed at 1,5 kHz (where transients live), the onset is the first sample of the rise that reaches 25 % of
the way from the local background level to the event's peak (so a strike on a still-ringing bell is placed right).
The file is padded with 50 ms of silence first, so an event on sample 0 is found at 0,000.
Events quieter than `--floor` dB below the file's peak are dropped (reverb tails, noise).

    python onsets.py file.wav                 # table: seconds, frame at 24 fps, level
    python onsets.py file.wav --fps 24 --json out.json
    python onsets.py file.wav --snap 204 210  # check: are frames 204 and 210 within ±1 frame of an onset?

As a module:  from onsets import onsets;  onsets("x.wav") -> [t0, t1, ...] (seconds, float)
"""
from __future__ import annotations

import argparse, json, sys
import numpy as np
import soundfile as sf


def _load(path):
    x, sr = sf.read(path, always_2d=True, dtype="float64")
    return x.mean(axis=1), sr


def onsets(path: str, floor_db: float = 40.0, min_gap: float = 0.025, delta: float = 0.06, detail: bool = False):
    import librosa
    from scipy import signal
    y, sr = _load(path)
    if len(y) == 0:
        return []
    pad = int(0.05 * sr)                      # 50 ms of silence in front, so an event on sample 0 is still seen
    y = np.concatenate([np.zeros(pad), y])
    hop = 128
    est = librosa.onset.onset_detect(y=y.astype(np.float32), sr=sr, units="samples", hop_length=hop,
                                     backtrack=False, delta=delta, wait=max(1, int(min_gap * sr / hop)))
    # transients live in the highs: refine on a 1,5 kHz high-passed, 0,5 ms-smoothed envelope
    hpf = signal.sosfilt(signal.butter(2, 1500, "highpass", fs=sr, output="sos"), y)
    # causal 1,5 ms peak-hold (bridges the zero-crossings of a ringing signal without moving an onset earlier)
    from scipy.ndimage import maximum_filter1d
    kh = max(2, int(0.0015 * sr))
    env = maximum_filter1d(np.abs(hpf), size=kh, origin=(kh - 1) // 2)
    gpk = env.max() + 1e-12
    out = []
    last = -1e9
    for e in est:
        a = int(max(0, e - 0.035 * sr, (last + 0.010) * sr + pad))
        b = min(len(env), int(e + 0.015 * sr))
        if b - a < 8:
            continue
        w = env[a:b]
        ip = int(np.argmax(w))
        lp = w[ip]
        if 20 * np.log10(lp / gpk + 1e-12) < -floor_db:
            continue
        # background level just before the rise (a struck bell over its own ring, a clap over applause)
        pre = w[:max(1, ip - int(0.002 * sr))]
        base = float(np.percentile(pre, 20)) if len(pre) > 4 else 0.0
        thr = base + 0.25 * (lp - base)
        i = ip
        while i > 0 and w[i - 1] >= thr:
            i -= 1
        t = (a + i - pad) / sr
        if t - last < min_gap:
            continue
        last = t
        out.append((max(0.0, t), 20 * np.log10(lp / gpk + 1e-12)) if detail else max(0.0, t))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--floor", type=float, default=40.0, help="drop events more than this many dB under the peak")
    ap.add_argument("--json", help="write [{t_s, frame, frame_round, level_db}] here")
    ap.add_argument("--snap", type=int, nargs="*", help="frames to check against the onsets (±1 frame)")
    a = ap.parse_args()
    ev = onsets(a.file, floor_db=a.floor, detail=True)
    rows = [dict(t_s=round(t, 5), frame=round(t * a.fps, 3), frame_round=int(round(t * a.fps)), level_db=round(l, 1))
            for t, l in ev]
    print(f"{a.file}: {len(rows)} onsets  (fps {a.fps:g})")
    for r in rows:
        print(f"  t {r['t_s']:9.5f} s   frame {r['frame']:8.3f} (≈ f{r['frame_round']})   {r['level_db']:6.1f} dB")
    if a.snap:
        fr = np.array([r["frame"] for r in rows])
        bad = 0
        for f in a.snap:
            d = (fr - f) if len(fr) else np.array([np.inf])
            k = int(np.argmin(np.abs(d)))
            ok = abs(d[k]) <= 1.0
            bad += not ok
            print(f"  snap f{f}: nearest onset f{fr[k]:.3f} (Δ {d[k]:+.3f} f) {'OK' if ok else 'FORA ±1 f'}")
        if bad:
            sys.exit(2)
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
