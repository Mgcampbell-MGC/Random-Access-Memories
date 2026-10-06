"""O PALCO test renders (low-res, ≤32 samples) into 02_PRODUTO/renders/_sets_tests/.

    /home/user/venvs/blender/bin/python test_palco.py [vazio kv01 kv45 elevador subida blecaute haze]

vazio     F15 f12 · cam A (KV-01 framing): the empty hard pool with the X
kv01      KV-01 framing, AO VIVO lit, yaw 12 deg camera-left
kv45      KV-45 framing (85 mm, 160 mm, -5 deg, glass 883 px, top y 610), lit
elevador  F15 f170 · the lift plate dropped 100 mm (cam A)
subida    F15 f190 · the plate rising 40 mm below flush, carrying the candle UNLIT (cam B)
blecaute  F15 f216 / C06 · spot off, the flame the only light (+ bounce, + optional label spill)
haze      KV-01 lit with the optional world-volume cone (density 0,0015)
"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import sets_lib as S

OUT = os.path.join(S.KIT, '02_PRODUTO', 'renders', '_sets_tests')
RES = (304, 540)


def kv01():
    return S.camera_glass(res=(1080, 1920), lens=50, cam_height=0.220, tilt_deg=-6, glass_px=384, top_y=900)


def kv45():
    return S.camera_glass(res=(1080, 1920), lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)


def shot(mode):
    S.cena(res=RES, samples=32)
    spot = mode not in ('blecaute',)
    h = S.palco(at=(0, 0, 0), spot=spot, lift_dz={'elevador': -0.100, 'subida': -0.040}.get(mode, 0.0),
                haze=0.0015 if mode == 'haze' else 0.0)
    root = None
    if mode not in ('vazio', 'elevador'):
        lit = mode != 'subida'
        root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=lit), at=h['place'], rot_deg=-12)
        S.ride(root, h['lift'])
        if lit:
            S.flame_bounce(h, root)
        if mode == 'blecaute':
            S.flame_spill(h, root)
    cam = kv45() if mode in ('kv45', 'subida', 'blecaute') else kv01()
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = RES
    S.clearance()
    p = os.path.join(OUT, 'PALCO_%s.png' % mode)
    t = time.time()
    S.render(p)
    print('SHOT', mode, round(time.time() - t, 1), 's', 'throw %.3f m' % h.get('throw', 0),
          'spot %.1f W' % (h['spot'].data.energy if 'spot' in h else 0))


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    for m in (argv or ['vazio', 'kv01', 'kv45', 'elevador', 'subida', 'blecaute']):
        shot(m)
