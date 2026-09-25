# All inputs from primary sources fetched 25 Sep 2026 (see OL5.md)
SM=1621.00          # Decreto 12.797/2025
def eff(anexo,rbt12):
    tabs={'III':[(180000,0.06,0),(360000,0.112,9360),(720000,0.135,17640)],
          'V':[(180000,0.155,0),(360000,0.18,4500),(720000,0.195,9900)]}
    for lim,a,d in tabs[anexo]:
        if rbt12<=lim: return (rbt12*a-d)/rbt12
def irpf(gross,inss):
    base=gross-max(inss,607.20)  # simplified discount 607,20 (25% of 2.428,80) vs legal deductions; take the larger deduction
    base=gross-inss if inss>607.20 else gross-607.20
    tab=[(2428.80,0,0),(2826.65,0.075,182.16),(3751.05,0.15,394.16),(4664.68,0.225,675.49),(1e12,0.275,908.73)]
    for lim,a,d in tab:
        if base<=lim: t=base*a-d; break
    t=max(t,0)
    # Lei 15.270 reduction (rendimentos tributáveis = gross)
    if gross<=5000: red=min(312.89,t)
    elif gross<=7350: red=978.62-0.133145*gross
    else: red=0
    return max(t-min(red,t),0)
def route(rev,name):
    rbt=rev*12
    out={}
    for r,(anexo,pl) in {'A_fator_r_28pct':('III',0.28*rev),'B_audiovisual_minPL':('III',SM),'C_anexoV_minPL':('V',SM)}.items():
        das=eff(anexo,rbt)*rev
        inss=0.11*min(pl,8475.55)
        ir=irpf(pl,inss)
        tot=das+inss+ir
        out[r]=dict(anexo=anexo,eff=round(eff(anexo,rbt)*100,3),pro_labore=round(pl,2),DAS=round(das,2),INSS_11=round(inss,2),IRPF=round(ir,2),total=round(tot,2),pct=round(tot/rev*100,2))
    return out
import json
res={}
for rev in [12200,15000,15800,25000]:
    res[rev]=route(rev,'')
print(json.dumps(res,indent=1,ensure_ascii=False))
# where does fator-r pro-labore start paying IRPF? pro-labore>5000 => rev > 5000/0.28
print('IRPF starts above revenue/month', round(5000/0.28,2))
# MEI DAS
print('MEI DAS', round(0.05*SM+5,2))
# blended no-fator-r 40% film / 60% stills at 15k
rev=15000; rbt=rev*12
print('blend 40/60 no fator r', round((0.4*eff('III',rbt)+0.6*eff('V',rbt))*rev + 0.11*SM,2), round(((0.4*eff('III',rbt)+0.6*eff('V',rbt))*rev + 0.11*SM)/rev*100,2))
