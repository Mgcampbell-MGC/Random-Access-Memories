"""A ESCOLA test renders (low-res, ≤32 samples) into 02_PRODUTO/renders/_sets_tests/.

    /home/user/venvs/blender/bin/python test_escola.py [c02 apresentadora geral]

c02             C02 · A PRIMEIRA FILA (4:5): upstage behind the lit candle, back panel to camera, the front row
                of eight monoblocs >= 2 m away, the handbag saving a seat
apresentadora   the ad previs medium shot (9:16, 50 mm, eye level, at the stage edge), spot from front-left
geral           a wide look at the room (for the set designer, not a deliverable framing)
"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import sets_lib as S

OUT = os.path.join(S.KIT, '02_PRODUTO', 'renders', '_sets_tests')


def shot(mode):
    S.cena(res=(432, 540), samples=32)
    preset = 'APRESENTADORA' if mode == 'apresentadora' else 'C02'
    h = S.escola(preset=preset)
    if mode in ('c02', 'geral'):
        root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True), at=h['place'], rot_deg=h['candle_rot'])
        S.flame_bounce(h, root, receivers=[o for o in h['coll'].objects if o.name.startswith('palco_tabuado')])
    sc = bpy.context.scene
    if mode == 'c02':
        S.escola_camera(h, 'C02', res=(432, 540))
    elif mode == 'apresentadora':
        S.figura_sentada(h)
        S.escola_camera(h, 'APRESENTADORA', res=(304, 540))
    else:
        S.camera_look((5.4, -11.5, 2.6), (-0.5, 1.0, 0.9), lens=24)
        sc.render.resolution_x, sc.render.resolution_y = (540, 360)
    S.clearance()
    p = os.path.join(OUT, 'ESCOLA_%s.png' % mode)
    t = time.time()
    S.render(p)
    print('SHOT', mode, round(time.time() - t, 1), 's', 'spot %.1f W' % h['spot'].data.energy)


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    for m in (argv or ['c02', 'apresentadora', 'geral']):
        shot(m)
