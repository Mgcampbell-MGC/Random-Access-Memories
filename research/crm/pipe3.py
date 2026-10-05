import pandas as pd, re, sys
sys.path.insert(0,'../hunt6/work/ol6')
from excl import EXCL
B=pd.read_pickle('brands_all.pkl')
BIG=r"L.?OREAL|UNILEVER|PROCTER|NATURA COSM|NATURA IND|AVON |BOTIC|BEIERSDORF|JOHNSON|KENVUE|COTY|ELCA|REVLON|ARDEN|GALDERMA|PIERRE FABRE|NAOS|COSMED|HYPERA|CIMED|EMS S|EUROFARMA|ACHE |MANTECORP|HENKEL|KAO |SHISEIDO|HINODE|MARY KAY|EMBELLEZE|DEVINTEX|NIELY|COLGATE|RECKITT|BAYER|SANOFI|ABBOTT|GLAXO|HALEON|WELEDA|OCCITANE|RAIA|DROGASIL|DPSP|PAGUE MENOS|DIMED|ARAUJO|CARREFOUR|AMERICANAS|GRANADO|PHEBO|MEGALABS|LIBBS|FARMOQUIMICA|BIOLAB|LEGRAND|GERMED|PRATI|MEDLEY|TEUTO|LVMH|PUIG|CHANEL|SAVOY|BETTECH|LAPRONAT|JEQUITI|SILVIO SANTOS|INTERPARFUMS|AMOREPACIFIC|ESTEE|SEPHORA|MINISO|NIVEA|PIERRE ALEXANDER|ANA HICKMANN COSMETICOS|DAVENE|FARMAX|SALON LINE|BIOMEDIC|THERASKIN|DERMAGE|ADCOS|BEL COL|FLORA PRODUTOS|IFF |GIVAUDAN|FIRMENICH|SYMRISE"
H=B.holder_names.str.upper()
B['excl']=''
B.loc[H.str.contains(BIG,regex=True),'excl']='grupo grande/multinacional'
for k,v in EXCL.items():
    if k in B.index and (v or True): B.loc[k,'excl']= B.loc[k,'excl'] or ('lista manual: '+(v or 'excluída'))
ex=B.examples.str.upper()
B['oils']=ex.str.count('ESSENCIAL|OLEO VEGETAL|ESSENCIA DIFUSORA|REFIL')>=3
B['imp']=H.str.contains('IMPORT')
B['pro']=B.fullphrase.str.contains(r'PROFISSIONAL|PROFESSIONAL|PROFESSIONNEL|\bPRO\b',regex=True)
B['newbrand']=B.brand_first_pre.isna()|(B.brand_first_pre>=pd.Timestamp('2025-01-01'))
B['untested']=B.main_cat.isin(['makeup','fragrance'])
print('excluded:',(B.excl!='').sum()); print(B[B.excl!=''].excl.str.split(':').str[0].value_counts().to_string())
K=B[B.excl==''].copy()
print('kept',len(K),' new>=3',(K.n_new>=3).sum(),' importer holders',K.imp.sum(),' oils',K.oils.sum(),' untested-shape main cat',K.untested.sum())
holders=set()
for h in K.holders: holders.update(h.split('|'))
print('distinct holder CNPJs',len(holders))
K['hcount']=K.holders.str.count(r'\|')+1
K.to_pickle('brands_keep.pkl')
B[B.excl!=''].to_pickle('brands_excl.pkl')
