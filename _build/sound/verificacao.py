#!/usr/bin/env python
"""HOLOFOTE · verificacao.py — the visual proof of every delivered file (we check sound by looking at it).

For each family writes one PNG into 04_FILMES/som/verificacao/: per file a waveform with the onsets measured by
onsets.py (blue lines) and a log-frequency spectrogram; films also get a 400 ms loudness curve (LUFS-M).
"""
import glob, os, sys
import numpy as np
import soundfile as sf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dsp  # noqa: E402
import onsets as ON  # noqa: E402

SOM = os.path.abspath(os.path.join(HERE, "..", "..", "04_FILMES", "som"))
OUT = os.path.join(SOM, "verificacao")


def sheet(name, files, loud=False):
    n = len(files)
    fig, axs = plt.subplots(n, 2, figsize=(15, 1.75 * n + 0.4), squeeze=False,
                            gridspec_kw=dict(width_ratios=[1.0, 1.0]))
    for i, f in enumerate(files):
        x, sr = sf.read(f, always_2d=True)
        y = x.mean(1)
        t = np.arange(len(y)) / sr
        a = axs[i, 0]
        a.plot(t, y, lw=0.35, color="#111")
        a.set_ylim(-1, 1)
        for o in ON.onsets(f):
            a.axvline(o, color="#0a84ff", lw=0.5, alpha=0.7)
        if loud:
            k = dsp.kweight(x)
            w, hop = int(0.4 * sr), int(0.025 * sr)
            p = np.cumsum(np.vstack([np.zeros((1, 2)), k ** 2]), axis=0)
            idx = np.arange(0, max(1, len(k) - w), hop)
            L = -0.691 + 10 * np.log10(((p[idx + w] - p[idx]) / w).sum(1) + 1e-15)
            a2 = a.twinx()
            a2.plot((idx + w / 2) / sr, L, color="#d2461e", lw=1.0)
            a2.set_ylim(-60, 0)
            a2.tick_params(labelsize=6)
        li = dsp.integrated(x)
        a.set_title(f"{os.path.basename(f)}   {len(y)/sr:.3f} s   TP {dsp.true_peak(x):.1f} dBTP"
                    + ("" if np.isnan(li) else f"   {li:.1f} LUFS-I"), fontsize=7.5, loc="left")
        a.tick_params(labelsize=6)
        s = axs[i, 1]
        s.specgram(y + 1e-9, NFFT=1024, Fs=sr, noverlap=768, cmap="magma", vmin=-130, vmax=-20)
        s.set_yscale("symlog", linthresh=300)
        s.set_ylim(40, sr / 2)
        s.tick_params(labelsize=6)
    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"{name}.png")
    fig.savefig(p, dpi=62)
    plt.close(fig)
    print(p)


def main():
    import warnings
    warnings.filterwarnings("ignore")
    sfx = sorted(glob.glob(os.path.join(SOM, "sfx", "*.wav")))
    sheet("VER-01_sfx_parte1", sfx[: len(sfx) // 2])
    sheet("VER-02_sfx_parte2", sfx[len(sfx) // 2:])
    sheet("VER-03_identidade", sorted(glob.glob(os.path.join(SOM, "identidade", "*.wav"))), loud=True)
    sheet("VER-04_musica", sorted(glob.glob(os.path.join(SOM, "musica", "*.wav")))
          + sorted(glob.glob(os.path.join(SOM, "musica", "pecas", "*.wav"))))
    sheet("VER-05_filmes", sorted(glob.glob(os.path.join(SOM, "filmes", "*.wav"))), loud=True)


if __name__ == "__main__":
    main()
