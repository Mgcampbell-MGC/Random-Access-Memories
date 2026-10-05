import xml.etree.ElementTree as ET, re, unicodedata, pandas as pd, sys, json
f=sys.argv[1]; rpi=sys.argv[2]
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^A-Z0-9 ]',' ',unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper())).strip()
SUPP=re.compile(r'suplement',re.I); HOME=re.compile(r'vela|difusor|aromatiz|home spray',re.I)
rows=[]
for ev,el in ET.iterparse(f,events=('end',)):
    if el.tag!='processo': continue
    ds=[d.attrib.get('codigo') for d in el.iter('despacho')]
    if 'IPAS009' in ds:
        tit=[t.attrib for t in el.iter('titular')]
        m=el.find('marca'); nome=(m.findtext('nome') if m is not None else None) or ''
        cls={c.attrib.get('codigo'):(c.findtext('especificacao') or '') for c in el.iter('classe-nice')}
        mk=[]
        if '03' in cls: mk.append('Cosméticos')
        if '05' in cls and SUPP.search(cls['05']): mk.append('Suplementos')
        if '04' in cls and HOME.search(cls['04']): mk.append('Casa e aroma')
        if mk and nome.strip() and tit and tit[0].get('pais')=='BR':
            rows.append(dict(rpi=rpi,processo=el.attrib.get('numero'),deposito=el.attrib.get('data-deposito'),marca=nome.strip(),
              titular=tit[0].get('nome-razao-social','').strip(),uf=tit[0].get('uf',''),n_titulares=len(tit),
              apresentacao=m.attrib.get('apresentacao','') if m is not None else '',mercado=' + '.join(mk)))
    el.clear()
D=pd.DataFrame(rows); D.to_pickle(f'inpi_{rpi}.pkl')
print(len(D),'filings'); print(D.mercado.value_counts().to_string()); print('distinct applicants',D.titular.nunique())
print('MEI-style names (8-digit root)',D.titular.str.match(r'^\d{2}\.?\d{3}\.?\d{3}\s').sum())
