"""Tabela de métricas de glifo para o motor de layout em JS (holofote.js).

Por que existe: 'toda linha ocupa a largura inteira' (plataforma §D.5, regra 2) tem de ser medido na TINTA, não na
caixa de avanço. O DOM só dá a caixa de avanço; o JS subtrai o side-bearing esquerdo do primeiro glifo e o direito
do último, que vêm desta tabela, calculada nos arquivos de fonte oficiais em _build/fonts/.

Saída: _build/brand/metricas.js  (window.HF_METRICAS)
  X  = Special Gothic Expanded One          {upm, cap, g:{char:[adv,xMin,xMax,yMin,yMax]}}
  C  = Special Gothic Condensed One
  S  = Shantell Sans wght 500 INFM 60 BNCE 0 (a Fã, impressão)
  V  = Special Gothic variável: V[wght][wdth] para wght 400/700 e wdth 75..125 (passo 1)
Uso: python metricas.py
"""
import json, os
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), 'fonts')

# Todo caractere que qualquer peça do sistema pode compor (português completo + figuras + sinais)
CHARS = (''.join(chr(c) for c in range(0x20, 0x7F)) +
         'ÁÀÂÃÄÉÊÈÍÎÓÔÕÖÚÜÇáàâãäéêèíîóôõöúüçªº«»·…–—“”‘’↑→←↓×§°')


def tabela(tt, glyphset):
    cmap = tt.getBestCmap()
    hm = tt['hmtx']
    out = {}
    for ch in CHARS:
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        bp = BoundsPen(glyphset)
        glyphset[gname].draw(bp)
        adv = glyphset[gname].width if hasattr(glyphset[gname], 'width') else hm[gname][0]
        if bp.bounds is None:  # espaço
            out[ch] = [round(adv, 1), 0, 0, 0, 0]
        else:
            x0, y0, x1, y1 = bp.bounds
            out[ch] = [round(adv, 1), round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)]
    return out


def main():
    M = {}
    for key, fn in (('X', 'SpecialGothicExpandedOne-Regular.ttf'), ('C', 'SpecialGothicCondensedOne-Regular.ttf')):
        tt = TTFont(os.path.join(FONTS, fn))
        M[key] = dict(upm=tt['head'].unitsPerEm, cap=tt['OS/2'].sCapHeight, x=tt['OS/2'].sxHeight,
                      g=tabela(tt, tt.getGlyphSet()))
    sh = TTFont(os.path.join(FONTS, 'ShantellSans-VF.ttf'))
    gs = sh.getGlyphSet(location={'wght': 500, 'INFM': 60, 'BNCE': 0, 'SPAC': 0})
    g = tabela(sh, gs)
    M['S'] = dict(upm=1000, cap=round(g['H'][4], 1), x=round(g['x'][4], 1), g=g)
    vf = TTFont(os.path.join(FONTS, 'SpecialGothic-VF.ttf'))
    V = {}
    for wght in (400, 500, 700):
        V[wght] = {}
        for wdth in range(75, 126):
            gs = vf.getGlyphSet(location={'wght': wght, 'wdth': wdth})
            V[wght][wdth] = tabela(vf, gs)
    M['V'] = dict(upm=1000, cap=710, x=504, g=V)
    js = 'window.HF_METRICAS = ' + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + ';\n'
    out = os.path.join(HERE, 'metricas.js')
    open(out, 'w', encoding='utf-8').write(js)
    print('escrito', out, round(len(js) / 1024), 'KB', '| Shantell x-height', M['S']['x'], 'cap', M['S']['cap'])


if __name__ == '__main__':
    main()
