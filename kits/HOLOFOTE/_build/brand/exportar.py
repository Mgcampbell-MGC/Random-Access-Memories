"""Exporta os ativos da marca que os outros times reaproveitam, em 01_MARCA/:
    marca/   A MARCA (o X de fita gaffer) e A TIRA (uma fita só): PNG 2048 transparente + SVG + JSON de geometria
    lambe/   O LAMBE em camadas soltas (grão, rugas, borda rasgada, altura 16 bits) nos tamanhos da campanha
    logo/png/  os SVGs aprovados de logo/ e O FOCO rasterizados em PNG (2400 px de largura), sem mexer nos SVGs
Uso: /home/user/venvs/web/bin/python _build/brand/exportar.py
"""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import marca, lambe  # noqa: E402

KIT = os.path.dirname(os.path.dirname(AQUI))
M = os.path.join(KIT, '01_MARCA')


def marcas():
    out = os.path.join(M, 'marca')
    os.makedirs(out, exist_ok=True)
    for nome, kw in (('A-MARCA_X_s927', dict(semente=927)), ('A-MARCA_X_s4', dict(semente=4)),
                     ('A-TIRA_s31', dict(semente=31, uma=True, angulo=-7.0))):
        img, meta, tiras = marca.gerar(2048, **kw)
        marca.salvar_png(img, os.path.join(out, nome + '.png'))
        marca.salvar_png(img, os.path.join(out, nome + '_sobre-preto.png'), 'preto')
        open(os.path.join(out, nome + '.svg'), 'w').write(marca.svg(tiras, meta['topo'], 2048, kw['semente']))
        json.dump(meta, open(os.path.join(out, nome + '.json'), 'w'), ensure_ascii=False, indent=1)
        print('marca', nome)


def overlays():
    out = os.path.join(M, 'lambe')
    os.makedirs(out, exist_ok=True)
    for tam, s in (('1080x1080', 11), ('1080x1350', 12), ('1080x1920', 13), ('2000x3000', 14)):
        W, H = map(int, tam.split('x'))
        print('lambe', lambe.overlays(W, H, s, out))


def logos():
    from render import renderizar
    out = os.path.join(M, 'logo', 'png')
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(AQUI, 'cache', 'svg2png')
    os.makedirs(tmp, exist_ok=True)
    jobs = []
    for svg in sorted(glob.glob(os.path.join(M, 'logo', '*.svg'))):
        vb = open(svg).read().split('viewBox="')[1].split('"')[0].split()
        w0, h0 = float(vb[2]), float(vb[3])
        W = 2400 if 'logo' in os.path.basename(svg) else 1200
        H = round(W * h0 / w0)
        html = os.path.join(tmp, os.path.basename(svg) + '.html')
        open(html, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}'
                              f'img{{display:block;width:{W}px;height:{H}px}}</style></head><body>'
                              f'<img src="file://{svg}"><script>window.HF_PRONTO=true</script></body></html>')
        jobs.append(dict(html=html, saida=os.path.join(out, os.path.basename(svg)[:-4] + '.png'), w=W, h=H, transparente=True))
    renderizar(jobs, verbose=False)
    print('logo png', len(jobs))


if __name__ == '__main__':
    marcas()
    overlays()
    logos()
