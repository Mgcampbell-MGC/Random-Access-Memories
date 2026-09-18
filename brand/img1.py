# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
TEAL='#1F4E4A'; CLAY='#C96F4A'; CREAM='#F7F3EC'; INK='#2B2B2B'; SAGE='#8FA89B'; LIGHT='#E8E0D4'

# ---------- 1. WORDMARK ----------
fig,ax=plt.subplots(figsize=(9,3.1)); ax.set_xlim(0,9); ax.set_ylim(0,3.1); ax.axis('off')
fig.patch.set_facecolor(CREAM)
# mark: two nested arcs suggesting an embrace / cradle
import numpy as np
th=np.linspace(np.pi*1.05,np.pi*1.95,200)
for r,w,c in ((0.92,9,TEAL),(0.62,9,CLAY)):
    ax.plot(1.55+r*np.cos(th),1.75+r*np.sin(th),lw=w,color=c,solid_capstyle='round')
ax.add_patch(Circle((1.55,1.62),0.20,color=TEAL))
ax.text(3.0,1.82,'ACOLHE',fontsize=46,color=TEAL,fontweight='bold',va='center',family='DejaVu Sans')
ax.text(3.08,1.12,'ENXOVAIS  ·  SUPRIMENTOS PARA O SETOR PÚBLICO',
        fontsize=10.5,color=CLAY,va='center',family='DejaVu Sans')
plt.tight_layout(); plt.savefig('logo.png',dpi=200,facecolor=CREAM); plt.close()

# ---------- 2. HOW IT WORKS ----------
fig,ax=plt.subplots(figsize=(11,4.4)); ax.set_xlim(0,11); ax.set_ylim(0,4.4); ax.axis('off')
fig.patch.set_facecolor('white')
steps=[("DIA 0","The town hall\npublishes the\ntender + item list",TEAL),
       ("DIA 0","Your script prices\nevery line against\nyour cost table",TEAL),
       ("DIA 1","You bid.\nCost: R$0",TEAL),
       ("DIA 10","Auction closes.\nWin or lose.",CLAY),
       ("DIA 11","ONLY NOW\nyou buy the goods",CLAY),
       ("DIA 15","Assemble + ship\nto the town hall",SAGE),
       ("DIA 45","Invoice attested.\nYou get paid.",SAGE)]
w=1.38; gap=0.16; x=0.28
for i,(d,t,c) in enumerate(steps):
    ax.add_patch(FancyBboxPatch((x,1.25),w,2.05,boxstyle="round,pad=0.05,rounding_size=0.10",
                                fc=CREAM if c!=CLAY else '#FAEDE6',ec=c,lw=2.0))
    ax.text(x+w/2,3.02,d,fontsize=9.5,color=c,fontweight='bold',ha='center',va='center')
    ax.text(x+w/2,2.12,t,fontsize=8.6,color=INK,ha='center',va='center',linespacing=1.55)
    if i<len(steps)-1:
        ax.add_patch(FancyArrowPatch((x+w+0.01,2.27),(x+w+gap-0.01,2.27),
                     arrowstyle='-|>',mutation_scale=13,color=SAGE,lw=1.8))
    x+=w+gap
ax.text(5.5,3.95,'HOW ONE ORDER RUNS, END TO END',fontsize=15,color=TEAL,fontweight='bold',ha='center')
ax.add_patch(FancyBboxPatch((0.28,0.30),10.44,0.72,boxstyle="round,pad=0.04,rounding_size=0.08",
                            fc='#FAEDE6',ec=CLAY,lw=1.8))
ax.text(5.5,0.66,'Nothing is ever bought on speculation. If you lose, you spent R$0 and hold no stock.',
        fontsize=11,color=CLAY,ha='center',va='center',fontweight='bold')
plt.tight_layout(); plt.savefig('flow.png',dpi=200,facecolor='white'); plt.close()
print("ok")
