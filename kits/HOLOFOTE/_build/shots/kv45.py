"""KV-45 plates (platform §E.1): 1080 x 1920, 85 mm, camera 160 mm high, tilt -5 deg, glass 883 px with its top at
y 610, candle yaw 12 deg camera-left, O PALCO lit. Lit and unlit plates, each clean (no type).
    /home/user/venvs/blender/bin/python kv45.py [aceso apagado] [--samples 256]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor as M
S = M.S


def build(lit):
    def f():
        h = S.palco(at=(0, 0, 0))
        root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=lit), at=h['place'], rot_deg=-12)
        S.ride(root, h['lift'])
        if lit:
            S.flame_bounce(h, root)
        S.camera_glass(res=(1080, 1920), lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)
        S.clearance()
    return f


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    n = int(a[a.index('--samples') + 1]) if '--samples' in a else 256
    pct = int(a[a.index('--pct') + 1]) if '--pct' in a else 100
    modes = [x for x in a if x in ('aceso', 'apagado')] or ['aceso', 'apagado']
    for m in modes:
        M.still('KV-45_%s' % m, build(m == 'aceso'), res=(1080, 1920), samples=n, wrap=S.wrap('02'), coat='#FFE81A', pct=pct)
