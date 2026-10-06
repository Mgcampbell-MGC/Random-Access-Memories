"""HTML → PNG em lote, com dados no hash da URL, esperando o motor de layout (window.HF_PRONTO).

Uso (linha de comando):
  python render.py pagina.html saida.png 1080x1350 ['{"chave": "valor"}'] [--transparente]
Uso (Python):
  from render import renderizar
  renderizar([dict(html=..., saida=..., w=1080, h=1350, dados={...}, transparente=False)])
Cada job devolve {'placeholders': [...], 'qa': [...]} lidos da página (HF.placeholders, window.HF_QA).
"""
import json, os, sys, urllib.parse
from playwright.sync_api import sync_playwright

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')


def renderizar(jobs, verbose=True):
    res = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--font-render-hinting=none', '--disable-lcd-text',
                                                             '--allow-file-access-from-files'])
        for j in jobs:
            w, h = int(j['w']), int(j['h'])
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=j.get('escala', 1))
            msgs = []
            pg.on('console', lambda m: msgs.append(m.text) if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e: msgs.append('pageerror: ' + str(e)))
            url = 'file://' + os.path.abspath(j['html'])
            if j.get('dados'):
                url += '#' + urllib.parse.quote(json.dumps(j['dados'], ensure_ascii=False))
            pg.goto(url)
            pg.wait_for_function('window.HF_PRONTO === true', timeout=120000)
            pg.wait_for_timeout(j.get('espera', 150))
            erro = pg.evaluate("document.body.getAttribute('data-erro')")
            if erro:
                raise RuntimeError(f"{j['html']}: {erro}")
            os.makedirs(os.path.dirname(os.path.abspath(j['saida'])), exist_ok=True)
            pg.screenshot(path=j['saida'], omit_background=j.get('transparente', False),
                          clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            info = pg.evaluate("({placeholders: (window.HF && HF.placeholders) || [], qa: window.HF_QA || []})")
            info['console'] = msgs
            res.append(info)
            if verbose:
                ruim = [q for q in info['qa'] if abs(q.get('erro', 0)) > 0.5]
                print('render', os.path.relpath(j['saida']), f'{w}x{h}', ('QA>0,5px: ' + str(ruim)) if ruim else '',
                      ('console: ' + ' | '.join(msgs)) if msgs else '')
            pg.close()
        b.close()
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    tr = '--transparente' in a
    pos = [x for x in a if not x.startswith('--')]
    w, h = map(int, pos[2].split('x'))
    dados = json.loads(pos[3]) if len(pos) > 3 else None
    print(json.dumps(renderizar([dict(html=pos[0], saida=pos[1], w=w, h=h, dados=dados, transparente=tr)])[0],
                     ensure_ascii=False)[:2000])
