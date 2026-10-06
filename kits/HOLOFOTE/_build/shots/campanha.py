"""HOLOFOTE · campanha — the final 3D plates of O LANÇAMENTO (platform §E.1–§E.3, §D.6–§D.11).

    _build/shots/blender.sh campanha.py -- SHOT [SHOT ...] [--teste] [--samples N] [--pct P]

SHOT: KV01_9x16 KV01_4x5 KV01_1x1 KV01_16x9 KV01_9x16_apagado (flame-gate reference)
      C01 C02 C04 C05_1x1 C05_9x16 C06 C08 C10
      L01 L02 L03 L04 L05 L06 L07
--teste  50 % resolution, 24 samples, no AOVs, into 02_PRODUTO/renders/_campanha_testes/ (look-dev only).

Every final goes through foto(): the director's colour management (S.cena), the trimmed light paths of motor.still,
a 16-bit master + 8-bit delivered plate in 02_PRODUTO/renders/, and — for every visible label — the UV fidelity
check (tools/fidelidade_uv.py) per candle: each candle's print material writes a `label_id` AOV, so in a four-candle
shot each label is compared with ITS OWN master and its own planted error (fid_multi.py). Reports land in
06_PRODUCAO/fidelidade/<SHOT>[__<copo>].json. LOJA shots render transparent over a shadow catcher; the exact
#FFF8EC plate is composited by code (S.loja_plate) and the check runs on that delivered image.

Never edits holofote.py, sets_lib.py or objects_lib.py: everything here builds on their public API.
"""
import sys, os, math, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motor as M                       # puts sets/, objects/, blender/ on sys.path and imports bpy, sets_lib, holofote
import bpy
from mathutils import Vector, Euler
import numpy as np
S = M.S
H = S.H
import objects_lib as OL               # noqa: E402

KIT = M.KIT
RENDERS = M.RENDERS
TESTES = os.path.join(RENDERS, '_campanha_testes')
FID = M.FID
WEB = M.WEB
PROD = os.path.join(KIT, '02_PRODUTO')
LOJA_OUT = os.path.join(KIT, '03_LANCAMENTO', 'L')
COAT = {k: v['coat'] for k, v in H.FAIXAS.items()}
INK = {k: v['ink'] for k, v in H.FAIXAS.items()}
BASE_RELIEF = os.path.join(PROD, 'base', 'HLF-BASE-200_PRECISAVA_altura16.png')
BASE_STICKER = os.path.join(PROD, 'base', 'HLF-BASE-200_ETIQUETA-LOTE.png')
SETLIST_C04 = os.path.join(HERE, 'cache', 'SETLIST_C04_lado-1.png')     # made by tipo_c.py (code-set, Shantell)


# ================================================================================================= helpers
def lab(root, faixa, wrap=None, tag=None):
    """A label to verify: the copo root, its faixa (coat + ink colours) and its master."""
    return dict(root=root, faixa=faixa, wrap=wrap or S.wrap(faixa), tag=tag or ('HLF-' + faixa))


def esconder(root, prefixes):
    for o in S.descendants(root):
        if any(o.name.startswith(p) for p in prefixes):
            o.hide_render = True
            o.hide_viewport = True


def vazio(root):
    """The clean empty glass (C08, L07): no capsule, no wax, no wick."""
    esconder(root, ('capsule', 'wax', 'wick', 'flame'))


def marcar(objs, inflamavel=True):
    for o in objs:
        for d in S.descendants(o):
            if d.type in ('MESH', 'CURVE'):
                d['inflamavel'] = inflamavel


def cam_fit(points, el_deg, az_deg, lens, res, box, fstop=None, focus=None, target=None, name='cam'):
    """A camera on a sphere around `target` (elevation, azimuth: az 0 = in front at -Y, negative = camera-left),
    looking at it, whose distance and lens shift fit the world `points` into the pixel `box` (x0, y0, x1, y1),
    centred. Verticals converge only by the elevation; there is no roll."""
    P = np.asarray(points, np.float64)
    tgt = Vector(target) if target is not None else Vector(P.mean(0))
    tilt, yaw = -el_deg, az_deg
    R = S.cam_matrix(tilt, yaw)
    d = S._dir(az_deg, el_deg)
    bw, bh = box[2] - box[0], box[3] - box[1]

    def meas(D):
        C = tgt + d * D
        px, py = S.project(P, C, R, lens, res)
        return C, px, py
    lo, hi = 0.02, 50.0
    for _ in range(90):
        mid = math.sqrt(lo * hi)
        _, px, py = meas(mid)
        if (px.max() - px.min()) > bw or (py.max() - py.min()) > bh:
            lo = mid
        else:
            hi = mid
    D = math.sqrt(lo * hi)
    C, px, py = meas(D)
    big = max(res)
    cx, cy = (px.max() + px.min()) / 2, (py.max() + py.min()) / 2
    bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    shift = ((cx - bx) / big, (by - cy) / big)
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_fit = 'AUTO'
    cd.sensor_width = 36.0
    cd.shift_x, cd.shift_y = shift
    cd.clip_start = 0.005
    cd.clip_end = 200
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = C
    ob.rotation_euler = Euler((math.radians(90 + tilt), 0, math.radians(yaw)))
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_distance = focus or (tgt - C).length
        cd.dof.aperture_fstop = fstop
    sc = bpy.context.scene
    sc.camera = ob
    sc.render.resolution_x, sc.render.resolution_y = res
    return ob


def pontos(objs, step=1):
    """World-space vertices of the evaluated meshes under these roots (for cam_fit)."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for r in objs:
        for o in S.descendants(r):
            if o.type != 'MESH' or o.hide_render:
                continue
            for c in o.bound_box:
                out.append(tuple(o.matrix_world @ Vector(c)))
    return out


def glass_frac(root, res):
    """Fraction of the frame height spanned by this copo's glass (decides §D.7.5: < 20 % = graphic thumbnail)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    g = [o for o in S.descendants(root) if o.name.startswith('glass') and o.type == 'MESH']
    if not g:
        return None
    g = g[0]
    ys = []
    for i, v in enumerate(g.data.vertices):
        if i % 7:
            continue
        p = world_to_camera_view(sc, sc.camera, g.matrix_world @ v.co)
        ys.append(p.y)
    return max(ys) - min(ys)


def _tag_ids(labels):
    """Give each label's print material a constant `label_id` AOV (after add_print_aovs, which skips materials
    that already hold an AOV node)."""
    vl = bpy.context.view_layer
    if 'label_id' not in [a.name for a in vl.aovs]:
        a = vl.aovs.add()
        a.name = 'label_id'
        a.type = 'VALUE'
    for k, L in enumerate(labels, 1):
        L['id'] = k
        prints = [o for o in S.descendants(L['root']) if o.name.startswith('print') and o.type == 'MESH']
        for p in prints:
            for m in p.data.materials:
                nt = m.node_tree
                n = nt.nodes.new('ShaderNodeOutputAOV')
                n.aov_name = 'label_id'
                n.inputs['Value'].default_value = float(k)


def _check(name, L, p8, aov_dir, multi, albedo=None, film=False):
    exr = os.path.join(aov_dir, '0001.exr')
    os.makedirs(FID, exist_ok=True)
    suf = ('__' + L['tag']) if multi else ''
    jp = os.path.join(FID, name + suf + ('__albedo' if albedo else '') + '.json')
    asset = albedo or p8
    cmd = [WEB, os.path.join(HERE, 'fid_multi.py'), '--master', L['wrap'], '--aov', exr, '--asset', asset,
           '--coat', COAT[L['faixa']], '--ink', INK[L['faixa']], '--json', jp,
           '--debug', os.path.join(aov_dir, 'debug%s%s.png' % (suf, '_albedo' if albedo else ''))]
    if multi:
        cmd += ['--id', str(L['id'])]
    if film:
        cmd += ['--film']
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        rep = json.load(open(jp))[0]
    except Exception:
        rep = {'erro': (r.stderr or r.stdout)[-800:]}
    rep['glass_frac_altura'] = L.get('frac')
    rep['thumbnail_sem_alegacao'] = bool(L.get('frac') is not None and L['frac'] < 0.20)
    json.dump([rep], open(jp, 'w'), indent=2, ensure_ascii=False)
    return rep


def foto(name, build, res, samples=64, transparent=False, pct=100, teste=False, threshold=0.02, loja=False):
    """Build and render one plate; run the label checks; composite the LOJA plate. Returns (png, info, reports)."""
    t0 = time.time()
    if teste:
        pct, samples = 50, min(samples, 24)
    sc = S.cena(res=res, samples=samples, transparent=transparent)
    sc.cycles.adaptive_threshold = threshold
    sc.cycles.volume_step_rate = 1.0
    sc.cycles.max_bounces = 8
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 4
    sc.cycles.transmission_bounces = 8
    sc.cycles.transparent_max_bounces = 8
    sc.cycles.volume_bounces = 0
    info = build() or {}
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = pct
    labels = info.get('labels', [])
    for L in labels:
        L['frac'] = glass_frac(L['root'], res)
    outdir = TESTES if teste else RENDERS
    os.makedirs(outdir, exist_ok=True)
    aov_dir = os.path.join(HERE, 'aov', name) + os.sep
    if labels and not teste:
        H.add_print_aovs()
        _tag_ids(labels)
        fo = H.enable_label_aovs(aov_dir)
        rl = next(n for n in sc.node_tree.nodes if n.bl_idname == 'CompositorNodeRLayers')
        fo.file_slots.new('label_id')
        sc.node_tree.links.new(rl.outputs['label_id'], fo.inputs['label_id'])
    stem = name + ('_alpha' if loja else '')
    if teste:
        p8 = os.path.join(outdir, stem + '.png')
        sc.render.image_settings.color_depth = '8'
        S.render(p8)
    else:
        sc.render.image_settings.color_depth = '16'
        p16 = os.path.join(outdir, stem + '_16bit.png')
        S.render(p16)
        p8 = os.path.join(outdir, stem + '.png')
        subprocess.run([WEB, '-c', 'import sys,cv2,numpy as np;a=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED);'
                        'a=(a.astype(np.float64)/257.0).round().clip(0,255).astype(np.uint8) if a.dtype==np.uint16 else a;'
                        'cv2.imwrite(sys.argv[2],a)', p16, p8], check=True)
    final = p8
    if loja:
        os.makedirs(LOJA_OUT, exist_ok=True)
        final = os.path.join(TESTES if teste else LOJA_OUT, name + '.png')
        S.loja_plate(p8, final)
    reps = []
    if labels and not teste:
        multi = len(labels) > 1
        for L in labels:
            rep = _check(name, L, final, aov_dir, multi)
            reps.append((L['tag'], rep))
            if info.get('albedo'):
                alb = os.path.join(aov_dir, 'albedo%s.png' % (('__' + L['tag']) if multi else ''))
                subprocess.run([WEB, os.path.join(HERE, 'fid_multi.py'), '--albedo', os.path.join(aov_dir, '0001.exr'), alb],
                               check=True, capture_output=True)
                reps.append((L['tag'] + ' (albedo)', _check(name, L, final, aov_dir, multi, albedo=alb)))
    dt = round(time.time() - t0, 1)
    print('FOTO', name, dt, 's', final, flush=True)
    for tag, r in reps:
        print('   FIDELIDADE', name, tag, json.dumps({k: r.get(k) for k in (
            'tiles', 'worst_tile', 'p5_tile', 'hue_shift_deg', 'sat_ratio', 'pass', 'glass_frac_altura',
            'thumbnail_sem_alegacao', 'erro')}, ensure_ascii=False), flush=True)
    log = os.path.join(HERE, 'campanha_log.jsonl')
    with open(log, 'a') as f:
        f.write(json.dumps(dict(nome=name, teste=teste, segundos=dt, samples=samples, pct=pct, res=res, arquivo=final,
                                fidelidade={t: {k: r.get(k) for k in ('tiles', 'worst_tile', 'p5_tile', 'hue_shift_deg',
                                                                       'sat_ratio', 'pass', 'glass_frac_altura')}
                                            for t, r in reps}, quando=time.strftime('%Y-%m-%d %H:%M:%S')),
                           ensure_ascii=False) + '\n')
    return final, info, reps


# ================================================================================================= KV-01 (§E.1)
KV01 = {'9x16': dict(res=(1080, 1920), glass=384, top=900, cx=None),
        '4x5': dict(res=(1080, 1350), glass=351, top=677, cx=None),
        '1x1': dict(res=(1080, 1080), glass=260, top=590, cx=None),
        '16x9': dict(res=(1920, 1080), glass=410, top=470, cx=1420)}


def b_kv01(fmt, lit=True):
    k = KV01[fmt]

    def f():
        h = S.palco(at=(0, 0, 0))
        root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=lit), at=h['place'], rot_deg=-12)
        S.ride(root, h['lift'])
        if lit:
            S.flame_bounce(h, root)
        S.camera_glass(res=k['res'], lens=50, cam_height=0.220, tilt_deg=-6, glass_px=k['glass'], top_y=k['top'],
                       center_x=k['cx'], fstop=5.6)
        S.clearance()
        return dict(labels=[lab(root, '02')])
    return f


# ================================================================================================= C01 · O MURO
# 4 x 3 lambe grid of 22 x 33 cm posters; the frame is the photographer's crop around the ledge: the headline poster
# 12 (MÃE AO VIVO. 09.05. INGRESSOS COM VOCÊ.) sits whole above the candles, the grid bleeds off the frame.
C01_GRADE = ['07', '01', '08', '02',
             '10', '12', '03', '06',
             '11', '04', '05', '09']


def b_c01():
    h = S.muro(n=4, spacing=0.100, grade=C01_GRADE, poster_w=0.22, ledge_z=0.315, drip_cell=2)
    roots = []
    for i, f in enumerate(['01', '02', '03', '04']):
        roots.append(H.copo(dict(faixa=f, wrap=S.wrap(f), lid='on', lid_art=S.tampa_art()), at=h['slots'][i], rot_deg=0))
    d = 0.60 * 50 / 36.0                       # a 0,60 m tall frame at the wall, 50 mm
    zc = 0.465
    cam = S.camera_pin((0.0, -d, zc), 0.0, 0.0, 50, (1080, 1350), (0.0, 0.0, zc), (540, 675), fstop=8.0, focus=d - 0.067)
    h['flash'] = S.flash(cam, target_dist=d - 0.067)
    S.clearance()
    return dict(labels=[lab(r, f) for r, f in zip(roots, ['01', '02', '03', '04'])])


# ================================================================================================= C02 · A PRIMEIRA FILA
def b_c02(spill=3.0, cam='preset'):
    def f():
        h = S.escola(preset='C02')
        root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True), at=h['place'], rot_deg=h['candle_rot'])
        S.flame_bounce(h, root, receivers=[o for o in h['coll'].objects if o.name.startswith('palco_tabuado')])
        if spill != 1.0 and h.get('spill'):
            h['spill'].data.energy *= spill
        S.escola_camera(h, 'C02', res=(1080, 1350))
        S.clearance()
        return dict(labels=[lab(root, '02')])
    return f


# ================================================================================================= C04 · A DISCOGRAFIA
C04_X = (-0.30, -0.10, 0.10, 0.30)


def b_c04():
    h = S.palco(at=(0, 0, 0), spot=False, rotunda_spill=None)
    esconder_objs = [h['tape_plate'], h['tape_floor']]
    for o in esconder_objs:
        o.hide_render = True
    roots = []
    pool_r, spot_deg = 0.078, 26.0
    throw = pool_r / math.tan(math.radians(spot_deg / 2))
    for x, f in zip(C04_X, ['01', '02', '03', '04']):
        r = H.copo(dict(faixa=f, wrap=S.wrap(f), lit=True, flame_seed=hash(f) % 7 * 0.13), at=(x, 0, 0), rot_deg=-6)
        roots.append(r)
        S.flame_bounce(h, r)
        tgt = Vector((x, 0, 0.020))
        loc = tgt + S._dir(-30.0, 55.0) * throw
        L = S._light('c04_spot_' + f, 'SPOT', loc, tgt, S.ENERGIA['palco_spot_k'] * throw ** 2,
                     color=S.balanced(3200, 3300), coll=h['coll'], spot_size=math.radians(spot_deg), spot_blend=0.04,
                     shadow_soft_size=0.0103 * throw)
    # the setlist, taped flat 60 cm in front of the row (its far edge 0,62 m from the flames), out of the pools
    side1 = SETLIST_C04 if os.path.exists(SETLIST_C04) else None
    sl = OL.setlist_taped(side1=side1, at=(0.0, -0.82, 0.0), rot_deg=-3.0)
    marcar([sl.root])
    # its only light: a dim, shadowless downstage wash light-linked to the paper and tape (the spill off the four
    # lanterns a real stage would have; nothing else sees it)
    wash = S._light('c04_setlist_wash', 'AREA', (0.0, -0.95, 0.9), (0.0, -0.82, 0.0), 2.2, coll=h['coll'],
                    shape='RECTANGLE', size=0.9, size_y=0.6, use_shadow=False)
    wash.visible_camera = False
    S.link_receivers(wash, [o for o in S.descendants(sl.root) if o.type == 'MESH'])
    S.clearance()
    pts = [(x, 0, z) for x in (C04_X[0] - 0.12, C04_X[-1] + 0.12) for z in (0.0, 0.11)] + \
          [(x, -1.02, 0.0) for x in (-0.09, 0.09)]
    cam_fit(pts, 24.0, 0.0, 70, (1080, 1350), (90, 470, 990, 1310), fstop=8.0,
            target=(0.0, -0.30, 0.05))
    return dict(labels=[lab(r, f) for r, f in zip(roots, ['01', '02', '03', '04'])])


# ================================================================================================= C05 · O CASE
def b_c05(fmt):
    res = (1080, 1080) if fmt == '1x1' else (1080, 1920)

    def f():
        h = S.palco(at=(0, 0, 0), pool_r=0.17, spot_aim_z=0.06)
        for o in (h['tape_plate'], h['tape_floor']):
            o.hide_render = True
        ang = OL.open_deg_for_camera(70)
        c = OL.case(state='open', open_deg=ang, copo=dict(faixa='02', wrap=S.wrap('02'), lid_art=S.tampa_art()),
                    band=True, band_kw=dict(route='corner'), at=(0, 0, 0), rot_deg=22.0)
        pts = pontos([c.root])
        box = (110, 110, 970, 970) if fmt == '1x1' else (90, 560, 990, 1460)
        cam = cam_fit(pts, 70.0, 0.0, 60, res, box, fstop=11.0, target=(0, 0, 0.07))
        bpy.context.view_layer.update()
        OL.place_work_bulb(c, cam, dist=1.3)
        return dict(labels=[], case=c)
    return f, res


# ================================================================================================= C06 · O MENOR HOLOFOTE
def b_c06(spill=0.012):
    h = S.palco(at=(0, 0, 0), spot=False, rotunda_spill=0.0)
    root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True), at=h['place'], rot_deg=-12)
    S.ride(root, h['lift'])
    S.flame_bounce(h, root)
    S.flame_spill(h, root, energy=spill)
    S.camera_glass(res=(1080, 1350), lens=85, cam_height=0.150, tilt_deg=-5, glass_px=405, top_y=600)
    S.clearance()
    return dict(labels=[lab(root, '02')], albedo=True)


# ================================================================================================= C08 · NOVA TEMPORADA
def b_c08():
    h = S.palco(at=(0, 0, 0), pool_r=0.150)
    root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=False), at=h['place'], rot_deg=-12)
    vazio(root)
    S.ride(root, h['lift'])
    rf = OL.refil(faixa='02', peel=0.5, at=(0.098, 0.012, 0.0), rot_deg=-150.0)
    gp, top = 440, 610
    px_mm = gp / 88.0
    S.camera_glass(res=(1080, 1350), lens=50, cam_height=0.220, tilt_deg=-6, glass_px=gp, top_y=top,
                   center_x=540 - 49 * px_mm * 0.95, fstop=5.6)
    return dict(labels=[lab(root, '02')])


# ================================================================================================= C10 · SALVA COMO
C10_COPOS = [('02', 'CASE-02_MAE-CORACAO'), ('01', 'CASE-01_DONA-CIDA'), ('03', 'CASE-03_MAINHA')]


def b_c10():
    h = S.muro(n=3, spacing=0.11, posters=False)
    roots = [H.copo(dict(faixa=f, wrap=S.wrap(personal=p)), at=h['slots'][i], rot_deg=0) for i, (f, p) in enumerate(C10_COPOS)]
    S.muro_camera(h, 'C10', res=(1080, 1350))
    S.clearance()
    return dict(labels=[lab(r, f, S.wrap(personal=p), p) for r, (f, p) in zip(roots, C10_COPOS)])


# ================================================================================================= LOJA (§E.3)
def _loja_cam_glass(h, res, fill, cam_height, tilt, center_x=None, size='200'):
    gp = int(round(res[1] * fill))
    top = (res[1] - gp) // 2
    return S.camera_glass(res=res, lens=85, cam_height=cam_height, tilt_deg=tilt, glass_px=gp, top_y=top, at=h['at'],
                          size=size, center_x=center_x)


def tampa_lean(at, side=1, out=0.050, back=0.040, face_deg=26.0, lean_deg=12.0, size='200'):
    """L01: the stage lid leaning on the candle's right side, its top (X + 'ela fica aqui.') turned to camera."""
    t = H.tampa(S.tampa_art(size), size=size)
    at = Vector(at)
    t.location = at + Vector((side * out, back, 0.0))
    t.rotation_euler = (math.radians(90 - lean_deg), 0.0, math.radians(side * face_deg))
    bpy.context.view_layer.update()
    zmin = min((o.matrix_world @ Vector(c)).z for o in S.descendants(t) if o.type == 'MESH' for c in o.bound_box)
    t.location.z -= zmin - at.z
    return t


def b_l01():
    h = S.loja()
    root = H.copo(dict(faixa='02', wrap=S.wrap('02')), at=h['place'], rot_deg=-20)
    t = tampa_lean(h['place'])
    pts = pontos([root, t])
    cam_fit(pts, 0.0, 0.0, 85, (1200, 1200), (96, 150, 1104, 1050), target=(0.03, 0, 0.044))
    return dict(labels=[lab(root, '02')])


def b_l02():
    h = S.loja()
    root = H.copo(dict(faixa='02', wrap=S.wrap('02')), at=h['place'], rot_deg=180)
    _loja_cam_glass(h, (1200, 1200), 0.68, 0.052, 0.0)
    return dict(labels=[lab(root, '02')])


def b_l03():
    h = S.loja(key_az=-84.0, key_el=9.0, key_dist=1.0, fill_ratio=0.12)
    root = H.copo(dict(faixa='02', wrap=S.wrap('02'), base_relief=BASE_RELIEF, base_sticker=BASE_STICKER),
                  at=(0, 0, (H.SIZES['200']['R_OUT'] + 0.10) * H.MM), rot_deg=0)
    root.rotation_euler = (math.radians(-90.0), 0.0, math.radians(15.0))
    pts = pontos([root])
    cam_fit(pts, 6.0, 0.0, 100, (1200, 1200), (96, 230, 1104, 970), target=(0, 0, 0.038))
    return dict(labels=[], copo=root)


def b_l04():
    h = S.loja(key_az=-40.0, key_el=55.0)
    ang = OL.open_deg_for_camera(70)
    c = OL.case(state='open', open_deg=ang, copo=dict(faixa='02', wrap=S.wrap('02'), lid_art=S.tampa_art()),
                setlist=False, band=True, band_kw=dict(route='drape'), at=(-0.02, 0.03, 0), rot_deg=0.0)
    sl = OL.setlist(state='fan', first_fold=-1, at=(0.155, -0.02, 0.0), rot_deg=-28.0)
    pts = pontos([c.root, sl.root])
    cam = cam_fit(pts, 70.0, 0.0, 70, (1200, 1200), (96, 96, 1104, 1104), fstop=11.0, target=(0.03, 0.0, 0.05))
    bpy.context.view_layer.update()
    OL.place_work_bulb(c, cam, dist=1.3, lit=False)
    return dict(labels=[])


def b_l05():
    h = S.loja()
    root = H.copo(dict(faixa='02', wrap=S.wrap('02'), lit=True, lid='stage', lid_rot_deg=12, lid_art=S.tampa_art()),
                  at=h['place'], rot_deg=-20)
    S.flame_bounce(h, root, receivers=h['seamless_parts'], energy=0.04)
    S.loja_camera(h, 'L05', res=(1200, 1200), fill=0.64)
    S.clearance()
    return dict(labels=[lab(root, '02')])


L06_ORDEM = [('200', '03'), ('200', '01'), ('200', '02'), ('200', '04'), ('080', '02'), ('ref', '02')]


def b_l06():
    h = S.loja(key_dist=1.6)
    sizes = [s if s != 'ref' else 0.0686 for s, _ in L06_ORDEM]
    pos = S.fila(tuple(sizes), gap=0.020, at=(0, 0, 0))
    roots, labels = [], []
    for (s, f), p in zip(L06_ORDEM, pos):
        if s == 'ref':
            rf = OL.refil(faixa=f, peel=0.0, at=p, rot_deg=-90.0)
            roots.append(rf.root)
            continue
        w = S.wrap(f) if s == '200' else os.path.join(S.ROTULOS, 'HLF-02-080_ROTULO_wrap.png')
        r = H.copo(dict(faixa=f, wrap=w, size=s, lid='on', lid_art=S.tampa_art(s)), at=p, rot_deg=0)
        roots.append(r)
        labels.append(lab(r, f, w, 'HLF-%s-%s' % (f, s)))
    pts = pontos(roots)
    cam_fit(pts, 10.0, 0.0, 85, (1200, 1200), (96, 96, 1104, 1104), fstop=11.0, target=(0, 0, 0.045))
    return dict(labels=labels)


def b_l07():
    h = S.loja()
    root = H.copo(dict(faixa='02', wrap=S.wrap('02')), at=(-0.045, 0.02, 0), rot_deg=-18)
    vazio(root)
    rf = OL.refil(faixa='02', peel=0.5, at=(0.050, -0.030, 0.0), rot_deg=-140.0)
    pts = pontos([root, rf.root])
    cam_fit(pts, 22.0, 0.0, 85, (1200, 1200), (96, 170, 1104, 1030), fstop=11.0, target=(0, 0, 0.04))
    return dict(labels=[lab(root, '02')])


# ================================================================================================= registry
def shots():
    T = {}
    for fmt, k in KV01.items():
        T['KV01_' + fmt] = dict(nome='KV-01_%s_limpo' % fmt, b=b_kv01(fmt), res=k['res'], s=96 if fmt == '9x16' else 64)
    T['KV01_9x16_apagado'] = dict(nome='KV-01_9x16_apagado_portao', b=b_kv01('9x16', lit=False), res=(1080, 1920), s=32, pct=50,
                                  nolabel=True)
    T['C01'] = dict(nome='C01_O-MURO_limpo', b=b_c01, res=(1080, 1350), s=64)
    T['C02'] = dict(nome='C02_A-PRIMEIRA-FILA_limpo', b=b_c02(), res=(1080, 1350), s=64)
    T['C04'] = dict(nome='C04_A-DISCOGRAFIA_limpo', b=b_c04, res=(1080, 1350), s=64)
    for fmt in ('1x1', '9x16'):
        f, res = b_c05(fmt)
        T['C05_' + fmt] = dict(nome='C05_O-CASE_%s_limpo' % fmt, b=f, res=res, s=64)
    T['C06'] = dict(nome='C06_O-MENOR-HOLOFOTE_limpo', b=b_c06, res=(1080, 1350), s=64)
    T['C08'] = dict(nome='C08_NOVA-TEMPORADA_limpo', b=b_c08, res=(1080, 1350), s=64)
    T['C10'] = dict(nome='C10_SALVA-COMO_limpo', b=b_c10, res=(1080, 1350), s=64)
    for k, b, n in (('L01', b_l01, 'L01_FRENTE'), ('L02', b_l02, 'L02_VERSO'), ('L03', b_l03, 'L03_A-BASE'),
                    ('L04', b_l04, 'L04_O-CASE-ABERTO'), ('L05', b_l05, 'L05_A-TAMPA-PALCO'), ('L06', b_l06, 'L06_A-TURNE'),
                    ('L07', b_l07, 'L07_NOVA-TEMPORADA')):
        T[k] = dict(nome=n, b=b, res=(1200, 1200), s=64, loja=True)
    return T


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    teste = '--teste' in a
    ns = int(a[a.index('--samples') + 1]) if '--samples' in a else None
    pc = int(a[a.index('--pct') + 1]) if '--pct' in a else None
    T = shots()
    pedidos = [x for x in a if x in T]
    for k in pedidos:
        t = T[k]
        b = t['b']
        if t.get('nolabel'):
            inner = b
            def b(inner=inner):
                i = inner()
                i['labels'] = []
                return i
        foto(t['nome'], b, t['res'], samples=ns or t['s'], transparent=t.get('loja', False),
             pct=pc or t.get('pct', 100), teste=teste, loja=t.get('loja', False))
