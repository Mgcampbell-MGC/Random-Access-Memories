# BRAZILIAN SaaS — HUNTED AND CLOSED, 4 Sep 2026

**Six lenses, fifteen agents, zero candidates reached adversarial review.** The second consecutive six-lens
hunt to hand the judge an empty board. Rather than manufacture one, the judge went and read the actual pricing
pages of six real Brazilian SaaS companies. **That census is the finding.**

---

## 1. The price census — 19 published plans, six vendors, retrieved 4 Sep 2026 by `curl`

*Undiscounted monthly list prices, i.e. the numbers most favourable to any candidate. A "Black" promotion was
live on Bling and ContaAzul at retrieval and is excluded.*

| Vendor | Source | Published monthly plans |
|---|---|---|
| **Bling** (Olist, ERP) | `bling.com.br/planos` | R$60 · R$120 · **R$650** · Elite *sob consulta* |
| **ContaAzul** (financial back office) | `contaazul.com/planos/` | R$289,90 · R$549,90 · R$719,90 · **R$1.029,90** |
| **Tiny** (ERP) | `tiny.com.br/planos` | R$66 · R$177 · R$390 · **R$948** |
| **Omie** (ERP) | `omie.com.br/precos/` | *a partir de* R$309 · R$419; seven revenue bands behind a calculator |
| **iClinic** (clinic EHR) | `iclinic.com.br/precos/` | R$99 · R$129 · R$169 · R$299 **per professional** |
| **Clinicorp** (dental) | `clinicorp.com/planos` | R$159,90 · R$369,90 |

> ### n = 19. Range **R$60–1.029,90**. **Median R$299/month.** Only **2 of 19 (10,5%)** exceed R$720.

Effective prices are lower still on annual billing: ContaAzul R$179,90–799,90; Tiny R$55–758.

**What that does to the bar** (R$12.300–15.400/month gross domestic):

| Observed price | Customers needed |
|---|---:|
| R$99 (iClinic Starter) | **124–156** |
| R$159,90 (Clinicorp Standard) | **77–96** |
| **R$299 (census median)** | **42–52** |
| R$650 (Bling Diamante) | 19–24 |
| R$1.029,90 (census maximum) | 12–15 |

**And the sentence that closes it: R$1.029,90 is what a funded, hundreds-of-employees incumbent charges a
médio-porte firm for its ENTIRE financial back office.** A solo operator's single-feature product does not price
above a full ERP. **Realistic band R$99–399 ⇒ 42–156 paying Brazilian SME customers.**

## 2. ★★ The R$1.200 ceiling, independently confirmed in a different category

The archive's R$450–1.200 figure is the price of back-office **LABOUR** (accountancy firms). This census is the
price of back-office **SOFTWARE**. **Different sellers, different category, no derivation between them — the
judge explicitly ran the multiply-out check and they are not the same number twice.** They land in the same
place anyway.

> **Whether a Brazilian SME buys its back office as PEOPLE or as LICENCES, total spend tops out around
> R$1.000–1.200/month. That is not a coincidence; it is the buyer's actual budget.**

## 3. ★★★ THE AGGREGATOR IS ITSELF AN SME — escapes (a) and (b) are the same escape

**This is new and it collapses two of the three named escapes into one.**

An accounting firm with 200 clients bills **200 × R$450–1.200 × 12 = R$1,08–2,88 M/year** —
**below the R$4,8 M Simples ceiling.** So "sell to an aggregator" does not escape the ceiling; **the aggregator
is inside it.**

> **To be above the Simples ceiling a Brazilian accounting firm needs ≈334 clients at R$1.200 each, or ≈889 at
> R$450.** *(Verified: 4.800.000 ÷ (1.200×12) = 333,3; ÷ (450×12) = 888,9.)*

⇒ **Escape (a) "sell above the Simples ceiling" and escape (b) "sell to an aggregator" are ONE escape, and it is
far narrower than I assumed when I wrote the brief.** Only escape (c) — **sell abroad in dollars** — is genuinely
independent, and it is not a Brazilian SaaS business at all.

## 4. ★★★ THE STEADY-STATE KILL — a one-time budget cannot fund a subscription business

**The cleanest proof in the document, and it needs no external source.**

A subscription base with monthly gross adds *a* and monthly churn *c* settles at **N\* = a/c**.
Her budget is **US$3.000 once, ever** = R$15.600, of which **R$8.000–12.000 goes to the v1 build**, leaving
**R$3.600–7.600 for acquisition, non-renewing.**

> ### ⇒ *a* → 0 after year one, therefore **N DECAYS GEOMETRICALLY TO ZERO. THERE IS NO STEADY STATE.**

To merely *hold* 45 customers at the census median (R$299 × 45 = R$13.455/month, mid-bar), forever:
**1,4 new customers/month at 3% churn · 2,3 at 5% · 3,2 at 7%.** *(Churn rates **UNVERIFIED** — no primary
Brazilian SMB SaaS source was found. **The decay-to-zero result does not depend on them; only the replacement
rate does.**)*

Year one ⇒ ~45 to build + ~20 to hold = **~65 sign-ups**, implying **CAC ≤ R$77** — and **the budget does not
reload in year two at any CAC.**

**Her complete channel list:** SEO ranking (out of reach, and the prize is shrinking — Pew 8% CTR with an AI
summary vs 15% without) · paid ads (one-time money, cannot fund perpetual replacement) · app stores (**median 13
installs across all 4.192 paid Atlassian apps**) · affiliate marketplaces (**Kiwify: R$5.000 lifetime sales
before you may list**) · audience (25.000–45.000 subscribers) · **cold written outreach** · **a partner who
already holds the customers.**

> **Two channels are live. Both are one-to-few. Neither produces 65 self-serve SME sign-ups a year.**
> **SaaS needs 42–156 customers; her distribution produces single digits.**

## 5. The monitoring pincer, confirmed in Brazil, in reais

**Above roughly R$1.000/month the published price disappears** — measured in the fetch itself: Bling Elite
*sob consulta* · Tiny's top tier *"GMV acima de R$400 mil — sob consulta"* · Clinicorp Premium *"Fale com um
especialista"* · Omie hides per-band prices behind a calculator · **`sankhya.com.br/planos/` and
`totvs.com/precos/` both returned HTTP 404 on the obvious paths.**
⇒ **Self-serve is R$60–1.030; above that the category is sales-force gated.** The pincer is not a US artefact.

---

## The laws

> ### ★★★ THE AGGREGATOR IS ITSELF AN SME. "SELL TO SOMEONE WHO HOLDS MANY SMALL CLIENTS" DOES NOT ESCAPE A SMALL-BUSINESS PRICE CEILING — IT INHERITS IT.
> 200 clients × R$450–1.200/month = R$1,08–2,88 M/year, **below the R$4,8 M Simples ceiling.** A Brazilian
> accounting firm needs **≈334 clients at R$1.200, or ≈889 at R$450**, to sit above it. ⇒ **Before pricing to an
> aggregator, COMPUTE THE AGGREGATOR'S OWN REVENUE. If it is itself below the ceiling you are trying to escape,
> you have not escaped anything.** *(This merges two of the three escapes from `THE R$1.200 CEILING` into one and
> leaves only "sell abroad in dollars" genuinely independent.)*

> ### ★★★ THE STEADY-STATE KILL — A ONE-TIME CAPITAL BUDGET CANNOT FUND A SUBSCRIPTION BUSINESS. N\* = a/c, AND WHEN *a* → 0, N → 0.
> Churn is perpetual; her US$3.000 is not. **Holding 45 customers at R$299 needs 1,4–3,2 new ones EVERY MONTH,
> FOREVER, and the budget does not reload.** ⇒ **Screen every recurring-revenue candidate on REPLACEMENT RATE,
> not on customer count** — ask *"how many must I add every month forever, and what channel produces that after
> the money runs out?"* **Needs no market research and kills a whole shape in one line.** *(It does NOT touch
> per-unit or one-off work, where there is no base to decay — which is exactly why the surviving candidates in
> this archive are per-unit.)*

> ### ★★ A SECOND MEASUREMENT IN A DIFFERENT CATEGORY IS WORTH MORE THAN A LARGER SAMPLE IN THE SAME ONE.
> `THE R$1.200 CEILING` was measured on accountancy **labour**; this census measured **software**. Different
> sellers, different product, no shared derivation — **and the same R$1.000–1.200 answer.** ⇒ **When you want to
> confirm a ceiling, do not re-sample the same market; find a DIFFERENT market that serves the same budget.**
> *(And run the multiply-out check first — the judge did.)*
