from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
F='research/raw_wild/fonts/'
def font(n,loc=None):
    f=TTFont(F+n)
    return instancer.instantiateVariableFont(f,loc) if loc else f
def wpc(f,s):
    cm=f.getBestCmap(); hm=f['hmtx']
    miss=[c for c in s if ord(c) not in cm]
    if miss: return None, miss
    return sum(hm[cm[ord(c)]][0] for c in s)/710.0, []
CN=font('SpecialGothicCondensedOne.ttf')
SG125=font('SpecialGothic.ttf',{'wdth':125,'wght':700})
SG100r=font('SpecialGothic.ttf',{'wdth':100,'wght':400})
for s in ['ELA ESTEVE EM TODAS.']:
    for f,n in [(SG125,'SG125b'),(CN,'CN')]:
        w,_=wpc(f,s); print(n,s,'cap to fill 72 =',round(72/w,2),'mm')
rows=[('ESTREIA · 03.08.2003 · 14:32','QUEM FEZ O SHOW FOI ELA'),('ESTREIA · O DIA EM QUE VOCÊ NASCEU','QUEM FEZ O SHOW FOI ELA'),('PRÉZINHO, DIA DAS MÃES','PRIMEIRA FILA'),('FESTA JUNINA','O BIGODE FOI ELA'),('FEIRA DE CIÊNCIAS','O VULCÃO TAMBÉM'),('PRONTO-SOCORRO, 3H','SEM INGRESSO. ENTROU.'),('FORMATURA','DE PÉ (COM O DEDO NA LENTE)'),('PRIMEIRO APÊ','4 VIAGENS DE CARRO'),('09.05.2027','A ATRAÇÃO É ELA'),('TURNÊ «VOCÊ» · DESDE O PRIMEIRO DIA','')]
cap=2.0
for a,b in rows:
    wa,_=wpc(CN,a); wb,_=wpc(CN,b) if b else (0,[])
    print(f'{a+"  "+b:70s} text {cap*(wa+wb):5.1f} mm  leaders {72-cap*(wa+wb):5.1f} mm')
warn=['ATENÇÃO','• Nunca deixe a vela acesa sem supervisão.','• Mantenha fora do alcance de crianças e animais.','• Acenda longe de cortinas, tecidos, papéis e correntes de ar,','  sobre superfície firme e resistente ao calor.','• O copo esquenta: não toque nem mova a vela acesa.','Advertências completas e modo de uso: ver embalagem externa.','ODORIZANTE DE AMBIENTE · Perfuma o ambiente com aroma agradável.','Advertências completas e modo de uso: ver o SETLIST e a embalagem.']
for s in warn:
    for capw in (1.9,2.0):
        w,m=wpc(CN,s); 
        print(f'CN cap {capw}: {s[:60]:62s} {capw*w:5.1f} mm' if w else ('MISSING',m))
for s in warn[1:6]:
    w,_=wpc(SG100r,s); print('SG100 regular cap 1.9', s[:40], round(1.9*w,1))
