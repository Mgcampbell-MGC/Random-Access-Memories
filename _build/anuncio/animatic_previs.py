"""Previs plates for the O ANÚNCIO animatics (platform §F.1–F.2): grey mannequins in A ESCOLA, framed AROUND the ad's
type layout so the client sees where every word will land on the people layer.

    _build/shots/blender.sh animatic_previs.py -- SHOT [SHOT ...] [--samples 32] [--pct 50]

Shots (each writes _tmp_animatic/plates/<SHOT>[_<key>].png at 1080 x 1920 x pct):
  SIT_H01  SIT_H02        0–6 s talk, seated on the stage edge (1A 1B 3A 3B / 1C 3C)
  USHER_H01               0–6 s talk, standing centre stage, hands behind the back (2A 2B)
  CLAP_H01  CLAP_H02      6–9 s Ad 1: slid off the stage, standing on the floor; keys A (apart) / M / B (together)
  PHONE_H01               6–9 s Ad 2: phone up, flash on, back to camera; sway keys L2 L1 C R1 R2 (root roll)
  HEART_H01 HEART_H02     6–9 s Ad 3: seated finger-heart -> point; keys A / M / B; camera yawed 18 deg so the point reads

Framing rule (1080 x 1920 space): the face and the gesture never sit under type (checked on test renders).
  talk:    tag plate y 560–620 at x 120 -> head top below y 640;  captions y 1000–1240 -> chin above y 990.
  gesture: title y 760–860              -> Ad 1: chin above y 750 and the clapping hands below y 865 (a close
           medium shot, the title on the chest between them); Ad 2: phone and head above the title, which crosses
           the chest; Ad 3: the heart and the point above y 750 and the title across the belly (chin to heart is
           ~0,10 m, too little room for a 100 px title between them).
  `--medir` prints the projected head / hand / phone boxes per key without rendering; every value above was
  measured that way, not eyeballed.
All presenters: 50 mm, eye level (tilt 0), f/4, the APRESENTADORA front-left spot re-aimed at the mark.
The presenter never holds the pack; no candle and no flame anywhere in these plates (CONAR art. 33)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(B, 'sets'))
sys.path.insert(0, os.path.join(B, 'objects'))
import bpy
from mathutils import Vector, Matrix
import sets_lib as S
import objects_lib as O

OUT = os.path.join(HERE, '_tmp_animatic', 'plates')
F_PX = 50.0 / 36.0 * 1920.0          # focal length in px at 1920 (sensor fit AUTO, 36 mm on the long side)

# ------------------------------------------------------------------------------------------------ extra pose 'e'
# hands behind the back, like a theatre usher (§F.2 Ad 2 hook). Built on the standing skeleton of pose 'c' with both
# arms re-solved by the library's own two-bone IK; nothing in objects_lib is edited.
_orig_pose = O._pose_skeleton


def _pose_skeleton(Bd, pose, key):
    if pose != 'e':
        return _orig_pose(Bd, pose, key)
    J, F = _orig_pose(Bd, 'c', key)
    Hh = Bd['H']
    L = {k: v * Hh for k, v in O.SEG.items()}
    pel = J['pelvis']
    for s, side in ((1, 'L'), (-1, 'R')):
        sh = J['shoulder_' + side]
        w = Vector((s * 0.040, pel.y + 0.125, pel.z + 0.085))
        el, wr = O._ik2(sh, w, L['ua'], L['fa'], (s * 1.0, 0.55, -0.2))
        J['elbow_' + side], J['wrist_' + side] = el, wr
        J['uarm_' + side] = sh.lerp(el, 0.45)
        J['farm_' + side] = el.lerp(wr, 0.5)
        F['hand_' + side] = (wr, O._frame((-s * 0.55, 0.25, -0.8), (0, 1, 0)), 'rest')
    return J, F


O._pose_skeleton = _pose_skeleton

# ------------------------------------------------------------------------------------------------ shots
# mark: root position (x, y, z). frame: head-centre pixel (1080 space) and pixels per metre at the head's depth.
SEAT_X = -0.60                     # the set's presenter mark (the flower heart on the TNT reads behind-right)
SHOTS = {
    'SIT_H01':   dict(body='H01', pose='a', mark=(SEAT_X, 0.0, 0.45), head_px=(540, 815), ppm=1333, keys={'': None}),
    'SIT_H02':   dict(body='H02', pose='a', mark=(SEAT_X, 0.0, 0.45), head_px=(540, 815), ppm=1333, keys={'': None}),
    'USHER_H01': dict(body='H01', pose='e', mark=(0.0, 0.95, 0.45), head_px=(540, 795), ppm=1150, keys={'': None}),
    'CLAP_H01':  dict(body='H01', pose='b', mark=(SEAT_X, -0.55, 0.0), head_px=(540, 563), ppm=1600,
                      keys={'A': 1, 'M': 7, 'B': 13}),
    'CLAP_H02':  dict(body='H02', pose='b', mark=(SEAT_X, -0.55, 0.0), head_px=(540, 563), ppm=1600,
                      keys={'A': 1, 'M': 7, 'B': 13}),
    'PHONE_H01': dict(body='H01', pose='c', mark=(0.0, 0.95, 0.45), head_px=(540, 600), ppm=900,
                      keys={'L2': -3.2, 'L1': -1.6, 'C': 0.0, 'R1': 1.6, 'R2': 3.2}, sway=True),
    'HEART_H01': dict(body='H01', pose='d', mark=(SEAT_X, 0.0, 0.45), head_px=(560, 360), ppm=1150, yaw=-18.0,
                      keys={'A': 1, 'M': 7, 'B': 13}),
    'HEART_H02': dict(body='H02', pose='d', mark=(SEAT_X, 0.0, 0.45), head_px=(560, 360), ppm=1150, yaw=-18.0,
                      keys={'A': 1, 'M': 7, 'B': 13}),
}


def build(name, samples, pct):
    sp = SHOTS[name]
    res = (1080, 1920)
    sc = S.cena(res=res, samples=samples)
    sc.render.resolution_percentage = pct
    h = S.escola(preset='APRESENTADORA', presenter_x=SEAT_X)
    two = sp['pose'] in ('b', 'd')
    m = O.previs(sp['body'], sp['pose'], key=None if two else 'A', frames=(1, 13), at=sp['mark'])
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    head = m.parts['head'].matrix_world.translation.copy()
    # re-aim the front-of-house spot at this mark (same lantern position, energy scaled to keep the irradiance)
    spot = h['spot']
    tgt = Vector((sp['mark'][0], sp['mark'][1] + (0.14 if sp['pose'] in ('a', 'd') else 0.0),
                  head.z - 0.30))
    old = h['throw']
    S._aim(spot, tgt)
    new = (spot.location - tgt).length
    spot.data.energy *= (new / old) ** 2
    # camera: eye level, 50 mm, d = F / ppm from the head, optionally orbited (yaw) about the head
    d = F_PX / sp['ppm']
    yaw = sp.get('yaw', 0.0)
    off = Matrix.Rotation(math.radians(yaw), 3, 'Z') @ Vector((0.0, -d, 0.0))
    loc = head + off
    px = (sp['head_px'][0], sp['head_px'][1])
    S.camera_pin(tuple(loc), yaw, 0.0, 50.0, res, tuple(head), px, fstop=4.0, focus=d)
    sc.render.resolution_percentage = pct
    return sp, m


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 32
    pct = int(a[a.index('--pct') + 1]) if '--pct' in a else 50
    shots = [x for x in a if x in SHOTS] or list(SHOTS)
    medir = '--medir' in a
    os.makedirs(OUT, exist_ok=True)
    for name in shots:
        sp, m = build(name, samples, pct)
        for k, v in sp['keys'].items():
            if medir:
                # where the head and hands land (1080 x 1920 px) on this key, from the camera itself; no render
                if sp.get('sway'):
                    m.root.rotation_euler = (0.0, math.radians(v), 0.0)
                bpy.context.scene.frame_set(v if (v is not None and not sp.get('sway')) else 1)
                bpy.context.view_layer.update()
                from bpy_extras.object_utils import world_to_camera_view as w2c
                sc, cam = bpy.context.scene, bpy.context.scene.camera
                out = {}
                for part in ('head', 'hand_L', 'hand_R', 'phone'):
                    ob = m.parts.get(part)
                    if ob is None:
                        continue
                    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
                    pp = [w2c(sc, cam, q) for q in pts]
                    xs = [q.x * 1080 for q in pp]
                    ys = [(1 - q.y) * 1920 for q in pp]
                    out[part] = (round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)))
                print('MEDIDA', name, k, out, flush=True)
                continue
            if sp.get('sway'):
                # sway: roll the whole figure about the feet (root on the stage), the phone moves ~6 cm per degree
                m.root.rotation_euler = (0.0, math.radians(v), 0.0)
                bpy.context.scene.frame_set(1)
            elif v is not None:
                bpy.context.scene.frame_set(v)
            p = os.path.join(OUT, name + ('_' + k if k else '') + '.png')
            S.render(p)
            print('PLATE', p, flush=True)


if __name__ == '__main__':
    main()
