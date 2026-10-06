import json, sys
sys.path.insert(0,'.')
from render import renderizar
TURNE = dict(titulo='ELA ESTEVE EM TODAS.', linhas=[
 ['PRÉZINHO, DIA DAS MÃES','PRIMEIRA FILA'],['FESTA JUNINA','O BIGODE FOI ELA'],['FEIRA DE CIÊNCIAS','O VULCÃO TAMBÉM'],
 ['PRONTO-SOCORRO, 3H','SEM INGRESSO. ENTROU.'],['FORMATURA','DE PÉ (COM O DEDO NA LENTE)'],['PRIMEIRO APÊ','4 VIAGENS DE CARRO'],
 ['09.05.2027','A ATRAÇÃO É ELA']])
renderizar([
 dict(html='cartaz.html', saida='teste/cartaz_amarelo.png', w=2000, h=3000, dados=dict(W=2000,H=3000,cor='amarelo',turne=TURNE)),
 dict(html='cartaz.html', saida='teste/cartaz_violeta.png', w=2000, h=3000, dados=dict(W=2000,H=3000,cor='violeta',turne=TURNE)),
])
