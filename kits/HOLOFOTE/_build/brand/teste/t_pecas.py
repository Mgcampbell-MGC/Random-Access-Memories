import sys, json
sys.path.insert(0, '.')
from render import renderizar
B1 = dict(receita='boletim', formato='1x1', cor='amarelo', data='02.05', linhas=['bom dia. faltam 7 dias', 'pro show. pode encaminhar.'])
B4 = dict(receita='boletim', formato='9x16', cor='violeta', data='05.05', linhas=['bom dia. ingressos com os filhos.', '(os filhos sabem quem são.)'])
B8 = dict(receita='boletim', formato='1x1', cor='rosa', data='09.05', linhas=['bom dia. terceiro sinal.', 'o show é hoje.'])
T = [['ESTREIA · 21.11.1999 · 06:40', 'QUEM FEZ O SHOW FOI ELA'], ['PRÉZINHO, DIA DAS MÃES', 'PRIMEIRA FILA'], ['FESTA JUNINA', 'O BIGODE FOI ELA'],
     ['PRONTO-SOCORRO, 3H', 'SEM INGRESSO. ENTROU.'], ['FORMATURA', 'DE PÉ (COM O DEDO NA LENTE)'], ['09.05.2027', 'A ATRAÇÃO É ELA']]
jobs = dict(b1=(1080,1080,B1), b4=(1080,1920,B4), b8=(1080,1080,B8), c03=(1080,1920,dict(receita='C03')), c07=(1080,1920,dict(receita='C07')), c09=(1080,1920,dict(receita='C09', turne=T)))
sel = sys.argv[1:] or list(jobs)
r = renderizar([dict(html='peca.html', saida=f'teste/{k}.png', w=jobs[k][0], h=jobs[k][1], dados=jobs[k][2]) for k in sel])
for k, x in zip(sel, r): print(k, [q for q in x['qa'] if abs(q.get('erro',0))>0.5], x['console'], [(q['item'][:20], q.get('cap')) for q in x['qa']][:12])
