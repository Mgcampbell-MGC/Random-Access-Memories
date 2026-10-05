import pandas as pd, re, requests, unicodedata, json, sys, os, html, concurrent.futures as cf
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36','Accept-Language':'pt-BR,pt;q=0.9'}
CA='/root/.ccr/ca-bundle.crt'
K=pd.read_pickle('brands_keep.pkl').sort_values('n_new',ascending=False)
SH=int(sys.argv[1]); OUT=f'disc_d{SH}.jsonl'
done=set()
import glob
for f_ in ['disc.jsonl','disc_b.jsonl','disc_c.jsonl']+glob.glob('disc_d*.jsonl'):
  if os.path.exists(f_):
    for l in open(f_):
        try: done.add(json.loads(l)['b'])
        except: pass
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
GENW=set('COSMETICOS COSMETICS BEAUTY PROFESSIONAL PROFISSIONAL SKIN HAIR CARE BRASIL OFICIAL MAKE PERFUMES PARFUM'.split())
def bases(b,full):
    out=[norm(b),norm(full)]
    t=[x for x in b.split() if x not in GENW]
    if t and len(norm(t[0]))>=5: out.append(norm(t[0]))
    if len(t)>=2: out.append(norm(' '.join(t[:2])))
    return [s for s in dict.fromkeys(out) if len(s)>=3]
def variants(s,cat,pro):
    v=[s,s+'cosmeticos','use'+s,s+'oficial',s+'beauty',s+'cosmetics',s+'store','loja'+s,s+'brasil']
    v+={'face':[s+'skin',s+'skincare'],'hair':[s+'hair',s+'cabelos'],'fragrance':[s+'perfumes',s+'parfum'],'makeup':[s+'make',s+'makeup'],'body':[s+'body'],'soap':[s+'saboaria'],'deo':[]}.get(cat,[])
    if pro: v+=[s+'professional',s+'profissional']
    return list(dict.fromkeys(v))
KWS=['cabelo','pele','shampoo','skincare','hidratante','cosmetic','cosmétic','beleza','capilar','corporal','sérum','serum','cachos','condicionador','máscara','body','creme','maquiagem','batom','perfume','fragr','parfum','colônia','make','sabonete','splash','beauty','cosmétic']
BAD=re.compile(r'for sale|à venda|slot|casino|gacor|parked|hostinger|index of|godaddy|domain is|domínio|em breve.*domínio',re.I)
S=requests.Session()
ad=requests.adapters.HTTPAdapter(pool_connections=100,pool_maxsize=100); S.mount('https://',ad)
def fetch(u,t=8):
    try: return S.get(u,headers=UA,timeout=t,verify=CA,allow_redirects=True)
    except Exception: return None
def valid(key,r):
    t=r.text[:800000]; tl=t.lower()
    m=re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I); title=html.unescape(m.group(1).strip()) if m else ''
    og=re.search(r'og:site_name["\']\s+content=["\']([^"\']+)',t)
    host=norm(re.sub(r'^https?://','',r.url).split('/')[0])
    head=norm(title+' '+(og.group(1) if og else '')+' '+host)
    kw=sum(1 for k in KWS if k in tl)
    if BAD.search(title) or re.search(r'this domain|este dom[ií]nio|domain for sale|buy this domain|parked free',tl[:20000]): return None
    br=bool(re.search(r'R\$|lang=["\']pt|pt-br|frete|cnpj|\.com\.br|parcel|carrinho|sacola|comprar',tl[:800000]))
    if key in head and kw>=3 and br: return title or host
    return None
def check(b,full,cat,pro):
    key=norm(b)
    for s in bases(b,full):
        for v in variants(s,cat,pro):
            for tld in ['.com.br','.com']:
                for pre in ['https://','https://www.']:
                    r=fetch(pre+v+tld+'/')
                    if r is None: continue
                    if r.status_code>=400: break
                    ti=valid(key,r)
                    if ti is not None: return r,ti
                    break
    s=bases(b,full)[0]
    for host in [s+'.lojavirtualnuvem.com.br',s+'.myshopify.com',s+'.lojaintegrada.com.br',s+'.commercesuite.com.br']:
        r=fetch('https://'+host+'/')
        if r is not None and r.status_code<400:
            ti=valid(key,r)
            if ti is not None: return r,ti
    return None,None
CNPJRE=re.compile(r'CNPJ[^0-9]{0,40}(\d{2}\.?\d{3}\.?\d{3}\s?/?\s?\d{4}\s?-?\s?\d{2})',re.I)
CNPJF=re.compile(r'\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b')
def contacts(t):
    t2=t.replace('\\/','/')
    cn=[re.sub(r'\D','',x) for x in CNPJRE.findall(t2)]+[re.sub(r'\D','',x) for x in CNPJF.findall(t2)]
    em=[e for e in re.findall(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+',t2) if not re.search(r'\.(png|jpg|jpeg|webp|gif|svg|js|css)$|sentry|example|wixpress|shopify|@2x|@3x|nuvemshop|tiendanube|domain\.com|email\.com|seuemail|u00|lojaintegrada|vtex|tray\.com|yampi|cloudflare|godaddy|wordpress|woocommerce|sentry|jquery|bootstrap',e,re.I)]
    ig=[x for x in re.findall(r'instagram\.com/([A-Za-z0-9_.]+)',t2) if x.lower() not in ('p','reel','reels','explore','accounts','stories','tv','direct','_u','sharer','share')]
    wa=re.findall(r'(?:wa\.me/\+?|api\.whatsapp\.com/send/?\?phone=\+?|web\.whatsapp\.com/send\?phone=\+?|whatsapp\.com/send\?phone=\+?)(\d{10,13})',t2)
    tel=re.findall(r'tel:\+?([\d\s\-\(\)]{10,20})',t2)
    tel=[re.sub(r'\D','',x) for x in tel]
    return cn,em,ig,wa,tel
def plat(t):
    return ','.join(k for k,p in [('shopify','cdn.shopify.com'),('nuvemshop','mitiendanube|nuvemshop|tiendanube'),('vtex','vteximg|vtexassets'),('tray','tcdn.com.br|traycdn|tray.com.br'),('lojaintegrada','lojaintegrada'),('woocommerce','woocommerce'),('wix','wixstatic'),('yampi','yampi'),('magazord','magazord')] if re.search(p,t,re.I))
def work(b,r0):
    r,ti=check(b,r0.fullphrase,r0.main_cat,bool(r0.pro))
    if r is None: return None
    base=re.match(r'https?://[^/]+',r.url).group(0)
    allt=r.text
    for p in ['/pages/contato','/contato','/institucional/contato','/fale-conosco','/pages/fale-conosco','/pages/quem-somos','/quem-somos','/policies/terms-of-service','/politica-de-privacidade']:
        if CNPJRE.search(allt) and '@' in allt and ('wa.me' in allt or 'whatsapp' in allt.lower()): break
        rr=fetch(base+p,8)
        if rr is not None and rr.status_code==200 and len(rr.text)<3000000: allt+=rr.text
    cn,em,ig,wa,tel=contacts(allt)
    u=lambda x: list(dict.fromkeys(x))
    return dict(url=r.url,title=str(ti)[:120],platform=plat(r.text),cnpjs=u(cn)[:4],emails=u(e.lower() for e in em)[:6],ig=u(ig)[:4],wa=u(wa)[:3],tel=u(tel)[:3])
out=open(OUT,'a')
items=[(b,r) for b,r in K.iterrows() if b not in done]
items=items[SH::3]
print('to do',len(items),flush=True)
with cf.ThreadPoolExecutor(48) as ex:
    futs={ex.submit(work,b,r):b for b,r in items}
    n=0
    for fu in cf.as_completed(futs):
        b=futs[fu]
        try: i=fu.result()
        except Exception as e: i=None
        out.write(json.dumps({'b':b,'i':i},ensure_ascii=False)+'\n'); out.flush()
        n+=1
        if n%100==0: print(n,flush=True)
print('done',flush=True)
