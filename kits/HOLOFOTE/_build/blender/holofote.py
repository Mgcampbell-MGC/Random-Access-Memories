"""HOLOFOTE · O COPO DO SHOW (platform §C.1, §C.5, §D.6) as an exact Blender model.

Units: millimetres in the specs, metres in Blender (MM = 0.001). The candle stands on z = 0 with its front panel
facing the camera at -Y. Every printed letter comes from the 2D master PNG through UV mapping, never from a
generator: the wrap follows the shared contract in _build/PRODUCTION_BRIEF.md (9552 x 2560 px, 40 px/mm, u = 0.25 is
the front panel centre, u = 0.75 the back, the seam sits in the empty left gap).

    import holofote as H
    root = H.copo(dict(faixa='02', wrap='.../HLF-02_ROTULO_wrap.png', lit=True), at=(0, 0, 0))

Spec keys (all optional):
  faixa       '01'..'04' (sets coating colour and ink)       coating   hex override
  wrap        path to the 9552x2560 transparent ink master  (None = unprinted glass)
  lit         bool: flame + melt pool + charred wick          burnt     bool: charred wick, no flame
  flame_scale float (film flicker drives this)                 flame_seed float (noise phase for films)
  lid         None | 'on' | 'stage' (the candle stands on the lid on the floor) — loose lids use tampa()
  lid_art     path to the lid top print (3600 x 3600 px, transparent, Ø90 mm disc)
  base_relief path to a 16-bit height map of the Ø62 base panel (PRECISAVA.)
  base_sticker path to the lot sticker art (40 x 12 mm)
  fingerprint (angle_deg, z_mm) | None — one print on the gloss, the anti-slop budget
  chroma      bool: the whole pack in flat chroma blue (stand-in for generated scenes)
  aov         bool: also write label AOVs (label colour and label UV) for the fidelity check
"""
import bpy, bmesh, math, os
from mathutils import Vector
from candle_lib import MM, srgb, material, chroma_material

FAIXAS = {
    '01': dict(name='CAMARIM', coat='#FF4FA0', ink='#121014'),
    '02': dict(name='AO VIVO', coat='#FFE81A', ink='#121014'),
    '03': dict(name='MAIS UM!', coat='#FF6A1A', ink='#121014'),
    '04': dict(name='ACÚSTICO', coat='#8424F5', ink='#FFF8EC'),
}
PRETO = '#121014'
CERA = '#F3E9D6'

# vessel dimensions (mm)
R_OUT, WALL, H_GLASS, BASE = 38.0, 3.5, 88.0, 12.0
R_IN = R_OUT - WALL
RIM_R = WALL / 2                     # full round rim
CHAMFER = 1.5
PANEL_R, PANEL_D = 31.0, 1.0         # recessed base panel
COAT_T = 0.08                        # coating thickness
COAT_TOP = 87.0                      # coating stops 1,0 mm below the rim
PRINT_Z0, PRINT_Z1 = 18.0, 82.0
PRINT_PROUD = 0.05
CAP_R, CAP_H, CAP_T, CAP_LIP = 34.0, 74.0, 0.3, 1.2
WAX_TOP = 76.0
WICK_PROUD = 5.0
WICK_W, WICK_T = 12.7, 0.7
FLAME_W, FLAME_D, FLAME_H = 16.0, 7.0, 14.0
LID_R, GASKET_RO, GASKET_RI, LIP_RO = 45.0, 38.0, 33.0, 34.4

# O COPO DO SHOW (200 g, §C.1) and O SINGLE (80 g, §C.9b). The SINGLE is re-set, never scaled.
SIZES = {
    '200': dict(R_OUT=38.0, WALL=3.5, H_GLASS=88.0, BASE=12.0, PANEL_R=31.0, PRINT_Z0=18.0, PRINT_Z1=82.0,
                CAP_R=34.0, CAP_H=74.0, WAX_TOP=76.0, WICK_PROUD=5.0, WICK_W=12.7, WICK_T=0.7,
                FLAME_W=16.0, FLAME_D=7.0, FLAME_H=14.0, LID_R=45.0, GASKET_RO=38.0, GASKET_RI=33.0, LIP_RO=34.4),
    '080': dict(R_OUT=29.0, WALL=3.0, H_GLASS=66.0, BASE=9.0, PANEL_R=23.0, PRINT_Z0=14.0, PRINT_Z1=63.0,
                CAP_R=25.5, CAP_H=55.0, WAX_TOP=54.9, WICK_PROUD=4.0, WICK_W=9.5, WICK_T=0.6,
                FLAME_W=12.0, FLAME_D=5.5, FLAME_H=11.5, LID_R=35.0, GASKET_RO=29.0, GASKET_RI=25.0, LIP_RO=25.9),
}


def use_size(size='200'):
    """Rebind the module's dimensions to one vessel size before building it."""
    g = globals()
    g.update(SIZES[size])
    g['R_IN'] = g['R_OUT'] - g['WALL']
    g['RIM_R'] = g['WALL'] / 2
    g['COAT_TOP'] = g['H_GLASS'] - 1.0


# ----------------------------------------------------------------------------------------------- geometry helpers
def _arc(cx, cz, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cz + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _dedupe(pts, eps=1e-6):
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > eps or abs(out[-1][1] - p[1]) > eps:
            out.append(p)
    return out


def lathe(name, profile_mm, segs=256, smooth_angle=35.0):
    """Revolve an (r, z) mm polyline round Z. Points on the axis are welded."""
    prof = _dedupe(profile_mm)
    bm = bmesh.new()
    vs = [bm.verts.new((r * MM, 0.0, z * MM)) for r, z in prof]
    es = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=segs,
                   use_duplicate=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(smooth_angle))
    return ob


def glass_profile():
    """Outer surface from the base centre up and over the rim, then the inner surface down to the floor centre."""
    p = [(0.0, PANEL_D)]
    p += [(PANEL_R - 0.4, PANEL_D)] + _arc(PANEL_R - 0.4, PANEL_D - 0.4, 0.4, math.pi / 2, 0, 3)  # panel edge fillet
    p += [(PANEL_R, 0.2)] + _arc(PANEL_R + 0.2, 0.2, 0.2, math.pi, 1.5 * math.pi, 3)
    p += [(R_OUT - CHAMFER - 0.15, 0.0), (R_OUT - CHAMFER + 0.05, 0.02)]
    p += [(R_OUT - 0.02, CHAMFER - 0.05), (R_OUT, CHAMFER + 0.15), (R_OUT, CHAMFER + 0.6)]
    p += [(R_OUT, H_GLASS - RIM_R - 0.6)]
    p += _arc(R_OUT - RIM_R, H_GLASS - RIM_R, RIM_R, 0, math.pi, 24)             # full round rim
    p += [(R_IN, H_GLASS - RIM_R - 0.6), (R_IN, BASE + 1.2)]
    p += _arc(R_IN - 1.0, BASE + 1.0, 1.0, 0, -math.pi / 2, 6)                    # inner floor fillet
    p += [(R_IN - 1.6, BASE), (0.0, BASE)]
    return p


def coating_profile():
    """The coating follows the outer glass surface, COAT_T proud, from the base centre to COAT_TOP on the rim round."""
    out = []
    g = glass_profile()
    # walk the outer part only: until the rim round passes COAT_TOP
    for i in range(len(g) - 1):
        r, z = g[i]
        r2, z2 = g[i + 1]
        if z > COAT_TOP and r < R_OUT - 0.01:
            break
        out.append((r, z))
        if r2 < r and z2 > COAT_TOP - 1:  # reached the top of the round
            break
    # offset outward along the polyline normal
    res = []
    for i, (r, z) in enumerate(out):
        a = out[max(0, i - 1)]
        b = out[min(len(out) - 1, i + 1)]
        tr, tz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tr, tz) or 1.0
        nr, nz = tz / L, -tr / L          # outward for a polyline walked base -> up
        res.append((max(0.0, r + nr * COAT_T) if r > 0 else 0.0, z + nz * COAT_T))
    res[0] = (0.0, PANEL_D - COAT_T)
    # stop exactly at COAT_TOP with a tiny thickness edge (paint edge)
    last = res[-1]
    res.append((last[0] - COAT_T, last[1]))
    return res


def capsule_profile():
    """Deep-drawn aluminium cup: outside up, rolled lip, inside down. Sits on the glass floor."""
    z0 = BASE
    lip_r = CAP_LIP / 2
    top = z0 + CAP_H                               # 86,0 mm
    p = [(0.0, z0), (CAP_R - 1.2, z0)] + _arc(CAP_R - 1.2, z0 + 1.2, 1.2, -math.pi / 2, 0, 6)
    p += [(CAP_R, top - CAP_LIP)]
    p += _arc(CAP_R - lip_r + 0.3, top - lip_r, lip_r, -math.pi / 2, math.pi, 14)   # rolled lip, outward roll
    p += [(CAP_R - CAP_T, top - CAP_LIP - 0.3), (CAP_R - CAP_T, z0 + CAP_T + 1.2)]
    p += _arc(CAP_R - CAP_T - 0.9, z0 + CAP_T + 0.9, 0.9, 0, -math.pi / 2, 5)
    p += [(0.0, z0 + CAP_T)]
    return p


def wax_profile(lit=False, pool_r=18.0, pool_depth=0.0):
    """Wax top: 0,8 mm concave toward the wick, a 2 mm memory ring climbing the capsule wall."""
    z0 = BASE + CAP_T
    Rw = CAP_R - CAP_T - 0.02
    p = [(0.0, z0), (Rw, z0), (Rw, WAX_TOP + 0.35)]
    # memory ring: wax climbs 0,35 mm on the wall over 2 mm
    p += [(Rw - 0.4, WAX_TOP + 0.2), (Rw - 1.0, WAX_TOP + 0.06), (Rw - 2.0, WAX_TOP)]
    n = 24
    for i in range(1, n + 1):
        r = (Rw - 2.0) * (1 - i / n)
        t = r / (Rw - 2.0)
        z = WAX_TOP - 0.8 * (1 - t * t)          # parabolic dish, -0,8 at the centre
        if lit and r < pool_r:
            z -= pool_depth * (1 - (r / pool_r) ** 4)
        p.append((r, z))
    return p


# ----------------------------------------------------------------------------------------------- materials
def coating_material(hexcol, fingerprint=None, relief=None):
    m = material('coating', **{'Base Color': srgb(hexcol), 'Roughness': 0.10, 'Coat Weight': 1.0,
                               'Coat Roughness': 0.03, 'Specular IOR Level': 0.5, 'Emission Strength': 0.0})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # orange peel: 0,4 mm noise, strength 0,04
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1 / (0.4 * MM)
    nz.inputs['Detail'].default_value = 2.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.04
    bump.inputs['Distance'].default_value = 0.02 * MM
    nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
    normal_out = bump.outputs['Normal']
    if relief:
        # base panel relief (planar projection of the Ø62 height map from below)
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1 / (2 * PANEL_R * MM), -1 / (2 * PANEL_R * MM), 1)
        mp.inputs['Location'].default_value = (0.5, 0.5, 0)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        tx = nt.nodes.new('ShaderNodeTexImage')
        tx.image = bpy.data.images.load(relief)
        tx.image.colorspace_settings.name = 'Non-Color'
        tx.extension = 'CLIP'
        nt.links.new(mp.outputs[0], tx.inputs[0])
        sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Object'], sep.inputs[0])
        under = nt.nodes.new('ShaderNodeMath')
        under.operation = 'LESS_THAN'
        under.inputs[1].default_value = (PANEL_D + 0.05) * MM
        nt.links.new(sep.outputs['Z'], under.inputs[0])
        mul = nt.nodes.new('ShaderNodeMath')
        mul.operation = 'MULTIPLY'
        nt.links.new(tx.outputs['Color'], mul.inputs[0])
        nt.links.new(under.outputs[0], mul.inputs[1])
        b2 = nt.nodes.new('ShaderNodeBump')
        b2.inputs['Distance'].default_value = 0.4 * MM
        b2.inputs['Strength'].default_value = 1.0
        nt.links.new(mul.outputs[0], b2.inputs['Height'])
        nt.links.new(normal_out, b2.inputs['Normal'])
        normal_out = b2.outputs['Normal']
    nt.links.new(normal_out, bs.inputs['Normal'])
    nt.links.new(normal_out, bs.inputs['Coat Normal'])
    if fingerprint:
        ang, zmm = fingerprint
        a = math.radians(ang)
        c = Vector((R_OUT * MM * math.sin(a), -R_OUT * MM * math.cos(a), zmm * MM))
        sub = nt.nodes.new('ShaderNodeVectorMath')
        sub.operation = 'SUBTRACT'
        sub.inputs[1].default_value = c
        nt.links.new(tc.outputs['Object'], sub.inputs[0])
        # rotate so the print's long axis is tilted 20 degrees
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Rotation'].default_value = (0, 0, 0)
        mp.inputs['Scale'].default_value = (1 / (7 * MM), 1 / (7 * MM), 1 / (10 * MM))
        nt.links.new(sub.outputs[0], mp.inputs['Vector'])
        ln = nt.nodes.new('ShaderNodeVectorMath')
        ln.operation = 'LENGTH'
        nt.links.new(mp.outputs[0], ln.inputs[0])
        mask = nt.nodes.new('ShaderNodeMapRange')
        mask.inputs['From Min'].default_value = 1.0
        mask.inputs['From Max'].default_value = 0.55
        nt.links.new(ln.outputs['Value'], mask.inputs['Value'])
        wv = nt.nodes.new('ShaderNodeTexWave')
        wv.wave_type = 'RINGS'
        wv.inputs['Scale'].default_value = 1.0
        wv.inputs['Distortion'].default_value = 4.0
        wv.inputs['Detail'].default_value = 3.0
        mp2 = nt.nodes.new('ShaderNodeMapping')
        mp2.inputs['Scale'].default_value = (1 / (0.45 * MM), 1 / (0.45 * MM), 1 / (0.62 * MM))
        nt.links.new(sub.outputs[0], mp2.inputs['Vector'])
        nt.links.new(mp2.outputs[0], wv.inputs['Vector'])
        mul = nt.nodes.new('ShaderNodeMath')
        mul.operation = 'MULTIPLY'
        nt.links.new(wv.outputs['Fac'], mul.inputs[0])
        nt.links.new(mask.outputs['Result'], mul.inputs[1])
        r1 = nt.nodes.new('ShaderNodeMapRange')
        r1.inputs['To Min'].default_value = 0.03
        r1.inputs['To Max'].default_value = 0.22
        nt.links.new(mul.outputs[0], r1.inputs['Value'])
        nt.links.new(r1.outputs['Result'], bs.inputs['Coat Roughness'])
        r2 = nt.nodes.new('ShaderNodeMapRange')
        r2.inputs['To Min'].default_value = 0.10
        r2.inputs['To Max'].default_value = 0.30
        nt.links.new(mul.outputs[0], r2.inputs['Value'])
        nt.links.new(r2.outputs['Result'], bs.inputs['Roughness'])
    return m


def glass_material():
    return material('glass', **{'Base Color': (1, 1, 1, 1), 'Roughness': 0.0, 'IOR': 1.52, 'Transmission Weight': 1.0,
                                'Specular IOR Level': 0.5})


def print_material(path, aov=False):
    img = bpy.data.images.load(path)
    img.colorspace_settings.name = 'sRGB'
    img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('print')
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = 0.55
    bs.inputs['Specular IOR Level'].default_value = 0.35
    uvn = nt.nodes.new('ShaderNodeUVMap')
    uvn.uv_map = 'UVMap'
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = img
    tx.extension = 'CLIP'
    tx.interpolation = 'Cubic'
    nt.links.new(uvn.outputs['UV'], tx.inputs['Vector'])
    nt.links.new(tx.outputs['Color'], bs.inputs['Base Color'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    out = nt.nodes['Material Output']
    nt.links.new(tx.outputs['Alpha'], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(bs.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    if aov:
        # label passes for the fidelity check (tools/fidelidade_uv.py): where the print is, its UV and its ink
        for name, sock in (('label_uv', uvn.outputs['UV']), ('label_ink', tx.outputs['Alpha'])):
            n = nt.nodes.new('ShaderNodeOutputAOV')
            n.aov_name = name
            nt.links.new(sock, n.inputs['Color' if name == 'label_uv' else 'Value'])
        n = nt.nodes.new('ShaderNodeOutputAOV')
        n.aov_name = 'label_mask'
        n.inputs['Value'].default_value = 1.0
    return m


def wax_material(lit=False, pool_r=18.0):
    m = material('wax', **{'Base Color': srgb(CERA), 'Roughness': 0.35, 'Subsurface Weight': 1.0,
                           'Subsurface Radius': (1.0, 2.0 / 3.0, 0.5), 'Subsurface Scale': 3.0 * 0.4 * MM,
                           'Specular IOR Level': 0.45})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # micro-texture: wax tops are never perfect (shrinkage frost and tiny ripples)
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1 / (1.6 * MM)
    nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.12
    bump.inputs['Distance'].default_value = 0.05 * MM
    nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    rr = nt.nodes.new('ShaderNodeMapRange')
    rr.inputs['To Min'].default_value = 0.28
    rr.inputs['To Max'].default_value = 0.45
    nt.links.new(nz.outputs['Fac'], rr.inputs['Value'])
    if lit:
        # melt pool: glossy liquid inside pool_r
        sep = nt.nodes.new('ShaderNodeVectorMath')
        sep.operation = 'LENGTH'
        xy = nt.nodes.new('ShaderNodeVectorMath')
        xy.operation = 'MULTIPLY'
        xy.inputs[1].default_value = (1, 1, 0)
        nt.links.new(tc.outputs['Object'], xy.inputs[0])
        nt.links.new(xy.outputs[0], sep.inputs[0])
        pool = nt.nodes.new('ShaderNodeMapRange')
        pool.inputs['From Min'].default_value = pool_r * MM
        pool.inputs['From Max'].default_value = (pool_r - 1.2) * MM
        nt.links.new(sep.outputs['Value'], pool.inputs['Value'])
        mixr = nt.nodes.new('ShaderNodeMix')
        mixr.data_type = 'FLOAT'
        nt.links.new(pool.outputs['Result'], mixr.inputs['Factor'])
        nt.links.new(rr.outputs['Result'], mixr.inputs['A'])
        mixr.inputs['B'].default_value = 0.05
        nt.links.new(mixr.outputs['Result'], bs.inputs['Roughness'])
        # darker, more translucent liquid
        mixc = nt.nodes.new('ShaderNodeMix')
        mixc.data_type = 'RGBA'
        nt.links.new(pool.outputs['Result'], mixc.inputs['Factor'])
        mixc.inputs['A'].default_value = srgb(CERA)
        mixc.inputs['B'].default_value = srgb('#E2CFAE')
        nt.links.new(mixc.outputs['Result'], bs.inputs['Base Color'])
    else:
        nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
    return m


def wood_material(charred=False, top_mm=7.5):
    """Wood wick: pale veneer, grain running vertically; the top 1,5 mm charred on lit or burnt shots.
    top_mm is the plank top in the wick's object coordinates."""
    m = material('wood', **{'Base Color': srgb('#B9936A'), 'Roughness': 0.8})
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1400, 300, 60)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeTexWave')
    wv.wave_type = 'BANDS'
    wv.bands_direction = 'X'
    wv.inputs['Distortion'].default_value = 3.0
    wv.inputs['Detail'].default_value = 3.0
    wv.inputs['Detail Scale'].default_value = 1.5
    nt.links.new(mp.outputs[0], wv.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = srgb('#A27B54')
    ramp.color_ramp.elements[1].color = srgb('#C7A47A')
    nt.links.new(wv.outputs['Fac'], ramp.inputs[0])
    col = ramp.outputs['Color']
    if charred:
        sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Object'], sep.inputs[0])
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1 / (0.6 * MM)
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        add = nt.nodes.new('ShaderNodeMath')
        add.operation = 'MULTIPLY_ADD'
        add.inputs[1].default_value = 0.6 * MM
        nt.links.new(nz.outputs['Fac'], add.inputs[0])
        nt.links.new(sep.outputs['Z'], add.inputs[2])
        ch = nt.nodes.new('ShaderNodeMapRange')       # charred band, ragged edge
        ch.inputs['From Min'].default_value = (top_mm - 2.2) * MM
        ch.inputs['From Max'].default_value = (top_mm - 1.6) * MM
        nt.links.new(add.outputs[0], ch.inputs['Value'])
        mx = nt.nodes.new('ShaderNodeMix')
        mx.data_type = 'RGBA'
        nt.links.new(ch.outputs['Result'], mx.inputs['Factor'])
        nt.links.new(col, mx.inputs['A'])
        mx.inputs['B'].default_value = srgb('#16110E')
        col = mx.outputs['Result']
        rr = nt.nodes.new('ShaderNodeMapRange')
        rr.inputs['To Min'].default_value = 0.8
        rr.inputs['To Max'].default_value = 0.55
        nt.links.new(ch.outputs['Result'], rr.inputs['Value'])
        nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
    nt.links.new(col, bs.inputs['Base Color'])
    return m


def capsule_materials():
    black = material('anodised', **{'Base Color': srgb('#141416'), 'Metallic': 0.6, 'Roughness': 0.35})
    alu = material('aluminium', **{'Base Color': srgb('#C9CBCD'), 'Metallic': 1.0, 'Roughness': 0.3})
    return black, alu


def flame_material(seed=0.0, strength=1.0):
    """Wood-wick flame as a volume emission: a broad fan, 1.900 K core falling to 1.400 K at the edge,
    a faint blue root, a dim gap right above the wick. Field built in the flame box's generated coords."""
    m = bpy.data.materials.new('flame')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])

    def M(op, a, b=None, c=None):
        n = nt.nodes.new('ShaderNodeMath')
        n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                nt.links.new(v, n.inputs[i])
        return n.outputs[0]

    def smooth(v, e0, e1):
        n = nt.nodes.new('ShaderNodeMapRange')
        n.interpolation_type = 'SMOOTHSTEP'
        n.inputs['From Min'].default_value = e0
        n.inputs['From Max'].default_value = e1
        nt.links.new(v, n.inputs['Value'])
        return n.outputs['Result']

    z = sep.outputs['Z']
    # tongues: a slow noise bends the fan sideways and splits the top
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 2.2
    nz.inputs['Detail'].default_value = 1.0
    nz.noise_dimensions = '4D'
    [i for i in nz.inputs if i.name == 'W'][0].default_value = seed
    nt.links.new(tc.outputs['Generated'], nz.inputs['Vector'])
    wob = M('MULTIPLY', M('SUBTRACT', nz.outputs['Fac'], 0.5), M('MULTIPLY', M('POWER', M('MAXIMUM', z, 0.0), 1.4), 0.9))
    x = M('ADD', M('MULTIPLY', M('SUBTRACT', sep.outputs['X'], 0.5), 2.0), wob)
    y = M('MULTIPLY', M('SUBTRACT', sep.outputs['Y'], 0.5), 2.0)
    # half-width profile: rounded root, widest at a third of the height, pointed tip
    zc = M('MAXIMUM', z, 0.0005)
    w = M('POWER', M('SINE', M('MULTIPLY', M('POWER', zc, 0.52), math.pi)), 0.9)
    w = M('MAXIMUM', w, 0.002)
    dx = M('DIVIDE', x, w)
    dy = M('DIVIDE', y, M('MULTIPLY', w, 0.9))
    d = M('SQRT', M('ADD', M('MULTIPLY', dx, dx), M('MULTIPLY', dy, dy)))
    core = M('MAXIMUM', M('SUBTRACT', 1.0, d), 0.0)
    gap = smooth(z, 0.03, 0.16)                     # dim right above the wick
    top = M('SUBTRACT', 1.0, M('MULTIPLY', M('POWER', zc, 3.0), 0.5))
    dens = M('MULTIPLY', M('MULTIPLY', M('POWER', core, 1.7), gap), top)
    # temperature: 1.400 K at the edge -> 1.900 K in the core
    tmp = nt.nodes.new('ShaderNodeMapRange')
    tmp.inputs['To Min'].default_value = 1750     # tuned by eye: a 1.400-1.900 K ramp renders salmon-pink
    tmp.inputs['To Max'].default_value = 2700     # under Khronos PBR Neutral; the point light stays at 1.900 K
    nt.links.new(M('POWER', core, 0.6), tmp.inputs['Value'])
    bb = nt.nodes.new('ShaderNodeBlackbody')
    nt.links.new(tmp.outputs['Result'], bb.inputs['Temperature'])
    em = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(bb.outputs[0], em.inputs['Color'])
    nt.links.new(M('MULTIPLY', dens, 1.5e4 * strength), em.inputs['Strength'])
    # faint blue root: the bottom 15 %, on the outside of the core
    blue = M('MULTIPLY', M('SUBTRACT', 1.0, smooth(z, 0.02, 0.22)), smooth(d, 0.45, 0.95))
    blue = M('MULTIPLY', blue, M('SUBTRACT', 1.0, smooth(d, 0.95, 1.25)))
    blue = M('MULTIPLY', blue, smooth(z, 0.0, 0.05))
    eb = nt.nodes.new('ShaderNodeEmission')
    eb.inputs['Color'].default_value = (0.10, 0.25, 1.0, 1)
    nt.links.new(M('MULTIPLY', blue, 0.9e3 * strength), eb.inputs['Strength'])
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(em.outputs[0], add.inputs[0])
    nt.links.new(eb.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs['Volume'])
    try:
        m.cycles.volume_step_rate = 0.1
    except Exception:
        pass
    return m


# ----------------------------------------------------------------------------------------------- parts
def print_shell(path, aov=False, chroma=False, segs=720):
    """Full 360 degree UV shell, PRINT_PROUD above the coating, z 18..82 mm. Seam in the empty left gap."""
    r = (R_OUT + COAT_T + PRINT_PROUD) * MM
    bm = bmesh.new()
    rows = [PRINT_Z0 * MM, PRINT_Z1 * MM]
    grid = []
    for j, z in enumerate(rows):
        row = []
        for i in range(segs + 1):
            u = i / segs
            ang = (u - 0.25) * 2 * math.pi            # u=0.25 front (-Y), increasing toward +X
            row.append(bm.verts.new((r * math.sin(ang), -r * math.cos(ang), z)))
        grid.append(row)
    uvl = bm.loops.layers.uv.new('UVMap')
    for i in range(segs):
        f = bm.faces.new((grid[0][i], grid[0][i + 1], grid[1][i + 1], grid[1][i]))
        for lp, (uu, vv) in zip(f.loops, ((i / segs, 0), ((i + 1) / segs, 0), ((i + 1) / segs, 1), (i / segs, 1))):
            lp[uvl].uv = (uu, vv)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # make sure normals point outward
    f0 = bm.faces[0]
    f0c = f0.calc_center_median()
    if f0.normal.dot(Vector((f0c.x, f0c.y, 0))) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    me = bpy.data.meshes.new('print')
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new('print', me)
    bpy.context.collection.objects.link(ob)
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    me.materials.append(chroma_material() if chroma else print_material(path, aov))
    return ob


def wick_plank(lit=False, burnt=False, chroma=False):
    w, t, proud = WICK_W * MM, WICK_T * MM, WICK_PROUD * MM
    depth = 10 * MM                       # buried part, mostly hidden
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    k = bpy.context.object
    k.name = 'wick'
    k.scale = (w, t, proud + depth)
    bpy.ops.object.transform_apply(scale=True)
    k.location = (0, 0, WAX_TOP * MM - 0.8 * MM + (proud + depth) / 2 - depth)
    # a slightly ragged, uneven top
    bm = bmesh.new()
    bm.from_mesh(k.data)
    bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if all(v.co.z > 0 for v in e.verts)], cuts=8)
    for v in bm.verts:
        if v.co.z > (proud + depth) / 2 - 1e-5:
            v.co.z -= (0.25 + 0.25 * math.sin(v.co.x * 900)) * MM * (1.6 if (lit or burnt) else 0.4)
    bm.to_mesh(k.data)
    bm.free()
    bv = k.modifiers.new('bev', 'BEVEL')
    bv.width = 0.12 * MM
    bv.segments = 2
    k.data.materials.append(chroma_material() if chroma else wood_material(charred=lit or burnt, top_mm=(proud + depth) / 2 / MM))
    return k


def flame(scale=1.0, seed=0.0, strength=1.0):
    """Wide, low wood-wick flame: 16 mm wide (along the plank) x 12 mm tall, 7 mm deep. scale/seed animate it."""
    W, D, Hh = FLAME_W * MM, FLAME_D * MM, FLAME_H * MM
    zb = (WAX_TOP - 0.8 + WICK_PROUD - 0.7) * MM
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, zb + Hh * scale / 2))
    f = bpy.context.object
    f.name = 'flame'
    f.scale = (W * (0.97 + 0.03 * scale), D, Hh * scale)
    f.data.materials.append(flame_material(seed, strength))
    f.visible_shadow = False
    bpy.ops.object.light_add(type='POINT', location=(0, 0, zb + 4.5 * MM * scale))
    L = bpy.context.object
    L.name = 'flame_light'
    L.data.energy = 0.25 * scale * strength
    L.data.color = (1.0, 0.56, 0.24)        # ~1.900 K
    L.data.shadow_soft_size = 3 * MM
    return f, L


def tampa(art=None, chroma=False, aov=False, size=None):
    """A TAMPA-PALCO: steel disc Ø90 x 3 mm + gasket ring (OD76 ID66, 1,5 mm) + inner lip Ø68,8 x 1 mm
    (O SINGLE: Ø70 disc, same logic). Built with the GASKET BOTTOM at z = 0 (stage pose). Returns the root empty."""
    if size:
        use_size(size)
    before = set(bpy.data.objects)
    Lr = LID_R
    disc_prof = [(0, 1.5), (Lr - 0.6, 1.5)] + _arc(Lr - 0.6, 2.1, 0.6, -math.pi / 2, 0, 4)
    disc_prof += [(Lr, 3.9)] + _arc(Lr - 0.6, 3.9, 0.6, 0, math.pi / 2, 4) + [(0, 4.5)]
    disc = lathe('tampa_disc', disc_prof, segs=256)
    gi, go = GASKET_RI, GASKET_RO
    gasket_prof = [(gi, 1.5), (gi, 0.4)] + _arc(gi + 0.4, 0.4, 0.4, math.pi, 1.5 * math.pi, 3)
    gasket_prof += [(go - 0.4, 0.0)] + _arc(go - 0.4, 0.4, 0.4, 1.5 * math.pi, 2 * math.pi, 3) + [(go, 1.5)]
    gasket = lathe('tampa_gasket', gasket_prof, segs=192)
    lo = LIP_RO
    lip_prof = [(lo - 1.6, 1.5), (lo - 1.6, 0.7), (lo - 1.2, 0.5), (lo, 0.5), (lo, 1.5)]
    lip = lathe('tampa_lip', lip_prof, segs=192)
    if chroma:
        for o in (disc, gasket, lip):
            o.data.materials.append(chroma_material())
    else:
        steel = material('powder', **{'Base Color': srgb(PRETO), 'Roughness': 0.45, 'Specular IOR Level': 0.45})
        nt = steel.node_tree
        bs = nt.nodes['Principled BSDF']
        tc = nt.nodes.new('ShaderNodeTexCoord')
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1 / (0.25 * MM)
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bump = nt.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.02 * 5
        bump.inputs['Distance'].default_value = 0.02 * MM
        nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
        if art and os.path.exists(art):
            mp = nt.nodes.new('ShaderNodeMapping')
            mp.inputs['Scale'].default_value = (1 / (2 * LID_R * MM), 1 / (2 * LID_R * MM), 1)
            mp.inputs['Location'].default_value = (0.5, 0.5, 0)
            nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
            tx = nt.nodes.new('ShaderNodeTexImage')
            tx.image = bpy.data.images.load(art)
            tx.extension = 'CLIP'
            tx.interpolation = 'Cubic'
            nt.links.new(mp.outputs[0], tx.inputs[0])
            # only on the top face (object z > 4,4 mm) and the brim edge band gets the curved line
            sep = nt.nodes.new('ShaderNodeSeparateXYZ')
            nt.links.new(tc.outputs['Object'], sep.inputs[0])
            top = nt.nodes.new('ShaderNodeMath')
            top.operation = 'GREATER_THAN'
            top.inputs[1].default_value = 4.3 * MM
            nt.links.new(sep.outputs['Z'], top.inputs[0])
            fac = nt.nodes.new('ShaderNodeMath')
            fac.operation = 'MULTIPLY'
            nt.links.new(tx.outputs['Alpha'], fac.inputs[0])
            nt.links.new(top.outputs[0], fac.inputs[1])
            mix = nt.nodes.new('ShaderNodeMix')
            mix.data_type = 'RGBA'
            mix.inputs['A'].default_value = srgb(PRETO)
            nt.links.new(fac.outputs[0], mix.inputs['Factor'])
            nt.links.new(tx.outputs['Color'], mix.inputs['B'])
            nt.links.new(mix.outputs['Result'], bs.inputs['Base Color'])
            # tape is cloth: rougher than the powder coat
            rr = nt.nodes.new('ShaderNodeMapRange')
            rr.inputs['To Min'].default_value = 0.45
            rr.inputs['To Max'].default_value = 0.78
            nt.links.new(fac.outputs[0], rr.inputs['Value'])
            nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
        disc.data.materials.append(steel)
        sil = material('silicone', **{'Base Color': srgb('#2A2A2C'), 'Roughness': 0.6})
        gasket.data.materials.append(sil)
        lip.data.materials.append(steel)
    new = [o for o in bpy.data.objects if o not in before]
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    root.name = 'tampa_root'
    for o in new:
        if o.parent is None:
            o.parent = root
    return root


TAMPA_TOP = 4.5  # mm, top of the disc when the gasket rests on the floor


def copo(spec, at=(0, 0, 0), rot_deg=0.0):
    """The whole candle. Returns the root empty (move/rotate the root, never the parts)."""
    use_size(spec.get('size', '200'))
    if spec.get('wick', 'double') == 'double':
        # §D.6 flame-legibility gate fallback: double-ply wood wick, flame 14 x 18 mm (taller, narrower)
        g = globals()
        g['WICK_T'] = 2 * g['WICK_T'] + 0.2
        g['FLAME_W'], g['FLAME_H'] = 14.0 * g['FLAME_W'] / 16.0, 21.0 * g['FLAME_W'] / 16.0
    chroma = spec.get('chroma', False)
    fx = FAIXAS[spec.get('faixa', '02')]
    coat_hex = spec.get('coating', fx['coat'])
    lit = spec.get('lit', False)
    burnt = spec.get('burnt', False)
    before = set(bpy.data.objects)

    glass = lathe('glass', glass_profile(), segs=256)
    glass.data.materials.append(chroma_material() if chroma else glass_material())
    coat = lathe('coating', coating_profile(), segs=256)
    coat.data.materials.append(chroma_material() if chroma else
                               coating_material(coat_hex, spec.get('fingerprint', (34, 0.66 * H_GLASS)), spec.get('base_relief')))
    cap = lathe('capsule', capsule_profile(), segs=256)
    if chroma:
        cap.data.materials.append(chroma_material())
    else:
        black, alu = capsule_materials()
        cap.data.materials.append(black)
        cap.data.materials.append(alu)
        # inside faces (r < CAP_R - CAP_T/2 and below the lip) -> aluminium
        for p in cap.data.polygons:
            c = p.center
            r = math.hypot(c.x, c.y) / MM
            if r < CAP_R - CAP_T / 2 - 0.05 and c.z / MM < BASE + CAP_H - CAP_LIP - 0.05 and p.normal.z < 0.9:
                p.material_index = 1
            if c.z / MM < BASE + CAP_T + 0.01 and p.normal.z > 0.5:
                p.material_index = 1
    pool_r = spec.get('pool_r', 17.0)
    wax = lathe('wax', wax_profile(lit, pool_r, 0.0), segs=256, smooth_angle=60)
    wax.data.materials.append(chroma_material() if chroma else wax_material(lit, pool_r))
    wick_plank(lit, burnt, chroma)
    if spec.get('wrap') or chroma:
        if spec.get('wrap') and not chroma:
            print_shell(spec['wrap'], spec.get('aov', False))
    if lit and not chroma:
        flame(spec.get('flame_scale', 1.0), spec.get('flame_seed', 0.0), spec.get('flame_strength', 1.0))
    if spec.get('base_sticker') and not chroma:
        sticker(spec['base_sticker'])
    lid_mode = spec.get('lid')
    new = [o for o in bpy.data.objects if o not in before]
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    root.name = 'copo_root'
    for o in new:
        if o.parent is None:
            o.parent = root
    if lid_mode == 'on':
        t = tampa(spec.get('lid_art'), chroma)
        t.location = (0, 0, H_GLASS * MM)          # gasket rests on the rim
        t.parent = root
    elif lid_mode == 'stage':
        t = tampa(spec.get('lid_art'), chroma)
        t.location = (at[0], at[1], at[2])
        t.rotation_euler = (0, 0, math.radians(spec.get('lid_rot_deg', 0.0)))
        at = (at[0], at[1], at[2] + TAMPA_TOP * MM)
    root.location = at
    root.rotation_euler = (0, 0, math.radians(rot_deg))
    return root


def sticker(path):
    """Lot sticker: clear matte PP 40 x 12 mm on the base underside, centred at -7,0 mm (toward the front)."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -7.0 * MM, PANEL_D * MM - COAT_T * MM - 0.03 * MM))
    s = bpy.context.object
    s.name = 'lot_sticker'
    s.scale = (40 * MM, 12 * MM, 1)
    s.rotation_euler = (math.pi, 0, 0)       # faces down
    img = bpy.data.images.load(path)
    m = bpy.data.materials.new('sticker')
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = 0.6
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = img
    nt.links.new(tx.outputs['Color'], bs.inputs['Base Color'])
    # clear film: mostly transparent where there is no ink, with a faint matte haze
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    fac = nt.nodes.new('ShaderNodeMath')
    fac.operation = 'MAXIMUM'
    fac.inputs[1].default_value = 0.12
    nt.links.new(tx.outputs['Alpha'], fac.inputs[0])
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(bs.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes['Material Output'].inputs[0])
    s.data.materials.append(m)
    return s


def enable_label_aovs(exr_dir=None):
    """Declare the label AOVs and (optionally) write them, with Diffuse Color, to a multilayer EXR in exr_dir."""
    sc = bpy.context.scene
    vl = bpy.context.view_layer
    names = [a.name for a in vl.aovs]
    for n, t in (('label_uv', 'COLOR'), ('label_ink', 'VALUE'), ('label_mask', 'VALUE')):
        if n not in names:
            a = vl.aovs.add()
            a.name = n
            a.type = t
    vl.use_pass_diffuse_color = True
    if exr_dir:
        sc.use_nodes = True
        nt = sc.node_tree
        rl = next((n for n in nt.nodes if n.bl_idname == 'CompositorNodeRLayers'), None)
        if rl is None:
            rl = nt.nodes.new('CompositorNodeRLayers')
            comp = nt.nodes.new('CompositorNodeComposite')
            nt.links.new(rl.outputs['Image'], comp.inputs['Image'])
        fo = nt.nodes.new('CompositorNodeOutputFile')
        fo.base_path = exr_dir
        fo.format.file_format = 'OPEN_EXR_MULTILAYER'
        fo.format.color_depth = '32'
        fo.file_slots.clear()
        for name in ('label_uv', 'label_ink', 'label_mask', 'DiffCol'):
            fo.file_slots.new(name)
            nt.links.new(rl.outputs[name], fo.inputs[name])
        return fo
