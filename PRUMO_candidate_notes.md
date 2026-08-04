# PRUMO — candidate #5, with the census done first

**Status: CANDIDATE, not a decision.** Written the night LÍQUIDO was killed.
Every number below that comes from official data is marked VERIFIED with its
source. Everything else is marked ESTIMATED or UNVERIFIED and must stay that way
until someone says it out loud on a phone call.

---

## 1. Why LÍQUIDO died, and what it changed

Pora ships the exact LÍQUIDO product today: contracts in bulk, automated nota
fiscal collection from creators, Pix batch payment, plus antecipação — the one
feature the blueprint refused to build. Their homepage claims **+2000
influenciadores já foram pagos**. They serve **"marcas e agências"** with
white-label branding for agencies — the precise buyer LÍQUIDO's go-to-market was
designed around.

The LÍQUIDO document listed "monitor Pora's customer count" as the leading
indicator for Death #4. That indicator had already fired before the document was
finished. The failure was not bad luck; it was **sequencing**. The process
checked "is the pain real" and "is the gate real" hard, and checked "has someone
already built this" last and lightly.

**Permanent change: the competitor check runs FIRST. A candidate does not get a
business model written for it until it survives that check.**

---

## 2. The graveyard from one night of applying that rule

| Candidate | Verdict | Killed by |
|---|---|---|
| Freight audit (CT-e vs tabela) | DEAD | 14+ incumbents: Fretefy, Intelipost, DATAFRETE, Gestão do Frete, Eccosys, Senior, Benner, Frete Rápido, Everlog, SANCON |
| Repasse médico | DEAD | ContSelf ("pioneira no mercado brasileiro") + Quark Clinic, MRB, AppHealth, iClinic — LÍQUIDO's mechanism, already shipped |
| Model-agency cachê | DEAD | Structural: the payer is the agency and the delay is *their float*. Cannot sell a fix to the party profiting from the problem |
| Marketplace repasse reconciliation | DEAD | Koncili, Marketize, MakeValue, GoSmarter, Joompulse, Anymarket — and adjacent to where VOLTA already died |
| Multimarca / atacado settlement | DEAD | ViaShopModa, brands.HUB, Convertr, Gestão Pedidos, Mercos |
| OOH media checking | DEAD | IVC is the ABOOH-endorsed official auditor; OOH Brasil shipped an AI planning platform |
| Trade marketing / PDV proof | DEAD | Checkmob, Sovis, Trade Marketing Force, MáximaTech, Tracking Trade, GMPromo |
| **BAIXA** (event verba) — *my own prior recommendation* | **DOWNGRADED** | I called the field clean. It is not: Linkana, Monkey, Pipefy, Nibo, Pagô, Cora, Flash occupy the corridor. No exact match, but not the open field I described |

### Two structural findings, which matter more than any single kill

**Finding 1 — the "repasse + nota fiscal gate" shape is farmed out in Brazil.**
ContSelf owns doctor repasse. Pora owns creator repasse. Superlógica owns
imobiliária repasse. isaac owns school repasse. Mercos owns rep commissions.
LÍQUIDO was the fourth draw from an exhausted deck. **Stop hunting the last
unoccupied vertical of that shape.**

**Finding 2 — reconciliation SaaS in Brazil is mature across the board.** Every
niche where two documents can be cross-checked for money already has funded
players. A solo founder with no capital arriving late to any of them loses on
principle, not on execution.

**Therefore:** the remaining opening is where **the incumbent is a human
consultancy, not a funded startup.**

---

## 3. PRUMO — what it is

Brazilian cultural projects funded through Lei Rouanet must document every
centavo spent against an approved planilha orçamentária, and submit a Relatório
de Execução Financeira through SALIC. Producers running several projects at once
do this in spreadsheets and folders of PDFs.

**PRUMO is the ledger that keeps every funded project's documentation
reconciled against its approved budget in real time** — so the prestação de
contas is a button, not a three-week archaeology dig, and no diligência ever
expires unanswered.

The name means documentary backing — *o lastro do projeto*.

### Why the incumbent check passes

Repeated targeted searches for proponente-side prestação de contas software
returned **consultancies and courses, not products**: Squadra, Cultura e
Mercado, Elaborando Projetos, IDEA, Maxximu, Agência NTZ, Proyatê, Direção
Cultura, Olivieri, Dolabella, SESC. Prosas is funder-side (publishing editais,
receiving proposals). Evoé is crowdfunding. Placarsoft and Fase.pro serve the
municipal Lei Paulo Gustavo side. One search summary said it plainly: *"Os
resultados não mencionam especificamente softwares de prestação de contas."*

This is the first candidate in five where the field is occupied by **hourly
humans**, whose price this founder can undercut while keeping a software margin.

---

## 4. The census — measured, not estimated

**This is the part that did not exist for LÍQUIDO.** Its fatal unknown — how
many buyers clear the volume floor — was flagged "no verified census exists" and
left open for weeks. Here it is a public API call, and it has now been made.

Source: **SALIC open data API**, `https://api.salic.cultura.gov.br/api/v1/projetos`,
all projects with `ano_projeto` 23–26. **45.863 project records pulled.**

| Measure | Value |
|---|---|
| Projects 2023–26 | 45.863 |
| Projects that actually raised money (`captado > 0`) | **10.945 (23,9%)** |
| Total captado, those projects | **R$ 8.448.892.045** |
| Funded and not archived/dead | 9.663 |
| Distinct proponentes with funded live projects | 5.690 (PJ 4.981 / PF 709) |

### Addressable buyers — PJ by concurrent funded live projects

| Concurrent funded projects | Proponentes | Their combined captado |
|---|---|---|
| ≥ 2 | 1.939 | R$ 6,18 bi |
| ≥ 3 | **933** | R$ 4,06 bi |
| ≥ 4 | **448** | R$ 2,64 bi |
| ≥ 5 | 246 | R$ 1,52 bi |
| ≥ 6 | 140 | R$ 990 mi |
| ≥ 8 | 38 | R$ 338 mi |
| ≥ 10 | 18 | R$ 138 mi |

Among the 933 with ≥3: **median captado R$ 2,06 milhões**, p75 R$ 4,63 mi,
p90 R$ 9,12 mi.

### Geography — and it favours her

Of the 933, **SP is the largest cluster with 293**, then RS 139, RJ 111, MG 105,
PR 79, SC 76.

**São Paulo alone holds 145 PJ proponentes running ≥4 funded projects
concurrently, with R$ 1,067 bilhões captado between them.**

**The business needs 12 customers. Her home city has 145 qualifying buyers.**
That is 8,3% penetration of one city's segment — and the names and CNPJs are
already extracted, not hypothetical.

### Named qualifying buyers (top of the list, by concurrent funded projects)

| Projects | Captado | UF | Proponente |
|---|---|---|---|
| 21 | R$ 14,8 mi | RS | MARCA PRODUCOES ARTISTICAS LTDA |
| 12 | R$ 34,5 mi | MG | ASSOCIACAO PRO-CULTURA E PROMOCAO DAS ARTES |
| 11 | R$ 12,0 mi | SP | INSTITUTO ACERTE - ARTE CULTURA E EDUCACAO |
| 11 | R$ 8,1 mi | SP | FBF CULTURAL LTDA |
| 10 | R$ 16,5 mi | MG | UNIVERSO PRODUCAO LTDA |
| 9 | R$ 55,9 mi | SP | INSTITUTO PEDRA |
| 8 | R$ 36,5 mi | SP | MANA PRODUCOES COMUNICACAO E EVENTOS LTDA |
| 8 | R$ 20,1 mi | PR | SINAPSE PRODUCOES CULTURAIS E TEATRAIS LTDA |
| 9 | R$ 6,8 mi | SP | EDUCARE PRODUCOES LTDA |
| 10 | R$ 5,8 mi | SP | INSTITUTO EVOLUIR CULTURAL |

---

## 5. The regulatory facts — VERIFIED against the primary text

From **Instrução Normativa MinC nº 29, de 29 de janeiro de 2026** (in force;
product of a public consultation with 521 contributions across 13 cities):

- **Art. 10 — carteira caps.** Pessoa física: até 2 projetos ativos, R$ 500.000.
  MEI: até 4, R$ 1.500.000. **Demais pessoas jurídicas: até 10 projetos ativos,
  R$ 15.000.000.** (Cut from 16 under the previous IN.)
- **Art. 11** — per-project approval caps: PF R$ 500.000, PJ R$ 1.500.000
  (exceptions to R$ 6 mi).
- **Art. 13, parágrafo único — the verified gate**, verbatim:
  > "As propostas de ações continuadas poderão superar o limite do valor da
  > carteira quando da apresentação de nova edição, **condicionando a
  > homologação da execução ao envio da prestação de contas da edição
  > anterior**."
- **Art. 65 § 2** — a diligência must be answered **within 20 days**.
- **Art. 66 § 3** — accepting medidas compensatórias can prevent automatic
  application of the inabilitação sanction.
- **Sanction**: reproved contas → **3 years of inabilitação**, applied to the
  proponente **and its gestores**, CNPJ flagged in SALIC as the public
  regularity check for all Pronac access; extendable to jointly responsible
  parties **including incentivadores and fornecedores** where fault is proven.
- **SGPTC** analyses a submitted prestação de contas within **6 months**.
- An accountant registered with the CRC is **already mandatory** on every
  project, and the legal representative signs and submits.

### CORRECTION I have to make against my own earlier claim

Earlier tonight I asserted that *any* unfinished prestação de contas occupies a
carteira slot, which would have made this a pure capacity sale. **The primary IN
29/2026 text does not define when a project stops occupying a slot.** That claim
came from an article about the superseded IN 23/25 and I could not confirm it.

What survives verification is narrower: the gate binds **ações continuadas** —
festivals, biennials, orchestra seasons, recurring programmes. That is a real,
verbatim, primary-source gate, and it happens to bind exactly the institutional
repeat proponentes who are the only ones clearing the ARPU floor. But it is
narrower than "your portfolio is clogged," and the pitch must not overstate it.

---

## 6. The honest weakness — do not sell fear

The catastrophic sanction is real and terrifying. **It is also rare.** Across all
45.863 projects:

| Signal | Count |
|---|---|
| Submitted prestação de contas, awaiting analysis | **3.611** |
| Archived for not answering a diligência | 262 |
| Suspended | 163 |
| Inadimplente | 107 |
| Prestação de contas **desaprovada** | **84** |
| Currently under diligência | 83 |

84 reprovações out of 45.863 projects is **0,18%**. Selling "avoid the 3-year
ban" is selling insurance against a 1-in-550 event — and that is precisely the
failure mode that killed Janela and Aval: *protection against losses Brazil does
not actually impose.*

**The honest sale is throughput, not fear.** 10.945 funded projects across
2023–26 must each be documented line-by-line, and 933 organisations are doing
three or more concurrently in spreadsheets. The deadline is real, the work is
universal, and the tail risk is a bonus argument — never the headline.

---

## 7. Price and the arithmetic

Anchor, VERIFIED: accounting/consulting on a cultural project customarily runs
**2–5% of total project value**, and **can be paid from the incentivized funds
themselves** when it sits in the approved planilha orçamentária with nota fiscal
and contract, booked under "Serviços de Terceiros." On a R$ 1,5 mi project that
is **R$ 30.000–75.000 of pre-approved budget.** The buyer is not spending their
own money — the strongest "frictionless yes" of any candidate so far.

Flat monthly by carteira size. No percentage.

| Faixa | Projetos financiados ativos | Preço/mês |
|---|---|---|
| Produtora | 1–3 | R$ 1.900 |
| Carteira | 4–6 | R$ 4.900 |
| Carteira cheia | 7–10 | R$ 8.900 |
| Instituição | 10+ / ações continuadas / >R$ 5 mi | R$ 14.900 |

**To R$ 40.000/month net:** ~12 customers averaging the Carteira band
(R$ 4.900) = **R$ 58.800 MRR**. Against LÍQUIDO's validated cost structure
(opex ~R$ 12.500, Simples Anexo III via Fator R, pró-labore R$ 19.900) this lands
around **R$ 36–38k net — slightly under the floor.** Reaching R$ 40k+ needs
either **14 customers** at that mix, or a mix weighted toward Carteira cheia.
Stated plainly rather than fudged: **the floor here is 14 customers, not 12.**

Available pool at ≥4 projects: **448 nationally, 145 in São Paulo.**

---

## 8. Day-one product (v0)

Three tables: `projetos`, `itens_orcamento`, `comprovantes`.
Five states per budget line: `previsto → contratado → nf_recebida → pago → comprovado`.

Six things it does:

1. Import the approved planilha orçamentária → it becomes the ledger of record
2. Attach to each line: nota fiscal, comprovante de pagamento, contrato
3. Validate each document against its line — CNPJ, valor, rubrica, date inside vigência
4. Flag divergences **before** submission (wrong rubrica, over-budget line, date outside window, missing doc)
5. **Diligência watchdog** — a 20-day countdown per open diligência with alerts. 262 projects were archived for missing exactly this
6. Generate the Relatório de Execução Financeira and the document dossier

**Magic moment:** upload the planilha, drag in the folder of notas, and see
instantly which lines are green, which are short, and which will get you
diligenciado.

No payment rail. This is a gate plus a calculation of record; it never needs to
move money — which makes it **simpler than LÍQUIDO**, with no Asaas dependency,
no BCB exposure, no custody question. Next.js + Supabase + file storage.
**~4 weeks to v0.**

Positioning on liability: the CRC accountant is already mandatory and already
signs. PRUMO feeds the contador — it never replaces the signature. That
resolves the "who is to blame" objection structurally.

---

## 9. The 10-day test — before anything is built

Five conversations with proponentes drawn from the extracted SP list.

1. *"No último projeto encerrado, quantas horas alguém passou montando a prestação de contas — e quantas pessoas?"*
2. *"Já perderam prazo de diligência? O que aconteceu?"*
3. *"Quem monta a prestação de contas hoje — equipe interna, contador, ou consultoria? E quanto custa?"*
4. *"Se existisse um sistema que conferisse cada nota contra a planilha aprovada e avisasse do erro antes de enviar, você pagaria do orçamento do projeto ou do seu bolso?"* — **this is the whole business in one question**
5. *"Quantos projetos financiados vocês tocam ao mesmo tempo?"*

**Stop conditions — any one alone ends it:**

- 3+ of 5 say prestação de contas takes under ~8 hours per project → no pain, spreadsheet wins. STOP.
- 3+ of 5 say the consultancy handles it and they are happy → the incumbent is good enough. STOP.
- 3+ of 5 will not pay from the project budget → the frictionless-yes premise is false. STOP.
- 3+ of 5 run only 1–2 funded projects → ARPU collapses. STOP.

---

## 10. What kills it

1. **The consultancies are good enough and own the relationships.** They are the
   incumbent *and* the obvious channel — but channel-partner models are already
   refused, so this must win direct.
2. **Political risk.** Rouanet is contested and rule-set dependent. Mitigating
   evidence: R$ 3,41 bi captado in 2025, third consecutive record year, up 45%
   over 2023, and the mechanism survived a CPI.
3. **MinC improves SALIC itself.** Government software moves slowly, but this is
   the incumbent that could close the gap for free.
4. **Judgement, not data-entry.** If the hard part is interpreting what MinC will
   accept rather than reconciling documents, software helps less than it looks.
   Question 1 tests this.
5. **Network fit is the weakest leg — stated plainly.** Cultural producers are
   not her modelling/luxury-events network. The bridge is the sponsor side
   (6.252 CNPJs sponsor via Rouanet, many of them consumer brands) and São
   Paulo's brand-sponsored cultural circuit. This is genuinely weaker than the
   agency network was for LÍQUIDO, and it is the single biggest reason this is a
   CANDIDATE and not a decision.

---

## 11. What is still UNVERIFIED

- **No buyer has said yes to any price.** The bands are anchored to the 2–5%
  consultancy norm, not to a director's mouth.
- **Hours per prestação de contas is unmeasured.** The entire labour-substitution
  case rests on it. Question 1 exists to replace it with five real numbers.
- **Whether SaaS is accepted as a planilha line item.** Accounting *services* are
  verified as payable from project funds; a software subscription specifically is
  not. A cultural-projects accountant must confirm before any quote is issued.
- **The slot-release trigger** (see the correction in §5).
- Whether the 13 PJ currently running more than 10 concurrent funded projects are
  actually over the new Art. 10 cap, or grandfathered/counted differently.

---

## Verdict

PRUMO is the **best-evidenced candidate of the five**, and the first where the
buyer census was completed *before* the business was written rather than deferred
indefinitely: **933 PJ proponentes with 3+ funded projects, 448 with 4+, 145 of
those in São Paulo, R$ 8,45 bi of captação needing documentation.**

Its two honest weaknesses — a rare catastrophic sanction that must not headline
the pitch, and a weak network fit — are named here rather than discovered in
month three.

**It is a candidate. It becomes a decision only after five phone calls.**
