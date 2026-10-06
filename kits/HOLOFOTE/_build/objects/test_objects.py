"""Low-res look-dev renders for the objects library (<= 540 px, <= 32 samples, Khronos PBR Neutral, exposure -3).

    /home/user/venvs/blender/bin/python test_objects.py -- <scene> [samples] [res]

Scenes: case_open, case_closed, case_hasp, band_detail, case_c05, props, paper, hands, phone,
previs_H01_sit, previs_H01_stand, previs_H02_sit, previs_H02_stand.
Output: 02_PRODUTO/renders/_objects_tests/T_<scene>.png (one Blender process at a time; these are look-dev, not finals)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import objects_lib as O
from candle_lib import MM, srgb, material, reset, world, area_light, spot, camera, render, glare

OUT = os.path.join(O.KIT, '02_PRODUTO', 'renders', '_objects_tests')
WRAP = os.path.join(O.KIT, '02_PRODUTO', 'rotulos', 'HLF-02_ROTULO_wrap.png')
TAMPA = os.path.join(O.KIT, '02_PRODUTO', 'tampa', 'HLF-TAMPA-90_topo.png')
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['case_open']
scene = args[0]
samples = int(args[1]) if len(args) > 1 else 24
res = int(args[2]) if len(args) > 2 else 540


def stage_floor(hexcol='#0A0A0B', rough=0.45, size=6):
    bpy.ops.mesh.primitive_plane_add(size=size)
    f = bpy.context.object
    f.name = 'floor'
    f.data.materials.append(material('floor', **{'Base Color': srgb(hexcol), 'Roughness': rough}))
    return f


def setup(w, h, samples=samples, exposure=-3.0):
    sc = reset(res=(w, h), samples=samples, view='Khronos PBR Neutral', exposure=exposure)
    sc.cycles.volume_step_rate = 1.0
    return sc


def look_rig(target=(0, 0, 0.06), key=40, rim=30, fill=6, d=1.0):
    # key high front-left (its floor reflection falls behind the object), rim behind-right, low fill right
    area_light((-0.45 * d, -0.35 * d, 1.0 * d), target, 0.45, key)
    area_light((0.55 * d, 0.75 * d, 0.45 * d), target, 0.3, rim)
    area_light((0.9 * d, -0.5 * d, 0.25 * d), target, 0.8, fill)


def lookdev(floor='#3B3B3E', world_s=5.0):
    """Neutral grey look-dev: mid-dark floor, soft grey world, one soft key (exposure -3 calibrated)."""
    world('#9A9A9E', world_s)
    stage_floor(floor, 0.65)


def sph(el, az, d, target):
    el, az = math.radians(el), math.radians(az)
    return (target[0] + d * math.cos(el) * math.sin(az), target[1] - d * math.cos(el) * math.cos(az), target[2] + d * math.sin(el))


if scene == 'case_open':
    setup(res, res)
    lookdev()
    O.case(state='open', open_deg=100, copo=dict(faixa='02', wrap=WRAP, lid_art=TAMPA), band=True)
    area_light((-0.5, -0.45, 0.9), (0, 0, 0.08), 0.5, 45)
    t = (-0.005, -0.01, 0.085)
    camera(sph(24, -30, 0.62, t), t, 60)
elif scene == 'case_closed':
    setup(res, res)
    lookdev()
    O.case(state='closed', copo=None, band=True)
    area_light((-0.5, -0.45, 0.9), (0, 0, 0.07), 0.5, 45)
    t = (-0.01, -0.02, 0.06)
    camera(sph(18, -34, 0.55, t), t, 60)
elif scene == 'case_hasp':
    setup(res, int(res * 0.75))
    lookdev()
    O.case(state='closed', copo=None, band=True)
    area_light((-0.5, -0.45, 0.9), (0, 0, 0.07), 0.5, 45)
    t = (-0.04, -0.09, 0.03)
    camera(sph(35, -40, 0.30, t), t, 60)
elif scene == 'band_detail':
    setup(res, int(res * 0.75))
    lookdev(floor='#77777B')
    c = O.case(state='closed', copo=None, band=True)
    area_light((-0.4, -0.5, 0.8), (-0.03, -0.1, 0.0), 0.4, 45)
    t = (-0.030, -0.080, 0.008)
    camera(sph(40, -8, 0.24, t), t, 60)
elif scene == 'props':
    setup(res, int(res * 0.75))
    lookdev(floor='#6C6C70')
    O.ingresso(faixa='02', at=(-0.115, 0.06, 0), rot_deg=18)
    O.refil(faixa='02', peel=0.0, at=(0.035, 0.085, 0), rot_deg=0)
    O.refil(faixa='02', peel=0.5, at=(0.125, 0.03, 0), rot_deg=-15)
    O.setlist(state='fan', at=(0.0, -0.075, 0), rot_deg=-8)
    O.pulseira(preset='loose', at=(-0.19, -0.13, 0), rot_deg=10)
    area_light((-0.45, -0.5, 0.8), (0, 0, 0.03), 0.6, 55)
    area_light((0.6, 0.6, 0.4), (0, 0, 0.03), 0.4, 20)
    t = (-0.02, -0.01, 0.03)
    camera(sph(38, -12, 0.75, t), t, 50)
elif scene == 'hands':
    setup(res, int(res * 0.6))
    world('#9A9A9E', 5.0)
    stage_floor('#5A5A5E', 0.8, 12)
    O.previs_stage(width=3.2, at=(0, 0, 0.55))
    O.previs('H01', 'd', 'A', at=(-0.42, 0, 0.55))
    O.previs('H01', 'd', 'B', at=(0.42, 0, 0.55))
    t = (0.0, -0.08, 1.18)
    camera(sph(10, -35, 2.0, t), t, 50)
    area_light((-2.0, -2.5, 3.0), t, 1.5, 900)
    area_light((2.5, 1.5, 2.0), t, 1.0, 300)
elif scene == 'phone':
    setup(int(res * 0.6), res)
    world('#9A9A9E', 5.0)
    stage_floor('#5A5A5E', 0.8, 12)
    O.previs('H01', 'c', 'A')
    t = (-0.18, -0.02, 1.85)
    camera(sph(5, -25, 1.0, t), t, 50)
    area_light((-2.0, -2.5, 3.0), t, 1.5, 900)
    area_light((2.5, 1.5, 2.0), t, 1.0, 300)
elif scene.startswith('previs_'):
    _, body, kind = scene.split('_')
    setup(res, int(res * 0.6))
    world('#9A9A9E', 5.0)
    stage_floor('#5A5A5E', 0.8, 12)
    if kind == 'sit':
        O.previs_stage(width=3.2, at=(0, 0, 0.55))
        for x, (pose, key) in zip((-0.85, 0.0, 0.85), (('a', 'A'), ('d', 'A'), ('d', 'B'))):
            O.previs(body, pose, key, at=(x, 0, 0.55))
        t = (0, 0.0, 0.85)
        camera((0, -4.2, 0.95), t, 50)
    else:
        for x, (pose, key) in zip((-0.85, 0.0, 0.85), (('b', 'A'), ('b', 'B'), ('c', 'A'))):
            O.previs(body, pose, key, at=(x, 0, 0))
        t = (0, 0.0, 1.08)
        camera((0, -5.4, 1.15), t, 50)
    area_light((-2.0, -2.5, 3.0), t, 1.5, 900)
    area_light((2.5, 1.5, 2.0), t, 1.0, 300)
elif scene == 'paper':
    setup(res, int(res * 0.75))
    lookdev(floor='#2B2B2E')
    O.setlist(state='folded', at=(-0.21, 0.04, 0), rot_deg=20)
    O.setlist(state='fan', at=(-0.03, -0.02, 0), rot_deg=-6)
    O.setlist_taped(at=(0.17, -0.02, 0), rot_deg=4)
    O.refil(faixa='02', peel=0.5, at=(-0.21, -0.17, 0), rot_deg=-25)
    area_light((-0.45, -0.5, 0.8), (0, 0, 0.03), 0.6, 55)
    area_light((0.6, 0.6, 0.4), (0, 0, 0.03), 0.4, 20)
    t = (-0.01, -0.03, 0.0)
    camera(sph(58, -6, 0.95, t), t, 50)
elif scene == 'case_c05':
    # C05 / L04 geometry: top-down at 70 deg; the lid opens to the mirror-safe angle; the bulb is placed in the mirror
    setup(res, res)
    world('#000000', 0.0)
    stage_floor()
    ang = O.open_deg_for_camera(70)
    c = O.case(state='open', open_deg=ang, copo=dict(faixa='02', wrap=WRAP, lid_art=TAMPA), band=True)
    t = (0, 0.0, 0.05)
    cam = camera(sph(70, 0, 0.78, t), t, 60)
    bpy.context.view_layer.update()
    O.place_work_bulb(c, cam, dist=1.3)
    spot(sph(62, -25, 1.6, (0, 0, 0.06)), (0, 0, 0.06), 260, 30, 0.08, 0.02, (1.0, 0.86, 0.70))
    area_light((0.6, 0.7, 0.5), (0, 0, 0.08), 0.3, 25)
else:
    raise SystemExit('unknown scene ' + scene)

os.makedirs(OUT, exist_ok=True)
render(os.path.join(OUT, 'T_%s.png' % scene))
