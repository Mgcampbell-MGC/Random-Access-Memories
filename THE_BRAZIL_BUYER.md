# THE BRAZILIAN SALARY-COMPARISON BUYER — 19 Aug 2026

**The hunt with the highest prior value: the channel was already proven, only the product was missing. It came
back with a channel CORRECTION that would have caused a false kill, a price CEILING that deletes a whole
family of candidates, and a lead.**

---

## 1. ★★ THE CHANNEL CORRECTION — VERIFIED BY ME, and it nearly went the other way

**`minhareceita.org` and `brasilapi.com.br` REDACT the email field.** The hunt measured 0/40 through those
mirrors — including Petrobras, Nubank, Magazine Luiza and Bradesco — and was minutes from writing *"the channel
is dead."* **`publica.cnpj.ws` serves the field intact.**

**I re-ran it myself on three CNPJs rather than take it on report:**

| CNPJ | `publica.cnpj.ws` | `minhareceita.org` | `brasilapi.com.br` |
|---|---|---|---|
| 33.000.167/0001-01 Petrobras | **`cc-rfisc@petrobras.com.br`** | `None` | `None` |
| 47.960.950/0001-21 Magazine Luiza | **`fiscal.estadual@magazineluiza.com.br`** | `None` | `None` |
| 18.236.120/0001-58 Nu Pagamentos | `None` *(genuine per-record absence)* | `None` | `None` |

> ### **CONFIRMED. Two of the three most convenient Brazilian CNPJ mirrors silently return `null` for an email that exists in the source. A fill-rate measured through either is a FALSE ZERO.**
>
> **This is the second time in two days that a wrong data source produced a confident wrong number in this
> project.** *(The first was my own FDA join.)* And note the failure mode is worse than an error: **it fails
> silently, in the direction of a kill, on the single most valuable channel in the file.**

**The layout is intact at source:** [`gov.br/receitafederal/dados/cnpj-metadados.pdf`](https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf)
still specifies **`CORREIO ELETRÔNICO — CONTÉM O E-MAIL DO CONTRIBUINTE`** in the ESTABELECIMENTOS layout.

### ★ THE FILL RATE — measured twice, independently

| Run | Sample | With email | Fill rate |
|---|---|---|---|
| Hunt agent, CNAE 6920601 ATIVA | **45** | 34 | **75,6%** |
| **Me, same CNAE, independent draw** | **14** | 11 | **78,6%** |
| *(agent's two internal batches)* | 13 / 32 | — | 76,9% / 75,0% |

**Four measurements clustered at 75–79%. Combined n≈59 → ~76%.**

> ### **★★ THE POSTAL LIST LAW IS NOW BOUNDED IN BRAZIL WITH A MEASUREMENT, NOT A HOPE.** *"Enumerable ≠ contactable"* holds across eleven inspected registers in the UK, EU, US and Australia — **and it does not hold in Brazil.** The Receita Federal CNPJ open data publishes a working email for roughly three quarters of active establishments, free, monthly, with CNAE, porte, capital social, situação cadastral and start date beside it.

**Sampling bias, stated plainly and shared by both runs:** `indicecnpj.com.br` paginates in CNPJ order and caps
near page 1.000, so every CNPJ sampled began `00000` — **pre-1996 registration roots.** Direction of bias is
genuinely unknown: old firms may hold stale records, but the field updates on every cadastral alteration and
active firms alter. **Treat ~76% as measured-with-known-bias. The definitive test is the bulk file itself,
which is free.**

**★ A correction of my own to add:** of 32 CNPJs I pulled from that CNAE listing page, **18 were NOT ATIVA
(56%)** while **0 had the wrong CNAE.** So the listing is accurate on activity code and **is not filtered to
active firms** — which means the population counts below, drawn from the same mirror, need re-checking against
the bulk file before anyone sizes a market on them.

**And a free segmentation lever nobody has used:** the same dataset carries **`PORTE DA EMPRESA`** (05 = DEMAIS,
i.e. neither ME nor EPP) and **`CAPITAL SOCIAL`**. **Filtering CNAE × porte 05 isolates the above-Simples
population — the only population that can pay — at zero cost, before a single email is sent.**

**Qualitative finding that matters as much as the rate:** the addresses are decision-makers, not switchboards —
`paulo.mendes@pcpconsultoria.com.br`, `tulio.resnitzky@toutatisbr.com`, `victor@contabilidadeatual.com.br`,
`lcsalvador@lcsalvador.com.br`. **At a five-person escritório even `contato@` lands on the sócio's desk.**

---

## 2. ★★ THE R$1.200 CEILING — this deletes a family of candidates in one line

> ### **A COMPLETE outsourced back office for a Brazilian small business — apuração do Simples, guias, escrituração fiscal, eSocial, folha — sells at R$450–1.200/month.** Mid-market (Lucro Presumido/Real) runs R$1.500–5.000.
>
> ### **NO BRAZILIAN SME WILL PAY R$1.000+/MONTH FOR ONE SUB-TASK WHEN THEIR ENTIRE COMPLIANCE BILL IS R$700.**

*(Sources: [Planus](https://planus.cnt.br/terceirizar-contabilidade-quanto-custa-por-mes-na-pratica-com-exemplos/),
[Ohub](https://www.ohub.com.br/precos/contabilidade-mensal) — **SECONDARY**, accountancy pricing pages, three
independent sources agreeing on the band; no primary survey located.)*

**The consequence is structural: the R$1.000+ price is only payable by (a) firms ABOVE the Simples ceiling, or
(b) firms that AGGREGATE many small businesses.** Every surviving candidate is one or the other. This killed
consultórios, farmácias, one-truck transportadoras and the whole "sell one clever thing to a Brazilian small
business" family at a stroke.

---

## 3. ★ THE LEAD — ESCRITÓRIOS DE CONTABILIDADE, priced per client in their portfolio

**Not one subscription. An aggregator play.** CNAE 6920-6/01, **113.133 listed active** *(mirror figure — see
the 56% caveat above)*.

**The obligation, and it is exogenous by statute.** Every month, for every client: eSocial folha events by day
15, **DCTFWeb by day 25** (IN RFB 2.005/2021, amended by IN RFB 2.237/2024), FGTS Digital by day 20. **Named
consequence: multa de 2% ao mês-calendário sobre as contribuições declaradas, limitada a 20%, mínimo R$500** —
issued automatically. **The firm controls neither the calendar nor its clients' headcount.** `THE
CONSTRAINT-SIDE LAW`, satisfied by statute.

**The specific pain.** DCTFWeb consolidates automatically from eSocial and EFD-Reinf. When the folha's own
totals, the eSocial totalizadores (S-5001 INSS, S-5002 IRRF) and the DCTFWeb consolidation disagree — usually a
rubrica mis-parameterised in S-1010 — the firm is notified automatically and must retify **after the deadline,
with juros and multa.** Tooling exists but is pitched at *"folhas de mais de 1.000 funcionários"* — **one
enterprise payroll, not sixty small ones.**

**The deliverable — four files they already hold, pure arithmetic, no opinion, no credential.**

> Per client per month they email four exports: the folha summary from their own system (Domínio, Alterdata and
> Questor all export), the eSocial S-5001/S-5002 totalizador, the DCTFWeb declared value, the FGTS Digital
> guia. **She returns one page per client: four numbers, three differences, and the list of client codes where
> they do not tie** — dated, with competência and CNPJ on every line. **She states no cause and proposes no
> fix.** The firm's CRC-registered contador does that.

**C1 clean** (no conversation needed to produce it) · **C4 clean** (files arrive by email, no credential, no
standing access) · **expert veto clean** (nothing asserted, so nothing believed).

**Arithmetic.** R$20–30 per client per month, floor R$1.000. A 60-client firm pays **R$1.500/month** against a
cheapest-possible junior at **R$3.734,35 base** — *(PRIMARY: CCT SINDCONT-SP × SESCON-SP 2025/26, PDF fetched
and read)* — call it R$5.600–6.300 fully loaded with 13º, férias+⅓, FGTS and the CCT's benefit clauses.
**R$1.500 is 24% of one head. At R$1.500 average she needs 39 firms for R$57.800.**

**★ Why this segment and no other:** accounting firms are the one Brazilian SME segment whose **entire operating
model is already receiving files by email and sending files back.** They will read a technical email and reply
in writing because that is their job. **Every other candidate segment defaults to WhatsApp and a phone call —
which breaks C1 at the exact moment it starts working.**

**The two real risks, named.**
- **Reserved-activity boundary.** Escrituração contábil is reserved (Decreto-Lei 9.295/46, CRC). Reconciliation
  and pre-processing are not — **but the line must be held explicitly in every sentence of the pitch**, and it
  is the kind of line a competitor can attack.
- **★ The sale may still be a phone call.** The existing B2B2B outsourcers for this exact buyer — Acelera
  Contador, ContabExpress — price ***"sob consulta, calculados pela carteira."*** **The whole question is
  whether a fixed published per-client price removes the call. If it cannot, `THE ONBOARDING LAW` closes this.**

---

## 4. ★★ THE VENDOR-URGENCY LAW — and it is dated to nineteen days

**The reforma tributária play looked like the answer for two hours** — cClassTrib, NCM and NBS remapping across
every product master in Brazil, on a statutory clock. Law-firm and vendor pages published this year still state
*"desde fevereiro de 2026 a Sefaz valida em tempo real… inconsistências bloqueiam o faturamento imediatamente."*

**Three primary facts kill it:**
1. **LC 214/2025 arts. 343/346** set IBS at 0,1% and CBS at 0,9% for 2026, and **art. 348 §1º** dispenses payment
   entirely for anyone *"que cumprirem as obrigações acessórias"* — the accessory obligation WAS the tax. **But
   LC 227/2026 inserted art. 348 §3º–§4º: an auto de infração now triggers a 60-day cure period, and curing
   extinguishes the penalty.** *(PRIMARY — Planalto fetched. Whether the 1,0% itself also survives the cure is
   the agent's reading of §1º against §3º and is **NOT CERTAIN**.)*
2. **Ato Técnico Conjunto CGIBS/RFB nº 1, de 31 de julho de 2026** postponed the validation rules that would
   have rejected NF-e, NFC-e, CT-e, GTV-e, BP-e, NF3e and NFCom lacking IBS/CBS fields — due to start **3 August
   2026**. Per [CGIBS's own page](https://www.cgibs.gov.br/receita-federal-e-comite-gestor-do-ibs-esclarecem-adiamento-das-regras-de-validacao-dos-documentos-fiscais-eletronicos):
   *"documentos fiscais terão sua emissão autorizada mesmo quando não contenham todos os campos relativos à CBS
   e ao IBS."* **No new date given.**
3. **The same page reports 88% compliance as at 4 August 2026. The ERP vendors already did the work.**

> ### **THE VENDOR-URGENCY LAW — when a statutory deadline creates a large data-cleanup task, the ERP vendors ABSORB it before a solo operator can sell it, and the vendor content describing the crisis OUTLIVES the crisis by months. Date-check the REGULATOR'S OWN PAGE before believing any compliance-urgency pitch.**
>
> **Here the gap between the blogs and the regulator is NINETEEN DAYS.** *(This is `THE COMPLIANCE COSTUME`
> with a clock on it: not a fake mandate, a real mandate that was quietly deferred.)*

---

## 5. THE OTHER TWO WORTH KEEPING

**★ HOSPITAIS E CLÍNICAS — the glosa spread, and the number is PRIMARY.** Observatório Anahp *Balanço* 7ª ed.,
Sept 2025 (PDF fetched and read): initial glosa **14,66%** in Q2 2025 against glosa that is ultimately justified
**1,97%** — *"das glosas iniciais de 15%, no final, cerca de 2% delas são mantidas."* **Thirteen points of gross
convénio revenue withheld on first pass and recovered only by someone doing the work.** A clinic billing
R$400.000/month has **R$52.000 contested monthly**; R$2.500/month is 4,8% of it. Cost side is a **faturista at
R$2.501,19/mês** (CAGED, n=53.894). Population 29.079 + 30.053. **Deliverable stays inside the expert veto: she
produces the line-by-line billed/paid/difference extract with the operadora's own glosa code verbatim — she
never says the glosa is wrong; the clinic's faturista argues it.** **Dies on screen 5: clinic owners are the
most WhatsApp-native buyers in Brazil.** And whether a mid-size clinic's glosa rate resembles ANAHP's
*associated large hospitals* is **UNVERIFIED**.

**★ IMPORTADORES — a genuine CLOCK-START that expires in 104 days.** Per
[gov.br/siscomex Cronograma de Desligamento LI/DI](https://www.gov.br/siscomex/pt-br/programa-portal-unico/cronograma-de-desligamento-li-di)
under Portaria Coana 165/2024, the phased DI shutdown completes **1 December 2026**. DUIMP cannot be registered
without the Catálogo de Produtos, and **all 10.300 NCMs now carry defined atributos**, published as CSV **last
updated 31/07/2026**. She never classifies anything — every statement is *"your file says X, the RFB file of
31/07/2026 says Y."* **Blocked on enumeration: the MDIC importer/exporter list returned 404 and 403 and the
bulk host was unreachable. UNVERIFIED, and it is the load-bearing fact.** Also a project, not a subscription.

---

## 6. KILLED, WITH CAUSES

**Screen-2 deaths (cheap entrenched Brazilian SaaS already owns it):** administradoras de condomínio 47.476
(Superlógica/Group/Ahreas) · corretoras de seguros 73.200 (Segfy/Quiver/Sciensa) · transportadoras 950.482 (the
CIOT integradoras) · farmácias 367.366 (a PDV software feature) · licitação monitoring (Effecti/Sollicita).

**Others:** laboratórios clínicos die twice — **RDC 786/2023 was revoked by RDC 978/2025**, and Controllab and
PNCQ sell the whole obligation end-to-end, output requiring interpretation · empresas de vigilância — cadence is
every 2–5 years, and the work is document assembly with the Polícia Federal, hitting **both** C1 and the
document-chasing veto · agências de viagem 223.556 — **demand-constrained** · advocacia 245.505 — a cálculo
judicial is a **determination** · engenharia consultiva — no file-computable recurring filing, plus construction
adjacency · RH/DP terceirizado — **2.004 is too thin** · **produtores rurais — they are *pessoas físicas* and are
not in the CNPJ base at all.**

---

## 7. THE CHEAPEST NEXT TEST — a COMPETITOR test, not a customer test

> **Email thirty escritórios de contabilidade from the free list, in Portuguese, one question:**
> ***"Vocês conferem hoje se o total da folha, o totalizador do eSocial e o valor declarado na DCTFWeb fecham
> entre si, cliente a cliente? Se sim, com qual ferramenta?"***
>
> **Count how many answers NAME A TOOL.** If most name one, the lead is dead on screen 2 and the aggregator
> thesis needs a different deliverable. **If most name a PERSON, the price is a salary and the lead holds.**

Written-only, free, no phone — **and it doubles as the first live measurement of the channel's reply rate**,
which is the number this entire file has never had.

**The single most important unknown:** whether ANY tool does multi-client eSocial × DCTFWeb reconciliation for
sixty small payrolls rather than one large one. **UNVERIFIED. Answer it before building anything.**
