import pandas as pd, re, collections, pickle, sys
sys.path.insert(0,'.')
from cats import cls
d=pd.read_pickle('cos.pkl')
w=pd.read_pickle('win90.pkl')
w['cat']=w.N.map(cls)
print(w.cat.value_counts().to_string())
INC={'hair','face','body','soap','deo','makeup','fragrance'}
GEN=set('COSMETICOS COSMETICO COSMETICS COSMETIC COSMETIQUE COSMETICA COSMETICAS PROFESSIONAL PROFISSIONAL PROFISSIONAIS PROFESSIONALS PROFESIONAL PROFESSIONNEL PRO BEAUTY CARE BRASIL BRAZIL LTDA OFICIAL OFFICIAL LINE LINHA DE DA DO DAS DOS E EM PARA COM SEM ML G KG L LT GR UN BY THE AND OF & | + HAIRCARE SKINCARE INDUSTRIA COMERCIO EPP ME COLLECTION COLECAO HOME CARE NATURAL NATURAIS VEGAN VEGANO VEGANA LAB LABS LABORATORIO LABORATORIOS BIO BIOCOSMETICOS DERMOCOSMETICOS NANOCOSMETICOS NANO MAKE MAKEUP PERFUMES PERFUMARIA PARFUM PARFUMS FRAGRANCES'.split())
TYPE=set('SHAMPOO XAMPU CONDICIONADOR MASCARA LEAVE IN CREME OLEO SERUM SORO TONICO LOCAO GEL SABONETE AMPOLA FINALIZADOR SPRAY HIDRATANTE PROTETOR ESFOLIANTE POMADA MOUSSE ATIVADOR KIT FLUIDO BALM RECONSTRUTOR AGUA BRUMA ELIXIR REPARADOR GELATINA EMULSAO PROTEINA UMECTANTE COMPLEXO CAPILAR CORPORAL FACIAL HIDRATACAO NUTRICAO RECONSTRUCAO MANTEIGA LIMPEZA ESPUMA CONDICIONANTE BODY LOTION CREAM BUTTER OIL SCRUB MASK WASH TREATMENT CLEANSER TONER ESSENCE AMPOULE DEFINIDOR MODELADOR MODELADORA CERA TRATAMENTO BANHO CACHOS CABELOS CABELO FIOS PELE ROSTO MAOS PES CURLS HAIR SKIN BATOM GLOSS BLUSH SOMBRA BASE CORRETIVO PO DELINEADOR LAPIS PALETA ILUMINADOR PRIMER PERFUME COLONIA DEO DESODORANTE SPLASH EAU TOILETTE EDP EDT MIST'.split())
def T(n):
    n=re.sub(r'[^A-Z0-9&+ ]',' ',n.replace(' - ',' | ').replace(' – ',' | ').replace('-',' '))
    return [x for x in n.split() if not re.match(r'^\d+([.,]\d+)?(ML|G|GR|KG|L|LT|MG|UN|X|%|OZ|FL)?$',x)]
def cands(n):
    t=T(n); c=set()
    segs=[s.split() for s in ' '.join(t).split('|')]; segs=[s for s in segs if s]
    tt=[x for x in t if x!='|']
    u=tt[:]
    while u and u[-1] in GEN: u=u[:-1]
    for k in (1,2,3,4):
        if len(u)>=k:
            g=u[-k:]
            if g[0] not in GEN: c.add(' '.join(g))
    for k in (1,2,3):
        if len(tt)>=k and tt[0] not in GEN: c.add(' '.join(tt[:k]))
    if len(segs)>1:
        for s in (segs[0],segs[-1]):
            s2=s[:]
            while s2 and s2[-1] in GEN: s2=s2[:-1]
            if 1<=len(s2)<=5 and s2[0] not in GEN: c.add(' '.join(s2))
    return c
w['cands']=w.N.map(cands)
allc=set().union(*w.cands.values); maxk=max(len(x.split()) for x in allc)
ph_hold=collections.defaultdict(set); ph_hc=collections.Counter()
for c,toks_ in zip(d.NU_CNPJ_EMPRESA.values,d['T'].values):
    tt=[re.sub(r'[^A-Z0-9&+]','',x) for x in toks_ if x not in ('-','–')]; tt=[x for x in tt if x]
    seen=set(); L=len(tt)
    for i in range(L):
        for k in range(1,min(maxk,L-i)+1):
            p=' '.join(tt[i:i+k])
            if p in allc and p not in seen:
                seen.add(p); ph_hold[p].add(c); ph_hc[(c,p)]+=1
pspread={p:len(v) for p,v in ph_hold.items()}
def core(p):
    t=p.split()
    while t and t[-1] in GEN: t=t[:-1]
    while t and t[0] in GEN: t=t[1:]
    return ' '.join(t)
def pick(row):
    best=None;bs=None
    for p in row.cands:
        toks=p.split()
        if any(x in TYPE for x in toks): continue
        h=ph_hc.get((row.NU_CNPJ_EMPRESA,p),0); s=pspread.get(p,999)
        if s>25 or h<2: continue
        if not core(p): continue
        sc=(h,len(toks))
        if bs is None or sc>bs: bs=sc;best=p
    return best
w['brand']=w.apply(pick,axis=1)
w['bkey']=w.brand.map(lambda p: core(p) if isinstance(p,str) else None)
print('unparsed share (all window rows)',round(w.brand.isna().mean(),3))
w.to_pickle('win_b.pkl')
# refile detection
def ts(n):
    n=re.sub(r'[^A-Z0-9 ]',' ',n)
    return frozenset(x for x in n.split() if x not in GEN and not re.match(r'^\d+([.,]\d+)?(ML|G|GR|KG|L|LT|MG|UN|X|OZ|FL)?$',x))
pre=d[~d.index.isin(set(w.index))]
pre_ts=pre.N.map(ts)
preset=collections.Counter(pre_ts.values)
tokidx=collections.defaultdict(set)
for i,s in zip(pre.index.values,pre_ts.values):
    for t in s: tokidx[t].add(i)
pts=pre_ts.to_dict()
wi=w[w.cat.isin(INC)].copy()
wi['ts']=wi.N.map(ts)
wi['refile_exact']=wi.ts.map(lambda s: preset.get(s,0)>0)
def fuzzy(row):
    if row.refile_exact: return True
    if not isinstance(row.bkey,str): return False
    bt=[t for t in re.sub(r'[^A-Z0-9 ]',' ',row.bkey).split() if t not in GEN]
    if not bt: return False
    cand=None
    for t in bt:
        s=tokidx.get(t,set()); cand=s if cand is None else cand&s
        if not cand: return False
    rest=row.ts-set(bt)
    if not rest: return False
    for i in cand:
        o=pts[i]-set(bt)
        if o and len(rest&o)/len(rest|o)>=0.75: return True
    return False
wi['refile']=wi.apply(fuzzy,axis=1)
print('included rows',len(wi),' refile share',round(wi.refile.mean(),3))
fs={}
for b in wi.bkey.dropna().unique():
    bt=[t for t in re.sub(r'[^A-Z0-9 ]',' ',b).split() if t not in GEN]
    cand=None
    for t in bt:
        s=tokidx.get(t,set()); cand=s if cand is None else cand&s
    if not cand: fs[b]=(None,0); continue
    dd=d.loc[list(cand)]; fs[b]=(dd.notif.min(),len(dd))
wi['brand_first_pre']=wi.bkey.map(lambda b: fs.get(b,(None,0))[0] if isinstance(b,str) else None)
wi['brand_pre_n']=wi.bkey.map(lambda b: fs.get(b,(None,0))[1] if isinstance(b,str) else 0)
hb=w.dropna(subset=['bkey']).groupby('NU_CNPJ_EMPRESA').bkey.nunique()
wi['holder_nbrands']=wi.NU_CNPJ_EMPRESA.map(hb).fillna(0).astype(int)
wi.to_pickle('win_inc.pkl')
print('done')
