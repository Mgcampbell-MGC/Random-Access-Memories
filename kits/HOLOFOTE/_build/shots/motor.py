"""Shot engine: one function renders a final still with its label AOVs and runs the fidelity check on it.

    import motor as M
    M.still('KV-45_aceso', build, res=(1080, 1920), samples=256, wrap=S.wrap('02'), coat='#FFE81A')

`build()` constructs the scene (set + candle + camera) after `S.cena()` has been called by the engine. Outputs:
  02_PRODUTO/renders/<name>.png          8-bit sRGB delivered plate (and <name>_16bit.png, the master)
  _build/shots/aov/<name>/0001.exr       label AOVs (git-ignored)
  06_PRODUCAO/fidelidade/<name>.json     the fidelidade_uv.py report (when a wrap is given)
Run under /home/user/venvs/blender/bin/python. One Blender process at a time.
"""
import os, sys, json, time, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(B, 'sets'))
sys.path.insert(0, os.path.join(B, 'objects'))
sys.path.insert(0, os.path.join(B, 'blender'))
import bpy
import sets_lib as S
import holofote as H

KIT = os.path.abspath(os.path.join(B, '..'))
RENDERS = os.path.join(KIT, '02_PRODUTO', 'renders')
FID = os.path.join(KIT, '06_PRODUCAO', 'fidelidade')
WEB = '/home/user/venvs/web/bin/python'


def still(name, build, res, samples=256, wrap=None, coat=None, ink='#121014', transparent=False, outdir=RENDERS,
          check=True, threshold=0.02, pct=100):
    t0 = time.time()
    sc = S.cena(res=res, samples=samples, transparent=transparent)
    sc.cycles.adaptive_threshold = threshold
    sc.cycles.volume_step_rate = 1.0
    # light paths trimmed for speed (measured): the scene has no caustics and no deep glass stacks to feed
    sc.cycles.max_bounces = 8
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 4
    sc.cycles.transmission_bounces = 8
    sc.cycles.transparent_max_bounces = 8
    sc.cycles.volume_bounces = 0
    build()
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = pct
    aov_dir = os.path.join(HERE, 'aov', name) + os.sep
    if wrap:
        H.add_print_aovs()
        H.enable_label_aovs(aov_dir)
    sc.render.image_settings.color_depth = '16'
    os.makedirs(outdir, exist_ok=True)
    p16 = os.path.join(outdir, name + '_16bit.png')
    S.render(p16)
    # 8-bit delivered copy (OpenCV keeps the 16-bit channels; PIL would truncate them)
    p8 = os.path.join(outdir, name + '.png')
    subprocess.run([WEB, '-c', 'import sys,cv2,numpy as np;a=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED);'
                    'a=(a.astype(np.float64)/257.0).round().clip(0,255).astype(np.uint8) if a.dtype==np.uint16 else a;'
                    'cv2.imwrite(sys.argv[2],a)', p16, p8], check=True)
    rep = None
    if wrap and check:
        exr = os.path.join(aov_dir, '0001.exr')
        os.makedirs(FID, exist_ok=True)
        jp = os.path.join(FID, name + '.json')
        r = subprocess.run([WEB, os.path.join(B, 'tools', 'fidelidade_uv.py'), '--master', wrap, '--aov', exr,
                            '--asset', p8] + (['--coat', coat] if coat else []) + ['--ink', ink, '--json', jp,
                            '--debug', os.path.join(HERE, 'aov', name, 'debug.png')],
                           capture_output=True, text=True)
        try:
            rep = json.load(open(jp))[0]
        except Exception:
            rep = {'erro': r.stderr[-800:]}
    print('STILL', name, round(time.time() - t0, 1), 's', json.dumps({k: rep.get(k) for k in (
        'tiles', 'worst_tile', 'p5_tile', 'hue_shift_deg', 'sat_ratio', 'pass')} if rep else {}), flush=True)
    return p8, rep
