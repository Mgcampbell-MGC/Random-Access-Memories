"""Codificar — encodes a folder of frames into an MP4 whose colours are converted AND tagged as BT.709.

Usage:
    python3 codificar.py PASTA_DE_QUADROS FILME.mp4 [--fps 30] [--trilha musica.mp3] [--segundos 15]

Why this exists (measured 26 Sep 2026): FFmpeg converts RGB to video colour with the old BT.601 formula unless told
otherwise, and tagging a file "bt709" does not change that conversion. HyperFrames' MP4 output is tagged BT.709 but
converted with BT.601, so a phone that trusts the tag shows the pack's saturated colours shifted (ΔE ≈6–7 measured on
a blue tube's green band). Render HyperFrames with `--format png-sequence` and encode here instead. `filme.py` uses the
same settings internally.
"""
import argparse
import glob
import os
import subprocess
import sys

# One place for the colour settings every film must carry.
BT709 = ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quadros")
    ap.add_argument("saida")
    ap.add_argument("--fps", default="30")
    ap.add_argument("--trilha")
    ap.add_argument("--segundos", type=float, help="length, for the music fade-out")
    a = ap.parse_args()
    frames = sorted(glob.glob(os.path.join(a.quadros, "*.png")))
    if not frames:
        sys.exit("no PNG frames in " + a.quadros)
    first = os.path.basename(frames[0])
    stem = first.rstrip("0123456789.png")
    digits = len(first) - len(stem) - len(".png")
    pattern = os.path.join(a.quadros, f"{stem}%0{digits}d.png")
    start = int(first[len(stem):len(stem) + digits])
    cmd = [ffmpeg(), "-y", "-loglevel", "error", "-framerate", str(a.fps), "-start_number", str(start), "-i", pattern]
    if a.trilha:
        cmd += ["-i", a.trilha, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-shortest"]
        if a.segundos:
            cmd += ["-af", f"afade=t=out:st={max(a.segundos - 1.5, 0)}:d=1.5"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "14", "-bf", "0", *BT709, "-movflags", "+faststart", a.saida]
    subprocess.run(cmd, check=True)
    print(f"{len(frames)} quadros -> {a.saida} (BT.709 convertido e marcado)")


if __name__ == "__main__":
    main()
