# OL5: how Sol legally opens and runs O LANÇAMENTO in São Paulo, and what it costs (25 Sep 2026)

**Hole:** "Exactly how does Sol legally open and run this in São Paulo, and what does it cost in tax and setup?"
**Verdict: CLOSED.** The residual risks are listed at the end.

**The plan is right in outline: an ME on Simples Nacional with a fator-r pró-labore, and 7311-4/00 avoided.** It gets five things wrong or leaves them out:

1. **Fator r is not what puts her films in Anexo III. The law already does that.** Film production falls under LC 123 art. 18 §5-B XV, which is Anexo III whatever the payroll. What fator r protects is the **stills**, which the Receita can classify as "design" or "publicidade".
2. **"≈9,1–9,4% all-in on every tier" only holds inside the target band.** At R$25.000/month the fator-r route costs **14,2%**.
3. **7410-2/03 is the wrong code.** It is "Design de produto" (fashion, jewellery, furniture). "Criação de imagens digitais" sits under **7410-2/99**.
4. **There is a timing trap that the plan does not mention.** The Simples option has to be switched on at the moment the CNPJ is registered. If it is missed, she stays out of Simples until **January 2028**.
5. **From 1 Nov 2026 the notas are issued through the national system.** Every Simples company must use the Emissor Nacional NFS-e from that date, so the service code she actually types is the **national code 130301**. The São Paulo code 06808 comes second.

Local copies of every source are in `work/ol5/`. The arithmetic is in `work/ol5/calc.py`.

---

## 1. Which CNAEs, which Anexo, and can she be an MEI?

### What the statute says (LC 123/2006, compiled text at Planalto)
Source: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm

- **§5-B, Anexo III directly.** *"serão tributadas na forma do Anexo III … XV - produções cinematográficas, audiovisuais, artísticas e culturais, sua exibição ou apresentação, inclusive no caso de música, literatura, artes cênicas, artes visuais, cinematográficas e audiovisuais."*
- **§5-I, Anexo V.** *"VI - engenharia, medição, … pesquisa, design, desenho e agronomia; … X - jornalismo e publicidade;"*
- **§5-J, the fator-r escape.** *"As atividades de prestação de serviços a que se refere o § 5º-I serão tributadas na forma do Anexo III desta Lei Complementar caso a razão entre a folha de salários e a receita bruta da pessoa jurídica seja igual ou superior a 28% (vinte e oito por cento)."*
- **§5-M, which activities fall to Anexo V when r is below 28%.** *"I - nos incisos XVI, XVIII, XIX, XX e XXI do § 5º-B deste artigo; II - no § 5º-D deste artigo."*
  - **Inciso XV is not on that list.** So audiovisual production stays in Anexo III even with zero payroll.

### What the Receita has ruled (Soluções de Consulta)
Each was read today on Receita's own normas search, at https://normas.receita.fazenda.gov.br/sijut2consulta/consulta.action.

- **SC COSIT 466/2017** (idAto=86540): *"A empresa optante pelo Simples Nacional contratada para prestar serviço de produção de filmes para publicidade, em relação a essa atividade, deve ser tributada na forma do Anexo III … desde que não preste o serviço de publicidade propriamente dito."*
- **SC COSIT 180/2019:** *"Os serviços de produção audiovisual, design gráfico, videografismos, produção de áudios, vídeos institucionais … enquadrando-se como serviço de produção audiovisual constante do inciso XV do parágrafo 5º-B do art. 18 da LC nº 123."*
  - Its context was withholding on labour supply, so it is supportive but not conclusive for stills.
- **SC COSIT 243/2025** (28/11/2025), on design: *"na apuração do Simples Nacional deve considerar as alíquotas do Anexo III, se o fator "r" for igual ou superior a 0,28 … ou do Anexo V, quando o fator "r" for inferior a 0,28."*
- **SC COSIT 145/2023**, on bundled contracts: *"Se esses contratos conjugados não fizerem essa discriminação de maneira clara, então todo o valor recebido pelas duas atividades é considerado receita de prestação de serviço de limpeza, que deve ser tributada na forma do Anexo IV."*
  - In other words, a bundle whose parts are not priced separately is taxed entirely at the worse Anexo.
- **SC COSIT 13/2022:** *"as receitas de promoção de vendas (CNAE 7319-0/02) e de marketing direto (CNAE 7319-0/03) são tributadas pelo Anexo III."*

### What each CNAE covers (IBGE/CONCLA API)
Source pattern: https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/{code}

| CNAE | IBGE text (quoted) | Simples | Vedação (Res. CGSN 140, Anexos VI/VII) | MEI (Anexo XI) | Federal low-risk (CGSIM 51/2019 Anexo I) |
|---|---|---|---|---|---|
| **5911-1/02** Produção de filmes para publicidade | "VÍDEOS PARA PUBLICIDADE; PRODUÇÃO DE"; "a produção de filmes em qualquer suporte (película, vídeo e DVD) para publicidade" | **Anexo III direct** (§5-B XV; SC 466/2017) | none | **no** | yes |
| 5911-1/99 | "PRODUÇÃO, GRAVAÇÃO DE VÍDEOS PARA DIFUSÃO NA INTERNET"; "COMPUTAÇÃO GRÁFICA NA PRODUÇÃO DE FILMES" | Anexo III direct (XV) | none | no | not listed |
| 5912-0/99 (post-production) | "ANIMAÇÃO EM FILMES … EFEITOS ESPECIAIS PARA FILMES" | Anexo III direct (XV) | none | **yes, "EDITOR(A) DE VÍDEO INDEPENDENTE"** | **not listed**, so it may trigger licensing |
| **7410-2/99** | "CRIAÇÃO DE IMAGENS DIGITAIS; … DESIGN GRÁFICO" | design, so **§5-I VI: fator r (III/V)** | none | no | yes |
| 7410-2/03 | "DESIGN DE PRODUTO" (furniture, jewellery, fashion) | fator r | none | no | yes |
| 7420-0/01 | "PRODUÇÃO FOTOGRÁFICA PARA PUBLICIDADE"; camera photography | Anexo III (XV "artes visuais" or §5-F residual) | none | **yes, "FOTÓGRAFO(A) INDEPENDENTE"** | yes |
| 7420-0/04 | filming of parties and events | Anexo III | none | yes, "FILMADOR(A)" | yes |
| 7319-0/99 | "COMPUTAÇÃO GRÁFICA PARA PUBLICIDADE" | publicidade, so **§5-I X: fator r** | none | "Bike propagandista" only | not listed |
| 7311-4/00 | "a criação e a produção de campanhas de publicidade" | publicidade, so **§5-I X: fator r** | none | no | yes |

**Notes on the table**
- **Vedação check.** Anexo VI (impeditive codes, https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=50966) and Anexo VII (ambiguous codes, …idArquivoBinario=54769) contain **none** of these codes.
  - The VI copy is dated 2019. No newer version was found, so treat this as UNVERIFIED for amendments made after 2019.
- **MEI list.** Read from https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/Anexo_XI.pdf (PDF created 16/10/2025).
- **Low-risk list.** Read from https://www.gov.br/empresas-e-negocios/pt-br/drei/cgsim/resolucoes-cgsim/arquivos/resolucao51alteradapela68.pdf.
- **The code does not set the Anexo; the activity does.** SC 466 says *"em relação a essa atividade"*.

**Best primary CNAE for "advertising images and short films for brands, made with software/AI, no physical shoot":**
- **Primary 5911-1/02.** It is honest, it is Anexo III by statute, and it is low-risk.
- **Secondary 7410-2/99.** This is the literal IBGE home of "criação de imagens digitais" and is also low-risk.
- **Leave out:**
  - 7410-2/03, the wrong kind of design;
  - 7420-0/01, which implies a camera shoot;
  - 5912-0/99, which is not on the federal low-risk list;
  - 7319-0/99 and 7311-4/00, which are publicity and therefore §5-I X.

### MEI: possible on paper, not worth it
- **Allowed occupations.** The nearest MEI occupations are *"EDITOR(A) DE VÍDEO INDEPENDENTE 5912-0/99"* and *"FOTÓGRAFO(A) INDEPENDENTE 7420-0/01"*. There is no MEI occupation for 5911-1/02, 7410-2/99 or 7311-4/00.
- **Ceiling.** LC 123 art. 18-A §1 sets *"até R$ 81.000,00"* a year. For a company starting mid-year, §2 sets *"R$ 6.750,00 … multiplicados pelo número de meses"*.
  - The target is R$12.200–15.800/month, which is **1,8–2,3× the monthly MEI ceiling**.
- **What happens if she goes over.** The penalty is set by §7 III b: *"retroativamente ao início de atividade, na hipótese de ter ultrapassado o referido limite em mais de 20%"*.
  - An ex-MEI has no pró-labore history, so fator r is about 0.
  - Her stills could then be re-taxed back to the start date at **Anexo V, 15,5%**.
- **Leaving MEI voluntarily only works in January.** The 2027 Roteiro says *"Não houve alteração na opção pelo SIMEI. Essa deverá ser realizada no decorrer do mês de janeiro"*.
  - Res. CGSN 190/2026 art. 144-D then carries the MEI months into the RBT12 and FS12 (last-12-months revenue and payroll).
  - So the first ME months of 2027 would run with FS12 ≈ 0, which means **Anexo V on the stills** until the payroll catches up.
- **What MEI would save.** The MEI DAS would be **R$86,05/month** (5% × R$1.621 + R$5 ISS; computed). Over October–December 2026 that saves roughly **R$1.700–1.900 (≈US$350)**.
  - The saving disappears once the SLU conversion and the Anexo V exposure are counted.
- **Verdict:** skip MEI.

---

## 2. Fator r: how it works and what it costs

**What counts as payroll.** From LC 123 §24 (above): *"considera-se folha de salários … o montante pago, nos doze meses anteriores ao período de apuração, … acrescido do montante efetivamente recolhido a título de contribuição patronal previdenciária e FGTS, incluídas as retiradas de pró-labore."*

**How the rule changes on 1 Jan 2027** (Res. CGSN 190/2026, DOU 10/08/2026, https://www.in.gov.br/web/dou/-/resolucao-cgsn-n-190-de-4-de-agosto-de-2026-724454118):
- FS12 becomes *"a folha de salários dos 12 (doze) meses antecedentes ao mês anterior ao PA"*.
- *"O fator "r" referente aos 2 (dois) primeiros meses de início de atividades será considerado 0,28."*
- **SC COSIT 17/2021:** FS12 is counted on a cash basis.
- **SC COSIT 65/2025:** *"a folha de salários não está limitada ao teto do INSS."*

**INSS on the pró-labore: 11%, withheld by the company, on top of the DAS.**
- **The rate.** IN RFB 2.110/2022 art. 37 II (https://www.in.gov.br/web/dou/-/instrucao-normativa-rfb-n-2.110-de-17-de-outubro-de-2022-437619362) sets *"11% (onze por cento), em face da dedução de 45% … da contribuição patronal recolhida ou declarada pelo contratante"*.
- **It applies to Simples companies.** Art. 41 says: *"As disposições contidas nesta Seção aplicam-se inclusive: I - ao contribuinte individual que presta serviços a empresa optante pelo Simples Nacional"*.
- **Months with no revenue are the exception.** SC COSIT 178/2026 (22/09/2026) applies **20%** to the partner's pró-labore in a month with no revenue.
  - That case was a company in Anexos I and IV, so how far it reaches is UNVERIFIED. **Avoid paying pró-labore in months with zero revenue.**
- **There is no employer charge on top.** LC 123 art. 13 VI puts the CPP (employer social security) inside the DAS *"exceto no caso da microempresa e da empresa de pequeno porte que se dedique às atividades … referidas no § 5º-C"*, which is Anexo IV.
  - In Anexo III, 43,40% of the DAS *is* the CPP.

**Other inputs to the arithmetic**

| Input | Value | Source |
|---|---|---|
| Salário mínimo | R$1.621,00 | Decreto 12.797/2025, https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12797.htm |
| IRPF monthly table | exempt to 2.428,80; 7,5%/182,16; 15%/394,16; 22,5%/675,49; above 4.664,68 at 27,5%/908,73 | Lei 15.191/2025, https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15191.htm |
| IRPF reduction | *"até R$ 5.000,00 … (de modo que o imposto devido seja zero)"*; from 5.000,01 to 7.350: *"R$ 978,62 - (0,133145 x rendimentos tributáveis…)"* | Lei 15.270/2025, https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15270.htm |
| Anexo III | 1st band 6,00%; 2nd band 11,20% minus 9.360 | LC 123 |
| Anexo V | 1st band 15,50%; 2nd band 18,00% minus 4.500 | LC 123 |

**All-in tax as % of revenue** (DAS + 11% INSS + IRPF on the pró-labore; RBT12 = 12 × monthly revenue)

| Monthly revenue | **A. Fator r** (pró-labore 28%) | B. Everything accepted as audiovisual (pró-labore = 1 minimum wage) | C. Stills in Anexo V (no fator r) |
|---|---|---|---|
| R$12.200 | **9,08%** (DAS 732 + INSS 375,76 + IRPF 0) | 7,46% | 16,96% |
| R$15.000 | **9,08%** (DAS 900 + INSS 462 + IRPF 0; pró-labore R$4.200) | 7,19% | 16,69% |
| R$15.800 | **9,34%** | 7,39% | 16,76% |
| R$25.000 | **14,19%** (DAS 2.020 at 8,08% + INSS 770 + **IRPF 757,92** on a R$7.000 pró-labore) | 8,79% | 17,21% |

**How to read the table**
- **Route A is the right default.** Nobody has ruled that AI-composited stills are "artes visuais". Fator r is calculated on **total** revenue, so it cannot be applied to the stills alone. Unless the bundle's parts are priced separately (SC 145/2023), a bundle is dragged to the worse Anexo.
- **What the insurance costs.** At the target it costs about **1,9 points of revenue** over route B. At R$25.000 it costs about **5,4 points**, because the fator-r pró-labore stops being IRPF-free once revenue passes about **R$17.860/month** (5.000 ÷ 0,28).
- **Route C must never happen.** A blend of 40% film and 60% stills with no fator r comes to **12,89%**.
- **The INSS is not pure cost.** It buys her a pension, which a pure-dividend setup would not.
- **Open question:** does the CPP inside the DAS count towards FS12? UNVERIFIED. If it does, the pró-labore she needs drops by about R$390/month at R$15k. **Plan without it.**

**Taking the rest as dividends needs full bookkeeping.** LC 123 art. 14 §1–2 limits tax-free distributions to the presumed profit (32% for services) *"subtraído do valor devido na forma do Simples Nacional no período"*, and *"§ 2º O disposto no § 1º … não se aplica na hipótese de a pessoa jurídica manter escrituração contábil e evidenciar lucro superior"*.
- At R$15k/month the cap without books is about R$3.900–4.764/month. She needs about R$6–8k/month on top of the pró-labore.
- **So the accountant must keep full books.** Contabilizei's plan says "Contabilidade completa".

---

## 3. NFS-e and ISS in São Paulo

**ISS rates (Lei 13.701/2003, https://legislacao.prefeitura.sp.gov.br/leis/lei-13701-de-24-de-dezembro-de-2003)**
- **The 2% band.** Art. 16 I applies 2% to *"q) no subitem 23.01 … programação visual, comunicação visual e congêneres"* and *"r) nos subitens 13.01, 13.02 e 13.03 …"*. Both were added by Lei 17.719/2021, from 1 Jan 2022.
- **What 13.02 means in São Paulo's list.** *"13.02 - Fotografia e cinematografia, inclusive revelação, ampliação, cópia, reprodução, trucagem e congêneres."* São Paulo numbers this 13.02; LC 116 numbers it 13.03.
- **Advertising pays 5%.** *"17.06 - Propaganda e publicidade, inclusive … elaboração de desenhos, textos e demais materiais publicitários"* is not in the 2% band, so it is **5%**.
  - 17.06 also appears on art. 9 II c's list for **ISS withholding by the client**, *"conforme cronograma a ser estabelecido pela Secretaria Municipal de Finanças"*. Whether that schedule is in force is UNVERIFIED.

**Municipal code.** IN SF/SUREM 19/2021 annex: *"06808 13.02 Fotografia e cinematografia, inclusive revelação, ampliação, cópia, retocagem, reprodução, trucagem e congêneres (inclusive para televisão). PJ 2%"*.
- The only other 2% option is 02501 (23.01).
- Neither code is in the list of codes closed on 31/12/2025, which was checked in both official xlsx files.
- Source: https://legislacao.prefeitura.sp.gov.br/instrucao-normativa-secretaria-municipal-da-fazenda-sf-surem-19-de-22-de-dezembro-de-2021/anexo/61f1544a1411920679f880ac/Anexo%20da%20Instru%C3%A7%C3%A3o%20Normativa%20SF-SUREM%20n%C2%BA%2019_2021.pdf

**From 1 Nov 2026 the national system is mandatory.** Res. CGSN 191/2026 (https://www.in.gov.br/en/web/dou/-/resolucao-cgsn-n-191-de-4-de-agosto-de-2026-724399487): *"a Microempresa (ME) ou Empresa de Pequeno Porte (EPP) optante pelo Simples Nacional utilizará, obrigatoriamente, a Nota Fiscal de Serviço eletrônica (NFS-e) de padrão nacional, emitida pelo Emissor Nacional da NFS-e"*, with effect *"a partir de 01 de novembro de 2026"*.
- São Paulo confirms it: *"foi adiada para 1º de novembro de 2026"* (https://notadomilhao.sf.prefeitura.sp.gov.br/noticias/exigencia-de-emissao-da-nfs-e-pelo-sistema-nacional-e-para-1o-de-novembro-de-2026/).

**Codes she will actually type in the Emissor Nacional** (national list, ANEXO_B, v1.01 of 22/01/2026, https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/documentacao-atual/anexo_b-nbs2-lista_servico_nacional-snnfse-v1-01-20260122.xlsx)
- **Service code:** **130301**, *"Fotografia e cinematografia, inclusive revelação, ampliação, cópia, reprodução, trucagem e congêneres."*
  - The alternatives, 230101 and 170601, are less suitable.
- **NBS codes:**
  - 1.1408.12.00, *"Serviços fotográficos e videográficos para propaganda"*;
  - 1.2501.21.00, *"Serviços de produção de programas de televisão, videoteipes e filmes"*.
  - **Avoid** 1.1409.30.00 (*"design de marcas, imagens…"*) and 1.1406.11.00 (*"campanhas publicitárias"*), because they describe the Anexo V activities.

**Is ISS inside the DAS? Yes.** Anexo III splits the DAS as *"ISS 33,50%"* in the 1st band (≈2,01% of revenue) and 32,00% in the 2nd.
- Inside Simples she pays that share, not the municipal rate. Only ME/EPP-specific benefits under §20 reduce it.
- **So choosing 13.02 over 17.06 does not change her ISS today.** It matters for three reasons: which Anexo the activity looks like, withholding by clients, and her rate if she ever leaves Simples.

**ISS is due in São Paulo.** LC 116 art. 3 makes the tax due *"no local do estabelecimento prestador"*. Neither 13.03 nor 17.06 is among the exceptions.

---

## 4. Tax reform, 2026–2027, for a Simples ME issuing NFS-e

**2026: nothing to pay.** LC 214/2025 art. 348 III (https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm): the 2026 test rates *"c) não serão aplicadas em relação às operações dos contribuintes optantes pelo Simples Nacional."*

**NFS-e fields.**
- For Simples companies, Ato Conjunto RFB/CGIBS nº 4/2026 §1 applies: *"a obrigatoriedade de emissão dos documentos … iniciar-se-á em 1º de janeiro de 2027."* (PDF: https://www.cgibs.gov.br/upload/arquivos/202607/31091735-20260730-16h30-ato-conjunto-rfb-cgibs-na-c2-ba-4-260731-090909.pdf)
- CGNFS-e adds: *"a ausência ou omissão das informações relativas ao IBS e à CBS na NFS-e até 31 de dezembro de 2026 não acarretará a rejeição do documento fiscal"* (https://www.gov.br/nfse/pt-br/noticias/cgnfs-e-orienta-sobre-os-prazos-para%20destaque-de-ibs-cbs-nas-notas-fiscais-de-servico).

**2027: the same DAS rate.** LC 214 Anexo XX rewrites Anexo III for 2027–2028 with **the same 6,00% and 11,20%/9.360**. CBS replaces PIS/COFINS in the split: 1st band *"CBS 15,43% … IBS 0,17%"*. Anexo V likewise keeps 15,50% and 18,00%/4.500.

**Optional "hybrid" regime: do not take it.** LC 214 art. 41 §3 lets a Simples company pay IBS/CBS outside the DAS. The choice is made in September or March.
- The Simples portal notice of 12/08/2026: *"A empresa que já é optante pelo Simples Nacional poderá optar por recolher a CBS e o IBS fora do regime único entre 1º e 30 de setembro … A escolha valerá para o período de janeiro a junho do ano seguinte"*.
- **Why it would not help her.** A client in the regular regime can only credit what she actually paid inside the DAS (art. 47 §9 II: *"em montante equivalente ao devido por meio desse regime"*), which is under 1% of price. Most indie brands are Simples themselves, so they cannot use credits anyway.
- **When to revisit:** only if a Lucro Real client demands full credits. The next window is March 2027.

**New rules from 2027 (Res. CGSN 190/2026)**
- **Revenue is recognised when the nota is issued, including deposits.** *"§ 8º As receitas … consideram-se auferidas no momento do faturamento da operação … § 9º Aplica-se o disposto no § 8º também na hipótese de valores recebidos adiantadamente"*, and *"considera-se faturamento: I - a emissão de documento fiscal…"*.
- **DEFIS is abolished.** Its information moves into the PGDAS-D once a year (Simples portal notice, 12/08/2026).
- **The Simples option window moves to September** (art. 6 §1: *"01 (um) de setembro a 30 (trinta) de setembro"*).

---

## 5. Setup: steps, time, fees and monthly cost

**The trap to avoid first.** Roteiro da Opção 2027, v. 18/09/2026 (https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/Roteiro%20da%20op%C3%A7%C3%A3o%20pelo%20Simles%20Nacional%20para%20o%20ano%20de%202027.pdf):
- *"a partir de 01/12/2025 a nova empresa deve formalizar sua intenção de optar pelo Simples Nacional no exato momento que solicitar a inscrição do CNPJ … Caso a opção não seja realizada no MAT no momento da inscrição do CNPJ, a empresa somente poderá solicitar o ingresso no Simples Nacional no próximo período regular de opção"*.
  - For an October 2026 company, the next regular period is September 2027, which means Simples only from **1/1/2028**.
- *"Não será possível cancelar o pedido de opção pelo Simples Nacional realizado como empresa em início de atividades."*

**Entity: SLU (sociedade limitada unipessoal), not EI (empresário individual)**
- CC art. 1.052: *"a responsabilidade de cada sócio é restrita ao valor de suas quotas … § 1º A sociedade limitada pode ser constituída por 1 (uma) ou mais pessoas."*
- **The name on every nota.** An EI *"opera sob firma constituída por seu nome"* (art. 1.156). A limitada *"Pode … adotar firma ou denominação"* (art. 1.158).
  - So an SLU puts "O LANÇAMENTO ESTÚDIO LTDA" on every nota, not Sol's civil name. **That matters for C2.**
- Source: https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm, as fetched today.

**Steps**
1. Get a gov.br account at silver or gold level.
2. Run the viability check (name and home address) through REDESIM/JUCESP VRE.
3. File the DBE/MAT and **switch Simples on**.
4. Register the SLU at JUCESP with a digital signature.
5. Receive the CNPJ and the São Paulo CCM (municipal registration).
6. Before 1 Nov 2026, use the NFS-e Paulistana with code 06808. From 1 Nov, use the Emissor Nacional with 130301.
7. Open a PJ bank account and set the CNPJ as the Pix key.
8. Have the accountant run the pró-labore through eSocial/DCTFWeb and file the PGDAS-D every month.

**Time.** For São Paulo state, the Mapa de Empresas bulletin for the 2nd four-month period of 2025 says *"O estado de São Paulo registrou o maior tempo de abertura de empresas no Brasil: 1 dia e 10 horas"* (https://www.gov.br/empresas-e-negocios/pt-br/mapa-de-empresas/boletins/mapa-de-empresas-boletim-2o-quadrimestre-2025.pdf). That covers viability and registration only.
- Bank, NFS-e and payroll setup take a few more days. Allow **1–2 weeks** end to end (UNVERIFIED).

**No operating licence (federal default).** 5911-1/02 and 7410-2/99 are both on the CGSIM 51/2019 Anexo I low-risk list. Whether São Paulo classifies them the same way is UNVERIFIED.

**One-time fees**

| Item | Cost | Source |
|---|---|---|
| JUCESP contrato social for an ME/EPP | **R$218,99** (an EI would be R$94,90) | Portaria JUCESP 146/2025: *"2.1 … (Empresa enquadrada em ME ou EPP). 5,70 R$ 218,99"*; *"1.1 Inscrição, Alteração (empresa enquadrada em ME ou EPP) 2,47 R$ 94,90"* (https://www.institucional.jucesp.sp.gov.br/downloads/Portaria%20n%C2%BA%20146%20-%20Tabela%20de%20Pre%C3%A7os%202026.pdf) |
| CNPJ, CCM, Simples option, Emissor Nacional | R$0 | CCM being free is standard but UNVERIFIED |
| Accountant's opening service and digital certificate | R$0 | Contabilizei: *"Processo de abertura grátis Certificado digital gratuito"*. Cora: *"ganhe 1 ano de Certificado Digital"* |
| TFE (municipal inspection fee), 2026 | **R$236,35** a year for 0–5 employees, due *"integralmente, ainda que o estabelecimento seja explorado apenas em parte do período"*. MEIs are exempt; an ME is not. | https://prefeitura.sp.gov.br/documents/d/fazenda/tabelavalorestfe2026-pdf |

**One-time total ≈ R$455 ≈ US$88** at PTAX 5,1795.

**Monthly fixed costs**
- **Accountant:** Contabilizei "PADRÃO", *"a partir de R$280 R$ 195 /mês"*, which includes "Contabilidade completa" and "Conta PJ gratuita" (https://www.contabilizei.com.br/quanto-custa-contabilizei/). The cheapest published alternative is Contweb, *"Simples Nacional a partir de R$ 99,99 / mês"* (https://www.contweb.com.br/planos-mensais).
- **Bank: R$0.**
  - Nubank PJ: *"Zero taxas de manutenção … Pix gratuito e ilimitado Você não paga nada nem para receber nem para fazer pagamentos e transferências"* (https://nubank.com.br/conta-pj/).
  - Cora: *"Conta PJ gratuita Sem mensalidades"* (https://www.cora.com.br/).
- **Optional, for C2:** Contabilizei *"Proteção do endereço pessoal e agilidade no CNPJ por R$60/mês"*. Without it, her home address is public on the CNPJ.
- **Total ≈ R$215–360/month (≈US$41–70)** including the TFE averaged over the year.

---

## 6. Pix against a nota fiscal

Pix is a sound rail. Four things to get right:
1. **Receive into the PJ account only.** LC 123 art. 29 VIII excludes a company from Simples if it *"não permitir a identificação da movimentação financeira, inclusive bancária"*.
2. **Issue one NFS-e per payment**, 50% on order and 50% on delivery. From 2027, revenue counts *at invoicing, deposits included* (Res. CGSN 190). That keeps the DAS aligned with the cash.
3. **Business clients withhold nothing.**
   - Lei 10.833 art. 32: *"A retenção de que trata o art. 30 não será exigida na hipótese de pagamentos efetuados a: … III - pessoas jurídicas optantes pelo SIMPLES."*
   - IN RFB 765/2007 (ementa): *"dispensa de retenção do imposto de renda na fonte sobre as importâncias pagas ou creditadas a pessoas jurídicas inscritas no … Simples Nacional"*.
4. **Describe the work as production, never as "planejamento/criação de campanha".** SC 466 keeps Anexo III only *"desde que não preste o serviço de publicidade propriamente dito"*.
   - Suggested wording: *"Produção de filme publicitário (15 s + 2 versões) e de N imagens publicitárias por composição digital (trucagem)"*.

---

## 7. The repaired setup, in one place

| | |
|---|---|
| **Entity** | SLU (sociedade limitada unipessoal) with a denominação, e.g. "O Lançamento Estúdio Ltda", and capital of R$1.000–5.000. The objeto social covers audiovisual and advertising-image production and the licensing of usage rights to the works produced. |
| **CNAEs, in order** | **5911-1/02 (primary), then 7410-2/99.** Drop 7410-2/03, 7420-0/01, 5912-0/99, 7319-0/99 and 7311-4/00. |
| **Regime** | Simples Nacional, switched on at CNPJ registration (MAT). Stay inside the DAS for IBS/CBS; do not choose the hybrid regime. |
| **Pró-labore** | **30% of trailing 12-month revenue**: 28% plus a safety margin, with a monthly check by the accountant. Minimum R$1.621. Do not pay it in months with zero revenue. Review it if a free formal consulta (e-CAC, written) confirms that stills fall under §5-B XV; if they do, cut it to one minimum wage. |
| **Service code** | Emissor Nacional **130301** (NBS 1.1408.12.00 for stills, 1.2501.21.00 for film). São Paulo municipal equivalent 06808 (item 13.02, 2%). |
| **All-in tax at target** | **9,1% at R$12,2–15,0k; 9,3% at R$15,8k** (DAS + 11% INSS; IRPF zero). Rises to **14,2% at R$25k**. |
| **Plus fixed costs** | ≈R$215–360/month, i.e. about 1,4–2,4% of R$15k. **Tax plus compliance ≈ 10,5–11,5% of revenue.** |
| **One-time setup** | ≈R$455 (US$88). |

## Residual risks
- **No ruling covers AI-composited stills.** "Artes visuais" (Anexo III directly) versus "design"/"publicidade" (fator r) is unsettled. Fator r neutralises this at a cost of about 1,9 points.
- **Months with zero revenue.** Per SC COSIT 178/2026, the pró-labore INSS may be charged at 20% in such months.
- **CPP in FS12.** Whether the CPP inside the DAS counts towards payroll is UNVERIFIED.
- **São Paulo licensing.** Whether São Paulo classifies these CNAEs as low-risk for a home address is UNVERIFIED.
- **Hidden-bundle risk.** If a nota bundles an unpriced "campanha" service, SC 145/2023 pulls the whole amount to the worse Anexo.
- **NFS-e field details from 2027.** The exact IBS/CBS fields a Simples company must fill (NT 008/009) are UNVERIFIED. The Emissor Nacional should handle them.
- **Promotional accountant price.** Contabilizei's R$195 is shown against R$280. Budget R$280.
