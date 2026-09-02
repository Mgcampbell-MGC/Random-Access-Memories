# PROBE KIT — 2 Sep 2026. Everything up to the send, for candidates #1 and #2.

**Sending cold mail to strangers is the founder's act, from her own domain, under her name. This kit does the
part that costs nothing and needs nobody's permission: the lists, the measured fill rates, the two email arms,
the pre-committed pass bars, and the scripts that regenerate every number.**

---

## PART A — CONFORMIDADE v2 (#1): the dental list, measured

### A1. The register is CNES, not the CNPJ file — and it is better
RDC 1.002/2025 applies to *every* service providing dental assistance, **including pessoa-física consultórios that
have no CNPJ**, and it is enforced by the vigilância sanitária against the CNES registration. The Ministry of
Health's open-data API serves CNES directly, no key, with the establishment's own registered email and phone:

`https://apidadosabertos.saude.gov.br/cnes/estabelecimentos?codigo_municipio=355030&codigo_tipo_unidade=22&limit=20&offset=0`
*(20 rows a page; tipo 22 = consultório isolado, 36 = clínica/centro de especialidade; name-match ODONT|DENT|BUCAL…)*

**Measured 2 Sep 2026, São Paulo capital, first 5.000 rows of each tipo** — `bin/cnes_dental_list.py 355030`:

| | |
|---|---|
| Dental establishments found | **1.986** *(a floor — both tipos have >5.000 rows in the city)* |
| **Email registered** | **1.394 / 1.986 = 70,2%** |
| Phone registered | 1.389 / 1.986 = 69,9% |
| Pessoa jurídica (has CNPJ) | 1.578 = 79,5% · **pessoa física 393 = 19,8%** *(invisible to any CNPJ-based list)* |
| Record updated 2025–26 | 1.986 / 1.986 |
| Email domains | gmail 577 · hotmail 258 · yahoo 66 · outlook 54 · uol 45 — **owners' own inboxes, not a contador's** |

**Two facts this settles.** (1) `THE POSTAL LIST LAW` is bounded again, on the exact buyer: **~70% of São Paulo
dental establishments publish a working email in a public register**, in line with the 76% measured on accounting
firms. (2) **The Receita bulk host is not a dependency any more** — `arquivos.receitafederal.gov.br/dados/cnpj/…`
returned **404 on every path tried on 2 Sep 2026**; CNES needs no CNPJ join and covers the PF fifth the CNPJ file
cannot see.

⚠ **The CSV is personal data from a public register. It stays in the scratchpad, never in git.** Regenerate it when
ready to send; take 60 rows at random, split 30/30; for the WhatsApp fallback the phone column is there.

### A2. The two arms — Portuguese, ready to paste
**Send from her own domain, her own name, ≤30 per arm, one send, no follow-up sequence.** Bottom line on every
message: *"Se não quiser receber outros e-mails meus, responda 'não' e não escrevo de novo."* Basis: contact data the
establishment itself published in a public register, B2B, one message, with opt-out.

**ARM A — the price question (30 clinics). Asks for a number, offers nothing.**
> **Assunto:** RDC 1.002/2025 — quanto custou a documentação da sua clínica?
>
> Olá, [nome da clínica].
> Sou a Sol, de São Paulo. Estou levantando com clínicas odontológicas quanto custou preparar a **Série de
> Documentos de Boas Práticas** exigida pela **RDC 1.002/2025** (prazo: dezembro de 2026).
> Duas perguntas rápidas — só o número já ajuda:
> 1. Quanto a clínica pagou, ou pretende pagar, pelo conjunto de documentos?
> 2. Quem elaborou — o próprio RT, um consultor, um modelo comprado?
> Em troca, mando o resumo do que ouvi das outras clínicas.
> Obrigada, Sol.

**ARM B — the offer (30 different clinics). Sells the pack at the price under test.**
> **Assunto:** RDC 1.002/2025 — os 17 documentos prontos antes de dezembro
>
> Olá, [nome da clínica].
> A **RDC 1.002/2025** exige que toda clínica odontológica tenha a Série de Documentos de Boas Práticas
> (art. 113 — 17 documentos) até **dezembro de 2026**.
> Eu preparo o conjunto completo a partir de um questionário de 40 minutos sobre a sua clínica — PGRSS, PGTS,
> plano de manutenção, controle da água, educação permanente, contratos de terceirizados e os demais — já
> preenchido com os dados da clínica, para o RT revisar e assinar. Entrega em 5 dias úteis. **R$ 1.500, por Pix,
> depois da entrega.**
> Se quiser ver um dos documentos antes de decidir, responda **"exemplo"**.
> Sol.

### A3. Counting, pre-committed before the first send
| Arm | Count | PASS | KILL |
|---|---|---|---|
| A | replies containing a **number** | **≥3 of 30 name ≥R$800** | modal answer ≤R$300, or "o RT fez" everywhere |
| B | replies asking **"exemplo"**, the price, or the deadline | **≥2 of 30** | 0 of 30 |
| Both | total replies of any kind | — | **0 of 60 ⇒ the email rail is dead for this buyer; retry ARM A only, by WhatsApp, to 20 phones** |

**What the R$97,90 kit changes:** the pack cannot sell on *conformance* — a 186-template Word kit already sells
that for R$97,90 on Hotmart. ARM B sells **the dentist's own hours**: the 10–20 hours of filling 186 blanks, against
a dated deadline. If ARM A's modal number is R$100–300 and ARM B gets nothing, the business is 40–50 packs a month
through the email rail at the floor — still on the bar — or it is not a business.

---

## PART B — REPRESENTANTE (#2): the foreign-applicant count, measured

### B1. Four weeks of INPI's marks gazette — `bin/inpi_foreign_applicants.py`
Source: `https://revistas.inpi.gov.br/txt/RM<edition>.zip`, editions 2901–2904 (11 Aug – 1 Sep 2026), free, no login.

| Edition | Processos | With a foreign titular | New filings w/ foreign titular | Distinct foreign titulares | Procuradores serving them | Madrid w/ foreign holder | **Madrid, no Brazilian procurador** |
|---|---|---|---|---|---|---|---|
| 2901 · 11 Aug | 40.888 | 2.598 | 344 | 1.482 | 271 | 116 | 79 |
| 2902 · 18 Aug | 37.130 | 4.285 | 409 | 2.434 | 375 | 812 | 713 |
| 2903 · 25 Aug | 47.345 | 3.762 | 665 | 2.222 | 318 | 662 | 562 |
| 2904 · 1 Sep | 36.995 | 4.092 | 872 | 2.245 | 320 | 939 | 719 |
| **4 weeks** | | | **2.290** | **6.990 distinct · 1.021 on new filings** | **707 distinct** | **2.529** | **2.073 (82%) · 1.610 distinct holders** |

**What it says, in order of weight:**
1. **The role is demonstrably held by individuals, at scale.** Of 707 procuradores serving foreign titulares,
   **369 are individual names (no firm word), handling 3.246 of 11.032 processos = 29%** — Carlos Eduardo Galhardi
   Alves 250, Ana Claudia Chaves Ramos Ferreira 202, Jacques Labrunie 171, Kivia Ribeiro da Silva Xavier 136.
   *(Whether they are registered Agentes da Propriedade Industrial is not in the XML — UNVERIFIED.)*
2. **The channel is concentrated but not closed:** top 10 firms hold 28,5%, top 50 hold 66,8%, and **404 of 707
   procuradores had three or fewer foreign processos in the month** — a long tail of small practices.
3. **★ The compelled pool nobody is serving yet is the Madrid Protocol.** In four weeks, **2.529 Madrid
   designations into Brazil carried a foreign holder, and 2.073 of them (82%) print NO Brazilian procurador** —
   1.610 distinct holders, ≈ **20.000 a year**: Thrive Brands LLC, Wishing Well Games LLC, Genmab A/S, Lundbeck,
   Wellbore Integrity Solutions. 1.759 were grants (IPAS770), 769 were publications for opposition (IPAS756).
   **The moment INPI issues an exigência or an opposition lands, LPI art. 217 makes a Brazil-resident procurador
   mandatory** — the exact compelled moment, on a dated clock, for a named foreign company. *(When exactly the
   duty attaches for Madrid holders: see the INPI FAQ note in the board — UNVERIFIED until fetched.)*
4. **Volume for the national route:** ~255 distinct new foreign applicants a week, all already represented.
   Country mix: US 3.658 · CN 2.683 · DE 858 · JP 695 · FR 691 · CH 602 · GB 601.

### B2. The asks — provider side only
**⚠ Do NOT email a foreign holder quoting its process number.** The file already recorded that the USPTO names
unsolicited serial-number email as a scam pattern; INPI publishes the same warning about *"boletos falsos."* A cold
mail that reads *"your designation nº 9xxx was published on…"* is indistinguishable from the fraud it would compete
with. The buyer-side test for #2 is therefore the observed price plus the provider quotes, not a holder survey.

**20 providers, as a prospective client** — 10 from the individual-procurador list above, 10 from search
(*"representante legal empresa estrangeira Brasil"*, *"procurador residente Brasil CNPJ estrangeiro"*):
> **Subject:** Standing legal representative in Brazil — quote
>
> Hello. We are a small US consumer brand about to (a) register a Brazilian trademark and (b) open a Brazilian
> subsidiary, and we need a Brazil-resident legal representative for the CNPJ and INPI filings.
> Could you send your monthly or annual fee for acting as our standing representative, and what it includes?
> Thank you, [name].

**Count:** replies containing a number, and the number. **PASS: ≥5 of 20 quote, with a median ≥US$300/month.**
Below that the observed US$400–800 is a ceiling held by firms, not a market price.

---

## PART C — what to record where
- Board #1: distribution rail is **CNES, 70,2% email, includes PF** · Receita bulk host 404 · template floor R$97,90.
- Board #2: **Madrid pool ≈20.000 holders/year without a Brazilian procurador**; individuals hold 29% of the role.
- `CLAUDE.md`: one bullet under the postal-list law — CNES as a second free email rail for Brazilian health
  establishments; the Receita host dependency.
