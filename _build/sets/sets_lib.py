"""HOLOFOTE · reusable sets for Blender 4.5 Cycles (platform §D.6, §D.8, §D.10, §E.1–E.4).

    import sys; sys.path.insert(0, '<kit>/_build/sets')
    import sets_lib as S
    S.cena(res=(1080, 1920), samples=1024)                # PBR Neutral, look None, exposure -3,0
    h = S.palco(at=(0, 0, 0))                             # O PALCO, built around the product placement
    root = S.H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True), at=h['place'], rot_deg=-12)
    S.ride(root, h['lift'])                               # the candle rides the lift plate
    S.flame_bounce(h, root)                               # warm flame bounce on the lacquer
    S.camera_glass(res=(1080, 1920), lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610, at=h['at'])
    S.clearance()                                         # §D.8 check: every lit flame >= 30 cm from paper/fabric/chairs
    S.render('out.png')

Sets: palco() · escola() · muro() · loja().  Helpers: camera_glass() (solver), ride(), lift(), flame_bounce(),
clearance(), balanced(), loja_plate().  Calibrated energies live in ENERGIA (see LEIA_ME.md).
Conventions: metres, Z up, the product's front faces -Y (camera side). Azimuth 0 = toward -Y, negative = camera-left.
"""
import sys, os, math, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'blender')))
sys.path.insert(0, HERE)
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, Euler
from candle_lib import MM, srgb, material, reset
import candle_lib as CL
import holofote as H
import texturas as T

KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
ROTULOS = os.path.join(KIT, '02_PRODUTO', 'rotulos')
TAMPAS = os.path.join(KIT, '02_PRODUTO', 'tampa')
CARTAZES = os.path.join(KIT, '01_MARCA', 'cartazes')

# ----------------------------------------------------------------------------------------------------------------
# Calibrated energies (exposure -3,0, Khronos PBR Neutral). Filled by calibrar.py; see LEIA_ME.md for the measurements.
#   *_k  : irradiance constant, energy = k * distance^2 (so moving a light keeps the coating at its hex)
ENERGIA = dict(
    palco_spot_k=593.0,       # W per m^2 of throw: 3.200 K hard spot (balanced 3.300 K), coating at hex on the lit panel
    palco_spill=12000.0,      # rotunda spill, light-linked to the rotunda: folds upper-left, ~90 % in shadow
    flame_bounce=0.08,        # warm bounce disc on the lacquer + tape (light-linked), cheat, see flame_bounce()
    escola_spot_k=700.0,      # C02 spot, balanced 3.050 K: back panel at hex (dE00 3,6) despite the warm wood bounce
    escola_house=1.0,         # practicals: 4 globes, dimmed (~5 %)
    escola_spill=0.020,       # C02 spill = 2 % of the spot, wide cone toward the front row
    escola_presenter=0.220,   # presenter key relative to the coating-calibrated spot (skin is not a coating)
    muro_flash_k=89.5,        # on-camera flash, energy = k x d^2: coating at hex (dE00 2,8)
    loja_key_k=83.0,          # LOJA key, energy = k x d^2: coating at hex (dE00 3,0), fill = 20 %
)
EXPOSURE = -3.0


def tampa_art(size='200'):
    """The lid's UV print (gaffer X + 'ela fica aqui.'): HLF-TAMPA-90 for the 200 g, HLF-TAMPA-70 for O SINGLE."""
    p = os.path.join(TAMPAS, 'HLF-TAMPA-%s_topo.png' % ('90' if size == '200' else '70'))
    return p if os.path.exists(p) else None


def wrap(faixa='02', personal=None):
    """Path to a label wrap master: wrap('02') -> HLF-02, wrap(personal='CASE-01_DONA-CIDA')."""
    name = 'HLF-%s_ROTULO_wrap.png' % (personal or faixa)
    return os.path.join(ROTULOS, name)


# ----------------------------------------------------------------------------------------------------------------
# render settings
def cena(res=(432, 540), samples=32, exposure=EXPOSURE, transparent=False, denoise=True):
    """Factory-reset scene with the director's colour management: Khronos PBR Neutral, look None, exposure -3,0."""
    sc = reset(res=res, samples=samples, view='Khronos PBR Neutral', look='None', exposure=exposure,
               transparent=transparent)
    sc.cycles.use_denoising = denoise
    sc.view_settings.use_white_balance = False
    w = bpy.data.worlds.new('mundo')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.0
    sc.world = w
    return sc


def render(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    CL.render(path)


def kelvin_rgb(k):
    """Blender's blackbody colour for k kelvin (luminance-normalised, linear Rec.709)."""
    L = bpy.data.lights.new('_k', 'POINT')
    L.use_temperature = True
    L.temperature = k
    c = tuple(L.temperature_color)
    bpy.data.lights.remove(L)
    return c


def balanced(kelvin, balance_k):
    """The colour a blackbody `kelvin` source records as through a camera white-balanced to `balance_k`
    (von Kries in linear Rec.709), normalised to luminance 1. balanced(3200, 3200) = white."""
    a, b = kelvin_rgb(kelvin), kelvin_rgb(balance_k)
    c = [a[i] / b[i] for i in range(3)]
    lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return tuple(x / lum for x in c)


# ----------------------------------------------------------------------------------------------------------------
# small node / mesh helpers
def _coll(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    return c


def _obj(name, me, coll, mat=None, smooth=False):
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if mat is not None:
        me.materials.append(mat)
    if smooth:
        me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    return ob


def _bm_obj(name, bm, coll, mat=None, smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _obj(name, me, coll, mat, smooth)


def _n(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items():
        if k in n.inputs and not hasattr(n, k):
            n.inputs[k].default_value = v
        else:
            setattr(n, k, v)
    return n


def _l(nt, a, b):
    nt.links.new(a, b)


def _math(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath')
    n.operation = op
    n.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            nt.links.new(v, n.inputs[i])
    return n.outputs[0]


def _mix(nt, fac, a, b):
    """RGBA mix; a/b are sockets or colour tuples, fac socket or float."""
    m = nt.nodes.new('ShaderNodeMix')
    m.data_type = 'RGBA'
    for sock, v in (('Factor', fac), ('A', a), ('B', b)):
        if isinstance(v, (int, float, tuple, list)):
            m.inputs[sock].default_value = v
        else:
            nt.links.new(v, m.inputs[sock])
    return m.outputs['Result']


def _img(nt, path, colorspace='Non-Color', ext='REPEAT', interp='Linear'):
    t = nt.nodes.new('ShaderNodeTexImage')
    t.image = bpy.data.images.load(path, check_existing=True)
    t.image.colorspace_settings.name = colorspace
    t.extension = ext
    t.interpolation = interp
    return t


def _maprange(nt, v, a, b, c, d, clamp=True):
    n = nt.nodes.new('ShaderNodeMapRange')
    n.clamp = clamp
    for k, x in zip(('From Min', 'From Max', 'To Min', 'To Max'), (a, b, c, d)):
        n.inputs[k].default_value = x
    nt.links.new(v, n.inputs['Value'])
    return n.outputs['Result']


def _flag(ob, inflamavel=False, apoio=False):
    """Tag for clearance(): inflamavel = paper, fabric, chairs, people (§D.8); apoio = the surface a candle stands on."""
    ob['inflamavel'] = bool(inflamavel)
    ob['apoio'] = bool(apoio)
    return ob


def _aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def _light(name, kind, loc, target, energy, color=(1, 1, 1), coll=None, **kw):
    L = bpy.data.lights.new(name, kind)
    L.energy = energy
    L.color = color
    for k, v in kw.items():
        setattr(L, k, v)
    ob = bpy.data.objects.new(name, L)
    (coll or bpy.context.scene.collection).objects.link(ob)
    ob.location = Vector(loc)
    if target is not None:
        _aim(ob, target)
    return ob


def _dir(az_deg, el_deg):
    """Unit vector from the subject toward a light at azimuth/elevation (az 0 = toward -Y, negative = toward -X)."""
    a, e = math.radians(az_deg), math.radians(el_deg)
    return Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))


def link_receivers(light_ob, objs):
    """Light linking: this light only illuminates objs."""
    c = bpy.data.collections.new(light_ob.name + '_recebe')
    for o in objs:
        c.objects.link(o)
    light_ob.light_linking.receiver_collection = c
    return c


def ride(objs, carrier):
    """Parent objects to a carrier (e.g. the lift plate) keeping their world transform."""
    if not isinstance(objs, (list, tuple)):
        objs = [objs]
    bpy.context.view_layer.update()
    for o in objs:
        mw = o.matrix_world.copy()
        o.parent = carrier
        o.matrix_parent_inverse = carrier.matrix_world.inverted()
        o.matrix_world = mw


def descendants(root):
    out = []
    stack = [root]
    while stack:
        o = stack.pop()
        out.append(o)
        stack.extend(o.children)
    return out


# ----------------------------------------------------------------------------------------------------------------
# §D.8 clearance
def clearance(min_m=0.30, raise_on_fail=False, verbose=True):
    """Distance from every lit flame to every object tagged inflamavel (paper, fabric, chairs, people).
    Returns a list of (flame, object, metres). A NO prints loudly (and raises if asked)."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    flames = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith('flame')
              and not o.hide_render]
    targets = [o for o in bpy.context.scene.objects if o.get('inflamavel') and not o.hide_render]
    rows = []
    for f in flames:
        pts = [f.matrix_world @ Vector(c) for c in f.bound_box]
        pts.append(sum(pts, Vector()) / len(pts))
        for t in targets:
            te = t.evaluated_get(dg)
            inv = t.matrix_world.inverted()
            best = 1e9
            if t.type == 'MESH':
                for p in pts:
                    ok, loc, nrm, idx = te.closest_point_on_mesh(inv @ p)
                    if ok:
                        best = min(best, ((t.matrix_world @ loc) - p).length)
            else:                                   # curves, text: measure the evaluated geometry's vertices
                try:
                    me = te.to_mesh()
                    vs = np.array([t.matrix_world @ v.co for v in me.vertices]) if len(me.vertices) else None
                    te.to_mesh_clear()
                except Exception:
                    vs = None
                if vs is None:
                    vs = np.array([t.matrix_world @ Vector(c) for c in t.bound_box])
                for p in pts:
                    best = min(best, float(np.min(np.linalg.norm(vs - np.array(p), axis=1))))
            rows.append((f.name, t.name, best))
    bad = [r for r in rows if r[2] < min_m]
    if verbose:
        if not flames:
            print('CLEARANCE: no lit flame in the scene')
        elif not targets:
            print('CLEARANCE: no paper/fabric/chair/person tagged in the scene')
        else:
            near = sorted(rows, key=lambda r: r[2])[:6]
            for r in near:
                print('CLEARANCE %-6s %-14s %-28s %.3f m' % ('NO' if r[2] < min_m else 'ok', r[0], r[1], r[2]))
    if bad and raise_on_fail:
        raise RuntimeError('§D.8 clearance failed: %s' % bad[:3])
    return rows


# ----------------------------------------------------------------------------------------------------------------
# camera solver
def _glass_points(size='200', n_az=96):
    """Points on the outer glass surface (from holofote's own profile) for silhouette extents."""
    H.use_size(size)
    prof = H.glass_profile()
    pts = []
    for r, z in prof:
        if r <= 0.01:
            continue
        for i in range(n_az):
            a = 2 * math.pi * i / n_az
            pts.append((r * MM * math.cos(a), r * MM * math.sin(a), z * MM))
    return np.array(pts)


def cam_matrix(tilt_deg, yaw_deg=0.0):
    """Rotation of a camera looking toward +Y (yaw 0), pitched by tilt (negative = down)."""
    return Euler((math.radians(90 + tilt_deg), 0.0, math.radians(yaw_deg)), 'XYZ').to_matrix()


def project(P, C, R, lens, res, shift=(0.0, 0.0), sensor=36.0):
    """Blender pinhole projection (sensor fit AUTO). Returns pixel x (from left), y (from top)."""
    W, Hh = res
    big = max(W, Hh)
    right, up, fwd = R @ Vector((1, 0, 0)), R @ Vector((0, 1, 0)), R @ Vector((0, 0, -1))
    P = np.asarray(P, np.float64).reshape(-1, 3) - np.asarray(C)
    x = P @ np.array(right)
    y = P @ np.array(up)
    z = P @ np.array(fwd)
    ppm = big / sensor
    px = W / 2 + (lens * x / z) * ppm - shift[0] * big
    py = Hh / 2 - ((lens * y / z) * ppm - shift[1] * big)
    return px, py


def solve_glass(res=(1080, 1920), lens=85.0, cam_height=0.160, tilt_deg=-5.0, glass_px=883, top_y=610,
                center_x=None, at=(0, 0, 0), yaw_deg=0.0, size='200', mode='silhouette'):
    """Solve camera distance and lens shift so the glass (0–88 mm) spans glass_px with its top at top_y.
    mode 'silhouette' measures the visible outline (back rim to front base edge); 'axis' the axis points.
    Returns dict(location, rotation_euler, shift_x, shift_y, distance, check)."""
    at = Vector(at)
    R = cam_matrix(tilt_deg, yaw_deg)
    back = R @ Vector((0, 0, 1))                     # camera +Z (away from the view)
    back.z = 0
    back.normalize()
    if mode == 'axis':
        H.use_size(size)
        pts = np.array([(0, 0, 0), (0, 0, H.H_GLASS * MM)])
    else:
        pts = _glass_points(size)
    pts = pts + np.array(at)
    cx = res[0] / 2 if center_x is None else center_x

    def measure(D, sh=(0, 0)):
        C = at + back * D
        C.z = at.z + cam_height
        px, py = project(pts, C, R, lens, res, sh)
        return C, px, py

    lo, hi = 0.05, 20.0
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        _, px, py = measure(mid)
        if (py.max() - py.min()) > glass_px:
            lo = mid
        else:
            hi = mid
    D = math.sqrt(lo * hi)
    C, px, py = measure(D)
    big = max(res)
    # axis x at the subject's mid height, so the candle is centred
    ax_px, _ = project(np.array([[at.x, at.y, at.z + 0.044]]), C, R, lens, res)
    shift_x = (ax_px[0] - cx) / big
    shift_y = (top_y - py.min()) / big               # +shift moves the frame up, the content down
    C, px, py = measure(D, (shift_x, shift_y))
    ax_px, _ = project(np.array([[at.x, at.y, at.z + 0.044]]), C, R, lens, res, (shift_x, shift_y))
    return dict(location=tuple(C), rotation_euler=tuple(Euler((math.radians(90 + tilt_deg), 0, math.radians(yaw_deg)))),
                shift_x=shift_x, shift_y=shift_y, distance=D, lens=lens,
                check=dict(top_y=float(py.min()), base_y=float(py.max()), glass_px=float(py.max() - py.min()),
                           axis_x=float(ax_px[0]), px_per_mm=float((py.max() - py.min()) / H.H_GLASS)))


def camera_glass(res=(1080, 1920), lens=85.0, cam_height=0.160, tilt_deg=-5.0, glass_px=883, top_y=610,
                 center_x=None, at=(0, 0, 0), yaw_deg=0.0, size='200', mode='silhouette', fstop=None, name='cam'):
    """Create (and make active) the camera solved by solve_glass(). Focus on the label (axis at mid height)."""
    s = solve_glass(res, lens, cam_height, tilt_deg, glass_px, top_y, center_x, at, yaw_deg, size, mode)
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_fit = 'AUTO'
    cd.sensor_width = 36.0
    cd.shift_x, cd.shift_y = s['shift_x'], s['shift_y']
    cd.clip_start = 0.005
    cd.clip_end = 200
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = s['location']
    ob.rotation_euler = s['rotation_euler']
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_distance = s['distance']
        cd.dof.aperture_fstop = fstop
    bpy.context.scene.camera = ob
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    s['object'] = ob
    return s


def camera_look(loc, target, lens=50.0, shift=(0, 0), fstop=None, focus=None, name='cam', roll_deg=0.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.shift_x, cd.shift_y = shift
    cd.clip_start = 0.005
    cd.clip_end = 300
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc)
    _aim(ob, target)
    if roll_deg:
        ob.rotation_euler.rotate_axis('Z', math.radians(roll_deg))
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_distance = focus or (Vector(target) - Vector(loc)).length
        cd.dof.aperture_fstop = fstop
    bpy.context.scene.camera = ob
    return ob


def camera_pin(loc, yaw_deg, tilt_deg, lens, res, anchor, anchor_px, fstop=None, focus=None, name='cam'):
    """A level-ish camera at loc (yaw 0 looks toward +Y, 180 toward -Y; tilt negative = down) whose lens shift
    puts the world point `anchor` at pixel anchor_px = (x, y from top). Verticals stay as straight as the tilt allows."""
    R = cam_matrix(tilt_deg, yaw_deg)
    big = max(res)
    px, py = project(np.array([anchor]), Vector(loc), R, lens, res)
    shift = ((px[0] - anchor_px[0]) / big, (anchor_px[1] - py[0]) / big)
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.shift_x, cd.shift_y = shift
    cd.clip_start = 0.005
    cd.clip_end = 300
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc)
    ob.rotation_euler = Euler((math.radians(90 + tilt_deg), 0, math.radians(yaw_deg)))
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_distance = focus or (Vector(anchor) - Vector(loc)).length
        cd.dof.aperture_fstop = fstop
    sc = bpy.context.scene
    sc.camera = ob
    sc.render.resolution_x, sc.render.resolution_y = res
    return ob


# ----------------------------------------------------------------------------------------------------------------
# flame bounce (all sets)
def flame_bounce(h, copo_root, energy=None, receivers=None, kind='disc'):
    """The flame's warm bounce on the floor in front of the base (§E.1).
    Physically the coated (opaque) glass shadows the floor near its base from a flame burning below the rim (the
    shadow line falls ~0,87 m out), so this is a MOTIVATED CHEAT, invisible to the camera: a 1.900 K source that
    casts no shadow and is light-linked to the floor and the tape only.
      kind 'disc'  (default) a Ø110 mm disc 35 mm above the base, facing down: a warm glow hugging the base;
      kind 'point' a point at the flame: reads as the flame's own reflection streaking toward camera."""
    fl = [o for o in descendants(copo_root) if o.name.startswith('flame_light')]
    if not fl:
        return None
    bpy.context.view_layer.update()
    p = fl[0].matrix_world.translation.copy()
    e = ENERGIA['flame_bounce'] if energy is None else energy
    if kind == 'point':
        L = _light('flame_bounce', 'POINT', p, None, e, color=(1.0, 0.56, 0.24), coll=h.get('coll'),
                   shadow_soft_size=0.004, use_shadow=False)
    else:
        base = copo_root.matrix_world.translation
        L = _light('flame_bounce', 'AREA', (p.x, p.y, base.z + 0.035), (p.x, p.y, base.z), e,
                   color=(1.0, 0.56, 0.24), coll=h.get('coll'), shape='DISK', size=0.11, use_shadow=False)
    L.visible_camera = False
    L.parent = fl[0]
    L.matrix_parent_inverse = fl[0].matrix_world.inverted()
    link_receivers(L, receivers if receivers is not None else h.get('floor_objs', []))
    h['flame_bounce'] = L
    return L


def flame_spill(h, copo_root, energy=0.012):
    """OPTIONAL cheat for blackout frames (C06, F15 f204–221): the flame cannot light the outside of an opaque
    coated glass, yet the platform asks for a 'dimly flame-lit' label. A shadowless 1.900 K disc at the flame,
    light-linked to this copo's coating and print only, gives that warm top-down wash. Off by default."""
    fl = [o for o in descendants(copo_root) if o.name.startswith('flame_light')]
    parts = [o for o in descendants(copo_root) if o.type == 'MESH' and (o.name.startswith('coating') or o.name.startswith('print'))]
    if not fl or not parts:
        return None
    bpy.context.view_layer.update()
    p = fl[0].matrix_world.translation.copy()
    L = _light('flame_spill', 'AREA', (p.x, p.y, p.z + 0.004), (p.x, p.y, p.z - 0.1), energy,
               color=(1.0, 0.56, 0.24), coll=h.get('coll'), shape='DISK', size=0.02, use_shadow=False)
    L.visible_camera = False
    L.parent = fl[0]
    L.matrix_parent_inverse = fl[0].matrix_world.inverted()
    link_receivers(L, parts)
    h['flame_spill'] = L
    return L


# ================================================================================================================
# 1. O PALCO
# ================================================================================================================
def _lacquer_material(mark, decal_path, scratch_path, name='laca', base_hex='#0A0A0B', downstage=0.30):
    """Black lacquer stage floor #0A0A0B: roughness 0,15–0,30 on a 400 mm noise, fine anisotropic scratches, two
    road-case scuff arcs, a tape-residue ghost and foot-traffic dust. Object coordinates (floor & plate share them)."""
    # roughness 0,32 (was 0,22): the near-mirror lacquer reflected the yellow coat as an olive smear (CCO review, 6 Oct)
    m = material(name, **{'Base Color': srgb(base_hex), 'Roughness': 0.32, 'Specular IOR Level': 0.5})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    obj = tc.outputs['Object']
    # roughness field
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 2.5, 'Detail': 3.0, 'Roughness': 0.55})
    _l(nt, obj, nz.inputs['Vector'])
    rough = _maprange(nt, nz.outputs['Fac'], 0.3, 0.7, 0.15, 0.30)
    # scratches (tile 0,5 m)
    mps = _n(nt, 'ShaderNodeMapping')
    mps.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    _l(nt, obj, mps.inputs['Vector'])
    si = _img(nt, scratch_path, interp='Cubic')
    _l(nt, mps.outputs[0], si.inputs['Vector'])
    sep_s = _n(nt, 'ShaderNodeSeparateColor')
    _l(nt, si.outputs['Color'], sep_s.inputs['Color'])
    scr_v = sep_s.outputs[0]
    # decal (1,2 m centred on the mark)
    mpd = _n(nt, 'ShaderNodeMapping')
    mpd.inputs['Location'].default_value = (0.5 - mark[0] / 1.2, 0.5 - mark[1] / 1.2, 0)
    mpd.inputs['Scale'].default_value = (1 / 1.2, 1 / 1.2, 1)
    _l(nt, obj, mpd.inputs['Vector'])
    di = _img(nt, decal_path, ext='CLIP', interp='Cubic')
    _l(nt, mpd.outputs[0], di.inputs['Vector'])
    sep = _n(nt, 'ShaderNodeSeparateColor')
    _l(nt, di.outputs['Color'], sep.inputs['Color'])
    scuff, resid, dust = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    # base colour: abrasion is whitish-grey, dust warm grey, residue a dull smear, scratches pale
    col = _mix(nt, _math(nt, 'MULTIPLY', dust, 0.30), srgb(base_hex), srgb('#3B3833'))
    col = _mix(nt, _math(nt, 'MULTIPLY', resid, 0.55), col, srgb('#24221F'))
    col = _mix(nt, _math(nt, 'MULTIPLY', scuff, 0.85), col, srgb('#6E6A64'))
    col = _mix(nt, _math(nt, 'MULTIPLY', scr_v, 0.55), col, srgb('#8F8A84'))
    _l(nt, col, bs.inputs['Base Color'])
    # downstage foot-traffic haze: the lacquer dulls ahead of the mark (toward the audience), mottled
    sxy = _n(nt, 'ShaderNodeSeparateXYZ')
    _l(nt, obj, sxy.inputs[0])
    ahead = _maprange(nt, sxy.outputs['Y'], mark[1] - 0.05, mark[1] - 0.32, 0.0, 1.0)
    mott = _maprange(nt, nz.outputs['Fac'], 0.3, 0.7, 0.55, 1.0)
    rough = _math(nt, 'ADD', rough, _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', ahead, mott), downstage))
    r = _math(nt, 'MAXIMUM', rough, _math(nt, 'MULTIPLY', dust, 0.55))
    r = _math(nt, 'MAXIMUM', r, _math(nt, 'MULTIPLY', resid, 0.55))
    r = _math(nt, 'MAXIMUM', r, _math(nt, 'MULTIPLY', scuff, 0.70))
    r = _math(nt, 'MAXIMUM', r, _math(nt, 'MULTIPLY', scr_v, 0.50))
    _l(nt, r, bs.inputs['Roughness'])
    # normal: scratch grooves + a gentle board undulation that breaks the reflection
    b1 = _n(nt, 'ShaderNodeBump', **{'Strength': 0.9, 'Distance': 0.00006, 'invert': True})
    _l(nt, scr_v, b1.inputs['Height'])
    nz2 = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 6.0, 'Detail': 2.0})
    _l(nt, obj, nz2.inputs['Vector'])
    b2 = _n(nt, 'ShaderNodeBump', **{'Strength': 0.05, 'Distance': 0.002})
    _l(nt, nz2.outputs['Fac'], b2.inputs['Height'])
    _l(nt, b1.outputs['Normal'], b2.inputs['Normal'])
    _l(nt, b2.outputs['Normal'], bs.inputs['Normal'])
    return m


def _tape_material(hexc='#FFE81A', gain=0.70, name='fita'):
    """Cloth gaffer tape: matte, woven bump, dirt toward the edges and along foot traffic. `gain` scales the linear
    albedo: under a 55 deg spot the floor gets ~1,5x the label's irradiance, so a 0,70 cloth reads at the hex in the
    pool instead of blowing out (real cloth tape is less reflective than a printed coat)."""
    base = tuple(c * gain for c in srgb(hexc)[:3]) + (1.0,)
    m = material(name, **{'Base Color': base, 'Roughness': 0.72, 'Specular IOR Level': 0.3})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    obj = tc.outputs['Object']
    wx = _n(nt, 'ShaderNodeTexWave', wave_type='BANDS', bands_direction='X')
    wx.inputs['Scale'].default_value = 1.0 / 0.0007
    wy = _n(nt, 'ShaderNodeTexWave', wave_type='BANDS', bands_direction='Y')
    wy.inputs['Scale'].default_value = 1.0 / 0.0005
    _l(nt, obj, wx.inputs['Vector'])
    _l(nt, obj, wy.inputs['Vector'])
    weave = _math(nt, 'MULTIPLY', wx.outputs['Fac'], wy.outputs['Fac'])
    bump = _n(nt, 'ShaderNodeBump', **{'Strength': 0.25, 'Distance': 0.00004})
    _l(nt, weave, bump.inputs['Height'])
    _l(nt, bump.outputs['Normal'], bs.inputs['Normal'])
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 55.0, 'Detail': 6.0, 'Roughness': 0.6})
    _l(nt, obj, nz.inputs['Vector'])
    uv = _n(nt, 'ShaderNodeUVMap')
    sp = _n(nt, 'ShaderNodeSeparateXYZ')
    _l(nt, uv.outputs['UV'], sp.inputs[0])
    edge = _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', sp.outputs['Y'], 0.5))
    edge = _maprange(nt, edge, 0.36, 0.5, 0.0, 1.0)
    dirt = _math(nt, 'ADD', _maprange(nt, nz.outputs['Fac'], 0.45, 0.75, 0.0, 0.55), _math(nt, 'MULTIPLY', edge, 0.6))
    dirt = _math(nt, 'MINIMUM', dirt, 1.0)
    col = _mix(nt, _math(nt, 'MULTIPLY', dirt, 0.35), base, srgb('#6B5F2A'))
    _l(nt, col, bs.inputs['Base Color'])
    return m


def _plain(name, hexc, rough=0.9, spec=0.3, **kw):
    return material(name, **{'Base Color': srgb(hexc), 'Roughness': rough, 'Specular IOR Level': spec, **kw})


def _square_ring(bm, inner, outer, z=0.0):
    """Faces between two concentric (rotated) squares given as 4 corner lists."""
    vi = [bm.verts.new((x, y, z)) for x, y in inner]
    vo = [bm.verts.new((x, y, z)) for x, y in outer]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vo[i], vo[j], vi[j], vi[i]))


def _rot2(x, y, a):
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def _tape_x(mark, x_rot, plate_half, plate_rot, gap, z0, strip=(0.048, 0.240), res=0.0015, seed=7, lift_corner=1):
    """The floor X: two strips crossed at +-45 deg (+x_rot). Returns bmesh split into (on_plate, on_floor) halves.
    The strips are cut along the lift plate's seams (with the seam gap removed)."""
    rng = np.random.default_rng(seed)
    W, Lh = strip[1], strip[0]           # length along local x, width along local y
    nu, nv = int(round(W / res)), int(round(Lh / res))
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new('UVMap')
    T = 0.00026                           # tape thickness, the second strip rides over the first
    for k, ang in enumerate((math.radians(45) + x_rot, math.radians(-45) + x_rot)):
        grid = []
        endj = [rng.normal(0, 0.0007, nv + 1).cumsum() * 0.35 for _ in range(2)]
        for e in endj:
            e -= e.mean()
        for i in range(nu + 1):
            row = []
            for j in range(nv + 1):
                u = -W / 2 + W * i / nu
                v = -Lh / 2 + Lh * j / nv
                if i == 0:
                    u += endj[0][j] + rng.normal(0, 0.00025)
                if i == nu:
                    u += endj[1][j] + rng.normal(0, 0.00025)
                x, y = _rot2(u, v, ang)
                z = z0
                if k == 1:                    # drape over strip 0 at the crossing
                    a0 = math.radians(45) + x_rot
                    d = abs(-x * math.sin(a0) + y * math.cos(a0))
                    t = min(1.0, max(0.0, (Lh / 2 + 0.0012 - d) / 0.0018))
                    z += T * (t * t * (3 - 2 * t))
                row.append(bm.verts.new((mark[0] + x, mark[1] + y, z)))
            grid.append(row)
        if k == 1 and lift_corner:            # one corner of the over-strip lifts 1 mm (front-right arm end)
            cu, cv = W / 2, -Lh / 2
            for i in range(nu + 1):
                for j in range(nv + 1):
                    u = -W / 2 + W * i / nu
                    v = -Lh / 2 + Lh * j / nv
                    dd = math.hypot(u - cu, v - cv)
                    if dd < 0.024:
                        grid[i][j].co.z += 0.001 * (1 - dd / 0.024) ** 2
        for i in range(nu):
            for j in range(nv):
                f = bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
                for lp, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                    lp[uvl].uv = (a / nu, b / nv)
    # cut along the plate seams (both sides of the gap) and drop the gap band
    ca, sa = math.cos(plate_rot), math.sin(plate_rot)
    ax_u, ax_v = Vector((ca, sa, 0)), Vector((-sa, ca, 0))
    cen = Vector((mark[0], mark[1], 0))
    for axis in (ax_u, ax_v):
        for s in (-1, 1):
            for off in (plate_half - gap / 2, plate_half + gap / 2):
                geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
                bmesh.ops.bisect_plane(bm, geom=geom, plane_co=cen + axis * s * off, plane_no=axis)
    on_plate, on_floor, drop = [], [], []
    for f in bm.faces:
        c = f.calc_center_median() - cen
        pu, pv = abs(c.dot(ax_u)), abs(c.dot(ax_v))
        m = max(pu, pv)
        if m < plate_half - gap / 2:
            on_plate.append(f)
        elif m > plate_half + gap / 2:
            on_floor.append(f)
        else:
            drop.append(f)
    bmesh.ops.delete(bm, geom=drop, context='FACES')
    bm2 = bm.copy()
    # split: in bm keep plate faces, in bm2 keep floor faces
    def keep(b, inside):
        kill = []
        for f in b.faces:
            c = f.calc_center_median() - cen
            m = max(abs(c.dot(ax_u)), abs(c.dot(ax_v)))
            if (m < plate_half) != inside:
                kill.append(f)
        bmesh.ops.delete(b, geom=kill, context='FACES')
        bmesh.ops.delete(b, geom=[v for v in b.verts if not v.link_faces], context='VERTS')
    keep(bm, True)
    keep(bm2, False)
    return bm, bm2


def _rotunda(coll, at, dist=4.0, width=11.0, height=6.5, amp=0.040, seed=3):
    """Black molton rotunda: vertical folds, 40 mm amplitude, hanging `dist` behind the mark."""
    rng = np.random.default_rng(seed)
    nx, nz = int(width / 0.012), 48
    periods = rng.uniform(0.17, 0.42, 7)
    phases = rng.uniform(0, 2 * math.pi, 7)
    weights = rng.uniform(0.4, 1.0, 7)
    weights /= weights.sum()
    sway = rng.uniform(0, 2 * math.pi)
    bm = bmesh.new()
    grid = []
    for j in range(nz + 1):
        z = height * j / nz
        row = []
        depth = 0.85 + 0.25 * (1 - z / height)        # folds open slightly toward the floor
        for i in range(nx + 1):
            x = -width / 2 + width * i / nx
            f = sum(w * math.sin(2 * math.pi * x / p + ph + 0.15 * math.sin(z * 1.3 + sway))
                    for w, p, ph in zip(weights, periods, phases))
            y = at[1] + dist + amp * depth * f / 0.62
            row.append(bm.verts.new((at[0] + x, y, at[2] + 0.004 + z)))
        grid.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))   # normals toward -Y
    m = material('molton', **{'Base Color': srgb('#0B0A0C'), 'Roughness': 0.95, 'Specular IOR Level': 0.2,
                              'Sheen Weight': 0.6, 'Sheen Roughness': 0.45})
    nt = m.node_tree
    tc = _n(nt, 'ShaderNodeTexCoord')
    nz_ = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 1.2, 'Detail': 4.0})
    _l(nt, tc.outputs['Object'], nz_.inputs['Vector'])
    _l(nt, _mix(nt, _maprange(nt, nz_.outputs['Fac'], 0.35, 0.7, 0, 0.5), srgb('#0B0A0C'), srgb('#151317')),
       nt.nodes['Principled BSDF'].inputs['Base Color'])
    ob = _bm_obj('rotunda', bm, coll, m, smooth=True)
    return _flag(ob, inflamavel=True)


def palco(at=(0.0, 0.0, 0.0), x_rot_deg=0.0, plate_rot_deg=0.0, lift_dz=0.0, floor_size=16.0,
          spot=True, spot_az=-30.0, spot_el=55.0, spot_deg=26.0, spot_blend=0.04, spot_radius=None,
          pool_r=0.090, spot_aim_z=0.020, spot_kelvin=3200, balance_k=3300, spot_energy=None,
          rotunda=True, rotunda_dist=4.0, rotunda_spill=None, haze=0.0, tape_hex='#FFE81A', tape_gain=0.58,
          floor_hex='#1A1918', downstage=0.30, seed=7):
    """O PALCO (§D.6): black lacquer stage, the floor X with its lift plate, the rotunda 4 m back, the hard spot.

    at          the product placement: the X centre (the candle stands on h['place']).
    lift_dz     the lift plate's offset in metres (0 = flush, -0.100 = dropped 100 mm). Animate with lift().
    pool_r      the spot pool radius on the floor across the beam (m). The spot's throw is solved from it
                (26 deg cone): pool_r 0,090 -> 0,39 m, matching KV-01's pool rx 380 px.
    balance_k   the camera white balance the 3.200 K spot is recorded at (3.300 = a hair warm; 3.200 = neutral).
    spot_radius None = 0,0103 x throw (a 0,6 deg source: 4 mm at 0,39 m). The platform's 20 mm assumes a long
                throw; at this throw it is a 2,9 deg source and the pool edge stops being hard.
    tape_gain   0,58 (was 0,70): the tape sits ~15 % below the glass coat so cup and X separate at thumbnail size.
    floor_hex   the lacquer's ALBEDO. The platform's #0A0A0B is the floor as seen; as an albedo (0,3 %) it is darker
                than any real black paint and PBR Neutral's toe erases the lit pool. #1A1918 (1,0 %) + dust reads.
    haze        world volume density for a visible cone (platform: 0,0015). 0 = off.
    Returns a dict of handles: place, lift (carrier empty), plate, floor, tape_plate, tape_floor, spot, rotunda,
    floor_objs (light-link receivers), coll."""
    at = Vector(at)
    coll = _coll('PALCO')
    h = dict(at=tuple(at), coll=coll)
    mark = (at.x, at.y)
    decal = T.palco_decal()
    scratch = T.palco_riscos()
    lac = _lacquer_material(mark, decal, scratch, base_hex=floor_hex, downstage=downstage)
    half = 0.055                                   # lift plate: 110 mm square
    gap = 0.0006
    pr = math.radians(plate_rot_deg)

    def sq(hh):
        return [tuple(Vector(_rot2(sx * hh, sy * hh, pr)) + Vector(mark)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

    # floor with the square hole
    bm = bmesh.new()
    S2 = floor_size / 2
    _square_ring(bm, sq(half), [(at.x - S2, at.y - S2 + 3.0), (at.x + S2, at.y - S2 + 3.0),
                                 (at.x + S2, at.y + S2 + 3.0), (at.x - S2, at.y + S2 + 3.0)], at.z)
    # hole walls: the deck edge, 19 mm thick, lacquer wraps it
    c = sq(half)
    vt = [bm.verts.new((x, y, at.z)) for x, y in c]
    vb = [bm.verts.new((x, y, at.z - 0.019)) for x, y in c]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vt[i], vt[j], vb[j], vb[i]))       # faces into the hole
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    floor = _flag(_bm_obj('palco_chao', bm, coll, lac), apoio=True)
    # the shaft under the plate (matte black, open top)
    bm = bmesh.new()
    cs = sq(half + 0.0005)
    zt, zb = at.z - 0.019, at.z - 0.45
    vt = [bm.verts.new((x, y, zt)) for x, y in cs]
    vb = [bm.verts.new((x, y, zb)) for x, y in cs]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vt[i], vt[j], vb[j], vb[i]))
    bm.faces.new(vb)
    poco = _bm_obj('palco_poco', bm, coll, _plain('poco', '#050505', 0.95, 0.1))
    # the plate: same lacquer, mesh in world coords so the texture is continuous when flush
    bm = bmesh.new()
    cp = sq(half - gap / 2)
    vt = [bm.verts.new((x, y, at.z)) for x, y in cp]
    vb = [bm.verts.new((x, y, at.z - 0.018)) for x, y in cp]
    bm.faces.new(vt)
    bm.faces.new(vb[::-1])
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vt[i], vb[i], vb[j], vt[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bev = bmesh.ops.bevel(bm, geom=[e for e in bm.edges if all(v.co.z > at.z - 1e-6 for v in e.verts)],
                          offset=0.0004, segments=2, affect='EDGES')
    plate = _flag(_bm_obj('palco_elevador', bm, coll, lac), apoio=True)
    # carrier empty at the plate's top centre
    lift_e = bpy.data.objects.new('palco_elevador_carga', None)
    coll.objects.link(lift_e)
    lift_e.location = (at.x, at.y, at.z)
    lift_e.parent = plate
    # the X, cut at the seams
    tape = _tape_material(tape_hex, tape_gain)
    bm_in, bm_out = _tape_x(mark, math.radians(x_rot_deg), half, pr, gap * 1.5, at.z + 0.00002, seed=seed)
    t_in = _bm_obj('palco_x_elevador', bm_in, coll, tape)
    t_out = _bm_obj('palco_x_chao', bm_out, coll, tape)
    for t in (t_in, t_out):
        sol = t.modifiers.new('esp', 'SOLIDIFY')
        sol.thickness = 0.00025
        sol.offset = 1.0
        _flag(t, apoio=True)
    t_in.parent = plate
    h.update(floor=floor, plate=plate, lift=lift_e, tape_plate=t_in, tape_floor=t_out, shaft=poco,
             floor_objs=[floor, plate, t_in, t_out], place=(at.x, at.y, at.z + lift_dz))
    lift(h, lift_dz)
    # rotunda
    if rotunda:
        h['rotunda'] = _rotunda(coll, at, rotunda_dist)
        sp = ENERGIA['palco_spill'] if rotunda_spill is None else rotunda_spill
        if sp > 0:
            L = _light('palco_spill', 'SPOT', (at.x - 3.2, at.y + rotunda_dist - 1.6, at.z + 4.8),
                       (at.x - 1.9, at.y + rotunda_dist, at.z + 2.4), sp, color=balanced(3200, balance_k),
                       coll=coll, spot_size=math.radians(50), spot_blend=1.0, shadow_soft_size=0.25)
            link_receivers(L, [h['rotunda']])
            h['spill'] = L
    # the hard spot
    if spot:
        throw = pool_r / math.tan(math.radians(spot_deg / 2))
        tgt = at + Vector((0, 0, spot_aim_z))
        loc = tgt + _dir(spot_az, spot_el) * throw
        e = ENERGIA['palco_spot_k'] * throw ** 2 if spot_energy is None else spot_energy
        rad = 0.0103 * throw if spot_radius is None else spot_radius
        L = _light('palco_spot', 'SPOT', loc, tgt, e, color=balanced(spot_kelvin, balance_k), coll=coll,
                   spot_size=math.radians(spot_deg), spot_blend=spot_blend, shadow_soft_size=rad)
        L['kelvin'] = spot_kelvin
        L['balance_k'] = balance_k
        h['spot'] = L
        h['throw'] = throw
    if haze > 0:
        set_haze(haze)
    return h


def lift(h, dz, frame=None):
    """Move the lift plate (and everything riding it) to dz metres below flush. Keyframe if frame is given."""
    p = h['plate']
    p.location.z = dz
    if frame is not None:
        p.keyframe_insert('location', index=2, frame=frame)
    h['place'] = (h['at'][0], h['at'][1], h['at'][2] + dz)
    return h['place']


def set_haze(density=0.0015, anisotropy=0.3):
    """World volume scatter for a visible cone (no noise texture)."""
    w = bpy.context.scene.world
    nt = w.node_tree
    vs = _n(nt, 'ShaderNodeVolumeScatter', **{'Density': density, 'Anisotropy': anisotropy})
    _l(nt, vs.outputs[0], nt.nodes['World Output'].inputs['Volume'])
    return vs


# ================================================================================================================
# 2. A ESCOLA — the empty Brazilian school auditorium (C02, the ad previs)
# ================================================================================================================
import objetos as O


def _tabuado(name='tabuado', hexa='#9A6A42', hexb='#7A4F2E'):
    """Varnished wooden stage boards (planks along X, 100 mm), worn and scuffed toward the front edge."""
    m = material(name, **{'Base Color': srgb(hexa), 'Roughness': 0.38, 'Specular IOR Level': 0.45,
                          'Coat Weight': 0.35, 'Coat Roughness': 0.25})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    obj = tc.outputs['Object']
    br = _n(nt, 'ShaderNodeTexBrick', offset=0.37, offset_frequency=1, squash=1.0, squash_frequency=1)
    br.inputs['Scale'].default_value = 1.0
    br.inputs['Brick Width'].default_value = 2.1
    br.inputs['Row Height'].default_value = 0.10
    br.inputs['Mortar Size'].default_value = 0.0011
    br.inputs['Mortar Smooth'].default_value = 0.2
    br.inputs['Bias'].default_value = 0.0
    br.inputs['Color1'].default_value = srgb(hexa)
    br.inputs['Color2'].default_value = srgb(hexb)
    br.inputs['Mortar'].default_value = srgb('#1C120B')
    _l(nt, obj, br.inputs['Vector'])
    mp = _n(nt, 'ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (2.5, 60.0, 60.0)
    _l(nt, obj, mp.inputs['Vector'])
    grain = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 3.0, 'Detail': 8.0, 'Distortion': 2.5})
    _l(nt, mp.outputs[0], grain.inputs['Vector'])
    col = _mix(nt, _maprange(nt, grain.outputs['Fac'], 0.35, 0.65, 0.0, 0.35), br.outputs['Color'], srgb('#5E3B22'))
    sxy = _n(nt, 'ShaderNodeSeparateXYZ')
    _l(nt, obj, sxy.inputs[0])
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 4.0, 'Detail': 4.0})
    _l(nt, obj, nz.inputs['Vector'])
    wear = _math(nt, 'MULTIPLY', _maprange(nt, sxy.outputs['Y'], 0.9, 0.0, 0.0, 1.0),
                 _maprange(nt, nz.outputs['Fac'], 0.4, 0.7, 0.2, 1.0))
    col = _mix(nt, _math(nt, 'MULTIPLY', wear, 0.45), col, srgb('#B08A63'))
    _l(nt, col, bs.inputs['Base Color'])
    _l(nt, _maprange(nt, wear, 0, 1, 0.32, 0.65), bs.inputs['Roughness'])
    bump = _n(nt, 'ShaderNodeBump', **{'Strength': 0.25, 'Distance': 0.0004})
    _l(nt, br.outputs['Fac'], bump.inputs['Height'])
    _l(nt, bump.outputs['Normal'], bs.inputs['Normal'])
    return m


def _granilite(name='granilite'):
    """Brazilian school terrazzo (granilite): grey with marble chips, polished, scuffed."""
    m = material(name, **{'Base Color': srgb('#8E8B85'), 'Roughness': 0.28, 'Specular IOR Level': 0.5})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    vo = _n(nt, 'ShaderNodeTexVoronoi', **{'Scale': 140.0, 'Randomness': 1.0})
    _l(nt, tc.outputs['Object'], vo.inputs['Vector'])
    ramp = _n(nt, 'ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = srgb('#6E6B66')
    ramp.color_ramp.elements[1].color = srgb('#D8D3C8')
    e = ramp.color_ramp.elements.new(0.6)
    e.color = srgb('#9A968E')
    _l(nt, vo.outputs['Color'], ramp.inputs['Fac'])
    edge = _maprange(nt, vo.outputs['Distance'], 0.0, 0.35, 0.0, 1.0)
    col = _mix(nt, _math(nt, 'MULTIPLY', edge, 0.6), ramp.outputs['Color'], srgb('#8E8B85'))
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 0.6, 'Detail': 3.0})
    _l(nt, tc.outputs['Object'], nz.inputs['Vector'])
    col = _mix(nt, _maprange(nt, nz.outputs['Fac'], 0.4, 0.7, 0.0, 0.3), col, srgb('#6A665F'))
    _l(nt, col, bs.inputs['Base Color'])
    _l(nt, _maprange(nt, nz.outputs['Fac'], 0.3, 0.7, 0.22, 0.45), bs.inputs['Roughness'])
    return m


def _parede(name='parede', baixo='#7F8C78', cima='#E6DCC3', barra=1.50):
    """Two-tone school wall: oil-paint barra below (sage), cream emulsion above, a dark line between, grime."""
    m = material(name, **{'Base Color': srgb(cima), 'Roughness': 0.85, 'Specular IOR Level': 0.3})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    sxy = _n(nt, 'ShaderNodeSeparateXYZ')
    _l(nt, tc.outputs['Object'], sxy.inputs[0])
    low = _maprange(nt, sxy.outputs['Z'], barra + 0.004, barra - 0.004, 0.0, 1.0)
    line = _math(nt, 'MULTIPLY', _maprange(nt, sxy.outputs['Z'], barra + 0.02, barra + 0.008, 0, 1),
                 _maprange(nt, sxy.outputs['Z'], barra - 0.004, barra + 0.004, 0, 1))
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 1.5, 'Detail': 6.0})
    _l(nt, tc.outputs['Object'], nz.inputs['Vector'])
    up = _mix(nt, _maprange(nt, nz.outputs['Fac'], 0.45, 0.75, 0, 0.35), srgb(cima), srgb('#B9AE96'))
    dn = _mix(nt, _maprange(nt, nz.outputs['Fac'], 0.45, 0.75, 0, 0.35), srgb(baixo), srgb('#5E6858'))
    col = _mix(nt, low, up, dn)
    col = _mix(nt, line, col, srgb('#3E4A3C'))
    _l(nt, col, bs.inputs['Base Color'])
    _l(nt, _maprange(nt, low, 0, 1, 0.85, 0.45), bs.inputs['Roughness'])
    return m


def _tnt(name='tnt', hexc='#E9B6C5'):
    """Faded pink TNT (non-woven polypropylene): thin, matte, a little translucent, sun-faded in streaks."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = 0.8
    bs.inputs['Specular IOR Level'].default_value = 0.25
    bs.inputs['Sheen Weight'].default_value = 0.3
    tc = _n(nt, 'ShaderNodeTexCoord')
    mp = _n(nt, 'ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (6.0, 6.0, 0.6)
    _l(nt, tc.outputs['Object'], mp.inputs['Vector'])
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 1.0, 'Detail': 4.0})
    _l(nt, mp.outputs[0], nz.inputs['Vector'])
    col = _mix(nt, _maprange(nt, nz.outputs['Fac'], 0.35, 0.7, 0.0, 0.6), srgb(hexc), srgb('#F0CDD6'))
    fib = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 900.0, 'Detail': 2.0})
    _l(nt, tc.outputs['Object'], fib.inputs['Vector'])
    bump = _n(nt, 'ShaderNodeBump', **{'Strength': 0.15, 'Distance': 0.0002})
    _l(nt, fib.outputs['Fac'], bump.inputs['Height'])
    _l(nt, bump.outputs['Normal'], bs.inputs['Normal'])
    _l(nt, col, bs.inputs['Base Color'])
    tl = _n(nt, 'ShaderNodeBsdfTranslucent')
    _l(nt, col, tl.inputs['Color'])
    mix = _n(nt, 'ShaderNodeMixShader')
    mix.inputs[0].default_value = 0.22
    _l(nt, bs.outputs[0], mix.inputs[1])
    _l(nt, tl.outputs[0], mix.inputs[2])
    _l(nt, mix.outputs[0], nt.nodes['Material Output'].inputs[0])
    return m


def _cortina_tnt(coll, x0, x1, y, z0, z1, seed=4):
    """A TNT panel stapled along the top every ~0,4 m: swags between staples, loose vertical folds below."""
    rng = np.random.default_rng(seed)
    W = x1 - x0
    nx, nz = int(W / 0.02), 60
    staples = np.arange(x0, x1 + 1e-6, 0.40)
    per = rng.uniform(0.12, 0.30, 6)
    ph = rng.uniform(0, 6.28, 6)
    bm = bmesh.new()
    grid = []
    for j in range(nz + 1):
        t = j / nz                                  # 0 bottom, 1 top
        z = z0 + (z1 - z0) * t
        row = []
        for i in range(nx + 1):
            x = x0 + W * i / nx
            k = np.searchsorted(staples, x)
            a = staples[max(k - 1, 0)]
            b = staples[min(k, len(staples) - 1)]
            s = 0.0 if b == a else (x - a) / (b - a)
            swag = 0.035 * math.sin(math.pi * s) * t ** 6          # sag between staples at the top
            fold = sum(0.012 * math.sin(2 * math.pi * x / p + q + 0.8 * t) for p, q in zip(per, ph))
            fold *= (0.3 + 0.7 * (1 - t))
            row.append(bm.verts.new((x, y + fold, z - swag)))
        grid.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    ob = _bm_obj('tnt_fundo', bm, coll, _tnt(), smooth=True)
    return _flag(ob, inflamavel=True)


def _box(coll, name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector(((x0 + x1) / 2 + v.co.x * (x1 - x0), (y0 + y1) / 2 + v.co.y * (y1 - y0), (z0 + z1) / 2 + v.co.z * (z1 - z0)))
    ob = _bm_obj(name, bm, coll, mat)
    if bevel:
        b = ob.modifiers.new('bev', 'BEVEL')
        b.width = bevel
        b.segments = 3
    return ob


def _plane(coll, name, corners, mat):
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(c) for c in corners])
    return _bm_obj(name, bm, coll, mat)


DUSK = (1.0, 0.80, 0.72)          # dusk through frosted glass: warm rose-grey, never blue (§D.11)


def escola(at=(0.0, 0.60), rot_deg=0.0, preset='C02', candle=None, stage_h=0.45, stage_depth=3.2, stage_w=9.0,
           room_w=13.0, room_len=15.0, ceiling=4.6, front_gap=2.20, rows=6, per_row=8, chair_pitch=0.58,
           row_pitch=0.95, bag_seat=4, bag_hex='#5A3A28', spot_kelvin=3200, balance_k=3050, house=None,
           dusk=1.0, presenter_x=-0.60, seed=11):
    """A ESCOLA: an empty Brazilian school auditorium at dusk. Stage front edge on y = 0 (stage toward +Y), the
    auditorium floor at z = 0, the stage top at z = stage_h.

    at          the product placement on the stage: (x, metres in from the stage edge). C02: 0,60 m.
    rot_deg     the candle's yaw; 0 = front panel to the audience, BACK panel to the upstage C02 camera.
    preset      'C02' (spot from above-upstage, elevation 60 deg, on the candle's back panel)
                'APRESENTADORA' (spot from front-left on the presenter's mark at the stage edge)
    front_gap   distance from the stage edge to the front of the front-row seats (>= 2 m, §D.8).
    bag_seat    index (0..per_row-1) of the front-row chair the handbag saves (None = no bag).
    Returns handles: place, candle_rot, chairs, front_row, bag, backdrop, spot, presenter, stage_edge_y, coll."""
    coll = _coll('ESCOLA')
    rng = np.random.default_rng(seed)
    h = dict(coll=coll, stage_h=stage_h, stage_edge_y=0.0, preset=preset)
    # ---- room shell
    xl, xr = -room_w / 2, room_w / 2
    yb = -room_len
    floor = _plane(coll, 'escola_piso', [(xl, yb, 0), (xr, yb, 0), (xr, stage_depth, 0), (xl, stage_depth, 0)], _granilite())
    wall = _parede()
    for name, corners in (('parede_esq', [(xl, yb, 0), (xl, stage_depth, 0), (xl, stage_depth, ceiling), (xl, yb, ceiling)]),
                          ('parede_dir', [(xr, stage_depth, 0), (xr, yb, 0), (xr, yb, ceiling), (xr, stage_depth, ceiling)]),
                          ('parede_fundo', [(xr, yb, 0), (xl, yb, 0), (xl, yb, ceiling), (xr, yb, ceiling)]),
                          ('parede_palco', [(xl, stage_depth, 0), (xr, stage_depth, 0), (xr, stage_depth, ceiling), (xl, stage_depth, ceiling)])):
        _plane(coll, name, corners, wall)
    _plane(coll, 'forro', [(xl, yb, ceiling), (xl, stage_depth, ceiling), (xr, stage_depth, ceiling), (xr, yb, ceiling)],
           material('forro', **{'Base Color': srgb('#DCD8CE'), 'Roughness': 0.9}))
    # ---- the stage: varnished boards on a painted apron, a worn rounded front edge people sit on
    sw = stage_w / 2
    top = _box(coll, 'palco_tabuado', -sw, sw, 0.0, stage_depth, stage_h - 0.03, stage_h, _tabuado(), bevel=0.012)
    apron = _box(coll, 'palco_frente', -sw, sw, 0.015, stage_depth, 0.0, stage_h - 0.03,
                 material('frente_palco', **{'Base Color': srgb('#3B2F28'), 'Roughness': 0.6, 'Specular IOR Level': 0.35}))
    for ob in (top, apron):
        _flag(ob, apoio=True)
    # steps at stage left
    for k in range(3):
        _box(coll, 'degrau_%d' % k, sw - 1.1, sw - 0.1, -0.30 * (3 - k), -0.30 * (2 - k) + 0.001, 0.0,
             stage_h * (k + 1) / 3 - 0.001, _tabuado('degrau'), bevel=0.006)
    # ---- backdrop: faded pink TNT with paper flowers and hearts (no letters)
    yb_ = stage_depth - 0.22
    tnt = _cortina_tnt(coll, -3.3, 3.3, yb_, stage_h + 0.02, stage_h + 2.85)
    h['backdrop'] = tnt
    deco = []
    flower_cols = [('#E98AA8', '#F6C6D3'), ('#F4F1EA', '#FBE3EA'), ('#D9536F', '#F09AAE'), ('#F2B8C9', '#FFFFFF'),
                   ('#F3D27A', '#FBE9B5')]
    zc, R, hxc = stage_h + 1.25, 0.50, presenter_x + 0.66
    for k in range(26):                               # a big heart outline made of paper flowers
        t = 2 * math.pi * k / 26
        hx = 16 * math.sin(t) ** 3 / 17 * R
        hz = (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 * R
        f = O.flor_papel(radius=rng.uniform(0.055, 0.085), petals=int(rng.integers(7, 10)),
                         colors=flower_cols[k % len(flower_cols)], seed=k, coll=coll)
        f.location = (hxc + hx, yb_ - 0.02, zc + hz)
        f.rotation_euler = (0, rng.normal(0, 0.3), math.pi)
        deco.append(f)
    for k in range(9):                                # loose flowers in the corners
        f = O.flor_papel(radius=rng.uniform(0.07, 0.12), petals=int(rng.integers(7, 10)),
                         colors=flower_cols[int(rng.integers(0, 5))], seed=100 + k, coll=coll)
        side = -1 if k % 2 else 1
        f.location = (side * rng.uniform(2.2, 3.0), yb_ - 0.02, stage_h + rng.uniform(0.6, 2.5))
        f.rotation_euler = (0, rng.uniform(0, 6.28), math.pi)
        deco.append(f)
    heart_cols = ['#D23A55', '#F08AA5', '#FFFFFF', '#E7637F', '#C42A45']
    nh = 15                                           # a garland of paper hearts on a string, sagging
    for k in range(nh):
        s = k / (nh - 1)
        x = -2.9 + 5.8 * s
        z = stage_h + 2.55 - 0.42 * math.sin(math.pi * s)
        c = O.coracao(size=rng.uniform(0.13, 0.19), hexc=heart_cols[k % 5], seed=k, coll=coll)
        c.location = (x, yb_ - 0.08, z - 0.10)
        c.rotation_euler = (rng.normal(0, 0.08), rng.normal(0, 0.12), math.pi + rng.normal(0, 0.15))
        deco.append(c)
    cur = bpy.data.curves.new('barbante', 'CURVE')
    cur.dimensions = '3D'
    cur.bevel_depth = 0.0012
    sp = cur.splines.new('POLY')
    sp.points.add(30)
    for k, p in enumerate(sp.points):
        s = k / 30
        p.co = (-3.0 + 6.0 * s, yb_ - 0.075, stage_h + 2.55 - 0.42 * math.sin(math.pi * (6.0 * s - 0.1) / 5.8), 1)
    string = bpy.data.objects.new('barbante', cur)
    coll.objects.link(string)
    cur.materials.append(material('barbante', **{'Base Color': srgb('#E9E1D0'), 'Roughness': 0.9}))
    for o in deco + [string]:
        _flag(o, inflamavel=True)
    h['decor'] = deco
    # ---- chairs: one modelled monobloc, linked duplicates in rows
    proto = O.monobloco(coll=coll)
    proto.rotation_euler = (0, 0, 0)                 # modelled facing +Y: toward the stage
    chairs, front = [], []
    for r in range(rows):
        yc = -front_gap - 0.26 - r * row_pitch
        for c in range(per_row):
            if r > 2 and rng.random() < 0.12:         # a few gaps in the back rows
                continue
            x = (c - (per_row - 1) / 2) * chair_pitch
            ob = proto if (r == 0 and c == 0) else proto.copy()
            if ob is not proto:
                coll.objects.link(ob)
            j = 0.015 if r == 0 else 0.035
            ob.location = (x + rng.normal(0, j), yc + rng.normal(0, j), 0)
            ob.rotation_euler = (0, 0, math.radians(rng.normal(0, 2.0 if r == 0 else 5.0)))
            _flag(ob, inflamavel=True)
            chairs.append(ob)
            if r == 0:
                front.append(ob)
    h['chairs'], h['front_row'] = chairs, front
    if bag_seat is not None and 0 <= bag_seat < len(front):
        ch = front[bag_seat]
        bag = O.bolsa(coll=coll, hexc=bag_hex)
        bag.location = ch.location + Vector((0.01, -0.015, ch['assento_z'] - 0.006))
        bag.rotation_euler = (0, 0, ch.rotation_euler.z + math.radians(9))
        _flag(bag, inflamavel=True)
        h['bag'] = bag
    # ---- fluorescent fittings, OFF
    for gx in (-3.6, 0.0, 3.6):
        for gy in np.arange(-1.5, -room_len + 1.0, -2.6):
            f = O.calha(coll=coll)
            f.location = (gx, gy, ceiling)
            f.rotation_euler = (0, 0, math.pi / 2)
    # ---- high windows on the left wall (dusk through frosted glass) + a double door at the back
    win = bpy.data.materials.new('vidro_crepusculo')
    win.use_nodes = True
    wnt = win.node_tree
    wnt.nodes.clear()
    em = _n(wnt, 'ShaderNodeEmission')
    em.inputs['Color'].default_value = srgb('#C8A592')
    em.inputs['Strength'].default_value = 1.2 * dusk
    _l(wnt, em.outputs[0], _n(wnt, 'ShaderNodeOutputMaterial').inputs['Surface'])
    frame = material('caixilho', **{'Base Color': srgb('#2B2B29'), 'Roughness': 0.5, 'Metallic': 0.6})
    for wy in np.arange(-2.5, -room_len + 1.5, -3.2):
        _plane(coll, 'janela', [(xl + 0.01, wy - 0.7, 2.55), (xl + 0.01, wy + 0.7, 2.55), (xl + 0.01, wy + 0.7, 3.45),
                                (xl + 0.01, wy - 0.7, 3.45)], win)
        for k in range(5):                         # vitrô bars
            yy = wy - 0.7 + 1.4 * k / 4
            _box(coll, 'caixilho', xl + 0.01, xl + 0.04, yy - 0.012, yy + 0.012, 2.55, 3.45, frame)
        for zz in (2.55, 3.0, 3.45):
            _box(coll, 'caixilho', xl + 0.01, xl + 0.04, wy - 0.7, wy + 0.7, zz - 0.012, zz + 0.012, frame)
        if dusk > 0:
            L = _light('crepusculo', 'AREA', (xl + 0.05, wy, 3.0), (xl + 3.0, wy + 0.5, 0.6), 60.0 * dusk,
                       color=DUSK, coll=coll, shape='RECTANGLE', size=1.4, size_y=0.9)
    door = material('porta', **{'Base Color': srgb('#6B5B4A'), 'Roughness': 0.5})
    _box(coll, 'porta', -1.0, 1.0, yb + 0.005, yb + 0.05, 0.0, 2.3, door)
    win = win.copy()
    win.node_tree.nodes['Emission'].inputs['Strength'].default_value = 0.35 * dusk
    for sx in (-0.5, 0.5):
        _plane(coll, 'porta_vidro', [(sx - 0.25, yb + 0.055, 1.4), (sx + 0.25, yb + 0.055, 1.4),
                                     (sx + 0.25, yb + 0.055, 2.0), (sx - 0.25, yb + 0.055, 2.0)], win)
    # ---- house practicals: four bulbs in globes on the side walls, dimmed to ~5 %
    hs = ENERGIA['escola_house'] if house is None else house
    glow = bpy.data.materials.new('globo')
    glow.use_nodes = True
    gnt = glow.node_tree
    gnt.nodes.clear()
    gem = _n(gnt, 'ShaderNodeEmission')
    gem.inputs['Color'].default_value = balanced(2700, balance_k) + (1.0,)
    gem.inputs['Strength'].default_value = 6.0 * hs
    _l(gnt, gem.outputs[0], _n(gnt, 'ShaderNodeOutputMaterial').inputs['Surface'])
    for gx in (xl + 0.18, xr - 0.18):
        for gy in (-3.0, -9.0):
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=0.09)
            g = _bm_obj('globo', bm, coll, glow, smooth=True)
            g.location = (gx, gy, 2.55)
            _light('pratico', 'POINT', (gx + (0.12 if gx < 0 else -0.12), gy, 2.55), None, 25.0 * hs,
                   color=balanced(2700, balance_k), coll=coll, shadow_soft_size=0.09)
    # ---- ambience: a dim warm world so nothing is pure digital black
    w = bpy.context.scene.world
    w.node_tree.nodes['Background'].inputs[0].default_value = srgb('#3A322C')
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.02 * dusk
    # ---- product placement and the spot
    px, py = at
    h['place'] = (px, py, stage_h)
    h['candle_rot'] = rot_deg
    h['presenter'] = (presenter_x, 0.14, stage_h)
    if preset == 'C02':
        throw = 3.2
        tgt = Vector((px, py, stage_h + 0.04))
        loc = tgt + _dir(180.0 - 6.0, 60.0) * throw
        e = ENERGIA['escola_spot_k'] * throw ** 2
        L = _light('escola_spot', 'SPOT', loc, tgt, e, color=balanced(spot_kelvin, balance_k), coll=coll,
                   spot_size=math.radians(18), spot_blend=0.05, shadow_soft_size=0.0103 * throw)
        # the same lantern's spill (lens halation): a wide, dim cone that reaches the front row
        sp = _light('escola_spill', 'SPOT', loc, Vector((px, py - 2.6, 0.5)), e * ENERGIA['escola_spill'],
                    color=balanced(spot_kelvin, balance_k), coll=coll, spot_size=math.radians(75), spot_blend=1.0,
                    shadow_soft_size=0.15)
        h['spill'] = sp
    else:
        # front-of-house spot from front-left, low and long so the beam carries past her onto the TNT
        throw = 8.0
        tgt = Vector((presenter_x, 0.14, stage_h + 0.50))
        loc = tgt + _dir(-35.0, 22.0) * throw
        e = ENERGIA['escola_spot_k'] * throw ** 2 * ENERGIA['escola_presenter']
        L = _light('escola_spot', 'SPOT', loc, tgt, e, color=balanced(spot_kelvin, balance_k), coll=coll,
                   spot_size=math.radians(30), spot_blend=0.22, shadow_soft_size=0.06)
    h['spot'] = L
    h['throw'] = throw
    return h


def escola_camera(h, preset='C02', res=None):
    """Camera presets (they set the render resolution too).
    'C02'           4:5, 85 mm, 0,72 m upstage of the candle and 0,03 m to its left (audience view), lens 21 cm
                    above the stage, level (verticals straight, lens shift only): the back panel pin-sharp right of
                    centre, the front row compressed across the frame above the stage edge, the handbag's seat
                    clear of the candle. f/16 so the monoblocs still read.
    'APRESENTADORA' 9:16, 50 mm, eye level of a person sitting on the stage edge (stage + 0,78 m), 1,40 m away,
                    locked off. Behind her the TNT backdrop."""
    if preset == 'C02':
        res = res or (1080, 1350)
        px, py, pz = h['place']
        sx = res[0] / 1080.0
        cam = camera_pin((px + 0.03, py + 0.72, pz + 0.21), 180.0, 0.0, 85, res, (px, py, pz + 0.044),
                         (610 * sx, 1010 * sx), fstop=16.0, focus=0.69)
    else:
        res = res or (1080, 1920)
        x, y, z = h['presenter']
        eye = z + 0.78
        sx = res[0] / 1080.0
        cam = camera_pin((x, y - 1.40, eye), 0.0, -3.0, 50, res, (x, y, eye - 0.08), (540 * sx, 760 * sx),
                         fstop=4.0, focus=1.40)
    return cam


def figura_sentada(h, coll=None):
    """A grey PREVIS stand-in for a person sitting on the stage edge, legs dangling (never delivered)."""
    x, y, z = h['presenter']
    m = material('figura', **{'Base Color': srgb('#7E7B78'), 'Roughness': 0.8})
    parts = []
    def cap(p0, p1, r):
        bm = bmesh.new()
        path = [Vector(p0).lerp(Vector(p1), t / 6) for t in range(7)]
        prof = [(r * math.cos(2 * math.pi * k / 16), r * math.sin(2 * math.pi * k / 16)) for k in range(16)]
        O.sweep(bm, path, prof, [Vector((0, 1, 0.01))] * 7)
        ob = _bm_obj('figura_p', bm, coll or h['coll'], m, smooth=True)
        parts.append(ob)
    cap((x, y + 0.02, z + 0.10), (x, y + 0.04, z + 0.58), 0.15)                   # torso
    for sxo in (-0.10, 0.10):
        cap((x + sxo, y + 0.02, z + 0.06), (x + sxo, y - 0.38, z + 0.07), 0.075)  # thighs over the edge
        cap((x + sxo, y - 0.40, z + 0.05), (x + sxo, y - 0.44, z - 0.38), 0.055)  # shins hanging
        cap((x + 1.9 * sxo, y + 0.0, z + 0.52), (x + 1.6 * sxo, y - 0.12, z + 0.20), 0.045)   # arms
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.105)
    hd = _bm_obj('figura_cabeca', bm, coll or h['coll'], m, smooth=True)
    hd.location = (x, y + 0.03, z + 0.74)
    parts.append(hd)
    for p in parts:
        _flag(p, inflamavel=True)
    return parts


# ================================================================================================================
# 3. O MURO — plaster, pasted lambe posters, a dried glue drip, a concrete ledge, the hard on-camera flash
# ================================================================================================================
PLACEHOLDER = ['#FFE81A', '#FF4FA0', '#FF6A1A', '#8424F5', '#FFF8EC']
# C01's default wall (row-major from the top-left). The headline poster 12 (MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ.)
# sits top-centre, clear of the candles; the posters behind the ledge's candle group contrast with them (rosa and
# amarelo candles before violeta 04, laranja and violeta candles before amarelo 05); the torn 07/08 and the old
# layers 09-11 give the wall its history; the bottom row runs under the ledge.
C01_GRADE = ['07', '12', '03', '06',
             '10', '04', '05', '08',
             '01', '02', '11', '09']


def cartazes(folder=CARTAZES):
    """The brand team's lambe posters, keyed by id, once PRONTO.txt exists: {id: dict(albedo, altura, nome, papel)}.
    Returns {} (=> flat placeholders) while the folder is not ready."""
    import json
    if not os.path.exists(os.path.join(folder, 'PRONTO.txt')):
        return {}
    out = {}
    man = os.path.join(folder, 'cartazes.json')
    if os.path.exists(man):
        for c in json.load(open(man))['cartazes']:
            arq = [os.path.join(folder, a) for a in c['arquivos']]
            alb = next((a for a in arq if a.endswith('_albedo.png')), None)
            alt = next((a for a in arq if a.endswith('_altura.png')), None)
            if alb and os.path.exists(alb):
                out[c['id']] = dict(albedo=alb, altura=alt if alt and os.path.exists(alt) else None,
                                    nome=c.get('nome', c['id']), papel=c.get('papel'))
    else:
        for p in sorted(glob.glob(os.path.join(folder, '3d', '*_albedo.png'))):
            k = os.path.basename(p).split('_')[0].replace('CARTAZ-', '')
            alt = p.replace('_albedo.png', '_altura.png')
            out[k] = dict(albedo=p, altura=alt if os.path.exists(alt) else None, nome=k, papel=None)
    return out


def _poster_material(spec, name, seed):
    """Lambe paper: the brand's albedo (never retouched) with its torn-edge alpha; matte paper with a semi-gloss
    film of dried paste in broad brush strokes. A placeholder is a flat colour field."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Specular IOR Level'].default_value = 0.4
    tc = _n(nt, 'ShaderNodeTexCoord')
    out = nt.nodes['Material Output']
    if 'albedo' in spec:
        ti = _img(nt, spec['albedo'], colorspace='sRGB', ext='CLIP', interp='Cubic')
        ti.image.alpha_mode = 'STRAIGHT'
        _l(nt, tc.outputs['UV'], ti.inputs['Vector'])
        _l(nt, ti.outputs['Color'], bs.inputs['Base Color'])
        alpha = ti.outputs['Alpha']
    else:
        bs.inputs['Base Color'].default_value = srgb(spec['cor'])
        alpha = None
    # paste film: broad near-horizontal brush strokes of lower roughness
    mp = _n(nt, 'ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (3.0, 30.0, 3.0)
    mp.inputs['Location'].default_value = (seed * 1.7, seed * 0.3, 0)
    _l(nt, tc.outputs['Object'], mp.inputs['Vector'])
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 1.0, 'Detail': 3.0, 'Distortion': 0.6})
    _l(nt, mp.outputs[0], nz.inputs['Vector'])
    _l(nt, _maprange(nt, nz.outputs['Fac'], 0.35, 0.7, 0.78, 0.42), bs.inputs['Roughness'])
    if alpha is not None:
        tr = _n(nt, 'ShaderNodeBsdfTransparent')
        mix = _n(nt, 'ShaderNodeMixShader')
        _l(nt, alpha, mix.inputs[0])
        _l(nt, tr.outputs[0], mix.inputs[1])
        _l(nt, bs.outputs[0], mix.inputs[2])
        _l(nt, mix.outputs[0], out.inputs['Surface'])
    return m


def _poster(coll, spec, w, h_, loc, rot_deg, name, seed, res=0.003, amp=0.0006):
    """One pasted poster: a grid in the XZ plane facing -Y, displaced by its height map (0,6 mm, midlevel 0,5)."""
    nx, nz = max(2, int(w / res)), max(2, int(h_ / res))
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new('UVMap')
    g = [[bm.verts.new((-w / 2 + w * i / nx, 0.0, -h_ / 2 + h_ * j / nz)) for i in range(nx + 1)] for j in range(nz + 1)]
    for j in range(nz):
        for i in range(nx):
            f = bm.faces.new((g[j][i], g[j][i + 1], g[j + 1][i + 1], g[j + 1][i]))     # normal -Y (to camera)
            for lp, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                lp[uvl].uv = (a / nx, b / nz)
    ob = _bm_obj(name, bm, coll, _poster_material(spec, name + '_mat', seed), smooth=True)
    hp = spec.get('altura') or T.rugas_cartaz(seed=seed % 7 + 1)
    tex = bpy.data.textures.new(name + '_alt', 'IMAGE')
    tex.image = bpy.data.images.load(hp, check_existing=True)
    tex.image.colorspace_settings.name = 'Non-Color'
    tex.extension = 'EXTEND'
    d = ob.modifiers.new('rugas', 'DISPLACE')
    d.texture = tex
    d.texture_coords = 'UV'
    d.direction = 'NORMAL'
    d.strength = amp if spec.get('altura') else amp * 1.6
    d.mid_level = 0.5
    ob.location = Vector(loc)
    ob.rotation_euler = (0, math.radians(rot_deg), 0)
    return _flag(ob, inflamavel=True)


def _reboco_material(name='reboco', hexc='#B9B1A3'):
    """Rough street plaster (reboco/chapisco): grainy bump, rain-streak stains, worn paint, matte."""
    path = T.reboco()
    m = material(name, **{'Base Color': srgb(hexc), 'Roughness': 0.92, 'Specular IOR Level': 0.3})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    mp = _n(nt, 'ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (math.radians(90), 0, 0)     # wall in XZ: map (x, z)
    _l(nt, tc.outputs['Object'], mp.inputs['Vector'])
    ti = _img(nt, path, interp='Cubic')
    _l(nt, mp.outputs[0], ti.inputs['Vector'])
    sep = _n(nt, 'ShaderNodeSeparateColor')
    _l(nt, ti.outputs['Color'], sep.inputs['Color'])
    hgt, stain, wear = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    col = _mix(nt, _maprange(nt, stain, 0.35, 0.85, 0.0, 0.28), srgb(hexc), srgb('#8A8174'))
    col = _mix(nt, _math(nt, 'MULTIPLY', wear, 0.35), col, srgb('#A59D90'))
    col = _mix(nt, _maprange(nt, hgt, 0.3, 0.7, 0.10, 0.0), col, srgb('#6E675C'))   # grain pits hold dirt
    _l(nt, col, bs.inputs['Base Color'])
    b = _n(nt, 'ShaderNodeBump', **{'Strength': 0.8, 'Distance': 0.0015})
    _l(nt, hgt, b.inputs['Height'])
    _l(nt, b.outputs['Normal'], bs.inputs['Normal'])
    return m


def _concreto(name='concreto', hexc='#8C887F'):
    m = material(name, **{'Base Color': srgb(hexc), 'Roughness': 0.88, 'Specular IOR Level': 0.35})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord')
    vo = _n(nt, 'ShaderNodeTexVoronoi', **{'Scale': 260.0})
    _l(nt, tc.outputs['Object'], vo.inputs['Vector'])
    nz = _n(nt, 'ShaderNodeTexNoise', **{'Scale': 9.0, 'Detail': 8.0})
    _l(nt, tc.outputs['Object'], nz.inputs['Vector'])
    col = _mix(nt, _maprange(nt, vo.outputs['Distance'], 0.0, 0.5, 0.35, 0.0), srgb(hexc), srgb('#A9A497'))
    col = _mix(nt, _maprange(nt, nz.outputs['Fac'], 0.45, 0.8, 0.0, 0.5), col, srgb('#5F5B54'))
    _l(nt, col, bs.inputs['Base Color'])
    b = _n(nt, 'ShaderNodeBump', **{'Strength': 0.5, 'Distance': 0.001})
    _l(nt, vo.outputs['Distance'], b.inputs['Height'])
    _l(nt, b.outputs['Normal'], bs.inputs['Normal'])
    return m


def _glue_drip(coll, top, length=0.16, seed=3):
    """A dried paste drip from a poster's bottom edge: a thin flattened rivulet ending in a bead."""
    rng = np.random.default_rng(seed)
    top = Vector(top)
    pts, rr = [], []
    n = 24
    for i in range(n + 1):
        t = i / n
        pts.append(top + Vector((0.004 * math.sin(t * 5 + seed) + rng.normal(0, 0.0006), -0.0008, -length * t)))
        rr.append(0.0028 * (1 - 0.45 * t) + (0.0028 * max(0, (t - 0.88) / 0.12) ** 0.6))
    bm = bmesh.new()
    prof = [(math.cos(2 * math.pi * k / 12), 0.35 * math.sin(2 * math.pi * k / 12)) for k in range(12)]
    O.sweep(bm, pts, prof, [Vector((0, -1, 0))] * len(pts), scales=[(r, r) for r in rr])
    m = material('cola_seca', **{'Base Color': srgb('#EDE4CF'), 'Roughness': 0.12, 'Specular IOR Level': 0.5,
                                 'Transmission Weight': 0.35, 'Coat Weight': 0.5, 'Coat Roughness': 0.08})
    return _bm_obj('cola_escorrida', bm, coll, m, smooth=True)


def muro(n=4, spacing=0.125, grade=None, cols=4, rows=3, poster_w=0.32, ledge_z=None, ledge_depth=0.13,
         wall_w=3.2, wall_h=2.6, drip_cell=2, folder=CARTAZES, posters=True, seed=21):
    """O MURO: a plaster wall (plane y = 0, facing -Y) with lambe posters in a cols x rows grid, a concrete ledge
    across the lower third, a dried glue drip. Posters are the brand team's 01_MARCA/cartazes/ (PRONTO.txt) or flat
    placeholders. Candles stand on h['slots'] (n of them, `spacing` apart, centred), unlit (§D.8: the ledge is
    within 30 cm of the paper — clearance() says NO for a lit candle here).
    grade      list of poster ids, row-major from the top-left (default C01_GRADE); a hex string = placeholder colour.
    poster_w   poster width in metres (the art is 2:3).
    posters    False = bare plaster (C10 'O MURO flash on plaster'); the ledge and grid geometry stay the same."""
    coll = _coll('MURO')
    rng = np.random.default_rng(seed)
    h = dict(coll=coll)
    ph = poster_w * 1.5
    gw = cols * poster_w - (cols - 1) * 0.012
    gh = rows * ph - (rows - 1) * 0.012
    z_base = 0.10
    if ledge_z is None:
        ledge_z = z_base + gh / 3.0
    # wall
    bm = bmesh.new()
    vs = [bm.verts.new(c) for c in ((-wall_w / 2, 0, 0), (wall_w / 2, 0, 0), (wall_w / 2, 0, wall_h + 0.4),
                                    (-wall_w / 2, 0, wall_h + 0.4))]
    bm.faces.new(vs)
    wall = _bm_obj('muro_reboco', bm, coll, _reboco_material())
    # ground (sidewalk) so the ledge sits somewhere
    _plane(coll, 'calcada', [(-wall_w / 2, -1.5, 0), (wall_w / 2, -1.5, 0), (wall_w / 2, 0, 0), (-wall_w / 2, 0, 0)],
           _concreto('calcada', '#7E7A73'))
    # posters
    pool = cartazes(folder)
    grade = grade or C01_GRADE
    show = posters
    posters = []
    k = 0
    for r in range(rows if show else 0):
        for c in range(cols):
            gid = grade[k % len(grade)]
            spec = pool.get(gid) if pool else None
            if spec is None:
                spec = dict(cor=gid if str(gid).startswith('#') else PLACEHOLDER[k % len(PLACEHOLDER)])
            x = -gw / 2 + poster_w / 2 + c * (poster_w - 0.012) + rng.normal(0, 0.006)
            z = z_base + gh - ph / 2 - r * (ph - 0.012) + rng.normal(0, 0.006)
            y = -0.0004 - 0.00025 * k                  # later posters on top
            p = _poster(coll, spec, poster_w, ph, (x, y, z), rng.normal(0, 0.5), 'cartaz_%02d' % k, seed + k)
            p['cartaz'] = str(gid)
            posters.append(p)
            k += 1
    h['posters'] = posters
    h['placeholders'] = not bool(pool)
    # the glue drip from the bottom edge of one poster
    if show and drip_cell is not None and 0 <= drip_cell < len(posters):
        p = posters[drip_cell]
        top = p.location + Vector((poster_w * 0.18, -0.0012, -ph / 2 + 0.004))
        h['drip'] = _glue_drip(coll, top, length=0.15, seed=seed)
    # the concrete ledge (chipped edges)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * wall_w, -ledge_depth / 2 + v.co.y * ledge_depth - 0.002, ledge_z - 0.035 + v.co.z * 0.07))
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=24, use_grid_fill=True)
    for v in bm.verts:
        if v.co.y < -ledge_depth + 0.004 and v.co.z > ledge_z - 0.004:
            v.co.z -= abs(rng.normal(0, 0.0015))
            v.co.y += abs(rng.normal(0, 0.0012))
    ledge = _bm_obj('muro_peitoril', bm, coll, _concreto())
    bv = ledge.modifiers.new('bev', 'BEVEL')
    bv.width = 0.004
    bv.segments = 2
    _flag(ledge, apoio=True)
    # two steel brackets under the cantilevered ledge, outside the poster field
    for bx in (-gw / 2 - 0.10, gw / 2 + 0.10):
        _box(coll, 'muro_mao_francesa', bx - 0.012, bx + 0.012, -ledge_depth + 0.02, -0.001, ledge_z - 0.22, ledge_z - 0.07,
             material('ferro', **{'Base Color': srgb('#3A3530'), 'Roughness': 0.6, 'Metallic': 0.7}))
    h['ledge_z'] = ledge_z
    h['slots'] = [(-(n - 1) / 2 * spacing + i * spacing, -ledge_depth / 2 - 0.002, ledge_z) for i in range(n)]
    h['grid'] = dict(w=gw, h=gh, z0=z_base, poster_w=poster_w, poster_h=ph)
    # a very dim warm ambience so the flash shadow is not digital black
    w = bpy.context.scene.world
    w.node_tree.nodes['Background'].inputs[0].default_value = srgb('#4A3E33')
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.015
    return h


def flash(cam, offset=(-0.05, 0.15), size=0.03, energy=None, target_dist=1.0, stop=0.0, name='flash'):
    """The hard on-camera flash: a 3 x 3 cm area light 15 cm above the lens axis (and 5 cm left, so the hard shadow
    falls down-right), parented to the camera, firing along the view. Energy = ENERGIA['muro_flash_k'] x d^2, d the
    distance to the subject plane. stop: extra stops over the coating calibration. Under PBR Neutral paper never truly
    clips: at 0 the papel poster reads ~(242, 236, 222) and the coating dE00 2,8; at +0,5 paper (249, 243, 232) and the
    coating washes to dE00 4,0 (saturation 0,73) — the platform's '+0,5 stop' costs the coating rule."""
    e = (ENERGIA['muro_flash_k'] * target_dist ** 2 if energy is None else energy) * 2.0 ** stop
    L = bpy.data.lights.new(name, 'AREA')
    L.shape = 'SQUARE'
    L.size = size
    L.energy = e
    L.color = (1.0, 0.985, 0.96)                     # 5.500 K flash, recorded near daylight balance
    ob = bpy.data.objects.new(name, L)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = cam
    ob.location = (offset[0], offset[1], 0.0)        # camera local: x right, y up, -z forward
    ob.rotation_euler = (0, 0, 0)
    return ob


def muro_camera(h, preset='C01', res=None, flash_on=True, stop=0.0):
    """'C01' 4:5: the whole poster grid, the ledge at 1/3 height, the candles centred, 50 mm, straight on.
    'C10' 4:5: closer, 85 mm at 1,12 m: the ledge's three glasses (0,11 m apart) ~26 % of frame height."""
    g = h['grid']
    res = res or (1080, 1350)
    sx = res[0] / 1080.0
    if preset == 'C01':
        lens = 50.0
        H_ = g['h'] * 1.0
        d = (H_ / 2) / math.tan(math.atan(18 / lens)) + 0.0
        cam = camera_pin((0.0, -d, h['ledge_z'] + 0.25), 0.0, 0.0, lens, res, (0.0, 0.0, h['ledge_z']),
                         (540 * sx, 1350 * sx * 2 / 3), fstop=8.0, focus=d - 0.06)
        dist = d
    else:
        lens = 85.0
        d = 1.12
        cam = camera_pin((0.0, -d, h['ledge_z'] + 0.10), 0.0, 0.0, lens, res, (0.0, -0.06, h['ledge_z'] + 0.044),
                         (540 * sx, 860 * sx), fstop=8.0, focus=d - 0.06)
        dist = d
    if flash_on:
        h['flash'] = flash(cam, target_dist=dist, stop=stop)
    return cam


# ================================================================================================================
# 4. LOJA — seamless shadow catcher, key + bounce; the #FFF8EC plate is added by code afterwards (loja_plate)
# ================================================================================================================
def loja(at=(0.0, 0.0, 0.0), key_az=-45.0, key_el=35.0, key_dist=1.2, key_size=0.30, fill_ratio=0.20,
         sweep_back=0.55, balance=None):
    """LOJA (§D.6, §E.3): render with S.cena(transparent=True). A seamless (floor, 0,35 m cove, back) that is a SHADOW
    CATCHER in papel, so it keeps the contact shadow and bounces papel light while the background stays alpha for
    the code-filled #FFF8EC plate. Key: 30 x 30 cm at 1,2 m, 45 deg left, elevation 35 deg. Fill: a white bounce on
    the right at 20 % of the key (a soft 0,8 x 1,0 m source, visible in the coat as a reflection strip).
    The cove starts `sweep_back` behind the product (>= 0,30 m from a lit flame, §D.8)."""
    coll = _coll('LOJA')
    at = Vector(at)
    h = dict(coll=coll, at=tuple(at), place=tuple(at))
    # seamless: floor -> cove -> back, as one shadow-catcher surface
    bm = bmesh.new()
    prof = [(-1.2 + 0.05 * i, 0.0) for i in range(int((sweep_back + 1.2) / 0.05) + 1)]
    R = 0.35
    for k in range(1, 13):
        a = math.radians(90 * k / 12)
        prof.append((sweep_back + R * math.sin(a), R * (1 - math.cos(a))))
    prof += [(sweep_back + R, R + 0.25 * i) for i in range(1, 9)]
    W = 3.0
    pm = material('papel_fundo', **{'Base Color': srgb(PAPEL_HEX), 'Roughness': 0.9, 'Specular IOR Level': 0.2})
    n_floor = sum(1 for y, z in prof if z == 0.0)
    parts = []
    for name, seg, flag in (('loja_fundo_chao', prof[:n_floor], dict(apoio=True)),
                            ('loja_fundo_curva', prof[n_floor - 1:], dict(inflamavel=True))):
        bm = bmesh.new()
        rows = [[bm.verts.new((at.x + xx, at.y + y, at.z + z)) for xx in (-W / 2, W / 2)] for y, z in seg]
        for i in range(len(rows) - 1):
            bm.faces.new((rows[i][0], rows[i][1], rows[i + 1][1], rows[i + 1][0]))
        ob = _bm_obj(name, bm, coll, pm, smooth=True)
        ob.is_shadow_catcher = True
        parts.append(_flag(ob, **flag))
    h['seamless'] = parts[0]
    h['seamless_parts'] = parts
    tgt = at + Vector((0, 0, 0.044))
    e = ENERGIA['loja_key_k'] * key_dist ** 2
    key = _light('loja_key', 'AREA', tgt + _dir(key_az, key_el) * key_dist, tgt, e, coll=coll, shape='SQUARE',
                 size=key_size)
    fill = _light('loja_rebatedor', 'AREA', tgt + _dir(60.0, 15.0) * key_dist, tgt, e * fill_ratio, coll=coll,
                  shape='RECTANGLE', size=0.8, size_y=1.0)
    h['key'], h['fill'] = key, fill
    return h


PAPEL_HEX = '#FFF8EC'


def loja_camera(h, preset='L01', res=(1200, 1200), fill=0.65, size='200', center_x=None):
    """'L01' 85 mm, lens at label height (52 mm), 0 deg tilt; the candle is turned 20 deg (3/4 front) by the caller.
    'L05' 3/4 front, 25 deg down. Product centred, glass `fill` of the frame height (§D.10: >= 62 %)."""
    at = h['at']
    gp = int(round(res[1] * fill))
    top = (res[1] - gp) // 2
    if preset == 'L01' and center_x is None:
        center_x = 0.40 * res[0]                    # the candle left of centre, the leaning lid to its right
    if preset == 'L01':
        s = camera_glass(res=res, lens=85, cam_height=0.052, tilt_deg=0.0, glass_px=gp, top_y=top, at=at, size=size,
                         center_x=center_x)
    else:
        s = camera_glass(res=res, lens=85, cam_height=0.0, tilt_deg=-25.0, glass_px=gp, top_y=top, at=at, size=size)
        # height solved from the 25 deg line of sight, then re-solved so the glass still spans gp
        d = s['distance']
        s = camera_glass(res=res, lens=85, cam_height=0.044 + d * math.tan(math.radians(25)), tilt_deg=-25.0,
                         glass_px=gp, top_y=top, at=at, size=size, center_x=center_x)
    return s['object']


def tampa_encostada(h, side=1, art=None, size='200'):
    """L01: the lid leaning against the candle's right side, its top (the X, 'ela fica aqui.') to camera."""
    t = H.tampa(art or tampa_art(size), size=size)
    at = Vector(h['at'])
    t.location = at + Vector((side * 0.072, 0.014, 0.0))
    t.rotation_euler = (math.radians(78), 0.0, math.radians(side * 14))     # top to camera, leaning back 12 deg
    bpy.context.view_layer.update()
    # rest the lowest point of the tilted disc on the floor
    zmin = min((o.matrix_world @ Vector(c)).z for o in descendants(t) if o.type == 'MESH' for c in o.bound_box)
    t.location.z -= zmin - at.z
    return t


def loja_plate(png_in, png_out, hexc=PAPEL_HEX):
    """Composite a transparent LOJA render (with its caught shadow) over the exact papel plate, by code."""
    from PIL import Image
    im = Image.open(png_in).convert('RGBA')
    plate = Image.new('RGBA', im.size, tuple(int(hexc.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    Image.alpha_composite(plate, im).convert('RGB').save(png_out)
    return png_out


def fila(sizes=('200', '200', '200', '200'), gap=0.018, at=(0.0, 0.0, 0.0)):
    """Positions for a lineup (L06 · A TURNÊ, C04, C01's ledge): candles of the given sizes ('200' Ø76, '080' Ø58)
    side by side along X with `gap` metres between glasses, centred on `at`. Extra widths (a capsule) as floats (m)."""
    widths = [(2 * H.SIZES[s]['R_OUT'] * MM) if isinstance(s, str) else float(s) for s in sizes]
    total = sum(widths) + gap * (len(widths) - 1)
    x = at[0] - total / 2
    out = []
    for w in widths:
        out.append((x + w / 2, at[1], at[2]))
        x += w + gap
    return out
