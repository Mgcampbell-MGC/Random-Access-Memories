# PART 0 — HOW TO BUILD FROM THIS DOCUMENT

This preface addresses the Claude Code session that will build Caixa Cheia from this document. You have no other context. Everything you need is in this document; anything the document does not settle is marked **[OPEN]** and collected in §23. Do not invent facts, prices, API fields, or legal positions that are not written here.

## 0.1 Read order

1. **§1 and §6 first** — the thesis and the locked decisions. §6 is a constitution: nothing in it may be changed by you, ever, regardless of how convenient a change would appear mid-build.
2. **§7–§10** — architecture, data model, importers, and the eligibility gate. These define the spine of the system.
3. **§11–§14** — WhatsApp, payments, offer/checkout/voucher, consent. These are the external integrations; each carries verified API facts and [OPEN] flags you must respect.
4. **§15–§16** — dashboards and the records vault (what you render on top of the spine).
5. **§5, §20, App C** — legal and tax architecture. You are not the lawyer, but the code enforces legal posture (fail-closed gate, operator-preserving approval artifact, allowlist importer), so you must understand *why* before you build *what*.
6. **App A and App B** — the pt-BR copy pack (use verbatim; never rewrite locked copy) and the error/webhook handbook (build monitors directly from it).
7. **§22–§24 (this part)** — sequencing, gates, and the week-1 checklist that tells you what exists in the real world before you write code.

## 0.2 Build order and definitions of done

Build in milestones. Each milestone has a definition of done (DoD); do not start the next until the current DoD is demonstrably met. Spec sections are binding.

| Milestone | Scope | Spec sections | Definition of done |
|---|---|---|---|
| **M0 — Repo + schema** | Monorepo (Next.js App Router + Node worker + Postgres), schema migrated, append-only audit tables, secrets vault for per-salon Asaas keys, TZ America/Sao_Paulo, money in integer centavos, phones E.164 | §7, §8 | Fresh clone → migrate → seed → all state machines (§8.7) representable; audit tables reject UPDATE/DELETE; CI green |
| **M1 — Importer + scan** | Trinks CSV adapter, column classifier with allowlist, dropped-columns receipt, dedupe, suppression-authority check, eligibility gate (4 campaign preconditions P1–P4 + 9 per-client checks C1–C9 + approval artifact, fail-closed), scan output (4 numbers) | §9, §10 | Real Trinks export file → scan produces total / lapsed / contactável / elegível; every dropped column logged by name+count with no content; a suppressed phone in a re-imported CSV stays suppressed |
| **M2 — Raio-X** | Audit generator: imported data → HTML→PDF + private stable URL; locked accounting language only (§19 + App A); Trinks caveat rendered ("active unconsumed balances only") | §19 | Given M1 data, one command produces the full Raio-X PDF + URL; regeneration is free and idempotent |
| **M3 — Offer page + Asaas (sandbox)** | Opaque offer page with all CDC disclosures (§13), Pix charge with 20% split on netValue, webhooks, pro-rata refund engine, fee read live from GET /v3/myAccount/fees (never hardcoded); transactional email (Resend) for Raio-X auto-release on Pix confirmation (§15.4) | §12, §13 | Full sandbox loop passes: charge → split PENDING → confirm → netValue split ≈ 20% → full refund reverses split → partial refund with `splitRefunds` reverses pro-rata |
| **M4 — Meta Tech Provider onboarding + templates** | Embedded Signup v4 coexistence flow, WABA-in-BRL creation, pt_BR template submission pipeline honoring every mechanical rule in §11 | §11, §17 | One real salon (or founder's test number) onboarded via ES; one MARKETING template approved in pt_BR; history-sync captured inside the 24h window |
| **M5 — Send engine + monitors** | Queued send loop (idempotent, 250-recipient portfolio limit aware), per-error handling from App B (131049 never retried; 131050 → permanent suppression), `user_preferences` webhook, free-text SAIR matcher, coexistence heartbeat monitor (day-9 dashboard alert; 9/10/12 escalation per §15.11), template pause/quality monitors (§11.5.1 ladder), delivered-not-sent accounting | §11, App B | A 5-recipient warm send completes; injected 131049/131050/132015 fixtures produce the specified state transitions and zero retries |
| **M6 — Dashboards** | The 10 founder screens of §15, pt-BR throughout | §15 | Every screen renders from real M1–M5 data; approval flow works end-to-end from Campanhas builder to owner "APROVO" |
| **M7 — Records vault** | Per-salon LIA/DPA versions, per-send approval artifacts (dated, named segment rule, count, message text), consent records with exact displayed string + version + timestamp + source + refusals, export bundles | §16, §14 | For any campaign, one click assembles the complete defense file: LIA version, DPA, approval artifact, gate results, suppression log, send manifest |

## 0.3 Go/no-go tests that gate coding work

Two real-world tests come **before** the code they would otherwise justify:

1. **Asaas unlinked split (Gate 1) before any payment UI.** Sandbox test with account B registered independently at sandbox.asaas.com (never via POST /v3/accounts — that tests the wrong thing), then re-run in production at R$5. Script and assertions in §12. A 400/403 on split creation = NO-GO → Efí fallback, and M3's payment layer is rewritten against a different provider. Do not build checkout screens against an unproven rail.
2. **Trinks header screenshots (Gate 2) before finalizing the Trinks adapter.** The adapter's column map is UNVERIFIED on three points (última visita as column; package join key; value vs sessions — §9). Twenty minutes in a Trinks trial settles it. Build the adapter interface first, freeze the column map only after the screenshots exist.

Also cheap and early: the Avec token pull (reports 0031/0129/0063/0006, 15 minutes) freezes the Avec adapter spec even though Avec is a weeks-7–10 build.

## 0.4 What to ask the founder at session start

Open every fresh build session by asking for the current state of:

- **Asaas**: does her independent production account exist and is it 100% approved (Pix key requires prova de vida)? Sandbox accounts A and B created? Gate 1 result?
- **Meta**: Business Verification status of her entity; Tech Provider App Review status (Advanced Access to `whatsapp_business_messaging` + `whatsapp_business_management`); the two demo videos; Access Verification. This is a 3–6 week clock (§11) — it must already be running.
- **CNPJ**: SLU incorporation status (must exist before the first production split — §6, §20), CNAE 7490-1/04, municipality/ISS, contador engaged with escrituração completa from inception.
- **Lawyer artifacts**: LIA template + laser annex, DPA + service contract (mandate-to-split, merchant-of-record clauses), offer-page cancellation clause per TJDFT 2110685, state-registry approach — the five-item lawyer checklist of §24, reproduced in App C.
- **Access material**: Trinks trial credentials + header screenshots; Avec API token; domain + hosting accounts; Meta app credentials.

## 0.5 Standing engineering laws

These bind every line of code, every milestone, forever:

1. **Fail-closed gate.** The gate is 4 campaign preconditions (P1–P4) + 9 per-client checks (C1–C9) + 1 approval artifact (§10). If any precondition cannot be evaluated, the campaign is blocked; if any per-client check cannot be evaluated, the client is excluded. Missing data is a "no". This includes the state-registry check C6: if an applicable state's do-not-disturb list is not loaded, promotional sends to recipients attributed to that state are blocked — no warning mode.
2. **Append-only records.** Approval artifacts, consent records, suppression entries, send manifests, gate results: insert-only tables. Corrections are new rows, never mutations.
3. **Suppression is authoritative.** The suppression list overrides every source system. A re-imported CSV can never resurrect an opted-out client. No override switch exists.
4. **No client PII to any LLM, ever.** Hard rule in code review. No customer/client row reaches a model, including for copy generation or debugging.
5. **Idempotent external calls.** Every Meta and Asaas call carries an idempotency strategy and stores full request/response logs.
6. **Delivered, not sent.** All accounting, modeling, and reporting count delivered messages. 131049/130472 failures are expected and never retried.
7. **Owner-touch budget.** The owner does 8 things (§17), plus two standing micro-behaviors accepted at onboarding: (a) opening the WhatsApp Business app at least every 13 days; (b) the redemption tap — when a client presents a voucher, the receptionist taps "confirmar uso" (client's voucher screen or the salon's magic link). Any feature that adds an owner-side step beyond these is rejected by default; the burden of proof is on the feature, and the default answer is no.

---


# PART I — THE BUSINESS

## 1. THE BUSINESS IN ONE SENTENCE

**The sentence (locked, pt-BR — this is the pitch, verbatim, everywhere):**

> "Eu escaneio seu sistema de graça e te mostro quanto dinheiro está dormindo no seu salão. O raio-X completo custa R$490 e volta inteiro como crédito. Depois eu rodo suas campanhas pelo seu próprio WhatsApp — e só ganho 20% do que cair no seu Pix. Zero mensalidade, sempre."

### The thesis in one page

**What it is.** Caixa Cheia sells managed prepaid revenue campaigns to Brazilian beauty businesses, delivered over the salon's own WhatsApp number, and paid only by results. The salon exports its client list from the software it already uses; Caixa Cheia imports it through an agnostic, allowlist-only pipeline, runs a fail-closed eligibility gate, and — only after the owner approves the exact send manifest — sends one approved WhatsApp marketing template from the salon's own number (Meta Cloud API coexistence; the founder is her own Meta Tech Provider). The message links to an opaque offer page carrying a priced prepaid package with full CDC disclosures; payment is a Pix charge created via the salon's own Asaas account, with 20% split to the founder's independent Asaas account at settlement. A voucher is issued, the client books, and either redeems or is refunded — with the fee reversed symmetrically. There is no bot, no AI concierge, and no founder-side inbox: client replies land in the salon's own WhatsApp Business App, answered by the salon's own people, as always. Full architecture in §7; rails in §11–§13.

**Who runs it.** One founder — a 26-year-old Brazilian woman, non-technical — who builds and operates everything by directing an AI coding tool (Claude Code). Zero employees at start; the first hire is a part-time ops VA around month 18 at the earliest. The design goal is a real, calm, one-person company with high personal net income: the honest month-24 target is ~R$45–55k/month personal net (see §21 for the arithmetic and what R$150k/month would actually require — a month-36–48 outcome contingent on specific proofs, not a plan).

**What the salon does (the owner budget, stated up front).** The owner does 8 things, plus two standing micro-behaviors accepted at onboarding: (a) open the WhatsApp Business app at least every 13 days; (b) the redemption tap — when a client presents a voucher, the receptionist taps "confirmar uso" (on the client's voucher screen or via the salon's magic link). Founder-side weekly reconciliation chases unredeemed and expiring vouchers. The full 8-touch list lives in §17; everything else is the founder's job.

**Why paid-only-on-results wins in this market.** Brazilian salons run 10–18% net margins and have been burned by every fixed-cost marketing product on the shelf: agency retainers of R$1,000–5,000/month, message-pack add-ons, R$99/month blast tools, R$2,997–4,797 one-time mentorias — all charged whether or not a single real lands in the till. In a market where the median owner's working capital is one bad month deep, "zero mensalidade, sempre" is not a discount posture; it is the only pricing that transfers execution risk to the party with the software, the copy, and the attribution machinery. And it is only offerable by someone who can *prove* attribution mechanically: because every campaign payment flows through a charge the system created, with the fee split at the Pix settlement itself, there is no reconciliation fight, no "that client would have come back anyway" invoice dispute, no chasing. The fee takes itself, only when money actually lands in the salon's Pix, and reverses itself when money is refunded. No competitor in Brazil sells this commercial model (see §4); several sell the underlying feature.

**The identity.** Caixa Cheia is not a "win-back tool." It is a **revenue-campaign engine where win-back is the audition and active-base campaigns are the business.** Win-back — messaging lapsed clients with a prepaid offer — is the lowest-risk, highest-defensibility first campaign for any account: the legal basis is strongest (prior relationship, see §5), the incrementality story is cleanest ("esse cliente não voltava"), and it proves the rails. But the durable revenue is in the salon's *active* base: package renewals, birthday cohorts, slow-day fills — unlocked per account only after two settled win-back campaigns, a GREEN WhatsApp quality rating, and an opt-out rate under 1% (Gate C, §3), capped at 2 active-base campaigns per location per quarter, all under one hard frequency ledger: maximum 1 marketing template per client per 60 days across all campaign types, with no override switch. The caps are not compliance decoration; they are what keeps the salon's own WhatsApp number — the asset the whole business rides on — healthy for years. The business model, in one line: earn the right to the active base by performing on the lapsed base, then run a small number of excellent campaigns per location forever.

**What the founder never does** (locked; full register in §6): no monthly subscription in any disguise, no holding client money, no bot, no cross-salon analytics on identifiable data, no health-data ingestion, no unofficial WhatsApp tools, no paid traffic, no salespeople. Every one of these refusals is load-bearing for the legal architecture (§5), the tax base (§20), or the one-person operating model (§18).

## 2. THE CUSTOMER AND THE MARKET

### 2.1 ICP definition

The customer is a **premium non-medical beauty business, barbershop, or laser/aesthetics clinic** that (a) runs on one of the five servable software systems and (b) has a client base worth campaigning against. Laser and aesthetics clinics are in scope from Day 1 under the agnostic-pipeline rule: the importer structurally drops every service, clinical, and free-text field before anything is written to the database, triggers are purely mathematical (e.g., `days_since_last_visit > 120`), and template copy never names a service — so the system cannot know and does not process what any client had done (mechanics in §9–§10; legal rationale in §5).

**Servable systems (verified):** Trinks, Avec, AppBarber/AppBeleza, Belasis, Fresha. Adapter build order: Trinks (launch) → Avec (weeks 7–10; chosen over Belasis on market size ~40k businesses plus its absorption of AZ4 and BeautyDate) → AppBarber → Fresha → Belasis. A new adapter is built when ≥25 qualified doors on that system appear in the Lista, or one 3+ location group demands it. Per-system export mechanics in §9. Booksy is *not* servable (no self-service export) but is a first-class prospecting directory (see 2.4).

Single premium salons are full customers, not a waitlist. But they are not the priority segment.

### 2.2 Why groups and franchisors are the priority segment

Three reasons, in descending order of force:

1. **One relationship = N locations.** A 5-location group signed once yields five campaign locations, five sets of safras, and one owner-approval relationship. Every unit-economics line in §21 scales on locations, not on sales conversations. The single scarcest resource in a one-person company is founder attention per relationship; groups multiply the denominator.
2. **Sell to whoever controls the software.** The eligibility question is never "does this salon want campaigns?" — it is "who decided which management system this salon runs, and who owns the client data?" For owner-operated groups that is the owner. For franchise networks it is usually the **franchisor**: Trinks itself sells a dedicated "Redes e Franquias" product and its published reference contacts are network-level executives — direct evidence that in this industry, software is a headquarters decision. One franchisor relationship can open dozens of doors that could never be sold one by one.
3. **The COF is a cheap, high-value research instrument.** Brazilian franchisors must issue a Circular de Oferta de Franquia to prospective franchisees, and the COF discloses whether the management software is mandated and who owns the client data — exactly the two facts that determine whether the sale happens at HQ or at the unit. A COF is obtainable free by posing as a prospective franchisee. Before pitching any franchisor on the named-targets list, pull its COF. [OPEN] COF terms on data/software control per named franchisor — to be resolved during the Lista build (§23 register).

### 2.3 The honest market size

The headline "1.3 million beauty businesses in Brazil" is noise: 94% of 2025's new beauty businesses are MEI — solo professionals with no exportable client database and no campaign budget. The premium universe that can actually be served is **low thousands**, best proxied by:

| Proxy | Number | Caveat |
|---|---|---|
| Salons with 20+ employees (CNAE 9602-5/01) | **1,661** | Dated — likely 2017–2020 vintage. [OPEN] Re-pull current count before any external use. |
| Beauty EPPs formalized in 2025 alone | **1,672** | Formation-rate signal, not a stock count. |
| Multi-unit share of the premium universe | **unpublished by anybody** | The census must be hand-built — hence A Lista. |

This smallness is a feature, not a flaw, for a one-person business: at ~70 owner relationships and ~100–160 locations by month 24 (§21), the addressable market never needs to be large — it needs to be *enumerable*. It is.

**Benchmarks that frame the pricing defense (§3):** premium salon monthly revenue runs **R$10–50k**; marketing-budget norms are **5–10% of revenue** in growth mode and **2–5%** for consolidated businesses; Trinks plans price at **R$76–110/mo** (5+ units "sob consulta"). Against those norms, a R$490 one-time credited audit and a success-only 20% fee sit inside what the segment already spends — with none of it fixed.

### 2.4 A Lista — the named-account census as the market instrument

Because no published dataset answers "which premium multi-unit beauty businesses run which software," the market instrument is a hand-built named-account census: **A Lista**. It doubles as the CRM (screen spec in §15) and as the adapter-prioritization signal (§2.1 threshold). The enumeration recipes below are verified working:

| Recipe | What it yields |
|---|---|
| Google `site:trinks.com` | Parseable public booking profiles in the format `Name - Category - Neighborhood - City`. A public booking page on trinks.com **is** the software signal — no guessing which system a prospect runs. |
| Google `site:trinks.com "unidade"` (variants: `"un."`, `"filial"`, `"- loja"`, mall names) | A **multi-unit detector**: surfaces Trinks-hosted brands with more than one location. |
| Booksy city directories | Hard counts with pagination and swappable numeric city IDs (São Paulo: 898 barbershops, 526 estética, 424 esteticistas). Prospecting only — Booksy accounts are not servable (§9). |
| Brand unit-locator pages | Authoritative per-brand location counts (can undercount — cross-check). |
| Trinks' own testimonial pages | A pre-qualified multi-unit lead list published by the incumbent itself. |
| Salão99 shutdown (dead 30/05) | Refugees migrating to Trinks/Gendo = a live, time-boxed prospect list. |

The census is a job of **days, not weeks**. It is gated by a pre-test:

> **3-day pre-test (SP + Rio "unidade" sweep):** if the sweep surfaces **≥15 owner-operated 2–8-unit brands**, the group-priority model holds. If it surfaces **<8**, re-base the segment strategy before the Beauty Fair. (Gate 3 in §23.)

### 2.5 Named targets

Verified named accounts, split by who signs:

| Target | Units | Type | Note |
|---|---|---|---|
| Laces and Hair | 9 | Owner-operated group | Sell to the owner |
| Studio W | 5 | Owner-operated group | Sell to the owner |
| Marcos Proença | 2 | Owner-operated group | |
| Antony Beauty Center | 2+ | Owner-operated group | |
| Fast Escova | 300+ | Franchisor | Sell to HQ; pull COF first |
| BR Barbearia | 52 | Franchisor | Sell to HQ; pull COF first |
| Jacques Janine | 50 | Franchisor | Sell to HQ; pull COF first |
| Turquesa Esmalteria | 53 | Franchisor | Sell to HQ; pull COF first |
| Esmalteria Nacional | 30+ | Franchisor | Sell to HQ; pull COF first |
| Confraria da Barba | 14+ | Franchisor | Sell to HQ; pull COF first |
| Beleza Natural | 48 | Company-owned network | Single HQ decision, no COF needed |
| Espaçolaser | 808 | Laser — franchised + owned hybrid | **Now in scope** under Option B (§1, §5). Data/software control varies across the hybrid network — the COF check is mandatory before any approach. |

Espaçolaser deserves the explicit flag: previously excluded as a laser business, it enters scope under the agnostic-pipeline rule, and at 808 units it is by far the largest single name on the list — but it is also the one where the COF check (who owns client data, whether software is mandated, franchised vs. owned unit split) matters most before a single conversation.

### 2.6 Beauty Fair, September 2026 — the forcing function

**Verified facts:** Beauty Fair runs **5–8 September 2026 at Expo Center Norte, São Paulo**. A professional badge is **free** with proof of activity (CNPJ or beauty-course certificate), grants access to the **extra business day on September 4**, and is approved within ≤3 business days. Public (non-professional) tiers: R$50 until 31/07, R$150 until 30/08, R$200 after / on-site.

**Registration urgency:** register **immediately** — the professional badge is free but the fallback R$50 public tier dies **31 July 2026**. Registration is a Week-1 checklist item (§24); the fair-week execution plan (named-target schedule from A Lista, scan-on-the-spot, printed anonymized Raio-X samples, target of 25 audit conversations and 10 paid audits) lives in §22.

## 3. THE OFFER LADDER AND PRICING

The ladder has exactly three rungs, and the only door is the free one.

### 3.1 Rung 1 — the free scan (the only acquisition door)

The owner sends two export files over one WhatsApp conversation; the system returns **four numbers**: total clients, lapsed clients, contactable clients, eligible clients (definitions and gate mechanics in §10; the scan flow screen is specced in §15). No charge, no signup, no login, no commitment. There is no other acquisition motion: no paid traffic, no cold outbound product, no salespeople (locked, §6). The scan is cheap to deliver (minutes of founder time), impossible to argue with (it is the salon's own data), and it sets up the audit as the obvious next question: *how much money is that, exactly?*

### 3.2 Rung 2 — Raio-X do Caixa (R$490 / R$990, 100% credited)

The full audit answers that question: how much money is sleeping in the salon's system — lapsed-client revenue potential plus unconsumed prepaid package balances (audit content and the locked accounting language are specced in §19; note the Trinks caveat that its package report shows *active unconsumed balances only*).

**Mechanics (locked):**

| Term | Value |
|---|---|
| Price, single site | **R$490**, one-time |
| Price, group | **R$990** per group, up to 8 locations |
| Crediting | **100% credited** against the first success fees |
| Validity | 12 months |
| Refund symmetry | If a fee that consumed audit credit is reversed by a refund, the credit is **restored** |
| Repeat charging | Never charged twice; regenerations free |
| Payment | Pix charge to the **founder's own** Asaas account — her own product, no split (§12) |
| Design partners | The audit may be **comped (R$0, founder discretion)** but is **always generated** — no salon reaches campaign #1 without a Raio-X |

**Framing (must be used in all sales conversations): it is a deposit, not a price.** The salon is not buying a report; it is depositing R$490 against campaign fees it will owe only on results. If campaigns never run or never settle, the salon bought a professional audit at a fraction of market rates (agency diagnostics and mentorias run R$2,997–4,797); if they do settle, the audit was free. Either branch is honest, and both are said out loud. The audit exists for three business reasons: it qualifies serious owners before the founder spends onboarding hours; it puts cash in the business during the build months (§21); and it converts the scan's four numbers into a named, itemized amount the owner cannot unsee.

### 3.3 Rung 3 — the 20% settled-net success fee

**The fee (locked): 20% of settled `netValue`, refund-reversed, success-only, identical for win-back and active-base campaigns.** No monthly subscription, retainer, minimum, or maintenance fee, ever, in any disguise.

Precision matters here because the fee computes on the Asaas **net**: a R$900 Pix charge at the standard R$1.99 Pix-in fee settles at R$898.01, and the split is **R$179.60, not R$180.00** (fees are read live via the Asaas fees endpoint and never hardcoded — see §12). Prose in this document uses R$180 as the round illustration; the ledger uses centavos. When a payment is refunded, the fee reverses with it — fully on full refunds, pro-rata on partial refunds (the pro-rata engine is core build, §12). A documented **fallback fee of 10% exists as a founder-only lever** — never offered proactively, never printed on any sales surface.

### 3.4 THE MARGIN GATE — pricing defense built into the product

The margin gate is the answer to the only hard pricing objection ("20% é muito"), and it is implemented as software, not as a talking point: **the system refuses to propose any campaign whose package math leaves the salon under 15% net** after professional commission, insumos, taxes, the Pix fee, and the 20% fee (the P2 margin precondition — formula and insumo bands in §10).

**Reference math — R$900 package, 40% commission, medium-insumo service:**

| Line | Amount |
|---|---|
| Package price (gross) | R$900 |
| Professional commission (40%) | −R$360 |
| Insumos (13%) | −R$117 |
| Asaas Pix fee | −R$2 |
| Simples Nacional (~8% of gross) | −R$72 |
| Caixa Cheia fee (20%) | −R$180 |
| **Salon keeps** | **≈R$169 ≈ 18.8% net** |

**The locked sales line (verbatim, pt-BR):** "desse pacote, sobra R$169 pra você e R$180 pra mim — mas esse cliente não voltava."

The math **breaks at ~50% commission or on high-insumo services** — and when it breaks, the gate blocks the campaign. This is deliberately a *refusal* the founder sells: every incumbent and agency will happily run a campaign that loses the salon money, because they are paid either way. Caixa Cheia is the only vendor whose software says "não" to a bad package — because on a success fee, a campaign that hurts the salon eventually hurts her. The refusal is the trust product.

Package economics are captured in a **3-question package-design step** before any campaign is proposed: (1) professional commission %, (2) insumo class, (3) package price. Three questions, gate math visible, pass/fail with the numbers shown (builder screen in §15). **R$900 is the default ticket** — consistent with premium service benchmarks (premium color R$250–450, balayage R$600–1,500) and the economics model in §21.

### 3.5 Campaign types, Gate C, and the frequency ledger

All campaign types run on the same rails (same gate, same approval artifact, same fee, same margin gate):

| Type | Availability | Notes |
|---|---|---|
| **Win-back** (lapsed clients) | First 2 campaigns per account — the audition | Strongest legal basis (§5), cleanest incrementality story |
| **Package renewals** | Gate C only | Renewal offer to clients with expiring/consumed balances |
| **Birthday cohorts** | Gate C only | Month-of-birthday segment |
| **Slow-day fills** | Gate C only | Capacity-targeted offers |

**Gate C — per-account unlock conditions for active-base campaigns (all three required):**
1. **2 settled win-back campaigns** on that account;
2. **WABA quality rating GREEN** on the salon's number;
3. **Opt-out rate <1%** (rolling, per campaign) across the account's campaigns — any campaign at ≥1% makes the business Gate-C ineligible (quality ladder in §11).

**Caps (locked, no override):** maximum **2 active-base campaigns per location per quarter**, and a hard **frequency ledger: max 1 marketing template per client per 60 days across ALL campaign types** — keyed on the phone and spanning all businesses of the same group — enforced in the eligibility gate (check C8, §10), with no override switch anywhere in the product.

### 3.6 Pricing defense — the objections, pre-answered

**"20% é muito."** Three answers, in order:

1. **Incrementality.** The fee applies only to revenue the campaign provably caused — clients the salon's own data says had lapsed, paying through a charge the campaign created. The benchmark performance-pricing ceiling in Brazilian marketing is 5–10% of *attributed* revenue precisely because attribution is normally contestable; here it is mechanical (Pix split at source), which is what makes 20%-of-actually-settled honest where 10%-of-claimed is not. "Esse cliente não voltava" is the whole argument.
2. **The split of the upside (DERIVED).** On the reference R$900 package, the salon's incremental contribution after commission, insumos, tax, and Pix fee — before her fee — is ≈R$349. Her R$180 is ≈51% of that incremental contribution; the salon keeps ≈49% (R$169) of money that did not exist before the campaign, at zero fixed cost and near-zero labour. She takes half the upside she creates and none of the downside.
3. **The gate.** Where the split would leave the salon thin, the software refuses the campaign (§3.4). The 20% never applies to a package where it doesn't work.

**"Mas eu pago imposto sobre os R$900 inteiros — sua taxa não me dá nenhum alívio fiscal."** Pre-answer this honestly, always (facts per §20): correct — the salon's receita bruta is the full R$900 (SC Cosit 143/2021; commissions are not deductible in the Simples), her fee gives the salon zero tax relief, and the true cost of the 20% is therefore ≈21.6% of gross. That is exactly why the reference math table (§3.4) charges Simples on the full gross *before* showing the salon its R$169 — the margin gate already prices the tax honesty in. Never claim the split avoids bitributação or defers tax (the claim circulating in PSP marketing is wrong); never imply any tax benefit. The pitch survives the honest number; that is the point of the gate.

**"E a mensalidade escondida?"** There is none, ever, in any disguise (locked, §6). The only other money that moves: WhatsApp message costs (~R$61 per 180-message campaign) are a transparent pass-through the salon pays Meta directly — the founder earns nothing on messages (§11) — and the one-time, fully-credited audit (§3.2).

## 4. COMPETITIVE POSITION

### 4.1 The finding: the feature is commoditized; the commercial model is unoccupied

Every major Brazilian salon-software incumbent already ships a lapsed-client feature. And yet: **zero Brazilian players sell salon win-back on a success fee or revenue share** — a verified negative across ~35 Portuguese-language queries. The competition is real at the feature layer and absent at the model layer. Caixa Cheia's position is not "we detect lapsed clients better"; it is "we are the only ones paid the way you'd want to pay."

### 4.2 The field

| Player | What they ship | Model | Why it isn't this business |
|---|---|---|---|
| **Trinks — "Convite de Retorno"** + "Relatório de Retorno" (since 03/2024) | Auto WhatsApp N days after visit; one-click WhatsApp from the lapsed report | Prepaid message packs | Sends from **Trinks' number, not the salon's** — the thread, the reply, and the relationship accrue to Trinks. Known defect: duplicate client records sharing one phone get double-messaged. **Strategic note: Trinks is a Grupo Stone company** — payments capital, and therefore the incumbent most structurally able to copy the Pix-split model. This argues for pace (§4.5). |
| **Gendo** | Abandonment report + automated WhatsApp/SMS package promos | Subscription | Detection + blast, no offer/payment/attribution layer |
| **AppBarber** | "Dias Sem Vir", "Assiduidade", lapsed report with per-row WhatsApp + "Enviar Para Todos" | Subscription | Puts the labour on the owner; no money in the message |
| **Booksy Brasil** | Unlimited blasts included | R$99,99/mo | Blast tool; no segmentation judgment, no payment, no attribution |
| **Avec IA** | Reactivation invites | Add-on | Feature inside a suite, not a managed campaign with a checkout |
| **Flly** | **Closest competitor:** managed done-for-you reactivation on the salon's **own** number; claims ~"1 in 4 reactivated", ~R$3,200/mo recovered | **~R$297/mo, no success fee** | The right service shape with the wrong pricing — "the only thing separating them from her is a pricing page." Watch closely. |
| **Reativa Clientes** | Lapsed detection (R$97/mo); owner sends manually, one by one | Subscription | Market proof that detection alone doesn't solve execution |
| **ReativaPlus** | Setup + monthly; recommends a burner chip | Subscription | Burner-chip advice = ban risk and illegitimacy (§6 refusal) |
| Beauty Core, ReativaZap, @deboracamposmkt (solo, RJ) | Assorted reactivation offers | Mixed | Small, no rails |
| **WinbackEngine (US)** | Multi-location win-back, human phone agents | **20% of net recovered, success-only, $1,000 refundable pilot** | **The model, validated in the US** — down to the refundable deposit that mirrors the Raio-X credit. Doesn't port: phone agents don't work in Brazil, WhatsApp is the native channel. Caixa Cheia is the WhatsApp-native, Pix-settled port of a proven commercial model. |
| Updent (dental, PT/ES) | Vertical reactivation | — | Adjacent-vertical validation |

### 4.3 The DIY objection, quantified and answered

The owner can do this herself, cheaply: SocialHub at R$99/mo per 1k notifications; Zenvia at R$0.47–0.55 per message; Booksy blasts free in plan. On cost, the objection is strong — ~R$61 of Meta fees per campaign is not the moat. On **labour and judgment**, it collapses: someone must pull and dedupe the export, define the segment, design a package that survives the margin math, write copy that clears Meta's template review, handle 131049/131050-class delivery failures, work the suppression list, take payment, track redemptions, and compute refunds. That is why Reativa Clientes' R$97/mo detection tool leaves owners sending messages one by one — detection was never the bottleneck; execution is.

Therefore the pitch is **"eu faço", never "eu encontrei"**. Caixa Cheia does not sell the list of lapsed clients (the salon's own software shows that for free); it sells segmentation judgment, offer design, copy, somebody working the campaign end to end — plus the only **hard attribution** in the market: the Pix split at source, which ends the "would they have come back anyway?" argument before it starts, because the fee only ever attaches to money that arrived through the campaign's own charge.

### 4.4 The five-point wedge

1. **Money in the message.** A priced offer + Pix checkout + settled-only fee, in the client's hand. Every competitor stops at the message; none of them takes payment.
2. **The salon's own number and thread.** Versus Trinks above all: replies, history, and the relationship stay in the salon's WhatsApp, forever.
3. **Prepaid-balance suppression.** The gate excludes clients who already hold unconsumed package balances (the CPC 47-sourced rule — gate check C4, §10) — nobody else even looks. Messaging a client to sell what they already paid for is the single most trust-destroying thing a salon can do; not doing it is a feature.
4. **Consent/LGPD defensibility as a sellable feature.** The per-send approval artifact, the LIA, the suppression architecture, the state-registry checks (§5, §14, §16) — packaged as the salon's own litigation defense, not as the founder's overhead.
5. **Mechanical attribution.** The split executes at settlement. No reports to trust, no invoices to dispute, no reconciliation meeting.

### 4.5 Why pace beats breadth

The moat is thin at the feature layer and structural at the model layer — and the one incumbent with the payments capital to copy the model (Trinks/Grupo Stone) already owns distribution to ~44k businesses. The correct response is not to out-build breadth (more adapters, more campaign types, more surfaces) but to out-run on the things an incumbent cannot copy quickly: named-account depth (A Lista, §2.4), signed groups and franchisors (one HQ relationship at a time, §2.2), per-account WABA health and consent capital accumulated over months (§11, §14), and a September 2026 fair-cohort head start (§22). Every week of the 90-day plan (§22) is sequenced against this clock. Breadth is a month-12 problem; by then the defensibility must already be in the relationships and the records vault, not the feature list.


# PART II — THE RULES

This part is the operating law of Caixa Cheia. Nothing in Part III (the build) or Part IV (operations) may contradict it. Where an engineering choice and a rule in this part collide, the rule wins and the engineering changes.

## 5. Legal Architecture

Caixa Cheia sends marketing messages over WhatsApp, on behalf of salons, to the salons' own past clients, and takes payment for the salon's services through a Pix charge with a 20% split. Four bodies of law govern that sentence: LGPD (lawful basis, operator status, sensitive data), state do-not-disturb statutes, the CDC (distance selling, packages, refunds), and Meta's platform policy — a fourth legal system with its own, faster enforcement arm. This section states each position, why it is defensible, and which design features are load-bearing (never removable — see §6).

Nothing here is legal advice; the artifacts in Appendix C go to a Brazilian lawyer for sign-off in week 1 (engagement scope in Appendix C; checklist in §24).

### 5.1 Lawful basis: legitimate interest, honestly argued

**Verdict.** The lawful basis to start operating — before any client has ticked a consent box — is **legitimate interest**: LGPD Art. 7º IX, executed through Art. 10º I ("apoio e promoção de atividades do controlador") and Art. 10º II (benefit to the data subject and their legítimas expectativas). The controller is the **salon**, not Caixa Cheia (see §5.3). The interest is the salon promoting its own services to its own existing clients, over the channel those clients already use with the salon, with a free in-message way out.

**The three anchors.** This is not a creative reading; it rests on three published Brazilian sources:

1. **ANPD Legitimate Interest Guide, Example 5** — a discount promotion sent to a pre-existing customer base via direct messaging, with an unsubscribe mechanism inside the message, assessed as a valid LI use case precisely because of the **relação prévia** (prior relationship). This is, almost feature for feature, the win-back campaign.
2. **ANPD Nota Técnica 2/2024, §5.55** — LI was *refused* for "oferta ativa" to people **without** a prior relationship. Read a contrario, the prior relationship is the distinguishing factor the ANPD itself named. Caixa Cheia's eligibility gate makes the prior relationship a machine-checked precondition, not an assumption.
3. **Data Privacy Brasil, catalog item C.7.1.1** — a customer database repurposed for direct marketing to those same customers, assessed positively, with a **12-month window** as the reference for how far back "customer" reaches. This anchor is the direct source of the 12-month hard ceiling in §5.1.3.

**The honest counterweights.** The LIA must state these, not bury them: NT 2/2024 §5.32 quotes ICO language preferring consent for direct marketing; the LGPD has no equivalent of GDPR Recital 47 (which expressly names direct marketing as a possible legitimate interest), so the argument rests on ANPD examples, not statutory text; and the Brazilian market posture is consent-first. These counterweights are why consent capture (§5.2) runs from day one as the destination basis, with LI as the launch basis — the **dual-track** design.

**The LIA is mandatory in practice, per salon, and it is the salon's document.** Formally the ANPD calls the LIA a "boa prática", but Art. 37 (compulsory processing record, expressly required for LI) and Art. 42 §2 (judicial reversal of the burden of proof) convert it into a practical obligation: a salon sued over a message must produce the balancing analysis, or LI collapses into assertion. Therefore: one LIA **per salon**, executed **before** that salon's first campaign, adopted and signed by the **salon owner** as controller. Caixa Cheia authors the template (Appendix C.1) and pre-fills it from the salon's actual data (base size, cadence tier, segment rule); the owner reviews and adopts it. It lives in the records vault (§16), versioned. Laser/aesthetics clinics get a mandatory annex (§5.4).

#### 5.1.2 The eligibility gate, stated in legal terms

The gate specified operationally in §10 is the legal architecture compiled into code. It is structured as **four campaign preconditions (P1–P4), nine per-client checks (C1–C9), and one approval artifact** — the identifiers below are the canonical ones used in §10 (normative spec), §15.5 (UI view), and §8 (`manifest_entries.checks` JSON keys). The gate is **fail-closed**: any check that cannot be evaluated (missing field, unloaded registry list, unverifiable date) is a fail, and the number is excluded.

**Campaign preconditions** (run once per campaign, all must pass before the manifest is built):

| Id | Precondition | Legal function |
|---|---|---|
| P1 | `docs_current` — signed contract + DPA + adopted LIA (current version) + current privacy notice on file for this business | Art. 37 record; Art. 42 §2 proof |
| P2 | `margin_gate` — the package math leaves the salon ≥15% net (see §3 and §10) | Not an LGPD item, but the gate is one pipeline: an economically abusive offer is a reputational and CDC risk |
| P3 | `copy_lint` — the template copy names **no service**, generic by construction (versioned lint wordlist) | Sensitive-data firewall (§5.4) and vida-sexual-adjacent categories (e.g., intimate waxing) |
| P4 | `channel_health` — the WABA quality ladder (§5.7, §11) permits sending | Meta's parallel legal system: quality loss kills the channel faster than any Procon |

**Per-client checks** (run per manifest row). A client's number may be included **only if** all nine pass; C2 carries the two lawful-basis branches:

| Id | Check | Legal function |
|---|---|---|
| C1 | `own_client` — the row originates from **this** business's own import (at least one recorded visit) | The relação prévia — the fact that distinguishes Example 5 from NT 2/2024 §5.55 |
| C2 | `lawful_basis` — **Branch A**: a consent record meeting the §5.2 capture spec (granted, not revoked) covering WhatsApp marketing from this salon; **or Branch B**: legitimate interest, with `last_visit` inside the business's cadence window (§5.1.3) and in no case older than **360 days** | Art. 7º I / Art. 8º (Branch A); Art. 7º IX / Art. 10º and legítimas expectativas with the 12-month ceiling per C.7.1.1 (Branch B) |
| C3 | `no_clinical_data` — structural assertion from the import's allowlist receipt: no clinical or service-descriptive field was ever ingested for this client (Option B — see §5.4 and §9) | Keeps the processing outside Art. 11 entirely |
| C4 | `package_balance` — CPC-47 exclusion: the client holds no unconsumed prepaid package or credit; if the business attests it sells no packages, the check passes with the attestation reference | CDC posture (§5.6): never solicit new prepaid value from a consumer the salon still owes services to |
| C5 | `suppression` — not on the suppression list (including global rows); anti-resurrection: suppression survives re-imports | Art. 18 (opposition/revocation) honored; the one variable that flips case-law outcomes (§5.7) |
| C6 | `state_registry` — not registered on an applicable state do-not-disturb list; **fail-closed** (§5.5) | State statutes reach WhatsApp and bind salons; SP registry is an absolute exclusion |
| C7 | `not_minor` — birthdate present → ≥18; birthdate absent → covered by the owner attestation "imported base is the adult client base", noted in the LIA | Art. 14 (consent-of-parent regime; marketing to minors is out of scope, full stop) |
| C8 | `frequency_60d` — no marketing template to this phone_hash in the last 60 days, across **all** businesses sharing the same parent_business_id (group scope — the only permitted cross-business lookup); no override exists | Proportionality/minimization limb of the LIA; avoids the "insistence" aggravator (§5.7) |
| C9 | `contactable` — valid E.164 number, deduplicated at import | Data quality and minimization: no misdirected processing |

**Approval artifact** (final precondition to send): a dated owner approval capturing the segment rule, recipient count, exact message text, template_id + template version, and the owner's reply (§5.3). No campaign transitions to `approved` without it. Approval validity: **7 days** — an expired approval requires re-approval. Legal function: preserves operator status (§5.3); documents the Art. 10 controller decision.

C5 and C8 re-run at send time, not only at manifest time — the suppression list is authoritative over every source system (constitution #15). Checks C3, P3, and the allowlist importer are **structural**: they are not per-send evaluations but properties of the pipeline that make certain violations impossible rather than merely prohibited.

#### 5.1.3 The 12-month ceiling and the cadence tiers

**Ceiling: no message under legitimate interest to anyone whose last visit is more than 360 days old. Hard, no override.** The only supportive worked example with a time bound (Data Privacy Brasil C.7.1.1) uses "último ano"; past twelve months, the legítimas-expectativas limb of Art. 10º II becomes an argument to invent rather than cite, and the business declines to be the test case. The build window is 90–360 days (also matching the Trinks report's one-year filter cap — see §9).

**Cadence tiers narrow the window by business type**, because "expectation" is empirical: a barbershop client returns monthly, a colorist's client quarterly, a laser client per protocol. Defaults — **barbershop 45 days, salon 90 days, laser/aesthetics 120 days** — owner-adjustable within a 30–180 day band, configured at the **business** level (never derived from per-client service data, which is never ingested). A client is "lapsed" when `days_since_last_visit` exceeds the tier; they remain contactable under LI until day 360. The tier is the LIA's proportionality evidence: contact happens when absence deviates from that business type's normal rhythm, not opportunistically.

### 5.2 The consent program

Legitimate interest is the launch basis; **consent is the destination basis**. Every campaign, every visit, and the QR card at reception (see §14) progressively converts the base. Because a salon's clients cycle through in roughly one service cycle, consent can rebuild a sendable base in weeks, not years. LI and consent tracks run **concurrently**: a valid consent record moves a client to Branch A; absence of one leaves them on Branch B if they qualify.

**Capture spec** (mechanics in §14; legal requirements here):

- **Unticked, unbundled checkbox.** Never pre-checked, never merged with terms-of-service acceptance, never a condition of booking.
- **Never conditioned on a discount or benefit.** This is the **Febrafar trap**: the ANPD's Febrafar proceeding and the Procon-MG fine pattern (R$8.4M+) target exactly the "give consent, get the discount" mechanic, which voids the "free" element of Art. 5º XII consent. The offer page, the voucher, and the checkout must work identically whether or not the box is ticked, and the copy says so explicitly.
- **Art. 9 notice before the tick** — who processes, for what, and how to leave — via the privacy-notice link/QR adjacent to the checkbox.
- **Specific scope.** "Receber novidades" does **not** cover discount offers: Art. 8 §4 voids generic authorizations. The locked text below names promotions and offers expressly.
- **Revocable free of charge**, by replying SAIR — the same channel the message arrives on (and see §11 for the full opt-out matcher).

**Locked consent text (pt-BR, verbatim — the only approved string; the salon's name and CNPJ are the only substitutions):**

> ☐ Autorizo o [SALÃO] (CNPJ …) a me enviar mensagens por WhatsApp, no número que informei, com promoções, ofertas e novidades sobre seus serviços. Posso cancelar quando quiser, de graça, respondendo SAIR. Não autorizar não muda em nada o meu atendimento.
>
> Saiba como usamos seus dados: [QR/link]

**Metadata stored with every capture** (schema in Appendix C.4): the exact displayed string and its version identifier (for native captures), timestamp, capture source (`qr_card` / `offer_page` / `checkout` / `fresha_import` / `observacao_marker` / `manual` — the QR card resolves to the consent page at `/c/{token}` and is recorded as `qr_card`), evidence class (`native_capture` / `imported_boolean` / `marker`), the phone number as stated by the client, and business ID (staff identifier and IP hash where available). **Refusals are recorded too** — a dated `refused` record is Art. 42 §2 evidence that the choice was real, and it feeds the suppression logic (a refusal is not an opt-out from LI, but a second solicitation shortly after a refusal is an aggravator; the gate's 60-day ledger covers this).

**Imported consent.** Only Fresha exports carry structured consent columns ("Accepts marketing" / "Accepts SMS marketing" — booleans, weaker than the full tuple). "Accepts marketing" TRUE imports as consent evidence with source `fresha_import` and evidence class `imported_boolean`; FALSE imports as a **refused record — a Branch-A exclusion, never a suppression entry** (the client may still qualify under Branch B). The industry norm elsewhere is a URL pasted into a free-text `Observação` field; the importer may parse Observação for consent markers **going forward** (source `observacao_marker`, evidence class `marker`), but retrofitting meaning onto old tags is not Art. 8-valid evidence and is not attempted.

### 5.3 Operator posture: how Caixa Cheia stays an operador

**The position.** For every salon, the salon is the **controller** (controlador) and Caixa Cheia is the **operator** (operadora): it processes the salon's client data on the salon's behalf, for the salon's purpose, under the salon's decisions. This is not a label but a set of facts that must remain true, and the product is built so they cannot quietly stop being true.

**Why per-send owner approval is the preserving fact.** The ANPD Guia de Agentes de Tratamento, Example 5, analyzes a marketing agency that proposes targeting and defines channels and tools — and concludes it **remains an operator** as long as the client takes the final decision. Caixa Cheia proposes more than most agencies (segment, copy, offer math), so the final decision must be unmistakably the salon's: before any send, the owner receives the **manifest** — dated, with the named segment rule, recipient count, exact message text, and template_id + template version — as a utility template from the salon's own number, and replies "APROVO" (matched case-insensitively as an exact word, trimmed). That reply, captured through the messages webhook and timestamped against the manifest hash, is the approval artifact; it is valid for **7 days**, after which the campaign requires re-approval. **Never skipped, never batched, never inferred from a standing instruction** — a standing "always approve" would collapse the Example-5 distinction and is refused (§6.2).

**What converts her into a controller.** Processing for **her own purpose**: cross-salon analytics on identifiable data, building her own marketable audience, reusing one salon's client list to benefit another, training anything on client rows. All banned (constitution #10, #12). The one deliberately permitted future exception — aggregate benchmarking on anonymized data — requires separate papering and is by default not built. The TJPR decision RI 0006880-13 (R$2,000 damages plus deletion for third-party marketing reuse of personal data) is the fact pattern this ban exists to make impossible.

**Art. 42 liability map.** Art. 42 §1 I makes the operator **solidarily liable** when it breaches the LGPD or departs from the controller's *lawful* instructions. Two consequences: (a) executing a knowingly bad list — one that fails the gate — exposes Caixa Cheia personally even though the salon is the controller; the gate's **exclusion log** (every number excluded, with the failed check) and recorded refusals to run non-compliant campaigns are her personal shield; (b) an *unlawful* instruction from a salon ("send to this bought list", "message my competitor's clients") gives no safe harbor — it must be refused and the refusal logged. Art. 45 routes consumer-facing damages through the CDC's objective, solidary liability chain, which is a second, independent reason the salon-facing paper trail must be complete.

**DPA.** A data processing agreement is executed with each salon at onboarding (e-signed in the guided session, §17), covering at minimum: object, duration, nature and purpose of processing, data types, the parties' rights and duties, security measures, breach notification, deletion/return at termination, and **disclosed suboperators** — Meta/WhatsApp (message transport), the cloud host, and Asaas (payment-processing context). Clause list in Appendix C.2.

### 5.4 Sensitive data and Option B: the agnostic metadata pipeline

Laser and aesthetics clinics are in scope from day 1 (constitution #5) — a decision that is only lawful because of the pipeline design described here. This subsection is the full rationale; it is also the substance of the laser LIA annex and **lawyer engagement item #1**.

**Why Art. 11 must be avoided rather than satisfied.** Art. 11's list of lawful bases for sensitive data is **closed** and does **not include legitimate interest** — the ANPD is explicit. If any part of this processing involves health data, the LI architecture of §5.1 is unavailable for it. Worse, **Art. 11 §4 prohibits communication or shared use of health data between controllers for economic advantage** — and **consent does not cure it**: a salon handing Caixa Cheia records that constitute health data, for a revenue-generating campaign, sits inside that prohibition no matter what the client signed. The only sound position is structural: **the data that crosses the salon → Caixa Cheia boundary must not be health data at all.**

**The two cumulative limbs of Art. 11 §1.** Ordinary data is treated as sensitive under §1 only when the processing both (i) **reveals** sensitive data and (ii) is **capable of causing harm** to the data subject. Both limbs must be present. The pipeline is designed so the first limb fails by construction and the second has nothing to attach to.

**What crosses the boundary — and what never does.** The importer is an **allowlist** (mechanics in §9): the only fields written are client identity (external ID, name, phone, optional birthdate), visit dates and ticket values, package-balance numbers, and consent records. It **explicitly drops** `service_description`, `anamnese`, `prontuário`, `observações`, and any clinical, health, category, gender, or notes field **before write** — dropped column names and counts (never content) are logged as minimization evidence. Avec's client screens carry Anamnese and Prontuário tabs; those are never ingested from any system. Triggers are purely mathematical (`days_since_last_visit > 120` for the laser tier); cadence lives at business level. **Caixa Cheia cannot know, and does not process, what service any client received.** There is no inference step to challenge because the inputs for inference were destroyed at parse time.

**Why "client of a laser clinic" alone is defensibly ordinary.** The residual signal — this phone number belongs to a client of this business — is the same for a laser clinic as for a barbershop. That it is not health data rests on: the closed Art. 11 list; the absence of any ANPD definition of health data reaching "is a customer of an aesthetics business"; and the absence of any beauty-sector precedent to the contrary. Defensible position, **not** a safe harbor: no ANPD guidance or enforcement exists on the beauty sector at all, and the ANPD's 2026–27 priorities include health data — flagged, and exactly what the lawyer signs off on (the "client-status question", Appendix C.1).

**Generic copy completes the defense.** Two content rules close the loop: (a) the WhatsApp **template copy never names any service** — machine-enforced; this also protects categories adjacent to vida sexual (e.g., intimate waxing) at ordinary salons; (b) the **offer page** names the package the salon is selling — but that is **owner-authored commercial content**, the clinic's public menu item entered by the owner in the campaign builder, not derived from or joined to any client record. The recipient sees a generic message from a business they know, leading to a public offer; no message artifact reveals anything about their history.

**The enforcement analogue to avoid.** The ANPD's RaiaDrogasil sanctioning process targeted profiling built on sensitive purchase-history inference used to sell targeted advertising. That is the pattern the agnostic pipeline structurally forecloses: no purchase-history content is held, so no inference on it can occur.

### 5.5 State do-not-disturb registries

**These statutes reach WhatsApp and bind salons — not just telecoms.** Anatel's Não-Me-Perturbe is voice-only and telecoms-only, and compliance with it is **not a defense** to state-law claims (ADI 5962). The state registries are separate consumer-protection statutes enforced by Procons, and several expressly cover app messages.

| State | Instrument | Reaches WhatsApp? |
|---|---|---|
| SP | Lei 17.832/2023 arts. 127–129 (via Lei 17.334/2021) | **Yes** — "mensagens de aplicativos"; PROCON-SP FAQ names WhatsApp, Telegram, Signal |
| PR | Lei 22.130/2024 | **Yes** — aplicativos; fines R$900–R$12M reported |
| GO | state registry law | **Yes** — "mensagens" |
| SC | state registry law | **Yes** — "mensagens eletrônicas" |
| DF | district registry law | **Yes** — "mensagens" |
| RS | state registry law | **Yes** — generic "qualquer outro meio eletrônico"; R$10k/contact |
| ES, MS | state registry laws | No — voice only (explicit) |
| MG | state registry law | No for WhatsApp — SMS at most |

**São Paulo mechanics (the binding template, since launch is SP-centered):**

- Blocking takes effect on the **30th day** after the consumer registers — registry status is time-stamped, not boolean.
- **Art. 127 §3: solidary liability** for everyone in the sending chain, including contractors from any state — Caixa Cheia is personally inside this, independent of her LGPD operator posture.
- Fines per **CDC art. 57**. Enforcement is real: PROCON-SP levied R$366M across 399 proceedings, 2010–2024.
- **The Q17 rule (PROCON-SP FAQ): for a registered number, the existing-customer relationship permits relationship/post-sale contact ONLY — "Não poderá ser feita … qualquer oferta de novos produtos ou serviços."** No existing-customer exception for promotional content. Since every Caixa Cheia send is by definition an offer, **a number on the SP registry is an absolute exclusion** — no override, no "but they're a regular".

**Gate implementation (check C6):** the recipient's UF is attributed by phone DDD→UF mapping (an imprecision noted in the LIA); numbers are checked against the SP registry before every manifest, and against PR/GO/SC/DF/RS as their lists become obtainable. If an applicable state's list (SP first) is not loaded, **promotional sends to recipients attributed to that state are BLOCKED — fail-closed, no warning mode.** **[OPEN]** The supplier-side list-access mechanism is unresolved: PROCON-SP FAQ Q10 implies one exists, but whether it is a download, an API, or a formal request — and the equivalents in PR/GO/SC/DF/RS — must be resolved by the week-1 lawyer engagement (item #5) **before the first send** (timeline-compatible: first sends land in weeks 4–6). The lawyer may authorize a documented interim measure; until then, sends to those recipients stay blocked. Carried in the §23 register as REQUIRED-BEFORE-FIRST-SEND, owner = lawyer.

### 5.6 CDC: the package-selling law

The consumer buys a prepaid package from the **salon** (the salon is the seller of record — constitution #14), by a link sent to their phone. That makes it a distance sale with a prepaid balance, and four CDC doctrines shape the product:

**1) Art. 49 — 7-day withdrawal.** A sale closed by link is "fora do estabelecimento comercial": the client may withdraw within 7 days for a **full, immediate refund "a qualquer título"**, monetarily updated. Decreto 7.962/2013 art. 5 adds: disclose the withdrawal method, accept withdrawal through the same channel as the purchase, and instruct immediate payment reversal. Consequence: the offer page discloses the 7-day right, and the refund flow (see §12) supports full refund with automatic split reversal, initiated from the salon's account.

**2) Expiry and forfeiture.** A validity period is enforceable **only if prominently disclosed before purchase**. **Total forfeiture of unused value is void** (arts. 51 II/IV, 39 V) even after expiry: on cancellation the salon refunds the proportional unused value. A modest pre-disclosed administrative fee is tolerated; generic "operating costs" cannot be passed on.

**3) TJDFT Acórdão 2110685 (15/04/2026) — the disclosure rule that writes the offer page.** Used sessions may be re-priced at the avulso (single-session) rate on cancellation **only if** the avulso price **and the exact cancellation arithmetic** were disclosed in writing **before** purchase. This holding dictates the offer page's mandatory content (Appendix C.5): package price, sessions, validity, avulso per-session price, the cancellation math worked as a formula, and the salon's CNPJ (art. 42-A). An offer page missing any of these is blocked from publishing (see §13).

**4) Ten-year prescription.** Unused package credit prescribes under CC art. 205 — **10 years**, not the CDC's shorter windows: a balance sold in 2026 is a live claim into 2036. The **per-client redemption ledger** (§16) — every session redeemed, dated, against every voucher — is the salon's litigation defense file, maintained automatically and sold as a feature. It also makes the pro-rata refund engine computable: refund = paid − (sessions used × disclosed avulso rate), exactly as pre-disclosed. Partial, months-later refunds are the **normal case** for packages, not an edge case; the split-reversal arithmetic lives in §12.

### 5.7 Meta policy: the independent gate

Meta's Business Messaging Policy is a parallel legal system with faster, harsher enforcement than any Procon: template pausing in hours, number-quality demotion, and account loss. Three rules matter:

**Opt-in is a platform requirement regardless of LGPD.** Meta requires that the business received the person's number **and** opt-in permission for the message category. Satisfying the LGPD does not satisfy Meta; they are **two separate gates**. The prior-relationship + notice + free-exit package documented per salon is also the salon's Meta opt-in position; the consent program (§5.2) strengthens both gates at once. Suppression honors all three Meta paths — `user_preferences` webhook stop events, error 131050, and liberal free-text matching (SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA, plus profanity), with a WhatsApp block treated as opt-out (handbook in §11 and Appendix B).

**Quality is the business-ending risk.** LGPD fines arrive in years; a RED quality rating arrives in days and kills the channel for that salon — a pattern of them kills Caixa Cheia's Tech Provider standing. Template pausing (3h → 6h → disabled) is driven by blocks, reports, **mutes and archives** over a rolling 7 days. The frequency ledger (1 template/60 days), the two-campaign win-back audition before active-base unlock, the opt-out thresholds (≥1% flags the business and makes it Gate-C ineligible; ≥3% auto-pauses its new sends — ladder in §11), and template warming (§11) are primarily quality protections; their legal value is secondary.

**The case-law one-variable rule.** Brazilian courts treat the marketing message per se as lawful ("mero dissabor" line, including TJDFT Ac. 2005290 for messages specifically); awards of R$1,500–6,000 appear when **a documented stop was ignored** — a registry entry, a refusal, a Procon complaint. Existing-customer status is treated leniently (the TIM case), but leniency evaporates on opt-out. Known aggravators: night/weekend sends, multiple sending numbers, multi-channel pursuit, ignored complaints, insults. The design avoids every one **by construction**: one number (the salon's own), business-hours scheduling, one channel, human replies from the salon, authoritative suppression no re-import can resurrect, and the 60-day frequency cap with no override. For any future pleading or notice: do not cite CDC art. 39 III for messages (a free-sample remedy with zero message case law); the courts' actual bases are art. 6º VI, art. 39 caput/IV, and CF art. 5º X. The TJPR LGPD-grounded award for third-party marketing reuse (RI 0006880-13) is the standing reminder that the DPA and operator framing of §5.3 are load-bearing, not paperwork.

## 6. Locked Decisions and Refusals

### 6.1 The constitution

These sixteen decisions are final. No section of this document, no build shortcut, no customer request, and no future optimization may change them without a deliberate, documented re-decision by the founder with legal review where marked.

1. **Fee: 20% of settled `netValue`, refund-reversed, success-only** — identical for win-back and active-base. No monthly subscription, retainer, minimum, or maintenance fee, ever, in any disguise. A 10% fallback fee exists as a founder-only lever, never offered proactively.
2. **Margin gate:** no campaign is proposed whose package math leaves the salon under ~15% net after professional commission, insumos, taxes, Pix fee, and the 20% fee (3-question package-design step; reference math in §3).
3. **Raio-X do Caixa: R$490 single-site / R$990 per group (up to 8 locations), one-time, 100% credited against first success fees, 12-month validity, refund-symmetric credit restore.** Never charged twice; regenerations free. The free scan is the only acquisition door.
4. **Multi-system from the start.** Servable: Trinks, Avec, AppBarber/AppBeleza, Belasis, Fresha. Adapter order: Trinks → Avec → AppBarber → Fresha → Belasis. New-adapter threshold: ≥25 qualified doors on that system in the Lista, or one 3+ location group demanding it.
5. **Laser/aesthetics: Option B — included via the agnostic metadata pipeline** (§5.4). Importer drops all clinical/service fields pre-write; triggers purely mathematical; template copy never names a service; laser LIA annex; lawyer sign-off is checklist item #1.
6. **ICP:** premium non-medical beauty businesses + barbershops + laser/aesthetics clinics on servable systems. Multi-unit groups (2–8) and franchisors are the priority segment; single premium salons are full customers, not a waitlist.
7. **WhatsApp: founder is her own Meta Tech Provider, direct Cloud API, R$0 fixed per salon.** No BSP. Each salon = own client-owned business portfolio + one coexistence WABA in BRL; the salon pays Meta for messages directly (transparent pass-through).
8. **Payments: Asaas, Pix only.** Split via `walletId` + `percentualValue: 20` to the founder's own independent account. No subaccounts, no BaaS, no merchant-of-record, founder never holds client money, no escrow, no netting. Adding credit card is prohibited without new legal review.
9. **No bot, no AI concierge, no founder-side inbox.** Replies land in the salon's WhatsApp Business App. No client row ever reaches an LLM.
10. **No cross-salon analytics on identifiable data.** Aggregate benchmarking only on anonymized data, only if separately papered — default: don't build it.
11. **Operator posture:** the salon is the controller; founder is operador. The per-send owner-approval artifact is the preserving fact — never skipped, never batched away. The LIA is the salon's document.
12. **Rejected forever:** see the refusals table (§6.2).
13. **Entity: SLU, ME, Simples Nacional, incorporated before the first split.** CNAE 7490-1/04; municipality at/near the 2% ISS floor; escrituração contábil completa from day one; pró-labore at minimum wage in year 1 (Fator R); NFS-e to the salon only, LC 116 item 10.02/10.09, never 1.05/1.09.
14. **The salon is the seller.** Salon's CNPJ on checkout and receipts (CDC art. 42-A); founder's brand subordinate everywhere consumer-facing; refunds always originate from the salon's account.
15. **The suppression list is authoritative over every source system.** A re-imported CSV can never resurrect an opted-out client.
16. **Vouchers redeem only at the issuing salon/group.** Cross-salon redemption is prohibited forever (would create a payment arrangement / e-money).

### 6.2 The refusals

Each of these has been considered and rejected. The one-line reason is the permanent answer.

| Refused | Why |
|---|---|
| Distributor / channel-partner models | Adds a layer that owns her customer relationship and dilutes the only asset — direct trust with owners. |
| Formal Trinks partnership | Trinks is a Grupo Stone company and the incumbent most able to copy her; a partnership hands them the playbook (see §4). |
| Monthly SaaS / retainer / minimum in any disguise | Rejected twice by the founder; success-only pricing **is** the product (constitution #1). |
| Merchant of record | Would put the full GMV in her tax base (~21.3% Anexo V on R$3.6M/yr = insolvency) and make her the consumer's counterparty (see §20). |
| Asaas subaccounts / creating accounts for salons | Triggers Asaas' regulatory homologation regime and holds client money — both prohibited by constitution #8. |
| Paid traffic | The Lista + free scan + fair is the acquisition engine; paid acquisition breaks the zero-fixed-cost economics (see §2, §21). |
| Hiring salespeople | One-person company by design; the first hire is a part-time ops VA around month 18 at the earliest. |
| Health-data ingestion (anamnese, prontuário, service descriptions) | Art. 11 has no LI basis and §4 prohibits sharing for economic advantage — consent cannot cure it (§5.4). |
| Unofficial WhatsApp tools (Z-API, Evolution, etc.) | Ban risk and illegitimacy; the entire channel dies with the number. |
| Standing / batched campaign approvals | Would collapse operator status under the ANPD Example-5 test (§5.3). |
| Discount-conditioned consent | The Febrafar trap; voids consent and draws the Procon fine pattern (§5.2). |
| Sends to SP-registered numbers under any exception | PROCON-SP Q17: no offer to a registered number, existing customer or not (§5.5). |
| Frequency-cap override switch | The 60-day ledger is a quality and legal shield; an override would be used (§5.1.2, §5.7). |
| Citing "split avoids bitributação" in sales | The claim is wrong (SC Cosit 143/2021 line); the pitch never implies tax relief for the salon (see §20). |
| Credit card acceptance | Prohibited without new legal review; Pix-only is a regulatory feature (constitution #8). |
| Cross-salon voucher redemption | Payment-arrangement / e-money territory (constitution #16). |


# PART III — THE MACHINE (BUILD SPECIFICATION)

## 7. System Architecture and Stack

### 7.1 The decided stack

| Component | Choice | Rationale (two lines) |
|---|---|---|
| Web app | **Next.js (App Router)** | One framework serves the founder dashboard, the client-facing offer/consent/voucher pages, and all inbound webhook routes. Server components + route handlers keep the surface small enough for one non-technical founder directing Claude Code. |
| Worker | **Small always-on Node process** (Railway or Fly.io) | Send loops, queues, and monitors must run when no HTTP request is in flight; serverless timeouts are the wrong shape for a 180-message send loop. One cheap always-on container covers every salon (see §21: infra ≈ R$100–300/mo total). |
| Database | **Postgres** (Supabase acceptable) | Relational integrity is the product: gates, ledgers, and approval artifacts are foreign-key chains, not documents. Append-only audit tables are enforced with triggers + revoked privileges (§8.8). |
| Payments | **Asaas REST v3** (see §12) | Verified native split-to-third-party-wallet on Pix; founder never holds client money. |
| Messaging | **Meta WhatsApp Cloud API, direct** (see §11) | Founder is her own Meta Tech Provider; R$0 fixed per salon; no BSP margin. |
| Transactional email | **Resend** (lightweight API) | Used ONLY for: Raio-X delivery on Pix confirmation, voucher/receipt copy, refund confirmations. Never marketing, never client outreach. |
| UI language | **pt-BR throughout** | The founder is Brazilian and every owner-facing and client-facing string is pt-BR (App A). English exists only in code and this document. |

No other runtime services. No Redis (Postgres `SELECT ... FOR UPDATE SKIP LOCKED` job queue is sufficient at this scale — ASSUMPTION: campaign volume per §21 never exceeds a few thousand jobs/day, which Postgres queuing handles trivially). No LLM in the data path — hard rule, see §7.6.

### 7.2 Monorepo layout

One repository. One deploy story.

```
caixa-cheia/
├── apps/
│   ├── web/                  # Next.js App Router
│   │   ├── app/(painel)/     # founder dashboard, pt-BR (screens: see §15)
│   │   ├── app/(publico)/    # offer page, voucher page, consent QR page,
│   │   │                     #   opt-out confirmation (see §13, §14)
│   │   ├── app/api/webhooks/meta/route.ts    # Cloud API webhooks
│   │   ├── app/api/webhooks/asaas/route.ts   # Asaas payment webhooks
│   │   └── app/api/...       # magic-link endpoints, Raio-X PDF render
│   └── worker/               # always-on Node process
│       ├── jobs/             # job handlers (list in §7.4)
│       └── loop.ts           # poll queue table, claim, execute, record
├── packages/
│   ├── db/                   # schema (SQL migrations, §8), typed query layer,
│   │                         #   append-only triggers, seed/test fixtures
│   └── shared/               # money (centavos), phone (E.164), TZ helpers,
│                             #   gate rules (§10), state machines (§8.7),
│                             #   importer adapters + column classifier (§9),
│                             #   error-code handbook constants (App B)
├── .env.example              # every variable in the §7.7 inventory
└── package.json              # workspaces
```

Rule: business logic (gate, margin math, state transitions, adapters) lives in `packages/shared` and is imported by both apps, so the dashboard preview and the worker execute the identical code path.

### 7.3 Environments

| Environment | Web | Worker | Database | Asaas | Meta |
|---|---|---|---|---|---|
| **dev** | localhost | localhost | local Postgres (or Supabase branch) | `api-sandbox.asaas.com/v3`, keys `$aact_hmlg_` | Meta test number on the founder's own dev WABA |
| **sandbox** | staging deploy | staging | staging DB | Asaas sandbox (account B registered independently at sandbox.asaas.com — never created via `POST /v3/accounts`; see §12) | same dev WABA; templates submitted for real review |
| **prod** | production deploy | production | production DB | `api.asaas.com/v3`, production keys; first split validated at R$5 (Gate 1, §23) | live salon WABAs (coexistence) |

Sandbox exists chiefly to rehearse the two irreversible externalities: the Asaas split lifecycle (payment confirmation is UI-only in sandbox) and Meta template review/pausing behavior. Never point dev at production Asaas keys; the per-salon key can move salon money (§7.6).

### 7.4 The always-on worker: jobs list

The worker is a single process running a claim-execute-record loop over a `jobs` table (Postgres queue). Every job is idempotent (§7.8). The complete job inventory:

**Send loops**
1. `campaign_send` — walks an approved+scheduled campaign's manifest, sends one template message per eligible recipient via `POST /{phone_number_id}/messages`, records a `sends` row per recipient, respects the WABA's messaging tier (new portfolios: 250 unique recipients/24h — one 180-recipient campaign fits) and the 60-day frequency ledger re-check at send time.
2. `owner_notify` — exactly TWO automated owner messages, both sent from the SALON's own WABA to the owner's phone as UTILITY templates (ASSUMPTION: utility categorization holds — service-management follow-up on the owner's own mandate; Meta recategorization risk noted): (1) the approval request ("responda APROVO"), (2) the post-campaign results message. Nothing else is automated: scan results, audit offers, heartbeat nudges, and monthly ledger links are MANUAL sends from the founder's own phone (per-surface table in §15).

**Webhook processors** (webhook routes only verify signature, persist the raw event to `external_calls`, and enqueue; processing is async in the worker)
3. `meta_status_processor` — delivery statuses and error codes per `wamid` → `sends` rows (131049, 130472, 131050, 131026, 131048, 132015, `held_for_quality_assessment`; handling per App B).
4. `meta_user_preferences_processor` — `user_preferences` webhook (stop/resume, category marketing_messages) → `suppressions` GLOBAL rows (`business_id` NULL — WhatsApp-level signal; authoritative, §8).
5. `meta_account_update_processor` — `PARTNER_REMOVED` with `COMPANION_INACTIVITY`/`PRIMARY_INACTIVITY` (coexistence death), template status changes, quality/tier changes.
6. `asaas_payment_processor` — payment lifecycle events → `charges`, `splits`, `vouchers` issuance on confirmation, Raio-X auto-release on audit-charge confirmation (automatic transactional EMAIL with the private URL via Resend + `audit_reports.status` flips to `released`; the dashboard renders the WhatsApp-ready message the founder forwards manually from her own phone — §15), `PAYMENT_SPLIT_DIVERGENCE_BLOCK`, `ACCOUNT_STATUS_*`.
7. `inbound_text_processor` — liberal free-text opt-out matcher (SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA, + profanity list) and owner "APROVO" replies (matching: case-insensitive exact word, trimmed) → `approvals`.

**Monitors** (cron-style, all times America/Sao_Paulo)
8. `monitor_heartbeat_13d` — daily: per coexistence WABA, days since last app-open signal. This job creates ALERTS only, it never sends: at day 9 it writes a `heartbeat_due` alert to the Painel; the FOUNDER sends the friendly nudge from her own phone on day 10 (locked copy: "abre o WhatsApp do salão hoje pra manter tudo rodando 🙂") and phones the owner on day 12; at day 13 the job marks the salon `paused(heartbeat)` and alerts the founder (§15).
9. `monitor_quality` — daily snapshot per WABA: quality rating (GREEN/YELLOW/RED), messaging tier, block/opt-out rates → `quality_snapshots`. Quality ladder (canonical in §11, restated identically): RED → auto-pause ALL sends and campaigns for that WABA; YELLOW → no NEW campaign proposals until founder review (already-approved scheduled sends hold); opt-out rate ≥1% (rolling per campaign) → flag + the business becomes Gate-C ineligible (Gate C criteria, §3); ≥3% → auto-pause new sends for that business. Template pausing (Meta-side 3h/6h/disabled) is handled independently by the send engine (job 14).
10. `monitor_split_status` — polls unresolved `splits`; flags `REFUSED` with `refusalReason = RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT` (pledged receivables) → founder alert + billing fallback (NFS-e + Pix cobrança to the salon, see §12).
11. `monitor_settlement_reconciliation` — daily: Asaas payment/split reports vs local `charges`/`splits`/`credit_ledger`; every divergence becomes a Painel alert; ties each settled fee to its NFS-e trail (§20).
12. `nfse_queue_processor` — QUEUE-BUILDER ONLY: batches settled fees per salon per period into `nfse_queue` (with `item_source` per §8.5). NFS-e issuance in v1 is MANUAL — the founder issues the nota to the SALON (never the consumer; LC 116 item 10.02/10.09 — see §20) in the municipal portal and records the number back against the queue row (§15). [OPEN] municipal NFS-e API/portal mechanics depend on the chosen municipality (§20, §23).
13. `monitor_frequency_ledger` — nightly integrity check: no `phone_hash` received >1 marketing template in any rolling 60 days across ALL businesses sharing the same `parent_business_id` (group scope — the sole permitted cross-business lookup, §8.9; defense-in-depth: the gate check C8 is the primary enforcement).
14. `monitor_template_state` — tracks template pausing ladder (3h → 6h → Disabled) and warming status; new templates are warmed on a small cohort before full sends (App B).

### 7.5 Integration map (diagram in text)

```
[Salon system: Trinks|Avec|AppBarber|Belasis|Fresha|Gendo]
        │  CSV/XLSX export (or Avec/Belasis REST pull)
        ▼
[Importer + column classifier (§9)]
        │  allowlist fields ONLY; everything else dropped at parse
        │  time and logged (name+count, no content)
        ▼
[Postgres: clients / visits / package_balances / consents]
        │
        ▼
[Eligibility gate (§10): preconditions P1–P4 + per-client C1–C9]
        │        ──fail──▶ [manifest_entries: per-check fail reasons]
        │ pass
        ▼
[Manifest ▸ owner approval via WhatsApp "APROVO" (§8: approvals)]
        │ approved + scheduled
        ▼
[Worker send loop] ──▶ [Meta Cloud API, salon's own number (coexistence)]
        │  statuses/errors via webhook ──▶ [sends / suppressions]
        ▼
[Client taps URL button] ──▶ [Offer page, opaque URL (§13)]
        │  Pix checkout: charge created by founder's code
        │  IN THE SALON'S Asaas account, with
        │  splits[{walletId: founder, percentualValue: 20}]
        ▼
[Asaas] ── settlement ──▶ salon 80% / founder 20% (on netValue)
        │  webhooks ──▶ [charges / splits / refunds]
        ▼
[Voucher issued (§13)] ──▶ [redemptions at the salon]
        ▼
[Ledger: credit_ledger + settlement reconciliation + NFS-e queue (§20)]
```

Every arrow that crosses a system boundary is an entry in `external_calls` (§7.8). Replies from clients never enter this map: they land in the salon's WhatsApp Business App and stay there (locked decision §6).

### 7.6 Security posture

1. **Per-salon Asaas API keys: encrypted at rest, access-logged.** Each salon's key can move that salon's money — this is the highest-sensitivity secret in the system (no OAuth exists at Asaas; see §12). Keys are stored AES-256-GCM-encrypted in `businesses.asaas_api_key_ciphertext` under a master key (`SECRETS_MASTER_KEY`) that lives only in the runtime environment, never in the DB or repo. Every decrypt writes a `secret_access_log` row (who/which job/why/when). Operational mitigations per §12: named keys with expiry, IP allowlist pinned to worker egress IPs, transfer-authorization webhook enabled on each salon account.
2. **No client PII to any LLM, ever — hard rule enforced in code review.** No customer/client row, phone, name, or derived field may be passed to any AI API. If Claude Code is used to debug production data, it works against synthetic fixtures in `packages/db`.
3. **Append-only audit tables** for `events`, `approvals`, `consents`, `suppressions`, `credit_ledger`, `dropped_columns_log`, `secret_access_log`, `redemptions`, `gate_runs`: `UPDATE`/`DELETE` revoked from the application role and blocked by trigger (§8.8). These tables are the operator-posture evidence (§5): the approval artifact, the exclusion log, the consent record, the gate-run record (Art. 37).
4. **LGPD data-subject deletion path.** On a titular deletion request (routed via the salon — the controller — per the DPA, see App C): the `clients` row is tombstoned (name → NULL, phone → salted SHA-256 hash retained in `phone_hash`, `deleted_at` set); `visits` and `package_balances` rows for that client are deleted; consent and suppression rows are RETAINED (they are legal-obligation records, and the suppression must survive deletion so a re-import cannot resurrect the number — matching happens on `phone_hash`). The deletion itself is written to `events`. DERIVED design from locked decision §6 #15 (suppression authoritative) + Art. 37 record-keeping duty (§5).
5. **Webhook authenticity**: Meta `X-Hub-Signature-256` verified against `META_APP_SECRET`; Asaas webhook token verified per request. Unverified payloads are logged and dropped.
6. **Magic links** (owner surfaces, §15): single-purpose signed tokens, **30-day expiry**, no owner password anywhere.
7. **Founder auth**: single `founder_user` row (email + TOTP); session cookie backed by the `sessions` table (`token_hash`, `expires_at`) — no third-party auth provider (§8.6).
8. **E-sign v1**: contract/DPA/LIA adoption is in-app click-to-sign with logged evidence (name, timestamp, IP hash) recorded in `documents.evidence` — no external e-sign provider at launch [ASSUMED sufficient for these B2B docs; lawyer confirms — §23 register].

### 7.7 Env/secrets inventory

Everything the build session must provision. Per-salon secrets are NOT env vars — they live encrypted in the database (§7.6).

| Variable | Scope | What it is |
|---|---|---|
| `DATABASE_URL` | web+worker | Postgres connection string |
| `SECRETS_MASTER_KEY` | web+worker | 32-byte key for AES-256-GCM encryption of per-salon Asaas keys |
| `APP_BASE_URL` | web+worker | Public https origin (offer/voucher/consent URLs, webhook registration) |
| `META_APP_ID` / `META_APP_SECRET` | web+worker | Founder's Business-type Meta app (Tech Provider, §11) |
| `META_SYSTEM_USER_TOKEN` | worker | Long-lived system-user token for `whatsapp_business_messaging` + `whatsapp_business_management` |
| `META_WEBHOOK_VERIFY_TOKEN` | web | Static token for webhook subscription handshake |
| `META_ES_CONFIG_ID` | web | Embedded Signup v4 configuration id (coexistence flow, §11) [OPEN: exact featureType string — verify at build; collected in §23] |
| `ASAAS_BASE_URL` | web+worker | `https://api-sandbox.asaas.com/v3` or `https://api.asaas.com/v3` |
| `ASAAS_FOUNDER_API_KEY` | worker | Founder's OWN Asaas account key (audit charges — her own product, no split; wallet lookups) |
| `ASAAS_FOUNDER_WALLET_ID` | worker | The `walletId` that receives every 20% split |
| `ASAAS_WEBHOOK_TOKEN` | web | Verifies inbound Asaas webhooks |
| `PDF_RENDER_MODE` | web | Raio-X HTML→PDF rendering (ASSUMPTION: headless Chromium in-process) |
| `RESEND_API_KEY` | web+worker | Transactional email (Raio-X delivery, voucher/receipt copy, refund confirmations ONLY — §7.1) |
| `SENTRY_DSN` (or equiv.) | web+worker | Error tracking. ASSUMPTION: some error tracker is used |
| `NODE_ENV` / `APP_ENV` | all | `dev` / `sandbox` / `prod` per §7.3 |

Deliberately absent: no e-sign provider key (v1 e-sign is in-app click-to-sign, §7.6) and no municipal NFS-e credentials (v1 issuance is manual via the municipal portal, §7.4 job 12; [OPEN] municipal mechanics — §20, §23).

### 7.8 Idempotency and stored request/response logs

Locked rule (constitution, §6 — restated): **all external calls are idempotent, with stored request/response logs.**

- Every outbound call to Meta or Asaas writes an `external_calls` row BEFORE the request (direction `out`, `idempotency_key`, full request JSON minus secrets) and updates it with the response (status, body, latency). Every inbound webhook writes a row (direction `in`, raw payload, signature-verification result) before any processing.
- Idempotency keys: `campaign_send` uses `send:{campaign_id}:{client_id}` — a retry after a crash re-reads `sends` and skips completed recipients; charge creation uses Asaas `externalReference = charge:{charge_uuid}` and checks for an existing payment with that reference before POSTing; webhook processing is keyed on the provider event id — duplicates are no-ops.
- **Never auto-retry error 131049** (per-user marketing cap): retries trigger a 24h blackout for those recipients (App B). Idempotent ≠ retried; the retry policy table lives in App B.
- These logs double as the Art. 42 §2 evidence trail (§5): the system can prove exactly what was sent, to whom, when, and on whose approval.

### 7.9 TZ / locale / money / phone conventions

| Concern | Convention |
|---|---|
| Timezone | All timestamps stored `timestamptz` (UTC on the wire); ALL display, scheduling, cron windows, and "business hours" logic in **America/Sao_Paulo**. Sends only within business hours (night/weekend sends are a case-law aggravator, §5). |
| Money | **Integer centavos** everywhere internally (`_centavos` suffix, `bigint`). Convert to decimal reais only at the Asaas API boundary (Asaas speaks decimal; `percentualValue` carries 4 decimals). Display format `R$ 1.234,56`. Never float. |
| Phones | **E.164** (`+5511...`) at every boundary; importer normalizes Brazilian formats (with/without 9th digit) on ingest; dedupe on normalized phone (Trinks duplicate-record defect, §9). |
| Locale | UI copy pt-BR; dates displayed `dd/mm/yyyy`; template language code exactly `pt_BR` (underscore — wrong code is Meta error 100). |
| IDs | UUIDv7 primary keys (time-ordered; ASSUMPTION — any UUID works). Asaas/Meta native ids stored verbatim alongside. |

---

## 8. Data Model

Postgres. Every table gets `id uuid primary key`, `created_at timestamptz not null default now()`; mutable tables also get `updated_at`. Only deltas from that pattern are shown. Money columns are `bigint` centavos. Phones are `text` E.164. DDL is normative: a fresh build session should transcribe it into migrations in `packages/db`.

### 8.1 Enums

```sql
create type business_kind      as enum ('salon','barbershop','laser_aesthetics');
create type business_structure as enum ('single','group','franchisor');
create type source_system      as enum ('trinks','avec','appbarber','belasis','fresha','gendo','other');

create type salon_state    as enum ('lead','scanned','audit_paid','onboarding','active','paused','churned');
create type pause_reason   as enum ('quality','heartbeat','choice');

create type campaign_type  as enum ('win_back','renewal','birthday','slow_day');
create type campaign_state as enum ('draft','gated','margin_ok','pending_approval','approved',
                                    'scheduled','sending','sent','settling','settled',
                                    'partially_refunded','zeroed','reported');

create type template_state as enum ('draft','submitted','approved','rejected','warming',
                                    'active','paused_3h','paused_6h','disabled');

create type voucher_state  as enum ('issued','partially_redeemed','redeemed',
                                    'refund_requested','refunded_partial','refunded');

create type send_status    as enum ('queued','sent','delivered','read','failed','held');

create type charge_kind    as enum ('package_sale','audit');
create type charge_state   as enum ('pending','received','confirmed','refunded',
                                    'partially_refunded','overdue','cancelled');

create type split_state    as enum ('PENDING','AWAITING_CREDIT','DONE',
                                    'PROCESSING_REFUND','REFUNDED','REFUSED','CANCELLED');

create type consent_value  as enum ('granted','refused','revoked');
create type consent_source as enum ('qr_card','offer_page','checkout','fresha_import',
                                    'observacao_marker','manual');
create type consent_evidence_class as enum ('native_capture','imported_boolean','marker');

-- NOTE: registry hits are GATE EXCLUSIONS (logged in state_registry_checks), never suppressions;
-- Fresha "Accepts marketing" = FALSE is a REFUSED consent record (Branch-A exclusion), never a suppression.
create type suppression_reason as enum ('user_preferences_stop','error_131050','free_text_optout',
                                        'whatsapp_block','manual','owner_request');
create type insumo_class   as enum ('low','medium','high');
create type registry_uf    as enum ('SP','PR','GO','SC','DF','RS');

create type document_kind  as enum ('lia','dpa','contract','privacy_notice');
create type esign_status   as enum ('draft','sent','signed');
create type attestation_kind as enum ('no_packages_sold','adult_base_only');
create type alert_type     as enum ('quality_yellow','quality_red','optout_threshold','heartbeat_due',
                                    'split_refused','split_divergence','kyc_pending','refund_due',
                                    'render_failed','registry_block','approval_expired');
create type nfse_item_source as enum ('split','credit_drawdown','billing_fallback');
```

### 8.2 Parties, imports, client data (allowlist)

```sql
create table businesses (
  id                        uuid primary key,
  name                      text not null,
  legal_name                text,
  cnpj                      text,                      -- salon is merchant of record (§5, §12)
  kind                      business_kind not null,
  structure                 business_structure not null default 'single',
  parent_business_id        uuid references businesses(id),  -- unit → group/franchisor HQ
  source_system             source_system not null,
  state                     salon_state not null default 'lead',
  pause_reason              pause_reason,              -- non-null only when state='paused'
  -- cadence_config (per-BUSINESS, never per-location, never per-client-service; §6)
  cadence_days              int not null,              -- default by kind: barber 45, salon 90, laser_aesthetics 120
  constraint cadence_range check (cadence_days between 30 and 180),
  -- package economics defaults for the margin gate P2 (3-question step; campaign snapshots override)
  default_commission_pct    numeric(5,2),              -- professional commission % of gross
  default_insumo_class      insumo_class,              -- bands (ASSUMED, defined in §10 P2): low 5% / medium 13% / high 22%
  default_simples_pct       numeric(5,2) not null default 8.0,   -- margin-gate P2 input
  -- Asaas (per-salon account; key ciphertext only — §7.6)
  asaas_account_status      text,                      -- from ACCOUNT_STATUS_* webhooks
  asaas_api_key_ciphertext  bytea,
  asaas_api_key_last4       text,
  asaas_key_expires_at      timestamptz,
  -- Meta / WhatsApp (client-owned portfolio + one coexistence WABA, BRL; §11)
  meta_portfolio_id         text,
  waba_id                   text,
  phone_number_id           text,
  display_phone             text,                      -- E.164
  coexistence               boolean not null default true,
  messaging_tier            text,                      -- '250','2000','10000','100000','unlimited'
  -- Gate C unlock bookkeeping (§3: 2 settled win-backs + GREEN + opt-out <1%)
  settled_winback_count     int not null default 0,
  active_base_unlocked      boolean not null default false,
  updated_at                timestamptz not null default now()
);
create index on businesses (state);
create index on businesses (parent_business_id);

create table locations (
  id            uuid primary key,
  business_id   uuid not null references businesses(id),
  name          text not null,
  city          text, uf text, neighborhood text
);

create table users (   -- owner contacts; approvers. NOT client end-consumers.
  id             uuid primary key,
  business_id    uuid not null references businesses(id),
  name           text not null,
  whatsapp_phone text not null,          -- E.164; where approval requests go
  email          text,
  role           text not null default 'owner',   -- 'owner'|'manager'
  is_approver    boolean not null default false
);

create table imports (
  id                 uuid primary key,
  business_id        uuid not null references businesses(id),
  location_id        uuid references locations(id),
  source_system      source_system not null,
  adapter_version    text not null,
  file_name          text,
  file_sha256        text not null,      -- idempotent re-upload detection
  row_count_raw      int,
  row_count_ingested int,
  row_count_deduped  int,                -- duplicate phones merged (Trinks defect)
  cap_suspected      boolean not null default false,  -- e.g. Gendo 5000-row silent cap → re-request flow (§9)
  status             text not null default 'parsed'   -- 'parsed'|'committed'|'rejected'
);

-- Minimization evidence: names+counts of columns DROPPED at parse time. Never content.
create table dropped_columns_log (      -- APPEND-ONLY
  id           uuid primary key,
  import_id    uuid not null references imports(id),
  column_name  text not null,           -- e.g. 'Anamnese', 'Observações', 'Sexo'
  row_count    int not null
);

-- ALLOWLIST ONLY (Option B, locked §6): no service, category, description,
-- notes, clinical, or gender fields exist in this schema. Structurally.
create table clients (
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  location_id      uuid references locations(id),   -- nullable; per-location counts (§15)
  external_id      text,                -- source-system id, when present
  name             text,                -- NULL after LGPD tombstone (§7.6)
  phone            text,                -- E.164; NULL after tombstone
  phone_hash       text not null,       -- salted SHA-256; survives deletion; suppression join key
  birthdate        date,                -- optional (birthday cohorts)
  first_import_id  uuid references imports(id),
  last_import_id   uuid references imports(id),
  deleted_at       timestamptz,         -- LGPD tombstone marker
  updated_at       timestamptz not null default now(),
  unique (business_id, phone_hash)
);
create index on clients (business_id, phone);

create table client_merges (             -- import external-id merge mapping (§9)
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  external_id_old  text not null,
  client_id        uuid not null references clients(id)
);

create table visits (
  id                   uuid primary key,
  client_id            uuid not null references clients(id) on delete cascade,
  business_id          uuid not null references businesses(id),
  location_id          uuid references locations(id),
  visit_date           date not null,   -- last_visit is the hard requirement (§9)
  ticket_value_centavos bigint,         -- optional
  import_id            uuid not null references imports(id),
  unique (client_id, visit_date)        -- idempotent re-import
  -- NO service field. Ever. (Option B)
);
create index on visits (business_id, visit_date);

create table package_balances (         -- CPC 47 source for the Raio-X (§19)
  id                       uuid primary key,
  client_id                uuid not null references clients(id) on delete cascade,
  business_id              uuid not null references businesses(id),
  value_remaining_centavos bigint,      -- some systems export value…
  sessions_remaining       int,         -- …others only session counts
  expiry                   date,
  as_of                    date not null,       -- snapshot date
  import_id                uuid not null references imports(id)
);
create index on package_balances (business_id, as_of);
```

### 8.3 Consent, suppression, registries

```sql
create table consents (                 -- APPEND-ONLY; latest row per phone wins. CANONICAL schema:
                                        -- App C.4 (§5) and §14.4 are regenerated views of THIS table.
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  client_id        uuid references clients(id),  -- NULLABLE: QR captures may precede import;
                                                 --   linked later by phone match
  phone_e164       text not null,
  value            consent_value not null,       -- refusals stored too (§14); Fresha "Accepts
                                                 --   marketing" FALSE ⇒ 'refused' (Branch-A gate
                                                 --   exclusion, NOT a suppression)
  source           consent_source not null,      -- fresha_import for ALL Fresha rows (§9)
  evidence_class   consent_evidence_class not null,  -- native_capture | imported_boolean | marker
  displayed_text   text,                -- EXACT string shown (App A locked copy);
                                        --   NOT NULL for native_capture (trigger-enforced);
                                        --   NULL allowed for imports
  text_version     text,                -- NOT NULL for native_capture (trigger-enforced)
  notice_version   uuid,                -- references notices(id)
  scope            text not null default 'whatsapp_marketing',
                                        -- FIXED string at launch; the gate does NOT key on scope.
                                        -- Granular scopes = post-launch ASSUMED extension (§14)
  staff_identifier text,                -- nullable; who captured it at reception
  ip_hash          text,                -- nullable; page captures
  captured_at      timestamptz not null
);
create index on consents (business_id, phone_e164, captured_at desc);
create index on consents (client_id, captured_at desc);

-- AUTHORITATIVE over every source system (locked §6 #15). Keyed on phone_hash
-- so a re-imported CSV — or a deleted+re-created client — can never resurrect
-- an opted-out number. APPEND-ONLY; stop/resume modeled as rows.
create table suppressions (
  id           uuid primary key,
  business_id  uuid references businesses(id),  -- NULLABLE: NULL = GLOBAL row (error 131050 /
                                                --   user_preferences are WhatsApp-global signals)
  phone_hash   text not null,
  action       text not null default 'stop',    -- 'stop' | 'resume' (user_preferences only)
  reason       suppression_reason not null,
  permanent    boolean not null default false,  -- error_131050 ⇒ true; never resumable
  source_text  text,                            -- the matched free text, e.g. 'SAIR'
  source_event uuid                             -- references external_calls(id)
);
create index on suppressions (business_id, phone_hash, created_at desc);
create index on suppressions (phone_hash, created_at desc);   -- global rows
-- Effective suppression = latest 'stop' not followed by 'resume', OR any permanent row,
-- evaluated over BOTH the business's rows and global (business_id IS NULL) rows.
-- Free-text suppressions are NEVER auto-removed: a later documented consent grant creates a
-- Branch-A basis, but the suppression row stays unless the founder manually reviews (§11, §15).

create table registry_lists (            -- loaded state do-not-disturb lists (SP first; §5)
  id           uuid primary key,
  state        registry_uf not null,
  source       text not null,            -- where/how the list was obtained
  version_date date not null,
  loaded_at    timestamptz not null
);

create table registry_entries (
  id           uuid primary key,
  list_id      uuid not null references registry_lists(id),
  phone_hash   text not null
);
create index on registry_entries (list_id, phone_hash);

-- Per-gate-run check log. FAIL-CLOSED: if an applicable state's list is not loaded (recipient UF
-- attributed by phone DDD→UF), promotional sends to that state are BLOCKED — no warning mode (§5, §10).
-- A registry hit is a GATE EXCLUSION logged here; it never creates a suppression row.
create table state_registry_checks (    -- SP first; PR/GO/SC/DF/RS as lists become obtainable (§5)
  id           uuid primary key,
  phone_hash   text not null,
  registry     registry_uf not null,
  checked_at   timestamptz not null,
  listed       boolean not null,        -- listed ⇒ absolute exclusion from promotional sends
  method       text                     -- [OPEN] list-access mechanism unresolved — REQUIRED
                                        --   BEFORE FIRST SEND, owner = lawyer (§23)
);
create index on state_registry_checks (phone_hash, registry, checked_at desc);
```

### 8.4 Campaigns, manifests, approvals, templates, sends

```sql
create table templates (
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  name             text not null,       -- ≤512 chars, lowercase+underscores (Meta rule)
  language         text not null default 'pt_BR',
  category         text not null default 'MARKETING',
  body             text not null,       -- ≤1024 chars; GENERIC copy, never names a service (§6)
  header           text,                -- ≤60
  footer           text,                -- ≤60
  buttons          jsonb,               -- ≤2 URL buttons; opt-out button best practice
  meta_template_id text,
  state            template_state not null default 'draft',
  rejection_reason text,
  updated_at       timestamptz not null default now()
);

create table campaigns (
  id                 uuid primary key,
  business_id        uuid not null references businesses(id),
  location_id        uuid references locations(id),           -- optional per-location targeting
  type               campaign_type not null,
  state              campaign_state not null default 'draft',
  segment_rule       jsonb not null,     -- named, mathematical rule, e.g.
                                         -- {"days_since_last_visit_gt":120,"lte":360}
  template_id        uuid references templates(id),
  -- package snapshot (offer page content is owner-authored commercial content, §13)
  package_name             text,
  package_price_centavos   bigint,
  package_sessions         int,
  package_validity_days    int,
  avulso_price_centavos    bigint,       -- CDC disclosure (§13)
  cancellation_terms       text,         -- exact pre-disclosed math (TJDFT 2110685, §5)
  -- margin gate inputs + result (3-question step; blocks <~15% salon net, §6 #2)
  commission_pct           numeric(5,2),
  insumo_class             insumo_class,
  margin_result            jsonb,        -- full worked math, salon_net_pct, pass boolean
  scheduled_at       timestamptz,
  offer_page_slug    text unique,        -- ONE opaque slug per campaign; same URL for every
                                         --   recipient (§13); button variable carries this token
  offer_valid_until  timestamptz,        -- drives the template {{3}} validity date, the offer-page
                                         --   shutoff, and settling→settled/zeroed close-out (§8.7)
  updated_at         timestamptz not null default now()
);
create index on campaigns (business_id, state);

create table lint_wordlist (             -- versioned copy-lint wordlist (gate precondition P3, §10)
  id       uuid primary key,
  version  text not null,
  terms    text[] not null,              -- service names etc. that generic copy must not contain
  active   boolean not null default false
);

create table manifests (                 -- frozen recipient list a campaign actually sends to
  id             uuid primary key,
  campaign_id    uuid not null references campaigns(id),
  generated_at   timestamptz not null,
  gate_version   text not null,          -- which rule set ran (§10)
  total_candidates int not null,
  eligible_count int not null,
  content_hash   text not null           -- hash of ordered eligible client ids + template body
);

create table manifest_entries (          -- per-client gate check results — the exclusion log (§5)
  id           uuid primary key,
  manifest_id  uuid not null references manifests(id),
  client_id    uuid not null references clients(id),
  eligible     boolean not null,
  checks       jsonb not null,
  -- EXACTLY the 9 per-client checks C1–C9 (§10 canonical identifiers) with pass/fail:
  -- {"own_client":"pass","lawful_basis":"pass","no_clinical_data":"pass",
  --  "package_balance":"pass","suppression":"pass","state_registry":"pass",
  --  "not_minor":"pass","frequency_60d":"fail","contactable":"pass"}
  -- Campaign preconditions P1–P4 are campaign-level and live in gate_runs, never here.
  fail_reasons text[],
  unique (manifest_id, client_id)
);

create table gate_runs (                 -- APPEND-ONLY. The Art. 37 processing record (§5).
  id                     uuid primary key,
  campaign_id            uuid not null references campaigns(id),
  ran_at                 timestamptz not null,
  precondition_results   jsonb not null,   -- {"P1":"pass","P2":"pass","P3":"pass","P4":"pass"}
  per_client_pass_count  int not null,
  per_client_fail_counts jsonb not null,   -- {"C1":0,"C2":12,...,"C9":1}
  gate_version           text not null
);
create index on gate_runs (campaign_id, ran_at desc);

create table approvals (                 -- APPEND-ONLY. The operator-posture artifact (§5, §6 #11).
  id               uuid primary key,
  campaign_id      uuid not null references campaigns(id),
  manifest_id      uuid not null references manifests(id),
  requested_at     timestamptz not null,
  segment_rule_text text not null,       -- the NAMED rule, human-readable, as shown to the owner
  recipient_count  int not null,
  message_text     text not null,        -- the exact template body the owner approved
  template_id      uuid not null references templates(id),
  template_version text not null,        -- the approved template version (§16)
  expires_at       timestamptz not null, -- requested_at + 7 days; expired ⇒ re-approve (§10)
  owner_user_id    uuid not null references users(id),
  owner_phone      text not null,
  owner_reply_text text,                 -- 'APROVO' (or the refusal — refusals recorded too)
  owner_reply_at   timestamptz,
  owner_reply_wamid text,                -- WhatsApp message id of the reply
  status           text not null default 'requested'  -- 'requested'|'approved'|'refused'|'expired'
);

create table sends (
  id                uuid primary key,
  campaign_id       uuid not null references campaigns(id),
  manifest_entry_id uuid not null references manifest_entries(id),
  client_id         uuid not null references clients(id),
  phone_hash        text not null,             -- C8 group-scope frequency queries (§8.9)
  idempotency_key   text not null unique,     -- send:{campaign_id}:{client_id}
  wamid             text,
  status            send_status not null default 'queued',
  error_code        int,                       -- 131049/131050/130472/131026/131048/132015 (App B)
  error_detail      text,
  held_for_quality  boolean not null default false,
  sent_at           timestamptz,
  delivered_at      timestamptz,               -- billing + model both key on DELIVERED (§11)
  read_at           timestamptz,
  updated_at        timestamptz not null default now()
);
create index on sends (campaign_id, status);
create index on sends (phone_hash, sent_at);   -- C8 60-day frequency ledger query: phone_hash
                                               --   across businesses sharing parent_business_id
```

### 8.5 Money: charges, splits, refunds, vouchers, credit, NFS-e

```sql
create table charges (
  id                    uuid primary key,
  kind                  charge_kind not null,
  business_id           uuid not null references businesses(id),
  campaign_id           uuid references campaigns(id),      -- null for audit charges
  client_id             uuid references clients(id),
  asaas_payment_id      text unique,
  asaas_account         text not null,   -- 'salon' (package_sale, split rides on it)
                                         -- | 'founder' (audit — her product, NO split)
  external_reference    text not null unique,   -- charge:{charge_uuid} — idempotency (§7.8)
  credit_drawdown       boolean not null default false,
                                         -- audit-credit drawdown: created WITHOUT split; fee
                                         -- accrues as credit_ledger entries; risk guard #4
                                         -- (missing-split alert) EXEMPTS flagged charges (§12)
  value_centavos        bigint not null,
  net_value_centavos    bigint,          -- from Asaas after its fee; split base (§12)
  asaas_status_raw      text,
  state                 charge_state not null default 'pending',
  pix_qr_payload        text,
  settled_at            timestamptz,
  updated_at            timestamptz not null default now()
);
create index on charges (business_id, state);

create table splits (
  id                  uuid primary key,
  charge_id           uuid not null references charges(id),
  asaas_split_id      text unique,
  wallet_id           text not null,     -- ASAAS_FOUNDER_WALLET_ID
  percentual_value    numeric(7,4) not null default 20.0000,
  value_centavos      bigint,            -- computed on netValue at settlement
  status              split_state not null default 'PENDING',
  refusal_reason      text,              -- RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT
  cancellation_reason text,              -- PAYMENT_REFUNDED | WALLET_UNABLE_TO_RECEIVE
  updated_at          timestamptz not null default now()
);

create table refunds (
  id               uuid primary key,
  charge_id        uuid not null references charges(id),
  kind             text not null,        -- 'full' | 'partial'  (partial = the NORMAL case, §12)
  value_centavos   bigint not null,
  reason           text,                 -- 'cdc_art49_7d' | 'pro_rata_cancellation' | ...
  asaas_status     text,
  requested_at     timestamptz not null,
  completed_at     timestamptz,
  pro_rata_math    jsonb                 -- worked arithmetic shown to salon+client (§12, §13)
);

create table refund_legs (               -- pro-rata split-reversal legs (splitRefunds[])
  id             uuid primary key,
  refund_id      uuid not null references refunds(id),
  split_id       uuid not null references splits(id),
  value_centavos bigint not null,        -- founder's fee share returned
  status         text not null default 'pending'   -- 'pending'|'done'|'failed'
);

create table vouchers (
  id                        uuid primary key,
  charge_id                 uuid not null unique references charges(id),
  client_id                 uuid references clients(id),   -- NULLABLE: checkout resolves by E.164
                                                           --   phone match; forwarded links are
                                                           --   legal buyers too (§13)
  buyer_name                text,
  buyer_phone_e164          text,
  business_id               uuid not null references businesses(id),  -- ONLY redeemable here (§6 #16)
  code                      text not null unique,
  state                     voucher_state not null default 'issued',
  sessions_total            int not null,
  sessions_remaining        int not null,
  value_total_centavos      bigint not null,
  value_remaining_centavos  bigint not null,
  expires_at                date not null,      -- validity prominently pre-disclosed (§13)
  updated_at                timestamptz not null default now()
);

create table redemptions (               -- APPEND-ONLY. The salon's litigation defense (§5).
  id             uuid primary key,
  voucher_id     uuid not null references vouchers(id),
  location_id    uuid references locations(id),
  redeemed_at    timestamptz not null,
  sessions_used  int not null default 1,
  value_centavos bigint,
  recorded_via   text not null           -- 'owner_magic_link' | 'founder_manual'
);

create table credit_ledger (             -- APPEND-ONLY. Audit-credit accounting (§3, §19).
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  entry_type       text not null,        -- 'audit_credit_grant' | 'fee_offset'
                                         -- | 'credit_restore' (refund-symmetric) | 'expiry'
  amount_centavos  bigint not null,      -- signed; grants positive, offsets negative
  balance_after_centavos bigint not null,
  charge_id        uuid references charges(id),
  refund_id        uuid references refunds(id),
  expires_at       date                  -- grant + 12 months
);

create table nfse_queue (                -- fee → nota to the SALON, never the consumer (§20)
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  period           text not null,        -- 'YYYY-MM'
  fee_centavos     bigint not null,
  split_ids        uuid[],               -- NULLABLE: credit-drawdown and billing-fallback fee
                                         --   items have no splits rows
  item_source      nfse_item_source not null default 'split',   -- split|credit_drawdown|billing_fallback
  service_code     text not null default '10.02',   -- 10.02/10.09; NEVER 1.05/1.09 (§20)
  status           text not null default 'pending', -- 'pending'|'issued'|'error'
  nfse_number      text,
  issued_at        timestamptz,
  error_detail     text
);
```

### 8.6 Health, documents, census, audit trail

```sql
create table quality_snapshots (
  id             uuid primary key,
  business_id    uuid not null references businesses(id),
  taken_at       timestamptz not null,
  quality_rating text not null,          -- 'GREEN'|'YELLOW'|'RED'|'UNKNOWN'
  messaging_tier text,
  optout_rate    numeric(6,4),           -- rolling per campaign (§11 ladder: ≥1% flag, ≥3% pause)
  block_signals  int,
  pacing_events  int                     -- held_for_quality_assessment count
);
create index on quality_snapshots (business_id, taken_at desc);

create table heartbeats (                -- coexistence 13-day app-open gate (§11)
  id               uuid primary key,
  business_id      uuid not null references businesses(id),
  last_signal_at   timestamptz,          -- from smb_app_state_sync / echoes webhooks
  days_since       int,
  nudge_sent_at    timestamptz,          -- day-10 nudge (founder-sent from her own phone, manual;
                                         --   recorded here after the day-9 heartbeat_due alert)
  status           text not null default 'ok'   -- 'ok'|'warning'|'dead'
);

create table notices (                   -- privacy notice versions (Art. 9, §14)
  id           uuid primary key,
  business_id  uuid references businesses(id),   -- null = master template version
  version      text not null,
  body         text not null,
  published_at timestamptz not null
);

create table documents (                 -- ONE table for all salon-facing legal docs (§5, §17):
                                         -- the LIA/DPA are the SALON'S documents; founder drafts templates
  id                uuid primary key,
  business_id       uuid not null references businesses(id),
  kind              document_kind not null,        -- lia | dpa | contract | privacy_notice
  version           text not null,
  content_hash      text not null,
  esign_status      esign_status not null default 'draft',   -- draft | sent | signed
  signed_at         timestamptz,
  signer_identifier text,
  evidence          jsonb                -- in-app click-to-sign evidence: name, timestamp, ip_hash (§7.6)
);
create index on documents (business_id, kind, version);

create table attestations (              -- owner attestations backing gate checks C4/C7 (§10)
  id           uuid primary key,
  business_id  uuid not null references businesses(id),
  kind         attestation_kind not null,   -- no_packages_sold | adult_base_only
  signed_at    timestamptz not null,
  document_id  uuid references documents(id),
  lia_version  text                          -- LIA version that notes the attestation
);

create table scan_results (              -- free-scan outputs (§15)
  id                 uuid primary key,
  business_id        uuid not null references businesses(id),
  import_id          uuid not null references imports(id),
  total_clients      int not null,
  lapsed_count       int not null,
  contactable_count  int not null,
  eligible_count     int not null,
  generated_at       timestamptz not null,
  share_message_text text                -- copy-ready text the founder sends manually (§15)
);

create table audit_reports (             -- Raio-X lifecycle (§15, §19)
  id           uuid primary key,
  business_id  uuid not null references businesses(id),
  status       text not null default 'draft',   -- 'draft'|'released'|'delivered'
  version      text not null,
  url_slug     text unique,
  pdf_path     text,
  released_at  timestamptz,
  charge_id    uuid references charges(id)      -- NULLABLE: design-partner audits are comped (R$0)
);

create table alerts (                    -- Painel alert inbox (§15)
  id              uuid primary key,
  type            alert_type not null,
  business_id     uuid references businesses(id),  -- nullable: system-wide alerts
  payload         jsonb,
  acknowledged_at timestamptz
);
create index on alerts (business_id, created_at desc);

create table jobs (                      -- the §7.4 worker's Postgres queue
  id         uuid primary key,
  kind       text not null,
  run_at     timestamptz not null default now(),
  payload    jsonb not null default '{}',
  status     text not null default 'queued',   -- 'queued'|'running'|'done'|'failed'
  attempts   int not null default 0,
  last_error text
);
create index on jobs (status, run_at);

create table history_sync_messages (     -- ONBOARDING-SCOPED history sync ONLY (§11): relationship
                                         -- evidence. content column ACCESS-RESTRICTED; never LLM-exposed.
  id             uuid primary key,
  business_id    uuid not null references businesses(id),
  wa_thread_hash text not null,
  content        text,                   -- ACCESS-RESTRICTED (§7.6); never LLM-exposed
  direction      text not null,          -- 'in' | 'out'
  message_ts     timestamptz not null,
  ingested_at    timestamptz not null default now()
);

create table founder_user (              -- single row; email + TOTP (§7.6)
  id              uuid primary key,
  email           text not null unique,
  totp_secret_enc bytea not null
);

create table sessions (                  -- founder dashboard sessions (§7.6)
  id         uuid primary key,
  token_hash text not null unique,
  expires_at timestamptz not null
);

create table lista (                     -- census CRM (§2, §15 screen 10)
  id             uuid primary key,
  name           text not null,
  city           text, uf text, neighborhood text,
  system_tag     source_system,
  unit_count     int,
  is_group       boolean not null default false,
  is_franchisor  boolean not null default false,
  status         text not null default 'lead',   -- mirrors pipeline kanban (§15)
  next_action    text,
  source_url     text,
  business_id    uuid references businesses(id), -- set on conversion
  updated_at     timestamptz not null default now()
);

create table external_calls (            -- APPEND-ONLY. §7.8 request/response log.
  id               uuid primary key,
  direction        text not null,        -- 'out' | 'in'
  provider         text not null,        -- 'meta' | 'asaas' | 'nfse' | ...
  idempotency_key  text,
  provider_event_id text,
  request          jsonb,                -- secrets redacted
  response         jsonb,
  http_status      int,
  signature_valid  boolean,
  latency_ms       int
);
create unique index on external_calls (provider, provider_event_id)
  where provider_event_id is not null;   -- duplicate webhooks are no-ops

create table secret_access_log (         -- APPEND-ONLY (§7.6)
  id           uuid primary key,
  business_id  uuid not null references businesses(id),
  accessed_by  text not null,            -- job name or dashboard actor
  purpose      text not null,
  accessed_at  timestamptz not null default now()
);

create table events (                    -- APPEND-ONLY master audit log
  id           bigint generated always as identity primary key,
  occurred_at  timestamptz not null default now(),
  actor        text not null,            -- 'founder'|'worker'|'webhook'|'owner'|'client'|'system'
  entity_type  text not null,
  entity_id    uuid,
  action       text not null,            -- 'state_transition'|'gate_run'|'lgpd_deletion'|...
  payload      jsonb not null
);
create index on events (entity_type, entity_id, occurred_at);
```

### 8.7 State machines (enums + allowed transitions)

Transitions are enforced in `packages/shared` (one `transition(entity, from, to)` function per machine, throwing on illegal moves) and every executed transition writes an `events` row. Anything not listed is illegal.

**Campaign** (`campaign_state`):

| From | To | Trigger |
|---|---|---|
| draft | gated | campaign preconditions P1/P3/P4 pass + per-client checks C1–C9 executed (§10); manifest built; gate_runs row written |
| gated | margin_ok | margin precondition P2 passes (≥15% salon net floor; evaluated after the gate per the §15 stepper) |
| gated / margin_ok | draft | any input edited (re-gate required) |
| margin_ok | pending_approval | approval request sent to owner |
| pending_approval | approved | owner replies "APROVO" (case-insensitive exact word, trimmed; approvals row with template_id+version) |
| pending_approval | draft | owner refuses or the approval expires (approvals.expires_at = requested_at + 7 days → re-approve) |
| approved | scheduled | send window set (business hours, America/Sao_Paulo) |
| scheduled | sending | worker claims the send job |
| sending | sent | last manifest recipient in terminal send status |
| sent | settling | first charge created from the offer page |
| settling | settled | offer window closed (campaigns.offer_valid_until passed + 48h after the last charge expiry); all charges terminal; ≥1 settle |
| settling | zeroed | same close-out trigger with zero settles (~7% of campaigns, §21) |
| settled | partially_refunded | any refund posts after settlement |
| settled / partially_refunded / zeroed | reported | results message sent to owner |

**Salon** (`salon_state`): `lead → scanned` (free scan delivered) `→ audit_paid` (R$490/R$990 Pix confirmed) `→ onboarding` (guided session, §17) `→ active`. `active → paused` with `pause_reason ∈ {quality, heartbeat, choice}`; `paused → active` when the cause clears; `any → churned` (terminal; data-retention clock starts per DPA). There is NO audit-skip transition: design partners get the audit COMPED (R$0 — `audit_reports.charge_id` NULL, founder discretion) but a Raio-X is always GENERATED; no salon reaches campaign #1 without one (§3, §17).

**Template** (`template_state`): `draft → submitted → approved | rejected`; `approved → warming` (small-cohort warm-up, App B) `→ active`; `active → paused_3h → paused_6h → disabled` (Meta's pausing ladder — mirror of Meta state, updated by webhook, never locally invented); `paused_3h/6h → active` on Meta unpause; `rejected → draft` (edit and resubmit). Meta may recategorize approved templates — a recategorized template is marked `disabled` locally and a new one created (Meta cannot recategorize in place, §11).

**Voucher** (`voucher_state`): `issued → partially_redeemed` (first redemption with sessions remaining) `→ redeemed` (`sessions_remaining = 0`); `issued | partially_redeemed → refund_requested`. From `refund_requested`: `→ refunded` (FULL pro-rata refund — terminal; `refund_legs` reverse the fee share); `→ refunded_partial` (PARTIAL refund executed — sessions/value reduced, the voucher CONTINUES and remains redeemable); `→ partially_redeemed | issued` if the client withdraws the request. `refunded_partial → redeemed` when the remaining sessions are consumed, or `→ refund_requested` again. `redeemed` and `refunded` are terminal.

**Charge/split** (mirrors of Asaas, never locally invented): `charge_state` follows Asaas payment webhooks (`pending → received/confirmed → refunded/partially_refunded`; `overdue/cancelled` for expired Pix). `split_state` follows the documented Asaas lifecycle `PENDING → AWAITING_CREDIT → DONE`, with `PROCESSING_REFUND → REFUNDED` on reversal and `REFUSED`/`CANCELLED` from `refusalReason`/`cancellationReason`. The reconciliation monitor (§7.4 job 11) alerts on any local/remote divergence.

### 8.8 Append-only enforcement

For `events`, `approvals`, `consents`, `suppressions`, `credit_ledger`, `dropped_columns_log`, `redemptions`, `external_calls`, `secret_access_log`, `gate_runs`, `history_sync_messages`:

```sql
create function forbid_mutation() returns trigger language plpgsql as $$
begin
  raise exception 'append-only table: % on % is forbidden', tg_op, tg_table_name;
end $$;

-- repeated per table:
create trigger t_append_only before update or delete on approvals
  for each row execute function forbid_mutation();

revoke update, delete on approvals from app_rw;   -- belt AND suspenders
```

Corrections to append-only data are made by writing a superseding row (e.g. a new `consents` row, a `resume` suppression row), never by editing history. `approvals.status` is the single narrow exception: it is written exactly once from `requested` to its terminal value by the reply processor; enforce with a column-level trigger permitting only that transition (DERIVED design choice; alternatively model replies as a second append-only table — either satisfies the artifact requirement of §5).

### 8.9 What is deliberately absent

No `services` table. No `gender` column. No `notes`/`observações` column. No cross-business client identity (no global person table — the same phone at two salons is two unrelated rows; cross-salon analytics on identifiable data is banned, locked §6 #10), with EXACTLY ONE carve-out: the 60-day frequency check C8 (§10) matches `phone_hash` across businesses sharing the same `parent_business_id` — same controller group, no other cross-business lookup exists. No POST-onboarding reply content is stored (client replies land in the salon's WhatsApp Business App and stay there); the onboarding history sync (`history_sync_messages`, §8.6) is the sole, access-restricted exception — relationship evidence only, never LLM-exposed. These absences are the Option B structural defense (§5): the schema cannot hold what the law must never see her process.


## 9. IMPORTERS AND ADAPTERS

### 9.1 The allowlist architecture (Option B)

The importer is the boundary between the salon's source system and the Caixa Cheia database. Its governing rule is inverted from a normal ETL pipeline: **columns are dropped by default, and only explicitly allowlisted fields may cross into the database.** There is no "map the rest later" bucket, no raw-file staging table containing full source rows, no generic JSON column that preserves unmapped data. Anything not on the allowlist ceases to exist at parse time.

This is not a convenience choice; it is the structural legal defense that makes laser and aesthetics clinics servable at all (see §5). LGPD Art. 11 has no legitimate-interest basis for sensitive data, and the anamnese/prontuário record is sensitive without question. Because the importer physically cannot store `service_description`, `anamnese`, `prontuário`, `observações`, or any clinical/health field, the founder cannot know and does not process what service any client had. All campaign triggers are purely mathematical (e.g., `days_since_last_visit > 120`), and template copy never names a service (enforced by gate precondition P3 `copy_lint`, see §10).

**Canonical fields (the complete allowlist):**

| Entity | Field | Type | Required | Notes |
|---|---|---|---|---|
| `client` | `external_id` | string | yes | Source-system client key |
| `client` | `name` | string | yes | First name used in template variable only |
| `client` | `phone` | string (E.164) | yes | Normalized at parse; join key for dedupe |
| `client` | `birthdate` | date | no | Used for birthday cohorts and minor exclusion |
| `visit` | `date` | date | yes* | *At minimum `last_visit_date` — see 9.4 |
| `visit` | `ticket_value` | integer centavos | no | Enriches Raio-X math |
| `package_balance` | `value_remaining` | integer centavos | no | CPC-47 exclusion source |
| `package_balance` | `sessions_remaining` | integer | no | Alternative balance measure |
| `package_balance` | `expiry` | date | no | |
| `consent` | `value` | boolean/enum | no | Fresha columns or own capture only (see §14) |
| `consent` | `captured_at` | timestamp | no | |
| `consent` | `source` | string | no | |
| `consent` | `scope` | string | no | Fixed `'whatsapp_marketing'` at launch |

Explicitly and permanently **not stored**: service names, categories, descriptions, notes/observações, gender, anamnese, prontuário, professional names, prices per service line, addresses, e-mail (not needed — the channel is WhatsApp). If a future feature appears to need one of these, the feature is redesigned or rejected (see §6).

**Column classifier.** Each adapter ships a mapping config: an ordered list of `(source_column_pattern → canonical_field)` rules plus an explicit denylist of known-dangerous columns (anamnese/prontuário/observações patterns) that are dropped even if a future mapping mistake would otherwise catch them. The classifier's output for every file is exactly three sets: mapped columns, denylisted columns, and unrecognized columns. The last two sets are **dropped identically** — unrecognized never means "keep and ask". One narrow, explicit carve-out: the Observações consent-marker parse (see §14) may extract a pre-agreed consent token from the Observações column **at parse time** into a `consents` row (`source: observacao_marker`); the Observações content itself is still never stored — only the structured consent row survives.

**Dropped-columns receipt.** Every import run writes an append-only record: file name, adapter, row count, and for each dropped column its **header name and cell count only — never content**. This receipt is minimization evidence (LGPD Art. 6º III) and appears in the salon's records vault (see §16) and in the founder's import screen (see §15). It is also a sales artifact: the founder can show an owner, in one screen, exactly what she refuses to touch.

```text
IMPORT RECEIPT — salão Bela Vista — 2026-09-12 14:03 BRT
Arquivo: clientes_trinks_export.xlsx (adapter: trinks/clientes v1)
Linhas: 1.412 | Clientes canônicos gravados: 1.377 (35 duplicatas de telefone mescladas)
Colunas mapeadas: Nome→name, Celular→phone, Nascimento→birthdate, Última visita→visit.date
Colunas descartadas (nome + contagem, conteúdo nunca lido além do parse):
  "Observações" (1.412), "Como conheceu" (1.412), "Profissional preferido" (1.402), ...
```

### 9.2 Dedupe rules (the Trinks defect)

Trinks' own reactivation tool double-messages clients when duplicate records share one phone number — a verified defect and a live differentiator. The importer's rule:

1. Normalize every phone to E.164 (`+55` + DDD + number; strip formatting; handle the 9th-digit mobile prefix).
2. Rows with an unparseable or landline-shaped phone are marked `uncontactable` (kept for Raio-X totals, never eligible).
3. Multiple source rows resolving to one E.164 phone **merge into one canonical client**: keep the most recent `last_visit_date`, sum nothing across identities (visits union by date), keep all `external_id`s in the `client_merges` mapping table (see §8) for traceability, prefer the row with a birthdate.
4. The merge is logged in `client_merges` (source `external_id`s → canonical client id) so a later export from the same system re-merges deterministically.
5. Salon Soft-style name-only joins (no stable id) are a flagged dedupe risk: join by phone first, name only as tiebreaker, never message a name-joined identity whose phone appears twice.

The frequency ledger and suppression list (see §10) key on the **`phone_hash`** (hash of the normalized E.164 phone, computed at normalization), never the source `external_id` — so a client duplicated in Trinks is still one person to the 60-day cap and one person to opt-out, and suppression survives the LGPD tombstone that nulls the phone (see §7.6).

### 9.3 Row-count-vs-cap guard (the Gendo truncation)

Gendo's client export ("Salvar no Excel", actually CSV) is capped by a page-size selector at a **maximum of 5,000 rows and truncates silently**. Any capped export from any system produces a Raio-X that understates the base and a campaign pool that silently misses clients.

Guard spec: each adapter declares `known_export_caps: [5000, ...]` (empty if none known). On import, if `row_count >= cap` or `row_count >= 0.98 × cap`, the import is marked `POSSIBLY_TRUNCATED`, the scan is blocked from being sent to the owner, and the UI shows a **re-request flow**: instructions (pt-BR, adapter-specific) for the owner to re-export in segments (e.g., filtered by name range or registration date) until segment row counts land clearly below the cap; segments are then merged through the same dedupe pipeline. A truncated import can never silently feed a campaign.

### 9.4 The hard requirement: last_visit_date, not history

The minimum servable dataset per client is **name + phone + last_visit_date**. Full visit history enriches the Raio-X and future event triggers, but its absence does not disqualify a system. This is what keeps Gendo likely-servable (its lineage export carries an `Última Visita` column — [OPEN], see 9.5) and keeps the adapter surface small.

### 9.5 Per-system adapter specs

Each adapter = one **mapping config** (column patterns → canonical fields) + one **quirks table** (caps, caveats, re-request scripts). Specs below reflect verified export paths and columns; unverified items are flagged.

**Trinks — launch adapter (weeks 2–4).** ~44k businesses (self-claim); market leader including barbershops. Self-serve Excel exports, not tier-gated. API exists but is partner-gated, separately paid, and has no endpoints for packages/balances/visit history — **CSV/Excel is the permanent architecture for Trinks**, not a stopgap.

| Item | Spec |
|---|---|
| Client export path | Meu Estabelecimento > Clientes > Todos os clientes > Mais filtros > filtro de última visita > Exportar |
| Lapsed report | "Relatório de clientes que não retornaram" — exportable, period filter **caps at exactly one year → the adapter builds windows of 90–360 days, never 365** |
| Package report | "Relatório de Saldo de Pacotes" per client, exportable. **Caveat: excludes packages "encerrados sem ser totalmente utilizados"** — expired-unused balances are invisible. The Raio-X number must be labeled "saldos ativos não consumidos" (active unconsumed balances only) or reconciled against "Venda de Pacotes – Encerrados" (see §19) |
| Consent field | None anywhere in the product |
| Known defect | Duplicate client records sharing one phone (see 9.2) |
| [OPEN] | Whether última visita is an export **column** (vs filter only) — Gate #2 of the 90-day plan; if filter-only, the adapter derives last_visit_date from the filtered lapsed report windows instead. Whether the package export carries a client join key. Whether balances export as value or only session counts. (All settleable in a 20-minute trial.) |

**Avec — adapter #2 (weeks 7–10).** ~40k businesses (self-claim); absorbed AZ4 and BeautyDate; owner Hyperlocal. Chosen over Belasis on market size + absorption. Export lives **only** in the Relatórios area — every one of the 278 numbered reports has a Print|Excel|PDF toolbar; the Lista de Clientes screen has no export (which is why migration guides false-negative it).

| Item | Spec |
|---|---|
| Report 0129 | Datas de últimas visitas + visit counts — the last_visit_date source |
| Report 0107 | Clientes que não retornaram em N dias — lapsed pool |
| Report 0002 | Visits per client + consumption |
| Report 0063 | Clientes com pacotes ativos — current-state balance snapshot, **the CPC-47 exclusion source** |
| Report 0006 (and 0013) | Credit/debit per client |
| Report 0031 | Services in period — pull for column verification only; service-level content is **not stored** (allowlist drops it); used transiently for aggregate Raio-X math at most, [OPEN] pending lawyer confirmation, default: don't ingest |
| Live API | Public REST at `api.avec.beauty`: `GET /reports/{code}?page=&limit=&inicio=&fim=`, token auth (verified reachable, clean 401 unauthenticated). Spec at doc.api.avec.beauty, including a "Relatórios franquias" folder — relevant to the franchisor segment (see §2) |
| Bulk option | Avec Lake — productized warehouse, 12 tables incl. histórico de agendamentos (Power BI/Looker/Metabase); a later option for large groups |
| Hard prohibition | Client records carry **Anamnese and Prontuário tabs — NEVER ingest**; no report containing them may be pulled; the denylist patterns cover both words |
| Consent field | None (0 hits across 278 report names) |
| [OPEN] | Exact column layouts of 0129/0107/0063/0006 — one token + 15 minutes closes this (week-1 task) |

**AppBarber/AppBeleza — adapter #3.** Barbershop leader (128k professional-app installs). Literal `Excel` button on report screens (visually verified from vendor help-center screenshots).

| Item | Spec |
|---|---|
| Agendamentos export | "Relatório de Agendamentos" grid, one export: `Cliente | Telefone | Profissional | Data (dd/mm/yyyy hh:mm) | Valor | Status`. Profissional column is dropped by the allowlist |
| Last visit | "Retorno por Período" gives Último Agendamento per client |
| Packages | PARTIAL: "Vendas de Pacotes" shows value paid, date, sessions used — Excel button on that screen **not visually confirmed** [OPEN]. Until confirmed, CPC-47 exclusion on AppBarber runs conservative (see §10 check C4) |
| Import direction | Inbound import to AppBarber is crippled (support ticket, 5-day SLA) — irrelevant to us; data flows OUT easily |
| Consent field | Zero of 161 help articles mention LGPD/consent |

**Fresha — adapter #4.** In Brazil since 07/2023, USD-only pricing, weak BR embedding — but **the only system with structured consent**.

| Item | Spec |
|---|---|
| Consent columns | Client export includes dedicated boolean columns **"Accepts marketing"** and **"Accepts SMS marketing"**. Mapping: "Accepts marketing" TRUE → `consents{value: granted, source: fresha_import, evidence_class: imported_boolean, captured_at: import_time, scope: 'whatsapp_marketing'}`; FALSE → a **refused record** (`value: refused`) — a Branch-A exclusion at gate check C2, **not** a suppression row. This is real evidence but weaker than the full consent tuple (no displayed string, no text version) — such clients pass Branch A of C2 with `evidence_class: imported_boolean`, and are still prioritized for native consent capture (see §14) |
| Visits | Appointments list export with date filters (PDF/CSV/XLSX); Client insights carry First/Last appointment + Total appointments |
| Packages | "Membership list" report exists; **no package export documented → CPC-47 unproven on Fresha** [OPEN]. Conservative mode until proven |
| Bulk option | Data connector (Snowflake, paid, per-location), 17 tables — no packages/consent tables |

**Belasis — adapter #5.** v5.2.13 (08/2025): "todos os relatórios do sistema possuem a opção de exportação". Reports include "Clientes inativos", "Retorno de clientes", "Todos os Agendamentos", "Extrato de Pacotes", "Pacotes em aberto".

| Item | Spec |
|---|---|
| Live API | Public REST at `api.belasis.com.br`: `GET /api/v1/clients` (searchable by Phone/Cellphone), `GET /api/v1/schedule_groups` (returns `client_id`, `start_date`, `end_date`) — dated per-client history via API |
| Quirks | Phone field is permission-gated in-product; packages are a paid add-on (some salons won't have the data); 90-day post-cancel freeze then deletion (churned-salon data disappears) |
| Consent field | None |

**Gendo — grade B, likely servable.** (=SuperAgendador rebrand; ~10k paying subscribers.) Client listing export capped at 5,000 rows with silent truncation (see 9.3). Family-lineage export columns: `Código | Nome | Telefone | Nascimento | Sexo | Pagamentos | Pendências | Visitas | Última Visita | Faltas` — Sexo, Pagamentos, Pendências, Faltas are dropped by the allowlist. [OPEN]: whether Gendo's current listing export actually carries the `Última Visita` column — settle via a 20-minute screen-share with any Gendo prospect before building. In-app Comportamento panel shows última visita + package credits; export of that panel is undocumented.

**Booksy — no adapter, ever.** Grade C: no self-service export (client list only via email support); reports are cash-flow/staff/tips only. Booksy is used exclusively as a **prospecting directory** (hard per-city counts, enumerable numeric city IDs — see §2). A Booksy-only prospect is logged in A Lista as `system: booksy, servable: no` and is not servable unless it also runs (or migrates to) a servable system.

**Dead / out / unservable systems.** Triage data for A Lista — a prospect on one of these systems is marked unservable (or, where noted, a migration lead):

| System | Status | Consequence for A Lista |
|---|---|---|
| Vagaro | Geo-blocked: serves US/CA/UK/AU only | Out of market — unservable |
| BeautyDate | Defunct → absorbed by Avec | Route via the Avec adapter |
| Salão99 | Dead 05/2026 | Refugees = live prospect list (system migration in progress) |
| SuperAgendador | Dead → rebranded/absorbed as Gendo | Route via Gendo (grade B above) |
| Personal MED | Print-only exports; medical vertical | Unservable (and out of vertical) |
| Simples Beleza | Not software (no product to export from) | Unservable |
| Software AZ | Discontinued → Avec | Route via the Avec adapter |
| Belio | Export on roadmap Q3-2026, 0% shipped | Unservable until export ships |
| Nuvem Gestor | No client/OS export + database deleted on cancel | Unservable; churn destroys the data |
| Salon Soft | Grade B−: exports exist but no stable client id — name-join dedupe risk (see 9.2 rule 5) | Servable with the name-join caveat only |

### 9.6 Adapter-threshold rule

A new adapter is built only when **≥25 qualified doors on that system exist in A Lista, OR one group of 3+ locations demands it** (locked, §6). Build order: Trinks (launch) → Avec (weeks 7–10) → AppBarber → Fresha → Belasis. Everything else waits for the threshold. The rule exists because each adapter is a permanent maintenance surface (export formats drift); the census (see §2, §18) provides the counts that trigger it.

---

## 10. THE ELIGIBILITY GATE

### 10.1 Posture: fail-closed

The gate is the machine that turns a raw imported base into a lawful send manifest. It is **fail-closed**: a client is ineligible until every check passes; a check that cannot be evaluated (missing data, missing registry list, unverified adapter caveat) **fails**, it does not warn — there is no warning mode anywhere in the gate. A campaign cannot reach `pending_approval` state (see §8.7 state machines) until the gate run completes with a non-empty eligible set and zero unevaluable checks. There is no founder-side override for any check except where a check explicitly defines a founder action (e.g., margin-gate 10% fallback fee, a founder-only lever never offered proactively — see §3).

The founder sees every gate run as a funnel — **4 campaign preconditions (P1–P4), 9 per-client checks (C1–C9), and 1 approval artifact** — each with a visible pass/fail count, in the Campanhas builder (see §15). The owner never sees the funnel; the owner sees the final manifest.

### 10.2 The gate structure: 4 campaign preconditions + 9 per-client checks + 1 approval artifact

This is the normative spec; §5 (legal view), §15 (UI view), and §8's `manifest_entries.checks` JSON keys are views of exactly this structure, under exactly these identifiers. Preconditions P1, P3, P4 run once per campaign, before the manifest is built; per-client checks C1–C9 run per manifest row in identifier order (funnel: each check sees only survivors of the previous; cheap structural checks first). P2 (margin) is a campaign precondition evaluated at builder step 4, after the per-client funnel — but a failing P2 still blocks the campaign from ever reaching `pending_approval` (see §10.3 and §8.7).

**P1 `docs_current` (campaign precondition).**
*Input:* `documents` status for this business (see §8, §16). *Pass:* signed contract, signed DPA, adopted LIA at current version (with laser annex if `businesses.kind = 'laser_aesthetics'`), current privacy notice version, all e-sign statuses complete. *Fail:* campaign blocked entirely; UI shows which document is missing/expired with a one-click link to the vault. *Founder sees:* ✅/❌ + document names.

**P2 `margin_gate` (campaign precondition, evaluated at step 4).**
*Input:* the 3-question package-design answers — professional commission %, insumo class, package price (see §3). *Insumo bands (ASSUMED, defined once here — every other section references these):* low = 5%, medium = 13%, high = 22% of price. *Formula (integer centavos):*

```text
net_to_salon = price
             − commission            (price × commission_pct)
             − insumos               (price × insumo_class_pct: low 5% / medium 13% / high 22%)
             − pix_fee               (live from GET /v3/myAccount/fees — never hardcoded)
             − simples               (price × default_simples_pct — businesses field, default 8% of gross)
             − fee                   (0.20 × netValue, i.e. price − pix_fee)
margin_pct = net_to_salon / price
PASS if margin_pct ≥ 0.15
```

Reference: R$900 at 40% commission → commission −360, insumos 13% −117, Pix −2, Simples ~8% −72, fee −180 → salon keeps ~R$169 ≈ 18.8% net (see §3 for the sales framing). The gate **refuses** to propose any campaign under ~15% salon net — it breaks at ~50% commission or high-insumo services, by design. *Fail:* campaign blocked; UI shows the arithmetic line-by-line and which input breaks it, so the founder can redesign the package with the owner. *Founder sees:* the full math table + PASS/FAIL.

**P3 `copy_lint` (campaign precondition).**
*Input:* the selected template text + all variable values. *Pass:* no token matches the **`lint_wordlist`** — a versioned table (see §8) of service names and service-implying terms (pt-BR: laser, depilação, botox, preenchimento, progressiva, balayage, mechas, limpeza de pele, massagem, sobrancelha, unha, barba… plus per-business additions), applied to template body, header, footer, buttons, and every variable value; additionally no `$` or `%` characters inside variable values, and template length/button rules hold. *Fail:* campaign blocked with the offending token highlighted. This check is structural (Option B, see §5): copy is ALWAYS generic; the offer page names the package as owner-authored commercial content, which is a different legal object (see §13). Every gate run records the wordlist version used. *Founder sees:* PASS or the flagged tokens.

**P4 `channel_health` (campaign precondition).**
*Input:* WABA quality rating, template status, 13-day heartbeat, messaging-limit tier (see §11 — the quality ladder is defined once in §11 and restated here). *Pass:* quality **GREEN** — the ladder: RED → auto-pause of ALL sends and campaigns for that WABA; YELLOW → no NEW campaign proposals until founder review (already-approved scheduled sends hold). Opt-out rate ≥1% (rolling, per campaign) → flag + the business is Gate-C ineligible; ≥3% → auto-pause of new sends for that business. Template must be `active` (Meta-side template pausing — 3h/6h/disabled — is handled independently by the send engine); heartbeat alive; manifest size ≤ remaining 24h unique-recipient budget (new portfolios: 250 — a 180-recipient campaign fits; this sub-check is re-verified once the manifest count is known). *Fail:* campaign blocked or manifest capped, with the specific reason. *Founder sees:* the four sub-indicators.

**C1 `own_client` (per client).**
*Input:* import provenance. *Pass:* the row originates from THIS business's own import (structural: the import pipeline records which business's source system produced the row; no cross-business pool exists). *Founder sees:* nothing to see when all pass; a non-zero exclusion here signals an import wiring fault.

**C2 `lawful_basis` (per client).**
*Input:* consent records (native capture per §14, Fresha imported booleans per §9.5) and `last_visit_date` vs. business-level cadence config. *Logic:*

```text
BRANCH A (consent): a consent record with value = granted, not revoked → PASS
    (a documented refusal — value = refused — is authoritative: FAIL, never LI-routed)
BRANCH B (legitimate interest), only when no consent record exists:
    PASS if cadence_days ≤ days_since_last_visit ≤ 360
```

*Cadence config:* lives at BUSINESS level, never derived from per-client services (Option B): floor = `cadence_days`, defaults barber 45 / salon 90 / laser_aesthetics 120, owner-adjustable within **30–180**; hard ceiling **360 days** — the 12-month line the supportive LI precedent uses ("último ano", see §5), and coincidentally the Trinks report's one-year cap (see §9.5). Clients lapsed >360 days are never in an LI pool (they may re-enter via consent capture, see §14). Active-base campaign types apply their own window logic on the same field (see §18) but the 360 ceiling and the 60-day ledger (C8) apply to all types. Each eligible client is tagged `basis: consent | legitimate_interest` in the manifest — this tag is stored per send and is the Art. 37 record's per-recipient line (see §5). *Founder sees:* counts per branch ("Consentimento: 41 · Legítimo interesse: 152 · Recusas excluídas: 9") + the window used.

**C3 `no_clinical_data` (per client).**
*Input:* the import's allowlist receipt (see §9.1). *Pass:* structural assertion that no clinical/service field was ingested for this client — the dropped-columns receipt proves the allowlist ran on the import that produced the row. *Fail:* only when provenance cannot be shown (e.g., a row predating receipt logging). *Founder sees:* receipt reference.

**C4 `package_balance` (per client).**
*Input:* `package_balances` records. *Pass:* client has **no** active unconsumed balance (`value_remaining > 0` or `sessions_remaining > 0`, not expired) — the CPC-47 exclusion. *Rationale:* a client who has already prepaid and not consumed is not a win-back target — messaging them to buy more prepaid services is commercially wrong and reputationally toxic; excluding them is a wedge nobody else has (see §4). *Conservative mode:* on systems where package export is unproven (Fresha) or unconfirmed (AppBarber), the check cannot evaluate → fail-closed means those clients are excluded — **unless** the business attests it sells no packages at all (an `attestations` row, kind `no_packages_sold` — see §8, §17): then the check passes with the attestation reference recorded. This is one of exactly two places an owner attestation substitutes for data (the other is C7). Trinks caveat: report shows active balances only; expired-unused invisible — acceptable, since expired balances are not a reason to suppress. *Founder sees:* excluded count + "fonte: relatório 0063" (or equivalent).

**C5 `suppression` (per client).**
*Input:* the `suppressions` table, keyed on `phone_hash`, including **global rows** (`business_id` NULL — 131050 / `user_preferences` stop events apply across all businesses), populated by: `user_preferences` webhook stop events, error 131050, liberal free-text opt-out matching (SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA + profanity), WhatsApp blocks, manual adds (see §11, App B). *Pass:* phone_hash not present. **The suppression list is authoritative over every source system (locked, §6) — anti-resurrection: a re-imported CSV can never resurrect an opted-out client.** *The guard:* suppression is checked at gate time against the live table AND re-checked at send time immediately before dispatch; imports never write to, delete from, or reset the suppression table — the import pipeline has no code path that touches it (enforced by schema permissions: the importer role has no grant on the table). Suppression entries are append-only with reason + timestamp; a resume event appends a `resume` row rather than deleting the stop. *Founder sees:* excluded count + Supressão center link.

**C6 `state_registry` (per client) — FAIL-CLOSED.**
*Input:* recipient's attributed state vs. loaded state do-not-disturb lists. *UF attribution:* by phone **DDD→UF mapping** (the allowlist stores no address); the mapping's imprecision (ported/relocated numbers) is noted in the LIA. SP's Bloqueio (Lei 17.832/2023) reaches WhatsApp and binds salons, with **no existing-customer exception for promotional content** (PROCON-SP FAQ Q17 — see §5); PR/GO/SC/DF/RS follow as lists become obtainable. *Design:* a **pluggable list check** — `registry_lists` (state, source, version_date, loaded_at) + `registry_entries` (list_id, phone_hash), see §8; one lookup per phone_hash across all loaded lists; a hit on any applicable list fails and is logged in `state_registry_checks`. **A registry hit is a gate exclusion, never a suppression row.** *No-list rule:* if an applicable state's list (SP first) is not loaded, **promotional sends to recipients attributed to that state are BLOCKED — fail-closed, no warning mode.** **[OPEN]: the supplier-side list-access mechanism is unverified** (PROCON-SP FAQ Q10 implies one exists — verify whether download/API/request; SP first). The week-1 lawyer engagement (item #5) must resolve the mechanism BEFORE the first send — timeline-compatible, since first sends land in weeks 4–6; the lawyer may authorize a documented interim measure — until then, blocked. Carried in the §23 register as REQUIRED-BEFORE-FIRST-SEND, owner = lawyer. The moment a list is obtainable, loading it is a drop-in. *Founder sees:* excluded count per state list, or the blocked-state count while no list is loaded.

**C7 `not_minor` (per client).**
*Input:* `birthdate` where present. *Pass:* `age ≥ 18`, or birthdate absent AND owner attestation on file. *Honest statement of the mechanism:* the allowlist carries birthdate as optional, and most source exports include it (Gendo: Nascimento; Trinks/Avec: present in client records — column presence [OPEN] per adapter). Where birthdate is present, the check is mechanical. **Where birthdate is absent, there is no mechanical way to detect a minor from allowlisted fields — the owner therefore attests that the imported base is the salon's adult client base and that minors (children's cuts etc.) are registered under a guardian's record or excluded from export** (an `attestations` row, kind `adult_base_only` — see §8), noted in the LIA and part of the LIA adoption signature (see §17, App C); the gate verifies the attestation is on file for the business. This is a stated residual risk, not a hidden one. *Founder sees:* excluded-by-birthdate count + attestation status.

**C8 `frequency_60d` (per client).**
*Input:* the send ledger — every marketing template send in `sends`, keyed on `phone_hash`, indexed by (phone_hash, sent_at). *Pass:* no marketing template to this phone_hash in the last 60 days across ALL campaign types and **ALL businesses sharing the same `parent_business_id`** (group scope — the ONLY permitted cross-business lookup in the system, carved out explicitly in §8.9). **No override exists — hard-coded (locked, §6).** There is deliberately no config row, no env var, no admin toggle; changing this requires a code change that the "no override" rule in §6 forbids. *Founder sees:* excluded count ("já contatados nos últimos 60 dias: 14").

**C9 `contactable` (per client).**
*Input:* phone validity + WABA-side knowledge. *Pass:* valid E.164 mobile, deduplicated at import (duplicate phones merged per §9.2), not flagged `uncontactable` at import, no prior terminal 131026 (recipient cannot receive) on record. (131049/130472 handling is send-time pacing, not gate-time exclusion — see App B.) *Founder sees:* uncontactable count.

**APPROVAL ARTIFACT (final precondition to send).**
The campaign may transition to `approved` (see §8.7) **only** after the owner-approval artifact exists: dated, capturing the named segment rule (e.g., "clientes sem visita há 90–360 dias, sem pacote ativo, sem opt-out"), the exact recipient count, the exact message text, the `template_id` + template version, and the owner's reply. The approval request is sent from the salon's own WABA to the owner's phone as a UTILITY template ("responda APROVO" — see §11, §15); the reply is captured via the messages webhook into `approvals.owner_reply_wamid`; APROVO matching is **case-insensitive exact word, trimmed**. **Approval validity: 7 days** (`approvals.expires_at`) — an expired approval requires re-approval before send. This artifact is THE fact that preserves operator posture (ANPD Guia de Agentes Example 5 — see §5): the salon takes the final decision. Never skipped, never batched across campaigns (locked, §6). If the manifest changes after approval (e.g., a suppression event lands between approval and send), the send-time re-check (C5/C8) shrinks the manifest silently downward — shrinking never requires re-approval; **growing always does**. *Founder sees:* approval status + artifact preview.

### 10.3 Gate pipeline pseudocode

```text
function run_gate(campaign):
    assert campaign.state == "draft"
    run = new GateRun(campaign, ran_at=now, gate_version)   # gate_version pins wordlist/
                                                            # cadence/registry-list/adapter versions

    # campaign preconditions (P2 margin runs AFTER the funnel, at builder step 4)
    for p in [P1_docs_current, P3_copy_lint, P4_channel_health]:
        r = p(campaign);  run.record_precondition(p, r)
        if r.fail: return run.abort(reason=p)               # fail-closed, stop early

    pool = load_clients(campaign.business, campaign.type)   # canonical clients, post-dedupe
    for client in pool:
        for c in [C1_own_client, C2_lawful_basis, C3_no_clinical_data,
                  C4_package_balance, C5_suppression, C6_state_registry,
                  C7_not_minor, C8_frequency_60d, C9_contactable]:
            r = c(client, campaign)
            if r.unevaluable: r = FAIL                      # cannot-evaluate == fail
            run.record_per_client(c, client, r)
            if r.fail: client.exclude(reason=c); break
        else:
            manifest.add(client, basis=client.basis)

    # P4 sub-check re-verified now that the manifest count is known
    if manifest.size > remaining_24h_recipient_budget: cap_or_abort(manifest)
    if manifest.empty: return run.abort(reason="empty_manifest")
    campaign.state = "gated"

    # builder step 4: margin gate — evaluated last, still blocks approval
    r = P2_margin_gate(campaign);  run.record_precondition(P2_margin_gate, r)
    if r.fail: return run.abort(reason=P2_margin_gate)      # never reaches pending_approval
    campaign.state = "margin_ok"                            # then pending_approval → approved (§8.7)
    return run.complete(manifest)

# send-time guard (separate, minimal):
function pre_dispatch(client):
    if suppressed(client.phone_hash) or frequency_60d_hit(client.phone_hash):
        drop(client, log=true)                              # shrink silently; never grow
```

### 10.4 What gets logged per gate run

Every gate run writes an append-only `gate_runs` record (see §8 for the canonical DDL): id, campaign_id, ran_at, `precondition_results` jsonb (keys P1–P4), `per_client_pass_count`, `per_client_fail_counts` jsonb (keys C1–C9), and `gate_version` — which pins the config used (cadence window, `lint_wordlist` version, registry-list versions loaded, adapter versions of the underlying imports). Per-client results live on each manifest row: `manifest_entries.checks` jsonb carries exactly the C1–C9 keys plus the basis tag (consent/LI); exclusion reasons are client id + check identifier — no free-text content; registry hits are additionally logged in `state_registry_checks`. Together with the owner-approval artifact and the dropped-columns receipts, this is the Art. 37 processing record and the Art. 42 §2 burden-reversal evidence (see §5): for any complaint, the founder can reconstruct exactly why a specific phone was or was not messaged on a specific date, under which basis, under which owner approval. The exclusion log is also her personal liability shield — documented refusals to execute a bad list (see §5). Gate-run summaries surface in the founder's Campanhas screen and in the salon's records vault (see §15, §16).


## 11. WHATSAPP INTEGRATION

Caixa Cheia sends every campaign message from the **salon's own WhatsApp number**, over the Meta WhatsApp Cloud API in **coexistence mode** — the salon keeps using its WhatsApp Business App exactly as before, and the system gains API send capability on the same number. The founder is her own **Meta Tech Provider** (locked decision, see §6): no BSP, no per-number monthly fee, R$0 fixed cost per salon. Each salon owns its own Meta business portfolio and its own WABA, created in BRL, with the salon's own payment method attached. Replies never touch the platform — they land in the salon's WhatsApp Business App, answered by the salon's humans (no bot, no founder-side inbox; locked, see §6).

This section is the implementation spec: the founder-side Tech Provider setup, the per-salon onboarding runbook, template management, the send engine, the monitors, suppression, and the interim-BSP contingency. Error codes and webhook events referenced here are consolidated in Appendix B.

### 11.1 Tech Provider setup runbook (founder-side, one-time)

This is the longest external clock in the whole build — **3–6 weeks realistic, start in week 1** (see §22/§24). It is free of charge at every step.

| Step | What | Notes |
|---|---|---|
| 1 | Create a Meta **Business-type app** with the **WhatsApp use case** in the founder's own Meta Business Portfolio | developers.facebook.com; the app is the platform's single credential root for Embedded Signup and all API calls |
| 2 | **Classic Meta Business Verification** of the founder's entity (the SLU, see §20) | **PLBV (business portfolio-level verification via a partner) is NOT available to Tech Providers** — only the classic document flow. Have CNPJ, contrato social, bank statement or utility bill ready |
| 3 | **App Review — Advanced Access** for two permissions: `whatsapp_business_messaging` and `whatsapp_business_management` | Requires **two demo screen-recordings**: (1) sending and receiving a message end-to-end; (2) creating a message template end-to-end. Record against a test WABA; narrate or caption in English |
| 4 | **Access Verification** | ~5 business days after App Review |
| 5 | Configure the app's **webhook endpoint** (single HTTPS URL, verify-token challenge) and subscribe to the field set in §11.2.4 | One endpoint serves every salon; events carry the WABA/phone-number ID to route internally |

**Throughput gate:** until verification + both reviews are complete, the app can onboard **10 new customers per rolling 7 days**; after completion this rises to **200 per rolling 7 days**. At Caixa Cheia's pace (3 design partners, then a fair cohort of ~10, see §22) the 10/7d limit only binds if Tech Provider approval slips past the Beauty Fair — that is exactly the scenario the §11.7 contingency exists for.

**No credit line:** Tech Providers get no Meta credit line. Message charges are billed to **each salon's own payment method** attached in WhatsApp Manager (BRL billing via Facebook Brasil; **boleto available**). This is a feature, not a gap — see the pass-through framing in §11.2.5.

### 11.2 Per-salon onboarding (Embedded Signup v4, coexistence)

#### 11.2.1 Preconditions checklist (verify BEFORE the onboarding call)

The onboarding session is one ~30-minute guided call on the salon's reception PC (owner-experience budget, see §17). Every item below is checked before the Embedded Signup popup is ever opened; a failed precondition aborts the session, because coexistence onboarding is a **one-way door** (coexistence↔API-only conversion is impossible in either direction; disconnect only via the app's own Settings; the Deregister API cannot be used on a coexistence number).

| # | Precondition | How verified |
|---|---|---|
| 1 | WhatsApp Business App version **≥ v2.24.17** on the salon's phone | Owner reads version from app Settings on the call |
| 2 | Number **≥ 3 months old with active messaging history** | Owner attests; this gate is Gupshup-documented as a Meta requirement — **[OPEN]** confirm exact wording in Meta docs at build |
| 3 | **NO payment method attached inside the WhatsApp Business app** | Owner checks in-app; if present, remove before signup |
| 4 | Owner has admin access to (or will create) the salon's Meta Business Portfolio | Created during the flow if absent |
| 5 | Owner **briefed and has acknowledged in writing** (a line in the onboarding checklist they sign, see §17) the coexistence side-effects below | Non-negotiable — these surprises destroy trust if discovered later |

**The side-effects briefing (owner must hear these before signup):**

- **Broadcast lists die** — new broadcast lists are disabled; existing ones become read-only. (For most salons this is the feature Caixa Cheia replaces anyway.)
- **Profile photo freezes** — the profile picture cannot be updated after onboarding. Owner sets the photo they want *first*.
- **Companion devices unlink** — all linked devices (WhatsApp Web, desktop) disconnect and must be re-linked; **Windows and WearOS companions are not supported** post-onboarding.
- **The 13-day rule** — the WhatsApp Business App on the phone must be **opened at least once every 13 days** or Meta silently kills the integration (see §11.5.2).
- Also disabled: disappearing messages, view-once, live location. Display name is not auto-reviewed; no OBA/blue badge (Meta Verified is the alternative path). Throughput is fixed at 20 messages/second.

#### 11.2.2 The Embedded Signup v4 flow

Embedded Signup **v4** only — v2 is deprecated 15 October 2026. Coexistence onboarding is a **customized ES flow** using the `whatsapp_business_app_onboarding` feature type. **[OPEN]** the older `coexistence` extras value may be stale — verify the current featureType string against Meta's ES docs at build time.

Flow, driven by the founder on the call:

1. Founder opens the onboarding wizard (see §15, surface 4-owner) which launches the ES popup under her Meta app's credentials.
2. Owner logs into their own Facebook/Meta account inside the popup, creates or selects **the salon's own business portfolio**, and walks the coexistence path (QR scan pairing the salon phone's WhatsApp Business App).
3. The flow creates the salon's **WABA — in BRL** (mandatory: from 07/2026 eligible Brazilian entities create WABAs in BRL; from 01/07/2027 Meta stops delivering for non-BRL WABAs of eligible customers; there is no reason ever to create anything else).
4. ES returns a **token code** to the platform's callback. The platform exchanges it server-side for a **business token scoped to that client's assets** and stores it encrypted in the secrets vault (see §7). ASSUMPTION: the exchange uses Meta's standard OAuth code-exchange endpoint (`GET /oauth/access_token` with app id, app secret, code) — confirm exact endpoint/params against current ES v4 docs at build **[OPEN]**; what is locked (see §6) is the pattern — a per-client business token obtained via token-code exchange — not the URL.
5. Platform registers the phone number, confirms the WABA/phone-number IDs, and writes them plus the onboarding state onto the salon's `businesses` row (see §8).

**Portfolio ownership — the only architecture that scales.** Business customers own all their WhatsApp assets: each salon's WABA lives in the **salon's own portfolio**, never the founder's. Two hard limits force this: Meta allows only **2 business portfolios per personal Facebook profile** (the founder cannot hold portfolios for clients), and a portfolio holds only **~4 coexistence WABAs** ([OPEN] — Infobip-documented, not confirmed by Meta). A coexistence WABA holds **exactly one number** and is **non-migratable**. One salon = one portfolio = one WABA = one number, owned by the salon.

#### 11.2.3 The 24-hour one-shot history sync

After onboarding, Meta delivers the number's **most recent 6 months of chat history in 3 phases via the `history` webhook — within a 24-hour one-shot window**. This history is a consent-evidence and relationship-evidence input (see §14, §16): it proves the prior relationship the legitimate-interest basis rests on.

Operating procedure:

- The webhook consumer must be **deployed, subscribed, and load-tested before the first salon onboards** — there is no second chance per onboarding.
- On onboarding completion, the platform opens a **sync watchdog**: expect phase-1 `history` payloads within minutes; alert the founder (Painel alert, see §15) if nothing arrives within 1 hour; escalate at 6 hours.
- **If the window is missed** (endpoint down, subscription missing, phases incomplete at 24h): the client must be **offboarded and re-onboarded** — disconnect via the salon app's Settings (the only disconnect path), verify preconditions again, re-run ES. Schedule the redo with the owner immediately; frame it as "precisamos refazer a conexão, leva 10 minutos" — never let a dead sync linger, because campaign eligibility evidence depends on it.
- Store history payloads append-only in `history_sync_messages` (see §8) — access-restricted, onboarding-scoped, indexed into the records vault (see §16). This is the sole exception to the no-reply-content-storage rule (no POST-onboarding reply content is ever stored); no client message content is ever sent to an LLM (hard rule, see §6/§7).

#### 11.2.4 Webhook subscriptions (per the founder's app; events route per-WABA)

Subscribe to ALL of:

| Field | Why |
|---|---|
| `messages` | Delivery/read/failure statuses per sent message; inbound free-text (for SAIR-matching, §11.6) |
| `history` | The 24-hour one-shot history sync (§11.2.3) |
| `smb_app_state_sync` | Contacts/state sync from the salon's app |
| `smb_message_echoes` | Echoes of messages the salon sends from its own app — feeds the heartbeat activity proxy (§11.5.2) and the per-client thread timeline ONLY. Never the frequency ledger: the ledger counts marketing template sends exclusively (gate check C8, see §10) and salon free-form messages must not count |
| `user_preferences` | Recipient marketing stop/resume events — suppression path 1 (§11.6) |
| `account_update` | `PARTNER_REMOVED` with `COMPANION_INACTIVITY`/`PRIMARY_INACTIVITY` = the 13-day death signal (§11.5.2); also ban/restriction events |

#### 11.2.5 Salon payment method — the transparent pass-through

Immediately after signup, still on the call, the owner attaches the **salon's own payment method** in WhatsApp Manager (BRL, Facebook Brasil billing, **boleto available** — most salon owners have no corporate card; boleto removes that objection).

The framing (see §3 for the commercial ladder): messages are a **transparent pass-through** — a 180-recipient campaign costs the salon **≈ R$57–61** paid directly to Meta (BR marketing rate ≈ $0.0625/msg, third-party corroborated; **[OPEN]** download Meta's own CSV rate card before external use). The founder earns **nothing** on messages and never touches message money. Pitch line logic: "o WhatsApp cobra de você o preço do WhatsApp, sem margem minha em cima — eu só ganho os 20% do que cair no seu Pix."

#### 11.2.6 Scaling the salon past 250: classic business verification per salon

A new portfolio starts at the **250 unique recipients / rolling 24h** messaging tier — one standard 180-recipient campaign fits with headroom. Tiers are **per portfolio** (shared across its numbers): 250 → 2,000 → 10,000 → 100,000 → Unlimited (there is **no 1,000 tier**).

The 250→2,000 path, either of:

1. **Classic business verification of the salon's portfolio** — the salon submits its own docs. Accepted Brazilian documents: **CNPJ card, MEI certificate, contrato social, bank statement, utility bill**. (PLBV is closed to Tech Provider-managed clients; classic only.) This is **need-triggered only**: verification is submitted only when a planned manifest would exceed 250 recipients. The CNPJ doc is collected during onboarding as a contingency, so submission is same-day whenever the need appears — no default document burden on day 1 (the 250 tier fits every standard 180-recipient campaign with headroom).
2. Organic: **2,000 delivered messages outside the customer-service window within 30 days with high-quality templates.**

Above 2,000, auto-promotion additionally requires **≥50% tier utilization over 7 days** — irrelevant at Caixa Cheia's per-salon volumes; 2,000 is the practical ceiling a salon ever needs.

### 11.3 Template management

All offer sends use **one pre-approved marketing template per campaign** (locked loop, see §6). Templates are created **per WABA** via the management API under each salon's business token.

**Non-negotiables:**

- Language **`pt_BR`** — underscore, exactly; a wrong language code returns error 100. Meta does not translate; **samples are required, in Portuguese**.
- Category **MARKETING, always**, for anything carrying an offer. Discount/urgency copy is precisely what the category is for (Meta's own examples include "{{15}}% off" and expiry dates); attempting offer copy in a UTILITY template earns the `PROMOTIONAL` rejection. Never try to sneak a cheaper category — recategorization risk cuts the other way too (below).

**Mechanical rules (encode as pre-submission lint — reject locally before Meta ever sees it):**

| Rule | Limit |
|---|---|
| No `$` or `%` inside `{{variables}}` | Put "R$" / "50%" in static text; variables carry bare numbers |
| Positional params | Sequential ({{1}}, {{2}}…); no dangling param at start or end of body |
| URL buttons | ≤ 2; URL ≤ 2,000 chars; **exactly 1 variable, appended at the END of the URL** (this is how the opaque **per-campaign** offer-page token travels — the same value for every recipient in the send, from `campaigns.offer_page_slug`, see §13) |
| Body | ≤ 1,024 chars |
| Header / Footer / Button label | 60 / 60 / 25 chars |
| Template name | ≤ 512 chars, lowercase + underscores only |
| Creation rate | ≤ 100 templates per WABA per hour (never a real constraint here) |
| `wa.me` links in CTAs | Rejected (Twilio-documented) — use the offer-page domain |
| Param values at send time | No newlines, tabs, or 4+ consecutive spaces — machine-blocked at send; sanitize in the send engine |

**Variable map (canonical):** the campaign template's **body** params are positional and fixed: **{{1}} = client first name, {{2}} = package commercial name (owner-authored), {{3}} = offer validity date (derived from `campaigns.offer_valid_until`, see §8)**. The **URL-button variable is a separate parameter namespace from body params** (button params are supplied in their own component at send time, so there is no {{1}} collision): it carries the **campaign token** (`campaigns.offer_page_slug`), the same value for every recipient in the send, supplied per-send.

Review is typically minutes, 24h SLA, 48h worst — submit templates at campaign-build time, not send time (see §18 operating week).

**Generic-copy lint:** template copy NEVER names any service (structural rule under Option B, see §5/§10) — the eligibility gate's campaign precondition **P3 `copy_lint`** (see §10) runs against the template body at build time, using the versioned lint wordlist (`lint_wordlist`, see §8): no service nouns, no clinical terms, no `$`/`%` inside variables, length/button rules, generic offer language only. The offer page (see §13) carries the specifics as owner-authored commercial content.

**No URL preview design consequence:** templated messages render **no URL preview card**. The copy must carry all persuasion weight — the link is a bare-looking button. This is why body copy quality and the button label ("Ver minha oferta") are first-class campaign inputs, not afterthoughts (see App A for locked copy).

**Recategorization watch:** `allow_category_change` is the default since 04/2025; Meta re-reviews approved templates and can flip utility→marketing with 1 day's notice (or none if flagged). An approved template cannot be recategorized by the sender — create a new one. 60-day appeal window. Monitor: any `message_template_category_update`-type event or category drift observed via the management API surfaces as a Painel alert. Since Caixa Cheia submits everything as MARKETING anyway, exposure is limited to Meta re-reviewing and pausing — which the quality monitors catch (§11.5).

**Template warming protocol:** every new or newly-unpaused template is first sent to a **small cohort** (operating default: the first 20–30 recipients of the manifest, then a pause, then the remainder — pacing detail in §18). Rationale: `held_for_quality_assessment` — Meta holds messages from new/unpaused templates and releases them on good early feedback, or drops them (with a failed-status webhook) on bad. Warming converts a potential 180-message drop into a 25-message drop plus a chance to fix the copy.

**Example API payloads** (shape per Graph API; builder verifies against current Meta docs at M4 **[OPEN]**):

Template creation — `POST /{waba_id}/message_templates`:

```json
{
  "name": "oferta_pacote_generica_v1",
  "language": "pt_BR",
  "category": "MARKETING",
  "components": [
    { "type": "BODY",
      "text": "Oi {{1}}! Temos uma condição especial no {{2}} pra você, válida até {{3}}.",
      "example": { "body_text": [["Ana", "Pacote Renove", "15/09/2026"]] } },
    { "type": "BUTTONS",
      "buttons": [
        { "type": "URL", "text": "Ver minha oferta",
          "url": "https://oferta.caixacheia.com.br/o/{{1}}",
          "example": ["https://oferta.caixacheia.com.br/o/x7k2m9qp"] }
      ] }
  ]
}
```

Template send — `POST /{phone_number_id}/messages`:

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999998888",
  "type": "template",
  "template": {
    "name": "oferta_pacote_generica_v1",
    "language": { "code": "pt_BR" },
    "components": [
      { "type": "body",
        "parameters": [
          { "type": "text", "text": "Ana" },
          { "type": "text", "text": "Pacote Renove" },
          { "type": "text", "text": "15/09/2026" }
        ] },
      { "type": "button", "sub_type": "url", "index": "0",
        "parameters": [ { "type": "text", "text": "x7k2m9qp" } ] }
    ]
  }
}
```

(Note the two namespaces: body params {{1}}–{{3}} vs the button's own {{1}}, which carries the per-campaign offer token.)

**Non-marketing message pricing & owner-facing categories:** UTILITY conversations are **~8–9× cheaper** than MARKETING in Brazil, and messages sent **inside an open 24h customer-service window are FREE**; a 72h-free window also exists for FEP/CTWA entry points. The published BR utility rate is conflicting — **$0.0068 vs $0.0080 — [OPEN]** (also in §23 register). Category classification of every owner-facing message: exactly **two** owner-facing messages are automated, both sent from the **salon's own WABA to the owner's phone as UTILITY templates** — (1) the campaign **approval request** ("responda APROVO"; the reply is captured via the `messages` webhook) and (2) the **campaign results message**. ASSUMPTION: UTILITY is defensible for both (service-management follow-up on the owner's own mandate), with recategorization risk per the watch above — if Meta flips them to MARKETING, cost rises but the mechanics are unchanged. Every other founder→owner surface (scan results, audit offer, onboarding scheduling, heartbeat nudge, ledger links) is **manual from the founder's own phone — never API, never automated** (channel table in §15). The opt-out confirmation is **never auto-sent** (locked, see §6).

### 11.4 Send engine

A single always-on Node worker (see §7) drains a per-campaign send queue.

**Rate:** coexistence throughput is **fixed at 20 messages/second**. A standard 180-recipient campaign is ≈ **9 seconds** of wire time. The worker paces at ≤ 20 mps per number (a global token bucket per phone-number ID), so throughput is never the constraint — correctness of the per-recipient state machine is.

**Per-recipient states:** `queued → sent → delivered → read` plus terminal failure states, driven by `messages` webhook statuses. Every recipient row stores: template used, params sent, message ID, each status timestamp, and any error code — append-only (see §8, §16).

**Error-code state machine (hard rules — encode exactly):**

```
on send/status error:
  131049  → recipient_state = CAPPED_24H          # per-user marketing cap hit
            NEVER retry this recipient in this campaign.
            Auto-retry ⇒ Meta imposes a 24h blackout for that recipient. Terminal for the send.
            Recipient remains eligible for FUTURE campaigns (cap is adaptive, per-user, global
            across all businesses; Brazil in scope; no published number — "2/24h" is folklore).
  131050  → recipient_state = SUPPRESSED_PERMANENT # user disabled marketing in WhatsApp
            Write to suppression list (authoritative, see §11.6 / §6). Never send again.
  132015  → campaign_state = PAUSED_TEMPLATE       # template paused by Meta
            Halt the whole queue for this template. Surface pause tier (3h/6h/disabled).
            Resume only after unpause + re-warm (§11.3).
  131048  → number_state = RESTRICTED              # number-level spam restriction
            Halt ALL sending on this number. Founder alert, severity high. See §11.5.
  131026  → recipient_state = UNDELIVERABLE        # recipient cannot receive
            Skip; mark; no retry this campaign.
  130472  → recipient_state = MARKETING_HOLDOUT    # Meta experiment holdout user
            Not billed. NOT an opt-out — do not suppress. Skip silently; count separately.
  held_for_quality_assessment (status)
          → recipient_state = HELD; await release or dropped-status webhook.
            If drops cluster (>10% of warm cohort) → auto-pause campaign, founder alert.
```

**Delivered-not-sent accounting:** Meta bills **on delivery** (since 07/2025), and conversion modeling runs on **delivered**, not sent (131049/130472 recipients cost nothing and convert nothing). All economics (§21), campaign results messages to owners (§15), and the message-cost pass-through estimate therefore count **delivered**. The results ledger stores sent / delivered / read / failed-by-code per campaign.

### 11.5 Monitors

All monitors feed the Qualidade dashboard and the Painel alert strip (see §15).

#### 11.5.1 Quality monitors + auto-pause switches

This table is the **single canonical quality ladder** — the eligibility gate's campaign precondition **P4 `channel_health`** (see §10) keys directly off it, and every other section restates it, never redefines it.

| Signal | Source | Threshold → action |
|---|---|---|
| Per-number quality rating | WABA health via management API / `account_update` | **YELLOW → no NEW campaign proposals for this WABA until founder review; already-approved scheduled sends hold** (they are not cancelled). **RED → auto-pause ALL sends and campaigns for that WABA**, founder alert |
| Template pause ladder | 132015 + template status | Pause tiers 3h → 6h → Disabled, per template, driven by blocks/reports/**mutes/archives** over a rolling 7 days — **handled independently by the send engine** (Meta-side, per template). Any pause → campaign halted (§11.4); Disabled → template retired, new template + warming required |
| Block / opt-out rate | suppression events per campaign | Opt-out (all three paths, rolling per campaign) **≥ 1% → flag + the business becomes Gate-C ineligible** (see §3/§6); **≥ 3% → auto-pause new sends for that business** (threshold ASSUMED — operating default, tune with data) |
| Delivery failure rate | error-code counts | 131049+131026 > 20% of a campaign → review list freshness (ASSUMED default) |
| Auto-demotion | — | Meta's tier auto-demotion on low quality was apparently removed Oct 2025 — **[OPEN]**; monitor as if it still exists |

#### 11.5.2 13-day heartbeat

The coexistence integration **silently dies if the salon's WhatsApp Business App isn't opened at least once every 13 days** (`COMPANION_INACTIVITY` / `PRIMARY_INACTIVITY` inside an `account_update` `PARTNER_REMOVED` webhook).

- Track `last_app_activity` per salon (from `smb_message_echoes` / `smb_app_state_sync` traffic as activity proxies; ASSUMPTION — exact freshness signal to confirm at build; also in §23 register).
- **Day 9** with no activity: **Painel alert** (worker creates the alert only, see §7 — nothing is auto-sent).
- **Day 10**: the founder sends the friendly nudge **manually from her own phone** (locked pt-BR copy, see App A): **"abre o WhatsApp do salão hoje pra manter tudo rodando 🙂"**
- **Day 12**: founder calls the salon.
- If `PARTNER_REMOVED` fires anyway: number offline. Recovery is a **full re-onboard** (one-way door, §11.2.1) including a fresh 24-hour history-sync window — treat as a sev-1 ops incident, schedule the redo same-day.

Salons that answer client replies daily (i.e., every healthy salon) never come near 13 days — the heartbeat exists for the vacation/phone-swap edge.

#### 11.5.3 `account_update` and `user_preferences` processing

- `account_update`: every event persisted; `PARTNER_REMOVED` → sev-1 alert (heartbeat death or salon disconnected via app Settings); ban/restriction subtypes → halt sends + alert.
- `user_preferences`: every event persisted append-only (category `marketing_messages`, value `stop`/`resume`); `stop` → suppression write; `resume` → suppression release **only for the Meta-preference path** (a free-text SAIR or a 131050 is never auto-released; see §11.6). There is **no bulk suppression endpoint** — the platform's own suppression list is the single mechanism.

### 11.6 Suppression integration (three paths)

The suppression list is **authoritative over every source system** — a re-imported CSV can never resurrect an opted-out client (locked, see §6; storage in §8; gate check in §10).

| Path | Trigger | Scope | Reversible? |
|---|---|---|---|
| 1. `user_preferences` webhook | Recipient toggles "Offers and announcements" off in WhatsApp | **Global** (business_id NULL, see §8) — permanent until a `resume` event | Only by the recipient's own `resume` |
| 2. Error **131050** | Send bounces off a user who disabled marketing | **Global** (business_id NULL, see §8) — permanent | No |
| 3. Free-text + block | Inbound message matching (liberal, case/accents-insensitive): **SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA** + profanity list; **a WhatsApp block is also treated as opt-out** | Per-business — permanent | **Never auto-removed.** A later documented consent grant (see §14) creates a Branch-A lawful basis, but the suppression row stays unless the founder manually reviews and removes it |

Every suppression write records path, raw evidence (webhook payload / message text / error payload), timestamp, and campaign context — this log is the litigation shield (see §5 case-law pattern: damages attach when a documented stop was ignored) and lives in the records vault (§16). Meta does not parse "SAIR" for you — inbound free-text matching is entirely the platform's responsibility, which is why `messages` webhook consumption is mandatory even though replies are answered by humans in the salon's app.

**No auto-reply on opt-out — ever** (locked, see §6). Suppression is immediate and silent. The opt-out page confirms page-initiated opt-outs; a founder-drafted quick-reply exists in the salon's WhatsApp Business App that the owner MAY send — optional, zero-obligation (see §14/§15/App A). A state-registry hit is a **gate exclusion** logged in `state_registry_checks` (see §8/§10) — it never creates a suppression row.

### 11.7 Interim-BSP contingency (only if Tech Provider approval lags)

If Meta verification/App Review has not cleared by the time the first design partners are ready (see §22 timeline), a stopgap BSP can bridge — with eyes open:

| Option | Terms | Caveats |
|---|---|---|
| **Dualhook** (preferred stopgap) | $12/1, $25/5, $45/10, $99/25 numbers + $3.50/connection; explicit coexistence + embedded signup support; **zero per-message markup** | **[OPEN]** bulk campaign sending is not documented — verify a 180-recipient template send end-to-end before committing a single real salon |
| **Gupshup** | Coexistence in closed beta; $0.001/msg | Support-ticket-gated access; beta = timeline risk |
| Twilio, Bird | — | Do **NOT** support coexistence (documented) — excluded |
| 360dialog | €49/number/mo | Works, but is exactly the fixed cost structure the direct path exists to avoid — last resort only |

**Chatwoot option (self-hosted, open source):** with Chatwoot, **the founder is still the Tech Provider** (embedded signup runs off her own Meta app credentials), so it is not a BSP detour — it is a possible build shortcut for onboarding/WABA management UI. Coexistence supported since v4.5.0 (08/2025). Two **[OPEN]** caveats before relying on it: (1) history sync was marked "later release" — verify it has shipped, because history sync is the consent/relationship-evidence source (§11.2.3); (2) it is an inbox tool — verify it can actually execute a 180-recipient template campaign, or use it only for onboarding/WABA management and send campaigns from the platform's own send engine (§11.4).

Migration note: numbers onboarded via an interim BSP live under that BSP's app. Because a coexistence WABA is non-migratable (§11.2.2), moving a salon to the direct stack later means offboard + re-onboard (§11.2.1 one-way door). Keep the interim cohort as small as possible — ideally zero.

---


## 12. PAYMENTS — ASAAS, PIX-ONLY, SPLIT AT SOURCE

### 12.1 Architecture

Two ordinary Asaas accounts, no platform relationship between them:

| Account | Owner | Role |
|---|---|---|
| **Salon account** | The salon's own CNPJ, opened by the owner (MEI/small-company accounts are first-class at Asaas) | Merchant of record. Every consumer charge is created here. Consumer money lands here. Refunds originate here. |
| **Founder account** | Caixa Cheia SLU (see §20) | Receives the 20% success fee via split at settlement. Never touches consumer money. Also receives the Raio-X audit charge directly — the audit is her own product, sold by her, with **no split** (see §12.7). |

The fee moves by attaching a **payment split** to every consumer charge at creation time: `splits: [{walletId: <founder wallet>, percentualValue: 20}]`. The recipient is identified by `walletId` only (read once via `GET /v3/wallets` on the founder account, or from the Integrações menu); Asaas documents no linking or permission step for split recipients. Asaas' own canonical split example is exactly this shape — an unrelated third party ("João" sells R$200, "Marcelo" receives 20%; the charge is created in João's account and Asaas debits and credits Marcelo's account). You cannot split to your own wallet (Asaas throws an exception), there is no documented minimum split value, and no documented limit on the number of walletIds per charge.

**Hard exclusions (locked, §6):** no Asaas subaccounts, no BaaS, no merchant-of-record posture by the founder, no escrow, no netting, and the founder never holds client money. Creating Asaas accounts *for* salons would trigger Asaas' regulatory homologation regime (60 days, 10-subaccount cap, R$2k per subaccount then blocked) — the salon-opens-its-own-account architecture avoids that regime entirely. The salon's Pix key requires 100% account approval plus prova de vida; track this with the `ACCOUNT_STATUS_*` webhooks during onboarding (see §17).

**PIX only — regulatory rationale.** Pix settles as a real-time gross transfer: the consumer's money arrives in the salon's account at once, final, with the fee split executed at that same settlement instant. There is no receivables schedule, no card-installment agenda, no chargeback window, and therefore nothing that could recharacterize the founder as a party to a payment arrangement, a receivables manager, or a holder of third-party funds — she is a commercial agent whose commission happens to be paid out by the salon's own PSP at the salon's standing instruction (the mandate-to-split clause in the service contract, see §5 and §20). Adding credit card would import receivables scheduling, chargebacks, and antecipação mechanics into this clean picture and is **prohibited without a new legal review** (locked decision, §6).

**Every payment flows through an API-created cobrança — product rule.** The split rides on a *charge*. A static QR code on the counter, or a consumer sending Pix directly to the salon's key, produces **no split** — the fee would silently not exist and attribution would collapse into a reconciliation argument. Therefore the offer page (§13) is the only purchase path, its checkout always calls `POST /v3/payments` and renders the charge's own QR, and the onboarding script (§17) tells the owner explicitly: campaign clients pay through the link, never through the counter QR.

### 12.2 The API integration

Base URLs: production `https://api.asaas.com/v3` (ASSUMPTION: standard Asaas production host; confirm during the Week-1 test), sandbox `https://api-sandbox.asaas.com/v3` (sandbox keys are prefixed `$aact_hmlg_`). All calls are made with the **salon's** API key (custody rules in §12.6) except reads of the founder's own account.

**Create the charge (just-in-time, from checkout — see §13.2):**

```http
POST /v3/payments
{
  "customer": "<asaas customer id, created via POST /v3/customers with name + CPF/phone>",
  "billingType": "PIX",
  "value": 900.00,
  "dueDate": "2026-09-15",
  "externalReference": "charge:<charge_uuid>",
  "description": "<package name — owner-authored, generic-safe>",
  "splits": [
    { "walletId": "<FOUNDER_WALLET_ID>", "percentualValue": 20 }
  ]
}
```

`externalReference` is always **`charge:{charge_uuid}`** — the internal charge UUID, nothing else. Campaign and client linkage live in local columns on the charge row (campaign_id; client_id resolved at checkout, §13.2), never in the reference string. There is no "offer" entity.

`PaymentSplitRequestDTO` fields available: `walletId` (required), `fixedValue`, `percentualValue` (4 decimals), `totalFixedValue` (installments — unused, PIX only), `externalReference`, `description`. We use `percentualValue: 20` on every normal charge; `fixedValue` is used in exactly one case — the credit-boundary charge of §12.7 — and never elsewhere (elsewhere it would break refund pro-rating and the netValue symmetry below). The 10% fallback fee (founder-only lever, §3) is the same payload with `percentualValue: 10`.

**Render the Pix QR:**

```http
GET /v3/payments/{id}/pixQrCode
→ { encodedImage (base64 QR), payload (copia-e-cola string), expirationDate }
```

**Webhooks to consume** (one endpoint per concern in the Next.js app, §7; every delivery stored raw in an append-only table before processing; idempotent by event id):

1. **Payment lifecycle events** — created / received (Pix settlement) / refunded. On the settlement event: mark the charge settled, write the split-ledger row, issue the voucher (§13.3), send the buyer's voucher/receipt email (Resend, §7). No automated owner message is sent (§15.11 channel model). *(Confirm the exact event-name enum against the Asaas webhook docs during the Week-1 sandbox test; this document locks the semantics, not the strings.)*
2. **Split events** — `PAYMENT_SPLIT_DIVERGENCE_BLOCK` (see §12.5); `PAYMENT_SPLIT_FEE` **[OPEN]** (appears in the webhook enum but is undocumented — obtain a written definition from Asaas commercial before launch; treat any delivery of it as an alert-and-halt for that charge until defined).
3. **Account status events** — `ACCOUNT_STATUS_*` on the salon account for onboarding/KYC tracking (Pix key needs full approval + prova de vida).
4. **Transfer-authorization webhook** on the salon account — part of key custody (§12.6): any transfer initiated with the stored key requires out-of-band authorization, so a stolen key cannot silently drain the salon.

**Split status lifecycle:**

```
PENDING → AWAITING_CREDIT → DONE
                     ↘ REFUSED   (refusalReason, e.g. RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT)
DONE → PROCESSING_REFUND → REFUNDED   (cancellationReason: PAYMENT_REFUNDED, WALLET_UNABLE_TO_RECEIVE, …)
```

The split executes **at settlement, instantly, and cannot be scheduled**. Fee revenue is recognized in the internal ledger only when the split status reaches `DONE` — "settled netValue" in the locked fee definition (§6) means exactly this.

**netValue math — the fee computes on net, and the salon bears the Asaas fee.** The split percentage applies to `netValue` = charge value minus the Asaas Pix receiving fee. Standard published pricing: Pix in R$1.99 per charge (R$0.99 for a 3-month promo window), Pix out 30 free transfers/month then R$2, no mensalidade. Reference example, used everywhere in this document:

```
Charge value            R$ 900.00
Asaas Pix fee           −R$   1.99      (salon bears it)
netValue                R$ 898.01
Founder split (20%)     R$ 179.60      ← NOT R$180.00
Salon receives          R$ 718.41
```

**Live-fee rule — never hardcode.** The Pix fee can be percentage-with-cap, promo-discounted, or renegotiated. Before computing any expected fee (margin gate §10 math, refund workbench, reconciliation), read the salon's real fee schedule live:

```http
GET /v3/myAccount/fees
→ { fixedFeeValue, percentageFee, minimumFeeValue, maximumFeeValue, discountExpiration }
```

Cache per salon with a short TTL; recompute on `discountExpiration`. Any code-review diff that introduces a literal `1.99` fails review.

### 12.3 The sandbox-then-production go/no-go test (Gate #1, Week 1)

**Why this is a gate.** Asaas hard-blocks *transfers* between unlinked accounts ("Não é possível realizar transferências … sem vínculo"). The split documentation contains no equivalent restriction, the FAQ distinguishes the two mechanisms, and Asaas' own canonical example is an unlinked third-party split — but **documented silence is not verified permission**. The entire fee rail depends on an unlinked-account split executing in production. Test it before writing anything else.

**Test design constraint (critical):** account B (the founder-role account) must be registered **independently** at sandbox.asaas.com through the normal signup — **never** created via `POST /v3/accounts` from account A. An API-created account is a *subaccount*, which tests the wrong case (the case this architecture deliberately avoids) and would pass even if unlinked splits are blocked. And because the sandbox auto-approves accounts and cannot prove production-side compliance checks, **the whole script re-runs in production at R$5** before the result counts.

**The script (sandbox first, then production at R$5):**

1. Register account A (salon role) and account B (founder role) independently at sandbox.asaas.com. Read B's `walletId` via `GET /v3/wallets` with B's key.
2. With A's key: create a customer, then `POST /v3/payments` — `billingType: PIX`, `value: 900.00`, `splits: [{walletId: <W_B>, percentualValue: 20}]`.
   - **Assert:** HTTP 200 and `splits[0].status = PENDING`.
   - **A 400/403 here = NO-GO** → stop; move to the Efí fallback (below).
3. Confirm the payment **in the sandbox web UI** — there is no API endpoint for payment confirmation in sandbox.
4. **Assert:** `netValue ≈ 898.01`; split value ≈ `179.60`; B's balance rose by the split amount; split status reaches `DONE`.
5. Full refund of the charge. This may 400 on a just-received charge — compensation/notification fees are not returned to A's balance; top up A and retry (this same behavior is a production runbook item, §12.4).
   - **Assert:** `refundedSplits[].done = true`; `splits[0].status = REFUNDED`; B's balance fell by the split amount.
6. New charge; partial refund via `POST /v3/payments/{id}/refund` with `splitRefunds: [{id: <split_id>, value: <amount>}]`.
   - **Assert:** the partial amounts reverse exactly as computed by the pro-rata formula in §12.4.
7. Exercise the failure modes: (a) split to a wallet whose account has incomplete KYC → expect `WALLET_UNABLE_TO_RECEIVE`; (b) update the payment sending `splits: []` → confirm the split is **silently disabled** (this is real and is why the guard in §12.5 exists).
8. **Negative-balance probe [OPEN]:** withdraw B's balance to zero, then refund a settled-and-split charge. Record whether Asaas forces B negative, queues a debit, or fails the reversal. This behavior is unverified and shapes the founder's cash-buffer policy (§21).
9. **Production re-run at R$5:** repeat steps 1–6 with the real founder account and a real (design-partner or founder-controlled) salon account, `value: 5.00`. Same assertions, proportional values.

**Pass** = every assertion holds in production. **Fail at any assertion** = NO-GO on Asaas → fallback is **Efí (Gerencianet)**, which names a "Split Pix" product — verify its recipient model supports unrelated third-party recipients before committing (Woovi/OpenPix unchecked second option; Iugu and Pagar.me are unsuitable master/sub platform models). A NO-GO here changes §12.2's payloads but nothing else in this document's commercial logic.

### 12.4 Refunds engine

**Full refund = automatic.** A full refund of a charge auto-reverses the split: `refundedSplits[].done = true`, split status → `REFUNDED`, the fee leaves the founder's balance. Nothing to build beyond ledger updates and the credit-restore rule (§12.8).

**Partial refund = the engine you must build, because partial is the NORMAL case.** A partial refund does **not** touch the split unless you say so. The call is:

```http
POST /v3/payments/{id}/refund
{
  "value": <refund amount to the consumer, at root>,
  "splitRefunds": [
    { "id": "<split_id>", "value": <founder-fee amount to reverse> }
  ]
}
```

The root `value` goes back to the consumer from the salon's balance; each `splitRefunds` item claws the stated amount back from that split's recipient. Pix supports multiple partial refunds up to the original total.

Why partial is normal, not an edge case: a prepaid package is redeemed over months. CDC art. 49 gives a 7-day full withdrawal (sold by link = fora do estabelecimento; full immediate refund "a qualquer título", monetarily updated). After day 7, a cancellation of a partly-used package legally requires a **proportional refund of unused value** — total forfeiture is void (CDC arts. 51 II/IV, 39 V), used sessions may be re-priced at the avulso rate only if the avulso price and the exact cancellation arithmetic were disclosed in writing before purchase (TJDFT Acórdão 2110685; this is why the offer page carries them — §13.1). So the system's steady state includes mid-life partial refunds, and every one must reverse the founder's fee pro-rata — the fee is success-only and **refund-reversed** by constitution (§6).

**The pro-rata formula (locked rule of this spec):**

```
split_refund_value = round( original_split_value × consumer_refund_value / original_charge_value , 2 )
```

Pro-rate against the original *charge* value (what the consumer sees and what the refund is quoted against), applied to the original *split* value (which already embeds the netValue fee math). This keeps the founder's retained fee exactly 20% of the salon's retained net at every point in the voucher's life.

**Worked example** (illustrative figures; the R$900 reference package used throughout this document, session count and avulso price ASSUMED for arithmetic):

- Package: R$900.00, 6 sessions, avulso price disclosed on the offer page: R$180.00/session.
- Original split: R$179.60 (from §12.2).
- Client uses 2 sessions, then cancels (after day 7).
- Consumer refund per the disclosed arithmetic: `900.00 − 2 × 180.00 = R$540.00`.
- Split reversal: `179.60 × 540.00 / 900.00 = R$107.76`.
- Payload: `{ "value": 540.00, "splitRefunds": [{ "id": "<split_id>", "value": 107.76 }] }`.
- End state: combined retained net R$358.01 (salon R$286.17 + founder R$71.84 ≈ 20% of retained net — within centavos, because the pro-rata runs on the charge value, not netValue).

**Refunds workbench (Dinheiro dashboard, §15) prefills** every field so the founder never does this arithmetic by hand: payment id and original value from the split ledger, split id and original split value from the same row, sessions used from the voucher redemption ledger (§13.3), avulso price and any pre-disclosed admin fee from the stored offer record, live Asaas fee from the cached `GET /v3/myAccount/fees`. Output: the consumer refund value, the `splitRefunds` payload, and a preview of both balances after execution. One confirm button; the raw request/response is stored append-only.

**Two production runbook items:**

- **Refund of a fresh charge can 400** — Asaas' compensation/notification fees are not returned, so the salon's balance may not cover the reversal minutes after settlement. Handling: catch the 400, show the founder the exact shortfall, and instruct the salon to top up its Asaas balance ("o valor da taxa do Pix não volta — o salão cobre a diferença"); retry after top-up. The salon funds the gap — never the founder.
- **Negative-balance behavior [OPEN]** — see test step 8 in §12.3. Until answered, the founder keeps her Asaas balance above the sum of splits `DONE` in the trailing 7 days as a reversal buffer.

### 12.5 Risk monitors

Four standing monitors run in the Node worker (§7); all surface on the Painel alert strip (§15).

1. **Pledged receivables — `RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT`.** Antecipação de recebíveis is routine for cash-strapped salons; if the salon has pledged its receivables, the split returns `REFUSED` with this `refusalReason` and the fee silently never arrives. Monitor: every split row is polled/webhook-tracked until `DONE`; any `REFUSED` fires an alert with the reason. **Billing fallback:** the fee for the affected settlements is invoiced instead — NFS-e to the salon (queued with `item_source = billing_fallback`; see §20 for the nota mechanics) plus a Pix cobrança created on the founder's own account for the salon to pay. The campaign is not paused for one refusal; a second refusal on the same salon pauses new campaigns for that salon until the owner explains the pledge.
2. **`WALLET_UNABLE_TO_RECEIVE`** — the founder's own account KYC is incomplete or restricted; splits cancel with this reason. Alert severity: highest (every fee in flight is affected). Preventive: complete founder-account approval before the first production charge; the go/no-go script exercises this failure deliberately.
3. **`PAYMENT_SPLIT_DIVERGENCE_BLOCK`** — a split-vs-net divergence blocks the funds for 2 business days. The only known cause in this design would be a fee-schedule change mid-flight; on receipt, re-read `GET /v3/myAccount/fees`, recompute, and alert. No automatic remediation.
4. **`splits: []` silent-disable guard.** Updating a payment with an empty `splits` array silently removes the split. Code-level guard: the payment-update wrapper **never** serializes the `splits` key unless the call site explicitly passes a non-null splits intent; additionally, after any update call, the payment is re-read and the presence + values of the split are asserted; a missing split raises a blocking alert before the charge can settle unsplit. **Exemption:** charges flagged `charges.credit_drawdown = true` (§12.7) are deliberately created without a split and are exempt from this guard — the guard fires only on charges that should carry one.
5. **`PAYMENT_SPLIT_FEE` [OPEN]** — in the webhook enum, undocumented. Get the written definition from Asaas commercial (Week-1 task); until then, log + alert on any occurrence.

### 12.6 API-key custody — the vault and the trust conversation

**Asaas has no OAuth.** There is no scoped-token or delegated-permission model: the founder holds each salon's **full API key**, and a full key can move the salon's money. This is the single largest trust asymmetry in the product and it is handled in two layers.

**Technical layer — the key vault (build spec):**

- Keys encrypted at rest (envelope encryption; master key in the platform secret manager, per §7), never present in code, logs, error messages, or LLM context (hard rule, §7).
- Per-salon **named keys** — Asaas supports up to 10 named keys per account, **with expiry**: the onboarding script creates a key named `caixa-cheia-<year>` with a 12-month expiry, rotated annually.
- **IP allowlist** on the key, restricted to the worker's and app's egress IPs.
- **Transfer-authorization webhook** enabled on the salon account, so no transfer executes on API say-so alone.
- **Access log:** every decrypt/use of a key writes an append-only row (timestamp, purpose, charge id). This log is shown to the owner on request — it is a feature, not just a control.

**Human layer — the trust conversation (scripted into onboarding, §17):** the founder says, in plain Portuguese, that the key she stores can in principle move money; that it is created named and expiring, locked to her servers' IPs, that transfers require the owner's separate authorization, and that every use is logged and viewable. She never asks for the owner's password, and the owner creates the key on their own screen during the guided session. Refusing to have this conversation, or hiding the asymmetry, is the kind of shortcut that converts a technical risk into a reputational one.

### 12.7 Credit ledger — the Raio-X credit

The audit (R$490 single-site / R$990 per group of up to 8 locations, one-time, see §3 and §19) is **100% credited against the first success fees**, valid 12 months, refund-symmetric. Mechanics:

- **The audit charge itself is created on the FOUNDER'S account, with no split** — it is her own product sold directly; the salon is her customer for it. (`POST /v3/payments` on her account, `billingType: PIX`, value 490.00 or 990.00; on the Pix confirmation webhook the Raio-X **auto-releases**: an automatic transactional email delivers the private URL to the owner, and the dashboard flips to "released" and renders the WhatsApp-ready message the founder forwards manually from her own phone — §15/§19.)
- On settlement, a **credit-ledger** row opens for that salon (or group): `credit_total`, `credit_remaining`, `expires_at = settlement + 12 months`.
- **Drawdown rule (DERIVED design):** while `credit_remaining > 0`, consumer charges for that salon are created **without a split** and flagged `charges.credit_drawdown = true` (which exempts them from risk guard #4, §12.5); the fee that *would* have been split (20% of expected netValue, live fees from §12.2) is debited from the credit ledger at settlement instead, as credit-ledger drawdown entries. Once `credit_remaining` reaches zero, normal `percentualValue: 20` splits attach again on every new charge. Rationale: the alternative — split normally and rebate the credit back — is foreclosed because Asaas blocks transfers between unlinked accounts (§12.3); withholding the split is the only clean mechanical form of "crédito que volta inteiro".
- **Boundary charge (credit exhausts mid-charge):** the single charge whose full fee would exceed `credit_remaining` carries a **`fixedValue` split equal to the uncovered remainder of the fee** (Asaas supports `fixedValue`; this is the one sanctioned `fixedValue` use, §12.2) — the covered portion draws down the last of the credit, the uncovered remainder arrives as a real split. No extra owner payment step, no NFS-e + cobrança detour. After the boundary charge, normal `percentualValue: 20` splits resume.
- **NFS-e for credited fees:** fee amounts consumed from credit are still invoiced — queued with `item_source = credit_drawdown` (§12.8) — so the nota trail stays unbroken.
- **Refund-symmetric restore:** if a charge whose fee was drawn from credit is later refunded (fully or pro-rata per §12.4), the drawn amount (pro-rata) is **restored** to `credit_remaining` — the credit only burns against fees that stick, exactly as the fee itself only exists on settled, unrefunded revenue. Expiry date does not extend on restore.
- Never charged twice; Raio-X regenerations are free (§3). The credit ledger is visible on the Salão detail and Dinheiro dashboards (§15) and in the owner's monthly ledger message.

### 12.8 Reconciliation — settlement → split ledger → NFS-e

One unbroken trail, so that any fee the founder ever received can be walked back to a settled consumer payment and forward to a nota fiscal:

```
Asaas settlement webhook (payment settled, split DONE)
   → split_ledger row: {payment_id, charge value, netValue, asaas_fee,
     split_id, split_value, split_status, business_id, campaign_id,
     externalReference (charge:{charge_uuid}), credit_drawdown}
   → monthly NFS-e queue (nfse_queue; v1 issuance is MANUAL from this
     queue — the worker only builds it, §15): one nota per salon per
     month, to the SALON (never the consumer — §20), value =
     Σ split_value DONE − Σ split reversals + credit-drawdown and
     billing-fallback items (item_source enum:
     split|credit_drawdown|billing_fallback; split_ids nullable),
     referencing the underlying payment_ids
   → reconciliation view (Dinheiro, §15): internal split ledger vs
     Asaas' own split/settlement reports, diffed line-by-line; any
     unmatched row is an alert, not a footnote.
```

The refund workbench writes reversal rows into the same ledger; the credit ledger's drawdown rows appear as fee events with `charges.credit_drawdown = true` and no split_id (the boundary charge alone carries both a drawdown portion and a real `fixedValue` split, §12.7). This trail is also the tax defense: the PSP's split reports tie each settlement to each NFS-e (§20), proving the founder's receita bruta is the 20% and nothing else.

## 13. OFFER PAGE, CHECKOUT, VOUCHER

### 13.1 The offer page

One page per campaign offer, at an **opaque, stable, per-campaign URL**: an unguessable slug (`/o/<random-token>`, stored as `campaigns.offer_page_slug` — §8), no client PII or sequential IDs in the URL, stable for the life of the campaign so the link in an already-delivered WhatsApp template never dies. The same URL serves every recipient — the page is about the offer, not the person; the WhatsApp template's URL-button variable carries this campaign token (same value for every recipient in the send).

**Offer window.** `campaigns.offer_valid_until` (§8) is the single source of the offer's end date: it fills the template's validity-date body variable ({{3}}), it is the prominent validity shown on this page (row 4 below), and at that instant the page **stops issuing new charges**. The campaign's settling state closes (settling → settled, or zeroed if nothing sold — §8.7) 48 hours after the last outstanding charge expires following `offer_valid_until`.

**Mandatory content checklist (CDC / TJDFT-driven — a page does not ship unless every row is present):**

| # | Element | Why (see §5) |
|---|---|---|
| 1 | Package name | Owner-authored commercial content |
| 2 | Total price (R$, centavos) | CDC transparency |
| 3 | Number of sessions | Defines the pro-rata math |
| 4 | Validity period, prominent | Expiry is enforceable ONLY if prominently pre-disclosed |
| 5 | **Avulso per-session price** | TJDFT Acórdão 2110685: used sessions may be re-priced at avulso rate only if disclosed in writing before purchase |
| 6 | **Exact cancellation arithmetic**, worked in numbers ("cancelou depois de usar 2 de 6 sessões: devolvemos R$900 − 2 × R$180 = R$540") | Same acórdão; total forfeiture is void; generic operating costs can't be passed on |
| 7 | 7-day withdrawal notice + how to exercise it, same channel | CDC art. 49; Decreto 7.962/2013 art. 5 |
| 8 | **Salon CNPJ, razão social, address** | CDC art. 42-A — the salon is the seller (§6) |
| 9 | Any admin fee on cancellation (modest, pre-disclosed only) | Tolerated only if disclosed |
| 10 | **Privacy-notice link + unticked consent checkbox** (single checkbox, scope `whatsapp_marketing`; NEVER a condition of purchase or price; ticking it writes a `consents` row — source `offer_page`/`checkout`, evidence_class `native_capture`, per §8.3) | LGPD; offer page/checkout are consent-capture sources (§14) |
| 11 | **Voucher redemption terms**: valid only at the issuing salon/group — cross-salon redemption prohibited | Locked (§6); §13.3 |
| 12 | Footer: the single locked line "tecnologia Caixa Cheia" and nothing else | Branding boundary (§6) |

**Owner-authored commercial content rule (Option B boundary, §5):** the package description — name, what it includes, price, session count — is written or approved by the salon owner as *commercial* content. It is never derived from, joined to, or informed by any client record. The page may name a service ("pacote de 6 sessões de laser") because it describes what the salon sells to the public; the WhatsApp template that carries the link never does (§11).

**Design rules:** mobile-first (all traffic arrives from a WhatsApp tap; templated messages render no URL preview card, so the page is the first visual the offer ever gets — it must load fast and land the price immediately). **No external trackers**: no Meta pixel, no analytics scripts, no fonts or assets from third-party origins — data-minimization posture (§5) and page speed. First-party page-view counting only. Founder branding is **subordinate**: a single footer line, locked copy — "tecnologia Caixa Cheia" — nothing else; the salon's name and identity own the page (§6).

### 13.2 Checkout flow

1. Client taps the URL in the WhatsApp template → offer page.
2. Client taps the buy button → enters name + CPF + phone (minimum needed to create the Asaas customer and the voucher). **Client resolution:** the buyer's phone is matched by E.164 against the business's imported clients to resolve `client_id` — **nullable when unmatched** (a forwarded link is a legal sale; the buyer's `buyer_name` + `buyer_phone_e164` are recorded on the voucher regardless — §8).
3. **Charge is created just-in-time** — `POST /v3/payments` on the salon's account with the split attached at creation (§12.2), `dueDate` = next day. Charges are never pre-created per recipient (most recipients won't buy; dead charges pollute the salon's Asaas account). If the same client re-opens checkout while a pending charge for this offer is unexpired, the existing charge is reused — no duplicates.
4. `GET /v3/payments/{id}/pixQrCode` → page renders the QR image and the **copia-e-cola** string with a copy button (on a phone, copia-e-cola is the primary path; the QR serves someone paying from a second device).
5. Page polls charge status / the settlement webhook fires → confirmation screen: "Pagamento confirmado ✔" + the voucher link, and the voucher URL is also recorded so the salon can resend it from its own WhatsApp thread.
6. Settlement webhook also: writes the split-ledger row (§12.8), marks the campaign result (§15). The owner sees the Pix land in the salon's own Asaas account (touch 8, §17) — no automated owner message is sent.

If the charge expires unpaid, the offer page simply issues a fresh one on the next tap — until `campaigns.offer_valid_until`, after which the page stops selling (§13.1). No dunning, no reminders — one message per client per campaign is the product's contract with the recipient (§11).

### 13.3 Voucher page

Issued on settlement, at its own opaque URL, delivered on the confirmation screen (and resendable by the salon). Contents:

- **Voucher code + QR** (the code encoded as QR for the front desk to scan).
- Package name, salon name/CNPJ, purchase date, validity end date.
- **Sessions remaining** (large), out of total.
- **Redemption history**: one dated line per session used.
- Link to the cancellation terms as disclosed at purchase (frozen copy of the offer-page arithmetic — the version the client actually bought under, not the current one).

**One-tap redemption (how the salon marks a session used):** the client shows the voucher (screen or code); the receptionist scans the QR or opens the salon-side magic link for that voucher — no login, per the owner-experience budget (§17) — and taps **"Confirmar uso"**; a confirmation dialog shows client name + sessions remaining; confirm appends a timestamped row to the redemption ledger (`recorded_via` values per §8) and decrements the counter. This tap is the **redemption micro-behavior** — one of the two standing micro-behaviors accepted at onboarding alongside the 8 owner touches (§17); founder-side weekly reconciliation chases unredeemed and expiring vouchers so nothing depends on the salon remembering. Mis-taps are undoable for 10 minutes by the same link (ASSUMPTION: undo window; pick any short value at build), after which corrections go through the founder with a logged reason.

The per-client redemption ledger is the salon's litigation defense in any package dispute — dated, per-session, tamper-evident (append-only). It is pitched as a feature, and it is also what makes the pro-rata refund arithmetic (§12.4) mechanical instead of contested. Voucher state machine (issued → partially_redeemed → redeemed; refund_requested → **refunded** (terminal, full refund) or **refunded_partial** (partial refund reduces sessions; the voucher continues live)) is specified in §8.7's state-machine list; redemption is valid **only at the issuing salon/group** — cross-salon redemption is prohibited forever (§6).

### 13.4 Refund request path

Decreto 7.962/2013 art. 5 requires that withdrawal be exercisable **through the same channel** the sale used, with immediate reversal instruction. Implementation:

- The voucher page (and the offer page's terms section) carries a **"Quero cancelar / devolução"** link → a one-field request form (reason optional) that opens a `refund_requested` state on the voucher and notifies both the salon and the founder.
- Because the sale happened over WhatsApp + web, a WhatsApp message to the salon saying the client wants to cancel counts too — the salon owner forwards/flags it, and the founder opens the same workflow manually. Same-channel is a floor, not a script.
- **Within 7 days of purchase (CDC art. 49):** full refund, immediate, monetarily updated — the workbench (§12.4) prefills the full-refund payload; no negotiation, no admin fee.
- **After 7 days:** pro-rata per the arithmetic disclosed on the offer page at purchase time — the workbench prefills from the frozen offer terms and the redemption ledger.
- **Refunds always originate from the salon's Asaas account** (§6): the refund API call runs against the salon's charge, consumer money returns from the salon's balance, and the split reversal makes the founder's fee follow symmetrically. Refund SLA surfaced on the Painel as "refunds due" alerts (§15).


## 14. CONSENT CAPTURE SYSTEM

Every campaign at launch runs on legitimate interest (the gate in §10, the legal analysis in §5). Consent is the better basis, and the system is built to migrate every salon's base from LI to documented consent, client by client, without the owner doing anything beyond printing one card. This section specifies the capture surfaces, the storage schema, the versioning and revocation rules, and the hard rules that keep captured consent valid under Art. 8 LGPD.

### 14.1 The QR card

The founder dashboard generates, per salon, a print-ready A5 PDF (one click from the Salão detail screen, see §15):

| Element | Content |
|---|---|
| Headline | Salon's own name and logo (uploaded at onboarding); Caixa Cheia branding limited to a footer line |
| Body | One sentence inviting the client to receive offers by WhatsApp (pt-BR, see App A) |
| QR code | Deep link to the salon's consent capture page: `/c/{token}` — an opaque per-salon token (one per card version); the token resolves to the salon and to the capture source (`qr_card`), which is stored on the consent row |
| Footer | "Saiba como usamos seus dados: [QR/link]" — second QR pointing to the salon's privacy notice (current version, see §16) |

The card sits at reception next to the card machine. The owner prints it once (owner step #5 of the 8-step budget, see §17). Each salon's QR is unique; scans are attributed to that salon and that card version.

### 14.2 The capture page

A single mobile page, no login, loading in under a second on 3G. Structure, top to bottom — order is load-bearing:

1. **Notice first (Art. 9).** Before any checkbox is visible without scrolling past it: who the controller is (the salon, with CNPJ), what will be sent (promotions, offers, news about the salon's services), on which channel (WhatsApp, to the number the client provides), how to stop (reply SAIR, free), and a link to the full privacy notice. The notice is displayed, not linked-only.
2. **Phone field.** Client enters their WhatsApp number (masked input, stored E.164).
3. **The consent checkbox — unticked, unbundled, its own element.** Never pre-checked, never combined with any other agreement, never inside terms-of-service text. The exact displayed string is this locked pt-BR copy, verbatim, with the salon's name and CNPJ interpolated:

> ☐ Autorizo o [SALÃO] (CNPJ …) a me enviar mensagens por WhatsApp, no número que informei, com promoções, ofertas e novidades sobre seus serviços. Posso cancelar quando quiser, de graça, respondendo SAIR. Não autorizar não muda em nada o meu atendimento.

   Followed by: "Saiba como usamos seus dados: [QR/link]".

4. **Two submit paths:** "Autorizar" (records a grant) and "Agora não" (records a refusal). Refusals are stored, not discarded — a documented refusal is an exclusion the gate must honor and evidence that the process is real (see §16 exclusion log).

At launch there is exactly ONE checkbox and ONE scope: `whatsapp_marketing`. Granular per-campaign-type scopes (birthday, package-renewal, slow-day) are an ASSUMED post-launch extension — no granular boxes on the launch page, and the gate (§10) does not key on scope.

Generic wording never substitutes for this text: "receber novidades" does not cover discount offers — Art. 8 §4 voids generic authorizations. Any salon-requested rewording goes through the version process below and, if it broadens scope, through the lawyer (week-1 checklist, §24).

### 14.3 The reception script

One line, spoken by whoever is at the desk while the client pays. The checkbox copy is locked (App A); the spoken line is not — the following is DERIVED copy consistent with the locked text (pt-BR, to be confirmed with the lawyer alongside the LIA template):

> "Quer receber as promoções do salão no seu WhatsApp? É só apontar a câmera aqui — e pra sair é só responder SAIR, quando quiser."

**The script is OPTIONAL.** The card works standalone at reception; saying the line is not an owner or staff obligation and adds nothing to the owner budget (§17). Two properties are mandatory in any variant that IS used: it must mention the free exit, and it must never mention a discount for signing (see 14.10). Staff never tick anything on the client's behalf; the client's own device does the capture.

### 14.4 Storage schema

Consent records live in the append-only `consents` table — the canonical DDL is §8.3; this section restates it (implementation pattern in §16.2):

```sql
consents (
  id                uuid primary key,
  business_id       uuid not null,
  client_id         uuid,            -- NULLABLE: QR captures may precede import; linked later by phone
  phone_e164        text not null,
  value             text not null,   -- 'granted' | 'refused' | 'revoked'
  source            text not null,   -- 'qr_card' | 'offer_page' | 'checkout' | 'fresha_import' | 'observacao_marker' | 'manual'
  evidence_class    text not null,   -- 'native_capture' | 'imported_boolean' | 'marker'
  displayed_text    text,            -- the EXACT string shown, fully interpolated (salon name, CNPJ); NOT NULL for native_capture, NULL allowed for imports
  text_version      text,            -- e.g. 'v1.0-2026-09'; NOT NULL for native_capture
  notice_version    uuid,            -- references notices(id) (§8.3); version in force at capture
  scope             text not null,   -- fixed string 'whatsapp_marketing' at launch (granular scopes = ASSUMED post-launch extension, §14.2)
  staff_identifier  text,            -- who was at the desk, when the salon can say (name or code); null for self-serve QR
  ip_hash           text,            -- optional; hashed, for dispute forensics
  captured_at       timestamptz not null   -- America/Sao_Paulo, stored UTC
)
```

The row is the Art. 8 §1 proof: exact string + version + timestamp + source. One row per decision event; a client's current status is the latest row per (phone_e164, business_id). Rows are never updated or deleted — revocation and re-grant are new rows.

### 14.5 Version changes → re-consent

Every distinct `displayed_text` template gets a `text_version`. Rules (DERIVED — the copy is locked, the change procedure is not; lawyer confirms with the LIA sign-off, week-1 checklist §24):

- **Non-material edits** (typo, formatting): new version number; existing grants remain valid.
- **Material edits** (purpose broadened, new channel): existing grants remain valid **only for what the old text authorized**. Sends relying on the broadened text require a fresh grant under the new version. The gate evaluates a grant against the version the client actually saw — it never assumes the current text.
- Consent captured under a retired version never silently upgrades. There is no bulk "migrate consents" operation in the codebase.

### 14.6 Revocation

"Posso cancelar quando quiser, de graça, respondendo SAIR" must be true everywhere, always:

- **SAIR (or any liberal-match stop word — SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA, plus profanity; full matcher in §11) received on the salon's number** → a `revoked` row is appended, the phone enters the suppression list (§11) immediately and silently — **no automated confirmation reply, ever** (constitution #9, §6: no bot). A founder-drafted quick-reply exists in the salon's WhatsApp Business App that the owner MAY send — strictly optional, zero-obligation, not part of the owner budget (§17); copy in App A.
- **A WhatsApp block or `user_preferences` stop webhook** → same suppression, same `revoked` row; the triggering event (matched stop word, webhook id, block signal) is preserved in the opt-out log (§16.1), which is the evidence record for the revocation.
- **Page-initiated opt-outs** are confirmed by the opt-out page itself — the only surface that confirms anything.
- Revocation is free, immediate, and never argued with. The suppression list is authoritative over every source system (constitution #15, §6): a re-imported CSV can never resurrect a revoked or opted-out client.

### 14.7 How consent replaces LI in the gate

Consent and LI are the two branches of per-client check **C2 `lawful_basis`** (§10). Each client row carries a derived `basis` field, computed at gate time:

| `basis` | Condition | Gate path |
|---|---|---|
| `consent` | Latest `consents` row is `granted`, not revoked (C2 **Branch A**) | The LI window conditions do not apply; every other per-client check (C1, C3–C9) and the campaign preconditions (P1–P4) still run |
| `li` | No grant on record, no refusal; last visit inside the business cadence window and ≤360 days (C2 **Branch B**) | Full Branch-B path (§10) |
| `blocked` | Latest row is `refused` or `revoked`, or phone is suppressed (C5) | Excluded, logged with reason |

A documented **refusal beats LI**: a client who tapped "Agora não" is excluded even if every Branch-B condition passes. Over roughly one service cycle (weeks), the QR card converts the active base from `li` to `consent`; the Salão detail screen shows consent % per location (§15) so the founder and owner watch the migration happen. LI and consent tracks run concurrently — LI is not switched off when consent capture starts.

### 14.8 Fresha import mapping

Fresha is the only servable system with structured consent: export columns **"Accepts marketing"** and **"Accepts SMS marketing"** (booleans). Mapping:

- `Accepts marketing = TRUE` → a `consents` row with `value = 'granted'`, `source = 'fresha_import'`, `evidence_class = 'imported_boolean'`, `displayed_text = NULL` (the original wording is not exported), `captured_at` = import timestamp (the original tick date is not in the export).
- `FALSE` → a `refused` row, same evidence class — a gate **Branch-A exclusion (C2), NOT a suppression row**. A Fresha FALSE excludes the client exactly like a refusal.

A boolean is **weaker evidence** than the native tuple — no exact string, no original timestamp, no staff, no version. The gate treats `imported_boolean` grants as valid to send, but the migration plan still targets these clients with the QR card to upgrade them to `native_capture`. The Raio-X and dashboards report them separately.

### 14.9 The Observação-parsing rule

Industry practice (Belle Software's LGPD guide) is a consent URL or note pasted into the client's `Observação` free-text field. The importer normally drops free-text fields at parse time (allowlist, §9). Exactly one exception: **forward-looking markers only**. If, after Caixa Cheia onboarding, the salon adopts a documented marker convention (e.g. staff paste a defined token recording that the client signed the physical consent card on a given date), the importer MAY parse that specific token into a consent row with `source = 'observacao_marker'`, `evidence_class = 'marker'`.

**Never retrofit.** Pre-existing tags, notes, or URLs in Observação are NOT parsed and NOT treated as consent: retrofitting meaning onto old free-text is not Art. 8-valid evidence. The classifier drops historical Observação content entirely (content never stored; column name logged in the dropped-columns receipt, §16).

### 14.10 Hard rule: consent is NEVER discount-conditioned

No surface — QR card, capture page, reception script, offer page, template copy — may ever offer a discount, gift, points, or any advantage in exchange for ticking the box. Why this is absolute: conditioned consent is not freely given (the Febrafar/ANPD trap), and the Procon-MG enforcement pattern around discount-conditioned data collection has produced fines in the R$8.4M+ range. The locked copy's last sentence — "Não autorizar não muda em nada o meu atendimento" — must be literally true. This is enforced in code review as a copy rule and in §18's campaign SOP as a checklist item; there is no override.

---


## 15. DASHBOARDS AND PRODUCT SURFACES

This section specifies every screen in the system, at build fidelity: purpose, user, layout, data elements with source tables, actions, empty/error states, and pt-BR UI strings. There are three surface classes with three different access models:

| Surface class | Who | Access model |
|---|---|---|
| Founder dashboard (10 screens) | Founder only | Authenticated login (single user; email + TOTP per §7.6, stored in `founder_user` + `sessions`, §8) |
| Salon-owner surfaces | Salon owners | **No login.** WhatsApp messages + magic links (signed URLs, 30-day expiry, re-issuable — §7.6). See §15.11 |
| Client-facing pages | End consumers | Public opaque URLs (unguessable tokens). See §15.12 and §13/§14 for business rules |

All UI is pt-BR (the founder is Brazilian). Timezone `America/Sao_Paulo` everywhere. Money displayed as `R$ 1.234,56`, stored as integer centavos (see §7). Table names used below (`businesses`, `locations`, `users`, `clients`, `visits`, `package_balances`, `consents`, `suppressions`, `registry_lists`, `registry_entries`, `state_registry_checks`, `campaigns`, `manifests`, `manifest_entries`, `gate_runs`, `approvals`, `templates`, `sends`, `charges`, `splits`, `refunds`, `refund_legs`, `vouchers`, `redemptions`, `credit_ledger`, `nfse_queue`, `quality_snapshots`, `heartbeats`, `notices`, `documents`, `attestations`, `scan_results`, `audit_reports`, `alerts`, `jobs`, `imports`, `dropped_columns_log`, `lista`, `external_calls`, `history_sync_messages`, `client_merges`, `lint_wordlist`) are the §8 canonical names; §8 is authoritative — any divergence between this section and §8 is a documentation bug to be resolved in favor of §8.

**Design laws for every screen** (derived from the locked decisions, §6):
1. No screen may ever display a clinical/service field — such fields never enter the database (allowlist importer, see §9), so no screen can leak them.
2. Every send-related screen surfaces the gate (§10) — there is no path to "send anyway."
3. Every money figure links to its underlying Asaas object id (payment id, split id) — attribution is mechanical, never estimated.
4. Anything that would add a step for the *owner* is rejected by default (§17 owner-experience budget: the owner does 8 things, plus the two standing micro-behaviors accepted at onboarding — opening the WhatsApp Business app at least every 13 days, and the one-tap voucher redemption confirmation).

### 15.0 Navigation map

Left sidebar, fixed, pt-BR labels (these are the canonical nav strings):

```
CAIXA CHEIA (logo)
├── Painel                    (home, §15.1)
├── Salões                    (list → Salão detail, §15.2)
├── Importar & Escanear       (wizard, §15.3)
├── Raio-X                    (generator + list, §15.4)
├── Campanhas                 (builder + list, §15.5)
├── Supressão                 (§15.6)
├── Qualidade                 (§15.7)
├── Dinheiro                  (§15.8)
├── Cofre de Registros        (§15.9)
└── A Lista                   (CRM, §15.10)
```

Global elements on every screen: header with environment badge (`PRODUÇÃO` / `SANDBOX`), alert bell (unread `alerts` count), and a global salon switcher (typeahead over `businesses.name`). Deep-link routes: `/painel`, `/saloes/{business_id}`, `/importar`, `/raiox/{report_id}`, `/campanhas/{campaign_id}`, `/supressao`, `/qualidade`, `/dinheiro`, `/cofre`, `/lista`.

---

### 15.1 Painel (home)

**Purpose:** the founder's single morning screen — what needs a decision today, what is moving through the pipeline, what the month has paid. **User:** founder. **Route:** `/painel`.

**Layout:** three horizontal bands.

**Band 1 — Pipeline kanban** (`Funil`). Five columns matching the salon state machine (§8.7):

| Column (pt-BR) | Salon state | Card contents | Source |
|---|---|---|---|
| `Lista` | lead | name, city, system tag, unit count | `lista` joined to `businesses` where created |
| `Escaneado` | scanned | name, scan date, 4 scan numbers, "dias desde o scan" | `businesses`, `scan_results` |
| `Raio-X pago` | audit_paid | name, R$ paid (or `Cortesia` for comped design-partner audits — always generated, §3), credit remaining | `businesses`, `charges`, `credit_ledger`, `audit_reports` |
| `Mandato` | onboarding | name, onboarding checklist progress (Embedded Signup / Asaas key / 3 assinaturas) | `businesses`, `documents` |
| `Ativo` | active | name, locations count, last campaign date, month-to-date fees | `businesses`, `locations`, `campaigns`, `splits` |

Cards are clickable → Salão detail. Drag-and-drop is **disabled** — state changes only through real events (a scan, a payment, a signature), never by hand. Paused/churned salons appear in a collapsed footer row `Pausados e encerrados (N)`.

**Band 2 — Hoje** (`Hoje`). Three queues side by side:

| Queue (pt-BR label) | Contents | Source | Row action |
|---|---|---|---|
| `Aprovações pendentes` | campaigns in `pending_approval`: salon, count, hours waiting, expiry countdown (7-day validity, `approvals.expires_at`) | `campaigns`, `approvals` | `Reenviar pedido` (re-sends the approval-request template from the salon's own number, max 1 resend/24h), `Abrir campanha` |
| `Envios agendados` | campaigns in `scheduled`/`sending`: salon, template, recipient count, scheduled time, live progress bar when sending | `campaigns`, `manifest_entries` | `Abrir monitor` |
| `Alertas` | unresolved `alerts`, newest first, color-coded by type | `alerts` | `Resolver`, `Abrir` (deep link to the relevant screen) |

Alert types (the `alert_type` enum in §8, each with its pt-BR display string):

| Type | pt-BR string | Deep link |
|---|---|---|
| `quality_yellow` | `Qualidade do número caiu para AMARELO — sem novas campanhas até revisão` | Qualidade |
| `quality_red` | `Qualidade do número caiu para VERMELHO — envios pausados` | Qualidade |
| `optout_threshold` | `Taxa de opt-out {≥1%: Gate C bloqueado \| ≥3%: novos envios pausados}` | Qualidade |
| `heartbeat_due` | `WhatsApp do salão sem abrir há {N} dias (limite 13)` | Qualidade |
| `split_refused` | `Split RECUSADO — {refusalReason}` | Dinheiro |
| `split_divergence` | `Fundos bloqueados 2 dias úteis (divergência de split)` | Dinheiro |
| `kyc_pending` | `Conta Asaas do salão aguardando aprovação` | Salão → Asaas tab |
| `refund_due` | `Reembolso a processar — voucher {code}` | Dinheiro → refunds workbench |
| `render_failed` | `Falha ao gerar o Raio-X — regenerar` | Raio-X |
| `registry_block` | `Lista estadual {UF} não carregada — envios promocionais para essa UF bloqueados` | Supressão |
| `approval_expired` | `Aprovação venceu (7 dias) — pedir nova aprovação` | Campanhas |

Template pauses (Meta-side 3h/6h/disabled) and import-cap truncations are surfaced in place — on the Qualidade card (§15.7) and in the import wizard (§15.3 step 2) respectively — not as `alerts` rows.

**Band 3 — Dinheiro do mês** (`Dinheiro do mês`). Four stat tiles, current calendar month, each clickable to Dinheiro:
- `Vendas geradas (bruto)` — sum of settled `charges.value` across all salons.
- `Minha taxa (líquida de estornos)` — sum of `splits` with status DONE minus refund reversals.
- `Créditos de Raio-X consumidos` — `credit_ledger` debits this month.
- `Reembolsos` — sum of `refunds` this month.

**Empty state** (day 1): kanban shows `A Lista está vazia — comece pelo censo. → Importar A Lista` linking to §15.10. **Error state:** if the Asaas reconciliation job (§15.8) has not run in >24h, band 3 shows a yellow banner `Números podem estar desatualizados — última conciliação: {timestamp}`.

---

### 15.2 Salão detail

**Purpose:** everything about one account in one place. **User:** founder. **Route:** `/saloes/{business_id}`.

**Header:** salon name, CNPJ, system tag (Trinks/Avec/…), state badge (`Lead / Escaneado / Raio-X pago / Onboarding / Ativo / Pausado ({motivo}) / Encerrado`), group parent link if `businesses.parent_business_id` is set, and a `WhatsApp do dono` click-to-chat link (opens the founder's own WhatsApp to the owner's number — the founder's relationship channel, not the campaign channel).

Eight tabs:

**Tab 1 — `Visão geral`.** KPI row: total clients (`clients` count for this business), consent coverage % (`consents` with latest value `granted` / total contactable), lifetime settled fees (`splits`), campaigns run (`campaigns`), refund rate. Timeline of events (scan, audit paid, signatures, campaigns, pauses) from the append-only audit tables (§8). Action buttons: `Nova campanha` (jumps to §15.5 with salon preselected), `Novo import` (§15.3), `Gerar Raio-X` (§15.4).

**Tab 2 — `Unidades`.** One row per location (`locations` — one importable client base per location; multi-unit groups have one location row per unit). Columns: location name, city/UF, client count (`clients.location_id`), lapsed count at the business cadence, last import date, source system. Row action: `Reimportar` (→ §15.3 with location preselected). **Cadence is configured at BUSINESS level, never per location** (`businesses.cadence_days`, editable 30–180, defaults barber 45 / salon 90 / laser_aesthetics 120 — see §10); the cadence editor sits in this tab's header row and every edit writes an audit row.

**Tab 3 — `Campanhas`.** Table of this salon's campaigns: date, type (`Win-back / Renovação / Aniversário / Dia fraco`), state (the campaign state machine, §8.7), recipients, delivered, settled count, gross, fee. Row click → campaign detail (§15.5 results view). Banner if Gate C (active-base unlock) is closed for this account: `Campanhas de base ativa bloqueadas — requisitos: 2 win-backs liquidados ({n}/2), qualidade VERDE ({status}), opt-out < 1% ({valor})` (Gate C definition in §3; rules restated in §6).

**Tab 4 — `Resultados`.** The per-salon results ledger — also the source of the owner's monthly ledger link (§15.11). Per campaign: gross settled, Asaas fee borne by salon, founder fee (20% of netValue — display the real split values from `splits`, e.g. R$ 179,60 on a R$ 900,00 Pix charge, never a hardcoded 20% of gross; see §12), refunds, salon net. Footer totals. Per-client redemption ledger link per voucher (the salon's CDC litigation defense, §13).

**Tab 5 — `Documentos`.** One row per `documents` record: LIA version + adoption status, DPA version + e-sign status, service contract status, laser annex if `businesses.kind = 'laser_aesthetics'` (see §5/§16), privacy notice version (`notices`). Each row: version, signed/adopted date, signer, `Baixar PDF`, `Ver histórico`. Owner attestations (`attestations`: no-packages-sold, adult-base-only) listed beneath with their backing document and LIA version. This tab is a filtered view of the Cofre (§15.9). Red banner if any required document is missing or superseded-unsigned: `Documento pendente — campanhas bloqueadas pelo gate` (this is gate precondition P1 `docs_current`, §10/§15.5).

**Tab 6 — `WhatsApp`.** This salon's coexistence WABA card (same component as §15.7): number (`businesses.display_phone`, `waba_id`, `phone_number_id`), quality rating (latest `quality_snapshots`), messaging-limit tier (`businesses.messaging_tier`: 250/2k/10k/…), heartbeat countdown (`heartbeats`: `App aberto há {N} dias — limite 13`), template list with per-template status (`templates.state`: draft → submitted → approved / rejected / warming / active / paused_3h / paused_6h / disabled), history-sync status from onboarding (the 24-hour one-shot, stored access-restricted in `history_sync_messages` — see §11), Meta payment-method status (`Forma de pagamento Meta: ativa / pendente`). Actions: `Copiar lembrete de heartbeat` (renders the locked nudge for the founder to send from her own phone, §15.11 surface 9), `Submeter novo modelo` (template composer with the lint rules of §11).

**Tab 7 — `Asaas`.** Account status (`ACCOUNT_STATUS_*` webhooks): approval %, prova de vida, Pix key status. Stored `walletId`. API key metadata ONLY — name, created, expiry, last-used; **the key value is never displayed after entry** (vault, §7). Live fees from `GET /v3/myAccount/fees` cached with fetch timestamp (`Taxa Pix atual: {fixedFeeValue/percentageFee} — consultada em {ts}`; never hardcoded, §12). Receivables-pledge risk indicator: last split refusal, if any, with `RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT` explained in plain pt-BR: `O salão antecipou recebíveis — o split está sendo recusado. Acionar cobrança da taxa por NFS-e + Pix.` Action: `Gerar cobrança de taxa (fallback)` → creates an entry in `nfse_queue` (item_source `billing_fallback`) + a direct Pix cobrança to the salon (the §12 billing fallback).

**Tab 8 — `Crédito`.** The audit-credit ledger for this account: opening credit (R$ 490,00 single-site / R$ 990,00 group), each success-fee consumption row (campaign, date, amount — drawdown-phase charges are flagged `charges.credit_drawdown` and carry no split until the boundary charge, §12), refund-driven credit restores (symmetric restore, §6), remaining balance, expiry date (12 months from audit payment). Read-only; rows are generated by the settlement pipeline, never by hand.

**Empty states:** a lead-stage salon shows tabs 2–8 as stubs with the single line `Disponível após o primeiro import / Raio-X / onboarding`.

---

### 15.3 Importar & Escanear (wizard)

**Purpose:** turn a salon's raw export file into allowlisted rows plus the free scan — the only acquisition door (§3). **User:** founder (the owner only sends files over WhatsApp; the founder uploads them). **Route:** `/importar`. Business rules live in §9 (adapters) and §10 (gate); this screen is their UI.

Five steps, linear, with a persistent progress rail: `1 Upload · 2 Detecção · 3 Mapeamento · 4 Recibo de descarte · 5 Scan`.

**Step 1 — Upload** (`Enviar arquivos`). Salon/location selector (or `Novo salão` inline-create for a lead). Drag-drop zone accepting .xlsx/.csv/.pdf-rejected (`PDF não é importável — peça a exportação em Excel`). Multiple files allowed (e.g., Trinks clients export + package balances export). Creates an `imports` row per file.

**Step 2 — Adapter auto-detect** (`Detecção do sistema`). The classifier fingerprints header rows against the adapter registry (§9: Trinks, Avec, AppBarber/AppBeleza, Belasis, Fresha, Gendo). Shows: detected system + confidence, file row count, and cap warnings (`Gendo: arquivo com exatamente 5.000 linhas — exportação provavelmente truncada. Repetir exportação em páginas.` — the §9 cap-detection rule, fires at/near known caps). Manual override dropdown `Forçar adaptador` (audit-logged). **Error state:** no adapter matches → `Sistema não reconhecido — salvar cabeçalhos para análise` (stores header row only, no data rows, and creates a Lista note; new-adapter threshold rules in §9.6).

**Step 3 — Mapping preview** (`Mapeamento`). Two-column table: source column → canonical allowlist field (`client.external_id / client.name / client.phone / client.birthdate / visit.date / visit.ticket_value / package_balance.value_remaining / package_balance.sessions_remaining / package_balance.expiry / consent.*` — Fresha only, §9) or **DESCARTADA**. First 5 sample rows shown for mapped columns only; dropped columns show name + row count, **never content** (minimization, §5). Phone normalization preview to E.164 with failure count (`{N} telefones inválidos — serão importados como não-contactáveis`). Dedupe preview (`{N} telefones duplicados — serão unificados` — the Trinks defect guard, §9; merges recorded in `client_merges`). Action: `Confirmar e importar`.

**Step 4 — Dropped-columns receipt** (`Recibo de descarte`). Auto-generated after import: the definitive minimization evidence artifact. Lists every dropped column name + count, timestamp, file hash, adapter version; explicitly confirms the clinical blocklist (`service_description`, `anamnese`, `prontuário`, `observações` and all non-allowlist fields) was dropped at parse time (§9, Option B). Written to `dropped_columns_log` and filed in the Cofre (§15.9). Buttons: `Baixar recibo (PDF)`, `Continuar para o scan`.

**Step 5 — Scan result** (`Scan`). The four numbers, as four large tiles (source: `scan_results`, computed per §10 gate definitions):

| Tile (pt-BR) | Definition | Source |
|---|---|---|
| `Clientes na base` | total distinct clients imported | `clients` |
| `Clientes sumidos` | last visit older than the business cadence, within the ≤360-day ceiling | `clients`, `visits`, `businesses.cadence_days` |
| `Contactáveis` | sumidos minus suppression/invalid-phone/minors | minus `suppressions` (incl. global rows) |
| `Elegíveis hoje` | contactáveis passing a dry run of the per-client checks C1–C9 incl. the 60-day group-scope frequency ledger | `scan_results.eligible_count` (gate dry-run, §10) |

Plus a money line: `Saldo de pacotes não consumido: R$ {X}` from `package_balances` when the source system provided it (with the Trinks caveat inline when adapter = Trinks: `apenas saldos ativos — pacotes vencidos sem uso não aparecem no relatório do Trinks`, §9/§19).

**Shareable scan message generator.** Renders the WhatsApp message the founder sends the owner from her own phone (`scan_results.share_message_text`), with a copy button (`Copiar mensagem`). Template (pt-BR, ASSUMED draft — final locked copy in App A):

```
Oi {NOME}! Escaneei sua base como prometido. Resultado:
• {TOTAL} clientes na sua base
• {SUMIDOS} sumiram há mais de {CADENCE} dias
• {CONTACTAVEIS} dá pra contatar
• {ELEGIVEIS} são elegíveis pra uma campanha já
Tem dinheiro dormindo aí. O Raio-X completo custa R$490 e volta
inteiro como crédito — quer que eu gere o seu?
```

**Empty/error states:** parse failure → step fails closed with the raw parser error and `Nada foi gravado no banco` (imports are transactional). Re-import of a location always runs the resurrection guard: suppressed clients stay suppressed regardless of file contents (§6, locked decision 15) — the step-5 screen shows `⛔ {N} clientes suprimidos foram ignorados na reimportação (proteção anti-ressurreição)`.

---

### 15.4 Raio-X generator

**Purpose:** produce and deliver the R$ 490/990 audit (product rules in §19; credit rules in §3). **User:** founder. **Route:** `/raiox`, `/raiox/{report_id}`.

**List view:** all `audit_reports`: salon, generated date, status (`Rascunho / Liberado / Entregue` — per §8; payment state derived from the linked charge; regenerations shown as version v+1), charge status (or `Cortesia` — design-partner audits are comped at founder discretion but always generated; no salon reaches campaign #1 without a Raio-X, §3), URL. Regenerations are free and unlimited (§3) — `Regerar` on any row re-renders from current data at v+1, same stable URL.

**Generator flow (3 panels):**

**Panel 1 — Input review** (`Revisão dos dados`). Shows the imported inputs the report will render: location(s) selected, scan numbers, package-balance totals with source-system caveats (Trinks expired-unused caveat auto-inserted, §19), visit-recency histogram. Data-quality warnings (`{N}% de telefones inválidos`, `sem dados de pacotes neste sistema — seção de saldos será omitida` — Fresha, §9). Nothing here is editable — the Raio-X renders only imported data.

**Panel 2 — Render** (`Gerar`). `Gerar Raio-X` produces the HTML report at a private stable URL (`/r/{unguessable_token}`) + PDF export (HTML→PDF, §7). Content spec is §19's; the locked accounting language ("Você já recebeu R$X de clientes por serviços que ainda não entregou…" — full locked strings in App A and §19) is hard-embedded in the template, not editable per report.

**Panel 3 — Delivery on payment** (`Entrega`). Creates the audit charge (R$ 490,00 or R$ 990,00 group ≤8 locations) as a Pix cobrança **on the founder's own Asaas account, with no split** — her own product (§12). Shows: charge status (`Aguardando Pix / Pago / Vencida`) and the payment-link message to copy to the owner (sent from her own phone). **Auto-release on payment:** on the `PAYMENT_RECEIVED`/`PAYMENT_CONFIRMED` webhook, the system (a) flips the URL from teaser to full report, (b) sends an automatic transactional EMAIL to the owner with the private URL (Resend, §7 — transactional email is used ONLY for Raio-X delivery, voucher/receipt copy, and refund confirmations), (c) flips this panel to `Liberado` and renders the WhatsApp-ready delivery message the founder forwards manually from her own phone (copy button), (d) opens the R$ 490/990 credit in `credit_ledger` with 12-month expiry, (e) moves the salon to `Raio-X pago` on the kanban. (Same rule stated in §19.7 step 3.) **Error state:** payment received but render failed → no `refund_due` alert (nothing to refund — regenerate instead); a `render_failed` alert deep-links here.

Teaser mode: before payment the URL shows only the 4 scan numbers + a lock panel `O Raio-X completo é liberado após o pagamento.` [OPEN — ASSUMED behavior; §19 may instead specify no pre-payment URL at all. Reconcile with §19; carried in the §23 register.]

---

### 15.5 Campanhas (builder + monitor)

**Purpose:** the core workflow — from salon selection to settled money, with the gate and the approval artifact as immovable checkpoints. **User:** founder. **Route:** `/campanhas` (list), `/campanhas/nova` (stepper), `/campanhas/{id}` (state-dependent view). The campaign state machine (§8.7): draft → gated → margin_ok → pending_approval → approved → scheduled → sending → sent → settling → settled / partially_refunded / zeroed → reported.

The builder is a 10-step stepper. Steps lock sequentially; going back invalidates downstream steps (a re-gate is forced by any upstream edit).

**Step 1 — `Salão e unidade`.** Select salon (active only) + location(s). Shows import freshness (`último import há {N} dias`); imports older than 30 days show `Recomendo reimportar antes de enviar` [ASSUMPTION: 30-day freshness warning — soft warning only, not a gate check].

**Step 2 — `Tipo de campanha`.** Cards: `Win-back` (always available), `Renovação de pacote`, `Aniversário`, `Dia fraco` — the latter three greyed out unless Gate C is open for this account, with the requirement checklist inline (2 settled win-backs + GREEN + opt-out <1% — Gate C definition, §3/§6). Quarterly cap enforced here: `Limite: 2 campanhas de base ativa por unidade por trimestre — {n}/2 usadas`.

**Step 3 — `Gate`** (the fail-closed eligibility gate; normative spec in §10). The gate is **4 campaign preconditions + 9 per-client checks + 1 approval artifact**. This step runs server-side as an append-only `gate_runs` row (precondition results P1–P4 + per-client pass/fail counts C1–C9); per-client results are stored in `manifest_entries.checks`. Precondition P2 (margin) is evaluated at step 4 and shows `Pendente — etapa 4` here; the approval artifact is collected at step 7 and shows `Pendente — etapa 7`.

Campaign preconditions (run once per campaign):

| Id | Precondition (pt-BR label) | Level |
|---|---|---|
| P1 | `docs_current` — `Documentos vigentes: contrato + DPA + LIA adotada + aviso de privacidade` | account |
| P2 | `margin_gate` — `Margem do salão ≥15% (etapa 4)` | package math |
| P3 | `copy_lint` — `Copy genérica — nenhum serviço nomeado (lista de termos versionada)` | template |
| P4 | `channel_health` — `Saúde do canal: qualidade do WABA permite envio (escada §11)` | channel |

Per-client checks (run per manifest row; keys exactly as stored in `manifest_entries.checks`):

| Id | Check (pt-BR label) |
|---|---|
| C1 | `own_client` — `Cliente próprio deste salão (veio do import deste negócio)` |
| C2 | `lawful_basis` — `Consentimento documentado OU interesse legítimo válido (última visita dentro da cadência, teto 360 dias)` |
| C3 | `no_clinical_data` — `Nenhum campo clínico ingerido (estrutural — recibo do allowlist)` |
| C4 | `package_balance` — `Sem pacote/crédito pré-pago não consumido (exclusão CPC 47; ou atestado "não vendo pacotes")` |
| C5 | `suppression` — `Não está na lista de supressão (anti-ressurreição; inclui linhas globais)` |
| C6 | `state_registry` — `Não consta em registro estadual de bloqueio — FAIL-CLOSED (UF por DDD; sem lista carregada = bloqueado)` |
| C7 | `not_minor` — `Não é menor de idade (≥18; sem nascimento → atestado de base adulta)` |
| C8 | `frequency_60d` — `Frequência: máx. 1 modelo de marketing por telefone a cada 60 dias — todo o grupo (parent_business_id)` |
| C9 | `contactable` — `Telefone E.164 válido, deduplicado` |

UI: a checklist where every check shows PASS/FAIL + affected counts + drill-down to the excluded client rows (name + phone last-4 + exclusion reason — the exclusion log that is her liability shield, §5). Structural checks (C3, P3) show PASS-by-construction with a tooltip explaining why. The campaign cannot reach `approved` until P1–P4 pass, every manifest row is C1–C9-evaluated, and the approval artifact exists. **There is no override control anywhere on this screen.** FAIL on an account-level precondition blocks with the fix deep-linked (`LIA vencida → Cofre de Registros`). Output: the eligible list count that seeds the manifest.

**Step 4 — `Gate de margem`** (precondition P2; rules in §6 locked decision 2, formula in §10). The 3-question package form; inputs and result are recorded in the campaign's `gate_runs` P2 entry:

| Field (pt-BR) | Input |
|---|---|
| `Comissão do profissional (%)` | numeric, 0–70 (default from `businesses.default_commission_pct`) |
| `Classe de insumo` | select: `Baixo / Médio / Alto` (cost bands per §10 P2: low 5% / medium 13% / high 22% of price — ASSUMED) |
| `Preço do pacote (R$)` | centavos |

Computed display (live, using real fee arithmetic on netValue per §12; Simples estimate from `businesses.default_simples_pct`, default 8%): commission, insumos, Pix fee, Simples estimate, 20% fee, `Sobra pro salão: R$ {X} ({Y}%)`. The sales-framing line renders beneath (locked copy): `"desse pacote, sobra R$169 pra você e R$180 pra mim — mas esse cliente não voltava."` with values substituted for the actual package. **Block state:** salon net < ~15% → red panel `⛔ Esse pacote não passa: sobra menos de 15% pro salão. Ajuste o preço, a comissão ou o serviço.` and the stepper cannot advance. No override button exists; the 10% fallback fee is a founder-only lever applied off-screen via account config, never surfaced here (§6).

**Step 5 — `Manifesto`** (manifest preview). The exact send list, frozen as `manifests` + `manifest_entries`: total count, 10 sample rows (name, phone masked to last 4, days-since-last-visit), and the exclusion summary (`{N} excluídos: {breakdown by check C1–C9}`). Segment rule rendered in words (`clientes desta unidade sem visita há 90–360 dias, contactáveis, dentro da frequência`) — this exact string goes into the approval artifact (§14, §16). Button: `Congelar manifesto`.

**Step 6 — `Modelo e copy`.** Pick an approved `templates` row (status `active` or `warming`) or compose a new one. Composer runs the mechanical lint (§11): pt_BR language code, no `$`/`%` inside variables, sequential params, ≤2 URL buttons, single end-of-URL variable, body ≤1,024 chars, no wa.me links, no 4+ consecutive spaces in params — each rule shown as a live check. Category is locked to MARKETING. Copy lint also enforces precondition P3 `copy_lint` (no service names — versioned `lint_wordlist` + manual confirm). Body params are {{1}} nome, {{2}} package commercial name (owner-authored), {{3}} validity date from `campaigns.offer_valid_until`; the URL-button variable is a separate namespace and carries the per-campaign offer token (§11, §13). Shows template quality state and pacing note for `warming` templates (`modelo novo — será aquecido em coorte pequena primeiro`, §11). New submissions show Meta review status (typically minutes, 24h SLA).

**Step 7 — `Aprovação do dono`.** Renders the approval-request WhatsApp message preview exactly as the owner will receive it (message spec in §14): the final message text verbatim, the segment rule in words, the count, the schedule, and the instruction to reply `APROVO`. Buttons: `Enviar pedido de aprovação` — sent from the **salon's own number** to the owner's number as a pre-approved **UTILITY template** [ASSUMPTION: utility category as service-management follow-up on the owner's own mandate — defensible, but Meta recategorization risk noted; §11], so the reply arrives on the salon-WABA messages webhook and is captured with its wamid. Then a live tracker: `Aguardando resposta… / APROVO recebido {timestamp}`. **APROVO matching: case-insensitive exact word, trimmed** (same rule in §18.1); anything else shows the actual reply text for founder review — no reply is ever auto-interpreted as approval except that match. On approval: the dated approval artifact (owner identity, exact message text, segment rule, count, template_id + template_version, timestamp, raw inbound `owner_reply_wamid`) is written to `approvals` and filed in the Cofre (§16). Expiry: an approval binds ONLY this frozen manifest — any growth or content change voids it and returns the campaign to step 5; send-time re-checks (C5/C8) may only shrink the manifest silently (§10). **Approval validity: 7 days** (`approvals.expires_at`); an expired approval fires an `approval_expired` alert and requires re-approval (§10).

**Step 8 — `Agendar`.** Date/time picker constrained to the locked send window (case-law aggravator avoidance, §5): **weekdays 09:00–18:00 America/Sao_Paulo; Saturday 10:00–16:00 only with recorded owner opt-in; never Sundays or holidays** (same rule in §18). Shows portfolio messaging-limit check: `Limite do portfólio: {tier} destinatários únicos/24h — esta campanha usa {N}` (250-tier fits one 180-recipient campaign, §11). Confirm → state `scheduled`.

**Step 9 — `Monitor de envio`** (live, state `sending`). Header: progress `{sent}/{total}`, pace (20 mps coexistence throughput cap, §11). Live table by outcome, from `sends` (webhook-fed):

| Bucket (pt-BR) | Meaning | Handling shown |
|---|---|---|
| `Entregues` | delivered | model converts on delivered (§11) |
| `Enviadas (aguardando entrega)` | sent, no delivery receipt yet | — |
| `Retidas (avaliação de qualidade)` | `held_for_quality_assessment` | `pacing — liberação automática ou descarte; não reenviar` |
| `Falha 131049 — limite por usuário` | per-user marketing cap | `NUNCA reenviar (blackout 24h)` — auto-retry structurally absent |
| `Falha 130472 — usuário sem marketing` | Meta experiment group | `não cobrado, não é opt-out` |
| `Falha 131050 — desativou marketing` | permanent | auto-written to `suppressions` as a GLOBAL row (business_id NULL, permanent) |
| `Falha 131026 — não pode receber` | recipient unreachable | — |
| `Outras falhas` | any other code | raw code + payload link (`external_calls`) |

Kill switch: `Pausar envio` (stops the queue; delivered messages are irrevocable). Auto-pause fires on quality triggers (§15.7).

**Step 10 — `Resultados`** (states settling → reported). Per-campaign P&L, all rows linked to Asaas ids: charges created, paid count, settled gross, Asaas fees (salon-borne), founder fee (sum of `splits` DONE), refunds and reversed fee, salon net, messages cost note (`~R$ {X} pagos pelo salão diretamente à Meta`). Voucher issuance list. Zero-settle campaigns show the `zeroed` state plainly (`7% das campanhas liquidam zero — sem taxa, sem cobrança`, §21). The post-campaign results message is the second (and last) automated owner-facing send: it goes from the **salon's own number** to the owner as a UTILITY template when the campaign settles (§15.11 surface 7; `owner_notify` job, §7.4) — this step shows its preview and send status. Button: `Marcar como reportada`.

**List view** (`/campanhas`): filterable table of all campaigns by state/salon/type with the same columns as the Salão tab 3. **Empty state:** `Nenhuma campanha ainda. A primeira campanha nasce de um Raio-X → Nova campanha`.

---

### 15.6 Supressão (suppression center)

**Purpose:** the authoritative do-not-contact store — authoritative over every source system (§6, locked decision 15). **User:** founder. **Route:** `/supressao`.

**Layout:** search bar (phone/name), main table of `suppressions`: phone (hash + client link where matched), scope (**per-salon by default; `business_id` NULL = GLOBAL row** — WhatsApp-level signals like error 131050 and `user_preferences` suppress globally; locked in §8), source, date, evidence link. Source enum (`suppression_reason`, §8) with pt-BR labels:

| Source | pt-BR label |
|---|---|
| `user_preferences_stop` | `Webhook do WhatsApp (parou de receber ofertas)` |
| `error_131050` | `Erro 131050 — desativou marketing` |
| `free_text_optout` | `Texto livre: {SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA, …}` |
| `whatsapp_block` | `Bloqueou o número` |
| `manual` | `Adição manual` |
| `owner_request` | `Pedido do salão` |

State-registry hits are **not** suppression rows — a registry hit is a gate exclusion logged in `state_registry_checks` (§8, §10 check C6).

**Actions:** `Adicionar manualmente` (phone + reason + note; audit-logged), `Exportar CSV`. **Removal is deliberately hard:** a `Reativar` action exists only for `manual`/`owner_request` sources, requires a typed justification, and never applies to webhook/131050 sources (those are permanent, §11). **Free-text suppressions are never auto-removed:** a later documented consent grant creates a Branch-A lawful basis, but the suppression row stays unless the founder manually reviews it (same rule in §11.6).

**Status panels:** (a) `Guarda anti-ressurreição` — last N re-imports and how many suppressed clients each one attempted to resurrect and was blocked (`{N} bloqueados ✓`); (b) `Registros estaduais` — per-UF row (SP, PR, GO, SC, DF, RS) over `registry_lists`: list obtained? last refresh date, entry count. **The registry check is FAIL-CLOSED:** recipient UF is attributed by phone DDD→UF mapping (imprecision noted in the LIA); if an applicable state's list (SP first) is not loaded, **promotional sends to recipients attributed to that state are BLOCKED — no warning mode** (same rule in §5 and §10). A missing applicable list raises a `registry_block` alert. The SP row carries the [OPEN] flag inline: `Mecanismo de acesso à lista para fornecedores em verificação (PROCON-SP FAQ Q10) — ver §23` — [OPEN] REQUIRED BEFORE FIRST SEND, owner = lawyer (week-1 engagement item #5, §24); the lawyer may authorize a documented interim measure — until then, blocked.

**Empty state:** `Nenhuma supressão registrada ainda. Elas chegam sozinhas — webhooks e respostas SAIR entram aqui automaticamente.`

---

### 15.7 Qualidade (quality monitor)

**Purpose:** keep every salon's number alive — quality, pacing, and the 13-day coexistence heartbeat (§11). **User:** founder. **Route:** `/qualidade`.

**Layout:** a card grid, one card per WABA (`businesses` with a `waba_id`, joined to `quality_snapshots` and `heartbeats`), sorted worst-first. Card contents:

| Element | Source | Display |
|---|---|---|
| Salon + number | `businesses` | header |
| Quality rating | Meta webhook → `quality_snapshots.quality_rating` | badge `VERDE / AMARELO / VERMELHO` |
| Messaging tier | `businesses.messaging_tier` | `250 / 2.000 / 10.000 / 100.000 / Ilimitado por 24h` |
| Block rate (7d) | `sends` | % with trend arrow |
| Opt-out rate (rolling per campaign) | `suppressions` / delivered | % — also the Gate C input (<1%, §3/§6) |
| Pacing events (7d) | `held_for_quality_assessment` count | number + last occurrence |
| Template states | `templates` | chips: `ativo {n} · aquecendo {n} · pausado {n} · desativado {n}` |
| Auto-pause state | `businesses.state = paused(quality)` | banner when active |
| **Heartbeat countdown** | `heartbeats` (from `smb_app_state_sync`/echo activity signals) | `App aberto há {N} dias` — green ≤7, yellow 8–10, red 11–13 |

**Quality ladder** (canonical in §11, restated identically; the switches are server-side, displayed on-card): **RED → auto-pause ALL sends and campaigns for that WABA. YELLOW → no NEW campaign proposals until founder review; already-approved scheduled sends hold. Opt-out rate ≥1% (rolling per campaign) → flag + the business becomes Gate-C ineligible. ≥3% → auto-pause new sends for that business.** Template pausing (Meta-side 3h/6h/disabled) is handled independently by the send engine. Heartbeat ladder: day-9 `heartbeat_due` alert → founder sends the locked nudge from her own phone on day 10 → phone call on day 12; heartbeat ≥13 days (`PARTNER_REMOVED`/`COMPANION_INACTIVITY` webhook = integration dead) → salon state `paused(heartbeat)` and a re-onboarding task (§11). Card actions: `Copiar lembrete` (renders the locked nudge for the founder to send manually, §15.11 surface 9), `Pausar campanhas` / `Retomar` (manual, audit-logged), `Ver eventos` (raw `external_calls` webhook log for this WABA).

**Header strip:** portfolio-wide aggregates: numbers GREEN/total, heartbeats at risk (yellow+red count), templates paused across all WABAs. **Empty state:** `Nenhum número conectado ainda — o primeiro aparece após o onboarding do primeiro salão.`

---

### 15.8 Dinheiro (money)

**Purpose:** reconciliation, refunds, credits, and invoicing — the founder's books. **User:** founder (and her contador, via exports). **Route:** `/dinheiro`. Four tabs:

**Tab 1 — `Conciliação`.** The split ledger vs Asaas truth. One row per charge: campaign link, salon, Asaas payment id, charge value, netValue, split status (`PENDING / AWAITING_CREDIT / DONE / PROCESSING_REFUND / REFUNDED / REFUSED`), expected fee vs actual received (from her own Asaas account statement), delta flag. Credit-drawdown charges (`charges.credit_drawdown = true`) legitimately carry no split and are exempt from the missing-split guard (§12). Filters: month, salon, status, `só divergências`. Refused splits show `refusalReason` verbatim with the receivables-pledge explainer and a `Gerar cobrança fallback` action (→ `nfse_queue` + Pix cobrança, §12). Divergence-block rows (`PAYMENT_SPLIT_DIVERGENCE_BLOCK`) show the 2-business-day hold countdown. Export: `CSV do mês (contador)`.

**Tab 2 — `Reembolsos` (workbench).** Queue of refund requests (from vouchers in `refund_requested`, owner messages, or CDC art. 49 seven-day withdrawals — rules in §13). Selecting a case opens the **pro-rata calculator, prefilled** from `vouchers` + `redemptions` + the offer page's pre-disclosed arithmetic (§13): package price, sessions total/used, avulso per-session price, disclosed cancellation math → computed refund value and the founder-fee reversal. Art. 49 cases (≤7 days) force full refund, calculator locked (`Arrependimento em 7 dias: reembolso integral obrigatório`). Action `Executar reembolso` fires `POST /v3/payments/{id}/refund` — full refunds auto-reverse the split; partial refunds MUST carry `splitRefunds: [{id, value}]` (the §12 rule; the workbench builds this payload and shows it before firing). Post-execution: split status, credit-ledger restore if audit credit was consumed (symmetric, §3), voucher state update (partial refund → `refunded_partial`: sessions reduced, voucher continues; full refund → `refunded`, terminal — §8.7), alert closure. Error surface: refund 400s (fees not returned / insufficient salon balance) display the Asaas error verbatim + `o salão precisa cobrir a diferença — falar com o dono` (§12). [OPEN] behavior when the recipient already withdrew the split (negative balance vs queued debit vs failure) — §12/§23.

**Tab 3 — `Créditos`.** Cross-salon view of `credit_ledger` (same data as Salão tab 8, all accounts): balances, expiries in the next 60 days highlighted (`Crédito de R$ {X} vence em {data} — priorizar campanha`), consumption history including drawdown entries (fee accrued against audit credit, §12).

**Tab 4 — `NFS-e`.** The invoice queue: one row per settled fee (or fallback cobrança) awaiting a nota — `nfse_queue` with `item_source` (`split / credit_drawdown / billing_fallback`): salon (the invoice always goes to the SALON, never the consumer, §20), competência month, fee total, underlying settlement ids (the reconciliation trail: PSP split report ↔ NFS-e, §20), status (`Pendente / Emitida / Cancelada`), nota number + link once issued. Issuance itself happens in the municipal system; this queue tracks it [ASSUMPTION: no NFS-e API integration in v1 — manual issuance with a tracking queue (the §7.4 worker only builds the queue); automate later]. Monthly banner: `Fator R: revisar pró-labore este mês (rotina do contador)` on the 1st (§20).

---

### 15.9 Cofre de Registros (records vault)

**Purpose:** the defensibility store — every artifact that makes her an operator and not a controller, browsable and exportable (full artifact rules in §16). **User:** founder; export packages go to lawyers/salons on demand. **Route:** `/cofre`.

**Layout:** salon selector + four panels:

**Panel 1 — `Documentos por salão`.** Per salon, from the `documents` table (kind: `lia / dpa / contract / privacy_notice`): LIA (template version, adopted version, adoption date, owner identity, laser annex flag), DPA (version, e-sign status, signed date), service contract (same), privacy notice (version, published date — `notices`). E-sign v1 is **in-app click-to-sign with logged evidence** (name, timestamp, IP hash — `documents.evidence`) [ASSUMED sufficient for these B2B docs; lawyer confirms — §23]. Owner attestations (`attestations`) listed with their backing document. Status chips: `Vigente / Pendente de assinatura / Substituído / Vencido`. Actions: `Enviar para assinatura` (click-to-sign flow), `Baixar PDF`, `Nova versão` (uploads/generates v+1; old versions are never deleted — append-only).

**Panel 2 — `Artefatos de aprovação`.** Every `approvals` row across all campaigns: date, salon, campaign link, owner identity, segment rule string, count, message text hash + full text, template_id + template_version, expiry (`expires_at`, 7 days), raw inbound APROVO message id (`owner_reply_wamid`). Read-only, append-only, searchable. This panel is the operator-posture evidence (§5, locked decision 11).

**Panel 3 — `Registros de consentimento`.** Browser over `consents`: phone (masked), salon, value (`autorizou / recusou / revogou` — refusals stored too, §14), evidence class (`captura nativa / booleano importado / marcador`), exact displayed string + text version for native captures, timestamp, source (`QR do balcão / página de oferta / checkout / import Fresha / marcador em Observação / manual`), revocations. Filter by salon/source/date. Per-record detail shows the verbatim consent string version rendered at capture time (§14).

**Panel 4 — `Exportar`.** Export tool: pick salon + artifact classes + date range → generates a ZIP (PDFs + CSV index + integrity hashes) for a lawyer, an ANPD inquiry, or an exiting salon. Every export is itself logged (who/when/what — access-logged vault, §7). Also home of the import dropped-columns receipts (§15.3 step 4).

**Empty state:** `O cofre enche sozinho: assinaturas, aprovações e consentimentos entram aqui automaticamente. Nada aqui pode ser apagado.`

---

### 15.10 A Lista (CRM)

**Purpose:** the hand-built census of qualified doors — prospecting truth and next-action queue (census method in §2/§18). **User:** founder. **Route:** `/lista`.

**Main table** (`lista`): columns exactly per §8 — `Nome`, `Cidade`, `Bairro`, `Sistema` (Trinks/Avec/AppBarber/Belasis/Fresha/Gendo/Booksy-directory/desconhecido), `Unidades` (count), `Grupo/Franqueador` (flag: `Grupo / Franqueador / Unidade única`), `Status` (`Novo / Contactado / Conversa / Scan enviado / Escaneado / Convertido / Descartado`), `Próxima ação` (free text + due date), `Fonte` (source URL). Row click → detail drawer with contact log (append-only notes) and `Converter em Salão` (creates the `businesses` lead and links it — the kanban entry point, §15.1).

**Filters:** system, city, unit count ≥2 (the priority-segment filter, §2), franchisor flag, status, next-action overdue. **Saved views:** `Grupos 2–8 unidades`, `Franqueadores`, `Beauty Fair alvo` (a boolean tag for the September 2026 fair schedule, §18/§22).

**Next-action queue** (right rail): entries with due next-actions, overdue first — the founder's daily prospecting worklist. Action: `Concluir + próxima` (logs the touch, prompts the next action + date).

**Import from sweep:** `Importar varredura` accepts the CSV produced by the enumeration sweeps (site:trinks.com parsing, Booksy directories, unit-locator pages — §2/§18): dedupes on name+city, updates unit counts, tags source. Post-import summary: `{novos} novos · {atualizados} atualizados · {duplicados} ignorados`. The 3-day gate metric renders as a header stat: `Grupos 2–8 unidades (SP+Rio): {N}` with the tripwire thresholds shown (≥15 holds / <8 re-base, §2/§23).

**Empty state:** `A Lista começa com a varredura de 3 dias (SP+Rio "unidade") — ver §18. Importar varredura →`

---

### 15.11 Salon-owner surfaces (no login: WhatsApp + magic links)

The owner never logs into anything (§6/§17: 8 things, plus the two standing micro-behaviors accepted at onboarding — open the WhatsApp Business app at least every 13 days, and the one-tap voucher redemption confirmation). Every owner touchpoint is a WhatsApp message, a transactional email (Raio-X delivery only), or a magic link (signed URL, **30-day expiry**, re-issuable — locked in §7.6). This table is the canonical per-surface channel model (§7.4, §11, and §18 conform to it). **Only surfaces 6 and 7 are automated** — both sent from the SALON's own WABA to the owner's phone as UTILITY templates [ASSUMPTION: utility category — service-management follow-up on the owner's own mandate; Meta recategorization risk noted]; everything else is a manual, human send from the founder's own phone (the dashboard renders copy-ready text; she pastes and sends — never automated, never API):

| # | Surface | Channel + sender | Trigger | Content / spec |
|---|---|---|---|---|
| 1 | Scan result message | Founder's phone (manual, copy-generated) | Import wizard step 5 | 4 numbers + Raio-X offer (§15.3 draft; final copy App A) |
| 2 | Audit payment link | Founder's phone (manual) | Raio-X panel 3 | Pix cobrança link on founder's account, R$ 490/990 (§15.4) |
| 3 | Raio-X delivery | **Auto-release on Pix webhook:** automatic transactional EMAIL with the private URL (Resend, §7) + dashboard flips to `Liberado` and renders the WhatsApp-ready message the founder forwards manually from her phone | Audit charge paid | Private stable URL + PDF (§15.4, content per §19; same rule in §19.7 step 3) |
| 4 | Onboarding session | Video/phone call, founder drives; owner on the reception PC | Audit paid → onboarding | ~30 min guided: Embedded Signup popup (coexistence, §11), Asaas walletId + API key entry (vaulted, §7/§12), 3 click-to-sign e-signatures — contract, DPA, LIA adoption (§16/§17) |
| 5 | Consent QR print page | Magic link | Onboarding complete | A5 card PDF with QR → consent capture page `/c/{token}`; print-optimized; locked checkbox copy per §14; reception script optional — the card works standalone (§14.3) |
| 6 | Approval request | **Salon's own WABA → owner (automated UTILITY template)** | Campaign step 7 | Message text verbatim + segment rule + count + `responda APROVO` (spec §14); reply captured via the messages webhook → `approvals.owner_reply_wamid`; APROVO matching: case-insensitive exact word, trimmed |
| 7 | Post-campaign results message | **Salon's own WABA → owner (automated UTILITY template, `owner_notify` job §7.4)** | Campaign settles (step 10) | Settled gross, fee, salon net, refunds; pt-BR draft in App A |
| 8 | Monthly ledger link | Founder's phone (manual, monthly) | Month close (§18) | Magic link to a read-only render of Salão tab 4 (`Resultados`) for that salon |
| 9 | Heartbeat nudge | Founder's phone (manual, copy-generated from the Qualidade card) | Day-9 `heartbeat_due` alert → nudge day 10 → phone call day 12 (§11) | Locked copy: `abre o WhatsApp do salão hoje pra manter tudo rodando 🙂` |
| 10 | KYC/Asaas status nudges | Founder's phone (manual) | `kyc_pending` alert | Plain-language next step for account approval / prova de vida / Pix key (§12) |

No owner-facing surface ever requires a password, an app install, or a dashboard visit. The monthly ledger magic link is the only "page" an owner routinely sees.

### 15.12 Client-facing pages

Public, opaque-token URLs; mobile-first (arriving from WhatsApp); salon-branded with the salon's CNPJ prominent (the salon is the seller, §6 locked decision 14); founder branding limited to a footer `tecnologia Caixa Cheia`. Business rules live in §13 (offer/checkout/voucher) and §14 (consent/opt-out) — this is the surface inventory:

| Page | Route pattern | Reached from | Must contain (see §13/§14 for full rules) |
|---|---|---|---|
| Offer page | `/o/{token}` — **one opaque token per CAMPAIGN** (`campaigns.offer_page_slug`; the same URL serves every recipient; the template's URL-button variable carries this campaign token, §11/§13) | Template URL button | Package name/price/sessions/validity, **avulso per-session price, exact cancellation math, salon CNPJ** (TJDFT-driven disclosures, §5/§13); privacy-notice link + unticked consent checkbox (never a condition of purchase, §14); `Pagar com Pix`. Page stops issuing charges at `campaigns.offer_valid_until` |
| Checkout | same page, Pix panel | `Pagar com Pix` | Her API-created Asaas charge on the salon's account with the 20% split attached (`POST /v3/payments` → `pixQrCode`, §12 — never a static QR); QR + copia-e-cola; salon CNPJ on the receipt. Buyer phone collected; `client_id` resolved by E.164 match, NULLABLE when unmatched (forwarded links are legal — buyer name/phone recorded on the voucher, §8) |
| Voucher page | `/v/{token}` | Payment confirmation message | QR/code, sessions remaining, redemption history, validity, salon address (§13); redeemable ONLY at the issuing salon/group (§6 locked decision 16). Redemption is the one-tap `confirmar uso` (on this screen or the salon's magic link — the standing micro-behavior, §17); founder-side weekly reconciliation chases unredeemed/expiring vouchers |
| Consent capture | `/c/{token}` | A5 QR card at reception | The locked unticked checkbox copy verbatim (§14 — single scope `whatsapp_marketing`; no granular checkboxes at launch), Art. 9 notice link, refusal also recorded |
| Opt-out confirmation | `/s/{token}` | Page-initiated opt-out | Confirmation `Pronto — você não vai mais receber ofertas do {SALÃO}. Sair não muda em nada o seu atendimento.` (ASSUMED draft; App A) + suppression written (§15.6). **No automated WhatsApp reply is ever sent on SAIR/stop events** (locked §6 #9): suppression is immediate and silent; a founder-drafted quick-reply exists in the salon's WhatsApp Business app that the owner MAY send — optional, zero-obligation (§14.6) |

Error states (all pages): expired/invalid token → generic `Link inválido ou vencido — fale com o salão.` (no data leakage); offer page after `offer_valid_until`, refund, or zero state → `Esta oferta não está mais disponível.`

### 15.13 A day in the life (navigation walkthrough)

Illustrative Tuesday in the §18 operating week (the authoritative weekly cadence is §18):

1. **08:45 — Painel.** Two alerts: one `heartbeat_due` (day 9 — the nudge goes out from her own phone tomorrow, day 10), one `split_refused`. Copies the nudge from the Qualidade card for the morning send (§15.7 → surface 9). Opens Dinheiro tab 1, confirms the refused split is a receivables pledge, fires the NFS-e fallback cobrança (§15.8).
2. **09:00 — Hoje queue.** One `APROVO` arrived overnight — campaign moves to `scheduled` for 10:00. One approval pending 26h → `Reenviar pedido`.
3. **09:15 — Campanhas builder.** Builds the week's new win-back for a fair-cohort salon: gate runs (2 clients excluded on C8 frequency, 1 on C5 suppression — drill-down verified), margin gate P2 passes at 18.8%, manifest frozen at 176, approval request sent (step 7).
4. **10:00–10:30 — Monitor.** Watches the 10:00 send: 168 delivered, 4 `131049` (no retry), 1 `131050` (auto-suppressed, global row), 3 pending. Closes the tab; webhooks do the rest.
5. **11:00 — Importar & Escanear.** Two export files arrived on WhatsApp from a Lista prospect. Upload → Trinks detected → mapping confirmed → dropped-columns receipt filed → scan message copied and sent. Lista entry moves to `Scan enviado`.
6. **15:00 — A Lista.** Works the next-action queue: 6 touches, 2 new conversations, 1 `Converter em Salão`.
7. **17:30 — Dinheiro.** Two Pix settles landed from Monday's campaign; reconciliation shows zero deltas. One refund request (client used 2 of 6 sessions): workbench prefills the pro-rata math from the offer page's disclosed arithmetic, fires the partial refund with `splitRefunds` (voucher → `refunded_partial`), credit ledger restores R$ 59,87 of audit credit.

Total screen time ≈ 2.5 hours; everything else is webhook-driven.

### 15.14 Section open items

- [OPEN] Raio-X pre-payment teaser URL vs no-URL-before-payment — reconcile with §19; carried in the §23 register.
- [OPEN] State-registry list-access mechanism (SP first; PROCON-SP FAQ Q10) — **REQUIRED BEFORE FIRST SEND, owner = lawyer** (week-1 engagement item #5); until resolved, sends to recipients attributed to that state are blocked (fail-closed, §15.6/§10). §23 register.
- [OPEN] Refund behavior when the split recipient's balance was already withdrawn — §12 sandbox test; §23 register.
- ASSUMPTIONS flagged in this section: UTILITY category for the two automated owner-facing templates (approval request, results message) — recategorization risk (§11); insumo cost bands low 5% / medium 13% / high 22% (defined once in §10 P2); 30-day import freshness warning (soft, non-gate); manual NFS-e issuance with tracking queue in v1 (§20); in-app click-to-sign sufficiency for the B2B docs (lawyer confirms, §23); scan/results/opt-out message drafts pending App A locked copy.
- Locked values this section relies on (resolved, no longer open): magic-link expiry 30 days (§7.6); approval validity 7 days (`approvals.expires_at`, §8/§10); send window weekdays 09:00–18:00 America/Sao_Paulo, Saturday 10:00–16:00 only with owner opt-in, never Sundays/holidays (§18); suppression scope — `business_id` nullable, NULL = global row for 131050/`user_preferences` (§8).


## 16. RECORDS VAULT AND AUDIT TRAIL

The vault ("Cofre de registros", dashboard screen 9, see §15) is where the operator posture stops being a claim and becomes files. Under Art. 42 §2 the burden can be reversed onto the agent; under Art. 42 §1 I an operator is solidarily liable when it breaches the law or departs from lawful instructions (full liability map in §5). The vault is the founder's proof, for every send, that she executed a lawful, documented, owner-approved instruction — and refused the unlawful ones.

### 16.1 What exists per salon

| Artifact | Contents | Created when |
|---|---|---|
| **LIA versions + adoption signature** | Every version of the salon's LIA (the salon's document; founder drafts the template), each with the owner's e-signature and date; laser clinics carry the specific annex (§5) | Onboarding; on every material change |
| **DPA** | Signed operator agreement: object, duration, nature/purpose, data types, rights/duties, suboperators disclosed (Meta/WhatsApp, cloud host, Asaas as payment-processor context) | Onboarding |
| **Service contract** | Signed commercial contract incl. mandate-to-split and merchant-of-record clauses (§5, §20) | Onboarding |
| **Privacy notice versions** | Every published version of the salon's client-facing notice, with effective dates — the notice the consent page and QR footer point to | Onboarding; on change |
| **Per-send approval artifacts** | Dated record: named segment rule, recipient count, exact message text, `template_id` + `template_version`, and the owner's "APROVO" reply (message id + timestamp). Approval validity: **7 days** — an expired approval requires re-approval before sending. Never skipped, never batched (constitution #11, §6) | Every campaign approval |
| **Gate-run logs** | Every gate execution (`gate_runs`, append-only, §8): the 4 campaign-precondition results (P1–P4), per-client pass count and fail counts per check (C1–C9), counts in/out, config snapshot (cadence, wordlist version), gate_version | Every gate run |
| **Exclusion log** | Every excluded client with machine-readable reason keyed to the gate check (suppressed C5, refused/revoked or no basis C2, registry hit C6, frequency ledger C8, minor C7, package balance C4) — and every **refusal-to-send**: campaigns the system or founder refused to run (margin gate P2 fail, quality pause P4, unlawful instruction), with reason and date. This is the Art. 42 shield: evidence she did not execute knowingly bad lists | Every gate run; every refusal |
| **Consent records** | The append-only `consents` table (§8.3, restated in §14.4) | Continuous |
| **Opt-out log** | Every suppression event: stop word matched, webhook (`user_preferences`, 131050), block-as-opt-out, manual add — with source message id where applicable (§11) | Continuous |
| **Dropped-columns receipts** | Per import: every column the classifier dropped (name + row count, never content) — the minimization evidence for the allowlist architecture (§9) | Every import |
| **State-registry check logs** | Per gate run (`state_registry_checks`): which registry lists (SP first) were checked, list version/date, hits excluded (a registry hit is a gate exclusion C6, never a suppression row). FAIL-CLOSED: recipients attributed (phone DDD→UF) to a state whose applicable list is not loaded are BLOCKED — no warning mode. [OPEN] list-access mechanism — REQUIRED BEFORE FIRST SEND, owner = lawyer (week-1 item #5); see §23 register | Every gate run |

### 16.2 Append-only implementation

All vault tables follow one pattern (Postgres, §7):

- `INSERT` only; `UPDATE`/`DELETE` revoked from the application role at the database level (`REVOKE UPDATE, DELETE ON ... FROM app_role`).
- Each row carries `created_at` and a `prev_hash`/`row_hash` pair (SHA-256 of the row's canonical JSON concatenated with the previous row's hash, per salon per table) — a cheap hash chain that makes silent tampering detectable and demonstrable to a third party. (DERIVED implementation choice; append-only audit tables themselves are mandated, §7.6/§8.8.)
- Corrections are new rows referencing the corrected row's id with a `supersedes` field, never edits.
- Signed PDFs (LIA, DPA, contract) are stored as immutable objects with content hashes recorded in the corresponding table row.

### 16.3 Retention

| Class | Rule |
|---|---|
| Legal-defense artifacts (LIA, DPA, contract, approvals, gate/exclusion/opt-out logs, consent records, receipts) | Retained for the relationship + the limitation window. ASSUMPTION: 5 years post-termination as the baseline civil/consumer prescription window, 10 years where a record underpins package-credit disputes (CC art. 205 — unused credit prescribes in 10 years, §5). Lawyer confirms exact spans (week-1 checklist, §24) |
| Client contact data (names, phones) of a churned salon | Returned/deleted per the DPA on termination — except phones on the suppression list, which are retained (hashed where feasible) precisely to keep honoring opt-outs, and rows inside legal-defense artifacts |
| Suppression list | Never deleted. Authoritative forever (constitution #15, §6) |

### 16.4 The Art. 37 register, auto-generated

Art. 37 requires a record of processing operations — compulsory for LI processing (§5). The register is not a document anyone writes; it is a view generated from the vault tables: per salon — purposes (from LIA version), data categories (from the allowlist config + dropped-columns receipts proving what is NOT processed), legal bases per client class (consent-record aggregates + LI), suboperators (from DPA), retention (from §16.3 config), security measures (static section), and processing volumes (from gate-run logs). One click exports it as PDF, current as of generation date. Both her register (as operator) and each salon's register (as controller — a deliverable she hands the owner) render from the same tables.

### 16.5 Data-subject requests

Requests arrive at the salon (the controller) — typically as a WhatsApp message. The founder supports the salon through the vault:

- **Access/confirmation:** one query by phone produces everything held on that titular: client row (allowlist fields only), visit dates, consent rows, suppression status, campaign inclusion/exclusion history. Simplified answer immediately; complete declaration within the statutory window. ASSUMPTION [OPEN]: 15 days for the complete declaration (Art. 19 II), with the ANPD small-agents regime (Resolução CD/ANPD nº 2/2022) potentially doubling deadlines for ME/EPP agents — confirm exact deadlines with the lawyer (§23 register); this document does not fix them.
- **Deletion:** delete the client row and visit history; retain the suppression entry (so the number is never re-contacted — deletion must not cause re-inclusion) and retain rows embedded in legal-defense artifacts under Art. 16 (defense in judicial/administrative proceedings — flag basis in the response). The deletion itself is logged (append-only): who, when, what classes removed.
- **Revocation of consent:** §14.6 flow — suppression immediate and silent; no automated confirmation (the opt-out page confirms page-initiated opt-outs; the optional owner-sent draft of §14.6 may follow, zero-obligation).

Every request and its resolution is a vault row with timestamps — response-time proof if ANPD or a Procon ever asks.

### 16.6 Why this vault is her liability shield

The Art. 42 map lives in §5; the vault is its physical counterpart. Operator status holds because the owner takes the final decision — the per-send approval artifact is that fact, preserved. Solidary liability attaches when she departs from lawful instructions or executes unlawful ones — the exclusion log and refusals-to-send prove she didn't. Burden reversal (Art. 42 §2) punishes agents who can't show their work — the hash-chained, append-only tables are the work. In the case-law pattern (§5), damages follow a documented stop that was ignored — the suppression list plus opt-out log prove every stop was honored, with timestamps. The vault is also a sales asset: "consent/LGPD defensibility as a sellable feature" is wedge #4 (§4).

### 16.7 Export formats

For a lawyer, an ANPD request, or litigation: per-salon export bundle = one ZIP containing (a) each vault table as CSV (UTF-8, ISO-8601 timestamps) plus a human-readable PDF rendering; (b) signed documents as original PDFs with content hashes; (c) the generated Art. 37 register; (d) a manifest listing every file with SHA-256 hashes and the hash-chain heads, so integrity is verifiable offline. Scoped variants: single-titular bundle (for data-subject requests) and single-campaign bundle (approval artifact + gate run + exclusions + send log + settlement trail).

---


# PART IV — THE OPERATION

## 17. Onboarding Playbook

Onboarding exists to move a salon from "paid the Raio-X" (or "impressed by the free scan") to "first campaign approved" while the owner does almost nothing. The design law (see §6; this section is the normative owner-budget statement): the owner does **8 things, plus two standing micro-behaviors accepted at onboarding**. Everything else is the founder's work, invisible to the owner. Every proposed onboarding "improvement" is tested against one question — *does this add a step for the owner, or for her?* Owner-side additions are rejected by default.

### 17.1 The owner's 8 touches (verbatim, the spine)

1. one WhatsApp conversation + send 2 export files
2. receive 4 numbers
3. pay R$490 Pix if audit
4. ONE ~30-min guided onboarding session on the reception PC (Embedded Signup, Asaas key, 3 signatures)
5. print one QR card
6. per campaign: read message, reply "APROVO"
7. answer client replies in own WhatsApp as always
8. watch Pix land

Plus **two standing micro-behaviors**, accepted explicitly at onboarding (recurring, not one-off touches):

- **(a) Open the WhatsApp Business app at least every 13 days** — the coexistence heartbeat (disclosure line 3, Appendix A.13; mechanics in §11).
- **(b) The redemption tap** — when a client presents a voucher, the receptionist taps **"confirmar uso"** (on the client's voucher screen or via the salon's magic link — see §12, §13). Founder-side weekly reconciliation chases unredeemed and expiring vouchers, so a missed tap costs a follow-up, not money.

### 17.2 What the founder does invisibly around each touch

**Touch 1 — one WhatsApp conversation + 2 export files.**
Before this conversation the founder has already done the work: the salon is a row in A Lista (see §15, screen 10) with system tag, unit count, and source URL; she knows which adapter applies and has the export path memorized (e.g., Trinks: Meu Estabelecimento > Clientes > Todos os clientes > Mais filtros > última visita filter > Exportar — see §9). The conversation runs the 9-question triage (§17.4) conversationally, never as a form. She then walks the owner through producing two exports — the client list and the packages/balances report — by voice note or screenshots, in under 10 minutes. The files arrive in the same WhatsApp thread; she uploads them into Importar & Escanear herself (see §15, screen 3). The owner never sees a mapping screen, a dropped-columns receipt, or a database.

Script (free-form message, pt-BR):

> "Oi, [NOME]! Pra eu escanear o salão de graça eu só preciso de dois arquivos que o seu [SISTEMA] já gera sozinho. Vou te mandar o passo a passo em 30 segundos — você clica, exporta e me manda aqui mesmo. Não precisa instalar nada e ninguém mexe no seu sistema."

**Touch 2 — receive 4 numbers.**
The founder runs the import (allowlist fields only, see §9), runs the scan, and sends the scan-result message (Appendix A.2): total de clientes, clientes sumidos, contactáveis, elegíveis. She has already sanity-checked the numbers against the export row counts (Gendo 5,000-row cap detection, Trinks duplicate-phone dedupe — see §9) so the four numbers are defensible if the owner pushes back.

**Touch 3 — pay R$490 via Pix (audit path).**
Founder creates the audit charge on **her own** Asaas account (her product, no split — see §12), sends the payment link with the audit offer message (Appendix A.3). On Pix confirmation, the webhook **auto-releases** the Raio-X: an automatic transactional **email** delivers the private URL + PDF to the owner, the dashboard flips the report to "released" and renders the WhatsApp-ready message that the founder forwards **manually from her own phone** (see §15 screen 4 and §19.7). If the owner stalls, one follow-up at day 3, one at day 7, then the lead is parked — no pressure loops. Design partners: the audit may be **comped** (R$0, founder discretion) but is always **generated** — no salon reaches campaign #1 without a Raio-X (see §3).

**Touch 4 — the ONE ~30-minute guided session.** Full agenda in §17.3.

**Touch 5 — print one QR card.**
Founder generates the A5 consent-card PDF (see §14) and sends the print link during the guided session. The owner prints one page and puts it at reception. Done. If the salon has no printer, the founder mails a laminated card (ASSUMPTION: cost < R$15, operational default) or the owner prints it at any papelaria.

**Touch 6 — per campaign: read, reply APROVO.**
Everything before that reply — gate, margin math, manifest, template — is §18. The approval request message (Appendix A.4) arrives from the **salon's own number** (utility template — see §11, §15) so the owner's reply is webhook-captured; it is engineered to be answerable in 15 seconds and to constitute the operator-preserving artifact (dated, named segment rule, count, exact message text, template id + version, and the owner's reply — see §5). An approval is valid for **7 days**; expired approvals require re-approval.

**Touch 7 — answer replies in own WhatsApp as always.**
Nothing to teach: coexistence means replies land in the salon's WhatsApp Business App exactly as before (see §11). The founder's only invisible work is monitoring free-text opt-outs (SAIR, PARE, etc.) via webhook and suppressing (see §11 and §16).

**Touch 8 — watch Pix land.**
The split executes at settlement (see §12); the owner sees money arrive in the salon's own Asaas account with no reconciliation work. When the campaign settles out, the results message (Appendix A.7) goes out automatically from the salon's own number (utility template — see §11, §15).

### 17.3 The ~30-minute guided session — minute-by-minute

One video call, founder shares nothing on screen except what the owner needs to click. Owner sits at the **reception PC**. The founder has pre-staged everything: WABA creation queued, contract/DPA/LIA pre-filled with the salon's CNPJ, e-sign envelopes ready, QR card rendered.

| Min | Step | Who clicks | Notes |
|---|---|---|---|
| 0–3 | Welcome + the honest-trade disclosure checklist (read aloud, owner confirms each line — Appendix A.13) | — | Broadcast lists die; profile picture freezes; open the app every 13 days; companion devices relink. Confirmations logged to the records vault (see §16). |
| 3–5 | Pre-flight: WA Business app version ≥ v2.24.17; number ≥3 months old; **no payment method attached in the WA Business app** | Owner (phone) | Any failure → branch (§17.5), session pauses or reschedules. |
| 5–12 | **Embedded Signup v4 popup** (coexistence flow) on the reception PC; owner logs into Facebook, follows the flow, scans the QR from the salon phone | Owner | Founder narrates every screen. WABA created in **BRL** (see §11). History sync starts — the 24-hour one-shot window begins; founder's monitor confirms the 3 phases complete same-day. |
| 12–16 | **Meta payment method** added in WhatsApp Manager (boleto or card, salon's own) | Owner | The transparent pass-through line, said verbatim: *"As mensagens custam uns R$60 por campanha de 180 clientes e esse valor você paga direto pra Meta, no seu próprio boleto. Eu não ganho nada em cima de mensagem — eu só ganho os 20% do que cair no seu Pix."* |
| 16–21 | **Asaas connection**: owner opens Asaas, Integrações menu; reads out the **walletId**; creates a **named API key** (expiry set, IP allowlist to founder's server) and pastes it into the vault entry page (encrypted at rest, access-logged — see §7) | Owner | Trust conversation happens here, not buried: *"Essa chave permite movimentar a conta do salão. Ela fica num cofre criptografado, com registro de todo acesso, e você pode revogar quando quiser dentro do Asaas."* If the salon has no Asaas account yet: open one live (CNPJ, 10 min), knowing KYC may take days (§17.5). |
| 21–27 | **3 e-signatures**: (1) service contract (mandate-to-split, merchant-of-record, "em nome e por conta do salão" — see §5, §20); (2) DPA; (3) LIA adoption (the salon's document; laser annex if applicable — see §5) | Owner | Founder summarizes each in one sentence before signing; no legalese reading on the call. |
| 27–30 | **Consent QR card**: founder sends print link, owner prints the A5 card, places it at reception; founder teaches the 10-second reception script (Appendix A.10 — **optional**: the card works standalone, see §14) | Owner | Session ends with: "Primeira campanha chega pra sua aprovação em até X dias. Você só responde APROVO." |

After the call, invisibly: founder submits the salon's first pt_BR templates for review, warms nothing yet (no sends until approval), verifies webhook subscriptions (`history`, `smb_app_state_sync`, `smb_message_echoes`, `user_preferences`, `account_update` — see §11 and App B), confirms history sync completed inside the 24h window, files all artifacts in the Cofre de registros (see §16), and collects the salon's CNPJ document as a contingency — classic Meta business verification is **need-triggered only**, submitted if and when a manifest would exceed the 250-recipient/24h tier (see §11).

### 17.4 The 9-question triage

Run conversationally in Touch 1. **These nine items are reconstructed operational defaults derived from the constraints in §9, §10, §11 and §12 — they are the operating checklist, not externally verified facts.**

| # | Question | Why it gates |
|---|---|---|
| 1 | Which system do you use? (Trinks / Avec / AppBarber / Belasis / Fresha / Gendo / other) | Adapter exists? Grade? (see §9). Booksy → prospect only, not servable. |
| 2 | Do you have owner/admin access to export reports? | Exports are the permanent architecture; no access = no scan. |
| 3 | Is the salon's WhatsApp number **at least 3 months old** with active history? | Meta coexistence gate (see §11). |
| 4 | Is the number on the WhatsApp **Business** app, version ≥ v2.24.17? | Coexistence requirement. |
| 5 | Is a **payment method attached inside the WA Business app**? | Must be removed before Embedded Signup (see §11, §17.5). |
| 6 | Is there a reception PC (or laptop) for the guided session? | Session design; fallback is phone-guided (§17.5). |
| 7 | Package economics: typical package price, professional commission %, insumo class | Feeds the margin gate's 3-question package-design step (see §6, §10). ~50% commission or high-insumo services will be blocked — better to know before the pitch. |
| 8 | Group structure: how many units, who controls the software choice, franchised? | Groups/franchisors are the priority segment (see §2); one relationship = N locations. |
| 9 | Roughly how many clients pass through per month? | Sizes the eligible pool and the 250-recipient first-tier fit (see §11); calibrates expectations before the scan. |

### 17.5 Failure branches

**No reception PC → phone-guided session.** Embedded Signup runs in the phone browser; the founder drives via screenshots and voice notes. Add ~15 minutes; split the session into two calls if attention frays. E-signatures and vault entry work fine on mobile. Nothing else changes.

**Number < 3 months old → not eligible yet.** Do not attempt onboarding — the coexistence gate will reject it (see §11). Say so honestly: *"Seu número é novo demais pro WhatsApp liberar a integração — precisa de 3 meses de uso ativo. A gente agenda pra [MÊS]; enquanto isso eu já deixo o Raio-X e o cartão de consentimento prontos."* Park the salon in `onboarding` with a dated resume trigger. Never suggest a new/burner number (that is the ReativaPlus anti-pattern — see §4).

**Payment method attached in the WA Business app → remove first.** Coexistence onboarding fails while a payment method is attached (see §11). Guide the owner: WA Business app > Settings > Business tools > remove the payment method — then proceed. If the salon actively uses in-app payments, pause and discuss what that flow does for them before removing anything.

**Asaas KYC delays.** A salon opening its Asaas account at onboarding may hit document review and — for the Pix key — the 100% approval + prova de vida requirement (see §12). Split status will return `WALLET_UNABLE_TO_RECEIVE`-class failures until the founder's own wallet-side checks pass, and charges cannot be created from an unapproved salon account. Branch: complete everything else in the session, monitor `ACCOUNT_STATUS_*` webhooks, and schedule the first campaign only after the account is fully approved. Never launch a campaign whose charges would land on an unapproved account.

**History-sync window missed (24h one-shot).** If the 3-phase sync does not complete within 24 hours of onboarding, the client must be offboarded and redone (see §11). The founder's monitor alarms at hour 12; redo costs the owner one more 10-minute call — apologize once, fix it, move on.

## 18. Campaign SOP and the Operating Week

### 18.1 The per-campaign runbook

Every campaign — win-back, renewal, birthday, slow-day — runs the same rail. The state machine is specified in §8.7 (`draft → gated → margin_ok → pending_approval → approved → scheduled → sending → sent → settling → settled | partially_refunded | zeroed → reported`); this is the human procedure wrapped around it.

1. **Gate.** Run the fail-closed eligibility gate (see §10): campaign preconditions **P1 `docs_current`**, **P3 `copy_lint`**, **P4 `channel_health`**, then the nine per-client checks **C1–C9** against every manifest row — all visible pass/fail with counts. Any structurally failed check kills the campaign, not the founder's judgment. Win-back is the only type allowed for a new account's first 2 campaigns; active-base types require Gate C unlocked for that account (2 settled win-backs + WABA quality GREEN + opt-out <1% — see §3).
2. **Margin.** Run the 3-question package math (commission %, insumo class, package price) — precondition **P2 `margin_gate`**, evaluated at this step but still blocking. Under 15% net to the salon → the system refuses to propose it (see §6, §10). The founder does not override; the 10% fallback fee is a founder-only lever, never offered proactively.
3. **Manifest.** Freeze the exact recipient list: segment rule (named, human-readable, e.g. `última visita 90–360 dias, sem pacote ativo, sem envio nos últimos 60 dias`), count, per-recipient C1–C9 results (suppression, frequency, registry, etc.). The manifest is immutable once approval is requested.
4. **Approval.** Send the approval request message (Appendix A.4) from the **salon's own number** (utility template — see §11, §15) so the owner's reply arrives via the messages webhook and is captured to `approvals.owner_reply_wamid` (see §8): date, named segment rule, count, the exact template text, template id + version, package terms, scheduled window. Only the reply **APROVO** — matched case-insensitive, exact word, trimmed — advances the state. The reply is archived in the vault (see §16) — this artifact is the operator-posture keystone (see §5). No approval, no send, ever; approvals are never batched across campaigns. An approval is valid for **7 days** — expired → re-approve.
5. **Warm if new.** A newly approved (or just-unpaused) template goes to a small cohort first — operational default **20–30 recipients** (ASSUMPTION; sized to survive `held_for_quality_assessment` pacing, see §11/App B). Full manifest follows only after early feedback is clean.
6. **Schedule business-hours.** Sends run **weekdays 09:00–18:00 America/Sao_Paulo; Saturday 10:00–16:00 only with the owner's explicit opt-in; never Sundays or holidays** (the case-law aggravator list, see §5). Respect the WABA's messaging tier (new portfolios: 250 unique recipients/24h — one 180-recipient campaign fits, see §11).
7. **Monitor.** Watch the send live: delivered/failed by error code. 131049 is terminal for 24h — never auto-retry (see App B). 131050 and `user_preferences` stop events write straight to the suppression list (as **global** rows, business_id NULL — see §8). Pacing holds are watched, not fought.
8. **Results message.** When settlement stabilizes, the results message (Appendix A.7) goes to the owner automatically from the salon's own number (utility template): settled count, gross to the salon, her fee, refunds if any. Delivered proactively — the owner never has to ask.
9. **Ledger update.** Post fees to the split ledger, reconcile against Asaas, apply audit-credit consumption (R$490/R$990 credits burn against fees first — see §3, §12), queue the NFS-e to the salon (manual issuance in v1, tracking queue — see §15, §20), and log per-recipient sends into the 60-day frequency ledger.

### 18.2 Cadence rules (recap — normative source §6/§10)

- **Hard frequency ledger (check C8):** max 1 marketing template per phone_hash per 60 days, across ALL campaign types and ALL businesses sharing the same parent_business_id (group scope — the only permitted cross-business lookup, see §8, §10). No override switch exists in the product.
- **Eligibility windows:** last visit within cadence window, ≤360 days absolute ceiling (never 365). Type defaults: barbershop 45d / salon 90d / laser-aesthetics 120d; owner-adjustable 30–180. Cadence lives at business level (see §8).
- **Account progression:** first 2 campaigns are win-back (the audition). Gate C then unlocks active-base types per account. Cap: 2 active-base campaigns per location per quarter.
- **Suppression is authoritative:** opt-outs survive every re-import. State do-not-disturb registry hits are **gate exclusions (check C6), never suppression rows** — fail-closed: recipient UF attributed by phone DDD; if an applicable state's list is not loaded, promotional sends to recipients attributed to that state are **blocked**, no warning mode (SP registry = absolute exclusion for promotional content, no existing-customer exception — see §5, §10).

### 18.3 The operating week

The week has one shape from the start; only volume and delegation change. Target load ~30 hours/week.

| Day | Block | Month 6 (≈15–25 locations) | Month 18 (≈60–100 locations, VA onboard) |
|---|---|---|---|
| **Mon** | Manifests & QA | Build the week's manifests, run gates, request approvals. ~4–6 campaigns. | VA preps exports and draft manifests from the queue; founder QAs every gate result and sends every approval request herself. ~15–25 campaigns. |
| **Tue** | Sends & settlement watch | Warm/full sends inside business hours; monitor error codes; watch splits settle. | Same, at volume; founder watches the alert board, not individual sends. |
| **Wed** | Audit debriefs — **the sales function** | 2–3 Raio-X walkthrough calls; each debrief IS the pitch (the numbers sell, see §19). | 4–6 debriefs; still 100% founder — this is the revenue conversation and is never delegated. |
| **Thu** | Scans & Lista outreach | Run new free scans; work A Lista (groups and franchisors first); send scan-result messages. | VA runs export collection for scans; founder does outreach conversations and group/franchisor relationships. |
| **Fri** | Reconciliation + one build improvement | Split ledger vs Asaas; refunds workbench; NFS-e queue; then ship exactly ONE product improvement via Claude Code. | Same; the one-improvement rule stays — it prevents the build from eating the business. |

**The VA (part-time, ~month 18 at the earliest — see §6):** does export collection, import runs, manifest preparation, and document filing. The VA **never** sells, **never** talks to owners about money, and **never** touches approvals — every approval request and every gate override decision (of which there are none — gates are fail-closed) remains with the founder. The VA has no access to Asaas keys or the vault's decryption path (see §7, §16).

### 18.4 Support model

There is no ticket system, no support inbox, no portal login. Owner questions arrive on the **same WhatsApp thread** that ran onboarding — one conversation per salon, forever, searchable. Response norm: same business day (operational default). Anything that recurs three times becomes either a copy fix in the results/approval messages or a Friday build improvement — support volume is treated as a product defect signal, not a workload to staff.

### 18.5 Escalation triggers (drop everything)

| Trigger | Signal | Immediate action |
|---|---|---|
| **Quality ladder** | WABA rating drops (YELLOW/RED), template paused (132015), pacing drops, or opt-out spike | One ladder (normative source §11.5.1): **RED** → auto-pause all sends and campaigns for that WABA. **YELLOW** → no NEW campaign proposals until founder review; already-approved scheduled sends hold. **Opt-out rate ≥1%** (rolling per campaign) → flag + business is Gate-C ineligible; **≥3%** → auto-pause new sends for that business. Template pausing (Meta-side 3h/6h/disabled) is handled independently by the send engine. Founder reviews copy/segment/cadence before any resume. See App B. |
| **Split REFUSED** | `refusalReason: RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT` — the salon pledged its receivables | Pause new campaigns for that salon; switch fee collection to billing fallback (NFS-e + Pix cobrança to the salon — see §12); have the receivables conversation with the owner honestly. |
| **Heartbeat expiry** | 13-day inactivity approaching, or `account_update` PARTNER_REMOVED (`COMPANION_INACTIVITY` / `PRIMARY_INACTIVITY`) | Dashboard alert at day 9; founder sends the locked nudge (Appendix A.8) **from her own phone** at day 10; phone call at day 12. If the integration dies, coexistence must be redone via Embedded Signup — schedule a 10-minute call, treat as P1 because campaigns silently fail otherwise. See §11. |
| **Refund due** | Voucher `refund_requested` (CDC art. 49 or partial cancellation) | Refunds workbench with pro-rata calculator prefilled (see §12, §15); salon-originated refund executed same day; split reversal verified; owner gets the refund acknowledgment (Appendix A.12). |


## 19. THE RAIO-X AUDIT PRODUCT

The "Raio-X do Caixa" is the paid audit and the only bridge from free scan to mandate: R$490 single-site / R$990 per group (up to 8 locations), one-time, 100% credited against first success fees, 12-month validity, refund-symmetric credit restore, never charged twice, regenerations free — full pricing and credit mechanics in §3. This section specifies the deliverable's content, the generation pipeline, and the fair version.

### 19.1 Form

One private, stable, opaque URL rendering an HTML page (mobile-first — owners read it on WhatsApp), plus a PDF of the same content for forwarding to a sócio or contador. pt-BR throughout, salon's name on top, "Raio-X do Caixa — [SALÃO]" as title, generation date, data-window disclosure ("dados de DD/MM/AAAA a DD/MM/AAAA, extraídos do seu [sistema]"). Five sections, fixed order.

### 19.2 Section 1 — Mapa de receita adormecida (lapsed-revenue map)

From allowlist data only (client, last visit date, historical ticket values — §9): the count of lapsed clients (beyond the business-type cadence window, within the ≤360-day ceiling, §10) crossed with **ticket value bands** — never services, which the pipeline does not possess:

| Faixa de ticket (histórico) | Clientes sumidos | Valor adormecido estimado |
|---|---|---|
| R$0–150 | n₁ | n₁ × band midpoint |
| R$150–300 | n₂ | … |
| R$300–600 | n₃ | … |
| R$600+ | n₄ | … |

Headline number: total estimated dormant revenue (DERIVED from the salon's own export; method footnote states it is count × historical ticket band midpoint, one visit each, no repeat-visit multiplier — deliberately conservative). Where the export lacks ticket values (system-dependent, §9), the band column falls back to the market ticket médio R$185 with an explicit "estimativa de mercado" label.

### 19.3 Section 2 — Dinheiro recebido, serviço devido (prepaid-liability finding)

For systems exporting package balances (Trinks; Avec report 0063; others per §9): the sum of active unconsumed prepaid balances. The language here is locked and accounting-safe — these three sentences appear verbatim, in this order, and no other framing of this finding is permitted anywhere in the product (no "passivo no balanço", no "você ainda vai pagar imposto sobre isso", no "dívida" — see §5/§20 for why):

> "Você já recebeu R$X de clientes por serviços que ainda não entregou. Esse dinheiro já está no seu caixa, mas ainda não é lucro — é serviço a executar."

> "Se esses clientes pedirem o dinheiro de volta da parte não utilizada, o Código de Defesa do Consumidor está do lado deles. Não é só pendência de agenda: é risco de caixa."

> "Não estou dizendo que existe uma dívida registrada no seu balanço — a maioria dos salões do Simples nem levanta balanço. Estou dizendo que R$X do seu caixa já tem dono: são horas de serviço que você ainda deve entregar."

Trinks caveat, printed with the number: the figure covers **"active unconsumed balances only"** — Trinks' package report excludes packages closed without full use, so the true figure may be higher (reconciliation option via "Venda de Pacotes – Encerrados", §9). Fresha: no package export documented → this section renders as "não disponível no seu sistema" with one line explaining why [OPEN, §23]. This section motivates the renewal campaign type (Gate C economics, §3) and the redemption ledger (19.6).

### 19.4 Section 3 — Quem você pode chamar (contactability & consent gap)

The eligibility funnel as money: total clients → with valid phone → within the LI window → not suppressed/refused/registry-blocked → **elegível hoje**. Each drop shown as count and as R$ (count × ticket band). The gap between "sumidos" (Section 1) and "elegível hoje" is the consent gap, stated in R$: "R$Y da sua receita adormecida está fora de alcance hoje — clientes de mais de 12 meses atrás, sem consentimento registrado."

Then the fix, presented as a document inside the document: the **90-day consent-capture playbook** — the QR card at reception (§14.1), the one-line script (§14.3), the projected recovery curve ("consent rebuilds a sendable base in ~one service cycle"), and the consent % the dashboard will report monthly. This playbook is gate check **C2 `lawful_basis` (§10)** packaged as an owner-facing deliverable; it is included free with every Raio-X and doubles as evidence the salon was put on a documented compliance path.

### 19.5 Section 4 — Primeira campanha recomendada

A concrete, gate-passing proposal — by default the R$900 win-back package — with the margin math printed in full, because the 20% fee survives scrutiny only when the owner sees the whole ledger (reference figures at 40% commission, medium insumo class; recomputed live from the 3-question package-design inputs, §3):

| Item | Valor |
|---|---|
| Pacote vendido | R$900,00 |
| Comissão profissional (40%) | −R$360,00 |
| Insumos (13%) | −R$117,00 |
| Taxa Pix (Asaas) | −R$2,00 (aprox.; lida ao vivo, ver §12) |
| Simples (~8% da receita bruta) | −R$72,00 |
| Taxa Caixa Cheia (20% do líquido) | −R$180,00 (efetivo R$179,60, ver §12) |
| **Fica com o salão** | **≈R$169 (≈18,8%)** |

With the locked sales framing: "desse pacote, sobra R$169 pra você e R$180 pra mim — mas esse cliente não voltava." And the honest outcome band for a 180-recipient campaign, all three shown (DERIVED, §21): **conservador** ~2 vendas ≈ R$1.800 brutos ao salão; **esperado** 4–5 vendas ≈ R$3.600–4.500; **otimista** até 7 vendas ≈ R$6.300 de receita pro salão — plus the disclosure that ~7% of campaigns settle zero, in which case the salon pays nothing (success-only fee, §3). If the salon's real inputs fail the margin gate (precondition P2, ≥15% net floor, §10), the Raio-X says so and proposes a different package — the refusal is printed, not hidden; it is the credibility feature.

### 19.6 Section 5 — Livro de resgates por cliente (redemption-ledger pitch)

The per-client redemption ledger every campaign package gets: each voucher's sessions, dates redeemed, remaining balance, and the exact pro-rata cancellation arithmetic disclosed before purchase (offer-page disclosures in §13; CDC analysis in §5 — validity enforceable only if pre-disclosed, total forfeiture void, avulso re-pricing only if pre-disclosed per TJDFT Acórdão 2110685). Pitch framing: when a client cancels or complains, the salon answers with a dated ledger and disclosed math instead of an argument — the salon's litigation defense, included, not an add-on. This is wedge material no incumbent ships (§4).

### 19.7 Generation pipeline

1. **Auto-render on import.** Every completed import (§9) renders a draft Raio-X (HTML → PDF + private stable URL) — the same engine also powers the free scan's 4 numbers (§15, screen 3).
2. **Founder review — mandatory.** No Raio-X is ever auto-sent. The founder checks band sanity, the Trinks caveat, Section 2 availability, and the Section 4 inputs; edits only the package-design inputs and a short intro note. Locked copy is not editable in the tool.
3. **Delivery on Pix confirmation — auto-release.** The R$490/R$990 charge is created in the founder's own Asaas account (her product — no split, §12). The Asaas payment-confirmation webhook auto-releases the report: an automatic transactional EMAIL (Resend, §7 stack) carries the private URL + PDF to the owner, the dashboard flips the report to "released" and renders the WhatsApp-ready message that the founder forwards manually from her own phone (per-surface channel model, §15.11), and the R$490 credit is booked into the salon's credit ledger (§15, screen 8; mechanics §3).
4. **Regenerations free** on fresh imports; each regeneration is a new dated version, previous versions retained (vault, §16).

### 19.8 The anonymized fair version

For Beauty Fair (September 2026, §22): a printed Raio-X of a real (design-partner, permissioned) or synthetic dataset with salon name replaced by "Salão Exemplo — 1.240 clientes", all counts rounded, no real client data on paper. Same five sections, same locked sentences, so the fair conversation is the product demo: hand it over, point at Section 1, offer the free scan on the spot (§18). If synthetic, footer states "dados ilustrativos"; if permissioned-real, the salon's written permission is a vault artifact (§16).


# PART V — ENTITY, TAX, MONEY

## 20. ENTITY + TAX

### 20.1 The entity decision: SLU, ME, Simples Nacional — incorporated before the first split

Caixa Cheia operates as a **Sociedade Limitada Unipessoal (SLU)**, enquadrada como **Microempresa (ME)**, opting into **Simples Nacional**, incorporated in week 1 — before the first Asaas split ever executes (see §12 for split mechanics, §22 for the week-1 sequence).

Why SLU and not MEI — three reasons, each independently disqualifying:

1. **The revenue cap makes MEI arithmetic impossible.** MEI caps receita bruta at R$81k/year. Because the founder's receita is her 20% fee only (§20.4), R$81k of fees corresponds to roughly **R$405k of GMV per year** — about R$33.7k of settled campaign volume per month. The month-12 model (§21) already passes that. MEI would be outgrown almost immediately, forcing a mid-year migration.
2. **The activity is not MEI-eligible.** Intermediação e agenciamento de serviços e negócios (CNAE 7490-1/04) is not on the MEI permitted-occupations list.
3. **Retroactive desenquadramento risk.** An ineligible or over-cap MEI can be desenquadrada retroactively, recomputing taxes as if the correct regime had applied all along — back taxes plus penalties on every month operated wrongly. For a business whose entire legal posture depends on clean characterization (§5), that is an unacceptable tail risk.

SLU specifically (rather than empresário individual) because it gives **limited liability with a single owner and no partners**, and because incorporating the definitive entity from day one means: pró-labore and Fator R run from month 1, escrituração contábil runs from inception, and the CNPJ never changes — the CNPJ appears in Meta Business Verification (§11), the Asaas account (§12), every DPA and service contract (§5, App C), and every NFS-e. Changing it later would mean redoing all of them.

**Registration parameters:**

| Item | Value |
|---|---|
| Entity type | SLU (Sociedade Limitada Unipessoal) |
| Porte | ME |
| Tax regime | Simples Nacional, target Anexo III via Fator R |
| CNAE principal | **7490-1/04** — intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários |
| Municipality | At or near the **2% ISS floor** (ISS ranges 2–5% by municipality; LC 116 sets the 2% floor). ISS is due at **her** municipality (§20.5), so where the SLU is domiciled directly sets the rate. Select the seat — home office or virtual office — in a municipality charging 2% for item 10.02/10.09 services. This is a permanent ~3-point saving inside the DAS, decided once at incorporation. |
| Service item (LC 116) | **10.02 or 10.09** (agenciamento/intermediação). **Never 1.05 or 1.09** (software licensing) — a software characterization would make her the principal and put gross campaign GMV in her tax base (§20.4). |

### 20.2 Escrituração contábil completa from day one — the R$6,600/month lever

Under LC 123 art. 14 §1º/§2º, a Simples company **without** full accounting books can distribute as exempt dividends only up to a presumed-profit ceiling: **32% × revenue − DAS paid**. Everything distributed above that ceiling is taxed at the owner's marginal IRPF rate, **27.5%**.

With **escrituração contábil completa** (livro diário, balancete, balanço), the exemption covers the **entire accounting profit** — which, for a near-zero-cost operator business like this one, is close to 100% of revenue.

The math at R$60k/month of fee revenue (roughly the month-24 run rate, §21):

```
Without full books (presumption route):
  exempt cap = 32% × revenue − DAS
             = 32% × 60,000 − (≈11.05% × 60,000 ≈ 6,630) = 19,200 − 6,630 = R$12,570
  everything distributed above the cap is taxed at up to 27.5% IRPF
  → at R$60k/mo on Anexo III, ≈ R$6,600/mo lost without full bookkeeping (DERIVED)

With full books: excess = 0. Cost of the books: a contador who is doing them anyway.
```

This is **the single largest tax lever in the business** — worth more per month than the entire infrastructure bill (§21) by a factor of ~25. Escrituração completa is contracted with the contador at incorporation, not retrofitted: books cannot be credibly reconstructed later, and the exemption is tested year by year.

### 20.3 Fator R routine — Anexo III vs Anexo V

Simples service companies under CNAE 7490-1/04 fall in **Anexo V** (15.5% entry rate, rising to ~18.1%) *unless* **Fator R** ≥ 28% — i.e., payroll+pró-labore over the trailing 12 months ≥ 28% of gross revenue over the same window — in which case **Anexo III** applies (effective ~6% at entry, ~11.05% at R$720k RBT12).

**Year 1 is free.** Pró-labore at the 2026 minimum wage (**R$1,621/month**) automatically satisfies the 28% test whenever monthly revenue is below ≈ R$5.8k (1,621 ÷ 0.28). Early months qualify at zero extra cost.

As revenue grows, holding Anexo III requires raising pró-labore to 28% of revenue, and pró-labore carries 11% INSS (employee side) plus IRPF. The trade stops paying at scale:

**Fator R value curve by monthly revenue** (DERIVED; re-derive with the contador quarterly):

| Monthly revenue | Pró-labore needed (28%) | Anexo III vs V saving, net of INSS/IRPF on the pró-labore | Verdict |
|---|---|---|---|
| ≤ R$5.8k | R$1,621 (minimum wage suffices) | Full spread, zero cost | Free — always take it |
| R$15–20k | R$4.2–5.6k | **≈ +R$1,100/mo** (peak of the curve) | Take it |
| R$60k | R$16.8k | **≈ +R$36/mo** (roughly a wash) | Marginal — decide monthly |
| > ~R$61k | > R$17.1k | **Negative** — the INSS/IRPF on the required pró-labore exceeds the Anexo spread | Drop to Anexo V, cut pró-labore back |

**Routine (monthly, with the contador, 15 minutes):** compute trailing-12-month Fator R; project next month; decide pró-labore for the coming month; log the decision. This is a standing agenda item, not a one-time setup — the optimum crosses zero right around the month-24 revenue band (§21), so by 2028 the answer likely flips.

**INSS teto note:** the 2026 INSS ceiling is a salário-de-contribuição of **R$8,475.55**, i.e., a maximum contribution of **R$932.31/month**. Contributions at or toward the teto are not dead weight: they buy **salário-maternidade** (directly relevant to a 26-year-old founder planning a long-horizon company) and pension accrual. When Fator R stops paying, do not automatically drop pró-labore to the minimum — the maternity/pension value of a higher contribution base is a separate, personal decision to price with the contador.

### 20.4 The tax-base architecture: her receita = her 20% only

This is the existential item in the whole money section. The founder's **receita bruta is her 20% fee only**, not the gross campaign GMV flowing through the splits. Legal basis: LC 123 art. 3º §1º — for operations "em conta alheia" (on another's account), receita bruta is the **resultado** of the operation, i.e., the commission; SC Cosit 159/2020 is the analogous Receita Federal reading for commission intermediaries.

**The contract does the work, not the split.** A payment split is just plumbing; what fixes the tax characterization is the legal structure around it. Four conditions must all hold, permanently, in the papered reality (see §5 and App C for the contract clauses):

| # | Condition | Where it lives |
|---|---|---|
| 1 | **The salon is the merchant of record** — the salon's CNPJ is on the PSP charge registration and on every consumer receipt (also a CDC art. 42-A requirement, §5) | Asaas account setup (§12), offer page (§13) |
| 2 | **The consumer contracts with the salon** — the package sale is a salon↔consumer contract; the founder is never a party | Offer page terms, voucher terms (§13) |
| 3 | **The salon invoices the consumer for the full amount**; the founder's NFS-e goes to the salon, for the fee only (§20.5) | NFS-e queue (§15), contador routine |
| 4 | **The service contract states she acts "em nome e por conta do salão"**, remuneration is a percentage commission, and it contains an **express mandate authorizing the PSP to pay her share directly via split**, with that split discharging the salon's payment obligation at settlement | Service contract + DPA (App C) |

**The insolvency math if mischaracterized.** If Receita ever treats the gross as her revenue — e.g., because the contracts read like she is selling packages, or the NFS-e pattern points at consumers, or the service item says software — then at month-24 scale (~R$300k GMV/month ≈ **R$3.6M/year**):

```
Anexo V on R$3.6M RBT12 ≈ 21.3% effective → ≈ R$767k/yr of tax
Her actual cash from that GMV: 20% × 3.6M = R$720k/yr of fees
Tax > total fee income. Instant insolvency.
Plus: R$3.6M approaches the R$4.8M Simples ceiling → regime expulsion risk on top.
```

This is why condition-checking is not optimization — it is survival. Every contract, invoice, and checkout surface is audited against the four conditions before launch (lawyer item, §12/§24), and any product change that touches money flow re-runs the check.

### 20.5 NFS-e mechanics

- **Issued to the SALON, never the end consumer.** One NFS-e per salon per settlement period, for the fee amount (sum of settled splits net of refund reversals in the period).
- **Service item 10.02 or 10.09** (agenciamento/intermediação). Never 1.05/1.09 (§20.1).
- **ISS is due at HER municipality** (LC 116 art. 3º caput; no location exception applies to items 10.02/10.09) — this is what makes the 2%-floor municipality choice (§20.1) effective.
- **The salon may NOT withhold ISS** on her invoices: LC 123 art. 21 §4 bars withholding when the service is taxed at the provider's own seat under Simples. If a salon's bookkeeper tries to withhold, this citation resolves it.
- **The NFS-e MUST state her effective ISS rate** (the rate inside her DAS for the period). If the rate is not stated on the nota, the taker's municipality may apply the **highest** rate. This is a per-invoice mechanical rule — the NFS-e queue (§15, Dinheiro dashboard) enforces the field.
- **Reconciliation trail:** every NFS-e references the underlying settled transactions; the Asaas split reports tie each settlement to each NFS-e. This trail is what proves, in any audit, that fee revenue = split receipts = declared receita (§16 records vault).

ISS (2–5%) is collected inside the DAS; there is no separate ISS payment while in Simples.

### 20.6 Dividends under the 2026 rules

Under **Lei 15.270/2025** (effective 2026):

- **10% IRRF applies only when ONE CNPJ pays ONE person more than R$50k in a single month** — and then on the whole amount, not just the excess. Below R$50k/month: **fully exempt**, as before.
- At her scale — month-24 distributable ≈ **R$54.9k/month** (§21.2) — the rule is explicit: **distribute ≤ R$50k/month per CNPJ and retain the remainder in the company (or take it as additional pró-labore)** → withholding stays **0%**. (Any older planning assumption of a flat 9–10% dividend tax at her scale is wrong.)
- **IRPFM** (minimum tax on high total income): triggers above R$600k/year of total income, phasing linearly to 10% at R$1.2M. Her pró-labore already pays IRPF above the IRPFM floor at her income level, so IRPFM adds nothing at the month-24 scale. Re-check if total annual income approaches R$600k.
- **Contested-for-Simples flag [OPEN]:** whether the 10% dividend IRRF constitutionally reaches Simples companies at all is contested (LC 123 art. 14 exemption + CF art. 146 III d argument). Moot below R$50k/month; if she ever plans a distribution above R$50k in a single month, get the contador's position first — and note the trivial lawful alternative of splitting the distribution across months.

### 20.7 The salon-side honesty block

What the 20% fee costs the **salon**, stated the way she must state it in sales conversations — because getting this wrong in a pitch is both dishonest and legally dangerous:

- **The salon's receita bruta is the FULL R$900**, not R$720. Receita Federal is explicit and repeated: SC Cosit 143/2021, SC Disit 5007/2025, SC Cosit 94/2025 — commissions and marketplace/intermediary fees are **not deductible** from a Simples company's receita bruta; CTN art. 123 bars private contracts from shifting tax liability.
- The salon owes Simples **at the sale** under either accounting regime (caixa = when it receives; competência = when the nota is issued at sale). The split does not defer, reduce, or restructure the salon's tax in any way. **Never imply a tax benefit.**
- **True cost of the 20% fee ≈ 21.6% of gross**: the salon pays Simples on the full R$900 including the R$180 it never keeps, so the fee's effective cost is 20% ÷ (1 − ~8% tax leakage) ≈ 21.6%. The margin gate (§6, §10) already prices this in — that is why the reference math on R$900 charges the salon Simples on gross.
- **Never repeat Asaas's blog claim that split billing "avoids bitributação."** It is wrong. The split changes who receives money, not who owes tax on what. Any salon contador will catch the claim, and credibility with the contador is worth more than any pitch line.
- The honest pitch (locked framing, §6): "desse pacote, sobra R$169 pra você e R$180 pra mim — mas esse cliente não voltava." Sell incrementality and the margin gate, never tax magic.

### 20.8 Contador checklist (week 1, one engagement — see §24)

1. **Escrituração contábil completa from incorporation** — contracted explicitly, with monthly balancetes (§20.2).
2. **Confirm the 20%-only tax base** against the actual contract + PSP architecture (the four conditions, §20.4) — the contador reads the service contract and the Asaas flow and signs off in writing that receita = fee.
3. **Fator R monthly routine** — standing calendar item; pró-labore decision each month (§20.3).
4. **NFS-e setup**: municipality registration, service item 10.02/10.09, effective-ISS-rate field on every nota, no-withholding position (§20.5).
5. **LC 214 forward model** (§20.9): have the contador model, now, whether her 20% computes before or after fiscal tax segregation.

### 20.9 Forward flags

- **LC 214/2025 fiscal split payment.** The IBS/CBS reform introduces *split payment fiscal* — tax segregated at settlement, on the same PSP rails her business runs on, during the 2027+ transition. Two consequences to model **now** with the contador: (a) whether her 20% is computed on the consumer price before tax segregation or on the post-segregation amount — this changes her fee per settle and must be fixed in the contract's fee-definition clause before it matters; (b) her own receipts will eventually arrive tax-segregated. [OPEN] — no operational rules published yet; standing contador agenda item.
- **ISS phase-down 2029–2032**: ISS (and her 2%-floor municipality advantage) phases out as IBS phases in. The municipality choice is worth full value for roughly the first three years and declining value after.
- **Reforma "demais receitas" language**: the reform's broadened revenue definitions are a second, independent reason the software-licensor characterization (items 1.05/1.09) must never attach to her (§20.1, §20.4).

---

## 21. UNIT ECONOMICS + INCOME MODEL

All numbers are labeled **DERIVED** (computed from verified facts elsewhere in this document) or **ASSUMED** (a modeling choice to be replaced by observed data). Fee per settle uses the exact split arithmetic from §12: R$900 charge − R$1.99 Asaas Pix fee → netValue R$898.01 → 20% = **R$179.60**, never R$180.

### 21.1 The per-campaign unit

One win-back campaign: 180 recipients, R$900 package, sent from the salon's own number (§11), Pix-only checkout with split at settlement (§12, §13).

| Line | Value | Label | Notes |
|---|---|---|---|
| Recipients (sent) | 180 | ASSUMED (standard cohort size) | Manifest-approved list after the full gate (§10: 4 campaign preconditions + 9 per-client checks + approval artifact) |
| Delivered | < 180 | DERIVED | Meta per-user marketing cap (error 131049) and no-marketing users (130472) mean delivered is always below sent; settle rates here are quoted **on sent** — the per-delivered rate is higher (§11, App B) |
| Settled purchases | 2 / 4–5 / 7 (conservative / expected / optimistic) | ASSUMED band | ~2.5% of sent at expected case |
| Fee per settle | **R$179.60** | DERIVED (§12 split math) | 20% × netValue R$898.01 |
| Founder fee, gross | R$359 / **≈R$808** / R$1,257 | DERIVED | settles × R$179.60 |
| Zero-settle campaigns | **~7% of campaigns settle zero** | ASSUMED | Already blended into the expected band; two consecutive R$0 at R$900 triggers offer interrogation (Gate 4, §23) |
| Salon's message cost | **≈ R$61** (180 × ~US$0.0625) | DERIVED (§11 pricing) | Pass-through: salon pays Meta directly on its own payment method; founder earns nothing on messages |
| Founder marginal cost per campaign | **≈ R$0** | DERIVED | No BSP, no per-message founder cost, no paid traffic |
| Founder time per campaign | **30–40 minutes real** | ASSUMED | Segment + margin gate + manifest + approval chase + monitor + results message |
| Founder fixed infra | **R$100–300/month TOTAL** | ASSUMED | One server + services (§7); flat regardless of salon count |

The unit is why the business works: revenue per campaign ≈ R$808 expected, marginal cost ≈ R$0, time ≈ 35 minutes. The binding constraints are **campaign supply** (how many eligible locations exist and how often each can lawfully be messaged — max 1 template/client/60 days, §6) and **founder hours**, not costs.

Active-base campaigns (renewals, birthdays, slow-day fills — Gate C accounts only, §6) run the same rails with smaller tickets and cohorts. Their per-campaign contribution is **ASSUMED at R$550** until proven — see §21.4.

### 21.2 The income model: months 6, 12, 24

Tax treatment throughout, per §20: Simples Anexo III via Fator R, escrituração completa, minimum-wage pró-labore early (rising per the Fator R curve), dividends 0% withholding at these scales. Effective DAS rate rises with RBT12: ~6% early, ~11% at the month-24 run rate.

**Month 6 — ≈ R$8–12k/month net** (fair cohort, win-back only, audits contributing cash):

| Input | Value | Label |
|---|---|---|
| Active locations (post-Beauty-Fair cohort) | 12–18 | ASSUMED |
| Campaigns/month (win-back cadence, 60-day frequency ledger) | ~10–14 | ASSUMED |
| Fee per campaign, expected | ≈ R$808 | DERIVED (§21.1) |
| Audit cash net of fee credits | ~R$1–2k/mo | ASSUMED (R$490/R$990 audits, 100% credited against first fees, §3 — early on, credits lag cash) |

```
Gross ≈ 12 campaigns × R$808 ≈ R$9,700  + audits ≈ R$1,500  ≈ R$11,200
− DAS ≈ 6% × 11,200 ≈ R$670        (Anexo III entry rate, low RBT12)
− infra ≈ R$200  − contador ≈ R$800 (ASSUMED)
− pró-labore INSS ≈ R$180 (minimum wage, mostly returns to her as salary)
Net ≈ R$9,300 → band R$8–12k/mo   (DERIVED endpoint)
```

**Month 12 — ≈ R$16–19k/month net** (Gate C open on qualified accounts, ~30–40 locations):

| Input | Value | Label |
|---|---|---|
| Active locations | 30–40 | ASSUMED |
| Blended campaigns/month | ~22–28 | ASSUMED (~0.7/location/mo: win-back cadence + first active-base safras) |
| Blend: mostly win-back ≈R$808, early active-base ≈R$550 | ≈ R$750 avg | ASSUMED |

```
Gross ≈ 25 campaigns × R$750 ≈ R$18,800  + audit cash tapering ≈ R$1,000
− DAS ≈ 7% × 19,800 ≈ R$1,400
− infra R$250 − contador R$1,000 − pró-labore INSS/IRPF net drag ≈ R$400
  (pró-labore now raised toward 28% per Fator R curve, §20.3 — Anexo III saving exceeds cost)
Net ≈ R$16,700 → band R$16–19k/mo   (DERIVED endpoint)
```

**Month 24 — ≈ R$45–55k/month personal net** (the honest target):

| Input | Value | Label |
|---|---|---|
| Owners | ~70 | ASSUMED |
| Locations (multi-unit groups drive locations > owners) | ~100–160 | ASSUMED |
| Blended cadence | monthly-ish, ~0.8 campaigns/location/mo → ~95–125 campaigns/mo | ASSUMED |
| Blend: win-back ≈R$808 DERIVED + active-base **≈R$550 ASSUMED — load-bearing, see §21.4** | ≈ R$620 avg | ASSUMED |

```
Gross ≈ 110 campaigns × R$620 ≈ R$68,200
− DAS ≈ 11.05% × 68,200 ≈ R$7,540   (Anexo III at ~R$720k+ RBT12; Fator R now ~breakeven,
                                      re-decide monthly per §20.3)
− infra R$300 − contador R$1,500 − part-time ops VA ≈ R$2,500 (ASSUMED, hired ~month 18)
− pró-labore tax drag ≈ R$1,500 (net of the salary she pays herself)
Distributable ≈ R$54,900; distribute ≤ R$50k/mo per CNPJ and retain the remainder
  (or take it as additional pró-labore) → 0% IRRF holds (§20.6)
Personal net ≈ R$46–55k/mo → band R$45–55k   (DERIVED endpoint)
```

Founder time check at month 24: ~110 campaigns × 35 min ≈ 64 hours/month of campaign work, plus onboarding and sales — full but feasible for one person with a part-time VA; this, not cost, is the scaling wall.

### 21.3 What must prove true for R$150k/month (month 36–48, not the plan)

R$150k/month is **not the target** — it is the conditional upside, reachable in months 36–48 only if ALL of the following hold:

1. **Active-base contribution ≥ R$550/campaign holds at 100+ campaigns** of observed volume (not the first lucky safras).
2. **A Lista reaches ≥ 500 qualified doors, including 60+ multi-unit groups** (§2, §17).
3. **Group mix delivers ≥ 2 locations per owner** on average — one relationship must keep equaling N locations (§2).

Miss any one and the business plateaus in the R$45–55k band — which is the stated, sufficient goal (§1).

### 21.4 The load-bearing assumption, flagged

**Active-base campaigns at ≈ R$550/campaign is the single assumption the month-24 and month-36+ numbers stand on.** Win-back economics (~R$808) are grounded in the fee math and conservative settle rates; active-base economics are projected, because renewals/birthday/slow-day cohorts are smaller and their settle behavior is unobserved until Gate C opens (~weeks 10–12, §22). It is labeled ASSUMED everywhere it appears, and Gate 7 (§23) exists to test it: **first 30 active-base campaigns must show median ≥ R$300 or Gate C re-closes.**

### 21.5 The R$300 downside world

If active-base lands at ≈ R$300/campaign instead of R$550: the blended average collapses toward win-back-only economics, cadence caps (1 template/client/60 days; 2 active-base campaigns/location/quarter, §6) bind harder, and the ceiling restates to **≈ R$30–35k/month** — a win-back + audits + groups business. Still a good one-person company; not the R$45–55k model. Critically, **she knows which world she is in by month 5**: the first 30 active-base campaigns land within weeks of Gate C opening, and the kill-condition dashboard (§15, §23) states the ceiling automatically. The fallback is known by Christmas 2026 (§23).

### 21.6 Fee sensitivity: the 10% lever

If the fee ever reprices from 20% to the documented fallback of **10%** (a founder-only lever, never offered proactively — §6), **everything in §21.2 scales down 30–50%**: fee per settle halves to R$89.80, and while lower friction may lift settle counts somewhat, no realistic lift recovers the halved take rate. The month-24 band would read ≈ R$25–35k. This is documented so the number is known **before** any negotiation where a large group demands it — it is a lever she may choose to pull for a strategic account, never a concession made in the room. Nothing else in the model (messages, infra, taxes) changes; the fee percentage is the entire sensitivity.


# PART VI — EXECUTION

## 22. THE 90-DAY PLAN

Timeline anchor: Week 1 begins late July 2026. Beauty Fair São Paulo runs 5–8 September 2026 (professional badge adds 4 September), landing in Weeks 6–7. The plan ends late October, when Gate 5 is read.

Owners: **F** = founder (the only human); **B** = build session (Claude Code); **L** = lawyer; **C** = contador.

| Week | Work | Owner | Deliverables | Exit criteria |
|---|---|---|---|---|
| **1** | Full week-1 checklist (§24): Asaas sandbox split test; Meta Business Verification + Tech Provider App Review started; SLU incorporation started; Beauty Fair registration (R$50 public tier dies 31/07; professional badge free); Trinks trial screenshots; Avec token pull; lawyer + contador engaged; domain/hosting | F (+B for test scripts) | Gate 1 sandbox result; Meta clock running; fair badge application in; Trinks/Avec column evidence | Gate 1 sandbox PASS; Meta application submitted; every §24 box ticked |
| **2** | M0: repo, schema, state machines, audit tables, secrets vault. Adapter column maps frozen from week-1 evidence | B | Migrated schema; CI; frozen Trinks map | M0 DoD met; Gate 2 read (última visita column exists → adapter proceeds; else redesign per §9) |
| **3** | M1: Trinks adapter, allowlist classifier, gate, scan. Start M3 offer page (CDC disclosure block from L's clause work) | B (+L clause review) | Working scan on a real export; dropped-columns receipt | M1 DoD met; scan produces 4 numbers from a real file |
| **4** | M3 complete: Asaas integration, splits, webhooks, pro-rata refund engine. **Gate 1 production re-run at R$5** (needs SLU CNPJ + approved production account). M2 Raio-X generator | B, F (production test) | Sandbox loop green; production R$5 split DONE; first Raio-X PDF | M2 + M3 DoD met; Gate 1 production PASS (fail → Efí rebuild, plan slips ~2 weeks) |
| **5** | M4: Embedded Signup v4 coexistence, BRL WABA creation, pt_BR templates submitted. Webhooks + suppression paths + consent QR page (M5 start). **3-day Lista sweep (Gate 3)**, then full census into A Lista CRM. Recruit 3 design partners (≥1 group) | B, F (partner recruiting) | ES flow working on test number; templates approved; Lista seeded; Gate 3 count | Gate 3 read: ≥15 owner-operated 2–8-unit brands SP+Rio → hold; <8 → re-base targeting before the fair |
| **6** | M5 complete: send engine, monitors, heartbeat. Design partners scanned; first Raio-Xs sold. Fair prep: named-target schedule from the Lista, printed anonymized Raio-X samples, scan-on-the-spot flow rehearsed on founder's laptop | B, F | Warm send on small cohort; fair kit (targets list, print pack, QR cards) | One real campaign approved and sent to a warm cohort; fair kit complete |
| **6–7** | **BEAUTY FAIR, 4–8 September** (see week plan below) | F | 25 audit conversations; 10 paid audits; scans performed on the spot | ≥10 paid Raio-Xs OR a documented read on why not (feeds Gate 5) |
| **7–8** | Onboard fair cohort: guided 30-min sessions (ES popup, Asaas key + walletId, 3 e-signatures). First win-back safras for new accounts. M6 dashboards hardening | F (sessions), B | Fair cohort active; campaigns settling | First 3 salons end-to-end (Gate 4 opens); onboarding ≤30 min owner time each |
| **8–10** | Avec adapter (from week-1 token evidence); win-back safra #2 across cohort; event-trigger queries; group aggregation views; M7 records vault complete | B, F | Avec adapter live; per-salon results ledgers; vault assembles defense files | Gate 4 read: 2× R$0 settles at R$900 → interrogate the offer, not the code |
| **10–12** | Gate C opens per qualifying account (2 settled win-backs + WABA GREEN + opt-out <1%, §3): first active-base safras (renewals, birthdays, slow-days). Kill-condition dashboard. Gate 6 watch (group waves unit #2) | F, B | First active-base campaigns; kill-condition dashboard live | **31/10: Gate 5 read** (scan→audit ≥20% of first 60). Gate 7 accumulating toward its 30-campaign read |

**Lawyer/contador track (parallel, weeks 1–4):** L delivers the five artifacts of the §24 checklist (LIA + laser annex is item #1 — laser targets are frozen until it lands); C confirms the 20%-only tax base architecture, sets up escrituração completa, Fator R monthly routine, NFS-e municipality + ISS rate statement.

### 22.1 Beauty Fair week plan (4–8 September)

- **Before the fair:** named-target schedule built from the Lista — every multi-unit brand and franchisor with a São Paulo presence gets a name, a booth/likely-presence note, and a time slot; Booksy/Trinks enumeration data (§2) prioritizes 2–8-unit owner-operated groups. Print pack: anonymized Raio-X samples (real structure, fake salon) + consent-QR A5 cards + one-page "a frase" leave-behind.
- **On the floor, per conversation (~10 min):** the sentence (§1, verbatim pt-BR) → ask which system they use (a trinks.com booking page IS the signal) → **scan on the spot**: owner exports the client file from their phone/laptop or forwards it; founder runs the scan on her laptop; four numbers back in minutes → show the printed anonymized Raio-X as "this is what R$490 buys, and it comes back as credit" → close the R$490 Pix there or book a 20-min call.
- **Targets:** 25 audit conversations, 10 paid audits across the four days. Multi-unit groups and franchisors outrank volume — one franchisor conversation (COF question: who mandates the software, who owns client data) is worth ten single-salon pitches.
- **Evenings:** log every conversation into A Lista CRM (status, system, next action); same-night follow-up message to every scan performed.

---

## 23. GATES, KILL CONDITIONS, AND THE OPEN REGISTER

### 23.1 The seven gates

| # | Test | When | Go reading | No-go reading → fallback |
|---|---|---|---|---|
| 1 | Asaas unlinked split: sandbox (independent account B), then production at R$5 | Week 1 (sandbox); Week 4 (production) | 200 + split PENDING→DONE; refund reverses; B's balance moves | 400/403 on split → **Efí** (named "Split Pix" product; verify recipient model), then Woovi/OpenPix; M3 rebuilt on the new rail |
| 2 | Trinks export carries última visita as a COLUMN (plus package join key, value-vs-sessions) | Week 1 screenshots; read Week 2 | Column exists → adapter as specced (§9) | Filter-only → adapter redesign: filtered-export-per-window flow before M1 freeze |
| 3 | Lista 3-day sweep, SP+Rio "unidade" variants | Week 5 | ≥15 owner-operated 2–8-unit brands → group-first model holds | <8 → re-base targeting (single premium salons + franchisors) before the fair; 8–14 → proceed, flag |
| 4 | First 3 salons end-to-end | Weeks 7–8 | Campaigns settle; fees land; owners re-approve safra #2 | 2 campaigns settle R$0 at R$900 → interrogate the OFFER (package, price, copy), not the pipeline |
| 5 | Scan→audit conversion ≥20% of first 60 scans | By 31 October 2026 | ≥20% → R$490 audit holds as the paid door | <20% → audit free-for-groups; economics restated campaign-only |
| 6 | First group waves unit #2 after unit #1 settles | Weeks 10–12 (event, not date) | Group expansion motion proven → multi-unit thesis holds | No group expands unprompted → group revenue modeled as N independent sales, month-24 numbers re-derived |
| 7 | First 30 active-base campaigns: median fee ≥R$300 | Accumulates from Week 10; read when n=30 | ≥R$550 median → month-24 R$45–55k model intact; R$300–550 → interpolate | <R$300 median → Gate C re-closes; ceiling restated ~R$30–35k/month |

### 23.2 Kill conditions and the honest fallback

If Gates 5–7 all read badly — audits don't convert, groups don't wave, active-base medians land ≈R$300 — the business does not die; it caps. The fallback is win-back campaigns + paid audits + whatever groups did close: a calm one-person business with a ceiling around **R$30k/month** (DERIVED from Gate 7's low branch, §21). The design guarantees the founder **knows which world she is in by Christmas 2026**: Gate 5 reads 31/10, Gate 7 within roughly 30 active-base campaigns of Gate C opening. There is no zombie scenario where she operates for a year without knowing.

Hard kills (stop, don't cap): Gate 1 fails in production **and** Efí/Woovi also fail the unrelated-recipient split (no attribution rail = no business as designed); Meta Tech Provider application is rejected with no cure path (the R$0 WhatsApp architecture is constitutional — a BSP cost structure per §11 interim options is a bridge, not a home).

### 23.3 The complete [OPEN] register

Every unresolved item in this document. Owner **F** = founder, **B** = build session, **L** = lawyer, **C** = contador.

| # | [OPEN] item | What settles it | Cost | Owner |
|---|---|---|---|---|
| 1 | Trinks: última visita as export column | Trial export header screenshot | 20 min trial | F |
| 2 | Trinks: package export client join key | Same trial session | included | F |
| 3 | Trinks: balances export as value vs sessions only | Same trial session | included | F |
| 4 | Trinks: WhatsApp add-on pack prices (price anchor) | Screenshot in trial | included | F |
| 5 | Avec: exact columns of reports 0031/0129/0063/0006 | One API token + 4 GET calls | 15 min | F+B |
| 6 | Meta: official BRL rate-card figures | Download Meta's CSV rate card | 10 min | B |
| 7 | Meta: BR utility-rate conflict ($0.0068 vs $0.0080/msg) + Oct 2026 service-message charge | Meta CSV rate card + pricing docs at build time (replies themselves stay in Business App) | 10 min | B |
| 8 | Meta: MM API availability on coexistence numbers | Meta docs / test once TP access granted | 30 min | B |
| 9 | Meta: current featureType string for coexistence ES (`whatsapp_business_app_onboarding` vs stale `coexistence`) | ES v4 docs at M4 build | 15 min | B |
| 10 | Meta: ~4 coex WABAs per portfolio limit (Infobip-sourced only) | Meta docs or empirical; moot under client-owned portfolios | 15 min | B |
| 11 | Meta: quality auto-demotion removal (Oct 2025) | Meta quality-rating docs at M5 | 15 min | B |
| 12 | Asaas: production unlinked split — **THE go/no-go (Gate 1)** | R$5 production test per §12 script | R$5 + 1h | F+B |
| 13 | Asaas: reversal after recipient withdrew (negative balance? queued debit? failure?) | Sandbox: withdraw B to zero, then refund | 30 min | B |
| 14 | Asaas: `PAYMENT_SPLIT_FEE` webhook enum meaning | Written definition from Asaas commercial | 1 email | F |
| 15 | Legal: state-registry supplier list-access mechanism (SP first; PROCON-SP FAQ Q10 implies one exists). **REQUIRED BEFORE FIRST SEND** — gate check C6 is fail-closed: with no list loaded, promotional sends to recipients attributed to that state are blocked; the lawyer may authorize a documented interim measure | Lawyer query / PROCON-SP contact (week-1 lawyer item #5; first sends are weeks 4–6) | inside L engagement | L |
| 16 | Legal: laser client-status question (does "is a client of a laser clinic" itself reveal health data?) — lawyer item #1 | LIA laser annex sign-off | inside L engagement | L |
| 17 | Legal: ANPD titular-rights regulation status | Lawyer check at engagement | inside L engagement | L |
| 18 | Legal: state gift-card/voucher laws sweep | Lawyer sweep | inside L engagement | L |
| 19 | Market: 40-group tripwire — Gate 3 sweep result | 3-day SP+Rio "unidade" sweep | 3 days F time | F |
| 20 | Market: current CNAE 9602-5/01 counts (1,661 figure is stale vintage) | Re-pull from public CNPJ data before external use | 2h | B |
| 21 | Market: COF terms on franchisor data/software control | Request COF as prospective franchisee (free) | 1–2 emails per brand | F |
| 22 | Gendo: whether client listing export carries Última Visita | 20-min screen-share with a Gendo salon | 20 min | F |
| 23 | Dualhook: bulk campaign-send capability (only if interim BSP needed) | Vendor support question before committing | 1 email | F |
| 24 | Chatwoot: history-sync shipped? 180-recipient template campaign capable? (only if used) | Test install once TP creds exist | 2–4h | B |
| 25 | Meta: exact 3-month number-age rule for coexistence eligibility (Gupshup-sourced; Meta wording unconfirmed) | Meta coexistence docs / empirical test at M4 | 15 min | B |
| 26 | Meta: ES v4 token-exchange endpoint (exact endpoint + request/response shape) — currently ASSUMED | ES v4 docs at M4 build | 15 min | B |
| 27 | Meta: heartbeat activity-signal source (how "Business App opened" is detected for the day-9 alert) | Meta docs / empirical test on a coexistence number at M5 | 1h | B |
| 28 | AppBarber: package-export Excel button (does the packages report export?) | Vendor help-center / trial screenshot | 20 min | F |
| 29 | Fresha: package export (CPC-47 balance exclusion unprovable on Fresha without it) | Fresha export docs / trial | 30 min | F |
| 30 | Avec: report 0031 ingestion pending lawyer sign-off (field-level allowlist review) | Lawyer review of 0031 columns from open item #5 | inside L engagement | L |
| 31 | E-sign: in-app click-to-sign (name, timestamp, IP hash) ASSUMED sufficient for these B2B docs; no external provider at launch | Lawyer confirms sufficiency | inside L engagement | L |
| 32 | NFS-e: municipal issuance mechanics (v1 = manual issuance with tracking queue) | Contador states the municipality's flow + credentials | inside C engagement | C |
| 33 | Raio-X delivery page: teaser-before-payment vs no-URL-until-paid | Founder decision at M2 | 0 | F |
| 34 | Suppression scope model: global vs per-business defaults beyond the locked rules (131050/user_preferences = global; owner_request = per-business) | Founder + lawyer review | inside L engagement | F+L |
| 35 | Approval validity (7 days) + owner magic-link expiry (30 days) — **LOCKED, resolved by default** (§15.5/§7.6); revisit only on lawyer objection | Lawyer may flag at engagement | 0 | L |
| 36 | Legal: data-subject response deadlines (ANPD regulation absent — interim deadline to adopt) | Lawyer sets interim SLA at engagement | inside L engagement | L |

---

## 24. WEEK-1 CHECKLIST

Every item is a real-world action; most gate later code. Time estimates are founder-hours unless marked.

- [ ] **Register for Beauty Fair — TODAY.** Professional badge (free, CNPJ or beauty-course certificate as proof of activity, approval ≤3 business days, includes 4 September). Backup: buy the R$50 public ticket before the tier expires **31 July**. *(30 min + R$0–50)*
- [ ] **Asaas sandbox split test (Gate 1, sandbox leg).** Create account A and — independently registered at sandbox.asaas.com, never via API from A — account B. Run the §12 script: charge R$900 with `splits:[{walletId, percentualValue: 20}]` → assert PENDING → confirm in UI → assert netValue ≈ 898.01, split ≈ 179.60 → full refund → `refundedSplits[].done true` → partial refund with `splitRefunds`. Also run open item #13 (withdraw-then-refund). *(2–3h with build session writing the script)*
- [ ] **Start Meta Business Verification + Tech Provider App Review.** Business-type Meta app with WhatsApp use case; classic Business Verification of her entity; App Review for `whatsapp_business_messaging` + `whatsapp_business_management` with the two demo videos; Access Verification. The 3–6 week clock starts only when submitted. *(3–4h to assemble + submit)*
- [ ] **Start SLU incorporation.** SLU, ME, Simples Nacional, CNAE principal 7490-1/04, municipality at/near the 2% ISS floor. Must exist before the first production split. *(2h founder + contador runs it)*
- [ ] **Trinks trial + header screenshots (Gate 2 evidence).** Open a trial; export Meu Estabelecimento > Clientes > Todos os clientes > Mais filtros > Exportar, plus "Relatório de clientes que não retornaram" and "Relatório de Saldo de Pacotes". Screenshot header rows; screenshot WhatsApp add-on pack prices (open items #1–4). *(1h)*
- [ ] **Avec API token pull.** Obtain a token for `api.avec.beauty`; GET reports 0031, 0129, 0063, 0006 for exact columns (open item #5). *(30 min)*
- [ ] **Engage the lawyer** with the five-item checklist (reproduced in App C): (1) LIA template sign-off + laser annex — item #1; (2) sensitive-service copy rules; (3) DPA + service contract (operator clauses, mandate-to-split, merchant-of-record); (4) offer-page cancellation clause per TJDFT Acórdão 2110685; (5) state-registry compliance approach (SP list-access first — REQUIRED before the first promotional send; gate check C6 is fail-closed **[OPEN #15]**). *(1h briefing; ASSUMPTION: fee not in this document — get a quote)*
- [ ] **Engage the contador** with the five-item checklist: (1) escrituração contábil completa from incorporation; (2) contract+PSP architecture confirming the 20%-only tax base (LC 123 art. 3º §1º); (3) Fator R monthly routine; (4) NFS-e municipality + ISS rate statement (10.02/10.09, never 1.05/1.09); (5) LC 214 split-payment forward model. *(1h briefing)*
- [ ] **Domain + hosting setup.** Domain, DNS, hosting for the Next.js app + always-on worker (Railway or Fly.io per §7), Postgres (Supabase acceptable), secrets vault. *(1–2h, mostly build session)*
- [ ] **Hand the build session its M0 kickoff** — this document + the §0.4 status answers. *(15 min)*

Week-1 total founder time: roughly **12–15 hours**. Nothing on this list waits for anything else on it; run all clocks in parallel.

---


# APPENDICES


## Appendix A — pt-BR Copy Pack

Every user-facing string in one place. **TEMPLATE** = submitted to Meta for review, language `pt_BR`, subject to §11 mechanics (body ≤1,024 chars; no `$` or `%` inside `{{variables}}`; sequential positional params; no dangling start/end params; URL button with exactly one variable appended at the END of the URL; no wa.me links; templated messages render **no URL preview** — the copy carries all weight). Client-facing templates (A.5, A.6) are category **MARKETING**; the two owner-facing automated messages (A.4 approval request, A.7 results) are category **UTILITY**, sent from the salon's own WABA to the owner's phone — ASSUMPTION: service-management follow-up on the owner's own mandate is a defensible UTILITY categorization; recategorization risk (Meta reclassifying to MARKETING) is noted. **FREE-FORM** = ordinary WhatsApp/App message or web/print copy, no Meta review. Items marked **(locked)** are verbatim from §6 and may not be edited by anyone, including a builder session.

### A.1 The business sentence (locked) — FREE-FORM (pitch, site, fair)

> "Eu escaneio seu sistema de graça e te mostro quanto dinheiro está dormindo no seu salão. O raio-X completo custa R$490 e volta inteiro como crédito. Depois eu rodo suas campanhas pelo seu próprio WhatsApp — e só ganho 20% do que cair no seu Pix. Zero mensalidade, sempre."

### A.2 Scan-result message — FREE-FORM (founder → owner, from her own phone, manual)

> "Pronto, [NOME] — escaneei o [SALÃO] de graça. Olha os 4 números:
> • **{{total}}** clientes no seu sistema
> • **{{sumidos}}** sumiram há mais de {{X}} dias
> • **{{contactaveis}}** têm WhatsApp válido
> • **{{elegiveis}}** eu posso contatar dentro das regras (LGPD + WhatsApp)
> Isso é dinheiro dormindo. O Raio-X completo mostra quanto, cliente por cliente, e o que fazer — custa R$490 e volta inteiro como crédito nas primeiras campanhas. Quer ver?"

### A.3 Audit offer message — FREE-FORM (founder → owner, from her own phone, manual)

> "O Raio-X do Caixa custa R$490 (uma vez só — grupo de até 8 unidades: R$990). Ele mostra: quanto os clientes sumidos representam em receita, quanto você já recebeu por serviços que ainda não entregou, e o plano de campanha pronto. E os R$490 voltam **inteiros** como crédito descontado das minhas primeiras comissões — na prática, o Raio-X sai de graça se a gente trabalhar junto. Vale por 12 meses. Aqui o Pix: {{link}}"

### A.4 Approval request message — TEMPLATE (UTILITY, Meta-submitted; salon's WABA → owner's phone; the approval artifact)

Sent from the **salon's own number** so the owner's reply arrives via the messages webhook and is captured to `approvals.owner_reply_wamid` (see §8, §15). APROVO matching: **case-insensitive exact word, trimmed**. Approval validity: **7 days** — expired → re-approve. Category UTILITY is an ASSUMPTION (service-management follow-up on the owner's own mandate); recategorization risk noted. Shown with named placeholders for readability; submitted with sequential positional params.

> "**Aprovação de campanha — [SALÃO]**
> Data: {{data}}
> Segmento: {{regra_do_segmento}} (ex.: última visita entre 90 e 360 dias, sem pacote ativo, sem mensagem nos últimos 60 dias)
> Destinatários: **{{n}}** clientes
> Oferta: {{pacote}} por R$ {{preço}} ({{sessões}} sessões, validade {{validade}})
> Modelo de mensagem: {{template_id}} (v{{versão}})
> Mensagem exata que seus clientes vão receber:
> ---
> {{texto_completo_do_template}}
> ---
> Envio: {{dia}}, horário comercial.
> Sua conta neste pacote: sobra ~R$ {{margem_salao}} por venda depois de comissão, insumos, impostos e minha taxa.
> Para autorizar, responda **APROVO**. Sem a sua aprovação nada é enviado. Esta aprovação vale por 7 dias."

(The margin line operationalizes the locked sales framing from §6: "desse pacote, sobra R$169 pra você e R$180 pra mim — mas esse cliente não voltava.")

### A.5 Win-back template exemplars — TEMPLATE (Meta-submitted)

Generic by construction: **no service is ever named** in template copy (Option B, see §5/§6). Discount figures live in static text, never inside variables. Each has one URL button.

**`volta_oferta_01`** — body:

> "Oi, {{1}}! Aqui é do [SALÃO]. Faz tempo que você não aparece e a gente sentiu sua falta. Preparamos o {{2}} com condição especial, válida só até {{3}}, exclusiva pra quem já é de casa. Toque no botão pra ver os detalhes e garantir pelo Pix. Se preferir não receber ofertas, é só responder SAIR."
> Button (URL): **Ver minha oferta** → `https://oferta.caixacheia.com.br/o/{{1}}`

**`volta_oferta_02`** — body:

> "{{1}}, sua cadeira continua aqui no [SALÃO] 🙂 Montamos o {{2}} com valor especial pra você voltar — são poucas vagas e a condição termina em {{3}}. Veja tudo certinho (preço, sessões e validade) no link e pague direto pelo Pix. Não quer mais receber mensagens assim? Responda SAIR."
> Button (URL): **Quero ver** → `https://oferta.caixacheia.com.br/o/{{1}}`

**`volta_oferta_03`** — body:

> "Oi, {{1}}! O [SALÃO] liberou o {{2}} pra um grupo pequeno de clientes — e você está na lista. Vale até {{3}}. No link você vê o pacote completo, com todas as regras, e garante na hora pelo Pix. Pra não receber ofertas, responda SAIR."
> Button (URL): **Ver condição** → `https://oferta.caixacheia.com.br/o/{{1}}`

(All bodies < 1,024 chars. **Body params:** {{1}} first name / {{2}} the package's commercial name, owner-authored — linted against the versioned P3 wordlist, never a service name / {{3}} validity date rendered from `campaigns.offer_valid_until`. **[SALÃO] is static text** — templates are submitted per salon WABA, so the salon's name is fixed copy, not a variable. **Button params are a separate namespace from body params**: the single button variable — written `{{1}}` in its own namespace — carries the **per-campaign** opaque offer token (`campaigns.offer_page_slug`), the same value for every recipient in the send (see §11, §13); it is never per-recipient and never PII. Copy is exemplar-grade; final per-salon submissions may vary wording but never the structural rules. The `oferta.caixacheia.com.br` domain is an ASSUMPTION pending domain purchase — see §7.)

### A.6 Active-base template exemplars — TEMPLATE (Meta-submitted; Gate C accounts only)

**Renewal — `renova_pacote_01`:**

> "Oi, {{1}}! Seu pacote no [SALÃO] está quase no fim. Pra você não ficar sem, liberamos o {{2}} — condição de renovação válida até {{3}}, com vantagem exclusiva de cliente da casa. Veja os detalhes e renove pelo Pix no link. Pra não receber ofertas, responda SAIR."
> Button (URL): **Renovar com vantagem** → `https://oferta.caixacheia.com.br/o/{{1}}`

**Birthday — `aniversario_01`:**

> "{{1}}, parabéns pelo seu mês! 🎉 O [SALÃO] preparou um presente: o {{2}}, uma condição especial de aniversário válida até {{3}}. É só tocar no botão pra ver e garantir pelo Pix. Não quer receber ofertas? Responda SAIR."
> Button (URL): **Ver meu presente** → `https://oferta.caixacheia.com.br/o/{{1}}`

**Slow-day — `agenda_semana_01`:**

> "Oi, {{1}}! Abrimos alguns horários com condição especial no [SALÃO] pra esta semana: o {{2}}, válido até {{3}} — poucas vagas. Veja o pacote e garanta o seu pelo Pix no link. Pra sair da lista de ofertas, responda SAIR."
> Button (URL): **Garantir horário** → `https://oferta.caixacheia.com.br/o/{{1}}`

(Same param rules as A.5: body {{1}} first name / {{2}} owner-authored package commercial name / {{3}} validity from `campaigns.offer_valid_until`; [SALÃO] static; button variable = per-campaign offer token in its own namespace.)

### A.7 Results message — TEMPLATE (UTILITY, Meta-submitted; salon's WABA → owner's phone, post-settlement; automated)

(Category UTILITY is an ASSUMPTION, same recategorization risk as A.4. Shown with named placeholders for readability; submitted with sequential positional params.)

> "**Resultado da campanha de {{data}} — [SALÃO]**
> Enviadas: {{enviadas}} • Entregues: {{entregues}}
> Vendas pagas no Pix: **{{vendas}}** — total **R$ {{bruto}}**
> Minha taxa (20% do líquido): R$ {{taxa}} {{credito_raio_x_aplicado}}
> Estornos: {{estornos}}
> O dinheiro já está na sua conta Asaas. Extrato completo: {{link_ledger}}
> Próxima janela possível pra esse grupo: {{proxima_data}} (regra dos 60 dias)."

### A.8 Heartbeat nudge (locked) — FREE-FORM (founder → owner, sent manually from her own phone at day 10 of inactivity; dashboard alert day 9, phone call day 12)

> "abre o WhatsApp do salão hoje pra manter tudo rodando 🙂"

### A.9 Consent statement (locked) — print/web (consent capture page and A5 QR card; see §14)

Locked checkbox (unticked, unbundled, never conditioned on a discount; single scope `whatsapp_marketing` at launch — granular scopes are a post-launch ASSUMED extension, see §14):

> "☐ Autorizo o [SALÃO] (CNPJ …) a me enviar mensagens por WhatsApp, no número que informei, com promoções, ofertas e novidades sobre seus serviços. Posso cancelar quando quiser, de graça, respondendo SAIR. Não autorizar não muda em nada o meu atendimento."
>
> "Saiba como usamos seus dados: [QR/link]"

### A.10 Reception script — spoken, FREE-FORM (taught in the guided session; **optional** — the QR card works standalone, see §14)

> "A gente tem um cartãozinho aqui: se você marcar, o salão te avisa no WhatsApp quando tiver promoção. É de graça, você cancela quando quiser respondendo SAIR, e não marcar não muda nada no seu atendimento."

### A.11 Opt-out confirmation — FREE-FORM (**optional, owner-sent**: a founder-drafted quick-reply saved in the salon's WhatsApp Business App that the owner MAY send — zero obligation, never sent automatically; no auto-reply ever, locked #9. Suppression is immediate and silent regardless; page-initiated opt-outs are confirmed by the opt-out page itself — see §14, §15)

> "Pronto! Você não vai mais receber ofertas do [SALÃO] por WhatsApp. Seu atendimento continua igualzinho. Se mudar de ideia, é só avisar a gente por aqui."

### A.12 Refund acknowledgment — FREE-FORM (owner-facing, when a refund executes)

> "Estorno processado: R$ {{valor}} devolvidos a {{cliente_iniciais}} via Pix, direto da conta do salão, referente a {{sessões_não_usadas}} sessões não utilizadas. Minha taxa sobre essa parte foi estornada junto — você não paga comissão sobre dinheiro devolvido. Recibo no extrato: {{link}}"

### A.13 Owner disclosure checklist — read aloud in the guided session, each line confirmed and logged (see §11 for the underlying mechanics)

> 1. "Suas **listas de transmissão** deixam de funcionar — as antigas ficam só de leitura. As campanhas passam a sair pelo sistema, com aprovação sua, uma a uma."
> 2. "A **foto de perfil** do WhatsApp do salão **congela** — depois da conexão ela não pode mais ser trocada. Escolhe a foto boa agora."
> 3. "Alguém do salão precisa **abrir o app do WhatsApp pelo menos a cada 13 dias**, senão a conexão cai sozinha. Eu te aviso antes, mas a regra é essa."
> 4. "Os **aparelhos conectados** (WhatsApp Web etc.) vão desconectar na hora — é só conectar de novo. Windows e relógio não são suportados."
> 5. "As **mensagens das campanhas** você paga direto pra Meta, uns R$60 por campanha de 180 clientes, no seu boleto. Eu não ganho nada em cima disso."
> 6. "O que você ganha em troca: campanhas profissionais saindo do **seu próprio número**, seus clientes respondendo **pra você**, e eu só ganho se **cair Pix na sua conta**."

### A.14 Raio-X do Caixa — section headers (the audit document; content spec in §19 — five sections, fixed order)

> 1. "**Mapa de receita adormecida**"
> 2. "**Dinheiro recebido, serviço devido**" (uses ONLY the locked accounting language from §19 — never "passivo", never "dívida", never "imposto sobre isso"; Trinks caveat: number = "saldos ativos não consumidos" only)
> 3. "**Quem você pode chamar**"
> 4. "**Primeira campanha recomendada**"
> 5. "**Livro de resgates por cliente**"


## APPENDIX B — ERROR / WEBHOOK HANDBOOK (META HALF)

(Asaas half: see the payments portion of Appendix B, cross-ref §12.)

| Code / event | Meaning | System action | Founder-visible alert |
|---|---|---|---|
| **131049** | Per-user marketing cap reached (adaptive, global across all businesses; Brazil in scope; no published limit) | Mark recipient CAPPED_24H, terminal for this campaign. **NEVER auto-retry** (retry ⇒ 24h blackout for the recipient). Not billed; excluded from delivered-based economics | None per-message; campaign summary shows capped count; >20% of campaign → list-freshness flag |
| **131050** | Recipient disabled marketing messages via WhatsApp "Offers and announcements" | Permanent **global** suppression write (path 2; business_id NULL, see §8). Never send again | Suppression counter increments; visible in Supressão center |
| **132015** | Template paused by Meta (quality ladder 3h → 6h → Disabled) | Halt entire queue for that template; hold campaign; re-warm on unpause; Disabled → retire template, create new | **Yes — immediate**: "Template pausado (3h/6h/desativado)" with campaign name |
| **131048** | Number-level spam restriction | Halt ALL sends on the number; freeze scheduled campaigns for the salon | **Yes — sev-1**: number restricted, salon name, last-campaign stats |
| **131026** | Recipient cannot receive the message | Skip recipient, mark UNDELIVERABLE, no retry this campaign | Campaign summary count only |
| **130472** | Recipient is in Meta's marketing-holdout experiment group | Skip; count separately; **not an opt-out — do not suppress**; not billed | Campaign summary count only |
| **Error 100** (template create) | Bad request — most common cause here: wrong language code (must be `pt_BR`) | Fail template submission locally; lint should prevent | Template screen shows rejection reason |
| `held_for_quality_assessment` (message status) | Meta holding messages from a new/unpaused template pending early-feedback assessment | Mark HELD; await release/drop status. Drops >10% of warm cohort → auto-pause campaign | **Yes** if drop-cluster triggers auto-pause |
| `PROMOTIONAL` (template rejection) | Offer copy submitted under UTILITY category | Never occurs by policy (MARKETING always); if seen, resubmit as MARKETING | Template screen |
| **`messages`** (webhook: statuses) | sent / delivered / read / failed per recipient | Drive per-recipient state machine; billing + conversion on **delivered** | Live send monitor (Campanhas screen) |
| **`messages`** (webhook: inbound text) | Client replied on the salon's number | Match against opt-out lexicon (SAIR, PARE, PARA, CANCELAR, NÃO QUERO, REMOVER, DESCADASTRAR, ME TIRA + profanity) → suppression path 3; otherwise no platform action (humans reply in the salon app) | Suppression events only |
| **`user_preferences`** | Recipient stop/resume for `marketing_messages` | Persist append-only; stop → **global** suppression (path 1; business_id NULL, see §8); resume → release path-1 suppression only | Supressão center log |
| **`history`** | The 24-hour one-shot history sync (6 months, 3 phases) | Ingest to vault; watchdog: no phase-1 within 1h → alert; incomplete at 24h → offboard/re-onboard procedure (§11.2.3) | **Yes** on watchdog trip: "Sync de histórico incompleto — reagendar onboarding" |
| **`smb_message_echoes`** | Echo of messages the salon sent from its own app | Update per-client thread timeline; heartbeat activity proxy ONLY — **never the frequency ledger** (marketing template sends only, gate check C8) | None |
| **`smb_app_state_sync`** | App state/contact sync from the salon's phone | Persist; heartbeat activity proxy | None |
| **`account_update`: PARTNER_REMOVED** (`COMPANION_INACTIVITY` / `PRIMARY_INACTIVITY`) | Coexistence integration killed — 13-day rule breached or salon disconnected in app Settings | Number offline; halt everything for the salon; recovery = full re-onboard incl. fresh history sync | **Yes — sev-1**: "Integração do [salão] caiu — reonboarding necessário" |
| **`account_update`** (ban/restriction subtypes) | WABA/number restriction or ban event | Halt sends; persist event | **Yes — sev-1** |
| Template category change events | Meta recategorized / re-reviewed a template (`allow_category_change` era; utility→marketing with ≤1 day notice) | Persist; if a MARKETING template is paused by re-review, treat as 132015 flow; 60-day appeal window | **Yes**: category/status drift on any active template |

**[OPEN] items carried by this section** (also in §23 register): Meta's official BRL rate-card figures (download CSV before quoting externally); utility BR rate conflict ($0.0068 vs $0.0080); current ES v4 coexistence featureType string (`whatsapp_business_app_onboarding` vs stale `coexistence` extras); ES v4 token-exchange endpoint/params (§11.2.2); Meta API payload shapes for template create/send (verify against current Graph API docs at M4, §11.3); ~4-coexistence-WABAs-per-portfolio limit (Infobip-only source); ≥3-months number-age gate exact Meta wording (Gupshup-sourced); heartbeat activity-signal source (§11.5.2, ASSUMPTION); quality auto-demotion removal (Oct 2025, unverified); MM API availability on coexistence numbers (later upgrade path only, see §7); Dualhook bulk-send capability and Chatwoot history-sync/campaign-send (contingency-only, §11.7).


### ASAAS HALF — EVENTS, ERRORS, AND WHAT THE SYSTEM DOES


Exact event-name strings for the generic payment lifecycle must be confirmed against Asaas' webhook documentation during the Week-1 sandbox test (§12.3); the semantics and required actions below are locked.

| Event / signal | Meaning | System action | Founder alert |
|---|---|---|---|
| Payment created (webhook) | Charge exists, unpaid | Store raw event; resolve the charge row via `externalReference` (`charge:{charge_uuid}`) — campaign/client linkage lives in the charge's local columns | None |
| Payment received/settled (Pix) | Consumer paid; split executing | Mark settled; split-ledger row; issue voucher; salon notification; credit-ledger drawdown if applicable (§12.7) | Painel "dinheiro do mês" tick |
| Payment refunded (full) | Full reversal; split auto-reversed | Assert `refundedSplits[].done=true` and split `REFUNDED`; ledger reversal row; voucher → refunded; credit restore if drawdown (§12.7) | Info-level |
| Partial refund executed | Root `value` returned; `splitRefunds` clawed back | Ledger reversal rows; voucher → `refunded_partial` (sessions reduced, voucher continues — §8.7) | Info-level |
| Split `PENDING` → `AWAITING_CREDIT` → `DONE` | Normal fee flow | Recognize fee revenue only at `DONE` | None |
| Split `REFUSED`, refusalReason `RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT` | Salon pledged its receivables (antecipação); fee will not arrive via split | Billing fallback: add fee to NFS-e queue + Pix cobrança to the salon (§12.5); 2nd occurrence pauses new campaigns for that salon | **High** — immediate |
| Split cancelled, reason `WALLET_UNABLE_TO_RECEIVE` | Founder account KYC incomplete/restricted | Halt new charge creation platform-wide until founder account green | **Critical** |
| `PAYMENT_SPLIT_DIVERGENCE_BLOCK` | Split vs net divergence; funds blocked 2 business days | Re-read `GET /v3/myAccount/fees`; recompute; hold ledger row as blocked | **High** |
| `PAYMENT_SPLIT_FEE` | **[OPEN]** — in the webhook enum, undocumented; written definition pending from Asaas commercial | Log + hold the affected charge's ledger row | **High** until defined |
| `ACCOUNT_STATUS_*` | Salon onboarding/KYC progress (Pix key needs 100% approval + prova de vida) | Update Salão detail onboarding checklist (§15/§17) | Onboarding board |
| Transfer-authorization webhook | A transfer was initiated with the stored key | Verify it was founder-initiated and expected; otherwise treat as key compromise: revoke key, rotate, notify owner | **Critical if unexpected** |
| HTTP 400 on refund of fresh charge | Salon balance can't cover reversal (Asaas fees not returned) | Show exact shortfall; instruct salon top-up; retry after (§12.4) | Actionable — refund SLA clock keeps running |
| 400/403 on charge creation with unlinked-wallet split | The go/no-go failure case | NO-GO → Efí fallback path (§12.3) | Gate #1 result |
| Payment update response missing `splits` | The `splits: []` silent-disable fired (or a bug stripped it) | Guard blocks settlement processing; re-attach or cancel charge | **High** |
| Negative-balance behavior on reversal after withdrawal | **[OPEN]** — untested (§12.3 step 8) | Until answered: founder holds a 7-day-trailing-splits buffer | Policy, not event |

WhatsApp/Meta events and error codes (131049, 131050, 132015, 131048, 131026, `held_for_quality_assessment`, `user_preferences`, `account_update`) are the other half of this appendix — see the WhatsApp half.


## Appendix C. Legal Artifacts

All five artifacts below are outlines to be drafted by the founder (with Claude Code) and **signed off by the lawyer in week 1** (single engagement, scope per §24). None is used with a real salon before sign-off. All executed versions live in the records vault (§16) with version history and e-sign status. E-sign at launch is in-app click-to-sign with logged evidence (name, timestamp, IP hash) — **[ASSUMED]** sufficient for these B2B documents; the lawyer confirms (§23 register).

### C.1 LIA template (per salon; the salon's document)

**Status: for lawyer sign-off, week 1 — engagement items #1 and #2.**

1. **Identification** — salon (controller), Caixa Cheia (operator), DPO/contact point, document version and date.
2. **Processing description** — data categories (allowlist fields only, enumerated), sources (named export/report per system), volume, retention, the fail-closed eligibility gate (preconditions P1–P4, per-client checks C1–C9, approval artifact — §5.1.2) summarized as controls.
3. **Legitimacy test** — the concrete interest (promotion of the salon's own services to its own clients, Art. 10º I/II); the three anchors (ANPD LI Guide Ex. 5; NT 2/2024 §5.55 a contrario; DPB C.7.1.1) stated as supporting sources.
4. **Necessity test** — minimization evidence: allowlist importer, dropped-columns log, no service/clinical data, mathematical triggers only, cadence at business level.
5. **Balancing test** — legítimas expectativas (prior relationship, cadence tier, 12-month ceiling); intrusion assessment (one message per 60 days, business hours, known number, free exit); **honest counterweights stated**: NT 2/2024 §5.32 consent-preference language, no Recital-47 equivalent, consent-first market posture.
6. **Safeguards** — in-message opt-out, authoritative suppression, state-registry screening (recipient UF attributed by phone DDD→UF mapping — imprecision acknowledged here), per-send owner approval, dual-track consent conversion, Art. 18 rights channel.
7. **Outcome and adoption** — controller's conclusion; owner signature block; owner attestations referenced with their versions (adult client base — gate check C7; no packages sold, where applicable — gate check C4); review triggers (new campaign type, new data field, regulatory change).
8. **Laser annex** (aesthetics/laser clinics only — lawyer item #1):
   - The Option B analysis in full: Art. 11 closed list / no LI; §1 two cumulative limbs and why "reveals" fails structurally; §4 sharing prohibition and why the pipeline never triggers it;
   - The **client-status question**: the reasoned position that "is a client of this clinic" alone is ordinary data, with the flagged absence of ANPD beauty-sector guidance and the 2026–27 health-data priority **[OPEN]**;
   - Pipeline attestations: dropped-field list for this clinic's system, generic-copy rule, owner-authored offer content;
   - RaiaDrogasil distinguishment (no purchase-history content held, no profiling possible).

### C.2 DPA — clause list

**Status: for lawyer sign-off, week 1 — engagement item #3.**

1. Parties and roles (salon = controlador; Caixa Cheia = operadora).
2. Object, duration, nature and purpose of processing (campaign execution on the salon's instruction).
3. Data types and data-subject categories (allowlist enumerated; sensitive data expressly out of scope).
4. Documented instructions; per-send approval mechanism defined as the instruction of record; refusal duty for unlawful instructions.
5. Confidentiality; personnel access (founder only at start).
6. Security measures (encryption at rest, access-logged key vault, append-only audit tables).
7. Suboperators, disclosed and authorized: Meta/WhatsApp (transport), cloud host, Asaas (payment-processing context); change-notice mechanism.
8. Data-subject rights assistance (Art. 18 requests routed to the controller; suppression executed by operator).
9. Breach notification (to controller, with timeline).
10. Prohibition on own-purpose processing and cross-salon use (mirrors constitution #10).
11. Return/deletion at termination; retention of legally required records (approval artifacts, redemption ledger).
12. Liability allocation referencing Art. 42; audit/evidence cooperation (Art. 42 §2).

### C.3 Service contract — the tax-critical clauses

**Status: for lawyer + contador sign-off, week 1 — lawyer item #3, contador item #2.** These clauses carry the tax architecture (see §20); the split alone does not.

1. **"Em nome e por conta do salão"** — Caixa Cheia acts in the salon's name and on its account; conta-alheia characterization (LC 123 art. 3º §1º).
2. **Percentage commission** — remuneration is 20% of settled net value of resulting sales, success-only; no fixed component.
3. **Mandate-to-split** — express mandate authorizing the PSP (Asaas) to credit Caixa Cheia's share directly at settlement, discharging the salon's payment obligation pro tanto.
4. **Merchant of record = salon** — the salon is seller of record; its CNPJ on PSP registration, checkout, and receipts; consumer contracts with the salon.
5. **No consumer invoicing by Caixa Cheia** — the salon invoices the consumer for the full amount; Caixa Cheia issues NFS-e to the salon only, for the fee only (LC 116 item 10.02/10.09).
6. Supporting clauses: refund mechanics (salon-originated, split-reversed), audit-credit terms (constitution #3), campaign-approval process, DPA incorporation by reference, term/termination, API-key custody and revocation.

### C.4 Consent record — schema

**Status: for lawyer sign-off, week 1 (validates Art. 8 evidentiary sufficiency).** This reproduces the canonical `consents` table (§8.3); §8.3 is authoritative if the two ever diverge.

```
consents {
  id                uuid
  business_id       uuid NOT NULL   -- the controller (salon)
  client_id         uuid NULL       -- nullable: QR captures may precede import; linked later by phone
  phone_e164        text NOT NULL   -- the phone number as stated by the client
  value             enum: granted | refused | revoked
  source            enum: qr_card | offer_page | checkout | fresha_import | observacao_marker | manual
  evidence_class    enum: native_capture | imported_boolean | marker
  displayed_text    text            -- exact string shown, verbatim; NOT NULL for native_capture, NULL allowed for imports
  text_version      text            -- locked-copy version id; NOT NULL for native_capture
  notice_version    uuid            -- references notices(id) (§8.3); version shown at capture
  scope             text            -- fixed 'whatsapp_marketing' at launch; the gate does not key on scope
  staff_identifier  text NULL
  ip_hash           text NULL
  captured_at       timestamptz     -- America/Sao_Paulo
}
-- Append-only. Refusals (value=refused) stored, never overwritten.
-- Revocation (SAIR / webhook stop / 131050 / block) appends a value=revoked row
--   AND writes a suppression-list entry (authoritative, §11).
-- Fresha "Accepts marketing": TRUE → granted / imported_boolean;
--   FALSE → refused record (Branch-A exclusion) — never a suppression entry.
```

### C.5 Offer-page mandatory disclosures — checklist

**Status: for lawyer sign-off, week 1 — engagement item #4 (TJDFT 2110685 clause).** The page cannot publish with any item missing (enforced in the builder, see §13).

- [ ] Package price (R$, centavos).
- [ ] Number of sessions included.
- [ ] Validity period, prominently displayed before purchase.
- [ ] Avulso (single-session) price.
- [ ] Exact cancellation arithmetic, worked as a formula: refund = amount paid − (sessions used × avulso price) − pre-disclosed admin fee, if any.
- [ ] Art. 49 notice: 7-day withdrawal, full refund, exercised through the same channel (Decreto 7.962/2013 art. 5).
- [ ] Selling salon's legal name and **CNPJ** (CDC art. 42-A).
- [ ] Voucher redemption terms: issuing salon/group only (constitution #16).
- [ ] Privacy-notice link; consent checkbox (locked text, C.4 capture) — **unticked, and never a condition of purchase or price**.
- [ ] "Tecnologia Caixa Cheia" footer only — no founder branding above it (constitution #14).


## APPENDIX D — SOURCES & VERIFICATION REGISTER

The load-bearing external facts a lawyer, accountant, or builder would need to re-check, with pointers as given in this document. "Verified" = confirmed against the named source; **[OPEN]** = flagged in §23.3.

| Fact | Source pointer | Status |
|---|---|---|
| **Market** | | |
| 1,661 salons with 20+ employees (CNAE 9602-5/01) | Public CNPJ/CNAE data; vintage likely 2017–2020 | Verified, stale — re-pull before external use **[OPEN #20]** |
| 1,672 beauty EPPs formalized in 2025; 94% of new beauty businesses are MEI | Public formalization statistics (see §2) | Verified |
| Beauty Fair 2026: 5–8 Sept, Expo Center Norte; free professional badge; R$50 tier until 31/07 | Beauty Fair official registration site | Verified |
| Salon economics: ticket médio R$185; commission 35–50%; net margin 10–18% | Sector benchmarks compiled in §2 | Verified (benchmark-grade) |
| Named groups/franchisors and unit counts (Fast Escova 300+, Jacques Janine 50, Espaçolaser 808, etc.) | Brand unit-locator pages; Trinks "Redes e Franquias" references | Verified at pull time; recount before citing externally |
| Zero BR players selling salon win-back on success fee | Negative search across ~35 PT queries | Verified negative (inherently rebuttable) |
| **Systems** | | |
| Trinks: self-serve Excel exports; "não retornaram" report capped at 1 year; API partner-gated, no package/visit endpoints | Trinks help docs + trial | Verified; column details **[OPEN #1–3]** |
| Avec: 278 reports, Print/Excel/PDF on every report; live REST API `api.avec.beauty` `GET /reports/{code}`; spec at doc.api.avec.beauty | Avec docs; API verified reachable (401 clean) | Verified; exact columns **[OPEN #5]** |
| AppBarber: Excel button on reports; "Retorno por Período" gives Último Agendamento | Vendor help-center screenshots | Verified (visual); package-export button **[OPEN #28]** |
| Belasis: all reports exportable (v5.2.13); API `api.belasis.com.br` /clients, /schedule_groups | Belasis release notes + API docs | Verified |
| Fresha: "Accepts marketing" / "Accepts SMS marketing" boolean export columns; no package export | Fresha export docs | Verified; CPC 47 on Fresha unproven **[OPEN #29]** |
| Gendo: export capped at 5,000 rows (silent truncation) | Gendo UI page-size selector | Verified |
| Booksy: no self-service export; directory enumerable by numeric city IDs | Booksy support docs + directory URLs | Verified |
| Consent stored as URL/attachment in Observação, not structured | Belle Software LGPD guide | Verified (industry-norm grade) |
| **Meta / WhatsApp** | | |
| BR marketing ≈ $0.0625/msg, per-message on delivery since 07/2025 | Third-party ×3; Meta CSV rate card is the authority | Corroborated — download rate card **[OPEN #6]** |
| Tech Provider path free; classic Business Verification (no PLBV); App Review two demo videos; ~3–6 weeks | Meta developer docs | Verified |
| Embedded Signup v4 (v2 dead 15/10/2026); coexistence featureType | Meta ES docs | Verified; featureType string **[OPEN #9]**; token-exchange endpoint **[OPEN #26]** |
| Coexistence: 6-month history sync in 24h one-shot; app open every 13 days; 20 mps; one number per coex WABA; one-way door | Meta docs (+ Gupshup for the 3-month number-age gate) | Verified; exact number-age rule **[OPEN #25]**; activity-signal source **[OPEN #27]** |
| Messaging limits 250→2k→10k→100k→unlimited, per portfolio, rolling 24h | Meta docs | Verified |
| Per-user marketing cap global, BR in scope; error 131049 never retried; 131050 permanent; `user_preferences` webhook | Meta docs / error reference | Verified |
| Template mechanics (pt_BR code; no $/% in variables; ≤2 URL buttons; 1 URL variable at end; wa.me rejected) | Meta template docs (+ Twilio for wa.me) | Verified |
| BRL mandate: WABAs in BRL from 07/2026; non-BRL delivery stops 01/07/2027 | Meta billing announcement | Verified |
| MM API on coexistence numbers | Third-party only; Meta silent | **[OPEN #8]** |
| **Asaas** | | |
| Split to unrelated third party via `walletId` + `percentualValue`; Asaas' own 20% example | Asaas split docs (canonical example) | Verified in docs; production behavior **[OPEN #12 — Gate 1]** |
| Split computes on netValue (R$900 → R$179.60 at R$1.99 fee); fees live via GET /v3/myAccount/fees | Asaas API docs | Verified |
| Full refund auto-reverses split; partial requires `splitRefunds`; refund may 400 (fees not returned) | Asaas refund docs | Verified; post-withdrawal reversal **[OPEN #13]** |
| Pledged receivables → split REFUSED (`RECEIVABLE_UNIT_AFFECTED_BY_EXTERNAL_CONTRACTUAL_EFFECT`); no OAuth (full API key custody) | Asaas docs | Verified |
| `PAYMENT_SPLIT_FEE` webhook enum | Enum present, undocumented | **[OPEN #14]** |
| **Legal** | | |
| LI basis: LGPD Art. 7º IX + 10º; ANPD LI Guide Example 5; NT 2/2024 §5.55; DPB C.7.1.1 (12-month window) | ANPD guides / NT 2/2024 | Verified |
| Operator posture: ANPD Guia de Agentes Example 5; Art. 42 §1 I solidary liability | ANPD Guia de Agentes; LGPD text | Verified |
| Art. 11: no LI for sensitive data; §4 bars health-data sharing for economic advantage | LGPD text + ANPD position | Verified; laser client-status question **[OPEN #16]** |
| SP registry reaches WhatsApp; Q17 bars ALL promotional content to registered numbers, no existing-customer exception | Lei 17.832/2023 arts. 127–129 + 17.334/2021; PROCON-SP FAQ | Verified; supplier list access **[OPEN #15]** |
| PR/GO/SC/DF/RS registries cover messages; damages pattern R$1,500–6,000 after ignored stop | State laws cited in §5; TJDFT Ac. 2005290; TJPR RI 0006880-13 | Verified |
| CDC art. 49 (7-day withdrawal, link sale = fora do estabelecimento); Decreto 7.962/2013 art. 5; cancellation math per TJDFT Acórdão 2110685 (15/04/2026) | Statute + case law as cited | Verified |
| CDC art. 42-A: salon CNPJ on checkout/receipts | CDC text | Verified |
| **Tax** | | |
| Receita bruta = 20% only (conta alheia) | LC 123 art. 3º §1º; SC Cosit 159/2020 analogue | Verified — contador confirms structure (C item 2) |
| Salon's receita = full R$900; commission not deductible | SC Cosit 143/2021; SC Disit 5007/2025; SC Cosit 94/2025; CTN art. 123 | Verified |
| Fator R (28% pró-labore → Anexo III); escrituração completa dividend rule (LC 123 art. 14 §1º/§2º) | LC 123 + Simples rules | Verified |
| Dividends: 10% IRRF only >R$50k/CNPJ/person/month (2026) | Lei 15.270/2025 | Verified |
| ISS at her municipality; item 10.02/10.09, never 1.05/1.09; no salon withholding | LC 116; LC 123 art. 21 §4 | Verified |
| Microentidade revenue language (no CPC 47 liability claim) | NBC TG 1002 item 23.7 | Verified |
| LC 214/2025 fiscal split payment from 2027+ | LC 214/2025 | Verified — contador forward-models (C item 5) |
