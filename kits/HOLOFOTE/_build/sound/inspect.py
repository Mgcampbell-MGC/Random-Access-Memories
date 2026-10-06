#!/usr/bin/env python
"""HOLOFOTE · inspect.py — "ears" for a team that cannot hear.

Prints peak / true-peak / RMS / LUFS / duration and the onset times of an audio file, and writes a PNG with the
waveform (top), a log-frequency spectrogram (middle) and an RMS envelope in dBFS (bottom).

    python inspect.py file.wav [file2.ogg ...] [--png out.png] [--grid png_dir]
"""
import argparse, os, sys
import numpy as np
import soundfile as sf

def load(path):
    x, sr = sf.read(path, always_2d=True, dtype="float64")
    return x, sr

def true_peak_db(x, sr):
    from scipy.signal import resample_poly
    up = resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(max(np.abs(up).max(), 1e-12))

def lufs(x, sr):
    import pyloudnorm as pyln
    if x.shape[0] < int(0.4 * sr):
        return float("nan")
    try:
        return pyln.Meter(sr).integrated_loudness(x)
    except Exception:
        return float("nan")

def onsets(x, sr):
    import librosa
    y = x.mean(axis=1).astype(np.float32)
    o = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=False, hop_length=128)
    return o

def stats(path):
    x, sr = load(path)
    d = x.shape[0] / sr
    pk = 20 * np.log10(max(np.abs(x).max(), 1e-12))
    rms = 20 * np.log10(max(np.sqrt((x ** 2).mean()), 1e-12))
    return dict(path=path, sr=sr, ch=x.shape[1], dur=d, peak=pk, tp=true_peak_db(x, sr), rms=rms, lufs=lufs(x, sr),
                onsets=onsets(x, sr)), x, sr

def plot(x, sr, title, out, marks=()):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    y = x.mean(axis=1)
    t = np.arange(len(y)) / sr
    fig, ax = plt.subplots(3, 1, figsize=(12, 7.5), sharex=True, gridspec_kw=dict(height_ratios=[1, 1.6, 0.8]))
    ax[0].plot(t, y, lw=0.4, color="#111")
    ax[0].set_ylim(-1.05, 1.05); ax[0].set_ylabel("amp"); ax[0].set_title(title, fontsize=10)
    n = 1024 if sr >= 32000 else 512
    ax[1].specgram(y + 1e-9, NFFT=n, Fs=sr, noverlap=n * 3 // 4, cmap="magma", vmin=-130, vmax=-20)
    ax[1].set_yscale("symlog", linthresh=200); ax[1].set_ylim(30, sr / 2); ax[1].set_ylabel("Hz")
    hop = max(1, sr // 200)
    fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (0, hop * 2)), hop * 2)[::hop]
    env = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    ax[2].plot(np.arange(len(env)) * hop / sr, env, lw=0.8, color="#c60")
    ax[2].set_ylim(-90, 0); ax[2].set_ylabel("RMS dBFS"); ax[2].set_xlabel("s"); ax[2].grid(alpha=0.3)
    for m in marks:
        for a in ax:
            a.axvline(m, color="#09f", lw=0.6, alpha=0.7)
    fig.tight_layout(); fig.savefig(out, dpi=80); plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--png", help="PNG path (single file)")
    ap.add_argument("--grid", help="write one PNG per file into this dir")
    ap.add_argument("--no-onsets", action="store_true")
    a = ap.parse_args()
    for f in a.files:
        s, x, sr = stats(f)
        on = s["onsets"]
        print(f"{os.path.basename(f):40s} {s['sr']}Hz {s['ch']}ch {s['dur']:6.3f}s peak {s['peak']:6.1f} TP {s['tp']:6.1f} "
              f"RMS {s['rms']:6.1f} LUFS {s['lufs']:6.1f}" + ("" if a.no_onsets else f"  onsets[{len(on)}] " + " ".join(f"{v:.3f}" for v in on[:14])))
        out = a.png if (a.png and len(a.files) == 1) else (os.path.join(a.grid, os.path.splitext(os.path.basename(f))[0] + ".png") if a.grid else None)
        if out:
            os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
            plot(x, sr, os.path.basename(f), out, () if a.no_onsets else on)

if __name__ == "__main__":
    main()
