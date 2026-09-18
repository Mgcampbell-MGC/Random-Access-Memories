# -*- coding: utf-8 -*-
import re, os, base64, subprocess, pathlib, urllib.request

CSS = open('fonts/gf.css', encoding='utf-8').read()
CA  = '/root/.ccr/ca-bundle.crt'
UA  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'

# --- keep only latin / latin-ext blocks, then inline every woff2 as a data: URI ---
blocks = re.findall(r'/\*\s*([a-z\-]+)\s*\*/\s*(@font-face\s*\{.*?\})', CSS, re.S)
keep = [b for name, b in blocks if name in ('latin', 'latin-ext')]
print(f'{len(blocks)} font-face blocks, keeping {len(keep)} (latin/latin-ext)')

cache = {}
def inline(m):
    url = m.group(1)
    if url not in cache:
        out = 'fonts/' + re.sub(r'\W+', '_', url.split('/')[-1])
        if not os.path.exists(out):
            subprocess.run(['curl','-s','--cacert',CA,'-A',UA,url,'-o',out], check=True)
        cache[url] = base64.b64encode(open(out,'rb').read()).decode()
    return f"url(data:font/woff2;base64,{cache[url]})"

font_css = "\n".join(re.sub(r'url\((https://[^)]+\.woff2)\)', inline, b) for b in keep)
print(f'inlined {len(cache)} woff2 files, {len(font_css)//1024} KB of CSS')

PAGES = [('Inicio.dc.html','Início',2420), ('Produtos.dc.html','Produtos',1620), ('Licitacoes.dc.html','Licitações',1720)]

for fn, title, h in PAGES:
    src = open(f'project/{fn}', encoding='utf-8').read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', src, re.S).group(1)
    style  = re.search(r'<style>(.*?)</style>', helmet, re.S).group(1)
    body   = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1).strip()
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>ACOLHE — {title}</title><style>{font_css}\n{style}\n'
            f'*{{-webkit-font-smoothing:antialiased}}</style></head><body>{body}</body></html>')
    open(f'flat_{fn.replace(".dc.html",".html")}','w',encoding='utf-8').write(html)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_page(viewport={'width':1280,'height':1000})
    for fn, title, h in PAGES:
        f = pathlib.Path(f'flat_{fn.replace(".dc.html",".html")}').resolve()
        pg.goto(f.as_uri())
        pg.wait_for_timeout(700)
        real = pg.evaluate("document.body.firstElementChild.getBoundingClientRect().height")
        out = f'pdf_{fn.replace(".dc.html",".pdf")}'
        pg.pdf(path=out, width='1280px', height=f'{max(h, round(real))}px',
               page_ranges='1', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
        print(f'  {title:12s} declared {h}px  rendered {round(real)}px  -> {out}')
    br.close()

subprocess.run(['pdfunite','pdf_Inicio.pdf','pdf_Produtos.pdf','pdf_Licitacoes.pdf',
                'ACOLHE_Site.pdf'], check=True)
print('merged ->', os.path.getsize('ACOLHE_Site.pdf'), 'bytes')
