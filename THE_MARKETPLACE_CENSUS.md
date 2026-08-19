# THE MARKETPLACE CENSUS — S5 tested with a full catalogue count, 19 Aug 2026

**DOOR 1 of `THE_REBUILD.md` — borrowed intent inside a B2B software marketplace — tested properly for the
first time. The agent did not sample or estimate. It pulled the entire paid cloud catalogue from Atlassian's
unauthenticated public REST API and counted every app in it.**

> **VERDICT: DOOR 1 IS CLOSED on this evidence. But the census produced three laws and one architecture worth
> more than the candidate, and one free stop-work test that must be run before ANY marketplace candidate is
> developed another hour.**

---

## 1. THE CENSUS — 4.192 paid cloud apps, counted

**Method: `GET marketplace.atlassian.com/rest/2/addons?hosting=cloud&cost=paid`, paged to exhaustion,
19 Aug 2026. 4.192 complete records plus a 34-app stratified live price sample. Re-runnable by anyone.**

| Percentile | Installs |
|---|---|
| p10 | **0** |
| p25 | 2 |
| **p50 — MEDIAN** | **13** |
| p75 | 102 |
| p90 | 535 |
| p95 | 1.173 |
| p99 | 4.774 |
| max | 62.659 (draw.io) |

- **623 of 4.192 paid apps (14,9%) have ZERO installs.** 1.931 (46,1%) have fewer than ten.
- **2.084 (49,7%) have zero reviews.** Median review count across the whole catalogue: **1**.
- **1.384 vendors. MEDIAN VENDOR: 8 INSTALLS across its entire catalogue.**
- The top of the table is **Appfire (93 apps, 183.501 installs), Tempo, Seibert/draw.io, Adaptavist,
  SmartBear, K15t, Deviniti** — software companies with staff.
- **Single-app vendors with ≥1.000 installs: 12 out of 1.384. One of the twelve is Atlassian itself.**

### And the number that actually decides it — measured, not asserted

**Four of those eleven genuine single-app vendors have short enough version histories that their earliest
retained release date is credible:** Magic Estimations (2020-11-07) · Intercom for Jira (2019-06-10) ·
JQL Tricks (2020-09-07) · Nave Kanban Analytics (2019-07-09).

> **They took roughly 5,8 to 7 YEARS to reach 1.000–1.400 installs.**

### What an install is worth — 34 live price tables

**27 of 34 (79%) are FREE at ten users** — Atlassian's standard small-team tier, so a large share of installs
generate exactly nothing. **Median annual price at 50 users: $450. At 100 users: ~$900.**

**$156.000/year ÷ $450 = 347 paying customers.** At a 25% install-to-paid rate that is **1.387 installs — the
96th percentile of every paid cloud app in the store.** *(The true conversion rate is not published by
Atlassian and could not be obtained — **UNVERIFIED** — but across any plausible value the answer lands between
p90 and p97.)*

> **The channel's no-sales-call property is real and was never the binding constraint** — a median app at 100
> seats is ~$900/year, far under the self-serve ceiling, so no human buyer with a calendar ever appears.
> **VOLUME is the constraint, and the measured time to reach it is five to seven years against an
> 18-month clock.**

**CORRECTION TO `GRAVEYARD.md`:** it records the Atlassian arithmetic as *"27 × $90"*. **Observed median
pricing does not support $90/month.** At the median 50-user price of $450/year, 27 customers yields
**~$1.013/month, not $2.430 — an overstatement of ~2,4×.** The graveyard's conclusion holds; its arithmetic
was optimistic and is restated here.

---

## 2. THREE LAWS

### THE VERIFICATION-IS-THE-BRAND LAW

**The largest live verified-revenue feed found states its verification rule verbatim:** *"To be verified…
your 𝕏 post must contain 'I made' and '$' sign."* **Membership in the verified set is conditional on posting
publicly.** The feed's largest indie-software entry breaks down as a revenue-verification tool, an analytics
tool, a course and a boilerplate — **products sold to the audience, about building for the audience** — plus
direct creator payouts. Several high entries are salaried jobs. Two of the largest are memecoin posts.

> ### THE VERIFICATION-IS-THE-BRAND LAW — publicly verifiable success in a channel is not a neutral sample of that channel. It is a sample of the operators who CHOSE TO BE VISIBLE, and visibility is itself their business model. **Asking any agent to "find verified examples" of a faceless business guarantees an audience-driven answer set. Use PLATFORM CENSUSES instead — they count everyone, including the silent.**

**And the corollary for C2:** a large share of what looks like solo-SaaS success is **audience monetisation
wearing SaaS clothing** — courses, boilerplates and tools sold to other indie hackers. **Closed to her twice
over: it needs a name, and it needs her to be believed as an expert.**

*(Also recorded as unreadable, in the same class as Etsy: **Indie Hackers returns a Cloudflare interactive
challenge on every path including `/robots.txt`.** Baremetrics Open Startups is down to five companies, none
a faceless solo. Bannerbear closed its open page. Nomad List's is offline. MicroConf's survey is email-gated
and ends in 2022.)*

### THE MERCHANT-OF-RECORD SPLIT — a ten-second screening question

| **GROUP A — the platform bills the customer** | **GROUP B — the platform is a directory** |
|---|---|
| **Atlassian · Shopify · monday.com · Salesforce Checkout · Xero** | **HubSpot · Intuit/QuickBooks · Chrome Web Store · WordPress.org · Slack · Notion** |
| Platform collects, remits the customer's taxes, pays her a net share | She builds her own billing and **is her own merchant of record** |
| **Converts her from a merchant selling to thousands of foreign consumers into a supplier invoicing ONE corporate counterparty — an ordinary service export** | **Re-opens exactly the configuration killed in `THE_MERCHANT_OF_RECORD_KILL.md`** by RIR/2018 art. 162 §1 and the stacked PIS/COFINS + US sales tax problem |

> **Group B's "0% revenue share" is not generosity. It is the absence of the only thing that made the platform
> useful to her.** Six of thirteen marketplaces eliminate themselves on this one question.

### THE UNCERTAINTY-PREMIUM LAW — see §4

---

## 3. THE FORGE ARCHITECTURE — the one genuinely positive finding

**Atlassian's own "Runs on Atlassian" documentation:** *"Apps exclusively use Atlassian-hosted compute and
storage"* · all storage is Atlassian-hosted · *"Your app must not egress data, with the exception of egress
for analytics purposes."*

> **She never receives a token, never stores customer data, never runs a server that can be breached.
> C4 IS SATISFIED BY THE PLATFORM'S ARCHITECTURE RATHER THAN BY HER DISCIPLINE — and the 0%-to-$1M revenue
> share is conditioned on precisely that architecture. The commercial incentive and the C4-compliant design
> are the same requirement.**

**This matters beyond Atlassian.** Most B2B apps require an OAuth grant stored as a long-lived refresh token —
standing access, a C4 violation, unavoidable for HubSpot, Intuit, Xero, Conta Azul, Bling, monday and
conventional Shopify apps.

> **NEW SCREENING QUESTION for every integration candidate: "is there a runtime where the PLATFORM holds the
> data and I hold nothing?" Where the answer is yes, the platform usually absorbs the trust gate as well.**

**The other C4-clean shapes, needing no marketplace:** **file-in / artefact-out** *(the customer uploads a
file and receives a generated file — exactly the shape `CLAUDE.md` already endorses)* · fully client-side
browser extensions *(no payment rail)* · WordPress plugins *(GPL, free-only in the repo)*.

---

## 4. PLATFORM RISK IS NOT THEORETICAL — it was falsified inside the research window

**Xero retired revenue share on 2 March 2026 and now CHARGES developers.** Listing is unavailable below the
**Plus tier at A$245/month**, which additionally requires App Certification plus an **initial and annual
Security Assessment**. **A channel that paid 85% last year bills A$245/month this year.** Atlassian's Connect
rate also goes 20% → 25% on 1 July 2026.

> ### THE UNCERTAINTY-PREMIUM LAW *(from the same agent's AI-monitoring kill, and it generalises here)* — a business whose price is supported by the buyer's ignorance of a new channel is priced on a DECAYING ASSET. **Before building on a platform or a measurement, ask: does the platform itself have both the data and the incentive to publish this? If yes, you are renting time, not building a business.**

---

## 5. THE STOP-WORK TEST — free, binary, and nobody has run it

**NOT ONE of the thirteen marketplaces documents whether it will pay a Brazilian.**

- **Atlassian:** EFT to a bank account in the partner's name, $500 accrual threshold, W-8BEN or W-8BEN-E.
  **A developer asked for the supported-country list on 4 Aug 2026 and Atlassian has not answered** — and
  noted the catch-22 that the support form requires a Vendor ID obtainable only by registering first.
- **Shopify:** payouts via Hyperwallet, $25 minimum, 0,50% conversion fee. **Brazil is not named anywhere.**
- **monday.com:** *"monthly payouts via Payoneer in USD."* Payoneer operates in Brazil, **so the rail exists —
  but monday publishes no country list and no tax-form requirement.**
- **RapidAPI:** **PayPal only**, and only a W9 (a US form) is documented. **Probably fatal for Brazil.**

> **Register a Marketplace Partner profile with a Brazilian address on Atlassian and on monday.com, and see
> whether the payout configuration accepts a Brazilian bank account. Written, faceless, free, binary, and it
> returns an answer in days. NO MARKETPLACE CANDIDATE SHOULD BE DEVELOPED ONE HOUR FURTHER UNTIL IT IS RUN.**

---

## 6. Brazil — one real finding and two thin ones

**PIX AUTOMÁTICO IS A GENUINE DOMESTIC SUBSCRIPTION RAIL, and it is new.** Live since **June 2025** under
**Resolução BCB nº 482, de 5 de junho de 2025**. The BCB's own implementation guide defines a *recorrência*
with periodicity, start date and receiving-user identity, supporting **fixed or variable amounts** for
*"assinaturas de serviços, mensalidades."*

> **A Brazilian PJ can collect recurring subscriptions natively, in BRL, with no card network and no foreign
> acquirer. That removes the acquirer-risk-review conversation flagged by THE ONBOARDING LAW, and removes the
> international merchant-of-record problem entirely for domestic sales.**

> ### ⚠ CORRECTED same day — **PIX IS NOT FREE FOR HER.** I wrote that it was. **Resolução BCB 19/2020 art. 4** expressly permits an institution to charge **a legal entity for both remittance and receipt**, and to charge **a natural person *"as a result of receiving funds for the purpose of purchasing."*** **Receiving Pix as payment for a sale is precisely the case the regulation allows a bank to price.** *(PagBank advertises "PIX 0% nos primeiros 30 dias" — free as a promotion, priced after.)* **What survives is still real: no acquirer risk review, no chargeback dispute argued by telephone, settlement in seconds. The per-transaction cost is PSP-specific and UNVERIFIED.**

**Pix Automático solves COLLECTION better than any foreign marketplace. It does nothing for DISTRIBUTION,
which is the constraint that actually kills this candidate.**

**Omie.Store:** a real ERP app store with healthy observed prices — **R$58,80 to R$559/month** — but
**64 vendors** against Atlassian's 1.384, every one an established software company, the storefront's primary
call to action is *"Fale com um consultor"*, and **no developer revenue-share or listing terms are published
at all. UNVERIFIED.** **Bling:** self-serve app registration with OAuth, monetisation described as a
percentage of monthly value by integrated customer count — **the percentage is behind Cloudflare 403 and
needs a human with a browser.** Its registration form requires a mobile number *"para eventuais contatos"* —
survivable under the relaxed C1, flagged not decided.

---

## 7. What would have to be true — and the row that kills it

| | Must hold | Verdict |
|---|---|---|
| 1 | Reach the **top 4–6%** of a marketplace catalogue | Measured: 256 of 4.192. **Possible, not probable** |
| 2 | **In months, not years** | **Measured: 5,8–7 years. Fails by an order of magnitude** |
| 3 | In-store search alone carries discovery, no launch audience | **UNVERIFIED — nobody has demonstrated a zero-audience launch with public evidence** |
| 4 | Platform is **Group A** | True for four; eliminates six |
| 5 | Platform **will pay a Brazilian** | **NOT ESTABLISHED FOR ANY OF THEM. Stop-work item** |
| 6 | The platform does not change the deal underneath her | **FALSIFIED inside the research window — Xero** |

> **Row 2 kills it. The project already held that consumer app stores take 12–18 months with organic discovery
> near zero. This is that finding reappearing in B2B form, WORSE. The built-in buyer intent is real; it simply
> is not enough.**
>
> ### **B2B marketplaces are not a different animal from consumer app stores. They are the same animal with a better-dressed buyer.**
