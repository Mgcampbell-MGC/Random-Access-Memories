"""HOLOFOTE · props for the sets (code-modelled, no downloaded assets).

    monobloco()   the white Brazilian bar chair (one-piece PP armchair): seat with skirt, slotted wrap-around back,
                  arm/top-rail loop, splayed channel legs. Returns one mesh object (modifiers applied) to instance.
    bolsa()       a woman's leather tote handbag
    flor_papel()  a crepe-paper flower (two rings of cupped petals + a crumpled centre)
    coracao()     a cut-paper heart
    calha()       a surface fluorescent fitting with two T8 tubes (OFF)
All objects: metres, Z up, origin at the floor contact, front toward +Y unless stated.
"""
import math
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix
from candle_lib import srgb, material


def _link(ob, coll):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def _bm_to_obj(name, bm, coll=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _link(bpy.data.objects.new(name, me), coll)


def _apply(ob, name=None):
    """Bake an object's modifiers into a new mesh datablock on the same object."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if name:
        me.name = name
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def _join(objs, name, coll=None):
    """Join objects (modifiers applied) into one new mesh object."""
    bm = bmesh.new()
    dg = bpy.context.evaluated_depsgraph_get()
    mats = []
    for o in objs:
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        me.transform(o.matrix_world)
        off = len(mats)
        for m in me.materials:
            mats.append(m)
        tmp = bmesh.new()
        tmp.from_mesh(me)
        for f in tmp.faces:
            f.material_index += off
        me2 = bpy.data.meshes.new('_t')
        tmp.to_mesh(me2)
        tmp.free()
        bm.from_mesh(me2)
        bpy.data.meshes.remove(me2)
        bpy.data.meshes.remove(me)
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    ob = _bm_to_obj(name, bm, coll)
    for m in mats:
        ob.data.materials.append(m)
    return ob


def catmull(points, n=8, closed=False):
    """Dense Catmull-Rom path through control points."""
    P = [Vector(p) for p in points]
    out = []
    m = len(P)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = P[(i - 1) % m] if closed else P[max(i - 1, 0)]
        p1, p2 = P[i], P[(i + 1) % m]
        p3 = P[(i + 2) % m] if closed else P[min(i + 2, m - 1)]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                              (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(P[-1])
    return out


def rrect(w, h, r, n=4):
    """Rounded-rectangle profile (closed, CCW)."""
    r = min(r, w / 2 - 1e-5, h / 2 - 1e-5)
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180),
                       (w / 2 - r, -h / 2 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sweep(bm, path, profile, ups, scales=None, caps=True):
    """Sweep a closed 2D profile along a path. ups: one up-hint per path point (the profile's +y);
    scales: optional (sx, sy) per point."""
    rings = []
    n = len(path)
    for i, p in enumerate(path):
        t = (path[min(i + 1, n - 1)] - path[max(i - 1, 0)]).normalized()
        up = Vector(ups[i])
        x = up.cross(t)
        if x.length < 1e-6:
            x = Vector((1, 0, 0)).cross(t)
        x.normalize()
        y = t.cross(x).normalized()
        sx, sy = scales[i] if scales else (1, 1)
        rings.append([bm.verts.new(p + x * (px * sx) + y * (py * sy)) for px, py in profile])
    k = len(profile)
    for i in range(n - 1):
        a, b = rings[i], rings[i + 1]
        for j in range(k):
            bm.faces.new((a[j], a[(j + 1) % k], b[(j + 1) % k], b[j]))
    if caps:
        bm.faces.new(rings[0][::-1])
        bm.faces.new(rings[-1])
    return rings


def _lerp_ups(keys, n):
    """Interpolate up-hints given as [(fraction, vector)] over n points."""
    out = []
    for i in range(n):
        f = i / max(n - 1, 1)
        for (fa, va), (fb, vb) in zip(keys, keys[1:]):
            if fa <= f <= fb:
                t = (f - fa) / max(fb - fa, 1e-9)
                out.append(Vector(va).lerp(Vector(vb), t).normalized())
                break
        else:
            out.append(Vector(keys[-1][1]).normalized())
    return out


# ------------------------------------------------------------------------------------------------ materials
def plastico_branco(name='PP_branco'):
    """White injection-moulded polypropylene, a little worn: grey grime at the feet, scuffs, a faint sheen."""
    m = material(name, **{'Base Color': srgb('#EEEDE8'), 'Roughness': 0.38, 'Specular IOR Level': 0.5,
                          'Subsurface Weight': 0.08, 'Subsurface Radius': (0.004, 0.004, 0.004), 'Subsurface Scale': 1.0})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    feet = nt.nodes.new('ShaderNodeMapRange')
    feet.inputs['From Min'].default_value = 0.12
    feet.inputs['From Max'].default_value = 0.0
    nt.links.new(sep.outputs['Z'], feet.inputs['Value'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 18.0
    nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    grime = nt.nodes.new('ShaderNodeMath')
    grime.operation = 'MULTIPLY'
    nt.links.new(feet.outputs['Result'], grime.inputs[0])
    nt.links.new(nz.outputs['Fac'], grime.inputs[1])
    g2 = nt.nodes.new('ShaderNodeMapRange')
    g2.inputs['From Min'].default_value = 0.45
    g2.inputs['From Max'].default_value = 0.8
    g2.inputs['To Max'].default_value = 0.35
    nt.links.new(nz.outputs['Fac'], g2.inputs['Value'])
    add = nt.nodes.new('ShaderNodeMath')
    add.operation = 'ADD'
    add.use_clamp = True
    nt.links.new(grime.outputs[0], add.inputs[0])
    nt.links.new(g2.outputs['Result'], add.inputs[1])
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = srgb('#EEEDE8')
    mix.inputs['B'].default_value = srgb('#A8A49A')
    nt.links.new(add.outputs[0], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], bs.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange')
    rr.inputs['To Min'].default_value = 0.30
    rr.inputs['To Max'].default_value = 0.55
    nt.links.new(add.outputs[0], rr.inputs['Value'])
    nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
    return m


# ------------------------------------------------------------------------------------------------ the monobloc
def monobloco(name='monobloco', coll=None, mat=None):
    """The iconic Brazilian white plastic bar armchair. Front toward +Y. ~W 0,56 x D 0,54 x H 0,79 m, seat 0,43 m."""
    parts = []
    T = 0.0042                                   # wall thickness
    # --- seat: rounded-rect dish with a skirt (front waterfall deeper)
    a, b, rc = 0.246, 0.215, 0.075
    nx, ny = 30, 28
    bm = bmesh.new()
    grid = []
    for j in range(ny + 1):
        row = []
        for i in range(nx + 1):
            u, v = -1 + 2 * i / nx, -1 + 2 * j / ny
            # square -> rounded rect: corner zones mapped onto quarter discs
            x, y = u * a, v * b
            cx, cy = a - rc, b - rc
            dx, dy = abs(x) - cx, abs(y) - cy
            if dx > 0 and dy > 0:
                s, t = dx / rc, dy / rc
                mx = s * math.sqrt(max(0.0, 1 - t * t / 2))
                my = t * math.sqrt(max(0.0, 1 - s * s / 2))
                x = math.copysign(cx + mx * rc, x)
                y = math.copysign(cy + my * rc, y)
            z = 0.430 - 0.010 * (1 - u * u) * (1 - (0.8 * v) ** 2)     # dish
            if v > 0.82:                                               # front waterfall
                z -= 0.012 * ((v - 0.82) / 0.18) ** 2
            if v < -0.85:                                              # rises into the back
                z += 0.010 * ((-v - 0.85) / 0.15) ** 2
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    # skirt: extrude the boundary down, deeper at the front
    edges = [e for e in bm.edges if e.is_boundary]
    ret = bmesh.ops.extrude_edge_only(bm, edges=edges)
    for v in [g for g in ret['geom'] if isinstance(g, bmesh.types.BMVert)]:
        depth = 0.026 + 0.022 * max(0.0, v.co.y / b)
        v.co.z -= depth
        v.co.x *= 0.985
        v.co.y = v.co.y * 0.985 - 0.002
    seat = _bm_to_obj(name + '_assento', bm, coll)
    s = seat.modifiers.new('esp', 'SOLIDIFY')
    s.thickness = T
    s.offset = -1
    sd = seat.modifiers.new('sub', 'SUBSURF')
    sd.levels = sd.render_levels = 1
    parts.append(seat)
    # --- backrest: curved, reclined panel with four horizontal slots
    bm = bmesh.new()
    nu, nv = 44, 64
    H0, Hh, W = 0.432, 0.345, 0.420
    slots = [(0.075, 0.098), (0.132, 0.155), (0.189, 0.212), (0.246, 0.269)]
    grid = []
    for j in range(nv + 1):
        row = []
        v = Hh * j / nv
        for i in range(nu + 1):
            u = -W / 2 + W * i / nu
            y = -0.205 - math.tan(math.radians(13)) * v + 0.55 * u * u
            row.append(bm.verts.new((u, y, H0 + v)))
        grid.append(row)
    for j in range(nv):
        for i in range(nu):
            uc = -W / 2 + W * (i + 0.5) / nu
            vc = Hh * (j + 0.5) / nv
            if any(lo < vc < hi for lo, hi in slots) and abs(uc) < 0.150:
                continue
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    back = _bm_to_obj(name + '_encosto', bm, coll)
    s = back.modifiers.new('esp', 'SOLIDIFY')
    s.thickness = 0.0055
    s.offset = 0
    bv = back.modifiers.new('bev', 'BEVEL')
    bv.width = 0.0018
    bv.segments = 2
    bv.limit_method = 'ANGLE'
    parts.append(back)
    # --- the loop: left front foot -> up the leg -> along the arm -> round the back top -> down the right leg.
    # On the real chair the front legs, arms and top rail are one continuous moulded channel.
    side = [(-0.284, 0.238, 0.000), (-0.276, 0.214, 0.200), (-0.270, 0.196, 0.420), (-0.268, 0.188, 0.560),
            (-0.270, 0.160, 0.612), (-0.272, 0.080, 0.622), (-0.268, -0.060, 0.628), (-0.258, -0.180, 0.650),
            (-0.240, -0.248, 0.705), (-0.205, -0.276, 0.758), (-0.130, -0.290, 0.786), (0.0, -0.297, 0.795)]
    ctrl = side + [(-x, y, z) for x, y, z in reversed(side[:-1])]
    path = catmull(ctrl, n=8)
    N = len(path)
    ups = _lerp_ups([(0.0, (0, 1, 0)), (0.13, (0, 1, 0.2)), (0.19, (0, 0.2, 1)), (0.30, (0, 0.1, 1)),
                     (0.40, (0, 1, 0.5)), (0.5, (0, 1, 0.25)), (0.60, (0, 1, 0.5)), (0.70, (0, 0.1, 1)),
                     (0.81, (0, 0.2, 1)), (0.87, (0, 1, 0.2)), (1.0, (0, 1, 0))], N)
    sc = []
    for i in range(N):
        f = abs(i / (N - 1) - 0.5) * 2             # 1 at the feet, 0 at the top centre
        if f > 0.74:                                # leg: wide channel, tapering to the foot
            t = (f - 0.74) / 0.26
            sc.append((1.18 - 0.30 * t + 0.10 * max(0.0, t - 0.92) / 0.08, 1.35 - 0.25 * t))
        elif f > 0.36:                              # arm pad
            sc.append((1.06, 1.0))
        else:                                       # top rail
            sc.append((0.88, 1.15))
    bm = bmesh.new()
    sweep(bm, path, rrect(0.052, 0.022, 0.0095), ups, sc)
    loop = _bm_to_obj(name + '_bracos', bm, coll)
    sd = loop.modifiers.new('sub', 'SUBSURF')
    sd.levels = sd.render_levels = 1
    parts.append(loop)
    # --- back legs: wide channels from the seat's rear corners, splayed back and out
    for sx in (-1, 1):
        top, foot = Vector((sx * 0.222, -0.185, 0.430)), Vector((sx * 0.268, -0.305, 0.0))
        mid = top.lerp(foot, 0.5) + Vector((sx * 0.006, -0.004, 0))
        path = catmull([top, mid, foot], n=8)
        n = len(path)
        scl = [(1.15 - 0.25 * i / (n - 1), 1.30 - 0.25 * i / (n - 1)) for i in range(n)]
        bm = bmesh.new()
        sweep(bm, path, rrect(0.052, 0.024, 0.0095), [Vector((0, -1, 0))] * n, scl)
        leg = _bm_to_obj(name + '_perna', bm, coll)
        sd = leg.modifiers.new('sub', 'SUBSURF')
        sd.levels = sd.render_levels = 1
        parts.append(leg)
    # --- under-seat stiffening rails (seen from low cameras): front-to-back channels joining the legs
    for sx in (-1, 1):
        bm = bmesh.new()
        path = catmull([(sx * 0.215, 0.18, 0.392), (sx * 0.212, 0.0, 0.388), (sx * 0.205, -0.17, 0.395)], n=6)
        sweep(bm, path, rrect(0.012, 0.030, 0.004), [Vector((0, 0, 1))] * len(path))
        parts.append(_bm_to_obj(name + '_trilho', bm, coll))
    ob = _join(parts, name, coll)
    ob.data.materials.clear()
    ob.data.materials.append(mat or plastico_branco())
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    try:
        bpy.context.view_layer.objects.active = ob
        ob.data.set_sharp_from_angle(angle=math.radians(50))
    except Exception:
        pass
    ob['assento_z'] = 0.432
    return ob


# ------------------------------------------------------------------------------------------------ the handbag
def couro(hexc='#5A3A28', name='couro'):
    m = material(name, **{'Base Color': srgb(hexc), 'Roughness': 0.42, 'Specular IOR Level': 0.45,
                          'Coat Weight': 0.25, 'Coat Roughness': 0.35})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi')
    vo.inputs['Scale'].default_value = 900.0
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.25
    bump.inputs['Distance'].default_value = 0.0002
    nt.links.new(vo.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 6.0
    nz.inputs['Detail'].default_value = 2.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = srgb(hexc)
    mix.inputs['B'].default_value = srgb('#6A4630')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = 0.35
    mr.inputs['From Max'].default_value = 0.75
    mr.inputs['To Max'].default_value = 0.5
    nt.links.new(nz.outputs['Fac'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], bs.inputs['Base Color'])
    return m


def bolsa(name='bolsa', coll=None, hexc='#5A3A28'):
    """A medium leather tote, standing, a little slumped. Origin at the bottom centre, front toward +Y."""
    bm = bmesh.new()
    W0, W1, D0, D1, Hh = 0.330, 0.290, 0.130, 0.085, 0.250
    nx, ny, nz = 12, 6, 10
    verts = {}
    res = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=6, use_grid_fill=True)
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z + 0.5        # z 0..1
        w = W0 + (W1 - W0) * z
        d = D0 + (D1 - D0) * z
        sag = 0.012 * math.sin(math.pi * (x + 0.5)) * z * z    # the top slumps inward at the middle
        v.co = Vector((x * w, y * d * (1 - 0.25 * z * z) - 0 * sag, z * Hh - sag * 2.0))
    body = _bm_to_obj(name + '_corpo', bm)
    sd = body.modifiers.new('sub', 'SUBSURF')
    sd.levels = sd.render_levels = 2
    parts = [body]
    for sy in (-1, 1):                       # two handles
        bm = bmesh.new()
        ctrl = [(-0.085, sy * 0.030, Hh - 0.012), (-0.080, sy * 0.034, Hh + 0.085), (0.0, sy * 0.036, Hh + 0.128),
                (0.080, sy * 0.034, Hh + 0.085), (0.085, sy * 0.030, Hh - 0.012)]
        path = catmull(ctrl, n=8)
        sweep(bm, path, rrect(0.016, 0.006, 0.0028), [Vector((0, sy, 0))] * len(path))
        h = _bm_to_obj(name + '_alca', bm)
        parts.append(h)
    ob = _join(parts, name, coll)
    ob.data.materials.append(couro(hexc))
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    ob['inflamavel'] = True
    return ob


# ------------------------------------------------------------------------------------------------ paper decor
def papel(hexc, name=None, translucent=0.25):
    m = bpy.data.materials.new(name or 'papel_' + hexc)
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = srgb(hexc)
    bs.inputs['Roughness'].default_value = 0.85
    bs.inputs['Specular IOR Level'].default_value = 0.2
    tl = nt.nodes.new('ShaderNodeBsdfTranslucent')
    tl.inputs['Color'].default_value = srgb(hexc)
    mix = nt.nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = translucent
    out = nt.nodes['Material Output']
    nt.links.new(bs.outputs[0], mix.inputs[1])
    nt.links.new(tl.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def flor_papel(radius=0.08, petals=8, rings=2, colors=('#E98AA8', '#F6C6D3'), center='#F2D44A', seed=0, coll=None,
               name='flor'):
    """Crepe-paper flower facing +Y (stuck flat on a backdrop). Origin at the back centre."""
    rng = np.random.default_rng(seed)
    mats = [papel(c) for c in colors] + [papel(center, translucent=0.1)]
    bm = bmesh.new()
    for r in range(rings):
        R = radius * (1.0 - 0.33 * r)
        np_ = petals - 2 * r
        off = rng.uniform(0, math.pi)
        for k in range(np_):
            ang = off + 2 * math.pi * k / np_ + rng.normal(0, 0.06)
            L, Wd = R * rng.uniform(0.9, 1.05), R * 0.62 * rng.uniform(0.9, 1.1)
            nu, nv = 6, 5
            vs = []
            for i in range(nu + 1):
                t = i / nu
                row = []
                for j in range(nv + 1):
                    s = -1 + 2 * j / nv
                    w = Wd * 0.5 * math.sin(math.pi * min(1.0, t * 1.1)) ** 0.8 * (1 - 0.15 * t)
                    px = t * L
                    py = s * w
                    cup = 0.25 * R * (s * s) * t + 0.18 * R * t * t + r * 0.012 + 0.004 * math.sin(7 * s + k)
                    crinkle = 0.0015 * math.sin(40 * t + 13 * s + k)
                    x = px * math.cos(ang) - py * math.sin(ang)
                    z = px * math.sin(ang) + py * math.cos(ang)
                    row.append(bm.verts.new((x, cup + crinkle, z)))
                vs.append(row)
            for i in range(nu):
                for j in range(nv):
                    f = bm.faces.new((vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]))
                    f.material_index = r % len(colors)
    c = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=radius * 0.22)
    for v in c['verts']:
        v.co.y += radius * 0.30 + rng.normal(0, radius * 0.02)
        v.co *= 1.0 + rng.normal(0, 0.08)
    for f in bm.faces:
        if all(v in c['verts'] for v in f.verts):
            f.material_index = len(colors)
    ob = _bm_to_obj(name, bm, coll)
    for m in mats:
        ob.data.materials.append(m)
    sol = ob.modifiers.new('esp', 'SOLIDIFY')
    sol.thickness = 0.0006
    ob['inflamavel'] = True
    return ob


def coracao(size=0.18, hexc='#D23A55', curl=0.02, coll=None, name='coracao', seed=0):
    """A cut-paper heart in the XZ plane facing +Y, slightly curled; origin at its centre."""
    rng = np.random.default_rng(seed)
    pts = []
    n = 72
    for k in range(n):
        t = 2 * math.pi * k / n
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 34 * size + rng.normal(0, size * 0.002), y / 34 * size + rng.normal(0, size * 0.002)))
    bm = bmesh.new()
    vs = [bm.verts.new((x, curl * (x / size) ** 2 * 4, z)) for x, z in pts]
    f = bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=[f])
    ob = _bm_to_obj(name, bm, coll)
    ob.data.materials.append(papel(hexc, translucent=0.15))
    sol = ob.modifiers.new('esp', 'SOLIDIFY')
    sol.thickness = 0.0008
    ob['inflamavel'] = True
    return ob


# ------------------------------------------------------------------------------------------------ fluorescent fitting
def calha(coll=None, name='calha', length=1.25):
    """Surface-mounted 2 x T8 fitting, tubes OFF. Origin at the top centre (ceiling contact), long axis X."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * length, v.co.y * 0.16, (v.co.z - 0.5) * 0.045))
    body = _bm_to_obj(name + '_corpo', bm)
    bv = body.modifiers.new('bev', 'BEVEL')
    bv.width = 0.004
    bv.segments = 2
    body.data.materials.append(material('chapa_branca', **{'Base Color': srgb('#E6E3DA'), 'Roughness': 0.35}))
    tubes = []
    for sy in (-0.040, 0.040):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.013, radius2=0.013, depth=length - 0.06,
                              matrix=Matrix.Rotation(math.pi / 2, 4, 'Y'))
        for v in bm.verts:
            v.co += Vector((0, sy, -0.062))
        t = _bm_to_obj(name + '_tubo', bm)
        t.data.materials.append(material('tubo_apagado', **{'Base Color': srgb('#E9E8E3'), 'Roughness': 0.25,
                                                            'Transmission Weight': 0.15, 'Specular IOR Level': 0.5}))
        tubes.append(t)
    for sx in (-1, 1):                    # lamp holders
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((sx * (length / 2 - 0.02) + v.co.x * 0.025, v.co.y * 0.13, -0.045 + (v.co.z - 0.5) * 0.04))
        hld = _bm_to_obj(name + '_soquete', bm)
        hld.data.materials.append(body.data.materials[0])
        tubes.append(hld)
    ob = _join([body] + tubes, name, coll)
    ob.data.polygons.foreach_set('use_smooth', [True] * len(ob.data.polygons))
    return ob
