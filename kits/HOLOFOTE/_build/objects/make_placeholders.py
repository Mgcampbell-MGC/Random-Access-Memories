"""Neutral placeholder art for the 3D props, used only until the packaging team's files exist.

Every placeholder is grey-on-neutral with the face name, its size in mm and an UP arrow, so a render shows at once
whether a face is mapped and which way up it reads. Atlases follow candle_lib.box(): a 4 x 3 grid of uniform
cells, top row [., top, ., .], middle [left, front, right, back], bottom [., bottom, ., .]. Each face is drawn at its
true aspect and then squashed into its square cell, exactly as the packaging team must deliver it.

    /home/user/venvs/blender/bin/python make_placeholders.py      (writes ./placeholders/*.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'placeholders')
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
COND = os.path.join(FONTS, 'SpecialGothicCondensedOne-Regular.ttf')

PRETO, PAPEL, AMARELO = (0x12, 0x10, 0x14), (0xFF, 0xF8, 0xEC), (0xFF, 0xE8, 0x1A)
GREY_ON_DARK, GREY_ON_LIGHT = (0x6A, 0x6A, 0x6E), (0x8E, 0x8C, 0x88)
NEUTRAL = (0xD9, 0xD7, 0xD2)
CELL = 512


def font(px):
    return ImageFont.truetype(COND, max(8, int(px)))


def face(w_mm, h_mm, bg, fg, title, ppm=8, arrow=True, extra=None):
    """One face at true aspect: border inset 1 mm, title + size centred, an UP arrow."""
    W, H = int(round(w_mm * ppm)), int(round(h_mm * ppm))
    im = Image.new('RGBA', (W, H), bg + (255,))
    d = ImageDraw.Draw(im)
    m = ppm
    d.rectangle([m, m, W - 1 - m, H - 1 - m], outline=fg + (255,), width=max(1, ppm // 4))
    size = min(H * 0.16, W * 0.09)
    lines = [title, f'{w_mm:g} × {h_mm:g} mm', 'PLACEHOLDER']
    fs = [font(size), font(size * 0.7), font(size * 0.55)]
    hs = [f.getbbox(t)[3] - f.getbbox(t)[1] for f, t in zip(fs, lines)]
    y = H / 2 - (sum(hs) + size * 0.5) / 2
    for t, f, h in zip(lines, fs, hs):
        bb = f.getbbox(t)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y - bb[1]), t, font=f, fill=fg + (255,))
        y += h + size * 0.25
    if arrow:
        ax, a = W - 4 * ppm, min(3.0 * ppm, H * 0.18)
        d.polygon([(ax, 2 * ppm), (ax - a / 2, 2 * ppm + a), (ax + a / 2, 2 * ppm + a)], fill=fg + (255,))
    if extra:
        extra(d, W, H, ppm)
    return im


def atlas(cells, bg):
    """cells: {name: Image}; names top/left/front/right/back/bottom and c00/c20/c30 (free top-row cells)."""
    pos = {'top': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2),
           'c00': (0, 0), 'c20': (2, 0), 'c30': (3, 0), 'c02': (0, 2), 'c22': (2, 2), 'c32': (3, 2)}
    A = Image.new('RGBA', (CELL * 4, CELL * 3), bg + (255,))
    for k, im in cells.items():
        cx, cy = pos[k]
        A.paste(im.resize((CELL, CELL), Image.LANCZOS), (cx * CELL, cy * CELL))
    return A


def bulb_frame(d, W, H, ppm):
    """Interior lid panel 126 x 126: ten printed bulbs (3 top, 3 bottom, 2 each side), mirror window 100 x 100."""
    m0 = 13 * ppm
    d.rectangle([m0, m0, W - m0, H - m0], fill=(0x30, 0x30, 0x34, 255))
    r = 4.5 * ppm
    c = 6.5 * ppm
    pts = [(W * f, c) for f in (0.25, 0.5, 0.75)] + [(W * f, H - c) for f in (0.25, 0.5, 0.75)]
    pts += [(c, H * f) for f in (0.37, 0.63)] + [(W - c, H * f) for f in (0.37, 0.63)]
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=PAPEL + (255,))
        d.line([x - r * 0.45, y, x + r * 0.45, y], fill=(0x8A, 0x8A, 0x8A, 255), width=max(1, ppm // 3))


def tickets(d, W, H, ppm):
    """Setlist: panel outlines P1..P4 (100 mm each), P4 split into four 25 mm tickets with the stub at x = 83."""
    for i in range(1, 4):
        y = i * 100 * ppm
        d.line([0, y, W, y], fill=GREY_ON_LIGHT + (255,), width=max(1, ppm // 4))
    for i in range(1, 4):
        y = (300 + 25 * i) * ppm
        d.line([0, y, W, y], fill=GREY_ON_LIGHT + (255,), width=max(1, ppm // 6))
    d.line([83 * ppm, 300 * ppm, 83 * ppm, H], fill=GREY_ON_LIGHT + (255,), width=max(1, ppm // 6))


def setlist_side(side):
    W, Hh, ppm = 105, 400, 10
    im = Image.new('RGBA', (W * ppm, Hh * ppm), PAPEL + (255,))
    for i in range(4):
        name = f'P{i + 1}' + ("'" if side == 2 else '')
        f = face(W, 100, PAPEL, GREY_ON_LIGHT, f'SETLIST · {name}', ppm=ppm, arrow=True)
        im.paste(f, (0, i * 100 * ppm))
    tickets(ImageDraw.Draw(im), W * ppm, Hh * ppm, ppm)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    # O CASE: base tray 130 x 130 x 102 and lid 130 x 130 x 30
    base = atlas({
        'front': face(130, 102, PRETO, GREY_ON_DARK, 'CASE BASE · FRENTE'),
        'back': face(130, 102, PRETO, GREY_ON_DARK, 'CASE BASE · VERSO'),
        'left': face(130, 102, PRETO, GREY_ON_DARK, 'CASE BASE · ESQ'),
        'right': face(130, 102, PRETO, GREY_ON_DARK, 'CASE BASE · DIR'),
        'bottom': face(130, 130, PRETO, GREY_ON_DARK, 'CASE BASE · FUNDO'),
    }, PRETO)
    base.save(os.path.join(OUT, 'PH_CASE_BASE_atlas.png'))
    lid = atlas({
        'top': face(130, 130, PRETO, GREY_ON_DARK, 'CASE TAMPA · TOPO'),
        'front': face(130, 30, PRETO, GREY_ON_DARK, 'TAMPA · FRENTE'),
        'back': face(130, 30, PRETO, GREY_ON_DARK, 'TAMPA · VERSO'),
        'left': face(130, 30, PRETO, GREY_ON_DARK, 'TAMPA · ESQ'),
        'right': face(130, 30, PRETO, GREY_ON_DARK, 'TAMPA · DIR'),
        'bottom': face(126, 126, PRETO, GREY_ON_DARK, 'INTERIOR · ESPELHO', arrow=True, extra=bulb_frame),
        'c00': face(44, 40, PRETO, GREY_ON_DARK, 'ALÇA'),
    }, PRETO)
    lid.save(os.path.join(OUT, 'PH_CASE_TAMPA_atlas.png'))
    # Carton O INGRESSO 96 x 96 x 98
    ing = atlas({
        'top': face(96, 96, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · TOPO'),
        'front': face(96, 98, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · FRENTE'),
        'back': face(96, 98, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · VERSO'),
        'left': face(96, 98, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · LAT 1'),
        'right': face(96, 98, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · LAT 2'),
        'bottom': face(96, 96, NEUTRAL, GREY_ON_LIGHT, 'INGRESSO · FUNDO'),
    }, NEUTRAL)
    ing.save(os.path.join(OUT, 'PH_INGRESSO_atlas.png'))
    # Setlist, both sides (105 x 400 mm, P1 at the top)
    setlist_side(1).save(os.path.join(OUT, 'PH_SETLIST_lado1.png'))
    setlist_side(2).save(os.path.join(OUT, 'PH_SETLIST_lado2.png'))
    # Refill: peel-lid print (the Ø66 printed circle, square image), wall band (laser marking, transparent)
    pl = face(66, 66, AMARELO, (0x55, 0x52, 0x40), 'PEEL Ø66', ppm=12)
    mask = Image.new('L', pl.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, pl.size[0] - 1, pl.size[1] - 1], fill=255)
    pl.putalpha(mask)
    pl.save(os.path.join(OUT, 'PH_REFIL_tampa.png'))
    band = Image.new('RGBA', (int(213.6 * 10), 12 * 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    f = font(60)
    for cx in (0.5,):
        t = 'LOTE · FAB · VAL  (PLACEHOLDER)'
        bb = f.getbbox(t)
        d.text((band.size[0] * cx - (bb[2] - bb[0]) / 2, 60 - (bb[3] + bb[1]) / 2), t, font=f, fill=(0xB0, 0xB0, 0xB0, 255))
    band.save(os.path.join(OUT, 'PH_REFIL_faixa.png'))
    # Wristband: 350 x 15 mm, grey dashes where the jacquard text will run
    ppm = 20
    wb = Image.new('RGBA', (350 * ppm, 15 * ppm), PRETO + (255,))
    d = ImageDraw.Draw(wb)
    x = 6 * ppm
    while x < 344 * ppm:
        d.rectangle([x, 5.5 * ppm, x + 26 * ppm, 9.5 * ppm], fill=(0x55, 0x55, 0x58, 255))
        x += 34 * ppm
    wb.save(os.path.join(OUT, 'PH_PULSEIRA_jacquard.png'))
    # Paper seal faces (the visible top face of the wrap, as seen; and the back face)
    # paper seal: ONE 60 x 15 strip printed outside (x = s along the strip): s 23-44 amarelo (sides + TOPO),
    # TOPO 25,5-41,5 labelled with its tops toward +x, BAIXO 44-60 papel
    ppm = 20
    st = Image.new('RGBA', (60 * ppm, 15 * ppm), PAPEL + (255,))
    d = ImageDraw.Draw(st)
    d.rectangle([23 * ppm, 0, 44 * ppm, 15 * ppm], fill=AMARELO + (255,))
    for s_ in (23, 25.5, 41.5, 44):
        d.line([s_ * ppm, 0, s_ * ppm, 15 * ppm], fill=(0x55, 0x52, 0x40, 255), width=2)
    lab = Image.new('RGBA', (15 * ppm, 16 * ppm), (0, 0, 0, 0))
    ImageDraw.Draw(lab).text((20, 90), 'SELO TOPO', font=font(46), fill=(0x55, 0x52, 0x40, 255))
    st.alpha_composite(lab.rotate(-90, expand=True), (int(25.5 * ppm), 0))
    st.save(os.path.join(OUT, 'PH_SELO_faixa.png'))
    print('placeholders ->', OUT)


if __name__ == '__main__':
    main()
