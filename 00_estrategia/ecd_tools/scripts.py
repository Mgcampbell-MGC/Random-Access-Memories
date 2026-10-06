ads={
'A1-hookA':("Pior show que ela já viu: você.","Esqueceu a coreografia, chorou, acenou pra mãe errada."),
'A1-hookB':("Prézinho. Você era um girassol.","Esqueceu a coreografia. Chorou. Acenou pra mãe errada."),
'A1-hookC(H02)':("Prézinho. Você, de abelhinha.","Errou o passo. Chorou. Acenou pra mãe errada."),
'A2-hookA':("Primeiro sinal.","Domingo, nove de maio. Atração principal: ela. Abertura: você."),
'A2-hookB':("Comunicado da produção.","Domingo, nove de maio. Atração principal: ela. Abertura: você."),
'A3-hookA':("Dois dias de fila por um ingresso.","Chorou na grade. E ela te buscou na porta, à uma da manhã."),
'A3-hookB':("Você sabe a setlist de todo mundo.","Menos a dela. Ela tá em turnê desde que você nasceu."),
'A3-hookC(H02)':("Gritou o nome dele o show inteiro.","Ele não sabe o seu. Ela escolheu o seu antes de você nascer."),
}
for k,(h,b) in ads.items():
    t=h+' '+b
    print(f"{k:14s} hook {len(h):3d} ch {len(h.split()):2d} w | total {len(t):3d} ch | {len(t)/6:4.1f} cps over 6 s | hook {len(h)/1.5:4.1f} cps over 1,5 s")
for k,(h,b) in ads.items():
    print(k,'hook over 2,0 s:',round(len(h)/2,1),'cps; body over 4,0 s:',round(len(b)/4,1))
