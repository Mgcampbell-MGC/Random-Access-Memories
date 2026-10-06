"""Flame look test: the KV-45 shot (kv45.build, aceso), rendered only in a border around the flame, at 200 %.
    _build/shots/blender.sh _build/shots/teste_chama_regiao.py -- NOME [SAMPLES]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import kv45, motor as M, sets_lib as S
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
nome, spp = argv[0], int(argv[1]) if len(argv) > 1 else 64
sc = S.cena(res=(1080, 1920), samples=spp)
kv45.build(True)()
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 200
sc.render.use_border, sc.render.use_crop_to_border = True, True
x0, x1, y0, y1 = 400, 680, 600, 900          # px, top-left origin at 1x
sc.render.border_min_x, sc.render.border_max_x = x0 / 1080, x1 / 1080
sc.render.border_min_y, sc.render.border_max_y = 1 - y1 / 1920, 1 - y0 / 1920
sc.cycles.max_bounces, sc.cycles.diffuse_bounces, sc.cycles.glossy_bounces = 8, 3, 4
out = os.path.join(HERE, '..', '..', '02_PRODUTO', 'renders', '_sets_tests', 'CHAMA_REG_%s.png' % nome)
S.render(out)
print('REG', nome)
