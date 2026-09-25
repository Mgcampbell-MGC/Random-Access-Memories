PTAX=5.20
NET_LO,NET_HI=10400,12950
# Veneza sample-shop list prices (observed 25 Sep 2026)
tube30=9.79; pump150=24.53
cls1,cls5=0.07,0.35
print('tube30 class1',round(tube30*(1-cls1),2),'class5',round(tube30*(1-cls5),2))
print('pump150 class1',round(pump150*(1-cls1),2),'class5',round(pump150*(1-cls5),2))
# landed unit (single 30 mL tube) at 500 units (class5) and at 24 units (class1)
label=0.40; anvisa=437.50
def landed(unitp,n,freight,icms):
    return unitp+label+anvisa/n+freight+unitp*icms
for n,disc,fr in [(500,cls5,0.40),(24,cls1,1.50)]:
    u=tube30*(1-disc)
    print('tube landed n=%d'%n, round(landed(u,n,fr,0),2),'to',round(landed(u,n,fr,0.13),2))
# min order R$5000 => units of tube only
print('R$5000 buys tubes at class5:',int(5000/(tube30*(1-cls5))),' at class1:',int(5000/(tube30*(1-cls1))))
# KIT = 1 pump + 2 tubes, class5
kit_cogs=pump150*(1-cls5)+2*tube30*(1-cls5)
print('kit product cost class5',round(kit_cogs,2),'class1',round((pump150+2*tube30)*(1-cls1),2))
price=89.90
labels=3*label; inbound=1.50; outbound=5.00
for icms in (0,0.13):
    for das in (0.04,0.0565):
        cost=kit_cogs+labels+inbound+kit_cogs*icms+outbound
        contrib=price-cost-price*das
        print(f'icms {icms} das {das}: cost {cost:.2f} contrib {contrib:.2f}')
cmin=89.90-(kit_cogs+labels+inbound+kit_cogs*0.13+outbound)-89.90*0.0565
cmax=89.90-(kit_cogs+labels+inbound+outbound)-89.90*0.04
fix_lo,fix_hi=400,700
kits_lo=(NET_LO+fix_lo)/cmax; kits_hi=(NET_HI+fix_hi)/cmin
print('kits/month',round(kits_lo),round(kits_hi))
# consumption: FTU rule 1 g per full two-hand application
for apps in (3,5):
    g=apps*22*1.0; kitg=150+2*30
    print('apps',apps,'g/month',g,'kits/month per pro',round(g/kitg,2))
per_lo,per_hi=66/210,110/210
print('pros needed',round(kits_lo/per_hi),round(kits_hi/per_lo))
print('salons @5',round(kits_lo/per_hi/5),round(kits_hi/per_lo/5))
rev_lo,rev_hi=kits_lo*price,kits_hi*price
print('gross rev/month',round(rev_lo),round(rev_hi),'per year',round(rev_lo*12),round(rev_hi*12))
sp_pool=307435+102050
print('SP beauty MEI',sp_pool,'÷4',sp_pool//4)
# capital first run
first=120*pump150*(1-cls5)+480*tube30*(1-cls5)
print('first run product',round(first,2))
cap_lo=first+2*anvisa+600*label+300+0+440+0+60
cap_hi=first+2*anvisa+600*0.5+400+first*0.13+440+500+60
print('capital',round(cap_lo),round(cap_hi),'USD',round(cap_lo/PTAX),round(cap_hi/PTAX))
presale=120*price+240*24.90
print('presale value of first run',round(presale,2))
# month-12 realistic
for salons in (30,60):
    kits=salons*5*0.4
    net=kits*((cmin+cmax)/2)-550
    print('m12 salons',salons,'kits',kits,'net R$',round(net),'US$',round(net/PTAX))
# Candidate 2 store own-label economics
store_cost=tube30*(1-cls5)+0.40+0.875+0.40
for shelf in (18.90,19.90):
    print('store own-label 30ml cost',round(store_cost,2),'shelf',shelf,'gross margin %',round((shelf/1.0-store_cost)/shelf*100,1))
# IBGE PAC retail margin on revenue
print('PAC 47.7 margin/revenue',round(124066521/311582566*100,1),'wholesale',round(119350320/371038620*100,1))
# C2 fee arithmetic
for fee in (800,1500):
    print('fee',fee,'projects/month',round((NET_LO+400)/(fee*0.94),1),round((NET_HI+700)/(fee*0.94),1))
