from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
F='research/raw_wild/fonts/'
cache={}
def font(name, loc=None):
    key=(name, tuple(sorted(loc.items())) if loc else None)
    if key not in cache:
        f=TTFont(F+name)
        if loc: f=instancer.instantiateVariableFont(f, loc)
        cache[key]=f
    return cache[key]
def w_per_capmm(f, s):
    cm=f.getBestCmap(); hm=f['hmtx']
    return sum(hm[cm[ord(c)]][0] for c in s)/710.0  # mm width per 1 mm cap
MEASURE=72.0
print('-- line 2 at cap 10.0 mm: find wdth to fit 72 mm')
for s in ['AO VIVO','CAMARIM','MAIS UM!','ACÚSTICO']:
    best=None
    for w in range(125,74,-1):
        width=w_per_capmm(font('SpecialGothic.ttf',{'wdth':w,'wght':700}),s)*10.0
        if width<=MEASURE: best=(w,width);break
    print(s, best)
print('-- headliner ladder at cap 17.9 mm (measure 72)')
names=['MÃE','VÓ','MAINHA','MAMIS','MAMÃE','DONA CIDA','VÓ ZEZÉ','TIA BETE','MADRINHA','DONA MARIA','MÃEZINHA','PAI','MAINHA ♥'.replace(' ♥','')]
for s in names:
    xp=w_per_capmm(font('SpecialGothicExpandedOne.ttf'),s)*17.9
    if xp<=MEASURE: print(f'{s:11s} step1 ExpandedOne cap17.9 width {xp:.1f} (needs track to fill)'); continue
    done=False
    for w in range(125,74,-1):
        width=w_per_capmm(font('SpecialGothic.ttf',{'wdth':w,'wght':700}),s)*17.9
        if width<=MEASURE: print(f'{s:11s} step2 SG wdth{w} cap17.9 width {width:.1f}'); done=True;break
    if done: continue
    cn=w_per_capmm(font('SpecialGothicCondensedOne.ttf'),s)
    if cn*17.9<=MEASURE: print(f'{s:11s} step3 Condensed cap17.9 width {cn*17.9:.1f}'); continue
    cap=MEASURE/cn
    print(f'{s:11s} step4 Condensed cap {cap:.1f} mm' + (' (>=12 ok)' if cap>=12 else ' -> step5 two lines'))
print('-- Expanded One width per cap mm for MÃE', w_per_capmm(font('SpecialGothicExpandedOne.ttf'),'MÃE'))
print('HOLOFOTE APRESENTA condensed width per cap', w_per_capmm(font('SpecialGothicCondensedOne.ttf'),'HOLOFOTE APRESENTA'))
