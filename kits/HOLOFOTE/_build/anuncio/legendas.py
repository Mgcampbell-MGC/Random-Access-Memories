"""Word timings and caption pages for the 8 ad masters (platform §F.3).

Without an ASR on this machine, words are aligned to the VO by its own energy: the speech is split at its pauses
(Kokoro pauses at commas and full stops), clauses are matched to speech segments in order, and inside a segment each
word gets time in proportion to its vowel count. Good to about one syllable; the final voice replaces the temp VO and
must be re-aligned (re-run this file on the final WAVs).

    /home/user/venvs/web/bin/python legendas.py VO_DIR OUT.json
Captions: max 2 lines, <= 30 characters per line, one terminal mark per caption, the active word in amarelo.
Timeline: hook audio starts at 0,10 s; body at 2,05 s; KV line at 9,25 s (after the CLAC at 9,0).
"""
import json, os, re, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STARTS = {'gancho': 0.10, 'corpo': 2.05, 'kv_vo': 9.25}
VOG = re.compile(r'[aeiouáéíóúâêôãõàü]', re.I)


def read(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    return x, sr


def segments(x, sr, hop=0.01, gap=0.07):
    n = int(hop * sr)
    env = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)])
    thr = max(env.max() * 0.06, 1e-4)
    on = env > thr
    segs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            segs.append([i * hop, j * hop])
            i = j
        else:
            i += 1
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < gap:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [s for s in merged if s[1] - s[0] > 0.04]


def clauses(text):
    parts = re.split(r'(?<=[,.:;!?])\s+', text.strip())
    return [p.split() for p in parts if p]


def weight(w):
    return max(1, len(VOG.findall(w))) + 0.15 * len(w)


def align(text, x, sr):
    """Spread words over the speech span by weight, then snap every clause boundary to the nearest detected pause
    (within 0,25 s); words inside a clause are re-spread between its snapped edges."""
    cl = clauses(text)
    segs = segments(x, sr)
    if not segs:
        return []
    a0, a1 = segs[0][0], segs[-1][1]
    pauses = [((segs[i][1] + segs[i + 1][0]) / 2, segs[i][1], segs[i + 1][0]) for i in range(len(segs) - 1)]
    W = [[weight(w) for w in c] for c in cl]
    tot = sum(map(sum, W))
    edges, acc = [a0], 0.0
    for c in W[:-1]:
        acc += sum(c)
        t = a0 + (a1 - a0) * acc / tot
        if pauses:
            m, e0, e1 = min(pauses, key=lambda p: abs(p[0] - t))
            if abs(m - t) < 0.25:
                edges.append((e0, e1))
                continue
        edges.append((t, t))
    edges.append(a1)
    out = []
    for i, words in enumerate(cl):
        s0 = edges[i] if i == 0 else edges[i][1]
        s1 = edges[i + 1] if i + 1 == len(cl) else edges[i + 1][0]
        ws = W[i]
        t = s0
        for w, k in zip(words, ws):
            d = (s1 - s0) * k / sum(ws)
            out.append(dict(palavra=w, t0=round(t, 3), t1=round(t + d, 3)))
            t += d
    return out


SHORT = {'a', 'à', 'o', 'e', 'de', 'da', 'do', 'na', 'no', 'em', 'um', 'pra', 'que', 'te', 'o', 'é'}


def split_lines(words, max_chars=30):
    """Best 1- or 2-line layout of a page: balanced, no line ending on a short function word."""
    txt = ' '.join(w['palavra'] for w in words)
    if len(txt) <= max_chars:
        return [txt]
    best = None
    for i in range(1, len(words)):
        l1 = ' '.join(w['palavra'] for w in words[:i])
        l2 = ' '.join(w['palavra'] for w in words[i:])
        if len(l1) > max_chars or len(l2) > max_chars:
            continue
        pen = abs(len(l1) - len(l2)) + (25 if words[i - 1]['palavra'].lower().strip(',.') in SHORT else 0)
        if best is None or pen < best[0]:
            best = (pen, [l1, l2])
    return best[1] if best else None


def pages(words, max_chars=30):
    """Pages close on a terminal mark; a clause too long for two lines splits at its best comma or midpoint."""
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        if re.search(r'[.!?…]$', w['palavra']):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    res = []
    while groups:
        g = groups.pop(0)
        lines = split_lines(g, max_chars)
        if lines is None:
            cut = next((i + 1 for i in range(len(g) - 1, 0, -1) if g[i]['palavra'].endswith(',') and
                        split_lines(g[:i + 1], max_chars)), len(g) // 2)
            groups[:0] = [g[:cut], g[cut:]]
            continue
        res.append(dict(linhas=lines, palavras=g, t0=g[0]['t0'], t1=g[-1]['t1']))
    return res


def main(vo_dir, out):
    R = json.load(open(os.path.join(HERE, 'roteiros.json')))['cortes']
    res = {}
    for cut, r in R.items():
        allw = {}
        for part, t0 in STARTS.items():
            x, sr = read(os.path.join(vo_dir, f'{cut}_{part}.wav'))
            ws = align(r[part], x, sr)
            for w in ws:
                w['t0'] = round(w['t0'] + t0, 3)
                w['t1'] = round(w['t1'] + t0, 3)
            allw[part] = dict(inicio_audio_s=t0, palavras=ws, paginas=pages(ws))
        res[cut] = allw
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
    for cut, v in res.items():
        print(cut, [len(v[p]['paginas']) for p in STARTS], [pg['linhas'] for pg in v['corpo']['paginas']])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
