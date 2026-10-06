"""Render the KV type layers (kv.html) for every format. Transparent PNGs by default; --preview puts them on preto.
    /home/user/venvs/web/bin/python tipo_kv.py OUTDIR [--preview]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'brand'))
from render import renderizar

SIZES = {'9x16': (1080, 1920), '4x5': (1080, 1350), '1x1': (1080, 1080), '16x9': (1920, 1080), 'kv45': (1080, 1920),
         'card': (1080, 1920)}


def job(fmt, out, dados=None, preview=False, plate=None):
    w, h = SIZES[fmt]
    d = dict(fmt=fmt, **(dados or {}))
    if preview:
        d['fundo'] = 'preto'
    if plate:
        d['plate'] = 'file://' + os.path.abspath(plate)
    return dict(html=os.path.join(HERE, 'kv.html'), saida=out, w=w, h=h, dados=d, transparente=not (preview or plate))


if __name__ == '__main__':
    outdir = sys.argv[1]
    pv = '--preview' in sys.argv
    jobs = [job(f, os.path.join(outdir, f'KV-01_{f}_tipo.png'), preview=pv) for f in ('9x16', '4x5', '1x1', '16x9')]
    for hl, tag in (('SUA VEZ.', 'SUA-VEZ'), ('A ATRAÇÃO É ELA.', 'A-ATRACAO-E-ELA'), (None, 'sem-titulo')):
        jobs.append(job('kv45', os.path.join(outdir, f'KV-45_tipo_{tag}.png'), dict(headline=hl), preview=pv))
    res = renderizar(jobs)
    print(json.dumps([r['qa'] for r in res], ensure_ascii=False))
