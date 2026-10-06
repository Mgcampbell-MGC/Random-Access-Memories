import sys, json
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.boundsPen import BoundsPen
F='research/raw_wild/fonts/'
def load(name, loc=None):
    f=TTFont(F+name)
    if loc: f=instancer.instantiateVariableFont(f, loc)
    return f
def width_mm(f, s, cap_mm, track=0):
    # track in 1/1000 em
    cm=f.getBestCmap(); hm=f['hmtx']; upm=f['head'].unitsPerEm
    capH=f['OS/2'].sCapHeight or 710
    size_mm = cap_mm*upm/capH  # em size in mm
    w=0
    gs=f.getGlyphSet()
    for i,ch in enumerate(s):
        g=cm.get(ord(ch))
        if g is None: return None
        w+=hm[g][0]
        if i < len(s)-1: w+=track
    # simple kerning ignored
    return w/upm*size_mm, size_mm
fonts={
 'XP':load('SpecialGothicExpandedOne.ttf'),
 'CN':load('SpecialGothicCondensedOne.ttf'),
 'SG125b':load('SpecialGothic.ttf',{'wdth':125,'wght':700}),
 'SG75b':load('SpecialGothic.ttf',{'wdth':75,'wght':700}),
 'SG100b':load('SpecialGothic.ttf',{'wdth':100,'wght':700}),
 'SH':load('ShantellSans.ttf',{'wght':500,'INFM':50,'BNCE':0,'SPAC':0}),
}
tests=[('XP','MÃE',20),('XP','HOLOFOTE',10),('SG125b','AO VIVO',9),('SG125b','CAMARIM',9),('SG125b','MAIS UM!',9),('SG125b','ACÚSTICO',9),('CN','HOLOFOTE APRESENTA',2.4),('CN','DOMINGO · 09.05',4.5),('SH','abertura: você',2.0/0.498*0.7),('CN','PESO LÍQUIDO 200 g',4.0),('CN','vela aromática',2.4),('CN','ELA ESTEVE EM TODAS.',4.0),
('XP','MAINHA',20),('XP','DONA CIDA',20),('XP','MÃE',22),('CN','MÃE',20),('SG75b','DONA CIDA',20),('SG75b','MADRINHA',20),('CN','DONA CIDA',20)]
for k,s,c in tests:
    r=width_mm(fonts[k],s,c)
    print(f"{k:7s} {s!r:28s} cap {c:5.2f} mm -> width {r[0]:6.1f} mm (em {r[1]:.2f} mm)")
