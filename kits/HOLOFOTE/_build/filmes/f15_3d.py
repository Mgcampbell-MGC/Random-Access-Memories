"""HOLOFOTE · the 3D frames of the films (platform §E.4). Only what genuinely needs 3D is rendered here; holds and the
KV-45 dolly push are built from stills in compor.py.

Run through the render lock (one Blender at a time on the shared 4 cores):
    _build/shots/blender.sh _build/filmes/f15_3d.py -- MODE [args]

MODES
  dry                     camera/lift plan for F15 f160–203 (no render): prints the projected candle per frame
  camA [--samples N]      F15 cam A (KV-01 9:16 framing), the EMPTY hard pool on the X, spot on      -> _render/F15_camA
  grua F0 F1 [--pct P] [--samples N]
                          F15 crane + dolly A -> B (f160–203) with the lift plate dropping (f168–175) and rising with
                          the UNLIT candle (f176–203). Writes label AOVs per frame when the candle is in the scene.
  blecaute [--samples N]  F15 f204–221 plate: KV-45 framing, spot and spill OFF, the flame the only light
                          (+ flame_bounce on the floor, + flame_spill on the label: §D.6/§D.7.3)          -> _render/F15_blecaute
  chama palco|blecaute FRAMES [--samples N]        FRAMES like 0-23 or 210-223,228,229
                          the flame flicker as a BORDER/CROP render of the flame region only, same camera as KV-45.
                          'palco' = KV-45 lit under the spot (24-frame loop, index 0–23); 'blecaute' = F15 f210–221
                          (ignition f210–215, then the loop) in the blackout scene                         -> _render/chama_*

Flicker (§D.6): flame_scale = 1 ± 6 % (sum of 2, 3 and 4 Hz sines, periodic in 24 frames), flame_seed on a closed
path (periodic in 24 frames), so the loop is seamless. Ignition f210–215: scale 0,10 → 1,0 (the wick catches).
"""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'shots'))
import motor as M          # noqa: E402  (sets the paths, imports bpy, sets_lib, holofote)
import bpy                 # noqa: E402
S, H = M.S, M.H

OUT = os.path.join(HERE, '_render')
RES = (1080, 1920)

# ---------------------------------------------------------------------------------------------------- timing
G0, G1 = 160, 203            # crane/dolly A -> B
DROP0, DROP1 = 168, 175      # lift plate drops 100 mm (empty)
RISE0, RISE1 = 175, 203      # rises carrying the candle; locks flush at f203
CANDLE_FROM = 176
LIFT_DZ = -0.100


def smoother(t):
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def lift_z(f):
    if f <= DROP0 - 1:
        return 0.0
    if f <= DROP1:
        return LIFT_DZ * smoother((f - (DROP0 - 1)) / (DROP1 - (DROP0 - 1)))
    if f < RISE1:
        return LIFT_DZ * (1.0 - smoother((f - RISE0) / (RISE1 - RISE0)))
    return 0.0


def crane_u(f):
    return smoother((f - G0) / (G1 - G0))


from ritmo import flicker, flame_state, IGNICAO   # noqa: E402  (shared with compor.py)


# ---------------------------------------------------------------------------------------------------- scenes
def settings(samples, pct=100, threshold=0.02):
    sc = S.cena(res=RES, samples=samples)
    # the director's still engine (motor.still) trims, so plates and our frames match
    sc.cycles.adaptive_threshold = threshold
    sc.cycles.volume_step_rate = 1.0
    sc.cycles.max_bounces = 8
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 4
    sc.cycles.transmission_bounces = 8
    sc.cycles.transparent_max_bounces = 8
    sc.cycles.volume_bounces = 0
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.resolution_percentage = pct
    sc.render.image_settings.color_depth = '16'
    return sc


def cam_A():
    return S.solve_glass(res=RES, lens=50, cam_height=0.220, tilt_deg=-6, glass_px=384, top_y=900)


def cam_B():
    return S.solve_glass(res=RES, lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)


def make_cam(name='cam'):
    cd = bpy.data.cameras.new(name)
    cd.sensor_fit = 'AUTO'
    cd.sensor_width = 36.0
    cd.clip_start = 0.005
    cd.clip_end = 200
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.scene.camera = ob
    return ob


def set_cam(ob, f, A, B):
    """Crane + dolly A -> B: height and distance interpolated in world space, tilt with them; the focal length and the
    lens shift interpolate on the same ease (the A framing is 50 mm, KV-45 is 85 mm). No yaw, no roll: the camera
    never orbits and the pack never turns (§D.11.7)."""
    u = crane_u(f)
    la, lb = A['location'], B['location']
    # distance along the view line logarithmically (a dolly reads linear in scale), height linearly
    da = math.hypot(la[0], la[1])
    db = math.hypot(lb[0], lb[1])
    d = math.exp(math.log(da) + (math.log(db) - math.log(da)) * u)
    z = la[2] + (lb[2] - la[2]) * u
    ob.location = (0.0, -d, z)
    ra, rb = A['rotation_euler'], B['rotation_euler']
    ob.rotation_euler = (ra[0] + (rb[0] - ra[0]) * u, 0.0, 0.0)
    cd = ob.data
    cd.lens = math.exp(math.log(A['lens']) + (math.log(B['lens']) - math.log(A['lens'])) * u)
    cd.shift_x = A['shift_x'] + (B['shift_x'] - A['shift_x']) * u
    cd.shift_y = A['shift_y'] + (B['shift_y'] - A['shift_y']) * u
    return u


def build_palco(candle=True, lit=False, spot=True, flame_scale=1.0, flame_seed=0.0, blackout_spill=False):
    if spot:
        h = S.palco(at=(0, 0, 0))
    else:
        h = S.palco(at=(0, 0, 0), spot=False, rotunda_spill=0.0)
    root = None
    if candle:
        spec = dict(faixa='02', wrap=S.wrap('02'), lit=lit, flame_scale=flame_scale, flame_seed=flame_seed)
        root = H.copo(spec, at=h['place'], rot_deg=-12)
        S.ride(root, h['lift'])
        if lit:
            S.flame_bounce(h, root)
            if blackout_spill:
                S.flame_spill(h, root)
    return h, root


def render(path):
    S.render(path)


def aov_on(aov_dir):
    H.add_print_aovs()
    H.enable_label_aovs(aov_dir + os.sep)


# ---------------------------------------------------------------------------------------------------- modes
def mode_dry():
    settings(8)
    h, root = build_palco(candle=True)
    A, B = cam_A(), cam_B()
    cam = make_cam()
    import numpy as np
    pts = S._glass_points('200', 32)
    rows = []
    for f in range(G0, G1 + 1):
        u = set_cam(cam, f, A, B)
        z = lift_z(f)
        bpy.context.view_layer.update()
        R = cam.matrix_world.to_3x3()
        px, py = S.project(pts + np.array([0, 0, z]), cam.location, R, cam.data.lens, RES,
                           (cam.data.shift_x, cam.data.shift_y))
        mx, my = S.project(np.array([[0, 0, 0]]), cam.location, R, cam.data.lens, RES, (cam.data.shift_x, cam.data.shift_y))
        rows.append(dict(f=f, u=round(u, 3), lift_mm=round(z * 1000, 1), lens=round(cam.data.lens, 2),
                         cam=[round(v, 4) for v in cam.location], mark=[round(float(mx[0]), 1), round(float(my[0]), 1)],
                         glass_top=round(float(py.min()), 1), glass_bot=round(float(py.max()), 1),
                         glass_x=[round(float(px.min()), 1), round(float(px.max()), 1)]))
    for r in rows:
        print('DRY', json.dumps(r))
    print('A', json.dumps({k: (v if not hasattr(v, '__len__') or isinstance(v, str) else list(v)) for k, v in A.items() if k != 'check'}, default=str))
    print('B', json.dumps({k: (v if not hasattr(v, '__len__') or isinstance(v, str) else list(v)) for k, v in B.items() if k != 'check'}, default=str))


def mode_camA(samples):
    settings(samples)
    build_palco(candle=False)
    cam = make_cam()
    set_cam(cam, G0, cam_A(), cam_B())
    t = time.time()
    render(os.path.join(OUT, 'F15_camA_16bit.png'))
    print('TEMPO camA', round(time.time() - t, 1))


def mode_grua(f0, f1, pct, samples):
    sc = settings(samples, pct)
    h, root = build_palco(candle=True)
    parts = S.descendants(root)
    A, B = cam_A(), cam_B()
    cam = make_cam()
    aov_dir = os.path.join(OUT, 'grua_aov')
    aov_on(aov_dir)
    os.makedirs(os.path.join(OUT, 'grua'), exist_ok=True)
    for f in range(f0, f1 + 1):
        sc.frame_current = f
        sc.frame_set(f)
        set_cam(cam, f, A, B)
        S.lift(h, lift_z(f))
        vis = f >= CANDLE_FROM
        for o in parts:
            o.hide_render = not vis
        t = time.time()
        render(os.path.join(OUT, 'grua', 'f%04d_%d.png' % (f, pct)))
        print('TEMPO grua', f, pct, round(time.time() - t, 1), flush=True)


def mode_blecaute(samples):
    sc = settings(samples)
    h, root = build_palco(candle=True, lit=True, spot=False, blackout_spill=True)
    S.camera_glass(res=RES, lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)
    aov_on(os.path.join(OUT, 'blecaute_aov'))
    sc.frame_current = 1
    S.clearance()
    t = time.time()
    render(os.path.join(OUT, 'F15_blecaute_16bit.png'))
    print('TEMPO blecaute', round(time.time() - t, 1))


def crop_box():
    """Pixel box (x0, y0, x1, y1) around the flame at KV-45, generous for scale 1,10 and the seed tongues."""
    return (430, 450, 650, 670)


def frames(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def mode_chama(kind, lista, samples):
    x0, y0, x1, y1 = crop_box()
    W, Hh = RES
    od = os.path.join(OUT, 'chama_' + kind)
    os.makedirs(od, exist_ok=True)
    for f in lista:
        if kind == 'palco':
            s, seed = flicker(f)
            gain = s
        else:
            s, seed = flame_state(f)
            gain = s
        # rebuild per frame: flame_scale/seed are build-time parameters of the director's model
        settings(samples, threshold=0.005)
        sc = bpy.context.scene
        sc.render.use_border = True
        sc.render.use_crop_to_border = True
        sc.render.border_min_x, sc.render.border_max_x = x0 / W, x1 / W
        sc.render.border_min_y, sc.render.border_max_y = 1 - y1 / Hh, 1 - y0 / Hh
        h, root = build_palco(candle=True, lit=True, spot=(kind == 'palco'), flame_scale=s, flame_seed=seed,
                              blackout_spill=(kind == 'blecaute'))
        for k in ('flame_bounce', 'flame_spill'):
            if h.get(k) is not None:
                h[k].data.energy *= gain
        S.camera_glass(res=RES, lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)
        t = time.time()
        render(os.path.join(od, 'c%04d.png' % f))
        print('TEMPO chama', kind, f, round(s, 4), round(seed, 4), round(time.time() - t, 1), flush=True)
    json.dump(dict(box=crop_box(), res=RES), open(os.path.join(od, 'box.json'), 'w'))


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]

    def opt(k, d):
        return type(d)(a[a.index(k) + 1]) if k in a else d
    mode = a[0]
    if mode == 'dry':
        mode_dry()
    elif mode == 'camA':
        mode_camA(opt('--samples', 128))
    elif mode == 'grua':
        mode_grua(int(a[1]), int(a[2]), opt('--pct', 100), opt('--samples', 64))
    elif mode == 'blecaute':
        mode_blecaute(opt('--samples', 128))
    elif mode == 'chama':
        mode_chama(a[1], frames(a[2]), opt('--samples', 192))
