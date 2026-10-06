"""Temporary VO for the 8 ad masters (Kokoro, local; the platform's licensed synthetic voice replaces it in production).
Each line is fitted to its window: hook <= 1,85 s, body <= 3,85 s, KV line <= 1,6 s, by adjusting speech rate only.
    /home/user/venvs/kokoro/bin/python vo.py OUTDIR
Writes <cut>_<part>.wav (48 kHz mono) and vo_tempos.json (duration and speed per line)."""
import json, os, sys
import numpy as np
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
TTS = '/home/user/maes_build/tts'
VOZ = {'H01': 'pf_dora', 'H02': 'pm_alex'}
JANELA = {'gancho': 1.85, 'corpo': 3.85, 'kv_vo': 1.6}


def resample(x, sr, to=48000):
    t0 = np.arange(len(x)) / sr
    t1 = np.arange(int(len(x) * to / sr)) / to
    return np.interp(t1, t0, x).astype(np.float32)


def wav(path, x, sr=48000):
    import wave
    y = np.clip(x, -1, 1)
    y = (y * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes())


def main(out):
    os.makedirs(out, exist_ok=True)
    k = Kokoro(os.path.join(TTS, 'kokoro-v1.0.onnx'), os.path.join(TTS, 'voices-v1.0.bin'))
    R = json.load(open(os.path.join(HERE, 'roteiros.json')))['cortes']
    log = {}
    for cut, r in R.items():
        for part in ('gancho', 'corpo', 'kv_vo'):
            txt = r[part]
            speed = 1.0
            for _ in range(8):
                a, sr = k.create(txt, voice=VOZ[r['apresentador']], speed=speed, lang='pt-br')
                dur = len(a) / sr
                if dur <= JANELA[part]:
                    break
                speed = min(1.6, speed * dur / JANELA[part] * 1.02)
            y = resample(a, sr)
            y = y / (np.abs(y).max() + 1e-9) * 0.7
            p = os.path.join(out, f'{cut}_{part}.wav')
            wav(p, y)
            log[f'{cut}_{part}'] = dict(texto=txt, voz=VOZ[r['apresentador']], velocidade=round(speed, 3), duracao_s=round(dur, 3),
                                        janela_s=JANELA[part], cps=round(len(txt) / dur, 1))
            print(cut, part, round(dur, 2), 's at', round(speed, 2))
    json.dump(log, open(os.path.join(out, 'vo_tempos.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
