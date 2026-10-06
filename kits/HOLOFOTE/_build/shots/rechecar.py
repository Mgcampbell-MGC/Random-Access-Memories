"""Re-run the label check on delivered campanha finals from their kept AOV EXRs (no re-render), with the current
_build/tools/fidelidade_uv.py, through fid_multi.py (per-glass label_id masks), keeping glass_frac_altura and the
§D.7.5 thumbnail flag. Prints a table: piece · worst · p5 · control · pass.

    /home/user/venvs/web/bin/python _build/shots/rechecar.py [NAME ...]     (default: every campanha report)
"""
import glob, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
FID = os.path.join(KIT, '06_PRODUCAO', 'fidelidade')
WEB = '/home/user/venvs/web/bin/python'
COAT = {'01': '#FF4FA0', '02': '#FFE81A', '03': '#FF6A1A', '04': '#8424F5'}
INK = {'01': '#121014', '02': '#121014', '03': '#121014', '04': '#FFF8EC'}
CASE = {'CASE-01': '01', 'CASE-02': '02', 'CASE-03': '03'}
MINE = ('KV-01_', 'C01_', 'C02_', 'C04_', 'C05_', 'C06_', 'C08_', 'C10_', 'L0')


def faixa_de(master):
    n = os.path.basename(master)
    for k, f in CASE.items():
        if k in n:
            return f
    return n.split('HLF-')[1][:2]


def main(names):
    rows = []
    reps = sorted(glob.glob(os.path.join(FID, '*.json')))
    for jp in reps:
        base = os.path.basename(jp)[:-5]
        if not base.startswith(MINE) or 'portao' in base:
            continue
        shot = base.split('__')[0].replace('_1x_informativo', '')
        if names and shot not in names:
            continue
        old = json.load(open(jp))[0]
        # a 2x route's report of record (it carries 'verificacao') was taken on the 2x AOVs in aov/<shot>_2x
        adir = shot + ('_2x' if old.get('verificacao') else '')
        aov = os.path.join(HERE, 'aov', adir, '0001.exr')
        if not os.path.exists(aov):
            rows.append((base, 'sem AOV'))
            continue
        f = faixa_de(old['master'])
        cmd = [WEB, os.path.join(HERE, 'fid_multi.py'), '--master', old['master'], '--aov', aov, '--asset', old['asset'],
               '--coat', COAT[f], '--ink', INK[f], '--json', jp,
               '--debug', os.path.join(HERE, 'aov', adir, 'debug%s.png' % (base[len(shot):]))]
        if old.get('label_id') is not None:
            cmd += ['--id', str(old['label_id'])]
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            new = json.load(open(jp))[0]
        except Exception:
            rows.append((base, 'erro: ' + (r.stderr or r.stdout)[-300:]))
            continue
        new['glass_frac_altura'] = old.get('glass_frac_altura')
        new['thumbnail_sem_alegacao'] = old.get('thumbnail_sem_alegacao')
        for k in ('verificacao', 'nota'):
            if old.get(k):
                new[k] = old[k]
        json.dump([new], open(jp, 'w'), indent=2, ensure_ascii=False)
        c = new.get('control') or {}
        rows.append((base, new.get('worst_tile'), new.get('p5_tile'), c.get('worst_tile'), c.get('caught'),
                     new.get('hue_shift_deg'), new.get('sat_ratio'), new.get('pass'),
                     round(new['glass_frac_altura'], 3) if new.get('glass_frac_altura') else None,
                     new.get('thumbnail_sem_alegacao')))
    print('peça | worst | p5 | controle (caught) | hue | sat | pass | copo/altura | miniatura §D.7.5')
    for r in rows:
        print(' | '.join(str(x) for x in r))
    return rows


if __name__ == '__main__':
    main(sys.argv[1:])
