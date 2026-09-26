"""Filme HyperFrames — builds a HyperFrames project for a launch film from one approved composite.

Usage:
    python3 filme_hyperframes.py PECA.png PASTA [--linhas "NOVO|Linha 1|Linha 2"] [--final "EM BREVE|01 · 11"]
                                 [--segundos 8] [--fonte marca.woff2]
    cd PASTA && npx hyperframes check . && npx hyperframes render . --format png-sequence -o ../quadros
    python3 codificar.py quadros FILME.mp4 --fps 30 [--trilha musica.mp3 --segundos 8]
    python3 relatorio_fidelidade.py EMBALAGEM.png FILME.mp4

Never deliver HyperFrames' own MP4: it is tagged BT.709 but converted BT.601, which shifts the pack's colours on phones
(measured ΔE ≈6–7). The PNG sequence plus codificar.py converts and tags correctly.

PECA.png is the output of compor.py; its sidecars PECA.alpha.png and (if present) PECA.hidden.png are read. The script
splits the piece into a background plate and a packaging layer, and writes PASTA/index.html: the background moves more
than the pack (parallax), a band of light crosses the background only, and the type lines come in and go out.

Why this keeps the label exact: the pack is an <img> that the browser only scales and moves. Nothing redraws it.
Tested 26 Sep 2026 on one tube, product-on-a-sill and in-hand (results in O_LANCAMENTO_AIRTIGHT.md §4.3).

Rules the layout enforces: type is placed only in the free column beside the pack or in the band above or below it,
never across it. Ink is dark on a bright scene and light on a dark one; `npx hyperframes check` then audits contrast.
Type must come ONLY from the brand's signed Ficha de Alegações. GSAP is downloaded once into PASTA so the render needs
no network. Before any client work: `npx hyperframes telemetry disable`; never `publish`, `cloud`, `lambda`, `cloudrun`
or `feedback --file-issue` on a client project, because those send the project off the computer.
"""
import argparse
import html
import os
import shutil
import sys
import urllib.request

import cv2
import numpy as np

GSAP_URL = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"


def free_regions(W, H, x0, y0, x1, y1, pad):
    """Rectangles that do not touch the pack box (plus padding), largest first."""
    regions = [
        ("direita", x1 + pad, pad, W - pad, H - pad),
        ("esquerda", pad, pad, x0 - pad, H - pad),
        ("abaixo", pad, y1 + pad, W - pad, H - pad),
        ("acima", pad, pad, W - pad, y0 - pad),
    ]
    regions = [(n, a, b, c, d) for n, a, b, c, d in regions if c - a > 0 and d - b > 0]
    return sorted(regions, key=lambda r: (r[3] - r[1]) * (r[4] - r[2]), reverse=True)


def ink(plate, r):
    _, a, b, c, d = r
    L = cv2.cvtColor(plate[int(b):int(d), int(a):int(c)], cv2.COLOR_BGR2LAB)[..., 0]
    return ("#1b1b1d", "rgba(255,255,255,0.55)") if L.mean() > 140 else ("#fbfbfa", "rgba(0,0,0,0.45)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("peca")
    ap.add_argument("pasta")
    ap.add_argument("--linhas", default="NOVO|Linha um|Linha dois", help="kicker|word|word…, from the Ficha only")
    ap.add_argument("--final", default="EM BREVE|01 · 11", help="small|big end card")
    ap.add_argument("--segundos", type=float, default=8.0)
    ap.add_argument("--fonte", help="brand font file (.woff2/.ttf) the brand supplied")
    ap.add_argument("--gsap", help="local gsap.min.js to copy instead of downloading")
    a = ap.parse_args()

    stem = a.peca.rsplit(".", 1)[0]
    img = cv2.imread(a.peca)
    alpha = cv2.imread(stem + ".alpha.png", cv2.IMREAD_GRAYSCALE)
    if img is None or alpha is None:
        sys.exit("need PECA.png and PECA.alpha.png from compor.py")
    hidden = cv2.imread(stem + ".hidden.png", cv2.IMREAD_GRAYSCALE)
    in_hand = hidden is not None and (hidden > 127).sum() > 50
    H, W = img.shape[:2]
    W2, H2 = W - W % 2, H - H % 2
    img, alpha = img[:H2, :W2], alpha[:H2, :W2]
    os.makedirs(a.pasta, exist_ok=True)

    # Layer = the pack (plus whatever covers it, so fingers move with it). Plate = the scene without it.
    lay = alpha.astype(np.float32) / 255
    if in_hand:
        lay = np.clip(lay + hidden[:H2, :W2].astype(np.float32) / 255, 0, 1)
    m = cv2.dilate((lay > 0.05).astype(np.uint8) * 255, np.ones((31, 31), np.uint8))
    plate = cv2.inpaint(img, m, 9, cv2.INPAINT_TELEA)
    ys, xs = np.where(lay > 0.05)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    cv2.imwrite(os.path.join(a.pasta, "plate.png"), plate if not in_hand else img)
    cv2.imwrite(os.path.join(a.pasta, "pack_layer.png"), np.dstack([img, (lay * 255).astype(np.uint8)])[y0:y1, x0:x1])

    # Zoom grows everything about the pack centre; keep type clear of the pack at the END of the move too.
    zoom = 0.10
    pad = int(0.04 * W2 + zoom * max(W2, H2) / 2)
    regions = free_regions(W2, H2, x0, y0, x1, y1, pad)
    if not regions:
        sys.exit("no room for type beside the pack: use a wider scene or --linhas ''")
    side = regions[0]
    end = next((r for r in regions if r[0] in ("abaixo", "acima") and r[4] - r[2] >= 0.09 * H2), side)
    col, shade = ink(plate, side)
    ecol, eshade = ink(plate, end)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    par = 0.0 if in_hand else 0.5  # a hand must move with its arm

    font_face, family = "", "sans-serif"
    if a.fonte:
        shutil.copy(a.fonte, os.path.join(a.pasta, "marca" + os.path.splitext(a.fonte)[1]))
        font_face = f'@font-face {{ font-family: "Marca"; src: url("marca{os.path.splitext(a.fonte)[1]}"); }}'
        family = '"Marca", sans-serif'
    gsap_path = os.path.join(a.pasta, "gsap.min.js")
    if a.gsap:
        shutil.copy(a.gsap, gsap_path)
    elif not os.path.exists(gsap_path):
        urllib.request.urlretrieve(GSAP_URL, gsap_path)

    lines = [html.escape(s) for s in a.linhas.split("|") if s.strip()]
    fin = [html.escape(s) for s in a.final.split("|") if s.strip()]
    sw = side[3] - side[1]
    big = int(min(64, max(28, sw / 6.2)))
    T = a.segundos
    words = "".join(f'<span class="word" id="w{i}">{w}</span>' for i, w in enumerate(lines[1:], 1))
    word_ids = ", ".join(f'"#w{i}"' for i in range(1, len(lines)))
    endb = f'<span class="small" id="e1">{fin[0]}</span>' + (f'<span class="big" id="e2">{fin[1]}</span>' if len(fin) > 1 else "")
    doc = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W2}, height={H2}" />
    <script src="gsap.min.js"></script>
    <style>
      {font_face}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W2}px; height: {H2}px; overflow: hidden; background: #111; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: {family}; }}
      .layer {{ position: absolute; display: block; }}
      #plate {{ left: 0; top: 0; width: {W2}px; height: {H2}px; transform-origin: {cx:.0f}px {cy:.0f}px; }}
      #sweep {{ left: 0; top: 0; width: {W2}px; height: {H2}px; mix-blend-mode: screen; pointer-events: none;
        background: linear-gradient(105deg, rgba(255,240,220,0) 40%, rgba(255,240,220,0.22) 50%, rgba(255,240,220,0) 60%); }}
      #pack {{ left: {x0}px; top: {y0}px; width: {x1 - x0}px; height: {y1 - y0}px; transform-origin: {cx - x0:.0f}px {cy - y0:.0f}px; }}
      #copy {{ left: {side[1]}px; top: {side[2]}px; width: {side[3] - side[1]}px; height: {side[4] - side[2]}px; color: {col}; text-shadow: 0 1px 14px {shade}; }}
      #kicker {{ display: block; font-weight: 600; font-size: {max(14, big // 3)}px; letter-spacing: 0.28em; margin-bottom: 8px; }}
      .word {{ display: block; font-weight: 800; font-size: {big}px; line-height: 1.02; }}
      #end {{ left: {end[1]}px; top: {end[2]}px; width: {end[3] - end[1]}px; height: {end[4] - end[2]}px; color: {ecol};
        text-shadow: 0 1px 14px {eshade}; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
      #end .small {{ display: block; font-weight: 600; font-size: {max(14, big // 3)}px; letter-spacing: 0.3em; }}
      #end .big {{ display: block; font-weight: 800; font-size: {int(big * 0.85)}px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T:g}" data-width="{W2}" data-height="{H2}">
      <img id="plate" class="layer clip" src="plate.png" data-start="0" data-duration="{T:g}" data-track-index="0" />
      <div id="sweep" class="layer clip" data-start="0" data-duration="{T:g}" data-track-index="1"></div>
      <img id="pack" class="layer clip" src="pack_layer.png" data-start="0" data-duration="{T:g}" data-track-index="2" />
      <div id="copy" class="layer clip" data-start="0.4" data-duration="{T * 0.68:.2f}" data-track-index="3">
        <span id="kicker">{lines[0] if lines else ""}</span>{words}
      </div>
      <div id="end" class="layer clip" data-start="{T * 0.74:.2f}" data-duration="{T * 0.26:.2f}" data-track-index="4">{endb}</div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const pan = {W2 * 0.018:.1f};
      tl.fromTo("#plate", {{ scale: 1.0, x: pan }}, {{ scale: {1 + zoom:.2f}, x: -pan, duration: {T:g}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#pack", {{ scale: 1.0, x: pan }}, {{ scale: {1 + zoom * (par if par else 1):.3f}, x: -pan, duration: {T:g}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#sweep", {{ x: -{W2} }}, {{ x: {int(W2 * 1.2)}, duration: {T * 0.75:.2f}, ease: "power1.inOut" }}, {T * 0.1:.2f});
      tl.fromTo("#kicker", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, 0.5);
      {f'tl.fromTo([{word_ids}], {{ opacity: 0, y: 28 }}, {{ opacity: 1, y: 0, duration: 0.6, stagger: 0.25, ease: "power3.out" }}, 0.9);' if word_ids else ''}
      tl.to(["#kicker"{", " + word_ids if word_ids else ""}], {{ opacity: 0, y: -16, duration: 0.4, stagger: 0.05, ease: "power2.in" }}, {T * 0.66:.2f});
      tl.fromTo("#end > span", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.6, stagger: 0.15, ease: "power3.out" }}, {T * 0.75:.2f});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
    with open(os.path.join(a.pasta, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"{W2}x{H2}, {T:g} s, texto em '{side[0]}', final em '{end[0]}', "
          f"{'mão: paralaxe desligada' if in_hand else 'paralaxe ligada'} -> {a.pasta}/index.html\n"
          f"próximo: npx hyperframes render {a.pasta} --format png-sequence -o quadros && "
          f"python3 codificar.py quadros FILME.mp4 --fps 30")


if __name__ == "__main__":
    main()
