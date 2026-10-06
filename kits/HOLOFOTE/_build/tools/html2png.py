"""Render an HTML file (or several) to PNG at an exact pixel size with Chromium.
python html2png.py page.html out.png 1080x1350 [--scale 1] [--transparent]"""
import sys, os
from playwright.sync_api import sync_playwright
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
def render(pairs, transparent=False, scale=1):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--font-render-hinting=none', '--disable-lcd-text'])
        for html, out, size in pairs:
            w, h = map(int, size.split('x'))
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
            pg.goto('file://' + os.path.abspath(html))
            pg.wait_for_load_state('networkidle')
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(300)
            pg.screenshot(path=out, omit_background=transparent, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            pg.close()
            print('rendered', out)
        b.close()
if __name__ == '__main__':
    a = sys.argv[1:]
    tr = '--transparent' in a
    sc = 1
    if '--scale' in a:
        sc = float(a[a.index('--scale') + 1])
    pos = [x for x in a if not x.startswith('--') and not x.replace('.', '').isdigit()]
    render([(pos[0], pos[1], pos[2])], tr, sc)
