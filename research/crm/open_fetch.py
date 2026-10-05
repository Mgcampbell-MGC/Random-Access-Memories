import requests, json, os, time, concurrent.futures as cf, sys
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
q=[l.strip() for l in open('queue.txt') if l.strip()]
todo=[c for c in q if not os.path.exists(f'reg/open/{c}.json')]
def get(c):
    for a in range(3):
        try:
            r=requests.get(f'https://api.opencnpj.org/{c}',headers=UA,timeout=30)
            if r.status_code==200: json.dump(r.json(),open(f'reg/open/{c}.json','w'),ensure_ascii=False); return 200
            if r.status_code==404: json.dump({'_status':404},open(f'reg/open/{c}.json','w')); return 404
            if r.status_code==429: time.sleep(10); continue
            return r.status_code
        except Exception: time.sleep(3)
    return 'ERR'
codes={}
with cf.ThreadPoolExecutor(4) as ex:
    for c,code in zip(todo,ex.map(get,todo)):
        codes[code]=codes.get(code,0)+1
print('done',len(todo),codes)
