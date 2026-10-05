import pandas as pd, json, re, os, sys, concurrent.futures as cf, unicodedata
src=open('disc.py').read().split("out=open(OUT,'a')")[0].replace("K=pd.read_pickle('brands_keep.pkl').sort_values('n_new',ascending=False)","K=pd.read_pickle('brands_keep.pkl')")
exec(src)
D=pd.read_pickle('final.pkl')
targets=D[(D.site=='')&(D.n_new>=2)&(~D.alertas.str.contains('importadora|estrangeiro'))].sort_values('n_new',ascending=False)
done=set()
if os.path.exists('disc2.jsonl'):
    for l in open('disc2.jsonl'): done.add(json.loads(l)['b'])
items=[m.upper() for m in targets.marca if m.upper() not in done and m.upper() in K.index]
print('targets',len(items),flush=True)
def amp(b): return norm(b.replace('&',' E '))
def check2(b):
    r0=K.loc[b]; key=norm(b); out=[]
    for s in dict.fromkeys([amp(b)]+bases(b,r0.fullphrase)):
        v=[s+'shop',s+'online','sou'+s,'meu'+s,s+'br',s+'loja',s+'cosmetico',s+'beautybr',s+'cosmeticosoficial']
        if r0.main_cat=='fragrance': v+=[s+'perfumaria',s+'parfums',s+'fragrancias',s+'perfume']
        if r0.main_cat=='makeup': v+=[s+'makeoficial',s+'cosmeticosmake']
        if s==amp(b) and s!=norm(b): v=[s]+v
        for vv in v:
            for tld in ['.com.br','.net.br','.shop','.store']:
                for pre in ['https://','https://www.']:
                    r=fetch(pre+vv+tld+'/')
                    if r is None: continue
                    if r.status_code>=400: break
                    if valid(key,r) or (s==amp(b) and valid(s,r)): return r
                    break
    return None
def work(b):
    r=check2(b)
    if r is None: return b,None
    base=re.match(r'https?://[^/]+',r.url).group(0); allt=r.text
    for p in ['/pages/contato','/contato','/fale-conosco','/quem-somos','/policies/terms-of-service']:
        rr=fetch(base+p,8)
        if rr is not None and rr.status_code==200 and len(rr.text)<3000000: allt+=rr.text
    cn,em,ig,wa,tel=contacts(allt)
    u=lambda x: list(dict.fromkeys(x))
    return b,dict(url=r.url,title='(2ª rodada)',platform=plat(r.text),cnpjs=u(cn)[:4],emails=u(e.lower() for e in em)[:6],ig=u(ig)[:4],wa=u(wa)[:3],tel=u(tel)[:3])
out=open('disc2.jsonl','a')
with cf.ThreadPoolExecutor(48) as ex:
    for b,i in ex.map(work,items):
        out.write(json.dumps({'b':b,'i':i},ensure_ascii=False)+'\n'); out.flush()
print('found',sum(1 for l in open('disc2.jsonl') if '"i": {' in l))
