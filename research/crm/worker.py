import requests, time, os, sys, json
prov=sys.argv[1]
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
CFG={'brasil':('https://brasilapi.com.br/api/cnpj/v1/{}',1.0),
     'minha':('https://minhareceita.org/{}',1.0),
     'cnpja':('https://open.cnpja.com/office/{}',12.5),
     'rws':('https://receitaws.com.br/v1/cnpj/{}',20.5),
     'pub':('https://publica.cnpj.ws/cnpj/{}',20.5)}
url,gap=CFG[prov]
outdir='reg/brasil' if prov in ('brasil','minha') else f'reg/{prov}'
EMAILP=['cnpja','rws','pub']
def done_email(c):
    return any(os.path.exists(f'reg/{p}/{c}.json') for p in EMAILP)
def claim(c,group):
    try:
        fd=os.open(f'reg/claims/{group}_{c}',os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.close(fd); return True
    except FileExistsError: return False
log=open(f'reg/{prov}.log','a')
while True:
    qf='queue.txt' if prov in ('brasil','minha') or not os.path.exists('equeue.txt') else 'equeue.txt'
    q=[l.strip() for l in open(qf) if l.strip()]
    nxt=None
    for c in q:
        if prov in ('brasil','minha'):
            if os.path.exists(f'{outdir}/{c}.json'): continue
            if not claim(c,'B'): continue
        else:
            if done_email(c): continue
            if not claim(c,'E'): continue
        nxt=c; break
    if nxt is None:
        if os.path.exists('queue.final'): break
        time.sleep(20); continue
    t0=time.time()
    try:
        r=requests.get(url.format(nxt),headers=UA,timeout=30); code=r.status_code
    except Exception as e:
        code='ERR'
    log.write(f'{time.strftime("%H:%M:%S")} {nxt} {code}\n'); log.flush()
    if code==200:
        json.dump(r.json(),open(f'{outdir}/{nxt}.json','w'),ensure_ascii=False)
    elif code in (404,400):
        json.dump({'_status':code},open(f'{outdir}/{nxt}.json','w'))
    else:
        os.remove(f'reg/claims/{"B" if prov in ("brasil","minha") else "E"}_{nxt}')
        time.sleep(65 if code==429 else 15)
    time.sleep(max(0,gap-(time.time()-t0)))
