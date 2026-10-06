"""HOLOFOTE · objects library: the props around the candle (platform §C.6–§C.9, §D.6, §E.2–E.3, §F.1–F.2).

Blender 4.5, Cycles. Units: specs in millimetres, Blender in metres (MM = 0.001). Every builder returns a `Built`
(an attribute bag whose `.root` is an empty): move or rotate the root, never the parts. Objects stand on z = 0 and
face the camera at -Y, like holofote.copo(). Printed art always comes from an image file mapped by UV, never from
a generator; every art path is a parameter, and until the packaging team's files exist the neutral placeholders
in ./placeholders are used (regenerate with make_placeholders.py).

    import sys; sys.path.insert(0, '.../_build/objects'); import objects_lib as O
    c = O.case(state='open', open_deg=O.open_deg_for_camera(70), copo=dict(faixa='02', wrap=WRAP))
    O.place_work_bulb(c, camera_object)

See LEIA_ME.md for the full API, the art conventions and the known spec conflicts.
"""
import bpy, bmesh, math, os, sys, glob
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(KIT, '_build', 'blender'))
from candle_lib import MM, srgb, material  # noqa: E402
import holofote as H  # noqa: E402  (the director's candle; used, never edited)

PRODUTO = os.path.join(KIT, '02_PRODUTO')
PH = os.path.join(HERE, 'placeholders')
PRETO, PAPEL, AMARELO = '#121014', '#FFF8EC', '#FFE81A'
FAIXA_COAT = {k: v['coat'] for k, v in H.FAIXAS.items()}


# =============================================================================================== small utilities
class Built:
    """Attribute bag returned by every builder (root plus named parts)."""
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        return 'Built(%s)' % ', '.join(self.__dict__)


def ph(name):
    """Path of a placeholder image; builds the set on first use."""
    p = os.path.join(PH, name)
    if not os.path.exists(p):
        import importlib.util
        spec = importlib.util.spec_from_file_location('make_placeholders', os.path.join(HERE, 'make_placeholders.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    return p


def find_art(folder, *keys):
    """First PNG in 02_PRODUTO/<folder>/ whose name contains every key (case-insensitive), else None."""
    d = os.path.join(PRODUTO, folder)
    if not os.path.isdir(d):
        return None
    for p in sorted(glob.glob(os.path.join(d, '*.png'))):
        n = os.path.basename(p).lower()
        if all(k.lower() in n for k in keys):
            return p
    return None


def pfile(folder, name):
    """02_PRODUTO/<folder>/<name> if it exists, else None (explicit file contracts, never keyword guesses)."""
    q = os.path.join(PRODUTO, folder, name)
    return q if os.path.exists(q) else None


def _img(path, colorspace='sRGB'):
    im = bpy.data.images.load(path, check_existing=True)
    im.colorspace_settings.name = colorspace
    return im


def _link(ob):
    bpy.context.collection.objects.link(ob)
    return ob


def _mesh_obj(name, verts, faces, edges=()):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], list(edges), [tuple(f) for f in faces])
    me.validate()
    me.update()
    return _link(bpy.data.objects.new(name, me))


def _empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.02
    e.location = loc
    return _link(e)


def _parent(children, parent):
    for c in children:
        if c is not None and c.parent is None and c is not parent:
            c.parent = parent


def _new_since(before):
    return [o for o in bpy.data.objects if o not in before]


def _finish(name, before, at=(0, 0, 0), rot_deg=0.0):
    """Parent everything created since `before` to a fresh root empty, then place the root."""
    new = _new_since(before)
    root = _empty(name)
    _parent(new, root)
    root.location = at
    root.rotation_euler = (0, 0, math.radians(rot_deg))
    return root


def _apply_modifiers(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def _boolean(ob, cutters, op='DIFFERENCE'):
    for i, c in enumerate(cutters):
        m = ob.modifiers.new('b%d' % i, 'BOOLEAN')
        m.operation = op
        m.solver = 'EXACT'
        m.object = c
    _apply_modifiers(ob)
    for c in cutters:
        bpy.data.objects.remove(c, do_unlink=True)
    return ob


def _smooth(ob, angle=30.0):
    for o in bpy.context.selected_objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle))
    ob.select_set(False)


def _bevel(ob, width_mm, segs=2, angle=40.0):
    b = ob.modifiers.new('bev', 'BEVEL')
    b.width = width_mm * MM
    b.segments = segs
    b.limit_method = 'ANGLE'
    b.angle_limit = math.radians(angle)
    return b


def _cuboid(name, x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from bounds in mm."""
    v = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    v = [(a * MM, b * MM, c * MM) for a, b, c in v]
    f = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    return _mesh_obj(name, v, f)


def _cylinder(name, cx, cy, r, z0, z1, segs=128):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r * MM, radius2=r * MM, depth=(z1 - z0) * MM)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx * MM, cy * MM, (z0 + z1) / 2 * MM))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _link(bpy.data.objects.new(name, me))


def _ellipsoid_bm(bm, center, radii, rot=None, segs=24, rings=14, power=1.0):
    """Add an ellipsoid (UV sphere) to a bmesh. center/radii in metres, rot a 3x3 Matrix. power < 1 squares it off
    into a superellipsoid (rounded box) on its local x and y axes, keeping the z (thickness) section round."""
    ret = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    R = rot if rot is not None else Matrix.Identity(3)
    for v in ret['verts']:
        x, y, z = v.co
        if power != 1.0:
            x = math.copysign(abs(x) ** power, x)
            y = math.copysign(abs(y) ** power, y)
        p = Vector((x * radii[0], y * radii[1], z * radii[2]))
        v.co = R @ p + Vector(center)
    return ret['verts']


# =============================================================================================== shader helpers
class _NT:
    """Terse node-tree builder."""
    def __init__(self, mat):
        self.nt = mat.node_tree

    def new(self, kind, **props):
        n = self.nt.nodes.new(kind)
        for k, v in props.items():
            setattr(n, k, v)
        return n

    def link(self, a, b):
        self.nt.links.new(a, b)

    def _in(self, sock, v):
        if v is None:
            return
        if isinstance(v, bpy.types.NodeSocket):
            self.link(v, sock)
        else:
            sock.default_value = v

    def m(self, op, a, b=None, c=None):
        n = self.new('ShaderNodeMath', operation=op)
        for i, v in enumerate((a, b, c)):
            self._in(n.inputs[i], v)
        return n.outputs[0]

    def v(self, op, a, b=None):
        n = self.new('ShaderNodeVectorMath', operation=op)
        self._in(n.inputs[0], a)
        self._in(n.inputs[1], b)
        return n.outputs['Value'] if op in ('LENGTH', 'DOT_PRODUCT', 'DISTANCE') else n.outputs['Vector']

    def sep(self, vec):
        n = self.new('ShaderNodeSeparateXYZ')
        self._in(n.inputs[0], vec)
        return n.outputs

    def comb(self, x, y, z):
        n = self.new('ShaderNodeCombineXYZ')
        for i, v in enumerate((x, y, z)):
            self._in(n.inputs[i], v)
        return n.outputs[0]

    def smooth(self, x, e0, e1):
        n = self.new('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP')
        self._in(n.inputs['Value'], x)
        n.inputs['From Min'].default_value = e0
        n.inputs['From Max'].default_value = e1
        return n.outputs['Result']

    def remap(self, x, a0, a1, b0, b1):
        n = self.new('ShaderNodeMapRange')
        self._in(n.inputs['Value'], x)
        n.inputs['From Min'].default_value = a0
        n.inputs['From Max'].default_value = a1
        n.inputs['To Min'].default_value = b0
        n.inputs['To Max'].default_value = b1
        return n.outputs['Result']

    def mix(self, fac, a, b):
        n = self.new('ShaderNodeMix', data_type='RGBA')
        self._in(n.inputs['Factor'], fac)
        self._in(n.inputs[6], a)
        self._in(n.inputs[7], b)
        return n.outputs[2]

    def mixf(self, fac, a, b):
        n = self.new('ShaderNodeMix', data_type='FLOAT')
        self._in(n.inputs['Factor'], fac)
        self._in(n.inputs[2], a)
        self._in(n.inputs[3], b)
        return n.outputs[0]

    def tex(self, path, vec=None, colorspace='sRGB', ext='CLIP', interp='Cubic'):
        n = self.new('ShaderNodeTexImage')
        n.image = _img(path, colorspace)
        n.extension = ext
        n.interpolation = interp
        if vec is not None:
            self.link(vec, n.inputs[0])
        return n

    def bump(self, height, distance_mm, strength=1.0, normal=None):
        n = self.new('ShaderNodeBump')
        self._in(n.inputs['Height'], height)
        n.inputs['Distance'].default_value = distance_mm * MM
        n.inputs['Strength'].default_value = strength
        if normal is not None:
            self.link(normal, n.inputs['Normal'])
        return n.outputs['Normal']


def _bsdf(m):
    return m.node_tree.nodes['Principled BSDF']


def _mat(name, **kw):
    return material(name, **kw)


# =============================================================================================== materials
FOIL_HEX = '#D9DBDD'


def case_material(name, atlas=None, foil=None, height=None, uv='UVMap', offset_mm=(0, 0, 0),
                  box=(65.0, 65.0, 0.0, 132.0), foil_mm=4.0, cap_mm=12.0, grain_mm=0.9, height_mm=0.29,
                  hide_rect=None, analytic_foil=None):
    """O CASE outer skin: black 120 g/m2 paper embossed with a tolex grain (0,2 mm, as bump) with the printed atlas.

    atlas   colour atlas (packaging team; the silver foil is drawn in it)        foil    foil mask atlas (white = foil)
    height  16-bit tolex height atlas, 0..1 (grain 0,15..0,85 = 0,2 mm, so height_mm = 0,29 mm per unit); without
            it a procedural Voronoi grain is used.
    analytic_foil  without a foil mask the foil is computed in 3D: a 4 mm band on the 12 edges of the CLOSED box and
            a 12 x 12 rounded flange at the 8 corners (defaults to True when foil is None).
    offset_mm  converts the object's coordinates to the closed-case frame (the lid rotates on its hinge).
    hide_rect  (x0, x1, z0, z1, dz, face_h) mm: inside this case-frame rectangle every channel is sampled dz mm lower on the
            same face (the base atlas shows the closed case, so the hasp tab is drawn on the base front; with a real
            tab this hides the drawing and keeps the grain continuous)."""
    if analytic_foil is None:
        analytic_foil = foil is None
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    tc = N.new('ShaderNodeTexCoord')
    p = N.v('ADD', N.v('MULTIPLY', tc.outputs['Object'], (1000.0, 1000.0, 1000.0)), offset_mm)   # mm, case frame
    uvs = None
    if atlas or foil or height:
        uvs = N.new('ShaderNodeUVMap', uv_map=uv).outputs['UV']
        if hide_rect:
            x0, x1, z0, z1, dz = hide_rect[:5]
            x, _, z = N.sep(p)
            inside = N.m('MULTIPLY', N.m('MULTIPLY', N.m('GREATER_THAN', x, x0), N.m('LESS_THAN', x, x1)),
                         N.m('MULTIPLY', N.m('GREATER_THAN', z, z0), N.m('LESS_THAN', z, z1)))
            dv = dz / hide_rect[5] / 3.0 if len(hide_rect) > 5 else dz / 102.0 / 3.0
            uvs = N.v('SUBTRACT', uvs, N.comb(0.0, N.m('MULTIPLY', inside, dv), 0.0))
    # --- grain height
    if height:
        th = N.tex(height, uvs, 'Non-Color')
        grain = N.m('ADD', th.outputs['Color'], 0.0)          # colour -> float
        hdist = height_mm
        rough_tolex = N.remap(grain, 0.15, 0.85, 0.80, 0.48)
    else:
        nz = N.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 0.35
        nz.inputs['Detail'].default_value = 2.0
        N.link(p, nz.inputs['Vector'])
        pd = N.v('ADD', p, N.v('MULTIPLY', N.v('SUBTRACT', nz.outputs['Color'], (0.5, 0.5, 0.5)), (1.6, 1.6, 1.6)))
        vo = N.new('ShaderNodeTexVoronoi', feature='SMOOTH_F1')
        vo.inputs['Scale'].default_value = 1.0 / grain_mm
        vo.inputs['Smoothness'].default_value = 0.6
        N.link(pd, vo.inputs['Vector'])
        peb = N.m('SUBTRACT', 1.0, N.m('MINIMUM', N.m('MULTIPLY', vo.outputs['Distance'], 1.6), 1.0))
        fine = N.new('ShaderNodeTexNoise')
        fine.inputs['Scale'].default_value = 1.0 / 0.18
        fine.inputs['Detail'].default_value = 3.0
        N.link(p, fine.inputs['Vector'])
        grain = N.m('ADD', N.m('MULTIPLY', peb, 0.7), N.m('MULTIPLY', fine.outputs['Fac'], 0.15))
        hdist = 0.2
        rough_tolex = N.remap(grain, 0.1, 0.85, 0.80, 0.48)
    # --- colour
    col = srgb(PRETO)
    if atlas:
        tx = N.tex(atlas, uvs)
        col = N.mix(tx.outputs['Alpha'], srgb(PRETO), tx.outputs['Color'])
    # --- foil
    fo = None
    if foil:
        fo = N.tex(foil, uvs, 'Non-Color').outputs['Color']
        fo = N.m('MINIMUM', N.m('MAXIMUM', fo, 0.0), 1.0)
    elif analytic_foil:
        x, y, z = N.sep(p)
        hx, hy, z0b, z1b = box
        hz, cz = (z1b - z0b) / 2, (z0b + z1b) / 2
        dx = N.m('SUBTRACT', hx, N.m('ABSOLUTE', x))
        dy = N.m('SUBTRACT', hy, N.m('ABSOLUTE', y))
        dzz = N.m('SUBTRACT', hz, N.m('ABSOLUTE', N.m('SUBTRACT', z, cz)))
        mn = N.m('MINIMUM', N.m('MINIMUM', dx, dy), dzz)
        mx = N.m('MAXIMUM', N.m('MAXIMUM', dx, dy), dzz)
        mid = N.m('SUBTRACT', N.m('SUBTRACT', N.m('ADD', N.m('ADD', dx, dy), dzz), mn), mx)
        surf = N.smooth(mn, 0.9, 0.5)
        edge = N.smooth(mid, foil_mm + 0.05, foil_mm - 0.05)
        cr = N.m('POWER', N.m('ADD', N.m('POWER', N.m('MAXIMUM', mid, 0.0), 4.0), N.m('POWER', N.m('MAXIMUM', mx, 0.0), 4.0)), 0.25)
        corner = N.smooth(cr, cap_mm + 0.06, cap_mm - 0.06)
        fo = N.m('MULTIPLY', N.m('MAXIMUM', edge, corner), surf)
        col = N.mix(fo, col, srgb(FOIL_HEX))
    if fo is not None:
        N.link(fo, bs.inputs['Metallic'])
        crink = N.new('ShaderNodeTexNoise')
        crink.inputs['Scale'].default_value = 1.0 / 0.6
        crink.inputs['Detail'].default_value = 4.0
        N.link(p, crink.inputs['Vector'])
        rough = N.mixf(fo, rough_tolex, N.remap(crink.outputs['Fac'], 0.3, 0.7, 0.20, 0.30))
        height_out = N.mixf(fo, grain, N.m('ADD', grain, N.m('MULTIPLY', crink.outputs['Fac'], 0.06)))
    else:
        rough = rough_tolex
        height_out = grain
    if isinstance(col, tuple):
        bs.inputs['Base Color'].default_value = col
    else:
        N.link(col, bs.inputs['Base Color'])
    N.link(rough, bs.inputs['Roughness'])
    bs.inputs['Specular IOR Level'].default_value = 0.5
    N.link(N.bump(height_out, hdist), bs.inputs['Normal'])
    return m


def mirror_print_material(name, atlas=None, espelho=None, uv='UVMap'):
    """The PMMA mirror (metallic 1,0, roughness 0,02). With the lid atlas and its mirror mask, whatever the mask
    leaves black inside the mirror ('olha a atração.') is printed ink on the mirror, in the atlas colour."""
    m = mirror_material(name)
    if not (atlas and espelho):
        return m
    N = _NT(m)
    bs = _bsdf(m)
    uvs = N.new('ShaderNodeUVMap', uv_map=uv).outputs['UV']
    mk = N.tex(espelho, uvs, 'Non-Color').outputs['Color']
    tx = N.tex(atlas, uvs)
    ink = N.m('SUBTRACT', 1.0, N.m('MINIMUM', N.m('MAXIMUM', mk, 0.0), 1.0))
    N.link(N.mix(ink, (0.90, 0.90, 0.89, 1), tx.outputs['Color']), bs.inputs['Base Color'])
    N.link(N.m('SUBTRACT', 1.0, ink), bs.inputs['Metallic'])
    N.link(N.mixf(ink, 0.02, 0.55), bs.inputs['Roughness'])
    return m


def tab_material(name, art_path=None):
    """The die-cut hasp tab: black tolex paper; its own RGBA art (die shape and slot in alpha) mapped on its front."""
    m = case_material(name, None, analytic_foil=False)
    if art_path:
        N = _NT(m)
        bs = _bsdf(m)
        tx = N.tex(art_path, N.new('ShaderNodeUVMap', uv_map='UVMap').outputs['UV'])
        N.link(N.mix(tx.outputs['Alpha'], srgb(PRETO), tx.outputs['Color']), bs.inputs['Base Color'])
    return m


def lining_material(name='lining'):
    """Black lining paper (inside walls, rims): matte, a faint fibre bump."""
    m = _mat(name, **{'Base Color': srgb('#0E0D10'), 'Roughness': 0.8, 'Specular IOR Level': 0.3})
    N = _NT(m)
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / (0.25 * MM)
    nz.inputs['Detail'].default_value = 4.0
    N.link(tc.outputs['Object'], nz.inputs['Vector'])
    N.link(N.bump(nz.outputs['Fac'], 0.03), _bsdf(m).inputs['Normal'])
    return m


def foil_material(name='foil'):
    m = _mat(name, **{'Base Color': srgb(FOIL_HEX), 'Metallic': 1.0, 'Roughness': 0.25})
    N = _NT(m)
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / (0.6 * MM)
    nz.inputs['Detail'].default_value = 4.0
    N.link(tc.outputs['Object'], nz.inputs['Vector'])
    N.link(N.bump(nz.outputs['Fac'], 0.04), _bsdf(m).inputs['Normal'])
    return m


def eva_material(name='eva'):
    """Black EVA foam, 30 kg/m3: roughness 0,8, closed-cell micro bump."""
    m = _mat(name, **{'Base Color': srgb('#18181B'), 'Roughness': 0.8, 'Specular IOR Level': 0.35})
    N = _NT(m)
    tc = N.new('ShaderNodeTexCoord')
    vo = N.new('ShaderNodeTexVoronoi', feature='F1')
    vo.inputs['Scale'].default_value = 1.0 / (0.35 * MM)
    N.link(tc.outputs['Object'], vo.inputs['Vector'])
    pit = N.m('POWER', N.m('MINIMUM', N.m('MULTIPLY', vo.outputs['Distance'], 1.8), 1.0), 0.5)
    N.link(N.bump(pit, 0.04), _bsdf(m).inputs['Normal'])
    N.link(N.remap(pit, 0.0, 1.0, 0.9, 0.74), _bsdf(m).inputs['Roughness'])
    return m


def mirror_material(name='mirror'):
    """O ESPELHO DE CAMARIM: 2 mm PMMA safety mirror, metallic 1,0, roughness 0,02."""
    return _mat(name, **{'Base Color': (0.90, 0.90, 0.89, 1), 'Metallic': 1.0, 'Roughness': 0.02})


def paper_material(name, art_path=None, base_hex=PAPEL, uv='UVMap', rough=0.82, back_art=None, back_hex=None,
                   mirror_back_u=False):
    """Uncoated card / paper with a fibre bump. When back_art/back_hex is given, back faces show the reverse."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Specular IOR Level'].default_value = 0.3
    uvn = N.new('ShaderNodeUVMap', uv_map=uv)
    col = srgb(base_hex)
    if art_path:
        tx = N.tex(art_path, uvn.outputs['UV'])
        col = N.mix(tx.outputs['Alpha'], srgb(base_hex), tx.outputs['Color'])
    if back_art or back_hex:
        geo = N.new('ShaderNodeNewGeometry')
        bcol = srgb(back_hex or base_hex)
        if back_art:
            vec = uvn.outputs['UV']
            if mirror_back_u:
                u, v, _ = N.sep(vec)
                vec = N.comb(N.m('SUBTRACT', 1.0, u), v, 0.0)
            tb = N.tex(back_art, vec)
            bcol = N.mix(tb.outputs['Alpha'], srgb(back_hex or base_hex), tb.outputs['Color'])
        col = N.mix(geo.outputs['Backfacing'], col, bcol)
    if isinstance(col, tuple):
        bs.inputs['Base Color'].default_value = col
    else:
        N.link(col, bs.inputs['Base Color'])
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / (0.3 * MM)
    nz.inputs['Detail'].default_value = 5.0
    N.link(tc.outputs['Object'], nz.inputs['Vector'])
    N.link(N.bump(nz.outputs['Fac'], 0.025), bs.inputs['Normal'])
    return m


def grey_material(name, hexcol, rough=0.85):
    """Previs mannequin: matte neutral grey."""
    return _mat(name, **{'Base Color': srgb(hexcol), 'Roughness': rough, 'Specular IOR Level': 0.25})


# =============================================================================================== atlas UV mapping
CELLS = {'top': (1, 2), 'bottom': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1),
         'c00': (0, 2), 'c20': (2, 2), 'c30': (3, 2)}


def _uv_atlas(ob, classify, offset_mm=(0, 0, 0)):
    """Per-polygon atlas UVs. classify(center_mm, normal) -> (cell, fn) where fn(co_mm) -> (a, b) in 0..1 inside
    the cell, or None (polygon gets material index 1 and no meaningful UV)."""
    me = ob.data
    while len(me.uv_layers):
        me.uv_layers.remove(me.uv_layers[0])
    uv = me.uv_layers.new(name='UVMap')
    off = Vector(offset_mm)
    for poly in me.polygons:
        c = poly.center / MM + off
        r = classify(c, poly.normal)
        if r is None:
            poly.material_index = 1
            for li in poly.loop_indices:
                uv.data[li].uv = (0.001, 0.001)
            continue
        cell, fn = r
        cx, cy = CELLS[cell]
        poly.material_index = 0
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co / MM + off
            a, b = fn(co)
            a = min(max(a, 0.0), 1.0)
            b = min(max(b, 0.0), 1.0)
            uv.data[li].uv = ((cx + a) / 4.0, (cy + b) / 3.0)


def _box_classifier(W, D, z0, z1, eps=0.6, inner_z=None, top=True):
    """Outer faces of an axis-aligned W x D box between z0 and z1 (mm, centred on x/y), box() orientation.
    inner_z maps the downward-facing interior panel at that height to the 'bottom' cell over the FULL W x D footprint
    (the packaging contract: the lid's inside is drawn on its 130 x 130 bottom cell, image top = front).
    top=False sends the top faces to the lining (an open tray's rim)."""
    hx, hy, Hh = W / 2, D / 2, z1 - z0

    def cls(c, n):
        if n.z > 0.9 and c.z > z1 - eps:
            return ('top', lambda v: (v.x / W + 0.5, v.y / D + 0.5)) if top else None
        if n.z < -0.9 and c.z < z0 + eps:
            return 'bottom', lambda v: (v.x / W + 0.5, 0.5 - v.y / D)
        if inner_z is not None and n.z < -0.9 and abs(c.z - inner_z) < eps and abs(c.x) < hx - 1.0 and abs(c.y) < hy - 1.0:
            return 'bottom', lambda v: (v.x / W + 0.5, 0.5 - v.y / D)
        if n.y < -0.9 and c.y < -hy + eps:
            return 'front', lambda v: (v.x / W + 0.5, (v.z - z0) / Hh)
        if n.y > 0.9 and c.y > hy - eps:
            return 'back', lambda v: (0.5 - v.x / W, (v.z - z0) / Hh)
        if n.x < -0.9 and c.x < -hx + eps:
            return 'left', lambda v: (0.5 - v.y / D, (v.z - z0) / Hh)
        if n.x > 0.9 and c.x > hx - eps:
            return 'right', lambda v: (v.y / D + 0.5, (v.z - z0) / Hh)
        return None
    return cls


# =============================================================================================== 1. O CASE
CASE = dict(W=130.0, D=130.0, HB=102.0, HL=30.0, T=2.0, MIRROR=100.0, MIRROR_T=2.0,
            BALL_P=1.7, BALL_D=2.6,                    # foil ball corner: protrusion past each face, centre inset
            FOAM_TOP=100.0, CUT=(0.0, -4.0, 92.0), CUT_DEPTH=86.0, SL_SLOT=(106.0, 3.0, 80.0), SL_Y=56.5,
            TAB=(52.0, 16.0, 3.0), TAB_X=0.0, TAB_T=0.8, TAB_UP=1.5,
            SLOT=(16.0, 3.0), SLOT_X=-13.0, SLOT_Z=94.0)


def case_contract(unit='HLF-CASE-02'):
    """The packaging team's O CASE files (02_PRODUTO/case/, generator _build/pack/case.py) for one unit, plus the
    geometry its json fixes (EVA cut-out and setlist slot, hasp tab and slot). Missing files -> placeholders and
    the analytic foil; missing json -> the CASE defaults (which mirror the 6 Oct contract)."""
    d = os.path.join(PRODUTO, 'case')

    def f(name):
        q = os.path.join(d, name)
        return q if os.path.exists(q) else None
    c = dict(base=f(unit + '_ATLAS_base.png'), tampa=f(unit + '_ATLAS_tampa.png'),
             base_foil=f('CASE_ATLAS_base_foil.png'), tampa_foil=f('CASE_ATLAS_tampa_foil.png'),
             base_height=f('CASE_ATLAS_base_altura16.png'), tampa_height=f('CASE_ATLAS_tampa_altura16.png'),
             espelho=f('CASE_ATLAS_tampa_espelho.png'), tab=f('CASE_ABA_hasp.png'), json=f(unit + '_case.json'))
    if c['base'] is None:
        c['base'] = ph('PH_CASE_BASE_atlas.png')
    if c['tampa'] is None:
        c['tampa'] = ph('PH_CASE_TAMPA_atlas.png')
    g = dict(CASE)
    if c['json']:
        import json
        try:
            j = json.load(open(c['json']))
            W = j['boxes']['base'][0]
            top = j['panels']['top'][0]
            cx, cy, cd = top['cutout_mm']
            g['CUT'] = (cx - W / 2, W / 2 - cy, cd)
            sx0, sy0, sl, sw = top['slot_mm']
            g['SL_SLOT'] = (sl, sw, CASE['SL_SLOT'][2])
            g['SL_Y'] = W / 2 - (sy0 + sw / 2)
            t = j['tab']
            g['TAB'] = (t['size_mm'][0], t['hangs_below_lid_front_mm'], t['corner_radius_mm'])
            g['TAB_X'] = t['x_mm_from_left'] + t['size_mm'][0] / 2 - W / 2
            g['SLOT'] = tuple(t['slot_mm']['size'])
            g['SLOT_X'] = t['slot_mm']['x_from_left'] + t['slot_mm']['size'][0] / 2 - W / 2
            g['SLOT_Z'] = CASE['HB'] - t['slot_mm']['centre_below_lid_edge']
        except Exception as e:                     # a half-written json: keep the defaults
            print('case_contract: json not read (%s); using defaults' % e)
    c['geom'] = g
    return c


def open_deg_for_camera(camera_elev_deg, ray_up_deg=30.0):
    """Lid opening angle at which a camera at this elevation sees the mirror reflect the space ABOVE the horizon
    (the dark ceiling and the work bulb), never the foam, the copo or the floor. A lid at angle a reflects a ray
    from elevation e to elevation (2a - 180 - e); setting that to ray_up_deg gives a = (e + 180 + ray_up)/2.
    At e = 70 deg the mirror only clears the pack above ~125 deg; 140 deg is the default for C05/L04."""
    return (camera_elev_deg + 180.0 + ray_up_deg) / 2.0


def _stadium(name, xc, zc, w, h, y0, y1, segs=12):
    """A slot cutter: a w x h rectangle with semicircular ends (x/z plane), extruded from y0 to y1 (mm)."""
    r = h / 2
    pts = []
    for i in range(segs + 1):
        a = -math.pi / 2 + math.pi * i / segs
        pts.append((xc + w / 2 - r + r * math.cos(a), zc + r * math.sin(a)))
    for i in range(segs + 1):
        a = math.pi / 2 + math.pi * i / segs
        pts.append((xc - w / 2 + r + r * math.cos(a), zc + r * math.sin(a)))
    bm = bmesh.new()
    vs = [bm.verts.new((x * MM, y0 * MM, z * MM)) for x, z in pts]
    fc = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[fc])
    for v in [g for g in ext['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.y = y1 * MM
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _link(bpy.data.objects.new(name, me))


def case(state='open', open_deg=100.0, unit='HLF-CASE-02', copo=None, setlist=True, setlist_kw=None,
         setlist_rise_mm=20.0, band=True, band_kw=None, at=(0, 0, 0), rot_deg=0.0, **art_override):
    """O CASE (§C.7): road case 130 x 130 x 132 = base tray 102 + lid 30 hinged at the back, 2 mm board wrapped in
    black tolex paper; silver hot-foil on the 12 closed-box edges + 8 ball corners (foil domes); a die-cut hasp tab
    hanging 16 mm below the lid front with ONE 16 x 3 slot aligned with a slot in the base front; magnets hidden.
    Inside the lid: the 100 x 100 PMMA mirror (metallic 1,0, roughness 0,02) in the printed bulb frame, with
    'olha a atração.' printed on the mirror where the mirror mask says so. Base: black EVA foam, Ø92 x 86 cut-out
    for the copo with its lid on, 3 mm setlist slot (positions from the packaging json).

    state  'open' | 'closed'        open_deg  lid angle from closed (100 = upright; for a camera at elevation e use
                                              open_deg_for_camera(e) so the mirror shows only the ceiling)
    unit   which personalised case atlas to use (HLF-CASE-0n...); art_override: base=, tampa=, base_foil=,
           tampa_foil=, base_height=, tampa_height=, espelho=, tab= (paths) replace single channels
    copo   None or a holofote.copo() spec (lid forced 'on'), placed in the cut-out
    setlist  the folded setlist standing in its slot, setlist_rise_mm above the foam (setlist_kw -> setlist())
    band   the wristband doubled through the hasp slot, clasp + paper seal on the floor in front
           (band_kw -> route 'drape'|'corner', art_path, seal_art, floor_turn_deg, tail_turn_deg, with_seal)
    Returns Built(root, base, lid, lid_pivot, tab, mirror, foam, copo, setlist, band, contract)."""
    K = case_contract(unit)
    K.update({k: v for k, v in art_override.items() if v})
    C = K['geom']
    before = set(bpy.data.objects)
    W, D, T, HB, HL = C['W'], C['D'], C['T'], C['HB'], C['HL']
    hx, hy = W / 2, D / 2
    hinge = Vector((0.0, hy, HB))
    tw, th, tr = C['TAB']
    sw, sh = C['SLOT']

    # ---- base tray (open top), with the hasp slot through the front wall
    base = _cuboid('case_base', -hx, hx, -hy, hy, 0, HB)
    _boolean(base, [_cuboid('cut', -hx + T, hx - T, -hy + T, hy - T, T, HB + 5),
                    _stadium('slot', C['SLOT_X'], C['SLOT_Z'], sw, sh, -hy - 1, -hy + T + 1)])
    _smooth(base, 35)
    _bevel(base, 0.5)
    hide = (C['TAB_X'] - tw / 2 - 0.6, C['TAB_X'] + tw / 2 + 0.6, HB - th - 0.6, HB + 1, 18.0, HB)
    base.data.materials.append(case_material('case_base', K['base'], K['base_foil'], K['base_height'], hide_rect=hide))
    base.data.materials.append(lining_material('case_lining'))
    _uv_atlas(base, _box_classifier(W, D, 0.0, HB, top=False))

    # ---- EVA foam: cut-out for the copo with its lid on, the setlist slot
    cx, cy, cd = C['CUT']
    slen, swid, sdep = C['SL_SLOT']
    foam = _cuboid('case_foam', -hx + T + 0.15, hx - T - 0.15, -hy + T + 0.15, hy - T - 0.15, T, C['FOAM_TOP'])
    _boolean(foam, [_cylinder('cut', cx, cy, cd / 2, C['FOAM_TOP'] - C['CUT_DEPTH'], C['FOAM_TOP'] + 5, 160),
                    _cuboid('cut', -slen / 2, slen / 2, C['SL_Y'] - swid / 2, C['SL_Y'] + swid / 2,
                            C['FOAM_TOP'] - sdep, C['FOAM_TOP'] + 5)])
    _smooth(foam, 30)
    _bevel(foam, 0.6, 2, 50)
    foam.data.materials.append(eva_material())

    # ---- lid (built closed, re-based on the hinge)
    lid = _cuboid('case_lid', -hx, hx, -hy, hy, HB, HB + HL)
    _boolean(lid, [_cuboid('cut', -hx + T, hx - T, -hy + T, hy - T, HB - 5, HB + HL - T)])
    _smooth(lid, 35)
    _bevel(lid, 0.5)
    lid.data.materials.append(case_material('case_lid', K['tampa'], K['tampa_foil'], K['tampa_height'],
                                            offset_mm=tuple(hinge)))
    lid.data.materials.append(lining_material('case_lid_lining'))
    _uv_atlas(lid, _box_classifier(W, D, HB, HB + HL, inner_z=HB + HL - T))

    # ---- hasp tab: 0,8 mm die-cut plate hanging th mm below the lid front edge (its top TAB_UP mm lapped onto the
    # lid face), lower corners rounded, one slot aligned with the base slot. Its art covers the hanging th mm.
    tab = _tab_object(C)
    tab.data.materials.append(tab_material('case_tab', K['tab']))
    tab.data.materials.append(lining_material('case_tab_edge'))
    tx0 = C['TAB_X'] - tw / 2

    def tab_cls(c, n):
        if n.y < -0.9:
            return 'c00', lambda v: ((v.x - tx0) / tw, (v.z - (HB - th)) / th)
        return None
    _uv_atlas(tab, tab_cls)
    me = tab.data                          # the tab art is its own image: map 'c00' back to the full 0..1 square
    for lp in me.uv_layers['UVMap'].data:
        u, v = lp.uv
        lp.uv = (u * 4.0, (v - 2.0 / 3.0) * 3.0)

    # ---- mirror: 100 x 100 x 2, reflective face 0,1 mm proud of the interior panel, UVs in the lid atlas
    mz = HB + HL - T - 0.1
    hm = C['MIRROR'] / 2
    mirror = _cuboid('case_mirror', -hm, hm, -hm, hm, mz, mz + C['MIRROR_T'])
    _uv_atlas(mirror, _box_classifier(W, D, mz, mz + C['MIRROR_T'], eps=0.05))
    _bevel(mirror, 0.3, 2)
    mirror.data.materials.append(mirror_print_material('case_mirror', K['tampa'], K['espelho']))
    mirror.data.materials.append(_mat('pmma_edge', **{'Base Color': srgb('#3A3D3E'), 'Roughness': 0.1}))

    # ---- ball corners: foil domes over each closed-box corner
    p, dd = C['BALL_P'], C['BALL_D']
    rr = dd + p
    balls_hi = []
    for zc in (0.0, HB + HL):
        for sxn in (-1, 1):
            for syn in (-1, 1):
                bm = bmesh.new()
                _ellipsoid_bm(bm, (sxn * (hx - dd) * MM, syn * (hy - dd) * MM, (zc + (dd if zc == 0 else -dd)) * MM),
                              (rr * MM,) * 3, segs=32, rings=16)
                mb = bpy.data.meshes.new('ball')
                bm.to_mesh(mb)
                bm.free()
                ob = _link(bpy.data.objects.new('case_ball', mb))
                mb.polygons.foreach_set('use_smooth', [True] * len(mb.polygons))
                ob.data.materials.append(foil_material())
                if zc > 0:
                    balls_hi.append(ob)

    # ---- pivot
    pivot = _empty('case_lid_pivot', hinge * MM)
    for ob in [lid, tab, mirror] + balls_hi:
        ob.data.transform(Matrix.Translation(-hinge * MM))
        ob.parent = pivot
    ang = 0.0 if state == 'closed' else open_deg
    pivot.rotation_euler = (-math.radians(ang), 0, 0)

    # ---- contents
    copo_root = None
    if copo is not None:
        spec = dict(copo)
        spec['lid'] = 'on'
        copo_root = H.copo(spec, at=(cx * MM, cy * MM, (C['FOAM_TOP'] - C['CUT_DEPTH']) * MM))
    sl = None
    if setlist and state == 'open':
        kw = dict(setlist_kw or {})
        kw.setdefault('state', 'folded')
        sl = _setlist_fn(**kw)
        z_bottom = C['FOAM_TOP'] - sdep
        sl.root.location = (0.0, C['SL_Y'] * MM, max(z_bottom, C['FOAM_TOP'] + setlist_rise_mm - 100.0) * MM)
    bd = None
    if band:
        bd = _band_through_case(C, closed=(state == 'closed'), **(band_kw or {}))
    root = _finish('case_root', before, at, rot_deg)
    return Built(root=root, base=base, lid=lid, lid_pivot=pivot, tab=tab, mirror=mirror, foam=foam, copo=copo_root,
                 setlist=sl, band=bd, state=state, open_deg=ang, contract=K)


def _tab_object(C):
    """The hasp tab plate (mm, case frame, closed): rounded lower corners, slot cut through."""
    tw, th, r = C['TAB']
    t, up = C['TAB_T'], C['TAB_UP']
    x0, x1 = C['TAB_X'] - tw / 2, C['TAB_X'] + tw / 2
    z0, z1 = C['HB'] - th, C['HB'] + up
    y1 = -C['D'] / 2 - 0.02
    y0 = y1 - t
    pts = [(x0, z1), (x1, z1)]
    for i in range(9):
        a = i / 8 * (math.pi / 2)
        pts.append((x1 - r + r * math.cos(a), z0 + r - r * math.sin(a)))
    for i in range(9):
        a = math.pi / 2 + i / 8 * (math.pi / 2)
        pts.append((x0 + r + r * math.cos(a), z0 + r - r * math.sin(a)))
    bm = bmesh.new()
    vf = [bm.verts.new((x * MM, y0 * MM, z * MM)) for x, z in pts]
    face = bm.faces.new(vf)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    for v in [g for g in ext['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.y = y1 * MM
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('tab')
    bm.to_mesh(me)
    bm.free()
    ob = _link(bpy.data.objects.new('case_tab', me))
    _boolean(ob, [_stadium('slot', C['SLOT_X'], C['SLOT_Z'], C['SLOT'][0], C['SLOT'][1], y0 - 1, y1 + 1)])
    _smooth(ob, 35)
    _bevel(ob, 0.2, 2)
    return ob


def mirror_frame(built):
    """World-space centre and normal of the case mirror."""
    mw = built.mirror.matrix_world
    me = built.mirror.data
    xs, ys, zs = ([v.co[i] for v in me.vertices] for i in range(3))
    zf = min(zs)                       # reflective face (local, faces -Z in the closed lid)
    centre = mw @ Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, zf))
    normal = (mw.to_3x3() @ Vector((0, 0, -1))).normalized()
    return centre, normal


def mirror_reflection(built, cam_loc):
    """Unit direction the mirror shows to a camera at cam_loc (the reflected view ray through the mirror centre)."""
    c, n = mirror_frame(built)
    d = (c - Vector(cam_loc)).normalized()
    return (d - 2 * d.dot(n) * n).normalized()


def work_bulb(at=(0, 0, 0), lit=True, light_w=0.0, cord_mm=600.0, filament=300.0):
    """A bare incandescent work-light bulb (A60, E27, clear glass, hanging on a black cord) for the case mirror to
    reflect (C05). The filament glows (~2.700 K); light_w > 0 adds a point light so it also lights the set.
    Built hanging: base up, glass down. filament = emission strength. Returns Built(root, light, filament)."""
    before = set(bpy.data.objects)
    prof = [(0.0, 0.0), (8.0, -0.6), (14.0, -3.0), (14.2, -8.0), (17.5, -20.0), (24.5, -33.0), (29.0, -45.0),
            (30.0, -55.0), (28.8, -65.0), (24.5, -74.5), (17.0, -81.0), (9.0, -84.3), (0.0, -85.2)]
    glass = H.lathe('bulb_glass', prof, segs=96, smooth_angle=60)
    glass.data.materials.append(_mat('bulb_glass', **{'Base Color': (1, 1, 1, 1), 'Roughness': 0.04, 'IOR': 1.5,
                                                       'Transmission Weight': 1.0}))
    capp = [(0.0, 26.0), (13.6, 26.0)] + [(13.6 if i % 2 == 0 else 12.6, 24.0 - i * 2.4) for i in range(10)] + [(13.0, 0.0), (0.0, 0.0)]
    cap = H.lathe('bulb_cap', capp, segs=64, smooth_angle=20)
    cap.data.materials.append(_mat('bulb_cap', **{'Base Color': srgb('#B9B6AE'), 'Metallic': 1.0, 'Roughness': 0.35}))
    # filament: a short coiled arc between two support wires, emissive
    bm = bmesh.new()
    pts = []
    for i in range(41):
        a = math.radians(-60 + 120 * i / 40)
        pts.append(Vector((9.0 * math.sin(a), 0.0, -48.0 + 3.0 * math.cos(a))) * MM)
    for i, p in enumerate(pts[:-1]):
        q = pts[i + 1]
        mid = (p + q) / 2
        d = (q - p)
        r = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45 * MM, radius2=0.45 * MM, depth=d.length * 1.05)
        rot = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        bmesh.ops.transform(bm, matrix=Matrix.Translation(mid) @ rot, verts=r['verts'])
    for sx in (-1, 1):
        a, b = Vector((sx * 2.0, 0, -6.0)) * MM, pts[0 if sx < 0 else -1]
        d = b - a
        r = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.25 * MM, radius2=0.25 * MM, depth=d.length)
        bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4(),
                            verts=r['verts'])
    me = bpy.data.meshes.new('filament')
    bm.to_mesh(me)
    bm.free()
    fil = _link(bpy.data.objects.new('bulb_filament', me))
    em = bpy.data.materials.new('filament')
    em.use_nodes = True
    nt = em.node_tree
    nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial')
    e = nt.nodes.new('ShaderNodeEmission')
    bb = nt.nodes.new('ShaderNodeBlackbody')
    bb.inputs[0].default_value = 2700
    nt.links.new(bb.outputs[0], e.inputs[0])
    e.inputs[1].default_value = filament if lit else 0.0
    nt.links.new(e.outputs[0], o.inputs[0])
    fil.data.materials.append(em)
    cord = _cylinder('bulb_cord', 0, 0, 2.6, 26.0, 26.0 + cord_mm, 16)
    cord.data.materials.append(_mat('cord', **{'Base Color': srgb('#0B0B0C'), 'Roughness': 0.5}))
    L = None
    if light_w > 0:
        bpy.ops.object.light_add(type='POINT', location=(0, 0, -48.0 * MM))
        L = bpy.context.object
        L.data.energy = light_w
        L.data.shadow_soft_size = 10 * MM
        L.data.color = (1.0, 0.72, 0.45)
    root = _finish('work_bulb_root', before, at)
    return Built(root=root, light=L, filament=fil)


def place_work_bulb(built_case, cam, dist=1.4, **kw):
    """Hang a work bulb exactly where the case mirror looks for this camera (camera object or location), so the
    mirror shows the dark ceiling plus one bare bulb. Returns the work_bulb Built."""
    cam_loc = cam.matrix_world.translation if hasattr(cam, 'matrix_world') else Vector(cam)
    c, _ = mirror_frame(built_case)
    r = mirror_reflection(built_case, cam_loc)
    if r.z < 0.05:
        print('WARNING: at this lid angle the mirror looks DOWN (r.z = %.2f): it will show the pack/floor. '
              'Use open_deg_for_camera().' % r.z)
    return work_bulb(at=c + r * dist, **kw)


# =============================================================================================== 2. O INGRESSO carton
INGRESSO = dict(W=96.0, D=96.0, H=98.0)


def ingresso(atlas_path=None, faixa='02', sku=None, size=None, at=(0, 0, 0), rot_deg=0.0, bulge_mm=0.35):
    """Carton O INGRESSO (§C.9), 96 x 96 x 98 tuck-end, SBS 400 g/m2. 4 x 3 atlas per candle_lib.box() (packaging
    team, 02_PRODUTO/cartucho/<sku>_CARTUCHO_ATLAS.png, sku defaults to HLF-<faixa>-200; cells may be non-square,
    the grid only has to be uniform). The panels bow out bulge_mm, the folded edges are rounded, the top tuck flap shows
    its slit along the front and both sides, and the ink cracks faintly white on the folds.
    size=(w, d, h) re-sets the carton (O INGRESSO SINGLE 74 x 74 x 76, NOVA TEMPORADA carton 74 x 74 x 82)."""
    W, D, Hh = size or (INGRESSO['W'], INGRESSO['D'], INGRESSO['H'])
    if not atlas_path:
        q = os.path.join(PRODUTO, 'cartucho', '%s_CARTUCHO_ATLAS.png' % (sku or 'HLF-%s-200' % faixa))
        atlas_path = q if os.path.exists(q) else ph('PH_INGRESSO_atlas.png')
    before = set(bpy.data.objects)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=15, use_grid_fill=True)
    hx, hy, hz = W / 2, D / 2, Hh / 2
    for v in bm.verts:
        x, y, z = v.co
        X, Y, Z = x * 2, y * 2, z * 2                                   # -1..1
        nx, ny, nz = x * W, y * D, z * Hh + hz
        # outward bow of each panel, zero at the edges
        bx = bulge_mm * (1 - Y * Y) * (1 - Z * Z) * (1 if X > 0 else -1) if abs(X) > 0.999 else 0.0
        by = bulge_mm * (1 - X * X) * (1 - Z * Z) * (1 if Y > 0 else -1) if abs(Y) > 0.999 else 0.0
        bz = 0.6 * bulge_mm * (1 - X * X) * (1 - Y * Y) if Z > 0.999 else 0.0
        v.co = Vector((nx + bx, ny + by, nz + bz)) * MM
    me = bpy.data.meshes.new('ingresso')
    bm.to_mesh(me)
    bm.free()
    ob = _link(bpy.data.objects.new('ingresso', me))
    # tuck slit: a 0,3 mm groove 0,7 mm below the top edge on the front and both sides
    g, gd = 0.3, 0.45
    zt = Hh - 0.7
    cut = [_cuboid('slit', -hx - 1, hx + 1, -hy - 1, -hy + gd, zt - g / 2, zt + g / 2),
           _cuboid('slit', -hx - 1, -hx + gd, -hy - 1, hy - 3, zt - g / 2, zt + g / 2),
           _cuboid('slit', hx - gd, hx + 1, -hy - 1, hy - 3, zt - g / 2, zt + g / 2)]
    _boolean(ob, cut)
    _smooth(ob, 30)
    _bevel(ob, 0.4, 3, 30)
    m = bpy.data.materials.new('ingresso')
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    uvn = N.new('ShaderNodeUVMap', uv_map='UVMap')
    tx = N.tex(atlas_path, uvn.outputs['UV'])
    col = N.mix(tx.outputs['Alpha'], srgb('#F4F2EE'), tx.outputs['Color'])
    tc = N.new('ShaderNodeTexCoord')
    pm = N.v('MULTIPLY', tc.outputs['Object'], (1000.0, 1000.0, 1000.0))
    x, y, z = N.sep(pm)
    dx = N.m('SUBTRACT', hx, N.m('ABSOLUTE', x))
    dy = N.m('SUBTRACT', hy, N.m('ABSOLUTE', y))
    dz = N.m('SUBTRACT', hz, N.m('ABSOLUTE', N.m('SUBTRACT', z, hz)))
    mn = N.m('MINIMUM', N.m('MINIMUM', dx, dy), dz)
    mx = N.m('MAXIMUM', N.m('MAXIMUM', dx, dy), dz)
    mid = N.m('SUBTRACT', N.m('SUBTRACT', N.m('ADD', N.m('ADD', dx, dy), dz), mn), mx)
    crack_n = N.new('ShaderNodeTexNoise')
    crack_n.inputs['Scale'].default_value = 1.0 / 0.25
    crack_n.inputs['Detail'].default_value = 6.0
    N.link(pm, crack_n.inputs['Vector'])
    crack = N.m('MULTIPLY', N.smooth(mid, 0.35, 0.05), N.smooth(crack_n.outputs['Fac'], 0.5, 0.62))
    col = N.mix(N.m('MULTIPLY', crack, 0.55), col, srgb('#FBFAF7'))
    N.link(col, bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.42
    bs.inputs['Specular IOR Level'].default_value = 0.4
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / 0.35
    nz.inputs['Detail'].default_value = 5.0
    N.link(pm, nz.inputs['Vector'])
    N.link(N.bump(nz.outputs['Fac'], 0.015), bs.inputs['Normal'])
    ob.data.materials.append(m)
    _uv_atlas(ob, _box_classifier_loose(W, D, 0.0, Hh))
    root = _finish('ingresso_root', before, at, rot_deg)
    return Built(root=root, box=ob, size=(W, D, Hh))


def _box_classifier_loose(W, D, z0, z1):
    """Like _box_classifier but by dominant normal only (the panels bow), never returning None."""
    Hh = z1 - z0

    def cls(c, n):
        a = max((abs(n.x), 'x'), (abs(n.y), 'y'), (abs(n.z), 'z'))[1]
        if a == 'z':
            if n.z > 0:
                return 'top', lambda v: (v.x / W + 0.5, v.y / D + 0.5)
            return 'bottom', lambda v: (v.x / W + 0.5, 0.5 - v.y / D)
        if a == 'y':
            if n.y < 0:
                return 'front', lambda v: (v.x / W + 0.5, (v.z - z0) / Hh)
            return 'back', lambda v: (0.5 - v.x / W, (v.z - z0) / Hh)
        if n.x < 0:
            return 'left', lambda v: (0.5 - v.y / D, (v.z - z0) / Hh)
        return 'right', lambda v: (v.y / D + 0.5, (v.z - z0) / Hh)
    return cls


# =============================================================================================== ribbons (band, tape)
class Turtle:
    """Frame-tracking path builder for strips (mm). t = tangent, n = the face normal of side 1; b = t x n."""
    def __init__(self, p, t, n, step=0.7):
        self.p, self.t, self.n = Vector(p), Vector(t).normalized(), Vector(n).normalized()
        self.s, self.step = 0.0, step
        self.samples = [(self.p.copy(), self.t.copy(), self.n.copy(), 0.0)]
        self.marks = {}

    def _push(self):
        self.samples.append((self.p.copy(), self.t.copy(), self.n.copy(), self.s))

    def mark(self, name):
        self.marks[name] = (self.p.copy(), self.t.copy(), self.n.copy(), self.s)
        return self

    def fwd(self, L):
        if L <= 1e-6:
            return self
        k = max(1, int(math.ceil(L / self.step)))
        for _ in range(k):
            self.p += self.t * (L / k)
            self.s += L / k
            self._push()
        return self

    def fwd_to(self, axis, value):
        i = 'xyz'.index(axis)
        return self.fwd((value - self.p[i]) / self.t[i])

    def bend(self, deg, r):
        """Curl about the strip's width axis; deg > 0 turns the tangent toward +n."""
        if abs(deg) < 1e-6:
            return self
        sg = 1.0 if deg > 0 else -1.0
        b = self.t.cross(self.n)
        c = self.p + self.n * (r * sg)
        k = max(2, int(abs(deg) / 4))
        R = Matrix.Rotation(math.radians(deg) / k, 3, b)
        for _ in range(k):
            self.t = (R @ self.t).normalized()
            self.n = (R @ self.n).normalized()
            self.p = c - self.n * (r * sg)
            self.s += r * abs(math.radians(deg)) / k
            self._push()
        return self

    def bend_to(self, direction, r):
        d = Vector(direction).normalized()
        ang = math.degrees(self.t.angle(d))
        return self.bend(ang if d.dot(self.n) > 0 else -ang, r)

    def turn(self, deg, r):
        """In-plane turn about n; deg > 0 turns toward n x t."""
        if abs(deg) < 1e-6:
            return self
        sg = 1.0 if deg > 0 else -1.0
        side = self.n.cross(self.t)
        c = self.p + side * (r * sg)
        k = max(2, int(abs(deg) / 4))
        R = Matrix.Rotation(math.radians(deg) / k, 3, self.n)
        for _ in range(k):
            self.t = (R @ self.t).normalized()
            self.p = c - self.n.cross(self.t) * (r * sg)
            self.s += r * abs(math.radians(deg)) / k
            self._push()
        return self

    def twist(self, deg, L):
        k = max(2, int(math.ceil(L / self.step)))
        R = Matrix.Rotation(math.radians(deg) / k, 3, self.t)
        for _ in range(k):
            self.n = (R @ self.n).normalized()
            self.p += self.t * (L / k)
            self.s += L / k
            self._push()
        return self

    def to_length(self, total, ops):
        """Run (op, *args) steps but stop exactly when the arc length reaches `total`."""
        for op in ops:
            if self.s >= total - 1e-6:
                break
            getattr(self, op[0])(*op[1:])
        # trim samples past `total`
        out = []
        for smp in self.samples:
            if smp[3] <= total + 1e-6:
                out.append(smp)
            else:
                p0, t0, n0, s0 = out[-1]
                p1, t1, n1, s1 = smp
                f = (total - s0) / max(1e-9, s1 - s0)
                out.append((p0.lerp(p1, f), t0.lerp(t1, f).normalized(), n0.lerp(n1, f).normalized(), total))
                break
        self.samples = out
        return self


def _strip_mesh(name, samples, width, total=None):
    """A strip of `width` mm along turtle samples. UV u = s/total (along), v = 1 on the -b edge (the art's top when
    side 1 is seen with the strip running left to right), 0 on the +b edge. Face normal = n (side 1)."""
    total = total or samples[-1][3]
    verts, faces, uvs = [], [], []
    for p, t, n, s in samples:
        b = t.cross(n).normalized()
        verts.append((p - b * (width / 2)) * MM)
        verts.append((p + b * (width / 2)) * MM)
        uvs.append(((s / total, 1.0), (s / total, 0.0)))
    for i in range(len(samples) - 1):
        a, bq = 2 * i, 2 * i + 1
        faces.append((a, bq, bq + 2, a + 2))
    ob = _mesh_obj(name, verts, faces)
    uv = ob.data.uv_layers.new(name='UVMap')
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            vi = ob.data.loops[li].vertex_index
            uv.data[li].uv = uvs[vi // 2][vi % 2]
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    return ob


# =============================================================================================== 5. A PULSEIRA
BAND = dict(L=350.0, W=15.0, T=1.0)


def jacquard_material(name, art_path, length_mm=350.0, width_mm=15.0, reverse=False, height=None):
    """Woven polyester band: side 1 is the art (amarelo jacquard text on black); side 2 is the woven reverse, the
    same weave seen from the back: mirrored (UVs are shared) and a little duller."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    uvn = N.new('ShaderNodeUVMap', uv_map='UVMap')
    tx = N.tex(art_path, uvn.outputs['UV'], ext='EXTEND')
    if reverse:
        hsv = N.new('ShaderNodeHueSaturation')
        hsv.inputs['Saturation'].default_value = 0.75
        hsv.inputs['Value'].default_value = 0.7
        N.link(tx.outputs['Color'], hsv.inputs['Color'])
        N.link(hsv.outputs['Color'], bs.inputs['Base Color'])
    else:
        N.link(tx.outputs['Color'], bs.inputs['Base Color'])
    if height:                      # the packaging team's woven height map (warp 0,20 / weft 0,25 mm)
        h = N.m('ADD', N.tex(height, uvn.outputs['UV'], 'Non-Color', ext='EXTEND').outputs['Color'], 0.0)
        N.link(N.bump(h, 0.06), bs.inputs['Normal'])
    else:                           # procedural weave: fine warp ribs along the band, a slower weft beat across
        u, v, _ = N.sep(uvn.outputs['UV'])
        um, vm = N.m('MULTIPLY', u, length_mm), N.m('MULTIPLY', v, width_mm)
        rib = N.m('SINE', N.m('MULTIPLY', vm, 2 * math.pi / 0.32))
        beat = N.m('SINE', N.m('MULTIPLY', um, 2 * math.pi / 0.55))
        h = N.m('ADD', N.m('MULTIPLY', rib, 0.6), N.m('MULTIPLY', N.m('MULTIPLY', rib, beat), 0.4))
        N.link(N.bump(h, 0.04), bs.inputs['Normal'])
    bs.inputs['Roughness'].default_value = 0.62
    bs.inputs['Sheen Weight'].default_value = 0.22
    bs.inputs['Sheen Roughness'].default_value = 0.4
    bs.inputs['Specular IOR Level'].default_value = 0.35
    return m


def band_art():
    """The wristband's art: (colour, height) from 02_PRODUTO/pulseira/ (PULSEIRA_tecido.png: x along the band from
    the clasp end, y across, black ground, amarelo jacquard; PULSEIRA_tecido_altura16.png), else the placeholder."""
    return (pfile('pulseira', 'PULSEIRA_tecido.png') or ph('PH_PULSEIRA_jacquard.png'),
            pfile('pulseira', 'PULSEIRA_tecido_altura16.png'))


def _band_object(samples, art_path, length, height=None):
    ob = _strip_mesh('pulseira', samples, BAND['W'], total=length)
    s = ob.modifiers.new('sol', 'SOLIDIFY')
    s.thickness = BAND['T'] * MM
    s.offset = 0.0
    s.use_even_offset = True
    s.use_quality_normals = True
    ob.data.materials.append(jacquard_material('pulseira', art_path, length, BAND['W'], height=height))
    ob.data.materials.append(jacquard_material('pulseira_verso', art_path, length, BAND['W'], reverse=True, height=height))
    ob.data.materials.append(_mat('pulseira_edge', **{'Base Color': srgb('#141316'), 'Roughness': 0.75}))
    s.material_offset = 1
    s.material_offset_rim = 2
    return ob


def clasp(p, t, up, length=20.0, width=19.0, height=5.6, z_under=0.8):
    """Black one-way slide clasp (festival-band bead), centred on p (mm) with the band running along t and the
    stacked band layers on its underside+z_under. Returns the object."""
    t, up = Vector(t).normalized(), Vector(up).normalized()
    b = t.cross(up).normalized()
    ob = _cuboid('clasp', -length / 2, length / 2, -width / 2, width / 2, -z_under, height - z_under)
    ch = _cuboid('ch', -length, length, -(BAND['W'] + 1.0) / 2, (BAND['W'] + 1.0) / 2, -0.05, 2.25)
    _boolean(ob, [ch])
    _bevel(ob, 1.4, 4, 60)
    _smooth(ob, 40)
    M = Matrix((t, b, up)).transposed().to_4x4()
    M.translation = Vector(p) * MM
    ob.matrix_world = M
    m = _mat('clasp', **{'Base Color': srgb('#0D0D0F'), 'Roughness': 0.32, 'Specular IOR Level': 0.5})
    N = _NT(m)
    tc = N.new('ShaderNodeTexCoord')
    x, y, z = N.sep(tc.outputs['Object'])
    ribs = N.m('MULTIPLY', N.m('SINE', N.m('MULTIPLY', x, 2 * math.pi / (1.6 * MM))), N.smooth(z, (height - z_under - 0.6) * MM, (height - z_under - 0.2) * MM))
    N.link(N.bump(ribs, 0.12), _bsdf(m).inputs['Normal'])
    ob.data.materials.append(m)
    return ob


SEAL = dict(size=(60.0, 15.0), stack=(16.0, 2.5),
            panels=dict(left=(23.0, 25.5), top=(25.5, 41.5), right=(41.5, 44.0), bottom=(44.0, 60.0)))


def seal_contract():
    """The packaging team's seal: one strip PULSEIRA_SELO_faixa.png (60 x 15 mm, 20 px/mm, x = s along the strip,
    y = across = along the band, printed OUTSIDE only) and its panel layout from PULSEIRA.json -> seal."""
    c = dict(SEAL)
    c['art'] = pfile('pulseira', 'PULSEIRA_SELO_faixa.png') or ph('PH_SELO_faixa.png')
    j = pfile('pulseira', 'PULSEIRA.json')
    if j:
        import json
        try:
            S = json.load(open(j))['seal']
            c['size'] = tuple(S['size_mm'])
            c['stack'] = tuple(S['stack_mm'])
            P = {p['name']: tuple(p['s_mm']) for p in S['panels']}
            c['panels'] = dict(left=P['lado-esquerdo'], top=P['TOPO'], right=P['lado-direito'], bottom=P['BAIXO'])
        except Exception as e:
            print('seal_contract: json not read (%s); using defaults' % e)
    return c


def seal(p, t, up, read_up=(0, 1, 0), art_path=None, stack_mm=None, length=None, paper=0.25):
    """The paper seal (§C.6, packaging redesign of 6 Oct): uncoated papel-cartaz wrapped round the stacked band and
    tail at p (mm, the centre of the stack's underside, t along the band, `up` the outward face). The strip is
    printed on the outside only; its panels land on the faces they were drawn for: left side, TOPO ("pode /
    rasgar."), right side, BAIXO ("o que se guarda é a pulseira."); the inner glue wrap (s 0-23) is hidden.
    On TOPO s increases toward read_up, so the letters' tops point toward the higher end of the strip and the text
    reads upright for a camera that has read_up as its screen-up (default +Y: a front camera at -Y). The text lines
    run ALONG the band, so the band must run across the frame at the seal for them to read upright.
    art_path overrides the strip; stack_mm (default the json's 2,5) and length (15) set the wrap."""
    C = seal_contract()
    art_path = art_path or C['art']
    stack_mm = stack_mm or C['stack'][1]
    length = length or C['size'][1]
    up = Vector(up).normalized()
    t = Vector(t).normalized()
    if t.cross(up).dot(Vector(read_up)) < 0:
        t = -t                                     # choose the wrap sense: +b (= t x up) is screen-up
    b = t.cross(up).normalized()
    w = C['stack'][0] / 2 + 0.05                   # 16 mm stack (+ paper slack)
    z0, z1 = -0.08, stack_mm + 0.08
    rc = 0.55
    # rounded rectangle in the (b, up) plane, built panel by panel in strip order: left side (going up), top
    # (-b -> +b), right side (going down), bottom (+b -> -b); each panel runs between corner mid-points
    def arc(cx, cz, a0, a1, n=4):
        return [(cx + rc * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cz + rc * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    BL, TL, TR, BR = (-w + rc, z0 + rc), (-w + rc, z1 - rc), (w - rc, z1 - rc), (w - rc, z0 + rc)
    segs = {
        'left': arc(*BL, 225, 180) + [(-w, z0 + rc), (-w, z1 - rc)] + arc(*TL, 180, 135),
        'top': arc(*TL, 135, 90) + [(-w + rc, z1), (w - rc, z1)] + arc(*TR, 90, 45),
        'right': arc(*TR, 45, 0) + [(w, z1 - rc), (w, z0 + rc)] + arc(*BR, 0, -45),
        'bottom': arc(*BR, -45, -90) + [(w - rc, z0), (-w + rc, z0)] + arc(*BL, -90, -135),
    }
    loop, svals = [], []
    for name in ('left', 'top', 'right', 'bottom'):
        pts = []
        for q in segs[name]:
            if not pts or math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) > 1e-6:
                pts.append(q)
        if name == 'top':                          # densify the printed face
            dense = [pts[0]]
            for q in pts[1:]:
                d = math.hypot(q[0] - dense[-1][0], q[1] - dense[-1][1])
                k = max(1, int(d / 0.4))
                for i in range(1, k + 1):
                    dense.append((dense[-1][0] + (q[0] - dense[-1][0]) * 1 / (k - i + 1),
                                  dense[-1][1] + (q[1] - dense[-1][1]) * 1 / (k - i + 1)))
            pts = dense
        L = [0.0]
        for i in range(1, len(pts)):
            L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
        s0, s1 = C['panels'][name]
        start = 1 if loop else 0                   # panels share their boundary point
        for q, l in list(zip(pts, L))[start:]:
            loop.append(q)
            svals.append(s0 + (s1 - s0) * l / L[-1])
    W_strip = C['size'][0]
    verts, faces, uvs = [], [], []
    rows = 9
    nl = len(loop)
    for j in range(rows):
        sj = -length / 2 + length * j / (rows - 1)
        for (x, z), sv in zip(loop, svals):
            verts.append(Vector(p) * MM + (x * b + z * up + sj * t) * MM)
            uvs.append((sv / W_strip, j / (rows - 1)))
    for j in range(rows - 1):
        for i in range(nl - 1):                    # open loop: the strip's end (s 60) meets s 23 at the corner
            a_, b_ = j * nl + i, j * nl + i + 1
            faces.append((a_, a_ + nl, b_ + nl, b_))
    ob = _mesh_obj('seal', verts, faces)
    me = ob.data
    uvl = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    c0 = me.polygons[len(me.polygons) // 2]
    if c0.normal.dot(c0.center - Vector(p) * MM - (up * (stack_mm / 2)) * MM) < 0:
        me.flip_normals()
    sol = ob.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = paper * MM
    sol.offset = 1.0
    sol.material_offset = 1
    sol.material_offset_rim = 2
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    # (with offset +1 the original faces end up outside and the generated shell inside)
    ob.data.materials.append(paper_material('seal_outside', art_path, PAPEL, rough=0.85))
    ob.data.materials.append(paper_material('seal_inside', None, PAPEL, rough=0.85))
    ob.data.materials.append(paper_material('seal_edge', None, PAPEL, rough=0.85))
    return ob


def _band_through_case(C=None, closed=False, route='drape', art_path=None, seal_art=None, floor_turn_deg=-90.0,
                       tail_turn_deg=55.0, with_seal=True, length=None):
    """The wristband doubled through the hasp's single aligned slot (tab + base front closed, base front open).
    Built as the OUTER leg's route from inside the slot to the clasp and on into the tail; the INNER leg is the
    same route offset one band thickness toward the case/floor and reversed, so the two layers nest exactly; a
    hidden 180 deg U-turn behind the wall joins them. Side 1 (jacquard) is outward on every visible run.
      route 'drape' (default): straight down the front face onto the floor, then (floor_turn_deg, -90 = to the
                    left) along the front of the case: the seal and clasp lie on the floor running across the frame,
                    so the seal's TOPO ("pode / rasgar.", lines along the band) reads upright from the front and
                    from above (C05). floor_turn_deg=0 runs straight at the camera (the seal then reads sideways).
                    It crosses ~15 mm of HOLOFOTE · AO VIVO (the slot sits at x = -13 mm, above the text).
      route 'corner': left along the front face ABOVE the text, round the front-left edge, the seal and clasp on
                    the upper left face (reading from the left), the tail down to the floor. Keeps the main panel
                    clear for a front-on closed shot. (The 350 mm band cannot reach the floor doubled on this route.)
    All in case-frame mm."""
    C = C or CASE
    L = length or BAND['L']
    T = BAND['T']
    hgt = None
    if not art_path:
        art_path, hgt = band_art()
    face = -C['D'] / 2 - (C['TAB_T'] + 0.02 if closed else 0.0)
    wall_in = -C['D'] / 2 + C['T']
    hx = C['W'] / 2
    xs, zs = C['SLOT_X'], C['SLOT_Z']
    out = Turtle((xs, wall_in + 0.8, zs + T / 2), (0, -1, 0), (0, 0, 1))
    out.fwd_to('y', face + 0.2).bend_to((0, 0, -1), 1.7)            # out of the slot, down the face (n = -Y)
    if route == 'drape':
        out.fwd_to('z', 1.5 + 3.0).bend_to((0, -1, 0), 3.0)        # onto the floor, toward the camera (n = +Z)
        out.fwd(1.0).turn(floor_turn_deg, 10.0)                     # then across the frame, in front of the case
        out.fwd(1.0)
        read = Vector((0, 1, 0))
        tail = [('bend', -9.0, 30.0), ('bend', 9.0, 30.0), ('turn', tail_turn_deg, 34.0), ('fwd', 400.0)]
    else:
        out.fwd(2.0).turn(-90.0, 8.0)                               # heading -X along the face, above the text
        out.fwd_to('x', -hx).bend(-90.0, 1.5)                      # round the front-left vertical edge (n = -X)
        out.fwd(3.0).turn(90.0, 5.0)                                # down the left face, clear of the edge
        out.fwd(3.0)
        read = Vector((0, 0, 1))
        tail = [('fwd_to', 'z', 1.5 + 3.0), ('bend_to', (-1, 0, 0), 3.0), ('fwd', 8.0), ('turn', 70.0, 22.0),
                ('fwd', 400.0)]
    out.mark('seal0')
    out.fwd(15.0 + 3.0 + 10.0)
    out.mark('clasp')
    out.fwd(6.0).mark('endA')
    # inner leg: the outer route from the slot to end A, offset by -n * T, reversed
    inner = []
    for p, t, n, s in out.samples:
        inner.append((p - n * T, -t, -n, 0.0))
    inner.reverse()
    # U-turn behind the wall: inner arrives heading +Y with n = -Z; turn up and back to heading -Y with n = +Z
    p0, t0, n0, _ = inner[-1]
    u = Turtle(p0, t0, n0)
    u.fwd(0.3).bend(-180.0, T / 2).fwd(0.3)
    # tail: continue the outer route past end A
    out.to_length(10_000.0, tail)
    seq = inner + u.samples[1:] + out.samples[1:]
    # arc length from positions, then trim to L
    s_acc, smp = 0.0, []
    for i, (p, t, n, _) in enumerate(seq):
        if i:
            s_acc += (p - seq[i - 1][0]).length
        smp.append((p, t, n, s_acc))
    tt = Turtle((0, 0, 0), (1, 0, 0), (0, 0, 1))
    tt.samples = smp
    tt.to_length(L, [])
    band = _band_object(tt.samples, art_path, L, hgt)
    cp, ct, cn, _ = out.marks['clasp']
    cl = clasp(cp - cn * 1.5, ct, cn)
    sl = None
    if with_seal:
        # the seal sits on the doubled run just before the clasp (case side), its text reading left->right from -Y
        k = [smp_ for smp_ in out.samples if smp_[3] <= out.marks['seal0'][3] + 7.5]
        sp, st, sn, _ = k[-1]
        sl = seal(sp - sn * 1.5, st, sn, read_up=read, art_path=seal_art)
    return Built(band=band, clasp=cl, seal=sl, length=tt.samples[-1][3])


def pulseira(preset='loose', ops=None, start=((0, 0, 0.5), (1, 0, 0), (0, 0, 1)), art_path=None, with_clasp=True,
             at=(0, 0, 0), rot_deg=0.0):
    """A PULSEIRA (§C.6) on its own: 15 x 350 mm woven band + clasp at end A, lying on z = 0.
    preset 'loose': a relaxed S on the floor, jacquard side up, clasp open at end A, tail end free.
    ops: your own Turtle steps, e.g. [('fwd', 40), ('turn', 30, 50), ('bend', 10, 60), ...] from `start`
    (point, tangent, side-1 normal, all mm). For the band threaded through O CASE use case(band=True).
    Returns Built(root, band, clasp)."""
    hgt = None
    if not art_path:
        art_path, hgt = band_art()
    before = set(bpy.data.objects)
    p, t, n = start
    tu = Turtle(p, t, n)
    if ops is None and preset == 'loose':
        ops = [('fwd', 28), ('turn', 38, 55), ('fwd', 22), ('bend', 7, 70), ('bend', -7, 70), ('turn', -95, 42),
               ('fwd', 18), ('turn', 55, 60), ('fwd', 400)]
    tu.to_length(BAND['L'], ops or [('fwd', 400)])
    band = _band_object(tu.samples, art_path, BAND['L'], hgt)
    cl = None
    if with_clasp:
        p0, t0, n0, _ = tu.samples[0]
        cl = clasp(p0 + t0 * 6.0 - n0 * (BAND['T'] / 2), t0, n0)
    root = _finish('pulseira_root', before, at, rot_deg)
    return Built(root=root, band=band, clasp=cl)


# =============================================================================================== 3. A SETLIST
SETLIST = dict(W=105.0, P=100.0, N=4, T=0.4, R=0.5)


def setlist(state='folded', fold_deg=None, side1=None, side2=None, lie=True, perforations=True, first_fold=-1,
            at=(0, 0, 0), rot_deg=0.0):
    """A SETLIST (§C.8): concertina card 105 x 400 flat, four 105 x 100 panels, 300 g/m2 uncoated papel (0,4 mm).
    side1 / side2: 105 x 400 art (P1 at the TOP of the image); side 2 is drawn as seen from the back, P1' at the top.
    state 'folded' (fold 178 deg, ~3 mm thick, standing, P1 facing -Y, bottom folds on z = 0) |
          'fan'    (default fold 70 deg: panels +-35 deg; lies on the floor, P1 far; lie=False stands it) |
          'flat'   (open on the floor, P1 away from the camera, faint residual creases).
    Perforations (between the tickets, the P3/P4 fold and the 22 mm stubs at x = 83) are cut into the card shader.
    first_fold -1 | +1 flips the zigzag: lying fans tilt P2/P4 (the tickets) toward a front camera with -1, P1/P3
    (the cover) with +1; seen from above (70 deg) all four panels show either way.
    Returns Built(root, card)."""
    S = SETLIST
    side1 = side1 or pfile('setlist', 'SETLIST_lado-1.png') or ph('PH_SETLIST_lado1.png')
    side2 = side2 or pfile('setlist', 'SETLIST_lado-2.png') or ph('PH_SETLIST_lado2.png')
    picote = pfile('setlist', 'SETLIST_picote_lado-1.png')
    before = set(bpy.data.objects)
    if fold_deg is None:
        fold_deg = {'folded': 180.0, 'fan': 70.0, 'flat': 3.0}[state]
    r = S['R']
    # path in the (y, z) plane: start at P1's top edge heading down, side 1 facing -Y
    tu = Turtle((0, 0, 0), (0, 0, -1), (0, -1, 0), step=2.0)
    sign = -1.0 if first_fold < 0 or state == 'folded' else 1.0
    for i in range(S['N']):
        straight = S['P'] - (r * math.radians(fold_deg) if i in (0, S['N'] - 1) else 2 * r * math.radians(fold_deg)) / 2
        tu.fwd(straight)
        if i < S['N'] - 1:
            tu.bend(sign * fold_deg, r)
            sign = -sign
    samples = tu.samples
    card = _strip_mesh('setlist', samples, S['W'], total=samples[-1][3])
    # strip UV convention: v=1 on the -b edge; here b = t x n with t=-Z, n=-Y -> b = -X, so v=1 is +X: re-map so
    # u (image x) runs -X -> +X as seen on side 1 and v (image y) runs from P1 (top, s=0) to P4 (bottom)
    me = card.data
    uvl = me.uv_layers['UVMap']
    tot = samples[-1][3]
    for poly in me.polygons:
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co / MM
            s_u = uvl.data[li].uv[0] * tot
            uvl.data[li].uv = (co.x / S['W'] + 0.5, 1.0 - s_u / tot)
    sol = card.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = S['T'] * MM
    sol.offset = -1.0
    sol.use_even_offset = True
    sol.material_offset = 1
    sol.material_offset_rim = 2
    m1 = _card_material('setlist_lado1', side1, perforations, tot, picote=picote)
    m2 = _card_material('setlist_lado2', side2, perforations, tot, mirror_u=True, picote=picote)
    card.data.materials.append(m1)
    card.data.materials.append(m2)
    card.data.materials.append(_mat('setlist_edge', **{'Base Color': srgb('#F7F1E4'), 'Roughness': 0.9}))
    # orientation
    zs = [v.co.z for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    if state == 'folded' or (state == 'fan' and not lie):
        me.transform(Matrix.Translation((0, -(max(ys) + min(ys)) / 2, -min(zs))))
    else:
        # lay the zigzag / open card on the floor: average path direction -> +Y (P1 away from the camera)
        p0, pN = samples[0][0], samples[-1][0]
        d = (p0 - pN)
        ang = math.atan2(d.z, d.y)
        me.transform(Matrix.Rotation(-ang, 4, 'X'))
        zs = [v.co.z for v in me.vertices]
        ys = [v.co.y for v in me.vertices]
        me.transform(Matrix.Translation((0, -(max(ys) + min(ys)) / 2, -min(zs) + S['T'] * MM)))
        if True:
            # side 1 must face up: flip if the open card faces down
            nrm = sum((p.normal for p in me.polygons), Vector())
            if nrm.z < 0:
                me.transform(Matrix.Rotation(math.pi, 4, 'Y'))
                zs = [v.co.z for v in me.vertices]
                me.transform(Matrix.Translation((0, 0, -min(zs) + S['T'] * MM)))
    me.update()
    root = _finish('setlist_root', before, at, rot_deg)
    return Built(root=root, card=card, length=tot)


_setlist_fn = setlist


def _card_material(name, art_path, perforations, total_len, mirror_u=False, picote=None):
    S = SETLIST
    m = paper_material(name, art_path, PAPEL, rough=0.88)
    if mirror_u:
        N = _NT(m)
        tx = [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
        uvn = [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeUVMap'][0]
        u, v, _ = N.sep(uvn.outputs['UV'])
        N.link(N.comb(N.m('SUBTRACT', 1.0, u), v, 0.0), tx.inputs['Vector'])
    if perforations and picote:
        # the packaging team's die mask (side 1 layout; side 2 reads it mirrored): the slits show as shadowed cuts
        N = _NT(m)
        bs = _bsdf(m)
        uvn = [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeUVMap'][0]
        vec = uvn.outputs['UV']
        if mirror_u:
            u, v, _ = N.sep(vec)
            vec = N.comb(N.m('SUBTRACT', 1.0, u), v, 0.0)
        pk = N.tex(picote, vec, 'Non-Color').outputs['Color']
        base_col = [l.from_socket for l in m.node_tree.links if l.to_socket == bs.inputs['Base Color']][0]
        N.link(N.mix(N.m('MULTIPLY', N.m('ADD', pk, 0.0), 0.65), base_col, (0.05, 0.045, 0.04, 1)), bs.inputs['Base Color'])
    elif perforations:
        N = _NT(m)
        bs = _bsdf(m)
        uvn = [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeUVMap'][0]
        u, v, _ = N.sep(uvn.outputs['UV'])
        xm = N.m('MULTIPLY', u if not mirror_u else N.m('SUBTRACT', 1.0, u), S['W'])
        ym = N.m('MULTIPLY', N.m('SUBTRACT', 1.0, v), S['P'] * S['N'])          # 0 at P1 top .. 400 at P4 bottom
        dash_x = N.smooth(N.m('PINGPONG', xm, 0.5), 0.12, 0.2)                    # 0,5 mm cut / 0,5 mm tie
        dash_y = N.smooth(N.m('PINGPONG', ym, 0.5), 0.12, 0.2)
        hl = None
        for yy in (300.0, 325.0, 350.0, 375.0):
            line = N.smooth(N.m('ABSOLUTE', N.m('SUBTRACT', ym, yy)), 0.16, 0.06)
            hl = line if hl is None else N.m('MAXIMUM', hl, line)
        vline = N.m('MULTIPLY', N.smooth(N.m('ABSOLUTE', N.m('SUBTRACT', xm, 83.0)), 0.16, 0.06), N.smooth(ym, 299.8, 300.2))
        perf = N.m('MAXIMUM', N.m('MULTIPLY', hl, dash_x), N.m('MULTIPLY', vline, dash_y))
        base_col = [l.from_socket for l in m.node_tree.links if l.to_socket == bs.inputs['Base Color']][0]
        N.link(N.mix(N.m('MULTIPLY', perf, 0.7), base_col, (0.05, 0.045, 0.04, 1)), bs.inputs['Base Color'])
    return m


def gaffer_material(name='gaffer', hexcol=AMARELO, seed=0.0):
    """Cloth gaffer tape: woven bump, matte, torn ends cut by alpha (the strip's UV u in 0..1 along its length)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    bs.inputs['Base Color'].default_value = srgb(hexcol)
    bs.inputs['Roughness'].default_value = 0.58
    bs.inputs['Specular IOR Level'].default_value = 0.4
    tc = N.new('ShaderNodeTexCoord')
    uvn = N.new('ShaderNodeUVMap', uv_map='UVMap')
    u, v, _ = N.sep(uvn.outputs['UV'])
    pm = N.v('MULTIPLY', tc.outputs['Object'], (1000.0, 1000.0, 1000.0))
    x, y, _ = N.sep(pm)
    weave = N.m('MULTIPLY', N.m('SINE', N.m('MULTIPLY', x, 2 * math.pi / 0.7)), N.m('SINE', N.m('MULTIPLY', y, 2 * math.pi / 0.7)))
    N.link(N.bump(weave, 0.025), bs.inputs['Normal'])
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 9.0
    nz.inputs['Detail'].default_value = 6.0
    nz.noise_dimensions = '2D'
    N.link(N.comb(N.m('ADD', v, seed), 0.0, 0.0), nz.inputs['Vector'])
    jag = N.m('MULTIPLY', N.m('SUBTRACT', nz.outputs['Fac'], 0.5), 0.035)
    keep = N.m('MULTIPLY', N.smooth(N.m('ADD', u, jag), 0.012, 0.02), N.smooth(N.m('SUBTRACT', u, jag), 0.988, 0.98))
    tr = N.new('ShaderNodeBsdfTransparent')
    mix = N.new('ShaderNodeMixShader')
    N.link(keep, mix.inputs[0])
    N.link(tr.outputs[0], mix.inputs[1])
    N.link(bs.outputs[0], mix.inputs[2])
    N.link(mix.outputs[0], m.node_tree.nodes['Material Output'].inputs[0])
    return m


def gaffer_strip(p0, p1, width=48.0, step_at=None, step_h=0.4, lift_end=0.0, hexcol=AMARELO, seed=0.0, z=0.0):
    """A strip of cloth gaffer tape from p0 to p1 (mm, on the floor at height z), torn at both ends.
    step_at=(point, normal_dir): the tape climbs onto a card edge of height step_h there. lift_end lifts the far
    end's corner by that many mm (the one lifted corner of the anti-slop budget)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0)
    L = d.length
    t = d.normalized()
    side = Vector((0, 0, 1)).cross(t).normalized()
    nu, nv = max(8, int(L / 1.5)), 6
    verts, faces, uvs = [], [], []
    for i in range(nu + 1):
        s = L * i / nu
        for j in range(nv + 1):
            w = -width / 2 + width * j / nv
            p = p0 + t * s + side * w
            h = z + 0.12
            if step_at is not None:
                q, nn = Vector(step_at[0]), Vector(step_at[1]).normalized()
                dd = (p - q).dot(nn)                       # > 0 = off the card
                h += step_h * (1 - min(1.0, max(0.0, (dd + 0.2) / 1.4)))
            if lift_end > 0 and s > L - 18:
                h += lift_end * ((s - (L - 18)) / 18) ** 2 * (1 if w > width / 4 else 0.25 * max(0.0, (w + width / 2) / width))
            verts.append(Vector((p.x, p.y, h)) * MM)
            uvs.append((s / L, j / nv))
    for i in range(nu):
        for j in range(nv):
            a = i * (nv + 1) + j
            faces.append((a, a + nv + 1, a + nv + 2, a + 1))
    ob = _mesh_obj('gaffer', verts, faces)
    uv = ob.data.uv_layers.new(name='UVMap')
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            uv.data[li].uv = uvs[ob.data.loops[li].vertex_index]
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    ob.data.materials.append(gaffer_material('gaffer', hexcol, seed))
    return ob


def setlist_taped(side1=None, at=(0, 0, 0), rot_deg=0.0, tape_hex=AMARELO, crease_deg=2.0, overlap_mm=10.0):
    """The setlist open flat and taped to the stage floor (C04 style): two torn strips of amarelo cloth gaffer,
    48 mm, across the top (P1) and bottom (P4) edges, each catching overlap_mm of the card; one corner lifted.
    P1 is away from the camera (+Y). side1: any 105 x 400 art (P1 at the top)."""
    before = set(bpy.data.objects)
    sl = setlist(state='flat', fold_deg=crease_deg, side1=side1, lie=True)
    ys = [(sl.card.matrix_world @ v.co).y / MM for v in sl.card.data.vertices]
    y_top, y_bot = max(ys), min(ys)
    W, half = SETLIST['W'], 24.0
    ct, cb = y_top - overlap_mm + half, y_bot + overlap_mm - half
    t1 = gaffer_strip((-W / 2 - 24, ct - 1.0, 0), (W / 2 + 26, ct + 1.0, 0), step_at=((0, y_top, 0), (0, 1, 0)),
                      step_h=SETLIST['T'] + 0.1, hexcol=tape_hex, seed=0.3)
    t2 = gaffer_strip((W / 2 + 22, cb - 1.0, 0), (-W / 2 - 25, cb + 1.0, 0), step_at=((0, y_bot, 0), (0, -1, 0)),
                      step_h=SETLIST['T'] + 0.1, lift_end=1.0, hexcol=tape_hex, seed=1.7)
    root = _finish('setlist_taped_root', before, at, rot_deg)
    return Built(root=root, setlist=sl, tapes=(t1, t2))


# =============================================================================================== 4. NOVA TEMPORADA
def refil_contract(faixa='02'):
    """The packaging team's refill files (02_PRODUTO/refil/, generator _build/pack/refil.py) and their geometry."""
    d = os.path.join(PRODUTO, 'refil')
    c = dict(lid=None, band=None, disc_mm=66.0, tab_mm=(9.0, 14.0), lid_px_mm=None,
             band_h=10.0, band_below_lip=12.0, band_centre_u=0.25)
    j = os.path.join(d, 'HLF-REF_refil.json')
    lid = os.path.join(d, 'HLF-REF-%s_TAMPA-PEEL.png' % faixa)
    band = os.path.join(d, 'HLF-REF_CAPSULA_faixa-laser.png')
    c['lid'] = lid if os.path.exists(lid) else None
    c['band'] = band if os.path.exists(band) else None
    if os.path.exists(j):
        import json
        try:
            J = json.load(open(j))
            L = [x for x in J['lids'] if x['sku'].endswith(faixa)][0]
            c['disc_mm'] = L['disc_mm']
            c['tab_mm'] = tuple(L['tab_mm'])
            c['lid_px_mm'] = (L['px'][0] / L['ppmm'], L['px'][1] / L['ppmm'])
            c['band_h'] = J['band']['height_mm']
            c['band_centre_u'] = J['band']['centre_u']
        except Exception as e:
            print('refil_contract: json not read (%s)' % e)
    return c


def refil(faixa='02', lid_art=None, band_art=None, peel=0.0, lid_d=68.6, at=(0, 0, 0), rot_deg=0.0):
    """NOVA TEMPORADA refill (§C.9): the A CÁPSULA of holofote.py (black anodised deep-drawn aluminium Ø68 x 74,
    rolled lip, wax + wood wick inside) standing on z = 0, closed by a heat-sealed paper/foil peel lid with its
    pull tab pointing +X (the packaging art's right).
    lid_art   the printed peel lid (packaging: HLF-REF-0n_TAMPA-PEEL.png, 40 px/mm: the Ø66 disc on the left, the
              tab to the right). The physical lid is lid_d (68,6, the lip's outer edge: a Ø66 lid cannot seal on the
              Ø67,4 lip); the ring outside the Ø66 print is the faixa colour.
    band_art  the laser-marked LOTE · FAB · VAL wall band (HLF-REF_CAPSULA_faixa-laser.png, u = 0,25 at the front,
              10 mm tall, centred 12 mm below the lip); the ink renders as bare aluminium.
    peel      0 sealed .. 1 fully peeled back from the tab side (0,5 = half-peeled, L07 / C08).
    Returns Built(root, capsule, wax, wick, lid)."""
    K = refil_contract(faixa)
    lid_art = lid_art or K['lid'] or ph('PH_REFIL_tampa.png')
    band_art = band_art or K['band'] or ph('PH_REFIL_faixa.png')
    before = set(bpy.data.objects)
    H.use_size('200')
    base = H.BASE
    cap = H.lathe('refil_capsule', H.capsule_profile(), segs=256)
    black, alu = H.capsule_materials()
    cap.data.materials.append(black)
    cap.data.materials.append(alu)
    for p in cap.data.polygons:
        c = p.center
        r = math.hypot(c.x, c.y) / MM
        if r < H.CAP_R - H.CAP_T / 2 - 0.05 and c.z / MM < base + H.CAP_H - H.CAP_LIP - 0.05 and p.normal.z < 0.9:
            p.material_index = 1
        if c.z / MM < base + H.CAP_T + 0.01 and p.normal.z > 0.5:
            p.material_index = 1
    wax = H.lathe('refil_wax', H.wax_profile(False), segs=256, smooth_angle=60)
    wax.data.materials.append(H.wax_material(False))
    wick = H.wick_plank(False, False, False)
    parts = [cap, wax, wick]
    # laser band: a 360 deg shell 0,02 mm proud of the wall, u = centre_u at the front (-Y)
    top = base + H.CAP_H
    zc = top - K['band_below_lip']
    z0, z1 = zc - K['band_h'] / 2, zc + K['band_h'] / 2
    r = H.CAP_R + 0.02
    segs = 720
    verts, faces, uvs = [], [], []
    for i in range(segs + 1):
        u = i / segs
        a = (u - K['band_centre_u']) * 2 * math.pi
        for k, z in enumerate((z0, z1)):
            verts.append(Vector((r * math.sin(a), -r * math.cos(a), z)) * MM)
            uvs.append((u, float(k)))
    for i in range(segs):
        a = 2 * i
        faces.append((a, a + 2, a + 3, a + 1))
    sh = _mesh_obj('refil_laser', verts, faces)
    uv = sh.data.uv_layers.new(name='UVMap')
    for poly in sh.data.polygons:
        for li in poly.loop_indices:
            uv.data[li].uv = uvs[sh.data.loops[li].vertex_index]
    f0 = sh.data.polygons[0]
    if f0.normal.dot(Vector((f0.center.x, f0.center.y, 0))) < 0:
        sh.data.flip_normals()
    sh.data.polygons.foreach_set('use_smooth', [True] * len(sh.data.polygons))
    m = bpy.data.materials.new('laser')
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    tx = N.tex(band_art, N.new('ShaderNodeUVMap', uv_map='UVMap').outputs['UV'])
    bs.inputs['Base Color'].default_value = srgb('#B9BBBD')
    bs.inputs['Metallic'].default_value = 1.0
    bs.inputs['Roughness'].default_value = 0.45
    tr = N.new('ShaderNodeBsdfTransparent')
    mix = N.new('ShaderNodeMixShader')
    N.link(tx.outputs['Alpha'], mix.inputs[0])
    N.link(tr.outputs[0], mix.inputs[1])
    N.link(bs.outputs[0], mix.inputs[2])
    N.link(mix.outputs[0], m.node_tree.nodes['Material Output'].inputs[0])
    sh.data.materials.append(m)
    parts.append(sh)
    lid = _peel_lid(faixa, lid_art, peel, lid_d, K, z=top + 0.04)
    parts.append(lid)
    holder = _empty('refil_offset', (0, 0, -base * MM))
    _parent(parts, holder)
    root = _finish('refil_root', before, at, rot_deg)
    return Built(root=root, capsule=cap, wax=wax, wick=wick, lid=lid)


def _peel_lid(faixa, lid_art, peel, lid_d, K, z, rings=44, segs=176, bend_r=7.0, bend_max=150.0):
    """Peel lid: polar disc + the pull tab along +X, 0,12 mm; printed paper on top, foil underneath with the seal
    ring pressed in by the lip. Peeling curls everything past a bend line (moving from the tab side, peel 0, to the
    far side, peel 1) back over the top on a radius bend_r."""
    R = lid_d / 2
    disc = K['disc_mm']
    tl, tw = K['tab_mm']
    if K.get('lid_px_mm'):
        img_w, img_h = K['lid_px_mm']
        x_end = img_w - disc / 2                   # the tab's end, from the disc centre
    else:
        img_w, img_h, x_end = disc + tl + 2.0, disc, disc / 2 + tl + 2.0
    verts = [(0.0, 0.0)]
    for i in range(1, rings + 1):
        rr = R * i / rings
        for j in range(segs):
            a = 2 * math.pi * j / segs
            verts.append((rr * math.cos(a), rr * math.sin(a)))
    faces = [(0, 1 + j, 1 + (j + 1) % segs) for j in range(segs)]
    for i in range(1, rings):
        o0, o1 = 1 + (i - 1) * segs, 1 + i * segs
        for j in range(segs):
            faces.append((o0 + j, o1 + j, o1 + (j + 1) % segs, o0 + (j + 1) % segs))
    k0 = len(verts)
    nx, ny, rc = 12, 10, 2.5
    for iy in range(ny + 1):
        y = -tw / 2 + tw * iy / ny
        x0 = math.sqrt(max(0.0, R * R - y * y)) - 1.0
        dy = abs(y) - (tw / 2 - rc)
        x1 = x_end - rc + math.sqrt(max(0.0, rc * rc - dy * dy)) if dy > 0 else x_end
        for ix in range(nx + 1):
            verts.append((x0 + (x1 - x0) * ix / nx, y))
    for iy in range(ny):
        for ix in range(nx):
            a = k0 + iy * (nx + 1) + ix
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    xb = R - peel * 2 * R
    th = math.radians(bend_max)
    out, uvs = [], []
    for k, (x, y) in enumerate(verts):
        zz = 0.015 if k >= k0 else 0.0
        xx = x
        if peel > 0 and x > xb:
            u = x - xb
            if u <= bend_r * th:
                ph_ = u / bend_r
                xx = xb + bend_r * math.sin(ph_)
                zz += bend_r * (1 - math.cos(ph_))
            else:
                x0_ = xb + bend_r * math.sin(th)
                z0_ = bend_r * (1 - math.cos(th))
                e = u - bend_r * th
                xx = x0_ + e * math.cos(th)
                zz += z0_ + e * math.sin(th)
        elif peel <= 0 and x > R - 0.5:
            zz += (x - R + 0.5) ** 2 * 0.012          # the tab lifts a touch on a sealed lid
        out.append(Vector((xx, y, z + zz)) * MM)
        uvs.append(((x + disc / 2) / img_w, (y + img_h / 2) / img_h))
    ob = _mesh_obj('refil_lid', out, faces)
    uv = ob.data.uv_layers.new(name='UVMap')
    for poly in ob.data.polygons:
        for li in poly.loop_indices:
            uv.data[li].uv = uvs[ob.data.loops[li].vertex_index]
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    sol = ob.modifiers.new('sol', 'SOLIDIFY')
    sol.thickness = 0.12 * MM
    sol.offset = -1.0
    sol.material_offset = 1
    sol.material_offset_rim = 1
    m = bpy.data.materials.new('peel_top')
    m.use_nodes = True
    N = _NT(m)
    bs = _bsdf(m)
    tx = N.tex(lid_art, N.new('ShaderNodeUVMap', uv_map='UVMap').outputs['UV'])
    coat = srgb(FAIXA_COAT.get(faixa, AMARELO))
    N.link(N.mix(tx.outputs['Alpha'], coat, tx.outputs['Color']), bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.5
    bs.inputs['Specular IOR Level'].default_value = 0.4
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / (0.5 * MM)
    N.link(tc.outputs['Object'], nz.inputs['Vector'])
    N.link(N.bump(nz.outputs['Fac'], 0.02), bs.inputs['Normal'])
    ob.data.materials.append(m)
    f = bpy.data.materials.new('peel_foil')
    f.use_nodes = True
    N = _NT(f)
    bs = _bsdf(f)
    bs.inputs['Metallic'].default_value = 1.0
    u, v, _ = N.sep(N.new('ShaderNodeUVMap', uv_map='UVMap').outputs['UV'])
    xm = N.m('SUBTRACT', N.m('MULTIPLY', u, img_w), disc / 2)
    ym = N.m('SUBTRACT', N.m('MULTIPLY', v, img_h), img_h / 2)
    rmm = N.m('SQRT', N.m('ADD', N.m('MULTIPLY', xm, xm), N.m('MULTIPLY', ym, ym)))
    ring = N.m('MULTIPLY', N.smooth(rmm, 33.0, 33.4), N.smooth(rmm, 34.4, 34.0))
    N.link(N.remap(ring, 0, 1, 0.28, 0.6), bs.inputs['Roughness'])
    N.link(N.mix(ring, srgb('#CFD1D3'), srgb('#A9A39A')), bs.inputs['Base Color'])
    N.link(N.bump(ring, 0.04), bs.inputs['Normal'])
    ob.data.materials.append(f)
    return ob


# =============================================================================================== 6. PREVIS MANNEQUIN
GREY = dict(skin='#8C8C8C', trousers='#5C5C5E', shoes='#3A3A3B', tee='#474748', cardigan='#BDBDBB',
            sweat='#A2A2A2', bag='#2E2E30', hair_H01='#D2D2D0', hair_H02='#2C2C2D', phone='#141416')

# Proportions are fractions of height H (Drillis & Contini-style segment ratios, tuned by eye on the renders).
BODIES = {
    'H01': dict(H=1.65, sh=0.095, hip=0.055, pelvis=(0.088, 0.066), waist=(0.071, 0.055), chest=(0.083, 0.062),
                neck=0.032, arm=(0.034, 0.029, 0.022, 0.021, 0.016), leg=(0.054, 0.047, 0.032, 0.031, 0.019),
                head=(0.045, 0.057, 0.066), top='cardigan', hair='buzz', bag=False),
    'H02': dict(H=1.76, sh=0.104, hip=0.051, pelvis=(0.084, 0.063), waist=(0.079, 0.059), chest=(0.093, 0.068),
                neck=0.037, arm=(0.038, 0.033, 0.024, 0.024, 0.018), leg=(0.054, 0.047, 0.033, 0.032, 0.020),
                head=(0.044, 0.056, 0.064), top='sweatshirt', hair='fade', bag=True),
}
SEG = dict(ua=0.186, fa=0.146, hand=0.108, th=0.245, sh=0.246, foot=0.152, ankle=0.039)


def _frame(y_dir, z_hint):
    """Right-handed rotation whose columns are X, Y, Z with Y = y_dir and Z as close to z_hint as possible."""
    Y = Vector(y_dir).normalized()
    Z = Vector(z_hint) - Y * Vector(z_hint).dot(Y)
    if Z.length < 1e-6:
        Z = Y.orthogonal()
    Z.normalize()
    return Matrix((Y.cross(Z), Y, Z)).transposed()


def _ik2(a, c, L1, L2, pole):
    """Two-bone IK: joint positions (mid, end) for a chain of lengths L1, L2 from a toward c, bending toward pole."""
    a, c = Vector(a), Vector(c)
    d = c - a
    dist = min(max(d.length, 1e-4), (L1 + L2) * 0.999)
    u = d.normalized()
    c = a + u * dist
    x = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(0.0, L1 * L1 - x * x))
    pv = Vector(pole) - u * Vector(pole).dot(u)
    pv = pv.normalized() if pv.length > 1e-6 else u.orthogonal().normalized()
    return a + u * x + pv * h, c


def _pose_skeleton(B, pose, key):
    """Joint positions (root-local metres, facing -Y) plus hand/foot/head frames for one pose key.
    Standing poses: root on the floor between the feet. Sitting poses: root on the stage's top front edge (the edge
    runs along X at y = 0, the stage is +Y, the drop is -Y)."""
    Hh = B['H']
    L = {k: v * Hh for k, v in SEG.items()}
    sit = pose in ('a', 'd')
    J, F = {}, {}
    lean, slouch = (6.0, 7.0) if sit else (0.0, 2.0)
    if sit:
        knee_y = -0.085
        hip_z = 0.056 * Hh
        J['pelvis'] = Vector((0.0, knee_y + L['th'] * 0.995, hip_z))
    else:
        J['pelvis'] = Vector((0.0, 0.0, 0.51 * Hh))
    Rw = Matrix.Rotation(math.radians(lean), 3, 'X')
    Rc = Matrix.Rotation(math.radians(lean + slouch), 3, 'X')
    J['waist'] = J['pelvis'] + Rw @ Vector((0, 0, 0.10 * Hh))
    J['chest'] = J['waist'] + Rc @ Vector((0, 0, 0.115 * Hh))
    J['neck'] = J['chest'] + Rc @ Vector((0, 0.004 * Hh, 0.088 * Hh))
    J['neck_top'] = J['neck'] + Matrix.Rotation(math.radians(lean + slouch - 10.0), 3, 'X') @ Vector((0, 0, 0.05 * Hh))
    for s, side in ((1, 'L'), (-1, 'R')):
        J['shoulder_' + side] = J['neck'] + Rc @ Vector((s * B['sh'] * Hh, 0.006 * Hh, -0.020 * Hh))
        J['hip_' + side] = J['pelvis'] + Vector((s * B['hip'] * Hh, 0.0, 0.0))
    # --- legs
    for s, side in ((1, 'L'), (-1, 'R')):
        hp = J['hip_' + side]
        if sit:
            kn = hp + Vector((s * 0.012, -L['th'] * math.cos(math.radians(3)), -L['th'] * math.sin(math.radians(3))))
            sw = math.radians(4.0 if side == 'L' else -3.0)       # the legs dangle, one a touch forward
            an = kn + Vector((s * 0.01, L['sh'] * math.sin(math.radians(9)) * (1 if side == 'L' else 0.6),
                              -L['sh'] * math.cos(math.radians(9))))
            fdir = Vector((s * 0.12, -math.cos(math.radians(38)) + sw, -math.sin(math.radians(38))))
        else:
            an = Vector((s * 0.105 * Hh / 1.7, 0.0, L['ankle']))
            kn, an = _ik2(hp, an, L['th'], L['sh'], (0, -1, 0))
            fdir = Vector((s * 0.16, -1.0, 0.0))
        J['knee_' + side], J['ankle_' + side] = kn, an
        J['thigh_' + side] = hp.lerp(kn, 0.45)
        J['calf_' + side] = kn.lerp(an, 0.32)
        F['foot_' + side] = (an, _frame(fdir, (0, 0, 1)))
    # --- head: looks at the camera (-Y), level
    yaw, pitch = 0.0, (-4.0 if sit else 0.0)
    Rh = Matrix.Rotation(math.radians(yaw), 3, 'Z') @ Matrix.Rotation(math.radians(-pitch), 3, 'X')
    F['head'] = (J['neck_top'] + Rh @ Vector((0, -0.010 * Hh, 0.050 * Hh)), Rh)
    # --- arms: wrist targets per pose, then IK
    S = {side: J['shoulder_' + side] for side in 'LR'}
    ch = J['chest']
    hands = {}
    if pose == 'a' or pose == 'd':
        # hands flat on the stage beside the hips, fingers forward
        for s, side in ((1, 'L'), (-1, 'R')):
            hands[side] = (Vector((s * 0.205, J['pelvis'].y - 0.03, 0.022)), (s * 0.25, -1, 0), (0, 0, 1), 'rest',
                           (s * 0.6, 1.0, 0.2))
    if pose == 'b':
        apart = (key != 'B')
        for s, side in ((1, 'L'), (-1, 'R')):
            x = s * (0.125 if apart else 0.019)
            w = Vector((x, ch.y - 0.27, ch.z - 0.035))
            hands[side] = (w, (-s * (0.25 if apart else 0.05), -0.55, 0.8), (s, 0, 0), 'flat', (s * 0.8, 0.4, -1.0))
    if pose == 'c':
        hands['L'] = (S['L'] + Vector((0.035, 0.02, -L['ua'] - L['fa'] + 0.03)), (0.05, -0.1, -1), (1, 0, 0), 'rest',
                      (0.3, 1.0, 0.0))
        hands['R'] = (S['R'] + Vector((-0.07, -0.05, L['ua'] + L['fa'] - 0.05)), (0.08, -0.05, 1), (0, -1, 0), 'hold',
                      (-1.0, 0.4, -0.2))
    if pose == 'd':
        if key != 'B':      # finger heart, at chin height in front of the right chest, palm to camera
            hands['R'] = (S['R'] + Vector((0.08, -0.30, -0.06)), (0.10, -0.35, 1.0), (0, 1, 0.2), 'heart',
                          (-0.6, 0.3, -1.0))
        else:               # pointing at the lens, arm out, index forward, palm down
            hands['R'] = (S['R'] + Vector((0.05, -L['ua'] - L['fa'] + 0.02, 0.06)), (0.06, -1, 0.06), (0, 0, 1), 'point',
                          (-0.7, 0.2, -1.0))
    for side in 'LR':
        w, fdir, ddir, shape, pole = hands[side]
        el, wr = _ik2(S[side], w, L['ua'], L['fa'], pole)
        J['elbow_' + side], J['wrist_' + side] = el, wr
        J['uarm_' + side] = S[side].lerp(el, 0.45)
        J['farm_' + side] = el.lerp(wr, 0.5)
        F['hand_' + side] = (wr, _frame(fdir, ddir), shape)
    # garment helper nodes
    up = Rw @ Vector((0, 0, 1))
    J['hem'] = J['pelvis'] - up * (0.07 * Hh) + Vector((0, -0.004 * Hh, 0))
    J['hem_s'] = J['pelvis'] - up * (0.03 * Hh)
    J['collar'] = J['neck'] + Rc @ Vector((0, 0.002 * Hh, -0.006 * Hh))
    J['yoke'] = J['neck'] + Rc @ Vector((0, 0.006 * Hh, -0.024 * Hh))
    F['torso'] = (J['chest'], Rc, Rw)
    return J, F


def _hand_parts(shape, s, Lh):
    """Ellipsoid parts (centre, axis, radii) of a hand in hand-local coords (Y fingers, Z dorsal, thumb on -X for the
    right hand). s = +1 left, -1 right. Same part count for every shape so two shapes can blend as shape keys."""
    u = Lh
    curl = dict(flat=4, rest=16, hold=78, point=118, heart=122)[shape]
    icurl = dict(flat=4, rest=14, hold=62, point=0, heart=48)[shape]
    tdir = dict(flat=(-0.42, 0.9, 0.0), rest=(-0.5, 0.85, -0.15), hold=(-0.15, 0.85, -0.55), point=(0.45, 0.55, -0.75),
                heart=(0.12, 1.0, 0.18))[shape]

    def mx(v):                     # parts are written for the right hand (thumb on -X); mirror x for the left
        return Vector((v[0] * (1 if s < 0 else -1), v[1], v[2]))
    parts = [(mx((0.01 * u, 0.27 * u, 0.0)), Vector((0, 1, 0)), (0.215 * u, 0.29 * u, 0.068 * u), 0.55)]
    for pivx, length, rad, c in ((0.060, 0.50, (0.165, 0.27, 0.058), curl), (-0.135, 0.48, (0.068, 0.26, 0.055), icurl)):
        piv = Vector((pivx * u, 0.47 * u, 0.0))
        R = Matrix.Rotation(math.radians(-c), 3, 'X')
        axis = R @ Vector((0, 1, 0))
        if shape == 'heart' and pivx < 0:
            axis = Matrix.Rotation(math.radians(18), 3, 'Z') @ axis
        cen = piv + axis * (length * u / 2 - 0.02 * u)
        parts.append((mx(cen), mx(axis), (rad[0] * u, rad[1] * u, rad[2] * u), 0.6 if pivx > 0 else 0.8))
    td = Vector(tdir).normalized()
    tp = Vector((-0.17 * u, 0.10 * u, -0.025 * u))
    parts.append((mx(tp + td * 0.18 * u), mx(td), (0.068 * u, 0.19 * u, 0.064 * u), 0.9))
    return parts


def _parts_mesh(name, parts, segs=20, rings=12):
    bm = bmesh.new()
    for part in parts:
        cen, axis, rad = part[:3]
        R = _frame(axis, (0, 0, 1))
        _ellipsoid_bm(bm, cen, (rad[0], rad[1], rad[2]), R, segs, rings, part[3] if len(part) > 3 else 1.0)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    return me


def _head_mesh(B, Hh, hair=None, segs=48, rings=32):
    """The head in head-local coords (centre at the origin, face toward -Y): an egg cranium with a narrower jaw, a
    chin, a simple nose and brow, small ears. hair='buzz' | 'fade' returns the hair shell instead."""
    w, d, h = (B['head'][0] * Hh, B['head'][1] * Hh, B['head'][2] * Hh)
    bm = bmesh.new()
    ret = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    for v in ret['verts']:
        x, y, z = v.co
        if z < 0:                                           # jaw narrows, chin comes forward
            x *= 1 - 0.30 * (-z) ** 1.5
            if y < 0:
                y *= 1 - 0.06 * (-z)
        if y > 0 and z > -0.2:
            y *= 1.04                                       # fuller back of the skull
        if y < -0.55:
            y = -0.55 - (-y - 0.55) * 0.80                  # a slightly flatter face plane
        if hair is None:
            nose = 0.11 * math.exp(-((x / 0.12) ** 2 + ((z + 0.05) / 0.17) ** 2)) * (1 if y < 0 else 0)
            brow = 0.035 * math.exp(-(((z - 0.22) / 0.08) ** 2)) * max(0.0, -y) * (1 - min(1.0, abs(x) / 0.6))
            chin = 0.05 * math.exp(-((x / 0.25) ** 2 + ((z + 0.82) / 0.15) ** 2)) * (1 if y < 0 else 0)
            y -= nose + brow + chin
        v.co = Vector((x * w, y * d, z * h))
    if hair:
        # a full shell over the skull that sinks 4 mm under the skin below the hairline: the visible edge is the
        # smooth intersection curve, never a stair-step of deleted faces
        bm.normal_update()
        for v in bm.verts:
            x, y, z = v.co.x / w, v.co.y / d, v.co.z / h
            line = 0.36 * max(0.0, -y) + 0.10 * (1 - abs(y)) - 0.42 * max(0.0, y)     # forehead, temples, nape
            k = min(1.0, max(0.0, (z - line + 0.05) / 0.07))
            k = k * k * (3 - 2 * k)
            if hair == 'buzz':
                t = 0.0035
            else:
                t = 0.0018 + 0.034 * min(1.0, max(0.0, (z - 0.30) / 0.45)) ** 1.4 * (0.75 + 0.25 * max(0.0, -y))
            v.co += v.normal * (t * k - 0.004 * (1 - k))
    else:
        for s in (1, -1):                                    # ears
            _ellipsoid_bm(bm, (s * w * 0.97, 0.06 * d, -0.04 * h), (0.10 * w, 0.20 * d, 0.30 * h),
                          Matrix.Rotation(math.radians(s * -12), 3, 'Z'), 16, 10)
    me = bpy.data.meshes.new('head' if not hair else 'hair')
    bm.to_mesh(me)
    bm.free()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    return me


def _catmull(P, sub):
    """Positions and parameters along a Catmull-Rom spline through P (sub samples per segment)."""
    P = [Vector(p) for p in P]
    ext = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        for k in range(sub):
            t = k / sub
            t2, t3 = t * t, t * t * t
            out.append((0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3),
                        i + t))
    out.append((P[-1], len(P) - 1.0))
    return out


def _loft_verts(P, RX, RY, lat0, n=28, sub=6, cap0=True, cap1=True, gap=None, caps=5):
    """Vertices of a smooth elliptical tube through joint positions P (radii RX/RY per joint, interpolated smoothly).
    lat0 is the lateral (x-radius) direction at the first joint, parallel-transported along the path.
    gap(param) -> half-angle (radians) of an opening centred on the 'front' (-depth) side; the tube is then an open
    sheet with no caps. Returns (verts, faces, ring_count, ring_size)."""
    smp = _catmull(P, sub)
    pts = [s[0] for s in smp]
    T = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        T.append((b - a).normalized())
    lat = Vector(lat0)
    lat = (lat - T[0] * lat.dot(T[0])).normalized()
    frames = []
    for i in range(len(pts)):
        if i:
            q = T[i - 1].rotation_difference(T[i])
            lat = (q @ lat)
            lat = (lat - T[i] * lat.dot(T[i])).normalized()
        frames.append((lat.copy(), T[i].cross(lat).normalized()))

    def rad(R, u):
        i = min(int(u), len(R) - 2)
        f = u - i
        f = f * f * (3 - 2 * f)
        return R[i] * (1 - f) + R[i + 1] * f
    rings = []
    for (p, u), (X, Y) in zip(smp, frames):
        rings.append((p, X, Y, rad(RX, u), rad(RY, u), u))
    open_ = gap is not None
    if not open_:
        def capring(r, direction, k):
            p, X, Y, rx, ry, u = r
            out = []
            for j in range(1, k + 1):
                ph = (math.pi / 2) * j / (k + 0.35)
                rr = max(rx, ry)
                out.append((p + direction * rr * 0.92 * math.sin(ph), X, Y, rx * math.cos(ph), ry * math.cos(ph), u))
            return out
        if cap0:
            rings = list(reversed(capring(rings[0], -T[0], caps))) + rings
        if cap1:
            rings = rings + capring(rings[-1], T[-1], caps)
    verts, faces = [], []
    for p, X, Y, rx, ry, u in rings:
        if open_:
            g = gap(u)
            ths = [-math.pi / 2 + g + (2 * math.pi - 2 * g) * j / (n - 1) for j in range(n)]
        else:
            ths = [-math.pi / 2 + 2 * math.pi * j / n for j in range(n)]
        for th in ths:
            verts.append(p + X * (rx * math.cos(th)) + Y * (ry * math.sin(th)))
    m = len(rings)
    for i in range(m - 1):
        for j in range(n - (1 if open_ else 0)):
            a, b = i * n + j, i * n + (j + 1) % n
            faces.append((a, b, b + n, a + n))
    if not open_:
        for end, rev in ((0, True), (m - 1, False)):
            f = [end * n + j for j in range(n)]
            faces.append(tuple(reversed(f)) if rev else tuple(f))
    return verts, faces


def _loft_obj(name, segs, JA, JB, mat, solid=None):
    """segs: list of (nodes, RX, RY, lat0, kw) lofts joined in one object; JB adds a shape key 'B'."""
    def build(J):
        V, Fc = [], []
        for nodes, RX, RY, lat0, kw in segs:
            v, f = _loft_verts([J[nn] for nn in nodes], RX, RY, lat0(J) if callable(lat0) else lat0, **kw)
            o = len(V)
            V += v
            Fc += [tuple(i + o for i in ff) for ff in f]
        return V, Fc
    V, Fc = build(JA)
    ob = _mesh_obj(name, V, Fc)
    me = ob.data
    # outward normals (the side/front sectors are built CCW seen along the tube, so check once and flip if needed)
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    if JB is not None:
        VB, _ = build(JB)
        ob.shape_key_add(name='Basis')
        kb = ob.shape_key_add(name='B')
        for i, v in enumerate(VB):
            kb.data[i].co = v
    if solid:
        s = ob.modifiers.new('sol', 'SOLIDIFY')
        s.thickness = solid
        s.offset = -1.0
    ob.data.materials.append(mat)
    return ob


def _skin(name, nodes, edges, radii, JA, JB, mat, root='pelvis', levels=2, smooth=0.5):
    idx = {n: i for i, n in enumerate(nodes)}
    me = bpy.data.meshes.new(name)
    me.from_pydata([JA[n] for n in nodes], [(idx[a], idx[b]) for a, b in edges if a in idx and b in idx], [])
    ob = _link(bpy.data.objects.new(name, me))
    sk = ob.modifiers.new('skin', 'SKIN')
    sk.use_smooth_shade = True
    sk.branch_smoothing = smooth
    for n in nodes:
        r = radii[n]
        me.skin_vertices[0].data[idx[n]].radius = (r, r) if isinstance(r, (int, float)) else r
    me.skin_vertices[0].data[idx[root]].use_root = True
    ss = ob.modifiers.new('sub', 'SUBSURF')
    ss.levels = levels
    ss.render_levels = levels
    if JB is not None:
        ob.shape_key_add(name='Basis')
        kb = ob.shape_key_add(name='B')
        for n in nodes:
            kb.data[idx[n]].co = JB[n]
    ob.data.materials.append(mat)
    return ob


def _arm_edges(side):
    s = '_' + side
    return [('chest', 'shoulder' + s), ('shoulder' + s, 'uarm' + s), ('uarm' + s, 'elbow' + s), ('elbow' + s, 'farm' + s),
            ('farm' + s, 'wrist' + s)]


def _leg_edges(side):
    s = '_' + side
    return [('pelvis', 'hip' + s), ('hip' + s, 'thigh' + s), ('thigh' + s, 'knee' + s), ('knee' + s, 'calf' + s),
            ('calf' + s, 'ankle' + s)]


def previs(body='H01', pose='a', key=None, frames=(1, 13), at=(0, 0, 0), rot_deg=0.0, phone_flash=True):
    """A neutral-grey previs mannequin for the O ANÚNCIO animatic (§F.1–F.2). Matte greys, no facial detail beyond
    the simple form (a nose and brow so the eyeline reads), mitten hands with a separate index and thumb.
    body  'H01' (a fã atrasada, ~25, 1,65 m: platinum buzz-cut silhouette, oversized cardigan open over a tee) |
          'H02' (o fã atrasado, ~23, 1,76 m: curly-top fade, oversized sweatshirt, crossbody bag).
    pose  'a' sitting on the stage edge, legs dangling, looking at camera (root = the stage's top front edge)
          'b' standing deadpan slow clap: key A hands apart, key B hands together (root = floor)
          'c' standing, right arm raised holding a phone back-to-camera, flash on (root = floor)
          'd' sitting, finger-heart (key A) then pointing at the lens (key B) (root = stage edge)
    key   None: animated between the keys (A at frames[0], B at frames[1]) for two-key poses; 'A' / 'B': static.
    The presenter never holds the pack. Returns Built(root, parts, keys)."""
    B = BODIES[body]
    Hh = B['H']
    two = pose in ('b', 'd')
    kA = 'A' if key in (None, 'A') or not two else 'B'
    JA, FA = _pose_skeleton(B, pose, kA)
    JB, FB = (None, None)
    if two and key is None:
        JB, FB = _pose_skeleton(B, pose, 'B')
    before = set(bpy.data.objects)
    mats = {k: grey_material('previs_' + k, v) for k, v in GREY.items()}
    X = Vector((1, 0, 0))
    H_ = Hh
    pr, wr_, cr = B['pelvis'], B['waist'], B['chest']
    sh = B['sh']
    a, la = B['arm'], B['leg']

    def limb(nodes, radii, k=1.0, add=0.0, **kw):
        r = [x * H_ * k + add for x in radii]
        return (nodes, r, r, (0, 0, 1), dict(n=20, sub=5, **kw))

    def arms(radii, k=1.0, add=0.0, nodes=('shoulder', 'uarm', 'elbow', 'farm', 'wrist'), **kw):
        return [limb([n + '_' + sd for n in nodes], radii, k, add, **kw) for sd in 'LR']
    torso_nodes = ['hem_s', 'pelvis', 'waist', 'chest', 'yoke', 'neck', 'neck_top']
    TX = [0.075, pr[0], wr_[0], cr[0], sh - 0.012, B['neck'], B['neck'] * 0.92]
    TY = [0.058, pr[1], wr_[1], cr[1], 0.044, B['neck'], B['neck'] * 0.92]
    parts = {}
    parts['body'] = _loft_obj('previs_body', [
        (torso_nodes, [x * H_ for x in TX], [y * H_ for y in TY], X, dict(n=32, sub=6))] + arms(a),
        JA, JB, mats['skin'])
    parts['trousers'] = _loft_obj('previs_trousers', [
        (['hem_s', 'pelvis', 'waist'], [0.080 * H_, pr[0] * 1.07 * H_, wr_[0] * 1.04 * H_],
         [0.062 * H_, pr[1] * 1.07 * H_, wr_[1] * 1.04 * H_], X, dict(n=32, sub=6))] +
        [limb(['hip_' + sd, 'thigh_' + sd, 'knee_' + sd, 'calf_' + sd, 'ankle_' + sd],
              (la[0] * 0.80,) + tuple(la[1:]), 1.10, 0.004) for sd in 'LR'],      # the thigh top merges into the pelvis
        JA, JB, mats['trousers'])
    if B['top'] == 'cardigan':
        gn = ['hem_s', 'pelvis', 'waist', 'chest', 'yoke', 'collar']
        parts['tee'] = _loft_obj('previs_tee', [
            (gn, [x * H_ * 1.06 + 0.003 for x in (0.078, pr[0], wr_[0], cr[0], sh - 0.010, B['neck'] * 1.12)],
             [y * H_ * 1.06 + 0.003 for y in (0.060, pr[1], wr_[1], cr[1], 0.048, B['neck'] * 1.12)], X,
             dict(n=32, sub=6, cap0=False, cap1=False))] +
            arms((a[0] * 1.08, a[1] * 1.15), nodes=('shoulder', 'uarm'), cap1=False), JA, JB, mats['tee'], solid=0.003)
        cn = ['hem', 'pelvis', 'waist', 'chest', 'yoke', 'collar']
        CX = [0.104, 0.104, 0.098, 0.103, sh + 0.004, 0.058]
        CY = [0.083, 0.082, 0.077, 0.081, 0.058, 0.052]

        def gap(u):                           # open front: a 1 cm placket line to the chest, then the V to the collar
            w = 0.0055 * H_ if u <= 2.4 else 0.0055 * H_ + (0.042 * H_) * ((u - 2.4) / 2.6) ** 1.2
            i = min(int(u), len(CX) - 2)
            f = u - i
            rx = (CX[i] * (1 - f) + CX[i + 1] * f) * H_
            return math.asin(min(0.97, w / rx))
        parts['cardigan'] = _loft_obj('previs_cardigan', [
            (cn, [x * H_ for x in CX], [y * H_ for y in CY], X, dict(n=40, sub=6, gap=gap))] +
            arms((0.043, 0.044, 0.039, 0.036, 0.031), cap1=False), JA, JB, mats['cardigan'], solid=0.007)
    else:
        sn = ['hem_s', 'pelvis', 'waist', 'chest', 'yoke', 'collar']      # ribbed hem gathers at the hip line
        parts['sweatshirt'] = _loft_obj('previs_sweatshirt', [
            (sn, [x * H_ for x in (0.103, 0.101, 0.099, 0.106, sh + 0.004, 0.047)],
             [y * H_ for y in (0.077, 0.076, 0.076, 0.081, 0.058, 0.045)], X,
             dict(n=36, sub=6, cap0=False, cap1=False))] +
            arms((0.042, 0.042, 0.036, 0.032, 0.023), cap1=False), JA, JB, mats['sweat'], solid=0.005)
    # head + hair
    hc, Rh = FA['head']
    head = _link(bpy.data.objects.new('previs_head', _head_mesh(B, Hh)))
    head.matrix_world = Matrix.Translation(hc) @ Rh.to_4x4()
    head.data.materials.append(mats['skin'])
    hair = _link(bpy.data.objects.new('previs_hair', _head_mesh(B, Hh, hair=B['hair'])))
    hair.matrix_world = head.matrix_world.copy()
    hair.data.materials.append(mats['hair_' + body])
    parts['head'], parts['hair'] = head, hair
    # hands (shape keys when the hand shape changes between keys), feet
    Lh = SEG['hand'] * Hh
    for s, side in ((1, 'L'), (-1, 'R')):
        wA, RA, shA = FA['hand_' + side]
        me = _parts_mesh('hand', _hand_parts(shA, s, Lh))
        hand = _link(bpy.data.objects.new('previs_hand_' + side, me))
        hand.data.materials.append(mats['skin'])
        hand.rotation_mode = 'QUATERNION'
        hand.location = wA
        hand.rotation_quaternion = RA.to_quaternion()
        if FB is not None:
            wB, RB, shB = FB['hand_' + side]
            if shB != shA:
                meB = _parts_mesh('handB', _hand_parts(shB, s, Lh))
                hand.shape_key_add(name='Basis')
                kb = hand.shape_key_add(name='B')
                for i, v in enumerate(meB.vertices):
                    kb.data[i].co = v.co
                bpy.data.meshes.remove(meB)
                kb.value = 0.0
                kb.keyframe_insert('value', frame=frames[0])
                kb.value = 1.0
                kb.keyframe_insert('value', frame=frames[1])
                kb.value = 0.0
            hand.keyframe_insert('location', frame=frames[0])
            hand.keyframe_insert('rotation_quaternion', frame=frames[0])
            hand.location = wB
            q = RB.to_quaternion()
            if q.dot(hand.rotation_quaternion) < 0:
                q.negate()
            hand.rotation_quaternion = q
            hand.keyframe_insert('location', frame=frames[1])
            hand.keyframe_insert('rotation_quaternion', frame=frames[1])
        parts['hand_' + side] = hand
        an, Rf = FA['foot_' + side]
        Lf, ha = SEG['foot'] * Hh, SEG['ankle'] * Hh
        foot = _link(bpy.data.objects.new('previs_foot_' + side, _parts_mesh('foot', [
            (Vector((0, 0.30 * Lf, -0.55 * ha)), Vector((0, 1, 0)), (0.20 * Lf, 0.56 * Lf, 0.52 * ha + 0.012)),
            (Vector((0, -0.05 * Lf, -0.25 * ha)), Vector((0, 1, 0)), (0.17 * Lf, 0.22 * Lf, 0.70 * ha + 0.01))], 24, 14)))
        foot.matrix_world = Matrix.Translation(an) @ Rf.to_4x4()
        foot.data.materials.append(mats['shoes'])
        parts['foot_' + side] = foot
    # shape-key animation of the skin graphs
    if JB is not None:
        for k in ('body', 'trousers', 'tee', 'cardigan', 'sweatshirt'):
            ob = parts.get(k)
            if ob is not None and ob.data.shape_keys:  # noqa
                kb = ob.data.shape_keys.key_blocks['B']
                kb.value = 0.0
                kb.keyframe_insert('value', frame=frames[0])
                kb.value = 1.0
                kb.keyframe_insert('value', frame=frames[1])
                kb.value = 0.0
        bpy.context.scene.frame_set(frames[0])
    # props
    if pose == 'c':
        wR, RR, _ = FA['hand_R']
        ph_ = _cuboid('previs_phone', -36, 36, -4, 4, 0, 150)
        _bevel(ph_, 5.0, 3, 30)
        ph_.data.materials.append(mats['phone'])
        ph_.parent = parts['hand_R']
        ph_.matrix_parent_inverse = Matrix.Identity(4)
        ph_.location = (0.0, 0.03, -0.022)                     # hand-local: up the fingers, on the palm side
        ph_.rotation_mode = 'XYZ'
        ph_.rotation_euler = (math.radians(-90), 0, 0)
        if phone_flash:
            fl = _cylinder('previs_flash', 0, 0, 3.0, 0, 0.6, 24)
            em = bpy.data.materials.new('flash')
            em.use_nodes = True
            nt = em.node_tree
            nt.nodes.clear()
            o = nt.nodes.new('ShaderNodeOutputMaterial')
            e = nt.nodes.new('ShaderNodeEmission')
            e.inputs[0].default_value = (1.0, 0.97, 0.9, 1)
            e.inputs[1].default_value = 400.0
            nt.links.new(e.outputs[0], o.inputs[0])
            fl.data.materials.append(em)
            fl.parent = ph_
            fl.matrix_parent_inverse = Matrix.Identity(4)
            fl.location = (0.022, -0.0045, 0.135)
            fl.rotation_euler = (math.radians(90), 0, 0)
        parts['phone'] = ph_
    if B['bag']:
        ch, Rc, Rw = FA['torso']
        dz = B['chest'][1] * Hh * 1.15
        bag_c = ch + Rc @ Vector((-0.035, -(dz + 0.034), -0.045 * Hh))
        bag = _cuboid('previs_bag', -115, 115, -32, 32, -55, 55)
        _bevel(bag, 26.0, 5, 30)
        bag.matrix_world = Matrix.Translation(bag_c) @ (Rc @ Matrix.Rotation(math.radians(-24), 3, 'Y')).to_4x4()
        bag.data.materials.append(mats['bag'])
        pts = [(-0.085, -(dz + 0.03), 0.02), (0.06, -(dz - 0.005), 0.10), (0.115, -0.03, 0.150), (0.105, 0.06, 0.13),
               (0.03, dz + 0.012, 0.03), (-0.08, dz - 0.01, -0.07), (-0.145, 0.03, -0.10), (-0.13, -(dz - 0.0), -0.09),
               (-0.095, -(dz + 0.03), -0.075)]
        cu = bpy.data.curves.new('strap', 'CURVE')
        cu.dimensions = '3D'
        cu.bevel_depth = 0.006
        cu.bevel_resolution = 2
        sp = cu.splines.new('NURBS')
        sp.points.add(len(pts) - 1)
        for i, q in enumerate(pts):
            w = ch + Rc @ Vector(q)
            sp.points[i].co = (w.x, w.y, w.z, 1.0)
        sp.use_endpoint_u = True
        sp.order_u = 4
        strap = _link(bpy.data.objects.new('previs_strap', cu))
        strap.data.materials.append(mats['bag'])
        parts['bag'], parts['strap'] = bag, strap
    root = _finish('previs_%s_%s_root' % (body, pose), before, at, rot_deg)
    return Built(root=root, parts=parts, keys=('A', 'B') if two else ('A',), frames=frames, body=body, pose=pose)


def previs_stage(width=2.6, depth=1.4, height=0.55, at=(0, 0, 0), hexcol='#6E6A64'):
    """A plain grey low stage for the previs: its top front edge runs along X through `at` (the sitting poses' root)."""
    before = set(bpy.data.objects)
    st = _cuboid('previs_stage', -width / 2 / MM, width / 2 / MM, 0, depth / MM, -height / MM, 0)
    st.data.materials.append(grey_material('previs_stage', hexcol, 0.7))
    root = _finish('previs_stage_root', before, at)
    return Built(root=root, stage=st)
