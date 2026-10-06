"""Recortar — crops an image to an exact delivery size, keeping the centre.

Usage:
    python3 recortar.py ENTRADA.png SAIDA.png 1080x1350

Use it twice in a launch:
- On a generated SCENE, before compor.py, to bring it to the delivery size (crop to the shape, then resize).
- On a finished PIECE from compor.py, to cut the 4:5 and 1:1 versions out of the 9:16 key visual. When the crop is
  already the requested size nothing is resized, so the packaging's pixels are copied, never resampled. The sibling
  masks compor.py writes (<name>.hidden.png, <name>.alpha.png) are cropped identically, so the checker and filme.py
  still work on the result.
"""
import argparse
import os
import sys

import cv2


def crop(img, w, h, interp):
    H, W = img.shape[:2]
    cw = min(W, int(round(H * w / h)))
    ch = min(H, int(round(cw * h / w)))
    x, y = (W - cw) // 2, (H - ch) // 2
    out = img[y:y + ch, x:x + cw]
    if (cw, ch) != (w, h):
        out = cv2.resize(out, (w, h), interpolation=interp)
    return out, (cw, ch) != (w, h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("tamanho", help="LARGURAxALTURA, e.g. 1080x1350")
    a = ap.parse_args()
    w, h = (int(v) for v in a.tamanho.lower().split("x"))
    img = cv2.imread(a.entrada, cv2.IMREAD_UNCHANGED)
    if img is None:
        sys.exit("não consegui abrir " + a.entrada)
    big = img.shape[1] >= w and img.shape[0] >= h
    out, resized = crop(img, w, h, cv2.INTER_AREA if big else cv2.INTER_CUBIC)
    cv2.imwrite(a.saida, out)
    src, dst = a.entrada.rsplit(".", 1)[0], a.saida.rsplit(".", 1)[0]
    masks = [s for s in (".hidden.png", ".alpha.png") if os.path.exists(src + s)]
    for s in masks:
        m = cv2.imread(src + s, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(dst + s, crop(m, w, h, cv2.INTER_AREA)[0])
    if resized and masks:
        print("AVISO: a peça foi redimensionada, então a embalagem foi reamostrada. Confira de novo, ou componha "
              "numa cena já do tamanho final.")
    if not big:
        print(f"AVISO: a imagem é menor que {w}x{h} e foi ampliada.")
    print(f"{a.entrada} -> {a.saida} {w}x{h}" + (" (redimensionada)" if resized else " (só recorte)"))


if __name__ == "__main__":
    main()
