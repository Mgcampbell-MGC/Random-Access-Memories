"""Contornos do wordmark HOLOFOTE para os templates HTML (holofote.js desenha o SVG).

Reaproveita o shaping de _build/logo.py (HarfBuzz, tracking -10, kerning ligado) sem alterar nada lá.
Separa cada O em contorno externo e contraforma, para a afinação (qualquer combinação de Os acesos).
Saída: _build/brand/wordmark.js  (window.HF_WORDMARK) em unidades da fonte, y para baixo, linha de base em y = 710.
Uso: python wordmark.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import logo  # noqa: E402  (_build/logo.py)


def main():
    glyphs, adv = logo.shape('HOLOFOTE')
    partes, os_ = [], []
    xmin, xmax = 1e9, -1e9
    for name, x, y in glyphs:
        cs = logo.contours(name, x, y)
        for _, b in cs:
            xmin = min(xmin, b[0] + x)
            xmax = max(xmax, b[2] + x)
        if name == 'O':
            outer = max(cs, key=lambda c: (c[1][2] - c[1][0]) * (c[1][3] - c[1][1]))
            inner = [c[0] for c in cs if c is not outer]
            os_.append(dict(ext=outer[0], cont=' '.join(inner)))
            partes.append(dict(o=len(os_) - 1))
        else:
            partes.append(dict(d=' '.join(c[0] for c in cs)))
    data = dict(cap=logo.CAP, adv=adv, inkX0=xmin, inkX1=xmax, partes=partes, Os=os_)
    js = 'window.HF_WORDMARK = ' + json.dumps(data, separators=(',', ':')) + ';\n'
    open(os.path.join(HERE, 'wordmark.js'), 'w').write(js)
    print('wordmark.js: ink', round(xmin), round(xmax), 'largura/cap', round((xmax - xmin) / logo.CAP, 3))


if __name__ == '__main__':
    main()
