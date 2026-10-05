import json, re, requests, unicodedata, html, os, concurrent.futures as cf, pandas as pd
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36','Accept-Language':'pt-BR,pt;q=0.9'}
CA='/root/.ccr/ca-bundle.crt'
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
def asc(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
KWS=['cabelo','pele','shampoo','skincare','hidratante','cosmetic','beleza','capilar','corporal','serum','cachos','condicionador','mascara','creme','maquiagem','batom','perfume','fragranc','parfum','colonia','sabonete','splash','beauty','body splash','perfumaria','esmalte','skin care','cuidados']
GENP=set('shampoo condicionador mascara creme hidratante serum oleo locao gel sabonete perfume colonia body splash desodorante batom base po para com de da do das dos e em ml g kg cabelos cabelo capilar corporal facial pele cachos kit leave in spray tonico agua bruma esfoliante balm fluido protetor finalizador ampola nutricao hidratacao reconstrucao maos pes rosto labial eau parfum toilette deo intense new the and of for hair skin care beauty natural vegano vegana'.split())
K=pd.read_pickle('brands_keep.pkl')
site={}
for f_ in ['disc.jsonl','disc_b.jsonl','disc_c.jsonl','disc_d0.jsonl','disc_d1.jsonl','disc_d2.jsonl','disc_e.jsonl','disc2.jsonl']:
    if os.path.exists(f_):
        for l in open(f_):
            d=json.loads(l)
            if d['i'] or d['b'] not in site: site[d['b']]=d['i']
prev=json.load(open('reval_all.json')) if os.path.exists('reval_all.json') else {}
todo=[(b,i['url']) for b,i in site.items() if i and b not in prev and b in K.index]
def ptoks(b):
    toks=set()
    for name in K.loc[b,'examples'].split(' || '):
        for t in re.findall(r'[a-z0-9]+',asc(name)):
            if len(t)>=5 and t not in GENP and t not in norm(b): toks.add(t)
    return toks
def chk(x):
    b,u=x
    try: r=requests.get(u,headers=UA,timeout=15,verify=CA)
    except Exception: return b,{'ok':None}
    t=r.text[:1500000]; tl=asc(t)
    m=re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I); title=html.unescape(m.group(1).strip()) if m else ''
    host=norm(re.sub(r'^https?://','',r.url).split('/')[0])
    kw=sum(1 for k in KWS if k in tl)
    br=bool(re.search(r'r\$|lang=["\']pt|pt-br|frete|cnpj|\.com\.br|parcel|carrinho|sacola',tl))
    keyhost=norm(b) in host
    pt=ptoks(b); hits=sorted(x for x in pt if x in tl)
    holders=[h.zfill(14) for h in K.loc[b,'holders'].split('|')]
    cn=set(re.sub(r'\D','',x) for x in re.findall(r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}',t))
    cnmatch=bool(cn & set(holders))
    strong = cnmatch or len(hits)>=2
    ok = strong or (keyhost and kw>=3 and br)
    return b,{'ok':ok,'conf':'confirmado' if strong else ('provável' if ok else 'rejeitado'),'kw':kw,'br':br,'keyhost':keyhost,'hits':hits[:5],'cnmatch':cnmatch,'title':title[:80]}
with cf.ThreadPoolExecutor(24) as ex:
    for b,v in ex.map(chk,todo): prev[b]=v
json.dump(prev,open('reval_all.json','w'),ensure_ascii=False)
vals=[v for v in prev.values()]
print('checked',len(prev),'confirmado',sum(v.get('conf')=='confirmado' for v in vals),'provável',sum(v.get('conf')=='provável' for v in vals),'rejeitado',sum(v.get('conf')=='rejeitado' for v in vals),'unreachable',sum(v.get('ok') is None for v in vals))
