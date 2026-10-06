"""O MURO test renders (low-res, ≤32 samples) into 02_PRODUTO/renders/_sets_tests/.

    /home/user/venvs/blender/bin/python test_muro.py [c01 c10]

c01   C01 · O MURO (4:5): the brand team's 12 lambe posters in a 4 x 3 grid (placeholders if PRONTO.txt is missing),
      the glue drip, the four candles UNLIT with lids on, 01-02-03-04, on the concrete ledge at 1/3 height, flash.
c10   C10 · SALVA COMO (4:5): bare plaster; MÃE ♥ (amarelo), DONA CIDA (rosa), MAINHA (laranja) on the
      ledge, unlit, closer, flash.
"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import sets_lib as S

OUT = os.path.join(S.KIT, '02_PRODUTO', 'renders', '_sets_tests')


def shot(mode):
    S.cena(res=(432, 540), samples=32)
    if mode == 'c01':
        h = S.muro(n=4, spacing=0.125)
        for i, f in enumerate(['01', '02', '03', '04']):
            S.H.copo(dict(faixa=f, wrap=S.wrap(f), lid='on'), at=h['slots'][i], rot_deg=0)
    else:
        h = S.muro(n=3, spacing=0.11, posters=False)
        for i, (f, p) in enumerate([('02', 'CASE-02_MAE-CORACAO'), ('01', 'CASE-01_DONA-CIDA'), ('03', 'CASE-03_MAINHA')]):
            S.H.copo(dict(faixa=f, wrap=S.wrap(personal=p)), at=h['slots'][i], rot_deg=0)
    S.muro_camera(h, mode.upper(), res=(432, 540))
    S.clearance()
    p = os.path.join(OUT, 'MURO_%s.png' % mode)
    t = time.time()
    S.render(p)
    print('SHOT', mode, round(time.time() - t, 1), 's', 'flash %.2f W' % h['flash'].data.energy,
          'placeholders' if h['placeholders'] else 'brand posters')


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    for m in (argv or ['c01', 'c10']):
        shot(m)
