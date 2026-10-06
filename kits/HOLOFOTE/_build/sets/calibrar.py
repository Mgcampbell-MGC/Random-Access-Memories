"""Calibrate a set's key light so the coating reads at its faixa hex in the lit area (PBR Neutral, exposure -3,0).

    /home/user/venvs/blender/bin/python calibrar.py palco|escola|muro|loja [--faixa 02]

Method: build the set with an UNPRINTED copo (pure coating, unlit), render once to a scene-linear EXR (Standard view,
exposure 0), sample the coating on the lit panel by projecting a grid of surface points, then solve the scale s
that makes s x (median coating radiance) read closest (CIEDE2000) to the hex through PBR Neutral. Energy scales by s.
Prints the result and appends it to calibracao.json (the record); the constants are copied into sets_lib.ENERGIA.
"""
import sys, os, json, math, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import numpy as np
from mathutils import Vector
import sets_lib as S
import medir

SCR = os.environ.get('CALIB_DIR', os.path.join(HERE, '_tex'))


def coat_points(root, az_center_deg=0.0, az_half=12.0, z0=0.035, z1=0.065, n=9):
    """World points on the coating (r = 38,08 mm) around a panel azimuth (candle-local; 0 = front panel centre)."""
    pts = []
    M = root.matrix_world
    for i in range(n):
        a = math.radians(az_center_deg - az_half + 2 * az_half * i / (n - 1))
        for j in range(n):
            z = z0 + (z1 - z0) * j / (n - 1)
            pts.append(M @ Vector((0.03808 * math.sin(a), -0.03808 * math.cos(a), z)))
    return pts


def sample(exr_path, cam, pts):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    img = bpy.data.images.load(exr_path)
    W, Hh = img.size
    px = np.array(img.pixels[:], np.float32).reshape(Hh, W, 4)
    vals = []
    for p in pts:
        co = world_to_camera_view(sc, cam, p)
        x, y = int(co.x * W), int(co.y * Hh)
        if 0 <= x < W and 0 <= y < Hh:
            vals.append(px[y, x, :3])
    return np.median(np.array(vals), axis=0), len(vals)


def run(which, faixa='02', res=(270, 480)):
    S.cena(res=res, samples=48, exposure=0.0)
    sc = bpy.context.scene
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'OPEN_EXR'
    sc.render.image_settings.color_depth = '32'
    spec = dict(faixa=faixa, wrap=None, lit=False)
    if which == 'palco':
        h = S.palco(at=(0, 0, 0), rotunda=False)
        root = S.H.copo(spec, at=h['place'], rot_deg=-12)
        cam = S.camera_glass(res=(1080, 1920), lens=85, cam_height=0.160, tilt_deg=-5, glass_px=883, top_y=610)['object']
        energy, key = h['spot'].data.energy, 'palco_spot_k'
        const = S.ENERGIA[key]
        az = 0.0
    elif which == 'escola':
        h = S.escola(preset='C02', candle=False)
        root = S.H.copo(spec, at=h['place'], rot_deg=h['candle_rot'])
        cam = S.escola_camera(h, 'C02')
        energy, key = h['spot'].data.energy, 'escola_spot_k'
        const = S.ENERGIA[key]
        az = 180.0
    elif which == 'muro':
        h = S.muro()
        root = S.H.copo(spec, at=h['slots'][1], rot_deg=0)
        cam = S.muro_camera(h, 'C01')
        energy, key = h['flash'].data.energy, 'muro_flash_k'
        const = S.ENERGIA[key]
        az = 0.0
    elif which == 'loja':
        h = S.loja()
        root = S.H.copo(spec, at=h['place'], rot_deg=-20)
        cam = S.loja_camera(h, 'L01')
        energy, key = h['key'].data.energy, 'loja_key_k'
        const = S.ENERGIA[key]
        az = 0.0
    else:
        raise SystemExit('unknown set ' + which)
    sc.render.resolution_x, sc.render.resolution_y = res
    bpy.context.view_layer.update()
    os.makedirs(SCR, exist_ok=True)
    exr = os.path.join(SCR, 'calib_%s.exr' % which)
    S.render(exr)
    med, n = sample(exr, cam, coat_points(root, az))
    hexc = medir.FAIXA_HEX[faixa]
    s, rep = medir.best_scale(med, hexc, S.EXPOSURE)
    now = medir.compare(medir.display(med, S.EXPOSURE), hexc)
    out = dict(set=which, faixa=faixa, samples=n, energy_rendered=energy, const_rendered=const,
               coat_linear=[float(x) for x in med], reads_now=now, scale=s, const_new=const * s,
               energy_new=energy * s, reads_new=rep)
    print('CALIB', json.dumps(out, indent=1))
    rec = os.path.join(HERE, 'calibracao.json')
    db = json.load(open(rec)) if os.path.exists(rec) else {}
    db['%s_%s' % (which, faixa)] = out
    json.dump(db, open(rec, 'w'), indent=1)
    return out


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument('which')
    ap.add_argument('--faixa', default='02')
    a = ap.parse_args(argv)
    run(a.which, a.faixa)
