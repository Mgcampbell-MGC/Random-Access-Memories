import pandas as pd, re, unicodedata, json, glob, os, sys
rpi=sys.argv[1]
D=pd.read_pickle(f'inpi_{rpi}.pkl')
STOP=r'\b(LTDA|LIMITADA|ME|EPP|EIRELI|S ?A|SA|SLU|UNIPESSOAL|MEI|EM RECUPERACAO JUDICIAL)\b'
def key(s):
    s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().upper()
    s=re.sub(r'[^A-Z0-9 ]',' ',s); s=re.sub(STOP,' ',s); return re.sub(r'\s+',' ',s).strip()
def dv(c12):
    w1=[5,4,3,2,9,8,7,6,5,4,3,2]
    def d(b,w):
        r=sum(int(x)*y for x,y in zip(b,w))%11; return '0' if r<2 else str(11-r)
    a=d(c12,w1); return c12+a+d(c12+a,[6]+w1)
idx={}
def add(name,cnpj):
    k=key(name); c=re.sub(r'\D','',str(cnpj)).zfill(14)
    if k and len(c)==14 and c!='0'*14: idx.setdefault(k,set()).add(c)
cos=pd.read_pickle('../crm/cos.pkl')[['NO_RAZAO_SOCIAL_EMPRESA','NU_CNPJ_EMPRESA']].drop_duplicates()
for n,c in cos.itertuples(index=False): add(n,c)
for f in ['alim.csv','san.csv']:
    t=pd.read_csv(f,sep=';',encoding='latin-1',dtype=str,usecols=['NO_RAZAO_SOCIAL_EMPRESA','NU_CNPJ_EMPRESA']).drop_duplicates()
    for n,c in t.itertuples(index=False): add(n,c)
for f in glob.glob('../crm/reg/open/*.json'):
    try: j=json.load(open(f))
    except: continue
    if j.get('razao_social'): add(j['razao_social'],os.path.basename(f)[:14])
print('name index',len(idx))
out=[]
for r in D.itertuples():
    t=r.titular; m=re.match(r'^(\d{2})\.?(\d{3})\.?(\d{3})\s',t)
    if m: out.append((dv(''.join(m.groups())+'0001'),'MEI: CNPJ calculado do nome')); continue
    s=idx.get(key(t),set())
    if len(s)==1: out.append((next(iter(s)),'nome igual ao da empresa na ANVISA'))
    elif len(s)>1:
        mat=[c for c in s if c[8:12]=='0001']; out.append(((mat or sorted(s))[0],'nome igual (matriz) na ANVISA'))
    else: out.append(('',''))
D['cnpj']=[o[0] for o in out]; D['cnpj_origem']=[o[1] for o in out]
D.to_pickle(f'inpi_{rpi}_m.pkl')
print('with CNPJ',(D.cnpj!='').sum(),'of',len(D),' applicants',D[D.cnpj!=''].titular.nunique(),'of',D.titular.nunique())
print(D.cnpj_origem.value_counts().to_string())
open('need.txt','w').write('\n'.join(sorted(set(c for c in D.cnpj if c and not os.path.exists(f'../crm/reg/open/{c}.json')))))
print('to fetch',len(open('need.txt').read().split()))
