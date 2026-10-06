import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor as M
S = M.S
import bpy
mode = sys.argv[sys.argv.index('--') + 1]
sc = S.cena(res=(1080, 1920), samples=32)
sc.render.resolution_percentage = 50
sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 4
sc.cycles.transmission_bounces = 8; sc.cycles.transparent_max_bounces = 8
h = S.palco(at=(0, 0, 0))
root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=False), at=h['place'], rot_deg=-12)
S.ride(root, h['lift'])
S.camera_glass(res=(1080, 1920), lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)
if mode == 'nocopo':
    for o in S.descendants(root): o.hide_render = True
if mode == 'nofloor':
    h['floor'].hide_render = True
if mode == 'norotunda':
    for o in bpy.data.objects:
        if 'rotunda' in o.name.lower(): o.hide_render = True
if mode == 'noglass':
    for o in bpy.data.objects:
        if o.name.startswith('glass'): o.hide_render = True
if mode == 'simplefloor':
    h['floor'].data.materials.clear(); h['floor'].data.materials.append(S.material('f', **{'Base Color': (0.01,0.01,0.01,1), 'Roughness': 0.25}))
t = time.time(); S.render('/home/user/maes_build/test/prof_%s.png' % mode); print('PROF', mode, round(time.time() - t, 1))
print([o.name for o in bpy.data.objects if o.type=='LIGHT'])
