import json,pandas as pd
K=pd.read_pickle('brands_keep.pkl')
seen=set()
import glob
for f in ['disc.jsonl','disc_b.jsonl','disc_c.jsonl']+glob.glob('disc_d?.jsonl')+['disc_e.jsonl']:
    try:
        for l in open(f): seen.add(json.loads(l)['b'])
    except Exception: pass
print(len(seen & set(K.index)))
