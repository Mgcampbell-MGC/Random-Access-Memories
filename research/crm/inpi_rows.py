# Turn INPI trademark filings (expand/inpi_<rpi>_m.pkl + disc_inpi_<rpi>.jsonl) into Lista rows.
import sys, json, re, unicodedata, urllib.parse, pandas as pd
RPI=sys.argv[1]; RPI_DATE=sys.argv[2]
src=open('assemble.py').read().split('rows=[]\nfor b,r0 in K.iterrows():')[0]
exec(src)
BIGRE=re.compile(open('pipe3.py').read().split('BIG=r"')[1].split('"')[0]+'|'+BIG2,re.I)
E='../expand/'
I=pd.read_pickle(f'{E}inpi_{RPI}_m.pkl')
disc={}
for l in open(f'{E}disc_inpi_{RPI}.jsonl'):
    d=json.loads(l); disc[d['p']]=d['i']
proc2marca=dict(zip(I.processo,I.marca))
site_by_marca={proc2marca[p]:i for p,i in disc.items() if i and p in proc2marca}
STOPK=r'\b(LTDA|LIMITADA|ME|EPP|EIRELI|S ?A|SA|SLU|UNIPESSOAL|MEI|COSMETICOS?|INDUSTRIA|COMERCIO|DE|DO|DA|E|PRODUTOS|BELEZA|DISTRIBUIDORA|IMPORTACAO|EXPORTACAO|SUPLEMENTOS?)\b'
def nkey(s):
    s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().upper()
    s=re.sub(r'^\d{2}\.?\d{3}\.?\d{3}\s','',s); s=re.sub(r'[^A-Z0-9 ]',' ',s); s=re.sub(STOPK,' ',s)
    return set(t for t in s.split() if len(t)>=3)
def bkey(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
I['bk']=I.marca.map(bkey)
I=I[~I.titular.str.contains(BIGRE)]
I=I.sort_values('cnpj',ascending=False).drop_duplicates(['bk','titular'])
rows=[]
for r in I.itertuples():
    mk='Beleza' if 'Cosméticos' in r.mercado else ('Suplementos' if 'Suplementos' in r.mercado else 'Casa e aroma')
    owner=r.cnpj or None; how=('pedido de marca no INPI + '+r.cnpj_origem) if owner else ''
    i=site_by_marca.get(r.marca)
    if i:
        for c in i.get('cnpjs',[])[:2]:
            if not cnpj_ok(c): continue
            rc=reg(c)
            if rc.get('razao') and nkey(rc['razao'])&nkey(r.titular):
                if not owner: owner=c; how='CNPJ no rodapé do site = titular do pedido no INPI'
                break
    O=reg(owner) if owner else None
    if O and not O.get('razao'): O=None
    alerts=['marca nova: pedido de registro no INPI, provavelmente ainda não lançou — ofereça a PRÉVIA']
    wa=[]; tel=[]; emails=[]
    if i:
        for w_ in i.get('wa',[]):
            p,k=phone_kind(w_)
            if k in ('?','0800') or placeholder(p[2:] if len(p)>10 else p): continue
            wa.append((fmt(p),'WhatsApp no site da marca',p))
        for t in i.get('tel',[]):
            p,k=phone_kind(t)
            if k=='?' or placeholder(p): continue
            tel.append((fmt(p),k+' (site da marca)',p))
        for e in i.get('emails',[]):
            if ACC.search(e) or not valid_email(e): continue
            emails.append((e,'site da marca'))
    regmails=[]
    if O:
        uf=O.get('uf','')
        for p in O['phones']:
            if placeholder(p): continue
            q,k=phone_kind(p)
            if k=='?': continue
            flag=' — ATENÇÃO: mesmo número em %d empresas (provável contador)'%phc[p] if phc.get(p,0)>=3 else (' — DDD de outro estado (pode ser do contador)' if uf in DDD and q[:2].isdigit() and int(q[:2]) not in DDD[uf] else '')
            tel.append((fmt(q),k+' (cadastro CNPJ)'+flag,q))
        for a,o in O['emails']:
            if not valid_email(a): continue
            acc=o=='ACCOUNTING' or ACC.search(a) or emc.get(a,0)>=3
            regmails.append((a,'cadastro CNPJ'+(' — PROVÁVEL CONTADOR' if acc else ''),bool(acc)))
    wa_best=wa[0] if wa else None
    mob=[t for t in tel if t[1].startswith('celular') and 'ATENÇÃO' not in t[1]]
    if not wa_best and mob: wa_best=(mob[0][0],'celular do cadastro (pode ter WhatsApp)',mob[0][2])
    tel_sorted=sorted(tel,key=lambda t:(('ATENÇÃO' in t[1]) or ('outro estado' in t[1]),'site' not in t[1]))
    tel_best=next((t for t in tel_sorted if not wa_best or t[2]!=wa_best[2]),tel_sorted[0] if tel_sorted else None)
    em_all=emails+[(a,t) for a,t,acc in regmails if not acc]; em_best=em_all[0] if em_all else None
    em_acc=[(a,t) for a,t,acc in regmails if acc]
    if em_acc and not em_best: alerts.append('só há e-mail do contador')
    porte=(O or {}).get('porte','') or ''
    porte={'MICROEMPRESA (ME)':'MICRO EMPRESA','EMPRESA DE PEQUENO PORTE (EPP)':'EMPRESA DE PEQUENO PORTE'}.get(porte.upper(),porte.upper())
    large='DEMAIS' in porte
    if large: alerts.append('empresa de porte maior (DEMAIS)')
    if O and O.get('situacao') and O['situacao'].upper()!='ATIVA': alerts.append('CNPJ '+O['situacao'])
    contact=bool(wa_best or tel_best or em_best)
    grade='B' if contact and not large else 'C'
    sc=6+(2 if wa else 0)+(1 if i else 0)+(1 if owner else 0)+(1 if (O or {}).get('uf')=='SP' else 0)-(3 if large else 0)
    reason=f"marca nova: pedido de registro no INPI em {r.deposito} (publicado na RPI {RPI}, {RPI_DATE}); classe: {r.mercado}"
    if how: reason+='; dono: '+how
    elif not contact: reason+='; contato não encontrado: use os links de busca'
    soc='; '.join(f'{n.title()} ({q})' for n,q in (O or {}).get('socios',[])[:4]) if O else ''
    word={'Beleza':'cosméticos','Suplementos':'suplementos','Casa e aroma':'velas aromas'}[mk]
    rows.append(dict(grade=grade,score=sc,marca=r.marca.strip().title() if r.marca.isupper() else r.marca.strip(),mercado=mk,fonte=f'INPI: pedido de marca (RPI {RPI})',
        categoria='',formato='',n_new=None,primeiro=None,ultimo=None,data_inpi=pd.to_datetime(r.deposito,format='%d/%m/%Y'),exemplos='',
        site=(i or {}).get('url',''),site_conf='confirmado' if (i and owner) else ('provável' if i else ''),plataforma='',
        instagram=next(('https://instagram.com/'+h for h in (i.get('ig',[]) if i else []) if h.lower().strip('.') not in IGJUNK and len(h)>2),''),
        whatsapp=wa_best[0] if wa_best else '',whatsapp_link=('https://wa.me/55'+wa_best[2]) if wa_best else '',whatsapp_origem=wa_best[1] if wa_best else '',
        telefone=tel_best[0] if tel_best else '',telefone_tipo=tel_best[1] if tel_best else '',outros_tel='; '.join(f'{t[0]} [{t[1]}]' for t in tel_sorted[1:5]),
        email=em_best[0] if em_best else '',email_origem=em_best[1] if em_best else '',outros_email='; '.join(f'{a} [{t}]' for a,t in (em_all[1:4]+em_acc[:2])),
        pessoas=soc,empresa=(O or {}).get('razao') or r.titular,cnpj=(f'{owner[:2]}.{owner[2:5]}.{owner[5:8]}/{owner[8:12]}-{owner[12:]}' if owner else ''),
        como_dono=how or 'titular do pedido de marca no INPI (CNPJ não encontrado)',porte=porte,capital=(O or {}).get('capital') if O else None,
        abertura=(O or {}).get('abertura','') if O else '',cidade=(O or {}).get('cidade','') if O else '',uf=(O or {}).get('uf') or r.uf,
        fabricante='',alertas='; '.join(alerts),motivo=reason,
        busca_google='https://www.google.com/search?q='+urllib.parse.quote(f'"{r.marca}" {word}'),
        busca_instagram='https://www.google.com/search?q='+urllib.parse.quote(f'site:instagram.com "{r.marca}"'),
        processos=f'INPI {r.processo}',_bk=r.bk,_cnpj=owner or ''))
N=pd.DataFrame(rows); N.to_pickle(f'inpi_rows_{RPI}.pkl')
print(len(N),'rows'); print(N.groupby(['mercado','grade']).size().to_string())
print('with CNPJ',(N._cnpj!='').sum(),' site',(N.site!='').sum(),' whatsapp',(N.whatsapp!='').sum(),' phone',(N.telefone!='').sum(),' email',(N.email!='').sum())
