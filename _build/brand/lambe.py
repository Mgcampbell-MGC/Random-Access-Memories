"""O LAMBE — o cartaz de papel colado na parede (plataforma §D.4, §D.5 regra 5, §D.6 O MURO).

Toda peça "cartaz" passa por aqui, com uma semente própria. O que ele faz, nesta ordem:
  1. SEPARA AS TINTAS. A arte chapada (cores exatas da paleta) é desmisturada pixel a pixel em papel + uma tinta com
     alfa (a borda antialias de "tinta sobre papel" é sempre a mistura de duas cores da paleta). Pixels que não são
     mistura de duas cores da paleta (ex.: uma miniatura de render) ficam intactos.
  2. REGISTRO. Cada chapa de tinta anda 1–2 px numa direção própria (fora de registro), e a chapa preta ganha uma
     segunda batida fantasma, 1–2 px fora, a 13 % (§D.4: "a 1–2 px ink misregistration").
  3. TINTA. Falhas pontuais (papel aparecendo), mancha de densidade, borda levemente irregular. (O antigo veio de
     tipo de madeira saiu em 6 out 2026: nos chapados pretos grandes lia como linhas de scanner.)
  4. PAPEL. Grão de fibra e manchas de massa do papel barato.
  5. COLA. Rugas da colagem (mapa de altura): vincos soltos, 3–5 vincos direcionais, bolhas e ondas na metade da
     escala de antes (as bolhas de 300–500 px liam como plástico); marcas do pincel; sombreado só no 'assado' (2D).
  6. BORDA. Corte reto com pequenos rasgos e um canto arrancado (quantidade ajustável), em alfa antialias. Todo rasgo
     mostra o miolo do papel: uma faixa de fibra branca de 6–12 px, irregular (fibra_borda). Com folga_tinta, nenhum
     rasgo de borda chega a menos disso de um glifo (cartazes limpos: 40 px).

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
    """Mapa de altura da colagem (0 = plano): vincos, vincos direcionais, bolhas, ondas largas. Escala ~ diagonal.
    Revisão do CCO, 6 out 2026: as bolhas de 300–500 px liam como plástico/lava nas áreas chapadas grandes (fundo dos
    B 9:16, C07, D02) — o campo foi reduzido a ~50 % (bolhas D/18, ondas D/8, borda suave) e entram 3–5 vincos
    DIRECIONAIS (a cola puxada pelo pincel numa direção dominante)."""
    D = math.hypot(H, W)
    vincos = np.zeros((H, W), np.float32)

    def traco(x, y, ang, comp, larg, curva, sinal):
        passos = 24
        pts = []
        for i in range(passos):
            pts.append((x, y))
            ang += r.normal(0, curva)
            x += math.cos(ang) * comp / passos
            y += math.sin(ang) * comp / passos
        lay = np.zeros((H, W), np.float32)
        pts = np.array(pts, np.float32)
        for i in range(passos - 1):      # afina nas pontas: intensidade senoidal
            w = math.sin(math.pi * (i + 0.5) / passos)
            cv2.line(lay, tuple((pts[i] * 16).astype(int)), tuple((pts[i + 1] * 16).astype(int)), float(w),
                     max(1, int(larg * 0.35)), cv2.LINE_AA, shift=4)
        k = int(larg * 2) | 1
        return cv2.GaussianBlur(lay, (k, k), 0) * sinal

    # vincos soltos: polilinhas em passeio aleatório, perfil gaussiano, sinal aleatório
    n = int(r.integers(7, 13) * forca + 2)
    for _ in range(n):
        vincos += traco(r.uniform(0, W), r.uniform(0, H), r.normal(math.radians(r.choice([60, 75, 105, 120, 20, 160])), 0.25),
                        r.uniform(0.06, 0.32) * D, r.uniform(0.0016, 0.006) * D, 0.07,
                        r.choice([-1.0, 1.0]) * r.uniform(0.6, 1.0))
    # vincos direcionais: quase paralelos, longos e finos, numa direção dominante por peça
    dom = r.uniform(0, math.pi)
    for _ in range(int(r.integers(3, 6))):
        vincos += traco(r.uniform(0, W), r.uniform(0, H), dom + r.normal(0, math.radians(7)), r.uniform(0.25, 0.5) * D,
                        r.uniform(0.0012, 0.003) * D, 0.025, r.choice([-1.0, 1.0]) * r.uniform(0.5, 0.85))
    # bolhas de cola: manchas positivas, metade da escala antiga e borda suave (sem platô)
    f = ruido.fractal(H, W, D / 18, r, 3)
    t = np.clip((f - 0.05) / 0.6, 0, 1)
    bolhas = cv2.GaussianBlur(t * t * (3 - 2 * t), (0, 0), max(1.0, D / 450)) * 0.4
    # ondas largas do papel molhado
    ondas = ruido.fractal(H, W, D / 8, r, 2) * 0.45
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


MIOLO = np.array([0.985, 0.975, 0.955], np.float32)       # miolo do papel: o pigmento é só na superfície


def _perfil(n, r, amp, escalas):
    return ruido.perfil_1d(n, r, amp, escalas)


def _amostra(perf, t):
    """Lê o perfil em t (0–1) por interpolação linear (o índice inteiro dava borda em degraus)."""
    n = len(perf)
    x = np.clip(t, 0, 1) * (n - 1)
    i0 = np.floor(x).astype(int)
    i1 = np.minimum(i0 + 1, n - 1)
    f = (x - i0).astype(np.float32)
    return perf[i0] * (1 - f) + perf[i1] * f


def _fibras(h, w, r):
    """Textura de fibra curta: três ruídos esticados (≈ 8 × 1,2 px) em ângulos aleatórios, somados. Média 0, desvio ~1."""
    f = np.zeros((h, w), np.float32)
    for ang in r.uniform(0, 180, 3):
        a = ruido.anisotropico(int(h * 1.45) + 12, int(w * 1.45) + 12, 8.0, 1.2, r)
        M = cv2.getRotationMatrix2D((a.shape[1] / 2, a.shape[0] / 2), float(ang), 1.0)
        a = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), borderMode=cv2.BORDER_REFLECT)
        oy, ox = (a.shape[0] - h) // 2, (a.shape[1] - w) // 2
        f += a[oy:oy + h, ox:ox + w]
    return f / (f.std() + 1e-6)


def fibra_borda(dpap, r, w0=7.0, w1=11.5):
    """Faixa de fibra do rasgo (revisão do CCO, 6 out 2026): dpap = distância em px PARA DENTRO do papel que fica
    (> 0 no papel, ≤ 0 fora). Devolve (alfa, franja): o alfa antialias da borda rasgada, com fibras curtas que passam
    1–3 px da borda, e a franja 0–1 — quanto do miolo branco aparece — numa faixa de w0–w1 px de largura variável,
    com a borda interna desfiada (fibras entrando na tinta) e o miolo um pouco irregular."""
    H, W = dpap.shape
    perto = (dpap < w1 + 8) & (dpap > -8)
    franja = np.zeros((H, W), np.float32)
    alfa = np.clip(dpap + 0.5, 0, 1).astype(np.float32)
    if not perto.any():
        return alfa, franja
    ys, xs = np.where(perto)
    y0, y1, x0, x1 = max(0, ys.min() - 2), min(H, ys.max() + 3), max(0, xs.min() - 2), min(W, xs.max() + 3)
    d = dpap[y0:y1, x0:x1]
    h, w = d.shape
    larg = w0 + (w1 - w0) * np.clip(ruido.valor(h, w, 40, r) * 1.7 + 0.5, 0, 1)        # 6–12 px, varia ao longo do rasgo
    fib = _fibras(h, w, r)                                                              # fibras curtas
    meio = ruido.valor(h, w, 5.0, r) / 0.3                                              # ondulação da borda interna
    borda_int = larg + 1.0 * np.clip(meio, -1.2, 1.2) + 1.5 * np.clip(fib, -0.4, 2.6)  # desfiada: fibras entram na tinta
    fr = np.clip((borda_int - d) / 1.3, 0, 1)
    fr = fr * (0.92 + 0.08 * np.clip(fib * 0.5, -1, 1))                                 # miolo com fibra, quase opaco
    franja[y0:y1, x0:x1] = np.clip(fr, 0, 1) * (d > -6)
    # pelos de fibra passando a borda: só onde a fibra é forte, até ~3 px para fora, semitransparentes
    pelo = np.clip(fib - 1.1, 0, 1.5) / 1.5 * np.clip((d + 3.0) / 3.0, 0, 1)
    alfa[y0:y1, x0:x1] = np.maximum(np.clip(d + 0.5, 0, 1), 0.85 * pelo)
    return alfa, franja


def aplicar_franja(rgb, franja, forca=0.96):
    """Pinta o miolo do papel (quase branco; a fibra já vem na franja) na faixa do rasgo. rgb float HxWx3."""
    f = (np.clip(franja, 0, 1) * forca)[..., None]
    return rgb * (1 - f) + MIOLO * f


def _rasgo_dist(H, W, cx, cy, raio, r, margem=60):
    """Distância (px) para dentro do papel a partir de uma região arrancada em volta de (cx, cy): disco deformado por
    ruído fractal (forma) + fibra fina absoluta (~1 px). Devolve (dpap janela, (y0, y1, x0, x1)); fora da janela = longe."""
    ext = raio * 1.8 + margem
    x0, x1 = int(max(0, cx - ext)), int(min(W, cx + ext))
    y0, y1 = int(max(0, cy - ext)), int(min(H, cy + ext))
    if x1 <= x0 or y1 <= y0:
        return None, None
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    rr = np.hypot(xx - cx, yy - cy)
    n = max(1024, int(2 * math.pi * raio * 1.4))
    t = (ang + np.pi) / (2 * np.pi)
    # forma: lóbulos grandes e médios; o detalhe fino (o que dava a 'estrela de serrote' nos cantos) agora é só a fibra
    forma = 1 + _amostra(_perfil(n, r, 0.35, ((0.2, 1.0), (0.05, 0.45), (0.012, 0.12), (0.004, 0.03))), t)
    fina = _amostra(_perfil(n, r, 1.0, ((4.0 / n, 1.0), (1.6 / n, 0.6))), t)              # ~1 px, período 2–6 px
    lim = raio * forma + 1.2 * fina
    return (rr - lim).astype(np.float32), (y0, y1, x0, x1)


def borda_rasgada(H, W, r, rasgo=0.3, evitar=None, folga=0.0, canto=None):
    """Contorno do cartaz: corte reto quase perfeito + mordidas na borda + (se rasgo>0) um canto arrancado.
    evitar: máscara booleana da tinta; cada rasgo fica a ≥ folga px dela (encolhe, troca de canto ou some).
    Devolve (alfa, franja) — franja = faixa de fibra branca nos rasgos (não no corte reto)."""
    D = math.hypot(H, W)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx + 0.5, W - 0.5 - xx), np.minimum(yy + 0.5, H - 0.5 - yy))
    tremor = 0.6 * ruido.valor(H, W, 30, r)
    corte = np.clip(d + tremor, 0, 1)
    dpap = np.full((H, W), 1e4, np.float32)
    info = []
    # distância euclidiana exata até a tinta: dl (radial) superestima a distância onde a borda é oblíqua ao raio
    dtinta = cv2.distanceTransform((~evitar).astype(np.uint8), cv2.DIST_L2, cv2.DIST_MASK_PRECISE) if evitar is not None else None

    def tenta(cx, cy, raio, rr_):
        """Aceita o rasgo se a tinta toda ficar a ≥ folga px da borda arrancada; senão encolhe."""
        for k in (1.0, 0.85, 0.72, 0.6, 0.5, 0.42):
            st = rr_.bit_generator.state
            dl, jan = _rasgo_dist(H, W, cx, cy, raio * k, rr_)
            if dl is None:
                return False
            if dtinta is not None:
                y0, y1, x0, x1 = jan
                sai = dl < 0.5                                   # o papel que o rasgo arranca
                if sai.any() and dtinta[y0:y1, x0:x1][sai].min() < folga:
                    rr_.bit_generator.state = st
                    continue
            y0, y1, x0, x1 = jan
            dpap[y0:y1, x0:x1] = np.minimum(dpap[y0:y1, x0:x1], dl)
            info.append(dict(cx=round(cx), cy=round(cy), raio=round(raio * k, 1)))
            return True
        return False

    if rasgo > 0:
        for _ in range(int(r.integers(1, 4) + rasgo * 6)):
            lado = int(r.integers(0, 4))
            raio = r.uniform(0.004, 0.02) * D * (0.5 + rasgo)
            if lado in (0, 1):
                cx, cy = (0 if lado == 0 else W), r.uniform(0.05, 0.95) * H
            else:
                cx, cy = r.uniform(0.05, 0.95) * W, (0 if lado == 2 else H)
            tenta(cx, cy, raio, r)
        sorteio = r.random() < 0.55 + 0.4 * rasgo
        if (sorteio if canto is None else canto):          # canto: None = sorteado; True/False = forçado
            cantos = [(0, 0), (W, 0), (0, H), (W, H)]
            i0 = int(r.integers(0, 4))
            raio = r.uniform(0.03, 0.08) * D * (0.6 + rasgo)
            for j in range(4):
                if tenta(*cantos[(i0 + j) % 4], raio, r):
                    break
    alfa_r, franja = fibra_borda(dpap, r)
    borda_rasgada.info = info
    return np.clip(corte * alfa_r, 0, 1), franja


def buraco(H, W, r, cx, cy, rx, ry, rot=0.0, ilhas=1.0):
    """Buraco rasgado num cartaz de cima (para revelar camada antiga): forma orgânica + faixa de fibra (fibra_borda).
    ilhas 0–1: quantidade de pedacinhos do cartaz de cima que ficaram grudados dentro do buraco.
    Devolve (m, franja): m = 1 dentro do buraco; franja = miolo branco na borda do papel de cima que ficou."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c, s = math.cos(rot), math.sin(rot)
    u = ((xx - cx) * c + (yy - cy) * s) / rx
    v = (-(xx - cx) * s + (yy - cy) * c) / ry
    ang = np.arctan2(v, u)
    rr = np.hypot(u, v)
    escala = min(rx, ry)
    n = max(2048, int(2 * math.pi * max(rx, ry) * 1.4))
    t = (ang + np.pi) / (2 * np.pi)
    lim = 1 + _amostra(_perfil(n, r, 0.42, ((0.25, 1.0), (0.07, 0.55), (0.018, 0.25), (0.005, 0.09), (0.002, 0.04))), t)
    fina = _amostra(_perfil(n, r, 1.0, ((4.0 / n, 1.0), (1.6 / n, 0.6))), t)
    dist = (lim - rr) * escala - 1.2 * fina          # px dentro do buraco (+)
    m = np.clip(dist + 0.5, 0, 1)
    if ilhas > 0:
        # ilhas: pedaços do cartaz de cima que ficaram grudados, com borda antialias e franja própria
        f = ruido.fractal(H, W, escala * 0.18, r, 3)
        lim_i = 0.62 - 0.2 * ilhas
        isl = ((f > lim_i) & (dist > escala * 0.05)).astype(np.float32)
        isl = cv2.GaussianBlur(isl, (0, 0), 0.7)
        m = m * (1 - isl)
    # distância para dentro do papel de cima que ficou: fora do buraco, a própria −dist; nas ilhas, a borda delas
    dpap = -dist
    if ilhas > 0:
        dpap = np.where(isl > 0.5, cv2.distanceTransform((isl > 0.5).astype(np.uint8), cv2.DIST_L2, 3), dpap)
    _, franja = fibra_borda(dpap.astype(np.float32), r)
    return m.astype(np.float32), (franja * (1 - m)).astype(np.float32)


def rasgo_linha(H, W, r, p0, p1, amp=0.035, outro=False, faixa=(7.0, 11.5)):
    """Rasgo ao longo da linha p0→p1 (px): devolve (mantém, franja) ou, com outro=True, (mantém, franja, sai, franja_sai).
    'mantém' = alfa do lado ESQUERDO da linha (olhando de p0 para p1); franja = fibra branca do miolo do papel exposta na
    borda rasgada (faixa = largura mín–máx em px, fibra_borda); 'sai'/'franja_sai' = o mesmo no pedaço que sai."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    s = (xx - x0) * ux + (yy - y0) * uy                      # ao longo
    d = (xx - x0) * uy - (yy - y0) * ux                      # distância assinada (− = esquerda)
    n = max(2048, int(L * 1.4))
    t = s / L
    perf = _amostra(_perfil(n, r, amp * L, ((0.14, 1.0), (0.04, 0.38), (0.012, 0.13), (0.004, 0.045), (0.0015, 0.02))), t)
    fina = _amostra(_perfil(n, r, 1.0, ((4.0 / n, 1.0), (1.6 / n, 0.6))), t)
    dist = perf + 1.2 * fina - d                              # >0 = fica
    alfa, franja = fibra_borda(dist.astype(np.float32), r, *faixa)
    mant = alfa
    if outro:
        alfa2, franja2 = fibra_borda((-dist).astype(np.float32), r, *faixa)
        return mant.astype(np.float32), franja.astype(np.float32), alfa2.astype(np.float32), franja2.astype(np.float32)
    return mant.astype(np.float32), franja.astype(np.float32)


def rasgado(topo, antigo, r, buracos=(), cortes=(), sombra=True, ilhas=1.0, amp=0.035):
    """Compõe um cartaz de cima RASGADO sobre um cartaz antigo (mesmo retângulo).
    topo/antigo = tuplas (assado, albedo, altura) de aplicar(). buracos = [(cx, cy, rx, ry, rot)] que revelam o antigo.
    cortes = [(p0, p1)]: rasga o cartaz de cima ao longo da linha (o lado direito sai).
    Devolve (assado, albedo, altura) já compostos; o alfa externo é o do cartaz de cima."""
    ta, tb, th = topo
    aa, ab, ah = antigo
    H, W = th.shape
    furo = np.zeros((H, W), np.float32)
    franja = np.zeros((H, W), np.float32)
    for (cx, cy, rx, ry, rot) in buracos:
        m, f = buraco(H, W, r, cx, cy, rx, ry, rot, ilhas)
        furo = np.maximum(furo, m)
        franja = np.maximum(franja, f)
    for (p0, p1) in cortes:
        m, f = rasgo_linha(H, W, r, p0, p1, amp)
        furo = np.maximum(furo, 1 - m)
        franja = np.maximum(franja, f)
    def junta(t, a, sombrear):
        c = t[..., :3] * (1 - furo[..., None]) + a[..., :3] * furo[..., None]
        if sombrear and sombra:
            # sombra fina da borda do papel de cima sobre o de baixo (luz de cima-esquerda)
            borda = cv2.GaussianBlur(np.roll(np.roll(1 - furo, 3, 0), 2, 1), (0, 0), 2.2)
            c = c * (1 - 0.28 * np.clip(borda - (1 - furo), 0, 1))[..., None]
        c = aplicar_franja(c, franja * (1 - furo))
        alfa = np.maximum(t[..., 3] * (1 - furo), a[..., 3] * furo)
        return np.dstack([np.clip(c, 0, 1), alfa])
    assado = junta(ta, aa, True)
    albedo = junta(tb, ab, False)
    altura = (0.35 + 0.65 * th) * (1 - furo) + 0.35 * ah * furo   # o antigo fica ~0,1 mm abaixo
    return assado, albedo, altura

# ------------------------------------------------------------------ 3. tinta
def textura_tinta(al, r, forca=1.0):
    H, W = al.shape
    nucleo = cv2.erode((al > 0.6).astype(np.uint8), np.ones((3, 3), np.uint8))
    dist = cv2.distanceTransform(nucleo, cv2.DIST_L2, 3)
    # falhas: aglomerados pequenos onde o papel aparece — raros (~1%), quase só no miolo dos chapados
    f = ruido.valor(H, W, 1.4, r) + 0.7 * ruido.valor(H, W, 5.0, r) + 0.5 * ruido.valor(H, W, 40.0, r)
    fs = (f - f.mean()) / (f.std() + 1e-6)
    falhas = np.clip((fs - 2.45) * 2.5, 0, 1) * np.clip((dist - 2) / 6.0, 0, 1)
    # mancha de densidade. A transição borda→miolo tem 2–3 px (o 'squeeze' da tinta na borda do tipo), nunca uma rampa
    # larga: uma rampa de 25 px lê como 'inner glow' digital, não como tinta. O antigo 'veio de madeira' (ruído esticado
    # 160 × 3 px) saiu na revisão do CCO de 6 out 2026: nos chapados pretos grandes (PIX, MÃE do D02) lia como linhas de
    # scanner. A textura de impressão agora é a batida fantasma de 1–2 px (aplicar), como pede o §D.4.
    mancha = np.clip(ruido.fractal(H, W, 70, r, 3) * 1.6, -1, 1) * 0.5 + 0.5          # 0–1
    miolo = np.clip((dist - 1.0) / 2.5, 0, 1)
    dens = 1 - forca * (0.85 * falhas + miolo * 0.035 * mancha)
    # borda irregular (tinta espalha / falha), ~0,5 px — só na borda antialias de verdade (gradiente alto): um véu
    # semitransparente (o brilho da plastificação, uma sombra) não é borda de tinta e não pode virar granulado
    gx = cv2.Sobel(al, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(al, cv2.CV_32F, 0, 1, ksize=3)
    borda = (al > 0.02) & (al < 0.98) & (np.hypot(gx, gy) > 0.35)
    jit = ruido.valor(H, W, 1.8, r) * 0.28 * min(1.0, forca)
    al2 = np.where(borda, np.clip(al + jit, 0, 1), al)
    return np.clip(al2 * dens, 0, 1)


def deslocar(a, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)


# ------------------------------------------------------------------ aplicar
def envelhecer(out, r, idade, papel):
    """Cartaz de camada antiga: sol desbota (menos saturação, mais claro) de forma manchada, um pouco de sujeira."""
    H, W, _ = out.shape
    k = idade * (0.55 + 0.45 * np.clip(ruido.fractal(H, W, max(H, W) / 5, r, 3) + 0.5, 0, 1))[..., None]
    lum = (out @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    sat = 1 - 0.38 * k
    desb = lum + (out - lum) * sat
    desb = desb + (1 - desb) * 0.16 * k                                   # clareia (UV + chuva)
    amarelado = np.array([1.0, 0.985, 0.94], np.float32)                  # o papel amarela
    desb = desb * (1 - 0.35 * k) + desb * amarelado * 0.35 * k
    sujeira = np.clip(ruido.fractal(H, W, 140, r, 4) * 1.4, 0, 1)
    escorrido = np.clip(ruido.anisotropico(H + 4, W + 4, 6.0, 260.0, r)[:H, :W], 0, 1)  # marcas verticais de chuva
    desb = desb * (1 - idade * (0.05 * sujeira + 0.035 * escorrido))[..., None]
    return np.clip(desb, 0, 1)


def aplicar(img, papel, semente=7, rasgo=0.3, rugas=1.0, registro=2.0, grao=1.0, tinta=1.0, borda=True, idade=0.0,
            folga_tinta=None, canto=None):
    """img: HxWx3 uint8 ou float. Devolve (assado RGBA float, albedo RGBA float, altura float 0–1, info).
    idade 0–1: cartaz de camada antiga (desbotado, sujo, mais enrugado).
    folga_tinta (px): nenhum rasgo de borda chega a menos disso de um glifo (cartazes limpos: 40)."""
    r = ruido.rng(semente)
    im = img.astype(np.float32) / (255.0 if img.dtype == np.uint8 else 1.0)
    H, W, _ = im.shape
    chapas, estranho = separar(im, papel)
    pap = rgb(papel)
    out = np.empty_like(im)
    out[:] = pap
    info = dict(semente=semente, chapas={}, papel=papel, idade=idade)
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
        if n == 'preto' and registro > 0:
            # a batida fantasma (§D.4: registro de 1–2 px): uma segunda impressão fraca da chapa preta, 1–2 px fora
            ga = r.uniform(0, 2 * math.pi)
            gm = r.uniform(1.0, 2.0)
            fan = deslocar(al, math.cos(ga) * gm, math.sin(ga) * gm) * 0.13
            out = out * (1 - fan[..., None]) + cor * fan[..., None]
            info['fantasma'] = dict(dx=round(math.cos(ga) * gm, 2), dy=round(math.sin(ga) * gm, 2), opacidade=0.13)
        out = out * (1 - al[..., None]) + cor * al[..., None]
        info['chapas'][n] = dict(dx=round(dx, 2), dy=round(dy, 2))
    out = np.where(estranho[..., None], im, out)
    if idade > 0:
        out = envelhecer(out, r, idade, papel)
        rugas = rugas * (1 + 0.6 * idade)
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
    if borda:
        evitar = None
        if folga_tinta:
            evitar = np.zeros((H, W), bool)
            for al in chapas.values():
                evitar |= al > 0.12
            evitar |= estranho
        alfa, franja = borda_rasgada(H, W, r, rasgo, evitar=evitar, folga=folga_tinta or 0.0, canto=canto)
        info['rasgos'] = list(getattr(borda_rasgada, 'info', []))
        assado = aplicar_franja(assado, franja)
        albedo = aplicar_franja(albedo, franja)
    else:
        alfa = np.ones((H, W), np.float32)
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
    a, _ = borda_rasgada(H, W, r, 0.35)
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
