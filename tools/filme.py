"""Filme — turns one approved composite into a short film with the packaging locked (no generator touches it).

Usage:
    python3 filme.py SAIDA.png FILME.mp4 [--segundos 15] [--formato 9:16] [--zoom 0.08] [--pan 0.05]
                     [--paralaxe 0.6] [--luz 22] [--trilha musica.mp3]

SAIDA.png is the output of compor.py; its sidecars SAIDA.alpha.png (the packaging layer) and, if present,
SAIDA.hidden.png (what covers the packaging) are read automatically.

The film is a camera move over a still: a slow push-in and pan, the background moving slightly more than the
product (parallax), and a soft band of light crossing the background. The packaging is only ever scaled and moved
as a whole, so every letter stays exactly as approved. It does NOT turn the product in 3D. If something covers the
packaging (a hand), parallax is switched off, because a hand that moves apart from its own arm looks broken.

Writes FILME.mp4 (H.264, for Instagram, TikTok and marketplaces) and, when the source has a hidden mask,
FILME.hidden.mp4, which relatorio_fidelidade.py reads frame by frame so covered parts count as hidden, not altered.
Needs: pip install imageio-ffmpeg (a bundled ffmpeg).
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

try:
    import imageio_ffmpeg
except ImportError:
    sys.exit("pip install imageio-ffmpeg")


def writer(path, w, h, fps, gray=False):
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt",
           "gray" if gray else "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
           "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def ease(t):
    return t * t * (3 - 2 * t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("composto")
    ap.add_argument("saida")
    ap.add_argument("--segundos", type=float, default=15)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--formato", default="9:16", help="9:16, 4:5, 1:1 or 16:9")
    ap.add_argument("--zoom", type=float, default=0.08, help="total push-in over the film")
    ap.add_argument("--pan", type=float, default=0.05, help="total pan as a share of width")
    ap.add_argument("--paralaxe", type=float, default=0.6, help="product moves this much of the background's zoom")
    ap.add_argument("--luz", type=float, default=22, help="strength of the light sweep on the background (0 = off)")
    ap.add_argument("--trilha", help="audio file to lay under the film")
    a = ap.parse_args()

    stem = a.composto.rsplit(".", 1)[0]
    img = cv2.imread(a.composto)
    alpha = cv2.imread(stem + ".alpha.png", cv2.IMREAD_GRAYSCALE)
    if img is None or alpha is None:
        sys.exit("need SAIDA.png and SAIDA.alpha.png from compor.py")
    hidden = cv2.imread(stem + ".hidden.png", cv2.IMREAD_GRAYSCALE)
    has_hidden = hidden is not None and (hidden > 127).sum() > 50
    H, W = img.shape[:2]
    img = img.astype(np.float32)
    al = alpha.astype(np.float32) / 255
    par = 0.0 if has_hidden else a.paralaxe
    if has_hidden and a.paralaxe:
        print("embalagem coberta (mão): paralaxe desligada")

    # Output frame: the largest box of the requested shape that fits, even-sized for H.264.
    fw, fh = (int(x) for x in a.formato.split(":"))
    ow = min(W, int(H * fw / fh))
    oh = int(ow * fh / fw)
    ow, oh = ow - ow % 2, oh - oh % 2
    ox, oy = (W - ow) // 2, (H - oh) // 2

    # Clean background plate behind the product, for parallax.
    plate = img
    if par:
        m = cv2.dilate((al > 0.05).astype(np.uint8) * 255, np.ones((31, 31), np.uint8))
        plate = cv2.inpaint(img.astype(np.uint8), m, 9, cv2.INPAINT_TELEA).astype(np.float32)
    ys, xs = np.where(al > 0.5)
    c = np.array([xs.mean(), ys.mean()])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fg = np.clip(al + (hidden.astype(np.float32) / 255 if has_hidden else 0), 0, 1)

    def affine(s, pan):
        return np.float32([[s, 0, c[0] * (1 - s) + pan], [0, s, c[1] * (1 - s)]])

    N = int(round(a.fps * a.segundos))
    vw = writer(a.saida if not a.trilha else a.saida + ".tmp.mp4", ow, oh, a.fps)
    hidden_out = stem_out(a.saida) + ".hidden.mp4"
    if not has_hidden and os.path.exists(hidden_out):
        os.remove(hidden_out)  # a stale mask from an earlier render would be read by the checker
    hw = writer(hidden_out, ow, oh, a.fps, gray=True) if has_hidden else None
    for i in range(N):
        t = i / max(N - 1, 1)
        e = ease(t)
        sb = 1 + a.zoom * e
        sp = 1 + a.zoom * e * (par if par else 1)
        pan = W * a.pan * (0.5 - e)
        bg = cv2.warpAffine(plate, affine(sb, pan), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        Ap = affine(sp, pan)
        fr = cv2.warpAffine(img, Ap, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        layer = cv2.warpAffine(fg, Ap, (W, H), flags=cv2.INTER_LINEAR)[..., None]
        if a.luz:
            band = np.exp(-(((xx + 0.6 * yy) - (-0.3 * W + 1.9 * W * t)) / (0.18 * W)) ** 2) * a.luz
            bg = bg + band[..., None]
        out = bg * (1 - layer) + fr * layer if (par or a.luz) else fr
        vw.stdin.write(np.clip(out[oy:oy + oh, ox:ox + ow], 0, 255).astype(np.uint8).tobytes())
        if hw:
            hm = cv2.warpAffine(hidden, Ap, (W, H), flags=cv2.INTER_NEAREST)
            hw.stdin.write(np.ascontiguousarray(hm[oy:oy + oh, ox:ox + ow]).tobytes())
    for p in (vw, hw):
        if p:
            p.stdin.close()
            p.wait()
    if a.trilha:
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", a.saida + ".tmp.mp4",
                        "-i", a.trilha, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest",
                        "-af", f"afade=t=out:st={max(a.segundos - 1.5, 0)}:d=1.5", a.saida], check=True)
        os.remove(a.saida + ".tmp.mp4")
    print(f"{N} quadros, {ow}x{oh}, {a.segundos:g} s -> {a.saida}")


def stem_out(p):
    return p.rsplit(".", 1)[0]


if __name__ == "__main__":
    main()
