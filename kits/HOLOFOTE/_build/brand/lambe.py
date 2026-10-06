"""O LAMBE — o cartaz de papel colado na parede (plataforma §D.4, §D.5 regra 5, §D.6 O MURO).

Toda peça "cartaz" passa por aqui, com uma semente própria. O que ele faz, nesta ordem:
  1. SEPARA AS TINTAS. A arte chapada (cores exatas da paleta) é desmisturada pixel a pixel em papel + uma tinta com
     alfa (a borda antialias de "tinta sobre papel" é sempre a mistura de duas cores da paleta). Pixels que não são
     mistura de duas cores da paleta (ex.: uma miniatura de render) ficam intactos.
  2. REGISTRO. Cada chapa de tinta anda 1–2 px numa direção própria (fora de registro), e a chapa preta ganha uma
     segunda batida fantasma de 1 px a ~10% (o 'slur' da impressão barata).
  3. TINTA. Falhas pontuais (papel aparecendo), mancha de densidade, veio de tipo de madeira nos chapados grandes,
     borda levemente irregular.
  4. PAPEL. Grão de fibra e manchas de massa do papel barato.
  5. COLA. Rugas da colagem (mapa de altura), marcas do pincel de cola; sombreado só na versão 'assada' (2D).
  6. BORDA. Corte reto com pequenos rasgos e um canto arrancado (quantidade ajustável), em alfa.

Saídas de aplicar(): RGBA 'assado' (2D), RGBA 'albedo' (3D: sem sombreado de ruga) e mapa de altura 16 bits.
Overlays soltos para CSS/compositing: python lambe.py overlays LxA --semente N --pasta destino/

Uso:
  python lambe.py aplicar entrada.png saida.png --papel amarelo [--semente 7] [--rasgo 0.3] [--rugas 1.0]
                         [--registro 2] [--albedo saida_albedo.png] [--altura saida_altura.png]
  python lambe.py overlays 1080x1350 --semente 7 --pasta ../../01_MARCA/lambe/
"""
import argparse, math, os, sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ruido  # noqa: E402

PALETA = dict(preto='#121014', papel='#FFF8EC', amarelo='#FFE81A', rosa='#FF4FA0', laranja='#FF6A1A',
              violeta='#8424F5')
ORDEM_IMPRESSAO = ['papel', 'amarelo', 'rosa', 'laranja', 'violeta', 'preto']   # claras primeiro, preto por último


def rgb(h):
    h = PALETA.get(h, h).lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


# ------------------------------------------------------------------ 1. separação de tintas
def separar(img, papel, tol=10 / 255):
    """img float HxWx3 (0–1). Devolve {tinta: alfa HxW}, máscara 'estranho' (pixels fora da paleta)."""
    H, W, _ = img.shape
    pap = rgb(papel)
    nomes = [n for n in PALETA if n != papel]
    melhor_res = np.full((H, W), 9.0, np.float32)
    melhor_t = np.zeros((H, W), np.float32)
    melhor_k = np.full((H, W), -1, np.int16)
    for k, n in enumerate(nomes):
        a = rgb(n)
        d = a - pap
        t = np.clip(((img - pap) @ d) / float(d @ d), 0, 1)
        res = np.linalg.norm(img - (pap + t[..., None] * d), axis=2)
        m = res < melhor_res
        melhor_res[m], melhor_t[m], melhor_k[m] = res[m], t[m], k
    estranho = melhor_res > tol
    chapas = {}
    for k, n in enumerate(nomes):
        al = np.where((melhor_k == k) & ~estranho, melhor_t, 0).astype(np.float32)
        if al.max() > 0.02:
            chapas[n] = al
    return chapas, estranho


# ------------------------------------------------------------------ texturas
def grao_papel(H, W, r):
    """Grão do papel barato: fibra fina + fibras orientadas + manchas de massa. Média 0, ~±1."""
    fino = ruido.valor(H, W, 1.3, r)
    fibras = np.zeros((H, W), np.float32)
    for ang in r.uniform(0, 180, 4):
        a = ruido.anisotropico(int(H * 1.5) + 8, int(W * 1.5) + 8, 9.0, 1.4, r)
        M = cv2.getRotationMatrix2D((a.shape[1] / 2, a.shape[0] / 2), float(ang), 1.0)
        a = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), borderMode=cv2.BORDER_REFLECT)
        oy, ox = (a.shape[0] - H) // 2, (a.shape[1] - W) // 2
        fibras += a[oy:oy + H, ox:ox + W] * 0.5
    massa = ruido.fractal(H, W, max(H, W) / 14, r, 4)
    return 0.45 * fino + 0.35 * fibras + 0.55 * massa


def mapa_rugas(H, W, r, forca=1.0):
    """Mapa de altura da colagem (0 = plano): vincos longos, bolhas, ondas largas. Escala ~ diagonal do cartaz."""
    D = math.hypot(H, W)
    h = np.zeros((H, W), np.float32)
    # vincos: polilinhas em passeio aleatório, perfil gaussiano, sinal aleatório
    vincos = np.zeros((H, W), np.float32)
    n = int(r.integers(7, 13) * forca + 2)
    for _ in range(n):
        x, y = r.uniform(0, W), r.uniform(0, H)
        ang = r.normal(math.radians(r.choice([60, 75, 105, 120, 20, 160])), 0.25)
        comp = r.uniform(0.06, 0.32) * D
        passos = 24
        pts = []
        for i in range(passos):
            pts.append((x, y))
            ang += r.normal(0, 0.07)
            x += math.cos(ang) * comp / passos
            y += math.sin(ang) * comp / passos
        larg = r.uniform(0.0016, 0.006) * D
        lay = np.zeros((H, W), np.float32)
        pts = np.array(pts, np.float32)
        # afina nas pontas: desenha segmentos com intensidade senoidal
        for i in range(passos - 1):
            w = math.sin(math.pi * (i + 0.5) / passos)
            cv2.line(lay, tuple((pts[i] * 16).astype(int)), tuple((pts[i + 1] * 16).astype(int)), float(w),
                     max(1, int(larg * 0.35)), cv2.LINE_AA, shift=4)
        k = int(larg * 2) | 1
        lay = cv2.GaussianBlur(lay, (k, k), 0)
        vincos += lay * r.choice([-1.0, 1.0]) * r.uniform(0.6, 1.0)
    # bolhas de cola: manchas suaves positivas
    bolhas = np.clip(ruido.fractal(H, W, D / 9, r, 3) - 0.18, 0, None) * 2.2
    # ondas largas do papel molhado
    ondas = ruido.fractal(H, W, D / 4, r, 2) * 0.6
    h = vincos * 1.0 + bolhas * 0.8 + ondas
    return h * forca


def sombreado(h, luz=(-0.55, -0.75)):
    """Sombreado lambertiano do mapa de altura (luz de cima-esquerda, flash um pouco acima da lente)."""
    gy, gx = np.gradient(cv2.GaussianBlur(h, (0, 0), 1.2))
    lx, ly = luz
    s = -(gx * lx + gy * ly)
    return s / (np.percentile(np.abs(s), 99.5) + 1e-6)


def marcas_pincel(H, W, r):
    """Brilho do pincel de cola passado por cima do cartaz: faixas largas quase horizontais."""
    a = ruido.anisotropico(int(H * 1.3) + 8, int(W * 1.3) + 8, W / 3.0, H / 60.0, r)
    M = cv2.getRotationMatrix2D((a.shape[1] / 2, a.shape[0] / 2), float(r.uniform(-12, 12)), 1.0)
    a = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), borderMode=cv2.BORDER_REFLECT)
    oy, ox = (a.shape[0] - H) // 2, (a.shape[1] - W) // 2
    return np.clip(a[oy:oy + H, ox:ox + W], 0, None)


def borda_rasgada(H, W, r, rasgo=0.3):
    """Alfa do contorno: corte reto quase perfeito + mordidas na borda + (se rasgo>0) um canto arrancado."""
    D = math.hypot(H, W)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx + 0.5, W - 0.5 - xx), np.minimum(yy + 0.5, H - 0.5 - yy))
    tremor = 0.6 * ruido.valor(H, W, 30, r)
    alfa = np.clip(d + tremor, 0, 1)
    if rasgo > 0:
        # mordidas: semicírculos irregulares na borda
        for _ in range(int(r.integers(1, 4) + rasgo * 6)):
            lado = int(r.integers(0, 4))
            raio = r.uniform(0.004, 0.02) * D * (0.5 + rasgo)
            if lado in (0, 1):
                cx, cy = (0 if lado == 0 else W), r.uniform(0.05, 0.95) * H
            else:
                cx, cy = r.uniform(0.05, 0.95) * W, (0 if lado == 2 else H)
            alfa *= 1 - _mancha_rasgo(H, W, cx, cy, raio, r)
        # canto arrancado
        if r.random() < 0.55 + 0.4 * rasgo:
            cx, cy = r.choice([0, W]), r.choice([0, H])
            raio = r.uniform(0.03, 0.08) * D * (0.6 + rasgo)
            alfa *= 1 - _mancha_rasgo(H, W, cx, cy, raio, r)
    return np.clip(alfa, 0, 1)


def _mancha_rasgo(H, W, cx, cy, raio, r):
    """Região arrancada: disco deformado por ruído fractal (borda de papel rasgado), suavizada 0,7 px."""
    x0, x1 = int(max(0, cx - raio * 1.8)), int(min(W, cx + raio * 1.8))
    y0, y1 = int(max(0, cy - raio * 1.8)), int(min(H, cy + raio * 1.8))
    m = np.zeros((H, W), np.float32)
    if x1 <= x0 or y1 <= y0:
        return m
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    rr = np.hypot(xx - cx, yy - cy)
    n = 512
    perf = 1 + ruido.perfil_1d(n, r, 0.35, ((0.2, 1.0), (0.05, 0.5), (0.012, 0.35), (0.004, 0.2)))
    idx = ((ang + np.pi) / (2 * np.pi) * (n - 1)).astype(int)
    lim = raio * perf[idx]
    m[y0:y1, x0:x1] = np.clip((lim - rr) + 0.5, 0, 1)
    return m


def buraco(H, W, r, cx, cy, rx, ry, rot=0.0):
    """Buraco rasgado num cartaz de cima (para revelar camada antiga): forma orgânica + franja de fibra."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c, s = math.cos(rot), math.sin(rot)
    u = ((xx - cx) * c + (yy - cy) * s) / rx
    v = (-(xx - cx) * s + (yy - cy) * c) / ry
    ang = np.arctan2(v, u)
    rr = np.hypot(u, v)
    n = 1024
    perf = 1 + ruido.perfil_1d(n, r, 0.42, ((0.25, 1.0), (0.07, 0.6), (0.018, 0.4), (0.005, 0.25)))
    idx = ((ang + np.pi) / (2 * np.pi) * (n - 1)).astype(int)
    lim = perf[idx]
    escala = min(rx, ry)
    dist = (lim - rr) * escala            # px dentro do buraco (+)
    m = np.clip(dist + 0.5, 0, 1)
    # ilhas: pedaços do cartaz de cima que ficaram grudados
    ilhas = (ruido.fractal(H, W, escala * 0.18, r, 3) > 0.42) & (dist > escala * 0.05)
    m = np.where(ilhas, m * 0.0, m)
    franja = np.clip(1 - np.abs(dist + escala * 0.012) / (escala * 0.014), 0, 1) * (dist < 0.5)
    fibra = np.clip(ruido.valor(H, W, 1.5, r) * 1.5 + 0.6, 0, 1)
    return m.astype(np.float32), (franja * fibra).astype(np.float32)


# ------------------------------------------------------------------ 3. tinta
def textura_tinta(al, r, forca=1.0):
    H, W = al.shape
    nucleo = cv2.erode((al > 0.6).astype(np.uint8), np.ones((3, 3), np.uint8))
    dist = cv2.distanceTransform(nucleo, cv2.DIST_L2, 3)
    # falhas: aglomerados pequenos onde o papel aparece — raros (~1%), quase só no miolo dos chapados
    f = ruido.valor(H, W, 1.4, r) + 0.7 * ruido.valor(H, W, 5.0, r) + 0.5 * ruido.valor(H, W, 40.0, r)
    fs = (f - f.mean()) / (f.std() + 1e-6)
    falhas = np.clip((fs - 2.45) * 2.5, 0, 1) * np.clip((dist - 2) / 6.0, 0, 1)
    # mancha de densidade e veio de madeira (só nos chapados grandes)
    mancha = np.clip(ruido.fractal(H, W, 90, r, 3), -1, 1)
    veio = ruido.anisotropico(H + 4, W + 4, 120.0, 2.2, r)[:H, :W]
    grande = np.clip((dist - 10) / 25, 0, 1)
    dens = 1 - forca * (0.85 * falhas + 0.03 * (mancha + 1) * grande + 0.045 * np.clip(veio, 0, None) * grande)
    # borda irregular (tinta espalha / falha), ~0,5 px
    borda = (al > 0.02) & (al < 0.98)
    jit = ruido.valor(H, W, 1.8, r) * 0.28
    al2 = np.where(borda, np.clip(al + jit, 0, 1), al)
    return np.clip(al2 * dens, 0, 1)


def deslocar(a, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)


# ------------------------------------------------------------------ aplicar
def aplicar(img, papel, semente=7, rasgo=0.3, rugas=1.0, registro=2.0, grao=1.0, tinta=1.0, borda=True):
    """img: HxWx3 uint8 ou float. Devolve (assado RGBA float, albedo RGBA float, altura float 0–1, info)."""
    r = ruido.rng(semente)
    im = img.astype(np.float32) / (255.0 if img.dtype == np.uint8 else 1.0)
    H, W, _ = im.shape
    chapas, estranho = separar(im, papel)
    pap = rgb(papel)
    out = np.empty_like(im)
    out[:] = pap
    info = dict(semente=semente, chapas={}, papel=papel)
    for n in ORDEM_IMPRESSAO:
        if n not in chapas:
            continue
        al = chapas[n]
        ang = r.uniform(0, 2 * math.pi)
        mag = registro * r.uniform(0.5, 1.0)
        dx, dy = mag * math.cos(ang), mag * math.sin(ang)
        al = deslocar(al, dx, dy)
        al = textura_tinta(al, r, tinta)
        cor = rgb(n)
        if n == 'preto' and registro > 0:      # segunda batida fantasma
            fan = deslocar(al, -dx * 0.6 + 0.8, -dy * 0.6 + 0.8) * 0.10
            out = out * (1 - fan[..., None]) + cor * fan[..., None]
        out = out * (1 - al[..., None]) + cor * al[..., None]
        info['chapas'][n] = dict(dx=round(dx, 2), dy=round(dy, 2))
    out = np.where(estranho[..., None], im, out)
    # papel: grão (mais no papel que na tinta)
    g = grao_papel(H, W, r)
    lum_tinta = 1 - np.clip(np.linalg.norm(out - pap, axis=2) * 1.5, 0, 1)
    amp = grao * (0.016 + 0.014 * lum_tinta)
    out = out * (1 + amp[..., None] * g[..., None])
    # cola
    h = mapa_rugas(H, W, r, rugas) if rugas > 0 else np.zeros((H, W), np.float32)
    albedo = np.clip(out, 0, 1)
    pincel = marcas_pincel(H, W, r)
    sh = sombreado(h) if rugas > 0 else np.zeros((H, W), np.float32)
    assado = albedo * (1 + 0.085 * sh[..., None]) + (0.035 * rugas) * pincel[..., None] * (1 - albedo) * 0.6
    assado = np.where(sh[..., None] > 0, assado + (1 - assado) * 0.025 * sh[..., None], assado)
    alfa = borda_rasgada(H, W, r, rasgo) if borda else np.ones((H, W), np.float32)
    hn = (h - h.min()) / (h.max() - h.min() + 1e-6) if rugas > 0 else np.full((H, W), 0.5, np.float32)
    A = lambda c: np.dstack([np.clip(c, 0, 1), alfa])
    return A(assado), A(albedo), hn, info


def ler(caminho):
    return np.asarray(Image.open(caminho).convert('RGB'))


def salvar(arr, caminho):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    if arr.ndim == 2:
        Image.fromarray((np.clip(arr, 0, 1) * 65535).astype(np.uint16)).save(caminho)
        return
    a8 = (np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(a8, 'RGBA' if a8.shape[2] == 4 else 'RGB').save(caminho, optimize=False, compress_level=6)


def overlays(W, H, semente, pasta):
    """Camadas soltas para CSS/compositing (cinza 50% = neutro)."""
    r = ruido.rng(semente)
    g = grao_papel(H, W, r)
    h = mapa_rugas(H, W, r, 1.0)
    sh = sombreado(h)
    p = marcas_pincel(H, W, r)
    a = borda_rasgada(H, W, r, 0.35)
    base = f'LAMBE_{W}x{H}_s{semente}'
    salvar(np.dstack([np.clip(0.5 + 0.05 * g, 0, 1)] * 3), os.path.join(pasta, base + '_grao.png'))
    salvar(np.dstack([np.clip(0.5 + 0.18 * sh + 0.05 * p, 0, 1)] * 3), os.path.join(pasta, base + '_rugas.png'))
    salvar(np.dstack([np.ones((H, W, 3), np.float32), a]), os.path.join(pasta, base + '_borda.png'))
    salvar((h - h.min()) / (h.max() - h.min() + 1e-6), os.path.join(pasta, base + '_altura16.png'))
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd')
    a1 = sub.add_parser('aplicar')
    a1.add_argument('entrada')
    a1.add_argument('saida')
    a1.add_argument('--papel', required=True)
    a1.add_argument('--semente', type=int, default=7)
    a1.add_argument('--rasgo', type=float, default=0.3)
    a1.add_argument('--rugas', type=float, default=1.0)
    a1.add_argument('--registro', type=float, default=2.0)
    a1.add_argument('--sem-borda', action='store_true')
    a1.add_argument('--albedo')
    a1.add_argument('--altura')
    a2 = sub.add_parser('overlays')
    a2.add_argument('tamanho')
    a2.add_argument('--semente', type=int, default=7)
    a2.add_argument('--pasta', required=True)
    a = ap.parse_args()
    if a.cmd == 'aplicar':
        assado, albedo, h, info = aplicar(ler(a.entrada), a.papel, a.semente, a.rasgo, a.rugas, a.registro,
                                          borda=not a.sem_borda)
        salvar(assado, a.saida)
        if a.albedo:
            salvar(albedo, a.albedo)
        if a.altura:
            salvar(h, a.altura)
        print('O LAMBE', a.saida, info)
    elif a.cmd == 'overlays':
        W, H = map(int, a.tamanho.split('x'))
        print('overlays', overlays(W, H, a.semente, a.pasta))
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
