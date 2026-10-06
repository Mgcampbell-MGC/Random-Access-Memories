import sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.boundsPen import BoundsPen
def measure(f, label):
    gs = f.getGlyphSet(); cm = f.getBestCmap(); upm = f['head'].unitsPerEm
    def bb(c):
        g = cm.get(ord(c))
        if g is None: return None
        p = BoundsPen(gs); gs[g].draw(p); return p.bounds
    digs = [bb(d) for d in '0123456789']
    tops = [round(b[3]) for b in digs]; bots=[round(b[1]) for b in digs]
    H = bb('H'); x = bb('x'); g = bb('g'); X = bb('X'); O=bb('O')
    fig = min(tops) - max(0,max(bots))
    print(f"{label}: upm {upm} | digit tops {min(tops)}-{max(tops)} bottoms {min(bots)}..{max(bots)} | H top {round(H[3])} | x top {round(x[3])} | g extent {round(g[1])}..{round(g[3])} | x/fig {round(x[3]/min(tops),3)} | gfull/fig {round((g[3]-g[1])/min(tops),3)}")
    missing=[c for c in 'ãõçáéíóúâêôàüª º“”‘’–—…·×→↑♥✓●' if ord(c) not in cm]
    print('   missing:', missing)
    # advance widths for figures (tabular?)
    hm=f['hmtx']; adv=[hm[cm[ord(d)]][0] for d in '0123456789']
    print('   digit advances', set(adv))
for p in sys.argv[1:]:
    f = TTFont(p)
    if 'fvar' in f:
        axes=[(a.axisTag,a.minValue,a.defaultValue,a.maxValue) for a in f['fvar'].axes]
        print(p.split('/')[-1],'axes',axes)
        locs=[]
        tags=[a[0] for a in axes]
        if 'wdth' in tags:
            for w in (75,100,125):
                for wt in (400,700):
                    locs.append({'wdth':w,'wght':wt})
        else:
            for wt in (400,500,700):
                d={'wght':wt}
                if 'BNCE' in tags: d['BNCE']=0
                if 'INFM' in tags: d['INFM']=50
                if 'SPAC' in tags: d['SPAC']=0
                locs.append(d)
        for loc in locs:
            g=instancer.instantiateVariableFont(TTFont(p),loc)
            measure(g, str(loc))
    else:
        measure(f, p.split('/')[-1])
