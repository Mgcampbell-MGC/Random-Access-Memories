"""A still rendered at 200 % becomes the 1× deliverable: plate and label AOVs box-filtered 2 × 2, then checked at 1×.

    /home/user/venvs/web/bin/python _build/shots/reduzir_2x.py KV-45_aceso [--coat #FFE81A] [--master ...]

Why (6 Oct 2026): KV-45's hairline under DOMINGO · 09.05 resolved only at the default tile grid at 1× (worst 0,815;
0,50 with the grid shifted 12 px), so the ads' pushed and encoded frames failed the label check. Rendering at 2× and
area-averaging gives true supersampled anti-aliasing instead of a denoiser's guess, and the hero gains the sharpness.
The 2× render keeps its own report (<name>_2x.json, the stricter check); the 1× outputs replace the usual names so
every downstream script is unchanged. The AOVs are pixel-filtered (premultiplied by the mask), so a box average of
every channel is exactly the AOV a 1× render would have written.
"""
import argparse, json, os, shutil, subprocess, sys
import numpy as np
import cv2
import OpenEXR

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
R = os.path.join(KIT, '02_PRODUTO', 'renders')
FID = os.path.join(KIT, '06_PRODUCAO', 'fidelidade')
AOV = os.path.join(HERE, 'aov')
WEB = '/home/user/venvs/web/bin/python'


def box(a):
    h, w = a.shape[:2]
    a = a[:h - h % 2, :w - w % 2]
    return a.reshape(h // 2, 2, w // 2, 2, *a.shape[2:]).mean(axis=(1, 3)).astype(a.dtype)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nome')
    ap.add_argument('--coat', default='#FFE81A')
    ap.add_argument('--master', default=os.path.join(KIT, '02_PRODUTO', 'rotulos', 'HLF-02_ROTULO_wrap.png'))
    a = ap.parse_args()
    n = a.nome
    # 1. move the 2× outputs aside
    p16, p8 = os.path.join(R, n + '_16bit.png'), os.path.join(R, n + '.png')
    q16, q8 = os.path.join(R, n + '_2x_16bit.png'), os.path.join(R, n + '_2x.png')
    big = cv2.imread(p16, cv2.IMREAD_UNCHANGED)
    if big is None or big.shape[0] < 3000:
        sys.exit('expected a 200 % render at ' + p16)
    shutil.move(p16, q16)
    shutil.move(p8, q8)
    d1, d2 = os.path.join(AOV, n), os.path.join(AOV, n + '_2x')
    if os.path.isdir(d2):
        shutil.rmtree(d2)
    shutil.move(d1, d2)
    j1, j2 = os.path.join(FID, n + '.json'), os.path.join(FID, n + '_2x.json')
    if os.path.exists(j1):
        shutil.move(j1, j2)
    # 2. plate: area-average in 16-bit linear-light-agnostic sRGB values (as the 1× encoder would see them)
    small = cv2.resize(big, (big.shape[1] // 2, big.shape[0] // 2), interpolation=cv2.INTER_AREA)
    cv2.imwrite(p16, small)
    cv2.imwrite(p8, (small.astype(np.float64) / 257.0).round().clip(0, 255).astype(np.uint8))
    # 3. AOVs: box-filter every channel
    f = OpenEXR.File(os.path.join(d2, '0001.exr'))
    part = f.parts[0]
    chans = {k: box(v.pixels) for k, v in part.channels.items()}
    hdr = {k: v for k, v in part.header.items() if k in ('compression', 'type', 'lineOrder')}
    os.makedirs(d1, exist_ok=True)
    OpenEXR.File(hdr, chans).write(os.path.join(d1, '0001.exr'))
    # 4. the 1× check, as motor.still runs it
    subprocess.run([WEB, os.path.join(KIT, '_build', 'tools', 'fidelidade_uv.py'), '--master', a.master,
                    '--aov', os.path.join(d1, '0001.exr'), '--asset', p8, '--coat', a.coat, '--json', j1,
                    '--debug', os.path.join(d1, 'debug.png')], check=True, capture_output=True)
    r1 = json.load(open(j1))[0]
    r2 = json.load(open(j2))[0] if os.path.exists(j2) else {}
    k = ('tiles', 'worst_tile', 'p5_tile', 'hue_shift_deg', 'sat_ratio', 'pass')
    print('1x', json.dumps({x: r1.get(x) for x in k}), '| control', r1.get('control'))
    print('2x', json.dumps({x: r2.get(x) for x in k}), '| control', r2.get('control'))


if __name__ == '__main__':
    main()
