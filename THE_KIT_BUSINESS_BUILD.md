# THE KIT BUSINESS — BUILD FILE

**12 September 2026. The founder: *"lets see if we can make it air tight… you have a history of Killing
before… its KISS 3–5 sku about 700 buyers we can get a list for to email or call."***

This file is built in the opposite mode to the rest of the archive. Not *what kills it* — **what would have
to be true, and is it.** Three streams ran. Two are back and are recorded here; the private-channel stream is
still out.

---

## ★★★ THE HEADLINE, AND IT REVERSES THE FOUNDER'S OWN FRAME

**She does not need the list of 700 buyers. She does not need to email or call ANY of them to win work.**

`Lei 14.133 art. 54`, verbatim from `planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm`:

> **Art. 54.** A publicidade do edital de licitação será realizada mediante divulgação e manutenção do
> **inteiro teor do ato convocatório e de seus anexos no Portal Nacional de Contratações Públicas (PNCP)**.

Every buyer in this market is **legally compelled to publish its own tender, in full, free, machine-readable,
to one national endpoint, before it buys.** The buyer finds her by publishing; she finds the buyer by polling.
Measured today: **median 10 working days of notice**, floor statutory at 8 (`art. 55 I a`) and 3 for dispensa
(`IN 67/2021 art. 6 par. único`), **98,1% of 105 open tenders give ≥5 business days, 0 give under 3.**

⇒ **THE TENDER DESK HAS NO ORIGINATION PROBLEM.** In an archive where *"not one of seventeen S3 candidates
died on economics — all died on distribution"*, this is the first candidate whose distribution is a statute.

**What the 561-buyer list IS still worth** — and this is the honest, smaller answer to *"can she call the
rest"*:
1. **Pesquisa de preços.** Before a body tenders, it collects quotes to set the `valorUnitarioEstimado`. A
   supplier on that list shapes the ceiling it will later bid under. This is a real, cheap, written lever.
2. **Dispensa direct quotes** below R$65.492,11, where a body may solicit rather than publish widely.
3. **The private layer** (stream 3, still running).
It is **not** how lots are won. Lots are won by bidding on a platform.

⇒ **A LAW: BEFORE BUILDING AN OUTREACH LIST, ASK WHETHER THE BUYER IS COMPELLED TO ANNOUNCE ITSELF.**
Where a statute forces publication, the list is a nice-to-have and the CRON is the business. This is the
mirror image of `THE POSTAL LIST LAW` — there, enumerable ≠ contactable; here, contactable is irrelevant
because the buyer contacts *her*.

---

## 1. THE SCOUTING RAIL — free, complete, and it is PNCP

**No paid alert service is needed.** The complete daily loop, every call of which was fetched
unauthenticated over plain HTTPS today:

```
Daily 07:00 cron:
1. GET pncp.gov.br/api/consulta/v1/contratacoes/proposta
        ?dataFinal=<today+60>&codigoModalidadeContratacao={6,8,4,12}&pagina=N
   → ~5.030 records/day nationwide, ~100 pages of 50   (tamanhoPagina=500 → HTTP 400; 50 works)
2. Keyword-filter objetoCompra                              → catches only 28%  ⚠ see §1(c)
3. For each remaining municipal record:
   GET pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}/itens
   → descricao (full spec), quantidade, valorUnitarioEstimado,
     criterioJulgamentoNome (por item vs global), tipoBeneficioNome (ME/EPP)
4. On a hit: GET .../arquivos → edital PDF → parse the TR
5. Route by linkSistemaOrigem (present on 74/105 = 70,5%) or grep the platform name from the edital
```

**Cost: R$0,00 in licence fees, ≈R$25/month of VPS.** Two minutes of compute a day.

**(a) The PNCP Consulta API exposes 12 GET paths and NO subscription, webhook or notification endpoint**
(`pncp.gov.br/api/consulta/v3/api-docs`). It is a polling rail by design. Two paths are purpose-built for
exactly this: `/v1/contratacoes/proposta` ("Consultar Contratações com Recebimento de Propostas Aberto") and
`/v1/contratacoes/publicacao`.

**(b) `dataEncerramentoProposta` is present on 105/105 (100%).** Worked example, Campina Verde/MG, fetched
today: published 10 Sep 15:04, closes 22 Sep 09:00, `linkSistemaOrigem =
https://licitanet.com.br/sessao/201038`, `valorTotalEstimado = 31836.68`.

**(c) ⚠ THE ONE REAL DESIGN CONSTRAINT — THE OBJECT TITLE IS NOT ENOUGH.** Only **29 of 105 (28%)** of open
kit-relevant tenders carry a kit keyword in `objetoCompra`. The rest hide kit lines inside generically-titled
purchases — Pirapó/RS *"materiais de expediente e artesanato para uso no CRAS"*, Matupá/MT *"aviamentos,
artigos para decoração, tecidos, confecção"*. **The cron must descend to the item list, not stop at the
object.** One extra `/itens` call per open tender per day. **That is the difference between seeing a quarter
of the market and seeing all of it — and it is exactly the labour the paid services sell.**

**(d) The lag, measured on the 29 kit-specific open tenders:**

| | business days | calendar days |
|---|---|---|
| min | 4 | 5,6 |
| p25 | 9 | 13,0 |
| **median** | **10** | **13,9** |
| p75 | 12 | 17,9 |

**27 of 29 (93%) give ≥8 working days.** Both sub-8 cases are explained, not exceptions: União do Sul/MT is a
*dispensa* (floor 3 days); Petrolândia/PE published on PNCP five days **after** its own proposal opening — a
municipal compliance defect.

**The commercial fallback, if a second pair of eyes is wanted for six months: Alerta Licitação R$369,90/year**
(R$44,90/month, 6.441 sources, 2 e-mails a day, `alertalicitacao.com.br`). **SIGA Pregão R$397/month;
ConLicitação and Effecti publish NO PRICE AT ALL** — `THE MONITORING PINCER` in reais, to the decimal.

---

## 2. WHAT IT COSTS TO BE ABLE TO BID — **R$0,00 up front**

The municipal market fragments across ~32 publishing systems and ~17 bidding platforms, **and it concentrates
fast.** All 105 open kit tenders, routed by `linkSistemaOrigem` or by grepping the edital PDF:

| Platform | n | share | cumulative | registration | per bid |
|---|---|---|---|---|---|
| **Portal de Compras Públicas** | 27 | 25,7% | 25,7% | **R$0** | R$129 crédito · R$165/mês · R$1.650/ano |
| *Município's own local system* | 18 | 17,1% | 42,9% | free, one-off | — |
| **Compras.gov.br (SICAF)** | 18 | 17,1% | 60,0% | **R$0** | **none** |
| **BLL** | 12 | 11,4% | 71,4% | **R$0** | **1,5% of the lot, capped R$600 — ONLY IF SHE WINS** |
| **Licitanet** | 11 | 10,5% | 81,9% | **R$0** | R$107 avulso · R$827/ano |
| **BNC** | 10 | 9,5% | 91,4% | **R$0** | R$118,80 per bid, POST-PAID, win or lose |
| Banrisul · Licitar Digital · BBMNET | 9 | 8,6% | 100% | free | UNVERIFIED |

**Five free registrations = 74,3% of the market. Eight = 82,9%.**
**Weighted variable cost ≈ R$75 per bid.** BLL is free unless she wins; Compras.gov.br is free always.
**Above ~13 bids/year on one platform, switch that platform to annual.** Unlimited on the three that charge =
R$4.997/year; at a realistic 30–60 bids/year across five, **pay-as-you-go is cheaper and is the right
default.**

**Primary sources.** BLL Regulamento 2026 art. 17 II, `bll.org.br/wp-content/uploads/2026/07/Regulamento-BLL-2026.pdf`:
*"**Apenas o licitante vencedor será responsável pelo pagamento da taxa de sucesso.** A cobrança será de 1,5%…
**limitada ao teto máximo de R$600,00**."* BNC Regulamento 2026, Termo de Adesão item 7: *"O boleto para
pagamento é liberado logo após a fase de disputa… **A não participação efetiva no edital não anula a
cobrança**."*

**And there is NO per-município registration burden.** Three statutory props:

> **Art. 63 II** — será exigida a apresentação dos documentos de habilitação **apenas pelo licitante vencedor**
> **Art. 87 §2º** — **É proibida a exigência… de registro cadastral complementar para acesso a edital e anexos**
> **Art. 70 II** — a documentação poderá ser substituída por registro cadastral emitido por órgão público

Confirmed on the supplier side by a real edital (Alvorada do Sul/PR, downloaded from PNCP today): *"A chave de
identificação e a senha dos operadores **poderão ser utilizadas em qualquer pregão eletrônico**."*

⚠ **PCP justifies its supplier fee as *"prevista em lei (Art. 62 da Lei 14.133/21)"*. Art. 62 is the
habilitação article and says nothing about platform fees.** Not a blocker; a tell about the counterparty.

---

## 3. THE SUPPLY SIDE — the margin is real and the bid filter IS the margin

**843 homologated award rows from 230 PNCP editais, against wholesale prices fetched from suppliers that
publish them** (Yanai Atacado/Brás — full catalogue via `/products.json`, 389 SKUs, no published MOQ;
Atacado Fortsul — R$600 minimum, published; Atacadão da Roupa, Santa Cruz do Capibaribe/PE — factory region,
5% cash discount. Login-gated: Yora R$800, Brascol, Emilio, Martins.)

| SKU | wholesale | median award | margin | **observed award FLOOR** |
|---|---|---|---|---|
| Body | R$5,64 | R$12,66 | **55%** | R$5,14 → **−10%** |
| Fralda pack | R$8,32 | R$17,10 | **51%** | R$7,00 → **−19%** |
| **Lençol berço** | **R$26,03** | **R$29,50** | **12%** | — **wholesale sits ABOVE award p25** |
| Toalha capuz | R$15,36 | R$19,03 | 19% | — |
| Kit higiene | R$5,78 | R$12,00 | **52%** | — |
| Banheira | R$17,89 | R$28,00 | 36% | — |

**Three real lots, priced end to end:**

| Lot | award | net after tax |
|---|---|---|
| Itapetininga/SP — R$161,80 × 225 | | **+21,6%** |
| Feira de Santana/BA — R$178 × 340 | | **+30,8%** |
| Saloá/PE — R$210 × 280, **18 items** | | **−3,1% — DEAD** |

⇒ **Blended 18–27% net on winnable lots. Every SKU is loss-making at the observed floor, and two of those
floors were set by confecções bidding direct.** **THE BID-SELECTION FILTER IS THE MARGIN.** There is no
pricing skill that rescues a lot she should not have entered.

**★ THE ASSEMBLER PROBLEM DISSOLVES, AND IT DISSOLVES BY READING THE TENDER TYPE.** No Brazilian co-packer
publishes prices (Support Pack, Tempos, Cotlog — all quote-only). **She does not need one.** On
*menor preço **POR ITEM*** lots, **nobody assembles a kit** — the município buys the components and the CRAS
staff assemble them. She drop-ships packs. The assembly margin she was worried about losing **does not exist
on those lots and neither does the assembly cost.** *(This is `THE TR IS THE PRODUCT` one level down — and it
is the second time in two days that reading the tender type, not the object, changed the answer.)*

**MOQ is NOT a kill.** Published minimums are **R$600–800** against a **median dispensa lot of R$58.475** —
**1,0–1,4%.** The inventory veto does not fire.

**★ CERTIFICATION IS NOT THE GATE — AND THE REAL GATE IS THE ATESTADO.** Checked at Inmetro:
- Textiles need **labelling** (Portaria 118/2021), **not certification**.
- **Rigid baths are NOT certified** — Portaria 563/2016 covers inflatable baths only.
- **Mamadeiras and chupetas ARE certified** (Portaria 490/2014) ⇒ **keep them out of the 3–5 SKU set.**

The actual entry barrier is the **ATESTADO DE CAPACIDADE TÉCNICA**. **TCE-SP Súmula 24** permits an edital to
demand 50–60% of the tendered quantity as prior delivered experience. **A first-time supplier is excluded
from any lot carrying one, by construction.** ⇒ **THE PARSER'S FIRST FILTER IS NOT PRICE, IT IS THE ATESTADO
CLAUSE.**

**Competition, measured: 223 distinct winners, 212 of them (95%) win in ONE UF only.** Most are generalist
tender desks, not baby-goods firms. **One-person operators are already winning these lots** — the same shape
the dispensa oracle found in thermal media.

**Unbudgeted cost line found: substituição tributária** on interstate purchases into a Simples ME. Yanai
warns of it on its own product pages. **Ask it in the supplier cadastro.**

**Freight: structure verified (Correios 30 kg cash limit, 50 kg with contract), price UNVERIFIED** — the
Correios calculator errors and Melhor Envio needs auth. Kit weight ≈0,93 kg clothing-only.

---

## 4. ★ THE CONSORTIUM CHANNEL — real, enormous, lumpy, and it must be bid by the LINE

**≥221 distinct intermunicipal consortia publish on PNCP** (a floor — counted from the first 1.000 of 35.729
matching records). **183 of 221 (83%) are in MG/PR/SP/SC/RS**, all freightable from São Paulo:
MG 78 · PR 34 · SP 30 · SC 22 · RS 19.

| Consortium | UF | What | Value |
|---|---|---|---|
| **CIMINAS** | MG | *"KITS PARA RECEM NASCIDOS E BOLSAS MATERNIDADE"* — **OPEN, closes 23 Sep 09:00**, Licitanet | **R$4.509.371,94 — 5.613 kits, ONE lot, "Sem benefício"** |
| **CISARP** | MG | *"KIT DE ENXOVAL PARA PRÉ NATAL E PUÉRPERAS"*, Apr 2026 | **R$8.703.955,50 across 38 SEPARATE LINES** |
| **CISAJE** | MG | *"KIT NATALINO"* — Feb 2025 **and** Nov 2025 | annual |
| **Macro Sul de Minas** | MG | *"itens de enxoval"* — Mar 2024 **and** Feb 2026 | recurring |
| **Cons. Interm. de Saúde** | PR | *"enxoval hospitalar"* — 2024, ×2 2025, 2026 | recurring |
| **CIM NOROESTE** | ES | *"kits natalidade… demanda dos municípios consorciados"* | — |

**The leverage: CIMINAS publishes 103 member municípios** (counted from its own list,
`ciminas.mg.gov.br/institucional/municipios`). **One ARP, 103 buyers, one bid.** And it compounds:

> **Art. 86 §5** — o quantitativo decorrente das adesões **não poderá exceder… ao dobro do quantitativo de cada
> item registrado**

⇒ a won consortium ARP reaches **3× its registered quantity** without a second bid.

**⚠ And the honest half.** Consortia are **2,1% of kit editais by count (13 of 626 in 2026)** — few, large,
lumpy, not a stream. **CIMINAS's R$4,5M is ONE undivided lot with no ME/EPP reservation — a factory lot,
unwinnable on R$15.600 of working capital.** **CISARP is the shape that lets her in: 38 separate lines, menor
preço per item, individual lines R$32.155–79.540. She bids three lines, not the kit.**
**And a live ARP locks its whole region until it expires — read the ARPs before building a per-município
cron.** They are all on PNCP, free.

**★ A FREE STATUTORY LEVER, found in the data.** **LC 123 art. 48 I** reserves items **up to R$80.000**
*exclusively* to ME/EPP — **per ITEM, not per tender.** CISARP's April 2026 ARP has **9 of 38 lines at or
below R$80.000** (touca R$66.590, escova/pente R$79.540, escova de dentes R$62.031) and **all 38 are flagged
`Sem benefício` on PNCP.** An impugnação is written, free, statutory, and needs no lawyer.
⇒ **BUILD THE R$80.000-PER-LINE CHECK INTO THE PARSER.**

---

## 5. WHAT IS STILL NOT SOLVED

**Scouting is solved and free. Registration is solved and free. Supply is solved and the margin is real.**
What binds is what `THE_ACOLHE_ASSESSMENT.md` already said and this stream confirms from a second direction:

**Working capital and lot size.** The lots open to a R$15.600 operator are the **R$30–150k per-item lines**,
not the R$4,5M kit lots, and those lines are won at menor preço against clothing wholesalers who buy better
than she does. `THE_WORKING_CAPITAL_ANSWER.md` names the instrument (**FGI PEAC** — no history requirement,
minimum R$1.000, 48 agents) and the free lever (**buyer selection: 15 vs 67 days to payment across 2.276
measured invoices**, worth ~3× capacity).

---

## THE NEXT TEST — costs nothing, needs no phone, ~1 day

**29 live tenders with deadlines 14–24 Sep are already pulled.** Pull every item list, price three wholesale
RFQs against them, **and count how many she would have won at ≥15% contribution.** Bar committed in advance:
**≥6 of 40 shadow-bids at ≥18% net.** Twenty real instances, a numeric bar, no conversation — the test design
this repo says works.

**Two parser filters to build first, both derived above:**
1. **Reject any edital carrying an atestado de capacidade técnica clause** (TCE-SP Súmula 24 — she cannot
   clear it, ever, until she has delivered).
2. **Reject "kit completo" lots over ~14 items** (Saloá/PE, 18 items, −3,1%).

And three written asks, none of them a sales call:
3. One sample kit under R$200 from Yanai, to hold the actual goods.
4. Cadastro at three suppliers, asking **the credit-terms question AND the substituição tributária question**.
5. One RFQ to three co-packers — to price the option, not to need it.

---

*Sources: all URLs above fetched 12 Sep 2026 unauthenticated. Reproducible from
`scratchpad/kits/push/` and `scratchpad/kits/buyers/`.
Stream 3 — the private maternity channel and CNES contacts — was still running when this was written.*

---

# STREAM 3 — THE PRIVATE LAYER, AND WHAT VERIFYING IT TURNED UP INSTEAD

*(12 Sep 2026. The founder: "what about private hospitals, and are all of those 1.100 maternity and delivery
for new babies?")*

## 6. THE ANSWER ON PRIVATE HOSPITALS: **NO — AND IT IS SETTLED, NOT MERELY UNFOUND**

**Brazilian private maternities do not buy newborn kits. They publish a list of what the mother must BRING.**
Three of the country's leading private maternities, in their own words:

> *"Enxoval do bebê: Macacão: 6 peças · Body: 6 peças · Calça com pé: 6 peças · Manta ou cobertor: 2 peças ·
> Luva: 2 pares · Meia: 2 pares"* — Hospital e Maternidade Santa Maria (Grupo Santa Joana), page titled
> **"Lista de enxoval"**, `maternidadesantamaria.com.br/guia-de-internacao/lista-de-enxoval/`

> *"o HNSG relacionou os itens necessários para o enxoval do bebê e da mamãe na ida à maternidade… **Monte
> kits para cada dia**"* — Hospital Nossa Senhora das Graças, `hnsg.org.br/internacao/lista-de-enxoval/`

> *"Também oferecemos algumas cortesias para você. Veja quais são: Curso para Gestante Online…; Teste do
> pezinho ampliado…; **Pacote de Estacionamento** – até 72 horas…; **Wifi**."* — Pro Matre Paulista's own
> **Plano Maternidade** (the paid birth package), `promatre.com.br/plano-maternidade/`

**And the structural tell: the hospital's answer to the enxoval need is a RETAIL SHOP, not a gift** — *Pro
Matre Baby*, inside the hospital, selling pelúcias, mordedores, sapatinhos, mantas. Five independent searches
for a private-hospital courtesy kit returned only **public** programmes (Mãe Paulistana, Cegonha Carioca,
Nascer Bem Paraná). Rede D'Or's maternity page greps **zero** hits on `kit|cortesia|enxoval|presente|brinde`.

**The list itself is real and good — it is just the wrong buyer.** Measured properly from CNES:
**4.414 active establishments with a centro obstétrico**, of which **2.099 (47,6%) are private**:
**70,5% publish an email, 91,2% a phone.** *(File written: `maternidades_privadas_cnes.csv`.)*
⚠ Three caveats from reading the rows rather than counting them: the CNES address is the **licensing**
contact, not purchasing (`licenciamentosp@rededor.com.br`, `societario@…`, one hospital's accountant at a
gmail address); **chains collapse the buyer count** (Hapvida 30 + Rede D'Or 21 + Intermédica 9 ≈ two
purchasing centres); and the filter is *has a centro obstétrico* — units with obstetric beds but no obstetric
centre are UNVERIFIED, because the API exposes no leitos endpoint.

**★ A REUSABLE TRAP, worth more than the list: paging CNES nationally WITHOUT `codigo_uf` SILENTLY DRIFTS.**
A flat run returned 4.414 rows containing only **3.051 distinct** CNES codes — 932 duplicated, one six times,
identical payloads at different offsets — i.e. it **skipped ~31% of the population while appearing complete**.
Sharding by UF returned 4.414 distinct codes, and the flat run's set is a strict subset. **Always shard CNES
paging by UF and dedupe on `codigo_cnes`.** *(And `/assistencia-a-saude/hospitais-e-leitos`, whose own summary
claims it returns "endereço, telefone e e-mail", returns neither in the actual row —
`A COUNT OF STRUCTURES IS NOT A CHECK OF CONTENT`, fired by the publisher's own docs.)*

## 7. ★★ THE GIFT OBLIGATION IS DISCHARGED BY MONEY

The employer channel is occupied and its own trade press ranks a **prepaid card as idea #1**:

> *"**1. Pay X: a opção mais completa, prática e personalizável** … oferecer um **cartão pré-pago** como parte
> do kit maternidade é uma forma inteligente de dar liberdade real… Para o RH… é possível acompanhar todos os
> envios, controlar orçamentos"* — Incentive, `incentive.com.br/kit-maternidade-corporativo-6-ideias…`

And the **same collective-agreement clause** is discharged two ways by two administrators — **a R$450 cesta**
(Central dos Benefícios) or **a R$600 gift card** (Bem Mais Benefícios / Icatu Seguros, SUSEP
15414.001273/2006-81): *"cartão presente no valor de R$600,00 que poderá ser utilizado em qualquer
estabelecimento."*

⇒ **A kit competes not with other kits but with money — zero MOQ, zero freight, zero SKU risk, and a manager
dashboard.** `THE TEMPLATE FLOOR TEST` in a benefits costume.

**★ THE ONE GENUINE RULE FOUND ON THE PRIVATE SIDE — and it dies on size.** *Kit natalidade* is a
**collective-bargaining obligation with the BOM written into the CCT**, carried identically by FENATIBREF
(national), SINTIBREF-MG, SINTIBREF-ES, SEIBREF-SP, SECOHTUH-ES and SINBRAF/RS — a 24-item table, declared
value **R$450**, and the duty sits on the employer: *"as empresas são obrigadas a contratar um seguro de vida,
no qual está embutida a entrega de uma Cesta Natalidade… composta por **16 itens pré-estabelecidos na
Convenção Coletiva**"* (SECHSAR). **Exogenous clock, non-stretchable unit, BOM written by someone else, no
relationship to hold — it passes limbs 1 and 2 of `THE MACHINE TEST` cleanly.** And then the administrator
publishes its own annual volume in its page title: **"Central dos Benefícios entrega 1.176 kits natalidade em
2024."** *(Title and slug are the publisher's own — PRIMARY; the article body is UNVERIFIED, Cloudflare 403.)*

**The private arithmetic, honestly:** the two visible private sub-channels together deliver **~3.356 kits/year**
(Bird's own published *"+2.180 Kits Bebê corporativos atendidos só em 2025"* plus Central's 1.176). At a R$400
ticket and 30% gross she needs ~1.440 kits/year ⇒ **~43% of the entire visible private B2B kit market**,
against `THE MARKET-MULTIPLE RULE`'s 15–25%. **It fails by about 2×.**

⇒ **THE PRIVATE LAYER IS A MARGIN LAYER, NOT A VOLUME LAYER.** Worth R$100–300k/year of high-margin,
fast-paying revenue *on top of* a public desk — which is precisely the working capital the public leg is short
of — and it cannot be an engine. **The founder's sequencing (public first, private second) was right; only the
sizing needed resetting.** ⚠ And private *hospitals* are **slower** to onboard than a município: Sírio-Libanês
requires **SAP Ariba homologação** plus contrato social, procuração, cartão CNPJ, FGTS, CNDs and alvará;
Hapvida runs **Coupa** and holds you in a database *"a ser pesquisado conforme necessidade."* The private
channel's speed advantage lives entirely in the gifting firms and benefits administrators — a quote and a PO,
no homologação at all.

## 8. ★★★ WHAT VERIFYING THE LEAD ACTUALLY FOUND — THE STATE TIER, AND IT IS ON THE SAME RAIL

The stream ended by pointing at a state programme (*Nascer Bem Paraná*, ~R$625/kit × 16.000 kits, SECONDARY).
**I ran the check myself — 8 keyword sweeps × 6 pages of PNCP, 1.538 distinct editais, 713 with a kit keyword
in the object — and the result corrects the lead in both directions.**

**Paraná is NOT on PNCP.** Zero hits under any of eight terms. Its headline number stays **UNVERIFIED**, and
more importantly **the cron cannot see that programme at all.**

**But four other states are, and they are the largest kit tenders in the entire dataset:**

| State | Object | Estimated | Homologated | Shape |
|---|---|---|---|---|
| **SE** | *itens de enxoval de bebê… PROGRAMA…* | **R$6.005.600** | **R$2.228.150** | SRP, **per-item** — bolsa 5.000 @R$220, toalha 5.000 @R$40, sabonete 5.000 @R$20,89 |
| **PB** | *kits de enxoval para recém-nascidos* | R$1.031.016 | R$700.272 | ⚠ **ONE undivided lot at R$979.465, "Sem benefício"** — a factory lot |
| **RO** | *montagem de kit maternidade, enxoval e higiene* | R$843.870 | R$357.660 | per-item, and **explicitly reserved**: *"Participação exclusiva para ME/EPP"* on toalha (3.000 @R$20,20) and camiseta (3.000 @R$13,77); *"Cota reservada para ME/EPP"* on vestimenta and bolsa |
| **RJ** | *Kits de Enxoval personalizado para Puérperas* | not published | — | **80.000 units per component line** — the largest volume seen anywhere |

**Three things this changes:**
1. **The state tier is 15 of 713 core editais (2,1%) — the same shape as consortia: few, enormous, lumpy.**
   It is not a stream and must not be modelled as one.
2. **It is reachable by the cron already built.** Same PNCP endpoint, same five free registrations *(plus one:
   RJ runs `compras.rj.gov.br`, its own portal)*. **No new capability.**
3. **★ AND THE HAIRCUT IS WORSE AT STATE LEVEL THAN MUNICIPAL: homologated ÷ estimated = SE 37% · RO 42% ·
   PB 68%**, against ACOLHE's measured municipal median of 79%. **Price against the state's homologated award,
   never its estimate — `THE REFERENCE-PRICE ILLUSION` fires harder the bigger the lot.**

⇒ **The board does not change. The kit desk's engine is municipal + consortium per-item lines; the state tier
is four to five lottery tickets a year, two of which carry ME/EPP reservations she qualifies for; the private
layer is margin on top. And the private hospital list, though excellent, is not a buyer list for this.**
