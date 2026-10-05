import pandas as pd, re, collections
w=pd.read_pickle('win_inc.pkl')
print('included rows',len(w),' with brand',w.bkey.notna().sum())
wb=w.dropna(subset=['bkey'])
new=wb[~wb.refile]
def agg(s):
    ns=s[~s.refile]
    cc=collections.Counter(ns.cat)
    return pd.Series({
      'n_rows':len(s),'n_new':ns.ts.map(lambda x: tuple(sorted(x))).nunique(),'n_refile':int(s.refile.sum()),
      'cats':','.join(f'{k}:{v}' for k,v in cc.most_common()),
      'main_cat':cc.most_common(1)[0][0] if cc else '',
      'n_days':ns.notif.dt.date.nunique(),'first':ns.notif.min(),'last':ns.notif.max(),
      'holders':'|'.join(sorted(s.NU_CNPJ_EMPRESA.unique())),
      'holder_names':'|'.join(sorted(s.NO_RAZAO_SOCIAL_EMPRESA.unique()))[:300],
      'holder_nbrands':int(s.holder_nbrands.max()),
      'brand_pre_n':int(s.brand_pre_n.max()),'brand_first_pre':s.brand_first_pre.min(),
      'examples':' || '.join(ns.sort_values('notif',ascending=False).NO_PRODUTO.head(8)),
      'processes':' '.join(ns.sort_values('notif',ascending=False).NU_PROCESSO.head(8)),
      'fullphrase':s.brand.mode().iloc[0]})
B=wb.groupby('bkey').apply(agg)
B=B[B.n_new>=1].copy()
print('brands with >=1 new SKU',len(B))
for k in [1,2,3,5,10]: print(' n_new>=',k,(B.n_new>=k).sum())
print(B.main_cat.value_counts().to_string())
B.to_pickle('brands_all.pkl')
