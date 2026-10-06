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


def cam_params(ob):
    cd = ob.data
    return dict(location=tuple(ob.location), rotation_euler=tuple(ob.rotation_euler), lens=cd.lens,
                shift_x=cd.shift_x, shift_y=cd.shift_y)


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


def build_palco(candle=True):
    """O PALCO + the UNLIT candle on the lift, for cam A and the crane (no flame in these frames)."""
    h = S.palco(at=(0, 0, 0))
    root = None
    if candle:
        root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=False), at=h['place'], rot_deg=-12)
        S.ride(root, h['lift'])
    return h, root


def build_kv45(lit, flame_scale=1.0, flame_seed=0.0, blackout=False, light_gain=1.0):
    """The KV-45 scene built by the director's OWN function (shots/kv45.py build()), so our frames, crops and blackout
    match the plates whatever the director changes there (flame, lights, framing). Two things are injected:
    the flame's flicker state (flame_scale/flame_seed, holofote's film parameters) and, for the blackout, spot and
    rotunda spill off + the label wash (flame_spill). light_gain scales the flame-derived cheat lights with the flame."""
    import kv45
    cap = {}
    copo0, palco0 = H.copo, S.palco

    def copo(spec, *a, **k):
        spec = dict(spec)
        if spec.get('lit'):
            spec.update(flame_scale=flame_scale, flame_seed=flame_seed)
        r = copo0(spec, *a, **k)
        cap['root'] = r
        return r

    def palco(*a, **k):
        if blackout:
            k.update(spot=False, rotunda_spill=0.0)
        h = palco0(*a, **k)
        cap['h'] = h
        return h
    H.copo, S.palco = copo, palco
    try:
        kv45.build(lit)()
    finally:
        H.copo, S.palco = copo0, palco0
    h, root = cap['h'], cap['root']
    if lit and blackout and h.get('flame_spill') is None:
        S.flame_spill(h, root)
    for k in ('flame_bounce', 'flame_spill'):
        if h.get(k) is not None:
            h[k].data.energy *= light_gain
    return h, root, bpy.context.scene.camera


def kv45_cam():
    """Camera B = the KV-45 camera, read from the director's scene (built, read, discarded)."""
    settings(1)
    _, _, cam = build_kv45(False)
    return cam_params(cam)


def render(path):
    S.render(path)


def aov_on(aov_dir):
    H.add_print_aovs()
    H.enable_label_aovs(aov_dir + os.sep)


# ---------------------------------------------------------------------------------------------------- modes
def mode_dry():
    B = kv45_cam()
    settings(8)
    h, root = build_palco(candle=True)
    A = cam_A()
    cam = make_cam()
    import numpy as np
    pts = S._glass_points('200', 32)
    for f in range(G0, G1 + 1):
        u = set_cam(cam, f, A, B)
        z = lift_z(f)
        bpy.context.view_layer.update()
        R = cam.matrix_world.to_3x3()
        sh = (cam.data.shift_x, cam.data.shift_y)
        px, py = S.project(pts + np.array([0, 0, z]), cam.location, R, cam.data.lens, RES, sh)
        mx, my = S.project(np.array([[0, 0, 0]]), cam.location, R, cam.data.lens, RES, sh)
        print('DRY', json.dumps(dict(f=f, u=round(u, 3), lift_mm=round(z * 1000, 1), lens=round(cam.data.lens, 2),
                                     cam=[round(v, 4) for v in cam.location], mark=[round(float(mx[0]), 1), round(float(my[0]), 1)],
                                     glass_top=round(float(py.min()), 1), glass_bot=round(float(py.max()), 1))))
    print('B', json.dumps(B))


def mode_camA(samples):
    settings(samples)
    build_palco(candle=False)
    cam = make_cam()
    A = cam_A()
    for k in ('location', 'rotation_euler'):
        setattr(cam, k, A[k])
    cam.data.lens, cam.data.shift_x, cam.data.shift_y = A['lens'], A['shift_x'], A['shift_y']
    t = time.time()
    render(os.path.join(OUT, 'F15_camA_16bit.png'))
    print('TEMPO camA', round(time.time() - t, 1))


def mode_grua(f0, f1, pct, samples):
    B = kv45_cam()
    sc = settings(samples, pct)
    h, root = build_palco(candle=True)
    parts = S.descendants(root)
    A = cam_A()
    cam = make_cam()
    aov_on(os.path.join(OUT, 'grua_aov'))
    os.makedirs(os.path.join(OUT, 'grua'), exist_ok=True)
    json.dump(dict(A=A, B=B), open(os.path.join(OUT, 'grua', 'cameras.json'), 'w'), default=list)
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
    h, root, cam = build_kv45(True, blackout=True)
    aov_on(os.path.join(OUT, 'blecaute_aov'))
    sc.frame_current = 1
    t = time.time()
    render(os.path.join(OUT, 'F15_blecaute_16bit.png'))
    print('TEMPO blecaute', round(time.time() - t, 1))


def crop_box(root, margin=36, scale_max=1.10):
    """Pixel box (x0, y0, x1, y1) around the flame at the KV-45 camera: the flame object's box at the largest flicker
    scale, projected, plus a margin for the seed's tongues; multiples of 2 px."""
    import numpy as np
    from mathutils import Vector
    bpy.context.view_layer.update()
    fl = [o for o in S.descendants(root) if o.type == 'MESH' and o.name.startswith('flame')][0]
    cam = bpy.context.scene.camera
    pts = []
    for c in fl.bound_box:
        p = fl.matrix_world @ Vector(c)
        base = fl.matrix_world @ Vector((0, 0, -0.5))
        pts.append(base + (p - base) * scale_max)
    R = cam.matrix_world.to_3x3()
    px, py = S.project(np.array([tuple(p) for p in pts]), cam.location, R, cam.data.lens, RES,
                       (cam.data.shift_x, cam.data.shift_y))
    x0, x1 = int(px.min() - margin) // 2 * 2, int(px.max() + margin + 2) // 2 * 2
    y0, y1 = int(py.min() - margin) // 2 * 2, int(py.max() + margin + 2) // 2 * 2
    return (max(0, x0), max(0, y0), min(RES[0], x1), min(RES[1], y1))


def mode_chama(kind, lista, samples):
    """kind 'palco': loop indices (0–23) at KV-45 lit; kind 'blecaute': F15 frame numbers in the blackout scene."""
    od = os.path.join(OUT, 'chama_' + kind)
    os.makedirs(od, exist_ok=True)
    W, Hh = RES
    box = None
    for f in lista:
        s, seed = flicker(f) if kind == 'palco' else flame_state(f)
        sc = settings(samples, threshold=0.005)
        h, root, cam = build_kv45(True, flame_scale=s, flame_seed=seed, blackout=(kind == 'blecaute'), light_gain=s)
        if box is None:
            box = crop_box(root)
        x0, y0, x1, y1 = box
        sc.render.use_border = True
        sc.render.use_crop_to_border = True
        sc.render.border_min_x, sc.render.border_max_x = x0 / W, x1 / W
        sc.render.border_min_y, sc.render.border_max_y = 1 - y1 / Hh, 1 - y0 / Hh
        t = time.time()
        render(os.path.join(od, 'c%04d.png' % f))
        print('TEMPO chama', kind, f, round(s, 4), round(seed, 4), box, round(time.time() - t, 1), flush=True)
        json.dump(dict(box=box, res=RES), open(os.path.join(od, 'box.json'), 'w'))


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
