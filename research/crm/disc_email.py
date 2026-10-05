import pandas as pd, json, re, os, sys, concurrent.futures as cf
sys.argv=['x']; 
exec(open('disc.py').read().split("out=open(OUT,'a')")[0].replace("K=pd.read_pickle('brands_keep.pkl').sort_values('n_new',ascending=False)","K=pd.read_pickle('brands_keep.pkl')"))
D=pd.read_pickle('final.pkl')
FREE=re.compile(r'(gmail|hotmail|outlook|yahoo|live|icloud|uol|bol|terra|ig|msn|globo|r7|zipmail)\.',re.I)
ACC=re.compile(r'contab|contador|escritorio|assessoria|consultoria|fiscal|tribut|legaliza',re.I)
done=set()
if os.path.exists('disc_email.jsonl'):
    for l in open('disc_email.jsonl'): done.add(json.loads(l)['b'])
items=[]
for _,r in D[(D.site=='')&(D.cnpj!='')].iterrows():
    doms=[]
    for e in [r.email]+re.findall(r'[\w.+-]+@[\w.-]+',r.outros_email):
        if not e or '@' not in e: continue
        d=e.split('@')[1].lower()
        if FREE.search(d) or ACC.search(d) or 'CONTADOR' in r.email_origem: continue
        doms.append(d)
    if doms and r.marca.upper() not in done: items.append((r.marca.upper(),list(dict.fromkeys(doms))[:2]))
print('candidates',len(items),flush=True)
def work(it):
    b,doms=it
    for d in doms:
        for pre in ['https://','https://www.']:
            r=fetch(pre+d+'/')
            if r is None or r.status_code>=400: continue
            tl=r.text[:800000].lower()
            kw=sum(1 for k in KWS if k in tl and k not in ('body','make'))
            if kw<2: break
            base=re.match(r'https?://[^/]+',r.url).group(0); allt=r.text
            for p in ['/contato','/pages/contato','/fale-conosco','/quem-somos']:
                rr=fetch(base+p,8)
                if rr is not None and rr.status_code==200 and len(rr.text)<3000000: allt+=rr.text
            cn,em,ig,wa,tel=contacts(allt)
            u=lambda x: list(dict.fromkeys(x))
            return b,dict(url=r.url,title='(domínio do e-mail da empresa)',platform=plat(r.text),cnpjs=u(cn)[:4],emails=u(e.lower() for e in em)[:6],ig=u(ig)[:4],wa=u(wa)[:3],tel=u(tel)[:3],via='email')
    return b,None
out=open('disc_email.jsonl','a')
with cf.ThreadPoolExecutor(24) as ex:
    for b,i in ex.map(work,items):
        out.write(json.dumps({'b':b,'i':i},ensure_ascii=False)+'\n'); out.flush()
print('found',sum(1 for l in open('disc_email.jsonl') if '"i": {' in l))
