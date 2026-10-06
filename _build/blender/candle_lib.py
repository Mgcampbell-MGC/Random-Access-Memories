"""Parametric candle studio for Blender (bpy 4.5, Cycles CPU).

Builds a photoreal candle pack from a spec dict and renders it. The label and box art are
image files painted onto the geometry by UV mapping, so the printed text in every render
is exactly the master artwork: nothing is ever drawn by a generator.

Usage (from the blender venv):
    python render_scene.py -- scene.json
where scene.json follows build_scene()'s keys. See __main__ at the bottom.
"""
import bpy, bmesh, math, json, sys, time, os
from mathutils import Vector, Euler

MM = 0.001


def srgb(hexstr, a=1.0):
    h = hexstr.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, a)


def reset(res=(1080, 1350), samples=128, view='Standard', look='None', exposure=0.0, transparent=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.02
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 12
    sc.cycles.transmission_bounces = 12
    sc.cycles.glossy_bounces = 6
    sc.cycles.transparent_max_bounces = 16
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 1.0
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA' if transparent else 'RGB'
    sc.render.image_settings.color_depth = '8'
    sc.view_settings.view_transform = view
    sc.view_settings.look = look
    sc.view_settings.exposure = exposure
    return sc


def material(name, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m


def emission_material(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial')
    e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = color
    e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


def chroma_material():
    """Flat matte chroma blue, the stand-in colour of the studio method (#0047FF-ish)."""
    return material('chroma', **{'Base Color': srgb('#0046FF'), 'Roughness': 1.0, 'Specular IOR Level': 0.0})


def world(color='#F2EEF0', strength=0.35):
    w = bpy.data.worlds.new('world')
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs[0].default_value = srgb(color)
    bg.inputs[1].default_value = strength
    return w


def sweep(color='#FF6FB5', roughness=0.7, size=3.0, curve=0.45, floor_y=-0.6):
    """Seamless studio sweep: floor + curved wall."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    fl = bpy.context.object
    fl.name = 'sweep'
    me = fl.data
    bm = bmesh.new()
    bm.from_mesh(me)
    edges = [e for e in bm.edges if all(v.co.y > size / 2 - 1e-4 for v in e.verts)]
    ret = bmesh.ops.extrude_edge_only(bm, edges=edges)
    for v in [g for g in ret['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z += size
    bm.to_mesh(me)
    bm.free()
    fl.location.y = size / 2 - 0.35
    b = fl.modifiers.new('bev', 'BEVEL')
    b.width = curve
    b.segments = 24
    b.limit_method = 'ANGLE'
    bpy.ops.object.shade_smooth()
    fl.data.materials.append(material('sweep', **{'Base Color': srgb(color), 'Roughness': roughness, 'Specular IOR Level': 0.25}))
    return fl


def _open_cylinder(radius, height, z0=0.0, verts=192, cap_bottom=True):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=height, location=(0, 0, z0 + height / 2),
                                        end_fill_type='NGON')
    o = bpy.context.object
    bm = bmesh.new()
    bm.from_mesh(o.data)
    top = [f for f in bm.faces if f.normal.z > 0.9]
    bmesh.ops.delete(bm, geom=top, context='FACES')
    if not cap_bottom:
        bot = [f for f in bm.faces if f.normal.z < -0.9]
        bmesh.ops.delete(bm, geom=bot, context='FACES')
    bm.to_mesh(o.data)
    bm.free()
    return o


def vessel(spec):
    """Vessel: cylinder tumbler. spec: kind glass|ceramic|tin, d_mm, h_mm, wall_mm, base_mm, color, finish."""
    R = spec.get('d_mm', 80) / 2 * MM
    H = spec.get('h_mm', 90) * MM
    wall = spec.get('wall_mm', 4) * MM
    base = spec.get('base_mm', 8) * MM
    kind = spec.get('kind', 'glass')
    o = _open_cylinder(R, H)
    o.name = 'vessel'
    s = o.modifiers.new('sol', 'SOLIDIFY')
    s.thickness = wall
    s.offset = -1
    s.use_even_offset = True
    bv = o.modifiers.new('bev', 'BEVEL')
    bv.width = min(wall * 0.45, 1.6 * MM)
    bv.segments = 5
    bv.limit_method = 'ANGLE'
    bpy.ops.object.shade_smooth()
    o.data.polygons.foreach_set('use_smooth', [True] * len(o.data.polygons))
    # thick base disc (inside the solidified shell)
    bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=R - wall * 0.98, depth=base, location=(0, 0, base / 2))
    b = bpy.context.object
    b.name = 'vessel_base'
    bb = b.modifiers.new('bev', 'BEVEL')
    bb.width = 1.0 * MM
    bb.segments = 4
    bpy.ops.object.shade_smooth()
    col = srgb(spec.get('color', '#FFFFFF'))
    if spec.get('chroma'):
        m = chroma_material()
    elif kind == 'glass':
        m = material('glass', **{'Base Color': col, 'Roughness': spec.get('roughness', 0.03), 'IOR': 1.52,
                                 'Transmission Weight': 1.0, 'Specular IOR Level': 0.5})
    elif kind == 'ceramic':
        m = material('ceramic', **{'Base Color': col, 'Roughness': spec.get('roughness', 0.35), 'Coat Weight': spec.get('coat', 0.4),
                                   'Coat Roughness': 0.08, 'Subsurface Weight': 0.05})
    elif kind == 'tin':
        m = material('tin', **{'Base Color': col, 'Metallic': 1.0, 'Roughness': spec.get('roughness', 0.22)})
    else:
        m = material('vessel', **{'Base Color': col, 'Roughness': 0.4})
    o.data.materials.append(m)
    b.data.materials.append(m)
    return o, R, H, wall, base


def wax(R_inner, base, fill_h, color='#F7EEE3', melted=False, chroma=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=R_inner - 0.15 * MM, depth=fill_h, location=(0, 0, base + fill_h / 2),
                                        end_fill_type='TRIFAN')
    w = bpy.context.object
    # add concentric rings on the top so the meniscus can curve smoothly
    bm0 = bmesh.new(); bm0.from_mesh(w.data)
    topf = [f for f in bm0.faces if f.normal.z > 0.9]
    bmesh.ops.subdivide_edges(bm0, edges=list({e for f in topf for e in f.edges if all(v.co.z > fill_h/2 - 1e-6 for v in e.verts) and not all(math.hypot(v.co.x, v.co.y) > R_inner*0.9 for v in e.verts)}), cuts=6, use_grid_fill=False)
    bm0.to_mesh(w.data); bm0.free()
    w.name = 'wax'
    bm = bmesh.new()
    bm.from_mesh(w.data)
    # slight concave top (wax shrinks toward the wick)
    for v in bm.verts:
        if v.co.z > fill_h / 2 - 1e-6:
            r = math.hypot(v.co.x, v.co.y) / R_inner
            # flat centre, meniscus rising at the wall (wax climbs the glass)
            v.co.z += (max(0.0, r - 0.82) / 0.18) ** 2 * 1.4 * MM - 0.6 * MM
    bm.to_mesh(w.data)
    bm.free()
    bv = w.modifiers.new('bev', 'BEVEL'); bv.width = 0.8 * MM; bv.segments = 3; bv.limit_method = 'ANGLE'
    bpy.ops.object.shade_smooth()
    w.data.polygons.foreach_set('use_smooth', [True] * len(w.data.polygons))
    if chroma:
        m = chroma_material()
    else:
        m = material('wax', **{'Base Color': srgb(color), 'Roughness': 0.12 if melted else 0.42,
                               'Subsurface Weight': 1.0, 'Subsurface Radius': (1.0, 0.7, 0.45), 'Subsurface Scale': 0.006,
                               'Specular IOR Level': 0.45, 'Coat Weight': 0.6 if melted else 0.0, 'Coat Roughness': 0.03})
    w.data.materials.append(m)
    return w, base + fill_h


def wick(top_z, kind='cotton', lit=False, chroma=False):
    if kind == 'wood':
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, top_z + 4 * MM))
        k = bpy.context.object
        k.scale = (12 * MM, 0.8 * MM, 9 * MM)
        col = srgb('#5A4030') if not lit else srgb('#1A1410')
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.75 * MM, depth=11 * MM, location=(0, 0, top_z + 4.5 * MM))
        k = bpy.context.object
        k.rotation_euler = (math.radians(4), math.radians(-3), 0)
        col = srgb('#2B2620') if not lit else srgb('#0E0B09')
    k.name = 'wick'
    k.data.materials.append(chroma_material() if chroma else material('wick', **{'Base Color': col, 'Roughness': 0.95}))
    return k


def flame(top_z, height_mm=26, strength=18.0):
    """Teardrop flame: emission with a vertical colour gradient (blue root, amber body, pale core)."""
    h = height_mm * MM
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0, 0, 0))
    f = bpy.context.object
    f.name = 'flame'
    for v in f.data.vertices:
        z = v.co.z  # -1..1
        t = (z + 1) / 2
        taper = (1 - t) ** 0.45 * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 1.25)))
        v.co.x *= 3.6 * MM * taper * 1.0
        v.co.y *= 3.6 * MM * taper * 1.0
        v.co.z = t * h
    f.location = (0, 0, top_z + 7.5 * MM)
    bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new('flame')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.05, 0.18, 1.0, 1)
    cr.elements[1].position = 0.18
    cr.elements[1].color = (1.0, 0.42, 0.06, 1)
    e = cr.elements.new(0.45)
    e.color = (1.0, 0.78, 0.38, 1)
    e2 = cr.elements.new(0.9)
    e2.color = (1.0, 0.55, 0.14, 1)
    nt.links.new(sep.outputs['Z'], ramp.inputs[0])
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs[1].default_value = strength
    nt.links.new(ramp.outputs[0], em.inputs[0])
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs[0].default_value = 0.45
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lw.outputs['Facing'], mix.inputs[0])
    nt.links.new(em.outputs[0], mix.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    f.data.materials.append(m)
    f.visible_shadow = False
    bpy.ops.object.light_add(type='POINT', location=(0, 0, top_z + 7.5 * MM + h * 0.35))
    L = bpy.context.object
    L.name = 'flame_light'
    L.data.energy = 1.6
    L.data.color = (1.0, 0.62, 0.3)
    L.data.shadow_soft_size = 4 * MM
    return f, L


def label_wrap(R, z0, height, image_path, span_deg=150, face_deg=0.0, paper='matte', offset=0.25, chroma=False):
    """A printed label wrapped round the cylinder. The image is the exact artwork (u = around, v = up).
    face_deg rotates the label centre; 0 faces the camera at -Y."""
    r = R + offset * MM
    bpy.ops.mesh.primitive_cylinder_add(vertices=384, radius=r, depth=height, location=(0, 0, z0 + height / 2),
                                        end_fill_type='NOTHING')
    lb = bpy.context.object
    lb.name = 'label'
    bpy.ops.object.shade_smooth()
    me = lb.data
    while len(me.uv_layers):
        me.uv_layers.remove(me.uv_layers[0])
    uv = me.uv_layers.new(name='UVMap')
    span = math.radians(span_deg)
    face = math.radians(face_deg)
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            ang = math.atan2(v.x, -v.y) - face
            ang = (ang + math.pi) % (2 * math.pi) - math.pi
            uv.data[li].uv = (0.5 + ang / span, (v.z + height / 2) / height)
    if chroma:
        lb.data.materials.append(chroma_material())
        return lb
    img = bpy.data.images.load(image_path)
    img.colorspace_settings.name = 'sRGB'
    m = bpy.data.materials.new('label')
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = 0.62 if paper == 'matte' else 0.18
    bs.inputs['Specular IOR Level'].default_value = 0.18 if paper == 'matte' else 0.5
    if paper == 'gloss':
        bs.inputs['Coat Weight'].default_value = 0.5
        bs.inputs['Coat Roughness'].default_value = 0.05
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = img
    tx.extension = 'CLIP'
    tx.interpolation = 'Cubic'
    nt.links.new(tx.outputs['Color'], bs.inputs['Base Color'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    out = nt.nodes['Material Output']
    nt.links.new(tx.outputs['Alpha'], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(bs.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    lb.data.materials.append(m)
    return lb


def lid(R, z, h_mm=14, color='#E8E2DA', kind='matte', chroma=False, image_path=None):
    """A slip lid sitting at height z (or placed beside the jar by moving the object)."""
    h = h_mm * MM
    bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=R + 1.2 * MM, depth=h, location=(0, 0, z + h / 2))
    l = bpy.context.object
    l.name = 'lid'
    b = l.modifiers.new('bev', 'BEVEL')
    b.width = 2.2 * MM
    b.segments = 6
    bpy.ops.object.shade_smooth()
    if chroma:
        l.data.materials.append(chroma_material())
        return l
    if kind == 'metal':
        m = material('lid', **{'Base Color': srgb(color), 'Metallic': 1.0, 'Roughness': 0.25})
    elif kind == 'wood':
        m = material('lid', **{'Base Color': srgb(color), 'Roughness': 0.55})
    else:
        m = material('lid', **{'Base Color': srgb(color), 'Roughness': 0.45, 'Coat Weight': 0.25})
    if image_path:
        # top print: planar projection on the lid top
        nt = m.node_tree
        bs = nt.nodes['Principled BSDF']
        tc = nt.nodes.new('ShaderNodeTexCoord')
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1 / (2 * (R + 1.2 * MM)), 1 / (2 * (R + 1.2 * MM)), 1)
        mp.inputs['Location'].default_value = (0.5, 0.5, 0)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        tx = nt.nodes.new('ShaderNodeTexImage')
        tx.image = bpy.data.images.load(image_path)
        tx.extension = 'CLIP'
        nt.links.new(mp.outputs[0], tx.inputs[0])
        mix = nt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.inputs['A'].default_value = srgb(color)
        nt.links.new(tx.outputs['Alpha'], mix.inputs['Factor'])
        nt.links.new(tx.outputs['Color'], mix.inputs['B'])
        nt.links.new(mix.outputs['Result'], bs.inputs['Base Color'])
    l.data.materials.append(m)
    return l


def box(w_mm, d_mm, h_mm, atlas_path=None, color='#FFFFFF', loc=(0, 0, 0), rot_deg=0.0, chroma=False, gloss=False):
    """A printed carton. atlas_path is a 4x3 net image: row1 [., top, ., .], row2 [left, front, right, back],
    row3 [., bottom, ., .]; each cell is face-sized in proportion is NOT required: cells are uniform and the
    art for each face is stretched to its cell, so draw the atlas with the same cell layout."""
    W, D, H = w_mm * MM, d_mm * MM, h_mm * MM
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] + H / 2))
    b = bpy.context.object
    b.name = 'box'
    b.scale = (W, D, H)
    b.rotation_euler = (0, 0, math.radians(rot_deg))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bv = b.modifiers.new('bev', 'BEVEL')
    bv.width = 0.6 * MM
    bv.segments = 3
    me = b.data
    while len(me.uv_layers):
        me.uv_layers.remove(me.uv_layers[0])
    uv = me.uv_layers.new(name='UVMap')
    cells = {  # (col,row) in a 4x3 grid, row 0 at bottom
        'top': (1, 2), 'bottom': (1, 0), 'left': (0, 1), 'front': (1, 1), 'right': (2, 1), 'back': (3, 1)}
    for poly in me.polygons:
        n = poly.normal
        if n.z > 0.5:
            face = 'top'
        elif n.z < -0.5:
            face = 'bottom'
        elif n.y < -0.5:
            face = 'front'
        elif n.y > 0.5:
            face = 'back'
        elif n.x < -0.5:
            face = 'left'
        else:
            face = 'right'
        cx, cy = cells[face]
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            if face in ('top', 'bottom'):
                a, bq = (v.x / W + 0.5), (v.y / D + 0.5)
                if face == 'bottom':
                    bq = 1 - bq
            elif face == 'front':
                a, bq = v.x / W + 0.5, v.z / H + 0.5
            elif face == 'back':
                a, bq = 0.5 - v.x / W, v.z / H + 0.5
            elif face == 'left':
                a, bq = 0.5 - v.y / D, v.z / H + 0.5
            else:
                a, bq = v.y / D + 0.5, v.z / H + 0.5
            uv.data[li].uv = ((cx + a) / 4, (cy + bq) / 3)
    if chroma:
        b.data.materials.append(chroma_material())
        return b
    m = material('box', **{'Base Color': srgb(color), 'Roughness': 0.25 if gloss else 0.6,
                           'Specular IOR Level': 0.4 if gloss else 0.2})
    if atlas_path:
        nt = m.node_tree
        tx = nt.nodes.new('ShaderNodeTexImage')
        tx.image = bpy.data.images.load(atlas_path)
        tx.interpolation = 'Cubic'
        nt.links.new(tx.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color'])
    b.data.materials.append(m)
    return b


def plinth(kind='cyl', size_mm=(160, 160, 60), color='#FFFFFF', loc=(0, 0, 0), roughness=0.5):
    sx, sy, sz = [s * MM for s in size_mm]
    if kind == 'cyl':
        bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=sx / 2, depth=sz, location=(loc[0], loc[1], loc[2] + sz / 2))
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] + sz / 2))
        bpy.context.object.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
    p = bpy.context.object
    p.name = 'plinth'
    bv = p.modifiers.new('bev', 'BEVEL')
    bv.width = 2 * MM
    bv.segments = 4
    bpy.ops.object.shade_smooth()
    p.data.materials.append(material('plinth', **{'Base Color': srgb(color), 'Roughness': roughness}))
    return p


def area_light(loc, target=(0, 0, 0.05), size=0.4, energy=80, color=(1, 1, 1), shape='RECTANGLE', size_y=None):
    bpy.ops.object.light_add(type='AREA', location=loc)
    L = bpy.context.object
    L.data.size = size
    L.data.shape = shape
    if size_y:
        L.data.size_y = size_y
    L.data.energy = energy
    L.data.color = color
    d = Vector(target) - Vector(loc)
    L.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return L


def spot(loc, target=(0, 0, 0.05), energy=200, size_deg=40, blend=0.15, radius=0.002, color=(1, 1, 1)):
    bpy.ops.object.light_add(type='SPOT', location=loc)
    L = bpy.context.object
    L.data.energy = energy
    L.data.spot_size = math.radians(size_deg)
    L.data.spot_blend = blend
    L.data.shadow_soft_size = radius
    L.data.color = color
    d = Vector(target) - Vector(loc)
    L.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return L


def camera(loc, target, lens=85, shift_x=0.0, shift_y=0.0, dof_dist=None, fstop=8.0):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.data.lens = lens
    c.data.shift_x = shift_x
    c.data.shift_y = shift_y
    c.data.clip_start = 0.01
    d = Vector(target) - Vector(loc)
    c.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if dof_dist:
        c.data.dof.use_dof = True
        c.data.dof.focus_distance = dof_dist
        c.data.dof.aperture_fstop = fstop
    bpy.context.scene.camera = c
    return c


def glare(threshold=0.9, size=7, mix=-0.6):
    """Soft bloom round the flame via the compositor (Fog Glow)."""
    sc = bpy.context.scene
    sc.use_nodes = True
    nt = sc.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    gl.glare_type = 'FOG_GLOW'
    gl.quality = 'HIGH'
    gl.threshold = threshold
    gl.size = size
    gl.mix = mix
    comp = nt.nodes.new('CompositorNodeComposite')
    nt.links.new(rl.outputs['Image'], gl.inputs['Image'])
    nt.links.new(gl.outputs['Image'], comp.inputs['Image'])
    if 'Alpha' in rl.outputs and 'Alpha' in comp.inputs:
        nt.links.new(rl.outputs['Alpha'], comp.inputs['Alpha'])


def render(path):
    sc = bpy.context.scene
    sc.render.filepath = path
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print('RENDERED', path, round(time.time() - t, 1), 's')


def candle(spec, at=(0, 0, 0), rot_deg=0.0, chroma=False):
    """Build one complete candle at a location. spec keys: vessel{}, fill_ratio, wax_color, wick, lit,
    melted, label{path, height_mm, z_mm, span_deg, paper}, lid{...} or None, lid_off(bool)"""
    before = set(bpy.data.objects)
    v, R, H, wall, base = vessel({**spec['vessel'], 'chroma': chroma})
    fill_h = (H - base) * spec.get('fill_ratio', 0.82)
    w, top = wax(R - wall, base, fill_h, spec.get('wax_color', '#F7EEE3'), melted=spec.get('melted', False), chroma=chroma)
    k = wick(top - 1.2 * MM, spec.get('wick', 'cotton'), lit=spec.get('lit', False), chroma=chroma)
    if spec.get('lit') and not chroma:
        flame(top - 1.2 * MM, spec.get('flame_mm', 24), spec.get('flame_strength', 16.0))
    lab = spec.get('label')
    if lab:
        label_wrap(R, lab.get('z_mm', 20) * MM, lab.get('height_mm', 50) * MM, lab.get('path'), lab.get('span_deg', 150),
                   lab.get('face_deg', 0.0), lab.get('paper', 'matte'), chroma=chroma)
    ld = spec.get('lid')
    if ld and not spec.get('lid_off'):
        lid(R, H, ld.get('h_mm', 14), ld.get('color', '#E8E2DA'), ld.get('kind', 'matte'), chroma=chroma,
            image_path=ld.get('top_print'))
    new = [o for o in bpy.data.objects if o not in before]
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    root.name = 'candle_root'
    for o in new:
        if o.parent is None:
            o.parent = root
    root.location = at
    root.rotation_euler = (0, 0, math.radians(rot_deg))
    return root, R, H


if __name__ == '__main__':
    pass
