"""Ruídos procedurais determinísticos (semente) para A MARCA e O LAMBE. Só numpy + OpenCV."""
import numpy as np
import cv2


def rng(semente):
    return np.random.default_rng(int(semente) & 0xFFFFFFFF)


def valor(h, w, escala, r, interp=cv2.INTER_CUBIC):
    """Ruído de valor: grade aleatória de passo `escala` px, interpolada para h×w. Média ~0, desvio ~0,3."""
    gh, gw = max(2, int(np.ceil(h / escala)) + 3), max(2, int(np.ceil(w / escala)) + 3)
    g = r.standard_normal((gh, gw)).astype(np.float32)
    big = cv2.resize(g, (int(gw * escala), int(gh * escala)), interpolation=interp)
    oy, ox = r.integers(0, max(1, big.shape[0] - h)), r.integers(0, max(1, big.shape[1] - w))
    return big[oy:oy + h, ox:ox + w]


def fractal(h, w, escala, r, oitavas=4, ganho=0.5, lac=2.0):
    out = np.zeros((h, w), np.float32)
    a, s, tot = 1.0, float(escala), 0.0
    for _ in range(oitavas):
        out += a * valor(h, w, max(1.0, s), r)
        tot += a
        a *= ganho
        s /= lac
    return out / tot


def anisotropico(h, w, escala_x, escala_y, r):
    """Ruído esticado (fibras, veio de madeira): escala diferente em x e y."""
    gh, gw = max(2, int(np.ceil(h / escala_y)) + 3), max(2, int(np.ceil(w / escala_x)) + 3)
    g = r.standard_normal((gh, gw)).astype(np.float32)
    big = cv2.resize(g, (int(gw * escala_x), int(gh * escala_y)), interpolation=cv2.INTER_CUBIC)
    return big[:h, :w]


def perfil_1d(n, r, amp, escalas=((0.25, 1.0), (0.06, 0.45), (0.015, 0.22))):
    """Perfil 1D fractal (borda rasgada), n amostras, amplitude `amp`."""
    out = np.zeros(n, np.float64)
    for frac, peso in escalas:
        k = max(2, int(1 / frac))
        pts = r.standard_normal(k + 3)
        xs = np.linspace(0, k, n)
        out += peso * np.interp(xs, np.arange(k + 3), pts)
    out /= max(1e-6, np.abs(out).max())
    return out * amp
