"""A MARCA — o X de fita gaffer amarela (plataforma §D.3, §C.5, §D.6).

Duas tiras cruzadas a ±45°, comprimento:largura 3,75:1 (ajustável), pontas rasgadas à mão com fios soltos,
microtextura de tecido (urdume e trama), a tira de cima sobe na de baixo (sombra e relevo no cruzamento) e uma ponta
descola 0,5 mm (sombra de levantamento). Tudo determinístico pela semente.

Saídas:
  PNG RGBA (mestre texturizado), em qualquer tamanho        --png
  SVG vetorial (geometria exata, cor chapada + trama em pattern) --svg
  JSON com a geometria das tiras (centro, ângulo, comprimento, largura, qual está por cima, ponta levantada)
  — para quem precisa compor texto ao longo de uma tira (ex.: "ela fica aqui." na tampa).

Uso:
  python marca.py --png saida.png [--svg saida.svg] [--tamanho 1024] [--semente 927] [--razao 3.75]
                  [--fios 40] [--fundo transparente|preto|papel|<hex>] [--sem-sombra] [--cor amarelo]
                  [--uma --angulo -6]   (uma tira só: o pedaço de fita da tampa)
"""
import argparse, json, math, os, sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ruido  # noqa: E402

CORES = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A', rosa='#FF4FA0', laranja='#FF6A1A', violeta='#8424F5')


def hex2rgb(h):
    h = CORES.get(h, h).lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def geometria(S, razao, r):
    """Duas tiras centradas, em px do canvas final. Tira 0 a +45° (sobe para a direita), tira 1 a −45°."""
    L = S * 1.0
    W = L / razao
    # o X inteiro (com pontas e fios) deve caber no quadrado: (L+W)/√2 ≤ 0,95 S
    lim = 0.95 * S * math.sqrt(2)
    if L + W > lim:
        k = lim / (L + W)
        L, W = L * k, W * k
    cx = cy = S / 2
    tiras = []
    for i, ang in enumerate((45.0, -45.0)):
        a = ang + r.uniform(-2.2, 2.2)              # mão humana: nunca exatamente 45°
        dx, dy = r.uniform(-0.012, 0.012) * S, r.uniform(-0.012, 0.012) * S
        Li = L * r.uniform(0.965, 1.0)
        tiras.append(dict(cx=cx + dx, cy=cy + dy, ang=a, L=Li, W=W))
    topo = int(r.integers(0, 2))                    # qual tira foi colada por cima
    levantada = dict(tira=int(r.integers(0, 2)), ponta=int(r.choice([-1, 1])))
    return tiras, topo, levantada


def perfis_pontas(W, r, n=600):
    """Perfil de cada ponta rasgada: deslocamento ao longo do comprimento em função da posição na largura.
    Rasgo à mão: inclinação + curva + ruído fractal + dentes IRREGULARES (espaçamento e altura aleatórios)."""
    out = []
    for _ in range(2):
        t = np.linspace(-0.5, 0.5, n)
        inclin = r.uniform(-0.22, 0.22) * W * t
        curva = r.uniform(-0.05, 0.05) * W * (1 - (2 * t) ** 2)
        frac = ruido.perfil_1d(n, r, 0.04 * W)
        # dentes: pontos com espaçamento aleatório (0,6–2,8% da largura) e altura aleatória, ligados em zigue-zague
        xs, x = [], -0.5
        while x < 0.5:
            xs.append(x)
            x += r.uniform(0.006, 0.028)
        xs.append(0.5)
        hs = r.uniform(-1, 1, len(xs)) * r.uniform(0.004, 0.018, len(xs)) * W
        hs[::2] *= 0.35
        dentes = np.interp(t, xs, hs)
        out.append(inclin + curva + frac + dentes)
    return out


def coords(S, ss, tira):
    """Coordenadas locais (s ao longo, t através) de cada pixel do canvas supersampled."""
    N = S * ss
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    xx = (xx + 0.5) / ss - tira['cx']
    yy = (yy + 0.5) / ss - tira['cy']
    a = math.radians(tira['ang'])
    ux, uy = math.cos(a), -math.sin(a)              # eixo da tira (y da tela para baixo)
    s = xx * ux + yy * uy
    t = -xx * uy + yy * ux
    return s, t


def mascara_tira(s, t, tira, perfis, fios, r, ss):
    L, W = tira['L'], tira['W']
    n = len(perfis[0])
    tn = np.clip((t / W + 0.5) * (n - 1), 0, n - 1)
    e0 = np.interp(tn.ravel(), np.arange(n), perfis[0]).reshape(t.shape)
    e1 = np.interp(tn.ravel(), np.arange(n), perfis[1]).reshape(t.shape)
    borda_long = 0.0035 * W * ruido.valor(t.shape[0], t.shape[1], 40 * ss, r)  # borda de fábrica, quase reta
    dentro_t = W / 2 - np.abs(t) + borda_long
    dentro_s0 = s - (-L / 2 + e0)
    dentro_s1 = (L / 2 + e1) - s
    d = np.minimum(dentro_t, np.minimum(dentro_s0, dentro_s1))
    return np.clip(d * ss + 0.5, 0, 1)


def fios_soltos(N, ss, tira, perfis, r):
    """Fios da tela (scrim) que sobram no rasgo: curtos, claros, densos como uma franja. Desenhados em px de tela."""
    L, W = tira['L'], tira['W']
    n = len(perfis[0])
    a = math.radians(tira['ang'])
    ux, uy = math.cos(a), -math.sin(a)
    vx, vy = -uy, ux
    m = np.zeros((N, N), np.float32)
    for perf, sinal in ((perfis[0], -1), (perfis[1], 1)):
        for _ in range(int(r.integers(14, 26))):
            tn = r.uniform(-0.48, 0.48)
            k = int((tn + 0.5) * (n - 1))
            s0 = sinal * L / 2 + perf[k] - sinal * 0.004 * W
            t0 = tn * W
            comp = r.uniform(0.006, 0.032) * W * (1.0 if r.random() > 0.15 else 2.0)
            ang = r.uniform(-0.45, 0.45)
            s1 = s0 + sinal * comp * math.cos(ang)
            t1 = t0 + comp * math.sin(ang)
            p0 = ((tira['cx'] + s0 * ux + t0 * vx) * ss, (tira['cy'] + s0 * uy + t0 * vy) * ss)
            p1 = ((tira['cx'] + s1 * ux + t1 * vx) * ss, (tira['cy'] + s1 * uy + t1 * vy) * ss)
            esp = max(1, int(round(r.uniform(0.0025, 0.0045) * W * ss)))
            cv2.line(m, tuple(int(round(v * 16)) for v in p0), tuple(int(round(v * 16)) for v in p1),
                     float(r.uniform(0.55, 0.95)), esp, cv2.LINE_AA, shift=4)
    return m


def textura_tecido(s, t, tira, fios, r, ss):
    """Variação de luminância (±) da fita: trama, urdume irregular, fibras e brilho baixo."""
    W = tira['W']
    pt = W / fios                                   # passo do urdume (fios ao longo da tira)
    ps = pt * r.uniform(0.9, 1.15)                  # passo da trama
    h0, w0 = s.shape
    t = t + 0.18 * pt * ruido.valor(h0, w0, 6 * pt * ss, r)        # fios nunca perfeitamente retos
    s = s + 0.18 * ps * ruido.valor(h0, w0, 6 * ps * ss, r)
    warp = np.cos(2 * np.pi * t / pt)
    weft = np.cos(2 * np.pi * s / ps)
    tela = 0.5 * (np.sign(np.sin(np.pi * s / ps) * np.sin(np.pi * t / pt)))  # tafetá: por cima/por baixo
    idx = np.floor(t / pt).astype(np.int64)
    var_fio = (np.sin(idx * 12.9898 + r.uniform(0, 100)) * 43758.5453) % 1.0 - 0.5  # cada fio um tom
    h, w = s.shape
    fibras = ruido.valor(h, w, 1.2 * ss, r) * 0.5
    brilho = ruido.fractal(h, w, 0.6 * W * ss, r, 3)
    v = 0.030 * warp * (0.55 + 0.45 * tela) + 0.018 * weft * (0.5 - 0.5 * tela) + 0.022 * var_fio \
        + 0.012 * fibras + 0.030 * brilho
    return v


def gerar(S=1024, semente=927, razao=3.75, fios=40, cor='amarelo', sombra=True, ss=None, uma=False, angulo=-6.0):
    """uma=True: UMA tira só (A TIRA: o pedaço de fita da tampa, 'ela fica aqui.'), quase horizontal, no ângulo dado."""
    r = ruido.rng(semente)
    ss = ss or (3 if S <= 1200 else 2 if S <= 2600 else 1)
    tiras, topo, lev = geometria(S, razao, r)
    if uma:
        L = 0.9 * S
        tiras = [dict(cx=S / 2, cy=S / 2, ang=angulo + r.uniform(-1.2, 1.2), L=L, W=L / razao)]
        topo, lev = 0, dict(tira=0, ponta=int(r.choice([-1, 1])))
    base = hex2rgb(cor)
    N = S * ss
    alfa = np.zeros((N, N), np.float32)
    rgb = np.zeros((N, N, 3), np.float32)
    sombra_bg = np.zeros((N, N), np.float32)
    ordem = [0] if uma else [1 - topo, topo]
    mascaras = {}
    for i in ordem:
        tira = tiras[i]
        s, t = coords(S, ss, tira)
        perf = perfis_pontas(tira['W'], r)
        m = mascara_tira(s, t, tira, perf, fios, r, ss)
        fio = fios_soltos(N, ss, tira, perf, r) * (m < 0.5)
        v = textura_tecido(s, t, tira, fios, r, ss)
        # ponta levantada: região final mais clara + dobra
        lev_m = np.zeros_like(m)
        if lev['tira'] == i:
            p = lev['ponta']
            ini = p * tira['L'] / 2 - p * 0.12 * tira['L']
            dd = (s - ini) * p
            lev_m = np.clip(dd / (0.03 * tira['L']), 0, 1) * (dd > 0)
            v = v + 0.045 * lev_m - 0.05 * np.exp(-((dd / (0.004 * tira['L'] + 1)) ** 2))
            if sombra:
                sh = (m * lev_m).astype(np.float32)
                off = int(0.006 * S * ss) + 1
                sh = np.roll(np.roll(sh, off, 0), off, 1)
                k = int(0.012 * S * ss) | 1
                sombra_bg = np.maximum(sombra_bg, cv2.GaussianBlur(sh, (k, k), 0) * 0.42)
        if i == topo and (1 - topo) in mascaras:
            # relevo: a tira de cima passa por cima das bordas da de baixo
            s0, t0, W0 = mascaras[1 - topo]
            perto = np.exp(-((np.abs(t0) - W0 / 2) / (0.012 * W0 + 0.6)) ** 2)
            v = v + 0.06 * perto * np.sign(t0) * (np.abs(t0) < W0 * 0.6)
        tinta = base[None, None, :] * (1 + v[..., None])
        tinta = np.where(v[..., None] > 0, tinta + (1 - tinta) * v[..., None] * 0.35, tinta)
        creme = hex2rgb('papel')[None, None, :] * 0.96
        fio_c = (fio > 0)[..., None]
        tinta = np.where(fio_c, base[None, None, :] * 0.35 + creme * 0.65, tinta)
        m = np.maximum(m, fio)
        if i == topo and (1 - topo) in mascaras:
            # sombra da tira de cima sobre a de baixo
            k = int(0.01 * S * ss) | 1
            sh = cv2.GaussianBlur(m, (k, k), 0)
            sh = np.roll(np.roll(sh, int(0.002 * S * ss) + 1, 0), int(0.002 * S * ss) + 1, 1)
            under = alfa > 0
            rgb = np.where(under[..., None], rgb * (1 - 0.16 * np.clip(sh - m, 0, 1))[..., None], rgb)
        rgb = rgb * (1 - m[..., None]) + tinta * m[..., None]
        alfa = alfa + m * (1 - alfa)
        mascaras[i] = (s, t, tiras[i]['W'])
    if sombra:
        k = int(0.006 * S * ss) | 1
        corpo = np.clip(alfa * 1.0, 0, 1)
        contato = cv2.GaussianBlur(np.roll(np.roll(corpo, 2 * ss, 0), ss, 1), (k, k), 0) * 0.09
        sombra_bg = np.maximum(sombra_bg, contato)
    # compõe sombra (preto-palco, semitransparente) por baixo da fita
    preto = hex2rgb('preto')
    a_tot = alfa + sombra_bg * (1 - alfa)
    cor_tot = (rgb * alfa[..., None] + preto[None, None, :] * (sombra_bg * (1 - alfa))[..., None]) / np.maximum(a_tot, 1e-6)[..., None]
    img = np.dstack([np.clip(cor_tot, 0, 1), np.clip(a_tot, 0, 1)])
    img = cv2.resize(img, (S, S), interpolation=cv2.INTER_AREA)
    meta = dict(tamanho=S, semente=semente, razao=razao, fios=fios, topo=topo, ponta_levantada=lev,
                tiras=[dict(cx=round(t['cx'], 2), cy=round(t['cy'], 2), angulo=round(t['ang'], 3),
                            comprimento=round(t['L'], 2), largura=round(t['W'], 2)) for t in tiras])
    return img, meta, tiras


def salvar_png(img, caminho, fundo='transparente'):
    rgba = (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    if fundo != 'transparente':
        bg = Image.new('RGBA', im.size, tuple(int(c * 255) for c in hex2rgb(fundo)) + (255,))
        bg.alpha_composite(im)
        im = bg.convert('RGB')
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    im.save(caminho)


def svg(tiras, topo, S, semente, cor='amarelo', fios=40):
    """SVG vetorial: contorno exato com pontas rasgadas, cor chapada e trama em <pattern>."""
    r = ruido.rng(semente + 1)
    c = CORES.get(cor, cor)
    defs, corpo = [], []
    for i in ([0] if len(tiras) == 1 else [1 - topo, topo]):
        t = tiras[i]
        L, W = t['L'], t['W']
        perf = perfis_pontas(W, r, n=90)
        ts = np.linspace(-0.5, 0.5, len(perf[0])) * W
        pts = [(L / 2 + perf[1][k], ts[k]) for k in range(len(ts))]
        pts += [(-L / 2 + perf[0][k], ts[k]) for k in reversed(range(len(ts)))]
        d = 'M' + ' L'.join(f'{s:.2f},{tt:.2f}' for s, tt in pts) + ' Z'
        pt = W / fios
        defs.append(f'<pattern id="trama{i}" width="{pt:.3f}" height="{pt:.3f}" patternUnits="userSpaceOnUse">'
                    f'<rect width="{pt:.3f}" height="{pt * 0.42:.3f}" fill="#000" fill-opacity="0.05"/>'
                    f'<rect width="{pt * 0.42:.3f}" height="{pt:.3f}" fill="#fff" fill-opacity="0.07"/></pattern>')
        g = (f'<g transform="translate({t["cx"]:.2f} {t["cy"]:.2f}) rotate({-t["ang"]:.3f})">'
             f'<path d="{d}" fill="{c}"/><path d="{d}" fill="url(#trama{i})"/></g>')
        corpo.append(g)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<defs>{"".join(defs)}</defs>{"".join(corpo)}</svg>')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--png')
    ap.add_argument('--svg')
    ap.add_argument('--json')
    ap.add_argument('--tamanho', type=int, default=1024)
    ap.add_argument('--semente', type=int, default=927)
    ap.add_argument('--razao', type=float, default=3.75)
    ap.add_argument('--fios', type=float, default=40)
    ap.add_argument('--cor', default='amarelo')
    ap.add_argument('--fundo', default='transparente')
    ap.add_argument('--sem-sombra', action='store_true')
    ap.add_argument('--uma', action='store_true', help='uma tira só (A TIRA), não o X')
    ap.add_argument('--angulo', type=float, default=-6.0, help='ângulo da tira única, graus')
    a = ap.parse_args()
    img, meta, tiras = gerar(a.tamanho, a.semente, a.razao, a.fios, a.cor, not a.sem_sombra, uma=a.uma, angulo=a.angulo)
    if a.png:
        salvar_png(img, a.png, a.fundo)
        print('A MARCA png', a.png)
    if a.svg:
        open(a.svg, 'w').write(svg(tiras, meta['topo'], a.tamanho, a.semente, a.cor, int(a.fios)))
        print('A MARCA svg', a.svg)
    js = a.json or (os.path.splitext(a.png or a.svg)[0] + '.json' if (a.png or a.svg) else None)
    if js:
        open(js, 'w').write(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
