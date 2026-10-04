"""Texto — writes the approved phrases onto a finished piece, beside the packaging, never over it.

Usage:
    python3 texto.py PECA.png PECA_texto.png --linhas "NOVO|Frase aprovada|segunda linha" [--fonte marca.ttf] [--cor #1A1A1A]

Why this exists: an AI image editor asked to "add the headline" redraws the whole picture, label included. Text must
be written by code onto the finished piece. This tool reads the packaging mask compor.py wrote (<piece>.alpha.png),
chooses the largest free band above, below, left or right of the pack, fits the lines into it, and then proves that
every packaging pixel is byte-identical to the input. The masks are copied next to the output so the checker and
filme.py still work. The first line is set smaller, as a kicker; the rest are the phrase. Text comes only from the
signed Ficha de Alegações.
"""
import argparse
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def font(path, size):
    if path:
        return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        sys.exit("Pillow antigo: rode python3 -m pip install -U pillow, ou passe --fonte")


def layout(draw, lines, fpath, box):
    """Largest size at which the block fits in box (x0, y0, x1, y1). Returns (size, rendered line list)."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    for size in range(int(bh / 3), 11, -2):
        sizes = [max(12, int(size * 0.55))] + [size] * (len(lines) - 1) if len(lines) > 1 else [size]
        fonts = [font(fpath, s) for s in sizes]
        boxes = [draw.textbbox((0, 0), ln, font=f) for ln, f in zip(lines, fonts)]
        w = max(b[2] - b[0] for b in boxes)
        h = sum(b[3] - b[1] for b in boxes) + int(size * 0.3) * (len(lines) - 1)
        if w <= bw and h <= bh:
            return fonts, boxes, w, h
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("peca")
    ap.add_argument("saida")
    ap.add_argument("--linhas", required=True, help="kicker|linha|linha, da Ficha de Alegações")
    ap.add_argument("--fonte", help="arquivo .ttf/.otf da marca")
    ap.add_argument("--cor", help="#RRGGBB; sem isto, preto ou branco conforme o fundo")
    a = ap.parse_args()

    img = Image.open(a.peca).convert("RGB")
    W, H = img.size
    stem_in, stem_out = a.peca.rsplit(".", 1)[0], a.saida.rsplit(".", 1)[0]
    try:
        alpha = np.array(Image.open(stem_in + ".alpha.png").convert("L"))
    except FileNotFoundError:
        sys.exit("preciso de " + stem_in + ".alpha.png (sai do compor.py)")
    pack = alpha > 8
    ys, xs = np.where(pack)
    m = int(0.05 * W)  # breathing room around the pack and the frame edge
    px0, py0, px1, py1 = xs.min() - m, ys.min() - m, xs.max() + m, ys.max() + m
    bands = {
        "acima": (m, m, W - m, py0),
        "abaixo": (m, py1, W - m, H - m),
        "esquerda": (m, m, px0, H - m),
        "direita": (px1, m, W - m, H - m),
    }
    lines = [s.strip() for s in a.linhas.split("|") if s.strip()]
    draw = ImageDraw.Draw(img)
    best = None
    for name, b in bands.items():
        if b[2] - b[0] < 0.15 * W or b[3] - b[1] < 0.06 * H:
            continue
        fit = layout(draw, lines, a.fonte, b)
        if fit and (best is None or fit[0][-1].size > best[1][0][-1].size):
            best = (name, fit, b)
    if best is None:
        sys.exit("não há espaço livre ao lado da embalagem para esse texto: encurte a frase ou gere a cena com mais "
                 "espaço em volta do produto")
    name, (fonts, boxes, w, h), b = best

    region = np.array(img)[b[1]:b[3], b[0]:b[2]].reshape(-1, 3)
    lum = (region @ np.array([0.2126, 0.7152, 0.0722])).mean()
    color = a.cor or ("#111111" if lum > 140 else "#FFFFFF")
    x = b[0] + (b[2] - b[0] - w) // 2
    y = b[1] + (b[3] - b[1] - h) // 2
    before = np.array(img)[pack].copy()
    for ln, f, bb in zip(lines, fonts, boxes):
        lw = bb[2] - bb[0]
        draw.text((x + (w - lw) // 2 - bb[0], y - bb[1]), ln, font=f, fill=color)
        y += (bb[3] - bb[1]) + int(fonts[-1].size * 0.3)
    after = np.array(img)[pack]
    if not np.array_equal(before, after):
        sys.exit("ERRO: o texto encostou na embalagem. Nada foi salvo.")
    img.save(a.saida)
    for s in (".alpha.png", ".hidden.png"):
        try:
            shutil.copyfile(stem_in + s, stem_out + s)
        except FileNotFoundError:
            pass
    print(f"texto {name} da embalagem, cor {color}; embalagem intacta: sim -> {a.saida}")


if __name__ == "__main__":
    main()
