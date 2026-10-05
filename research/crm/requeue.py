import pandas as pd, json, collections, os
K=pd.read_pickle('brands_keep.pkl')
wb=pd.read_pickle('win_b.pkl')
HNB={str(c).zfill(14):n for c,n in wb.dropna(subset=['bkey']).groupby('NU_CNPJ_EMPRESA').bkey.nunique().items()}
RV=json.load(open('reval_all.json')) if os.path.exists('reval_all.json') else {}
site_owner=collections.OrderedDict()
for f_ in ['disc.jsonl','disc_b.jsonl','disc_c.jsonl','disc_d0.jsonl','disc_d1.jsonl','disc_d2.jsonl','disc_e.jsonl','disc2.jsonl']:
    if not os.path.exists(f_): continue
    for l in open(f_):
        d=json.loads(l)
        if d['i'] and d['i'].get('cnpjs') and (d['b'] not in RV or RV[d['b']].get('ok')):
            for c in d['i']['cnpjs'][:2]:
                if len(c)==14: site_owner[c]=d['b']
sc=collections.defaultdict(float)
for b,r in K.iterrows():
    for h in r.holders.split('|'):
        h=h.zfill(14); sc[h]=max(sc[h],r.n_new)
own=[h for h in sorted(sc,key=lambda h:-sc[h]) if HNB.get(h,99)<=15]
makers=[h for h in sorted(sc,key=lambda h:-sc[h]) if HNB.get(h,99)>15]
q=list(dict.fromkeys(list(site_owner)+own+makers))
eq=list(dict.fromkeys(list(site_owner)+own))
for f,L in [('queue.txt',q),('equeue.txt',eq)]:
    open(f+'.tmp','w').write('\n'.join(L)+'\n'); os.replace(f+'.tmp',f)
print('queue',len(q),'email queue',len(eq),'(site owners',len(site_owner),', holders with <=15 brands',len(own),', makers skipped for e-mail',len(makers),')')
