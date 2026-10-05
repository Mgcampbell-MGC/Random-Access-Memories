import pandas as pd, re, unicodedata, sys, glob
def bkey(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
A=pd.read_pickle('final.pkl').drop(columns='n')
A['mercado']='Beleza'; A['fonte']='ANVISA: produto notificado'; A['data_inpi']=pd.NaT
A['_bk']=A.marca.map(bkey); A['_cnpj']=A.cnpj.str.replace(r'\D','',regex=True)
N=pd.concat([pd.read_pickle(f) for f in sorted(glob.glob('inpi_rows_*.pkl'))],ignore_index=True)
N=N.sort_values('data_inpi').drop_duplicates(['_bk','empresa'],keep='last')
same=N._bk.isin(set(A._bk))
for _,r in N[same].iterrows():
    ix=A.index[A._bk==r._bk]
    for i in ix:
        A.at[i,'data_inpi']=r.data_inpi
        A.at[i,'alertas']=(A.at[i,'alertas']+'; ' if A.at[i,'alertas'] else '')+f"marca registrada no INPI em {r.data_inpi:%d/%m/%Y}"
N=N[~same].copy()
cn2a=A[A._cnpj!=''].groupby('_cnpj').marca.apply(lambda s: ', '.join(s[:3])).to_dict()
for i,r in N.iterrows():
    if r._cnpj and r._cnpj in cn2a:
        N.at[i,'alertas']+=f"; a empresa já está na lista com: {cn2a[r._cnpj]}"
        for j in A.index[A._cnpj==r._cnpj]:
            A.at[j,'alertas']=(A.at[j,'alertas']+'; ' if A.at[j,'alertas'] else '')+f"a mesma empresa pediu marca nova no INPI: {r.marca} ({r.data_inpi:%d/%m/%Y})"
            A.at[j,'score']+=2
D=pd.concat([A,N],ignore_index=True)
D['_m']=D.mercado.map({'Beleza':0,'Suplementos':1,'Casa e aroma':2}); D['_g']=D.grade.map({'A':0,'B':1,'C':2})
D=D.sort_values(['_m','_g','score'],ascending=[True,True,False]).drop(columns=['_m','_g','_bk','_cnpj']).reset_index(drop=True)
D.insert(0,'n',range(1,len(D)+1))
D.to_pickle('final_all.pkl')
print(len(D),'rows'); print(D.groupby(['mercado','grade']).size().unstack(fill_value=0).to_string())
print('INPI rows merged into existing ANVISA brands:',int(same.sum()),' ANVISA rows flagged same company new mark:',int(A.alertas.str.contains('pediu marca nova').sum()))
