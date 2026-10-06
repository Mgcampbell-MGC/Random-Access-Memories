"""Render one packshot from a JSON scene file.

    /home/user/venvs/blender/bin/python render_scene.py -- scene.json

scene.json keys (all optional except out):
  out: output PNG path
  res: [w, h]            samples: int        exposure: float (Standard view; ~ -4.3 for the default rig)
  transparent: bool      chroma: bool (whole product in flat chroma blue: the stand-in for generators)
  world: {color, strength}
  sweep: {color, roughness} | null
  plinths: [{kind, size_mm, color, loc}]
  candles: [{spec: {...candle spec...}, at: [x,y,z], rot_deg}]
  boxes: [{w_mm, d_mm, h_mm, atlas, color, loc, rot_deg, gloss}]
  lids_loose: [{R_mm, at:[x,y,z], rot:[rx,ry,rz] deg, h_mm, color, kind, top_print}]
  lights: [{type: area|spot, loc, target, size, energy, color, size_y}]
  camera: {loc, target, lens, shift_x, shift_y, dof_dist, fstop}
  glare: bool
"""
import sys, json, math
sys.path.insert(0, '/home/user/Random-Access-Memories/kits/HOLOFOTE/_build/blender')
import bpy
from candle_lib import *

cfg = json.load(open(sys.argv[sys.argv.index('--') + 1]))
reset(res=tuple(cfg.get('res', [1080, 1350])), samples=cfg.get('samples', 128), view=cfg.get('view', 'Standard'),
      exposure=cfg.get('exposure', -4.3), transparent=cfg.get('transparent', False))
w = cfg.get('world', {})
world(w.get('color', '#FFFFFF'), w.get('strength', 0.3))
if cfg.get('sweep') is not None and not cfg.get('transparent'):
    s = cfg.get('sweep', {})
    sweep(s.get('color', '#F4EFEA'), s.get('roughness', 0.7))
elif cfg.get('transparent'):
    # shadow catcher floor so the cutout keeps its contact shadow
    bpy.ops.mesh.primitive_plane_add(size=3)
    f = bpy.context.object
    f.is_shadow_catcher = True
for p in cfg.get('plinths', []):
    plinth(p.get('kind', 'cyl'), p.get('size_mm', [160, 160, 60]), p.get('color', '#FFFFFF'), p.get('loc', [0, 0, 0]),
           p.get('roughness', 0.5))
chroma = cfg.get('chroma', False)
for c in cfg.get('candles', []):
    candle(c['spec'], tuple(c.get('at', [0, 0, 0])), c.get('rot_deg', 0.0), chroma=chroma)
for b in cfg.get('boxes', []):
    box(b['w_mm'], b['d_mm'], b['h_mm'], b.get('atlas'), b.get('color', '#FFFFFF'), tuple(b.get('loc', [0, 0, 0])),
        b.get('rot_deg', 0.0), chroma=chroma, gloss=b.get('gloss', False))
for L in cfg.get('lids_loose', []):
    o = lid(L['R_mm'] * MM, 0.0, L.get('h_mm', 14), L.get('color', '#E8E2DA'), L.get('kind', 'matte'), chroma=chroma,
            image_path=L.get('top_print'))
    o.location = tuple(L.get('at', [0.12, 0.02, 0]))
    r = L.get('rot', [0, 0, 0])
    o.rotation_euler = tuple(math.radians(x) for x in r)
for L in cfg.get('lights', []):
    if L.get('type', 'area') == 'spot':
        spot(tuple(L['loc']), tuple(L.get('target', [0, 0, 0.05])), L.get('energy', 200), L.get('size_deg', 40),
             L.get('blend', 0.15), L.get('radius', 0.002), tuple(L.get('color', [1, 1, 1])))
    else:
        area_light(tuple(L['loc']), tuple(L.get('target', [0, 0, 0.05])), L.get('size', 0.4), L.get('energy', 80),
                   tuple(L.get('color', [1, 1, 1])), L.get('shape', 'RECTANGLE'), L.get('size_y'))
cam = cfg.get('camera', {})
camera(tuple(cam.get('loc', [0, -0.44, 0.12])), tuple(cam.get('target', [0, 0, 0.05])), cam.get('lens', 85),
       cam.get('shift_x', 0.0), cam.get('shift_y', 0.0), cam.get('dof_dist'), cam.get('fstop', 8.0))
if cfg.get('glare', True) and not chroma:
    glare()
render(cfg['out'])
