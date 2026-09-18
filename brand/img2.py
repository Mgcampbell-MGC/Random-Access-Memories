# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
TEAL='#1F4E4A'; CLAY='#C96F4A'; CREAM='#F7F3EC'; INK='#2B2B2B'; SAGE='#8FA89B'; RED='#A63A3A'

# ---------- 3. WHERE THE MARGIN IS ----------
fig,axes=plt.subplots(1,2,figsize=(11,4.6)); fig.patch.set_facecolor('white')
ax=axes[0]
names=['Bodysuit','Babygro','Baby bath','Towel','Blanket']
marg=[-21.0,-0.5,-13.4,16.8,39.3]
cols=[RED if m<0 else (CLAY if m<50 else SAGE) for m in marg]
ax.barh(names,marg,color=cols,height=0.6)
ax.axvline(0,color=INK,lw=1); ax.axvline(50,color=CLAY,lw=1.6,ls='--')
ax.text(50,4.65,'  50% needed',color=CLAY,fontsize=9,fontweight='bold',va='center')
ax.set_xlim(-35,75); ax.set_title('SELLING THE ITEMS SEPARATELY',fontsize=11.5,color=TEAL,fontweight='bold',pad=12)
ax.set_xlabel('gross margin  %',fontsize=9)
for s in ('top','right'): ax.spines[s].set_visible(False)
for i,m in enumerate(marg): ax.text(m+(2 if m>=0 else -2),i,f'{m:+.0f}%',va='center',ha='left' if m>=0 else 'right',fontsize=9,color=INK)
ax.tick_params(labelsize=9.5)

ax=axes[1]
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
ax.add_patch(FancyBboxPatch((0.5,1.6),9,6.6,boxstyle="round,pad=0.1,rounding_size=0.2",fc=CREAM,ec=SAGE,lw=2.5))
ax.text(5,7.5,'SELLING THE WHOLE KIT',fontsize=11.5,color=TEAL,fontweight='bold',ha='center')
ax.add_patch(Rectangle((1.4,5.0),3.0,1.5,fc='white',ec=INK,lw=1.4))
ax.text(2.9,5.75,'costs you\nR$169–230',fontsize=11,ha='center',va='center',color=INK,linespacing=1.5)
ax.annotate('',xy=(6.0,5.75),xytext=(4.6,5.75),arrowprops=dict(arrowstyle='-|>',lw=2.4,color=SAGE))
ax.add_patch(Rectangle((6.0,5.0),2.6,1.5,fc=SAGE,ec=SAGE,lw=1.4))
ax.text(7.3,5.75,'sells for\nR$359',fontsize=11,ha='center',va='center',color='white',fontweight='bold',linespacing=1.5)
ax.text(5,3.9,'+36%  to  +53%',fontsize=27,color=SAGE,fontweight='bold',ha='center')
ax.text(5,2.7,'The bag has no published price.\nEvery item inside it does.',fontsize=10,color=CLAY,ha='center',
        style='italic',linespacing=1.6)
ax.text(5,0.75,'This is the whole business. Sell the bag, not the items.',fontsize=11.5,color=TEAL,
        ha='center',fontweight='bold')
plt.tight_layout(); plt.savefig('margin.png',dpi=200,facecolor='white'); plt.close()

# ---------- 4. WHAT IS IN A KIT ----------
fig,ax=plt.subplots(figsize=(11,5.0)); ax.set_xlim(0,11); ax.set_ylim(0,5.0); ax.axis('off')
fig.patch.set_facecolor('white')
items=[('1','Mochila / backpack'),('2','Banheira (baby bath, 24 L)'),('3','Cobertor / blanket'),
 ('4','Cueiro / swaddle'),('5','Pagão / babygro'),('6','Fralda descartável RN'),
 ('7','Body manga longa'),('8','Kit enxoval'),('9','Pano de boca / muslin'),
 ('10','Par de meias'),('11','Toalha de banho'),('12','Toalhas umedecidas'),
 ('13','Sabonete líquido'),('14','Shampoo infantil'),('15','Óleo infantil'),
 ('16','Kit higiene (pente, escova, tesoura)'),('17','Saboneteira')]
ax.text(0.35,4.65,'WHAT ONE REAL KIT CONTAINED',fontsize=14,color=TEAL,fontweight='bold')
ax.text(0.35,4.28,'Itaquaquecetuba / SP — 5.000 kits sold at R$359,05 each.  The town hall wrote this list, not you.',
        fontsize=9.5,color=CLAY)
for i,(n,t) in enumerate(items):
    col=i//6; row=i%6
    x=0.35+col*3.62; y=3.72-row*0.56
    ax.add_patch(FancyBboxPatch((x,y-0.19),0.40,0.38,boxstyle="round,pad=0.02,rounding_size=0.06",fc=TEAL,ec=TEAL))
    ax.text(x+0.20,y,n,fontsize=8.6,color='white',ha='center',va='center',fontweight='bold')
    ax.text(x+0.56,y,t,fontsize=9.4,color=INK,va='center')
ax.add_patch(FancyBboxPatch((7.6,0.28),3.05,1.30,boxstyle="round,pad=0.05,rounding_size=0.12",fc=CREAM,ec=SAGE,lw=2))
ax.text(9.13,1.28,'Another town will ask for',fontsize=8.8,color=INK,ha='center')
ax.text(9.13,1.00,'12 items, or 22, or a',fontsize=8.8,color=INK,ha='center')
ax.text(9.13,0.72,'different mix entirely.',fontsize=8.8,color=INK,ha='center')
ax.text(9.13,0.44,'The script prices whatever arrives.',fontsize=8.6,color=CLAY,ha='center',fontweight='bold')
plt.tight_layout(); plt.savefig('kit.png',dpi=200,facecolor='white'); plt.close()

# ---------- 5. WHERE TO SELL ----------
fig,ax=plt.subplots(figsize=(11,4.4)); fig.patch.set_facecolor('white')
ufs=['MG','MA','BA','CE','PE','SE','PA','RN','MT','SP','ES']
val=[632,443,361,139,221,234,86,71,262,200,96]
gross=[4.1,42.7,13.0,28.3,20.0,25.0,31.6,18.9,-1.7,-10.1,-30.4]
cols=[SAGE if g>10 else (CLAY if g>0 else RED) for g in gross]
ax.bar(ufs,val,color=cols,width=0.62)
ax.set_ylabel('R$ thousand of business you could win at a real margin',fontsize=9)
ax.set_title('WHERE TO BID  —  and São Paulo is where you BUY, never where you sell',
             fontsize=12.5,color=TEAL,fontweight='bold',pad=12)
for i,(v,g) in enumerate(zip(val,gross)):
    ax.text(i,v+14,f'{g:+.0f}%',ha='center',fontsize=8.8,color=INK,fontweight='bold')
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.tick_params(labelsize=10)
ax.text(0.5,0.92,'green = healthy margin   ·   orange = thin   ·   red = you lose money',
        transform=ax.transAxes,ha='center',fontsize=9,color=INK,style='italic')
plt.tight_layout(); plt.savefig('states.png',dpi=200,facecolor='white'); plt.close()
print("ok")
