"""LOJA test renders (low-res, ≤32 samples) into 02_PRODUTO/renders/_sets_tests/.

    /home/user/venvs/blender/bin/python test_loja.py [l01 l05]

l01   L01 · FRENTE: AO VIVO unlit, 3/4 front (yaw 20 deg), the lid leaning on its right side, 85 mm at label height
l05   L05 · A TAMPA-PALCO: AO VIVO LIT standing on its upturned lid, 3/4 front, 25 deg down
Each writes the transparent render (…_alpha.png) and the code-composited plate version (#FFF8EC).
"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import sets_lib as S

OUT = os.path.join(S.KIT, '02_PRODUTO', 'renders', '_sets_tests')


def shot(mode):
    S.cena(res=(540, 540), samples=32, transparent=True)
    h = S.loja()
    if mode == 'l01':
        S.H.copo(dict(faixa='02', wrap=S.wrap('02')), at=h['place'], rot_deg=-20)
        S.tampa_encostada(h)
        S.loja_camera(h, 'L01', res=(540, 540), fill=0.62)
    else:
        root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True, lid='stage', lid_rot_deg=12, lid_art=S.tampa_art()), at=h['place'],
                        rot_deg=-20)
        S.flame_bounce(h, root, receivers=h['seamless_parts'], energy=0.04)
        S.loja_camera(h, 'L05', res=(540, 540))
    S.clearance()
    a = os.path.join(OUT, 'LOJA_%s_alpha.png' % mode)
    t = time.time()
    S.render(a)
    S.loja_plate(a, os.path.join(OUT, 'LOJA_%s.png' % mode))
    print('SHOT', mode, round(time.time() - t, 1), 's', 'key %.1f W' % h['key'].data.energy)


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    for m in (argv or ['l01', 'l05']):
        shot(m)
