"""LIVRO DA MARCA · 16 pranchas 1920 × 1080 em 01_MARCA/livro/ + 01_MARCA/placeholders.json.
Uso: /home/user/venvs/web/bin/python _build/brand/livro.py [n …]
Depende das peças já geradas (cartazes.py, lancamento.py, exportar.py): as pranchas mostram os arquivos reais.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from render import renderizar  # noqa: E402

KIT = os.path.dirname(os.path.dirname(AQUI))
OUT = os.path.join(KIT, '01_MARCA', 'livro')
NOMES = {1: 'CAPA', 2: 'A-IDEIA', 3: 'O-INSIGHT', 4: 'AS-TRES-VOZES', 5: 'O-LOGO', 6: 'CORES-E-A-AFINACAO', 7: 'O-FOCO-E-A-MARCA',
         8: 'PALETA', 9: 'TIPOGRAFIA-I', 10: 'TIPOGRAFIA-II', 11: 'AS-SETE-REGRAS', 12: 'AS-DUAS-LUZES', 13: 'DISPOSITIVOS-I',
         14: 'DISPOSITIVOS-II', 15: 'NUNCA', 16: 'SUA-VEZ'}


def main():
    ns = [int(a) for a in sys.argv[1:]] or sorted(NOMES)
    os.makedirs(OUT, exist_ok=True)
    jobs = [dict(html=os.path.join(AQUI, 'livro.html'), saida=os.path.join(OUT, f'LIVRO-{n:02d}_{NOMES[n]}.png'), w=1920, h=1080,
                 dados=dict(n=n, kit='file://' + KIT + '/'), espera=300) for n in ns]
    res = renderizar(jobs, verbose=False)
    pj = os.path.join(KIT, '01_MARCA', 'placeholders.json')
    ph = json.load(open(pj)) if os.path.exists(pj) else {}
    for n, j, r in zip(ns, jobs, res):
        nome = os.path.basename(j['saida'])
        for k in [k for k in ph if k.split('::')[0] == nome]:
            del ph[k]
        for q in r['placeholders']:
            chave = nome if len(r['placeholders']) == 1 else f"{nome}::{q['id']}"
            ph[chave] = [round(q['x']), round(q['y']), round(q['w']), round(q['h'])]
        ruins = [q for q in r['qa'] if abs(q.get('erro', 0)) > 0.5]
        print(nome, ('QA ' + str(ruins)) if ruins else '', ('console ' + ' | '.join(r['console'])) if r['console'] else '')
    json.dump(dict(sorted(ph.items())), open(pj, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
