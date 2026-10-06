"""S01 · DIGITANDO (platform §E.2): a message typed, held, deleted letter by letter, replaced. 2D, no product.

    /home/user/venvs/web/bin/python _build/filmes/s01/s01.py [--teste]

Outputs:
  04_FILMES/S01_DIGITANDO_som.mp4 and _mudo.mp4        1080 × 1920, 24 fps, BT.709 converted and tagged
  04_FILMES/som/filmes/HLF-S01_DIGITANDO_som.wav + .json  −14 LUFS integrated, ≤ −1 dBTP, cue list with onsets
  06_PRODUCAO/filmes/HLF-S01_DIGITANDO.json               timeline, durations, loudness (no label: no fidelity check)

Timing is the platform's: 12 frames per word typed, an 18-frame hold on the half-typed "d", 2 frames per deleted
letter, 12 frames per word for "domingo tô aí.". Those counts alone sum to 202 frames (8,4 s), so the platform's
"6 s" cannot hold its own rhythm; the rhythm is the joke, so the film runs to the rhythm (see FILM_NOTE below).
The sign-off "holofote nela." lands on the first clap of HLF-ID-01 (one person's ovation).
"""
import json, os, subprocess, sys, shutil, argparse
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(KIT, '_build', 'sound'))
sys.path.insert(0, os.path.join(KIT, '_build', 'brand'))
import dsp  # noqa: E402

FPS = 24
NOME = 'HLF-S01_DIGITANDO'
M1 = 'mãe, você foi a melhor plateia d'
M2 = 'domingo tô aí.'
FILM_NOTE = ('The platform says 6 s; its own frame counts (12 f/word, 18 f hold, 2 f/letter deleted, 12 f/word) '
             'sum to 202 f = 8,4 s before the sign-off. Director: the rhythm wins; the film runs %0.2f s.')
UI = os.path.join(KIT, '_build', 'sound', '_fontes', 'kenney_ui', 'x', 'Audio')


def muro(path, seed=7):
    """O MURO's papel plaster, flat-lit from the upper left: papel #FFF8EC, three noise octaves at ±0,55 % (fine grain over a faint trowel cloud), a soft
    ±2,5 % light falloff. Subtle on purpose: it should read as a painted wall, never as a texture."""
    rng = np.random.default_rng(seed)
    h, w = 1920, 1080
    n = np.zeros((h, w), np.float32)
    for s, a in ((0.8, 0.55), (3, 0.35), (60, 0.25)):
        z = rng.standard_normal((h, w)).astype(np.float32)
        z = cv2.GaussianBlur(z, (0, 0), s)
        n += a * z / (z.std() + 1e-6)
    n = n / n.std() * 0.0055
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot((xx - 180) / w, (yy - 260) / h)
    light = 1.0 + 0.025 * (0.5 - d)
    base = np.array([0xEC, 0xF8, 0xFF], np.float32)          # BGR of #FFF8EC
    img = base[None, None, :] * (light * (1 + n))[..., None]
    cv2.imwrite(path, np.clip(img, 0, 255).astype(np.uint8))


def linha_do_tempo():
    """Per-frame state + the sound events (frame of each keystroke). Deterministic human jitter on keystrokes."""
    rng = np.random.default_rng(11)
    est, ev = [], []
    f = 0

    def idle(k, n1=0, n2=0, fase2=0, lock=0, caret_blink=True):
        nonlocal f
        for i in range(k):
            on = 1 if not caret_blink else (1 if ((f // 12) % 2 == 0) else 0)
            est.append(dict(n1=n1, n2=n2, fase2=fase2, lock=lock, caret=on))
            f += 1

    def digitar(texto, start_n, fase2):
        """12 frames per word (a word owns its trailing space); keystrokes spread inside the word with ±1 f jitter."""
        nonlocal f
        palavras, n = [], start_n
        cur = ''
        for ch in texto:
            cur += ch
            if ch == ' ':
                palavras.append(cur); cur = ''
        if cur:
            palavras.append(cur)
        for p in palavras:
            k = len(p)
            quando = [int(round(i * 12 / k)) for i in range(k)]
            quando = [min(11, max(0, q + (int(rng.integers(-1, 2)) if 0 < i < k - 1 else 0))) for i, q in enumerate(quando)]
            quando = sorted(set(quando)) if len(set(quando)) == k else [int(round(i * 12 / k)) for i in range(k)]
            for j in range(12):
                n_now = n + sum(1 for q in quando if q <= j)
                if j in quando:
                    ev.append(dict(f=f, tipo='tecla', ch=p[quando.index(j)]))
                est.append(dict(n1=0 if fase2 else n_now, n2=n_now if fase2 else 0, fase2=fase2, lock=0, caret=1))
                f += 1
            n += k
        return n

    idle(6)                                         # the empty wall, caret blinking
    n = digitar(M1, 0, 0)                           # 7 words × 12 f = 84 f
    hold0 = f
    idle(18, n1=n)                                  # 18 f on the half-typed "d"
    while n > 0:                                    # 2 f per deleted letter
        n -= 1
        ev.append(dict(f=f, tipo='apagar'))
        for _ in range(2):
            est.append(dict(n1=n, n2=0, fase2=0, lock=0, caret=1)); f += 1
    idle(6, fase2=1)
    n2 = digitar(M2, 0, 1)                          # 3 words × 12 f = 36 f
    idle(12, n2=n2, fase2=1)
    lock_f = f
    ev.append(dict(f=f, tipo='assinatura'))
    for _ in range(34):                             # sign-off: caret gone, lockup on
        est.append(dict(n1=0, n2=n2, fase2=1, lock=1, caret=0)); f += 1
    return est, ev, dict(hold_inicio=hold0, assinatura=lock_f, quadros=len(est))


def quadros(est, out_dir, teste=False):
    from playwright.sync_api import sync_playwright
    from render import CHROME
    os.makedirs(out_dir, exist_ok=True)
    for p in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, p))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--font-render-hinting=none', '--disable-lcd-text',
                                                             '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        msgs = []
        pg.on('console', lambda m: msgs.append(m.text) if m.type in ('error', 'warning') else None)
        pg.goto('file://' + os.path.join(HERE, 's01.html'))
        pg.wait_for_function('window.HF_PRONTO === true', timeout=60000)
        erro = pg.evaluate("document.body.getAttribute('data-erro')")
        if erro:
            raise RuntimeError(erro)
        info = pg.evaluate('window.HF_INFO')
        alvo = range(len(est)) if not teste else [0, 30, 89, 100, 140, 170, 200, 230, len(est) - 1]
        for i in alvo:
            pg.evaluate('e => window.quadro(e)', est[i])
            pg.screenshot(path=os.path.join(out_dir, 'q%04d.png' % i), clip=dict(x=0, y=0, width=1080, height=1920))
        b.close()
    if msgs:
        print('console:', msgs)
    return info


def grao(out_dir, seed=3):
    """Per-frame luminance grain, ±1,2 levels: keeps the flat papel from banding in H.264 and reads as a camera."""
    rng = np.random.default_rng(seed)
    for p in sorted(os.listdir(out_dir)):
        a = cv2.imread(os.path.join(out_dir, p)).astype(np.float32)
        g = rng.standard_normal(a.shape[:2]).astype(np.float32) * 1.2
        cv2.imwrite(os.path.join(out_dir, p), np.clip(a + g[..., None], 0, 255).astype(np.uint8))


def som(ev, n_quadros, wav, js):
    dur = n_quadros / FPS
    x = dsp.silence(dur + 0.25)
    rng = np.random.default_rng(5)
    teclas = [dsp.read(os.path.join(UI, f)) for f in ('click2.ogg', 'click4.ogg', 'click5.ogg', 'switch13.ogg',
                                                       'switch14.ogg')]
    # a soft fingertip on glass, not a game UI: lowpass, a touch of the room, quiet
    teclas = [dsp.lp(dsp.hp(t, 900), 5200) for t in teclas]
    apagar = [dsp.lp(dsp.pitch(t, -3.0), 3800) for t in teclas[2:4]]
    tom = dsp.read(os.path.join(KIT, '04_FILMES', 'som', 'sfx', 'HLF-SFX-15_tom_de_sala_loop.wav'))
    while len(tom) < len(x):
        tom = np.vstack([tom, tom])
    x = dsp.place(x, dsp.fade(tom[:len(x)], 0.4, 0.6), 0.0, gain_db=-14.0)
    cues = []
    for i, e in enumerate(ev):
        t = e['f'] / FPS
        if e['tipo'] == 'tecla':
            s = teclas[int(rng.integers(0, len(teclas)))]
            x = dsp.place(x, s, t, gain_db=-17.0 + float(rng.uniform(-1.5, 1.5)))
        elif e['tipo'] == 'apagar':
            s = apagar[i % 2]
            x = dsp.place(x, s, t, gain_db=-20.0 + float(rng.uniform(-1.0, 1.0)))
        elif e['tipo'] == 'assinatura':
            idw = dsp.read(os.path.join(KIT, '04_FILMES', 'som', 'identidade',
                                        'HLF-ID-01_vinheta_ovacao_de_uma_pessoa_so_2s0.wav'))
            t0 = t - 1.1005                       # its first clap, measured by the sound team, on the lockup frame
            x = dsp.place(x, idw, t0, gain_db=0.0)
            cues.append(dict(label='HLF-ID-01 (1ª palma no quadro da assinatura)', quadro=e['f'],
                             arquivo='identidade/HLF-ID-01_vinheta_ovacao_de_uma_pessoa_so_2s0.wav',
                             inicio_s=round(t0, 4), sync='onset'))
    x = x[:int(dur * dsp.SR)]
    x, _ = dsp.norm_mix(x, -14.0, -1.0)
    dsp.write(wav, x)
    li, tp = dsp.integrated(x), dsp.true_peak(x)
    # measured onset of the first clap against the lockup frame
    from onsets import onsets  # sound team's detector
    on = onsets(wav)
    lock_t = [e for e in ev if e['tipo'] == 'assinatura'][0]['f'] / FPS
    on = [o['t_s'] if isinstance(o, dict) else float(o) for o in on]
    near = min(on, key=lambda o: abs(o - lock_t)) if len(on) else None
    rep = dict(arquivo=os.path.basename(wav), duracao_s=round(len(x) / dsp.SR, 3), fps=FPS, lufs_i=round(li, 2),
               true_peak_dbtp=round(tp, 2), normalizacao='−14 LUFS integrado, ≤ −1 dBTP', cues=cues,
               teclas=sum(1 for e in ev if e['tipo'] == 'tecla'), apagadas=sum(1 for e in ev if e['tipo'] == 'apagar'),
               fontes_teclas='Kenney UI Audio (CC0): click2, click4, click5, switch13, switch14',
               quadros_chave=[dict(quadro=round(lock_t * FPS), onset_medido_s=round(near, 4) if near else None,
                                   desvio_quadros=round((near - lock_t) * FPS, 3) if near else None,
                                   ok=bool(near is not None and abs(near - lock_t) * FPS <= 1.0))])
    json.dump(rep, open(js, 'w'), ensure_ascii=False, indent=2)
    return rep


def mux(frames, wav, som_mp4, mudo_mp4):
    cod = os.path.join(KIT, '_build', 'tools', 'codificar.py')
    py = sys.executable
    subprocess.run([py, cod, frames, mudo_mp4, '--fps', str(FPS)], check=True)
    from codificar import ffmpeg  # noqa
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', mudo_mp4, '-i', wav, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', som_mp4],
                   check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--teste', action='store_true')
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, '_s01'), exist_ok=True)
    muro(os.path.join(HERE, '_s01', 'muro.png'))
    est, ev, marcos = linha_do_tempo()
    out = os.path.join(HERE, '_s01', 'quadros' if not a.teste else 'teste')
    info = quadros(est, out, teste=a.teste)
    print('layout', json.dumps(info, ensure_ascii=False))
    print('marcos', marcos, 'duração %.2f s' % (len(est) / FPS))
    if a.teste:
        return
    grao(out)
    sys.path.insert(0, os.path.join(KIT, '_build', 'tools'))
    fil = os.path.join(KIT, '04_FILMES')
    wav = os.path.join(fil, 'som', 'filmes', NOME + '_som.wav')
    js = os.path.join(fil, 'som', 'filmes', NOME + '_som.json')
    rep = som(ev, len(est), wav, js)
    filme = NOME.replace('HLF-', '')                 # films are named like the films team's (F06C_SINAL_07-05_som.mp4)
    mux(out, wav, os.path.join(fil, filme + '_som.mp4'), os.path.join(fil, filme + '_mudo.mp4'))
    prod = os.path.join(KIT, '06_PRODUCAO', 'filmes')
    os.makedirs(prod, exist_ok=True)
    json.dump(dict(filme=NOME, formato='9:16 1080×1920', fps=FPS, quadros=len(est),
                   duracao_s=round(len(est) / FPS, 3), marcos=marcos, layout=info,
                   nota=FILM_NOTE % (len(est) / FPS), som=rep, fidelidade='não se aplica (sem embalagem)'),
              open(os.path.join(prod, NOME + '.json'), 'w'), ensure_ascii=False, indent=2)
    print('ok', NOME, rep['lufs_i'], rep['true_peak_dbtp'], rep['quadros_chave'])


if __name__ == '__main__':
    main()
