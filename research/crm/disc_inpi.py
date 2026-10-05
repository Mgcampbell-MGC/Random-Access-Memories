import pandas as pd, re, unicodedata, json, html, os, sys, requests, concurrent.futures as cf
rpi=sys.argv[1]
D=pd.read_pickle(f'inpi_{rpi}_m.pkl')
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36','Accept-Language':'pt-BR,pt;q=0.9'}
CA='/root/.ccr/ca-bundle.crt'
S=requests.Session(); S.mount('https://',requests.adapters.HTTPAdapter(pool_connections=200,pool_maxsize=200))
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
def fetch(u,t=(3,8)):
    try: return S.get(u,headers=UA,timeout=t,verify=CA,allow_redirects=True)
    except Exception: return None
KW=['cabelo','pele','shampoo','skincare','hidratante','cosmétic','cosmetic','beleza','capilar','corporal','sérum','serum','perfume','fragr','maquiagem','sabonete','suplement','colágeno','colageno','vitamina','cápsula','capsula','whey','creatina','vela','difusor','aroma']
BAD=re.compile(r'for sale|à venda|slot|casino|gacor|parked|hostinger|index of|godaddy|domain|domínio',re.I)
CNPJF=re.compile(r'(\d{2}\.?\d{3}\.?\d{3}\s?/?\s?\d{4}\s?-?\s?\d{2})')
def cnpj_ok(c):
    if len(c)!=14 or len(set(c))==1: return False
    w1=[5,4,3,2,9,8,7,6,5,4,3,2]
    def d(b,w):
        r=sum(int(x)*y for x,y in zip(b,w))%11; return '0' if r<2 else str(11-r)
    return c[12]==d(c[:12],w1) and c[13]==d(c[:13],[6]+w1)
def valid(key,r):
    if r is None or r.status_code>=400: return None
    t=r.text[:800000]; tl=t.lower()
    m=re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I); title=html.unescape(m.group(1).strip()) if m else ''
    host=norm(re.sub(r'^https?://','',r.url).split('/')[0])
    if BAD.search(title) or re.search(r'this domain|este dom[ií]nio|buy this domain',tl[:20000]): return None
    br=bool(re.search(r'R\$|lang=["\']pt|pt-br|frete|cnpj|carrinho|sacola|comprar',tl))
    kw=sum(1 for k in KW if k in tl)
    if key in norm(title+' '+host) and kw>=2 and br: return title or host
    return None
def contacts(t):
    t=t.replace('\\/','/')
    cn=[c for c in (re.sub(r'\D','',x) for x in CNPJF.findall(t)) if cnpj_ok(c)]
    em=[e.lower() for e in re.findall(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+',t) if not re.search(r'\.(png|jpg|jpeg|webp|gif|svg|js|css)$|sentry|example|wixpress|shopify|@2x|@3x|nuvemshop|tiendanube|domain\.com|email\.com|seuemail|u00|lojaintegrada|vtex|yampi|cloudflare|godaddy|wordpress|woocommerce|jquery|bootstrap',e,re.I)]
    ig=[x for x in re.findall(r'instagram\.com/([A-Za-z0-9_.]+)',t) if x.lower().strip('.') not in ('p','reel','reels','explore','accounts','stories','tv','direct','_u','sharer','share','wix','shopify','google','sephora','instagram','facebook')]
    wa=re.findall(r'(?:wa\.me/\+?|api\.whatsapp\.com/send/?\?phone=\+?|whatsapp\.com/send\?phone=\+?)(\d{10,13})',t)
    tel=[re.sub(r'\D','',x) for x in re.findall(r'tel:\+?([\d\s\-\(\)]{10,20})',t)]
    u=lambda x: list(dict.fromkeys(x))
    return u(cn)[:4],u(em)[:6],u(ig)[:3],u(wa)[:3],u(tel)[:3]
GEN={'Cosméticos':['cosmeticos','beauty','oficial','store','cosmetics','skin','hair'],'Suplementos':['suplementos','nutrition','oficial','store','vitaminas'],'Casa e aroma':['aromas','home','velas','oficial','store']}
def work(r):
    key=norm(r.marca)
    if len(key)<4: return r.processo,None
    gens=sum((GEN.get(m.strip(),[]) for m in r.mercado.split('+')),[])
    slugs=list(dict.fromkeys([key]+[key+g for g in gens]+['use'+key,'loja'+key]))
    urls=[p+s+t+'/' for s in slugs for t in ['.com.br','.com'] for p in ['https://','https://www.']]
    with cf.ThreadPoolExecutor(16) as ix: got=list(ix.map(fetch,urls))
    for u,r2 in zip(urls,got):
        ti=valid(key,r2)
        if ti:
            base=re.match(r'https?://[^/]+',r2.url).group(0); allt=r2.text
            for p in ['/pages/contato','/contato','/fale-conosco','/quem-somos','/policies/terms-of-service','/politica-de-privacidade']:
                if CNPJF.search(allt) and '@' in allt: break
                rr=fetch(base+p)
                if rr is not None and rr.status_code==200 and len(rr.text)<3000000: allt+=rr.text
            cn,em,ig,wa,tel=contacts(allt)
            return r.processo,dict(url=r2.url,title=str(ti)[:100],cnpjs=cn,emails=em,ig=ig,wa=wa,tel=tel)
    return r.processo,None
todo=D[D.cnpj==''].drop_duplicates('marca')
out=open(f'disc_inpi_{rpi}.jsonl','a'); done=set()
if os.path.exists(f'disc_inpi_{rpi}.jsonl'):
    for l in open(f'disc_inpi_{rpi}.jsonl'): done.add(json.loads(l)['p'])
todo=todo[~todo.processo.isin(done)]
print('to search',len(todo),flush=True)
with cf.ThreadPoolExecutor(6) as ex:
    for p,i in ex.map(work,list(todo.itertuples())):
        out.write(json.dumps({'p':p,'i':i},ensure_ascii=False)+'\n'); out.flush()
print('found',sum(1 for l in open(f'disc_inpi_{rpi}.jsonl') if '"i": {' in l))
