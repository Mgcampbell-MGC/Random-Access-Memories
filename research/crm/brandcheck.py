import json, re, requests, unicodedata, concurrent.futures as cf
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
L=[json.loads(l) for l in open('disc_email.jsonl')]
def chk(d):
    if not d['i'] or 'brand_on_site' in d['i']: return d
    b=d['b']; u=d['i']['url']; txt=''
    try:
        r=requests.get(u,headers=UA,timeout=15,verify='/root/.ccr/ca-bundle.crt'); txt=r.text
        base=re.match(r'https?://[^/]+',r.url).group(0)
        for p in ['/search?q='+b.split()[0].lower(),'/busca?q='+b.split()[0].lower(),'/loja/busca.php?palavra_busca='+b.split()[0].lower()]:
            try:
                rr=requests.get(base+p,headers=UA,timeout=12,verify='/root/.ccr/ca-bundle.crt')
                if rr.status_code==200: txt+=rr.text
            except Exception: pass
    except Exception: pass
    d['i']['brand_on_site']= norm(b) in norm(txt)
    return d
with cf.ThreadPoolExecutor(24) as ex: L=list(ex.map(chk,L))
open('disc_email.jsonl','w').write(''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in L))
f=[d for d in L if d['i']]
print('email sites',len(f),'brand on site',sum(d['i']['brand_on_site'] for d in f))
for d in f[:15]: print(d['b'][:22],d['i']['url'][:40],d['i']['brand_on_site'])
