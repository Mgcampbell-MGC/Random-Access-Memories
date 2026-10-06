"""campanha.py's 2x route, for any plate (also the multi-glass ones): the director's reduzir_2x.py method without its
single-label check. Moves the 200 % outputs aside (<stem>_2x_16bit.png, <stem>_2x.png, aov/<name>_2x/) and writes the
1x plate (INTER_AREA from the 16-bit master) and the 1x AOVs (2 x 2 box filter of every channel: the AOVs are
pixel-filtered, so the box average is exactly what a 1x render would have written). campanha.foto then runs the label
check twice: on the 2x outputs (<name>_2x[__copo].json) and on the 1x deliverable (<name>[__copo].json).

    /home/user/venvs/web/bin/python _build/shots/reduzir_multi.py <name> <stem>
"""
import os, shutil, sys
import numpy as np
import cv2
import OpenEXR

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
R = os.path.join(KIT, '02_PRODUTO', 'renders')
AOV = os.path.join(HERE, 'aov')


def box(a):
    h, w = a.shape[:2]
    a = a[:h - h % 2, :w - w % 2]
    return a.reshape(h // 2, 2, w // 2, 2, *a.shape[2:]).mean(axis=(1, 3)).astype(a.dtype)


def main(name, stem):
    p16, p8 = os.path.join(R, stem + '_16bit.png'), os.path.join(R, stem + '.png')
    q16, q8 = os.path.join(R, stem + '_2x_16bit.png'), os.path.join(R, stem + '_2x.png')
    big = cv2.imread(p16, cv2.IMREAD_UNCHANGED)
    assert big is not None and big.dtype == np.uint16, p16
    shutil.move(p16, q16)
    shutil.move(p8, q8)
    small = cv2.resize(big, (big.shape[1] // 2, big.shape[0] // 2), interpolation=cv2.INTER_AREA)
    cv2.imwrite(p16, small)
    cv2.imwrite(p8, (small.astype(np.float64) / 257.0).round().clip(0, 255).astype(np.uint8))
    d1, d2 = os.path.join(AOV, name), os.path.join(AOV, name + '_2x')
    if os.path.isdir(d1):
        if os.path.isdir(d2):
            shutil.rmtree(d2)
        shutil.move(d1, d2)
        f = OpenEXR.File(os.path.join(d2, '0001.exr'))
        part = f.parts[0]
        chans = {k: box(v.pixels) for k, v in part.channels.items()}
        hdr = {k: v for k, v in part.header.items() if k in ('compression', 'type', 'lineOrder')}
        os.makedirs(d1, exist_ok=True)
        OpenEXR.File(hdr, chans).write(os.path.join(d1, '0001.exr'))
    print('2x -> 1x', big.shape[1], 'x', big.shape[0], '->', small.shape[1], 'x', small.shape[0], flush=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
