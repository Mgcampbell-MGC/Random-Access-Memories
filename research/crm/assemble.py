import pandas as pd, json, re, os, collections, unicodedata, urllib.parse
K=pd.read_pickle('brands_keep.pkl')
import sys; sys.path.insert(0,'../hunt6/work/ol6'); from excl import EXCL
EXN={re.sub(r'[^A-Z0-9]','',k) for k in EXCL}
K=K[~K.index.map(lambda b: re.sub(r'[^A-Z0-9]','',b) in EXN)]
BIG2=r'INDITEX|ZARA HOME|H&M|RENNER|RIACHUELO|C&A MODAS|O BOTICARIO|GRUPO BOTICARIO|NATURA'
K=K[~K.holder_names.str.upper().str.contains(BIG2,regex=True)]
_wb=pd.read_pickle('win_b.pkl')
HNAME={str(c).zfill(14):n for c,n in zip(_wb.NU_CNPJ_EMPRESA,_wb.NO_RAZAO_SOCIAL_EMPRESA)}
HNB={str(c).zfill(14):n for c,n in _wb.dropna(subset=['bkey']).groupby('NU_CNPJ_EMPRESA').bkey.nunique().items()}
GENT=set('COSMETICOS COSMETICS BEAUTY PROFESSIONAL PROFISSIONAL SKIN HAIR CARE BRASIL OFICIAL MAKE PERFUMES PARFUM LTDA INDUSTRIA COMERCIO'.split())
def namematch(brand,name):
    bt=[t for t in re.sub(r'[^A-Z0-9 ]',' ',brand.upper()).split() if len(t)>=4 and t not in GENT]
    nn=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().upper()
    return bool(bt) and all(t in nn for t in bt)
DDD={'SP':[11,12,13,14,15,16,17,18,19],'RJ':[21,22,24],'ES':[27,28],'MG':[31,32,33,34,35,37,38],'PR':[41,42,43,44,45,46],'SC':[47,48,49],'RS':[51,53,54,55],'DF':[61],'GO':[62,64],'TO':[63],'MT':[65,66],'MS':[67],'AC':[68],'RO':[69],'BA':[71,73,74,75,77],'SE':[79],'PE':[81,87],'AL':[82],'PB':[83],'RN':[84],'CE':[85,88],'PI':[86,89],'PA':[91,93,94],'AM':[92,97],'RR':[95],'AP':[96],'MA':[98,99]}
ACC=re.compile(r'contab|contador|contadores|contadora|escritorio|assessoria|consultoria|consultec|auditoria|fiscal|cont\.|ctb|tribut|legaliza|despachante|societario|admempresas|empresas\d*@|\.cnt\.br|\.adv\.br|advocacia|advogad|juridico',re.I)
SVC=re.compile(r'TERC\w{0,3}RIZ|INDUSTRIALIZ|NACIONALIZ|SOLUCOES INTEGRADAS|ASSESSORIA|CONSULTORIA|REGULAT|ADVERTISING|SERVICOS DE IMPORTACAO|PRIVATE LABEL|REPRESENTAC',re.I)
FREE=re.compile(r'@(gmail|hotmail|outlook|yahoo|live|icloud|uol|bol|terra|ig)\.',re.I)

JUNK=re.compile(r'typedesign|typefoundry|foundry|fonts?@|@fonts|sentry|wixpress|example|exemplo|seuemail|seu-email|seunome|yourname|youremail|nome@|usuario@|user@|teste@|test@|email@email|meuemail|@domain|@dominio|@site\.|@email\.com|@mail\.com$|noreply|no-reply|webmaster@|postmaster@|privacy@shopify|@sentry',re.I)
def valid_email(e):
    e=e.strip().lower().strip('.')
    m=re.match(r'^[a-z0-9._%+-]+@([a-z0-9-]+\.)+([a-z]{2,6})$',e)
    if not m: return False
    if JUNK.search(e): return False
    if re.search(r'\d+\.\d+',e.split('@')[1]): return False
    return True
def placeholder(p):
    d=re.sub(r'\D','',p)
    if len(d)<10: return True
    n=d[2:]
    if len(set(n))<=2: return True
    if re.search(r'12345|23456|34567|45678|98765|87654|00000|11111|99999',n): return True
    return False

def J(p):
    try: return json.load(open(p))
    except: return None
# ---- site discovery
site={}
for f_ in ['disc.jsonl','disc_b.jsonl','disc_c.jsonl','disc_d0.jsonl','disc_d1.jsonl','disc_d2.jsonl','disc_e.jsonl','disc2.jsonl']:
    if not os.path.exists(f_): continue
    for l in open(f_):
        d=json.loads(l)
        if d['i'] or d['b'] not in site: site[d['b']]=d['i']
RV=json.load(open('reval_all.json')) if os.path.exists('reval_all.json') else {}
SE={}
if os.path.exists('disc_email.jsonl'):
    for l in open('disc_email.jsonl'):
        d=json.loads(l)
        if d['i']: SE[d['b']]=d['i']
# CNPJs seen on many brand sites are platforms/agencies
cn_sites=collections.Counter()
for b,i in site.items():
    if i:
        for c in set(i.get('cnpjs',[])): cn_sites[c]+=1
PLAT_CN={c for c,n in cn_sites.items() if n>=3}
# ---- registry
def reg(c):
    c=c.zfill(14)
    r={'cnpj':c}
    b=J(f'reg/brasil/{c}.json')
    if b and '_status' not in b:
        r.update(razao=b.get('razao_social') or '',fantasia=b.get('nome_fantasia') or '',porte=b.get('porte') or '',capital=b.get('capital_social'),
                 abertura=b.get('data_inicio_atividade') or '',cnae=f"{b.get('cnae_fiscal','')} {b.get('cnae_fiscal_descricao','')}",
                 cidade=(b.get('municipio') or '').title(),uf=b.get('uf') or '',situacao=b.get('descricao_situacao_cadastral') or '',
                 mei=b.get('opcao_pelo_mei'),
                 socios=[(s.get('nome_socio',''),s.get('qualificacao_socio','')) for s in (b.get('qsa') or [])],
                 phones=[re.sub(r'\D','',x) for x in [b.get('ddd_telefone_1') or '',b.get('ddd_telefone_2') or ''] if re.sub(r'\D','',x)])
    else: r.update(razao='',fantasia='',porte='',capital=None,abertura='',cnae='',cidade='',uf='',situacao='',mei=None,socios=[],phones=[])
    em=[]
    x=J(f'reg/open/{c}.json')
    if x and '_status' not in x:
        if x.get('email'): em.append((x['email'].lower(),''))
        for t in x.get('telefones') or []:
            if not t.get('is_fax'): r['phones'].append(f"{t.get('ddd','')}{t.get('numero','')}")
        if not r['razao']:
            cap=x.get('capital_social')
            try: cap=float(str(cap).replace('.','').replace(',','.'))
            except: cap=None
            pc=[cc for cc in x.get('cnaes') or [] if cc.get('is_principal')]
            r.update(razao=x.get('razao_social',''),fantasia=x.get('nome_fantasia',''),porte=x.get('porte_empresa',''),capital=cap,abertura=x.get('data_inicio_atividade',''),
                     cnae=f"{x.get('cnae_principal','')} {pc[0]['descricao'] if pc else ''}",cidade=(x.get('municipio') or '').title(),uf=x.get('uf',''),situacao=x.get('situacao_cadastral',''),
                     socios=[(q.get('nome_socio',''),q.get('qualificacao_socio','')) for q in x.get('QSA') or []])
    x=J(f'reg/cnpja/{c}.json')
    if x and '_status' not in x:
        for e in x.get('emails') or []: em.append((e.get('address','').lower(),e.get('ownership') or ''))
        for p in x.get('phones') or []: r['phones'].append(f"{p.get('area','')}{p.get('number','')}")
        if not r['razao']:
            co=x.get('company') or {}
            r.update(razao=co.get('name',''),porte=(co.get('size') or {}).get('text',''),capital=co.get('equity'),abertura=x.get('founded',''),
                     cidade=(x.get('address') or {}).get('city',''),uf=(x.get('address') or {}).get('state',''),situacao=(x.get('status') or {}).get('text',''),
                     cnae=f"{(x.get('mainActivity') or {}).get('id','')} {(x.get('mainActivity') or {}).get('text','')}",
                     socios=[((m.get('person') or {}).get('name',''),(m.get('role') or {}).get('text','')) for m in co.get('members') or []])
    x=J(f'reg/rws/{c}.json')
    if x and x.get('status')=='OK':
        if x.get('email'): em.append((x['email'].lower(),''))
        for t in re.split(r'/',x.get('telefone') or ''):
            t=re.sub(r'\D','',t)
            if t: r['phones'].append(t)
        if not r['razao']:
            r.update(razao=x.get('nome',''),porte=x.get('porte',''),abertura=x.get('abertura',''),cidade=(x.get('municipio') or '').title(),uf=x.get('uf',''),situacao=x.get('situacao',''),
                     socios=[(s.get('nome',''),re.sub(r'^\d+-','',s.get('qual',''))) for s in x.get('qsa') or []])
    x=J(f'reg/pub/{c}.json')
    if x and 'estabelecimento' in x:
        e=x['estabelecimento']
        if e.get('email'): em.append((e['email'].lower(),''))
        for dd,tt in [(e.get('ddd1'),e.get('telefone1')),(e.get('ddd2'),e.get('telefone2'))]:
            if dd and tt: r['phones'].append(f'{dd}{tt}')
        if not r['razao']:
            r.update(razao=x.get('razao_social',''),porte=(x.get('porte') or {}).get('descricao',''),capital=x.get('capital_social'),abertura=e.get('data_inicio_atividade',''),
                     cidade=((e.get('cidade') or {}).get('nome','') if isinstance(e.get('cidade'),dict) else ''),uf=((e.get('estado') or {}).get('sigla','') if isinstance(e.get('estado'),dict) else ''),
                     socios=[(s.get('nome',''),((s.get('qualificacao_socio') or {}).get('descricao','') or '').strip()) for s in x.get('socios') or []])
    seen=set(); emails=[]
    for a,o in em:
        if a and a not in seen: seen.add(a); emails.append((a,o))
    r['emails']=emails
    r['phones']=list(dict.fromkeys(p for p in r['phones'] if len(p)>=10))
    r['has_email_lookup']=any(os.path.exists(f'reg/{p}/{c}.json') for p in ('cnpja','rws','pub','open'))
    return r
allc=set()
for b,r0 in K.iterrows():
    allc.update(h.zfill(14) for h in r0.holders.split('|'))
    i=site.get(b)
    if i: allc.update(c for c in i.get('cnpjs',[]) if len(c)==14)
R={c:reg(c) for c in allc}
# shared-contact detection (same e-mail or phone on >=3 distinct companies => accountant/agency)
emc=collections.Counter(); phc=collections.Counter()
for c,r in R.items():
    for a,o in r['emails']: emc[a]+=1
    for p in r['phones']: phc[p]+=1
json.dump({'emc':{k:v for k,v in emc.items() if v>=3},'phc':{k:v for k,v in phc.items() if v>=3}},open('shared.json','w'))
def cnpj_ok(c):
    if len(c)!=14 or len(set(c))==1: return False
    def dv(b,w):
        r=sum(int(x)*y for x,y in zip(b,w))%11; return '0' if r<2 else str(11-r)
    w1=[5,4,3,2,9,8,7,6,5,4,3,2]
    return c[12]==dv(c[:12],w1) and c[13]==dv(c[:13],[6]+w1)
VALID_DDD={11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,41,42,43,44,45,46,47,48,49,51,53,54,55,61,62,63,64,65,66,67,68,69,71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99}
IGJUNK=set('wix shopify google sephora facebook instagram meta tiktok youtube nuvemshop tiendanube tray vtex lojaintegrada wordpress woocommerce yampi bagy magazord loja_integrada traycommerce shopifybrasil wixbrasil'.split())
def phone_kind(p):
    p=re.sub(r'\D','',p)
    if p.startswith('55') and len(p)>=12: p=p[2:]
    if p.startswith(('800','300')) and len(p)==10: p='0'+p          # 0800/0300 typed without its zero
    if p.startswith('0') and not p.startswith(('0800','0300')) and len(p) in (11,12): p=p[1:]   # trunk zero: 062 3230-4969
    if p.startswith(('0800','0300','4004','4003')): return p,'0800'
    if len(p)>=10 and int(p[:2]) not in VALID_DDD: return p,'?'
    if len(p)<10: return p,'?'
    ddd,num=p[:2],p[2:]
    if len(num)==9 and num[0]=='9': return p,'celular'
    if len(num)==8 and num[0] in '6789': return ddd+'9'+num,'celular (número antigo, 9 acrescentado)'
    if len(num)==8 and num[0] in '2345': return p,'fixo'
    return p,'?'
def fmt(p):
    p=re.sub(r'\D','',p)
    if p.startswith(('0800','0300','4004','4003')): return f'{p[:4]} {p[4:7]} {p[7:]}'
    if len(p)==11: return f'({p[:2]}) {p[2:7]}-{p[7:]}'
    if len(p)==10: return f'({p[:2]}) {p[2:6]}-{p[6:]}'
    return p
rows=[]
for b,r0 in K.iterrows():
    holders=[h.zfill(14) for h in r0.holders.split('|')]
    hnames=r0.holder_names.split('|')
    i=site.get(b) or None
    rv=RV.get(b) if i else None
    if i and (rv is None or not rv.get('ok')): i=None   # not re-validated, rejected or unreachable
    site_conf=rv.get('conf','') if i else ''
    if i and site_conf=='provável' and len(re.sub(r'[^a-z0-9]','',b.lower()))<=3: i=None; site_conf=''   # 2-3 letter names match too many unrelated hosts
    foreign = bool(i) and not rv.get('br',True)
    se_neg = b in SE and SE[b].get('brand_on_site') is False
    if not i and b in SE and SE[b].get('brand_on_site'):
        i=SE[b]; site_conf='site da empresa dona (domínio do e-mail no CNPJ; a marca aparece no site)'; foreign=False
    scn=[c for c in (i.get('cnpjs',[]) if i else []) if len(c)==14 and c not in PLAT_CN and not c.startswith('12345678') and len(set(c[:8]))>2 and cnpj_ok(c)]
    owner=None; how=''
    for c in scn:
        if c in holders: owner=c; how='CNPJ no rodapé do site = titular na ANVISA'; break
    if not owner and scn:
        owner=scn[0]; how='CNPJ no rodapé do site da marca'
    if not owner:
        for h in holders:
            if namematch(b,HNAME.get(h,'')): owner=h; how='nome da empresa titular na ANVISA contém a marca'; break
    weak=False
    if not owner:
        few=[h for h in holders if HNB.get(h,99)<=2]
        if few:
            owner=min(few,key=lambda h:HNB.get(h,99)); how=f'titular na ANVISA registra só {HNB.get(owner)} marca(s): provável dono'
    if not owner:
        for h in holders:
            cn=(R.get(h) or {}).get('cnae','')
            if cn and not cn.startswith(('20','21')) and HNB.get(h,99)<=15:
                owner=h; how='titular na ANVISA é empresa de comércio (não fábrica): provável dono'; break
    if not owner:
        few=[h for h in holders if HNB.get(h,99)<=5]
        if few:
            owner=min(few,key=lambda h:HNB.get(h,99)); weak=True
            how=f'titular é fábrica com {HNB.get(owner)} marcas: pode ser o dono ou fábrica terceirizada — confirme na ligação'
    if owner and how.startswith('titular na ANVISA é empresa de comércio') and HNB.get(owner,0)>5:
        weak=True; how=f'titular é empresa de comércio com {HNB.get(owner)} marcas: pode ser importadora ou agente — confirme na ligação'
    if owner and SVC.search(unicodedata.normalize('NFKD',HNAME.get(owner,'')+' '+str((R.get(owner) or {}).get('razao',''))).encode('ascii','ignore').decode()) and not how.startswith(('nome da empresa','CNPJ no rodapé')):
        owner=None; how='titular parece prestador de serviço (fábrica terceirizada, importação ou regulatório): o dono da marca não aparece no cadastro'
    if owner and se_neg and not how.startswith(('nome da empresa','CNPJ no rodapé')):
        owner=None; how='titular parece fábrica terceirizada (o site dessa empresa não mostra a marca)'
    O=(R.get(owner) or reg(owner)) if owner else None
    alerts=[]
    # contacts
    wa=[]; tel=[]; emails=[]
    if i:
        for w_ in i.get('wa',[]):
            w2=w_[2:] if w_.startswith('55') else w_
            if placeholder(w2) or w2.startswith('0'): continue
            p,k=phone_kind(w_)
            if k in ('?','0800'): continue
            wa.append((fmt(p),'WhatsApp no site da marca',p))
        for t in i.get('tel',[]):
            if placeholder(t[2:] if t.startswith('55') and len(t)>=12 else t): continue
            p,k=phone_kind(t)
            if k=='?': continue
            tel.append((fmt(p),k+' (site da marca)',p))
        dom=re.sub(r'^https?://(www\.)?','',i['url']).split('/')[0]
        for e in i.get('emails',[]):
            if ACC.search(e) or not valid_email(e): continue
            tag='site da marca'+(' (domínio próprio)' if dom.split('.')[0] in e else '')
            emails.append((e,tag))
    regmails=[]
    if O:
        uf=O.get('uf','')
        for p in O['phones']:
            if placeholder(p): continue
            q,k=phone_kind(p)
            if k=='?': continue
            flag=''
            if phc.get(p,0)>=3: flag=' — ATENÇÃO: mesmo número em %d empresas (provável contador)'%phc[p]
            elif uf in DDD and q[:2].isdigit() and int(q[:2]) not in DDD[uf]: flag=' — DDD de outro estado (pode ser do contador)'
            tel.append((fmt(q),k+' (cadastro CNPJ)'+flag,q))
        for a,o in O['emails']:
            if not valid_email(a): continue
            acc = o=='ACCOUNTING' or ACC.search(a) or emc.get(a,0)>=3
            shared = (not acc) and emc.get(a,0)==2
            regmails.append((a,'cadastro CNPJ'+(' — PROVÁVEL CONTADOR' if acc else '')+(' — mesmo e-mail em outra empresa' if shared else ''),bool(acc)))
    # best picks
    wa_best = wa[0] if wa else None
    mob=[t for t in tel if t[1].startswith('celular') and 'ATENÇÃO' not in t[1]]
    if not wa_best and mob: wa_best=(mob[0][0],'celular do cadastro (pode ter WhatsApp)',mob[0][2])
    tel_sorted=sorted(tel,key=lambda t:(('ATENÇÃO' in t[1]) or ('outro estado' in t[1]), 'site' not in t[1]))
    tel_best=next((t for t in tel_sorted if not wa_best or t[2]!=wa_best[2]),tel_sorted[0] if tel_sorted else None)
    em_all=emails+[(a,t) for a,t,acc in regmails if not acc]
    em_best=em_all[0] if em_all else None
    em_acc=[(a,t) for a,t,acc in regmails if acc]
    # flags
    untested=r0.main_cat in ('makeup','fragrance')
    if untested: alerts.append('formato não testado (maquiagem/perfume)')
    if r0.imp: alerts.append('titular é importadora')
    if r0.pro: alerts.append('linha profissional (salão)')
    if r0.oils: alerts.append('óleos essenciais/aromas')
    if em_acc and not em_best: alerts.append('só há e-mail do contador')
    if O and O.get('situacao') and O['situacao'].upper() not in ('ATIVA',): alerts.append('CNPJ '+O['situacao'])
    porte=(O or {}).get('porte','') if O else ''
    porte={'MICROEMPRESA (ME)':'MICRO EMPRESA','EMPRESA DE PEQUENO PORTE (EPP)':'EMPRESA DE PEQUENO PORTE'}.get((porte or '').upper(),(porte or '').upper())
    large = bool(re.search(r'DEMAIS',porte or '',re.I))
    if large: alerts.append('empresa de porte maior (DEMAIS)')
    if foreign: alerts.append('site estrangeiro: marca importada')
    if site_conf=='provável': alerts.append('site provável (nome bate, mas sem CNPJ ou produto confirmado na página)')
    holder_is_maker = not owner or owner not in holders
    makers=[f'{HNAME.get(h,"").title()} ({h[:2]}.{h[2:5]}.{h[5:8]}/{h[8:12]}-{h[12:]})' for h in holders if h!=owner]
    # score & grade
    sc=min(r0.n_new,12)+min(r0.n_new/ max(r0.n_days,1),4)
    if r0.newbrand: sc+=3
    if owner: sc+=2
    if wa and wa[0]: sc+=2
    if i: sc+=1
    if O and O.get('uf')=='SP': sc+=1
    last=r0['last']
    if pd.notna(last) and (pd.Timestamp('2026-09-30')-last).days<=30: sc+=2
    if untested: sc-=2
    if r0.pro: sc-=2
    if r0.imp: sc-=5
    if r0.oils: sc-=6
    if large: sc-=3
    contact = bool(wa_best or tel_best or em_best)
    if not owner or r0.imp or r0.oils or foreign: grade='C'
    elif r0.n_new>=3 and contact and not large and not weak: grade='A'
    elif contact: grade='B'
    else: grade='C'
    cats={'hair':'cabelo','face':'rosto/skincare','body':'corpo','soap':'sabonete/corpo','deo':'desodorante','makeup':'maquiagem','fragrance':'perfume/fragrância'}
    catlist=', '.join(f"{cats.get(k.split(':')[0],k)} {k.split(':')[1]}" for k in r0.cats.split(','))
    first,lastd=r0['first'],r0['last']
    reason=f"{r0.n_new} produto(s) novo(s) entre {first:%d/%m} e {lastd:%d/%m}/2026 ({catlist})"
    if r0.newbrand: reason+='; marca nova (primeiro registro em 2025 ou depois)'
    if how: reason+='; dono: '+how
    elif not owner: reason+='; dono não identificado — produto feito por terceiro'
    if wa: reason+='; WhatsApp no site'
    soc='; '.join(f'{n.title()} ({q})' for n,q in (O or {}).get('socios',[])[:4]) if O else ''
    brand_name=r0.fullphrase.title() if isinstance(r0.fullphrase,str) else b.title()
    q=urllib.parse.quote(f'"{b.title()}" cosméticos')
    rows.append(dict(
        grade=grade,score=round(sc,1),marca=b.title(),categoria=cats.get(r0.main_cat,r0.main_cat),formato='Não testado (maquiagem/perfume)' if untested else 'Testado',
        n_new=int(r0.n_new),primeiro=first,ultimo=lastd,exemplos=r0.examples.title()[:400],
        site=(i or {}).get('url',''),site_conf=site_conf,plataforma=(i or {}).get('platform',''),
        instagram=next(('https://instagram.com/'+h for h in (i.get('ig',[]) if i else []) if h.lower().strip('.') not in IGJUNK and len(h)>2),''),
        whatsapp=wa_best[0] if wa_best else '',whatsapp_link=('https://wa.me/55'+wa_best[2]) if wa_best else '',whatsapp_origem=wa_best[1] if wa_best else '',
        telefone=tel_best[0] if tel_best else '',telefone_tipo=tel_best[1] if tel_best else '',
        outros_tel='; '.join(f'{t[0]} [{t[1]}]' for t in tel_sorted[1:5]),
        email=em_best[0] if em_best else '',email_origem=em_best[1] if em_best else '',
        outros_email='; '.join(f'{a} [{t}]' for a,t in (em_all[1:4]+em_acc[:2])),
        pessoas=soc,empresa=(O or {}).get('razao','') if O else '',cnpj=(f'{owner[:2]}.{owner[2:5]}.{owner[5:8]}/{owner[8:12]}-{owner[12:]}' if owner else ''),
        como_dono=how or ('não identificado' if not owner else ''),porte=porte,capital=(O or {}).get('capital') if O else None,abertura=(O or {}).get('abertura','') if O else '',
        cidade=(O or {}).get('cidade','') if O else '',uf=(O or {}).get('uf','') if O else '',
        fabricante=('; '.join(makers))[:300],
        alertas='; '.join(alerts),motivo=reason,
        busca_google='https://www.google.com/search?q='+q,busca_instagram='https://www.google.com/search?q='+urllib.parse.quote(f'site:instagram.com "{b.title()}"'),
        processos=r0.processes))
D=pd.DataFrame(rows)
D['go']=D.grade.map({'A':0,'B':1,'C':2})
D=D.sort_values(['go','score'],ascending=[True,False]).drop(columns='go').reset_index(drop=True)
D.insert(0,'n',range(1,len(D)+1))
D.to_pickle('final.pkl')
print(D.grade.value_counts().to_string())
print('with owner',(D.cnpj!='').sum(),' site',(D.site!='').sum(),' whatsapp',(D.whatsapp!='').sum(),' phone',(D.telefone!='').sum(),' email',(D.email!='').sum())
