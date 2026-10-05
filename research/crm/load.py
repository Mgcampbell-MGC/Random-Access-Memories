import pandas as pd, unicodedata, re
df=pd.read_csv('TA_CONSULTA_COSMETICOS.CSV',sep=';',encoding='latin-1',dtype=str,quotechar='"')
print('rows',len(df)); print(df.columns.tolist())
v=pd.to_datetime(df.DT_VENCIMENTO,format='%d/%m/%Y %H:%M:%S',errors='coerce')
df['venc']=v; df['notif']=v-pd.DateOffset(years=10)
def strip(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
df['N']=df.NO_PRODUTO.map(strip)
df['midnight']=df.venc.dt.strftime('%H:%M:%S')=='00:00:00'
df['T']=df.N.map(lambda n: n.replace('-',' - ').split())
df.to_pickle('cos.pkl')
el=df[df.DS_TIPO_PETICAO.eq('Notificado')&(~df.midnight)&df.notif.notna()]
T_END=el.notif.max(); T0=(T_END.normalize()-pd.Timedelta(days=90))
print('newest notification',T_END,' window start',T0)
w=el[el.notif>=T0].copy()
yr=w.NU_PROCESSO.str.extract(r'^25351\d{6}(\d{4})')[0]
print('rows in 90d window',len(w),' process-year matches notif year',(yr==w.notif.dt.year.astype(str)).mean())
w.to_pickle('win90.pkl')
open('window.txt','w').write(f'{T0.date()} {T_END}\n')
