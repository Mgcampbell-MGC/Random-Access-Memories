"""Flame look test after the CCO review: KV-45 set, lit, small and fast. Variants of the camera so the wick shows.

    _build/shots/blender.sh _build/shots/teste_chama.py -- NOME CAM_ALT_M TILT_DEG TOP_Y [RES_PCT] [SAMPLES]
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sets'))
import bpy
import sets_lib as S

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
nome, alt, tilt, top_y = argv[0], float(argv[1]), float(argv[2]), int(argv[3])
pct = int(argv[4]) if len(argv) > 4 else 50
spp = int(argv[5]) if len(argv) > 5 else 32
S.cena(res=(1080, 1920), samples=spp)
h = S.palco()
root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True), at=h['place'], rot_deg=-12)
S.ride(root, h['lift'])
S.flame_bounce(h, root)
S.camera_glass(res=(1080, 1920), lens=85, cam_height=alt, tilt_deg=tilt, glass_px=883, top_y=top_y)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = pct
sc.cycles.max_bounces, sc.cycles.diffuse_bounces, sc.cycles.glossy_bounces = 8, 3, 4
sc.cycles.transmission_bounces, sc.cycles.volume_bounces = 8, 0
S.clearance()
out = os.path.join(HERE, '..', '..', '02_PRODUTO', 'renders', '_sets_tests', 'CHAMA_%s.png' % nome)
t = time.time()
S.render(out)
print('CHAMA', nome, round(time.time() - t, 1), 's')
