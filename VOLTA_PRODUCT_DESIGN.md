# VOLTA — Product & System Design

**Managed financial recovery for professional Mercado Livre Full sellers in Brazil**

*Design dossier · answers two questions: **how would you build this**, and **what does "hell yes" look like** · success-fee only · read-only OAuth · LGPD / sa-east-1*

> **Promessa:** *"Encontramos valores elegíveis que não voltaram para a sua operação, montamos a prova e acompanhamos o caso até o crédito. Você só paga sobre o que efetivamente receber."*

> **Visual companion:** an interactive one-page overview of everything below (workbench mock, architecture, engine, economics, roadmap, risks) is published as a Claude artifact. This document is the written system of record.

---

## 1. The Product in One Paragraph

VOLTA is the **system of record for what Mercado Livre owes you — and the machine that collects it.** It connects, read-only, to a seller's Mercado Livre and Mercado Pago accounts, reconciles operational events (Full inventory movements, inbound receiving, orders, returns, claims) against financial movements (Mercado Pago releases, credits, fees), and surfaces the money the seller is owed but never received: damaged or lost Full stock, inbound quantity shortfalls, returns never restocked, claims about to expire, approved credits that never posted, and duplicate deductions. A **deterministic engine computes every centavo in code**; an **LLM ("Work") drafts the Portuguese, reads the invoices, and summarizes the replies but never invents a number**; and **a human approves every external action.** The seller pays only when a VOLTA-managed case results in a confirmed credit that actually lands in their financial records. This is the Amazon FBA reimbursement-recovery playbook — a mature, proven US industry — brought to Mercado Livre, plus a second recoverable pool (Mercado Pago payments) that the FBA tools don't have.

---

## 2. The Thesis — Build the Workbench, Not the Chatbot

The founder's instinct is correct, and the reason is precise: **running this business out of a raw ChatGPT/Claude chat is too weak because a chat has no memory, no webhooks, no evidence graph, and no audit log — it resets every session.** That makes the LLM a rentable commodity. The durable asset — the moat — is the **workbench**:

- **A deterministic reconciliation engine.** Rules compute *expected credit − matched credit = unresolved difference*, joined across Mercado Livre's data streams on `inventory_id`, `shipment_id`, `claim_id`, and NF-e line items.
- **An append-only case-and-evidence system of record.** Every case is a first-class object; every figure is traceable to a raw event and a rule-version.
- **An accumulating, cross-seller library of which case types Mercado Livre actually pays.** This compounds with scale — every confirmed credit teaches the library, so *confirmed credits per human operating hour rises as VOLTA grows.*

**The one hard rule the whole business hangs on:** *Code computes every centavo; the LLM computes none.* Money, quantities, deadlines, and fees are calculated in deterministic code and stored as integer `centavos`. This is what makes a zero-downside, success-fee promise defensible in an adversarial, money-moving process.

**The single most important architectural decision:** an **append-only, hash-chained event spine** as the system of record. Success fees are contestable — a seller or Mercado Livre can dispute any figure — so VOLTA must be able to replay, on demand, exactly *which raw payload* and *which rule-version* produced any BRL amount, who approved it, and when. This one decision simultaneously delivers the audit log, the LGPD accountability record, and the dispute-defense asset. Everything else follows from it.

---

## 3. Why Now — The Proven Analog

Marketplace reimbursement-recovery is a mature US industry. The "no downside" structure — *we only get paid when you get paid* — is why it converts.

| Player (US / FBA) | Model | Fee | Proof point |
|---|---|---|---|
| **GETIDA** (category leader) | Automated audit + human case managers; SP-API OAuth | 25%; first $400 free; enterprise 10–18% | $1B+ recovered, ~90% win rate |
| **Seller Investigators** | Human-led weekly review | 25%; no setup fee | ~95.9% success |
| **Refully** | Automated + dashboard | 18%; first $1,000 free | Software-first |

Pricing converges on **15–25% pure success fee, no monthly minimum, no upfront.** Typically **~1–3% of FBA revenue** is recoverable — meaningful pure margin.

**Timing tailwind:** since Oct 2024 Amazon cut its claim window from 18 months to 60 days, auto-reimburses more, and (Mar 2025) pays lost/damaged inventory at *manufacturing cost, not sale price*. This *raises* the value of a fast, always-on detector that catches tight windows and audits whether the platform's auto-reimbursement was actually correct. Software wins; manual-only players get squeezed.

**Translation to Mercado Livre + Mercado Pago:**

- **The Full layer (the FBA analog):** lost / damaged / *extravio* inventory, inbound receiving shortfalls, returns never restocked, wrong-dimension (cubagem) fee overcharges. Mercado Livre runs a *compensação por atraso / extravio / avaria* program — but, exactly as with Amazon, sellers under-claim and never audit whether the payout was correct or complete.
- **The Mercado Pago layer (VOLTA's edge, no Amazon equivalent):** chargebacks wrongly debited, MDR / commission overcharges, mediation reversals, tarifa discrepancies, held funds. A *second* recoverable pool.

**The category-defining move:** one OAuth to ML + Mercado Pago → automated reconciliation across **both logistics and payments** → an instant free audit surfacing a hard BRL number → success fee → files within tight claim windows → a live *dinheiro recuperado* ledger. Brazil has no credible automated player today. The first one can define the category.

> ⚠️ **The 1–3% figure is transplanted from US Amazon data and is unverified for Mercado Livre.** It is the single assumption the 45-day pilot exists to test (see §15).

---

## 4. The Product & the Five "Hell Yes" Moments

| # | Moment | What it is |
|---|---|---|
| 1 | **The Number** | An instant free audit surfaces a concrete recoverable BRL figure and case count — quantified before the seller pays a single real. |
| 2 | **The Receipt** | Click any case and see the *proof*: the ledger movement flagged "danificado," the NF-e XML quantity, and the missing credit line, side by side. Provable, never vibes. |
| 3 | **The Deadline Radar** | `CLAIM_ACTION_DEADLINE` catches claims "aguardando ação do vendedor" before Mercado Livre auto-closes them in its own favor. Money otherwise lost to silence. |
| 4 | **One-Tap Approval** | A human approves the basis and submission; VOLTA assembles the evidence, drafts the explanation, coordinates the action. Case-prep trending toward two minutes. |
| 5 | **Dinheiro Recuperado** | A live ticker of confirmed credits landing in the seller's account. Watching R$0 climb to R$47.000 is the retention engine. |

**Product line:** (A) **Historical Recovery Audit** — a 90–180 day retrospective that *starts* the engagement, not a report; (B) **Managed Recovery** — evidence, submission, monitoring, reconciliation, invoice-on-confirmed-credit; (C) **Continuous Protection** — always-on ingestion, detection, deadline monitoring, monthly statements (R$1.490/mo + 15%); (D) **White-Label Partner Service** — VOLTA runs the recovery rail behind agencies, ERPs, accountants, and 3PLs.

---

## 5. The End-to-End Loop

1. **Connect** — seller authorizes read-only OAuth to ML + Mercado Pago on one `/connect` screen. No passwords shared; one-click revoke.
2. **Audit** — a background worker backfills 90–180 days in ≤15-day windows; the engine reconciles logistics *and* payments.
3. **The Number** — the seller sees a hard recoverable BRL figure and case count. *Você só paga sobre o que voltar.*
4. **Triage** — the operator opens not a dashboard but a queue sorted by **PRV** (value × confidence × deadline-urgency).
5. **Decide** — the Case Detail Cockpit shows the money math as a code-computed *Esperado vs Recebido* diff, an AI-built evidence checklist, and an AI-drafted PT explanation. Read, judge, act in under 20 minutes (target sub-5).
6. **Approve** — a named human confirms eligibility and monetary basis. Nothing leaves the building without this.
7. **Submit** — VOLTA executes the permitted API action (evidence, messaging) or generates a copy-paste dashboard packet where ML exposes no endpoint.
8. **Monitor** — a deadline board tracks the case through *Em análise ML*; anything expiring in 72h escalates.
9. **Reconcile & bill** — when the credit posts in the Mercado Pago report (after `baseline_date`, excluding pre-existing credits), the Fee Ledger matches it, computes the fee, and drafts the NFS-e. Fee only on confirmed, recorded credit.

---

## 6. The Operator Workbench

The workbench is where the north star is won or lost. **The operator decides; they never assemble.** Every case arrives pre-reconciled, pre-drafted, pre-scored. Keyboard-first, single-column, command-driven (`J/K` move, `Enter` opens, `A` approve, `R` reject, `D` request-docs, `S` escalate), every action batchable and reversible for 30s.

**The single most important screen — the Case Detail Cockpit** — is five stacked panels, no tabs, no scrolling for the decision:

1. **Header strip** — case ID, seller, `case_type`, PRV score, deadline countdown (red if ≤7d), confidence badge.
2. **The money math as a ledger diff** — two columns, *Esperado vs Recebido*, join key highlighted: "Declarado: 200 un × R$ 47,90 · Recebido no check-in: 188 un · **Valor não creditado: R$ 574,80**." Every number is code-computed and carries hover-provenance to its source event and rule-version. The LLM never touches this figure.
3. **Evidence panel** — an AI-built checklist: NF-e XML ✓ (parsed `<det>` qty auto-matched to the shortfall), packing list ✓, POD ✗. Red items block submission; one click fires the templated PT document request.
4. **AI-drafted explanation** — the administrative *explicação* in plain Portuguese, editable inline, watermarked "gerado por Work · números do motor de regras."
5. **Action bar** — Aprovar / Rejeitar / Pedir documento / Escalar, each logging an immutable approval record. Approve advances to the submission gate; it does not itself fire anything external.

**The other surfaces:** Triage Queue (dense, virtualized, PRV-sorted, bulk actions), Approval + Submission console (the human gate; shows exactly which API action executes or emits a dashboard packet), Monitoring / Deadline board (kanban with the deadline swimlane pinned), Credit reconciliation + fee invoicing, Seller portal, and the re-skinned White-Label Partner portal.

**North-star instrumentation:** every screen surfaces *confirmed credits per operating hour*; a live timer runs per case; cases where prep exceeds 20 min are auto-flagged for rule-tuning. The workbench polices its own efficiency.

---

## 7. System Architecture

VOLTA is a **modular monolith, not microservices**: one FastAPI (Python 3.12) deployable with clean internal modules (`ingest`, `normalize`, `reconcile`, `rules`, `cases`, `submit`, `billing`), plus **two isolated processes** — the webhook receiver and the AI service. Everything runs in AWS **sa-east-1 (São Paulo)** for LGPD residency.

**Data flow:** `ingest → normalize → reconcile → detect → case → review → approve → submit → monitor → reconcile credit → invoice`.

| Component | Function | Choice / why |
|---|---|---|
| API + business logic | Integrations, rules, workflow | **FastAPI** — one deployable, no distributed-systems tax for a small team |
| System of record + event store | Canonical state + append-only `case_events` | **PostgreSQL 16** — one store, Row-Level Security for tenant isolation |
| Object storage | Invoices / evidence / generated PDFs | **S3 (SSE-KMS)**, per-tenant prefix |
| Job queue | Imports, reconciliation, monitoring | **Redis + Dramatiq**, durable |
| Scheduler | Polling + deadline sweeps | **APScheduler** |
| Webhook receiver | Persist pointer, ACK <200ms | Isolated process; poller backfills missed notifications |
| AI service | Drafts only | **Isolated** — no DB write to money fields, no ML/MP network route |

**Key patterns:**
- **Event-sourced spine.** `case_events` is append-only and **hash-chained** (each row stores `prev_hash`). Current case state is a projection; nothing mutates a case except by appending an event. The audit log *is* this stream.
- **Idempotent ingestion.** Natural key `(seller_id, source, resource_type, resource_id, resource_version)` with `INSERT … ON CONFLICT DO NOTHING`. Because reconciliation is a deterministic function of canonical state, rules re-run any time without duplicate cases (candidate keyed by `(rule_id, join_key)`).
- **Tenant isolation is structural.** `tenant_id` on every row + Postgres RLS + per-request `SET app.tenant_id`. Per-tenant envelope encryption: a compromised key exposes exactly one seller.
- **Observability.** OpenTelemetry traces every case lifecycle; the 8 metrics are first-class gauges headlined by confirmed credits ÷ human minutes; a reconciliation-freshness SLO (lag < 6h) and a deadline-risk dashboard (claims expiring < 72h) guard against the biggest silent failure — a missed claim window.

---

## 8. The Deterministic Recovery Engine

The engine's contract: **code computes every centavo; the LLM computes none.** All money is integer `centavos` (BRL). Every candidate is a ledger row answering *expected credit − matched credit = unresolved difference*, stamped with the exact `rule_id@version` and `config_hash` that produced it. Thresholds, windows, and tolerances are **fields in `rule_defs`, not code** — a new rule or tuned window ships by inserting a versioned row, no redeploy.

| Rule | Reconciliation (join) | Amount formula | Deadline |
|---|---|---|---|
| `FULL_DAMAGE_NO_MATCHED_CREDIT` | stock op (damage, warehouse cause) × credit on `inventory_id+movement_id` | `qty × unit_ref` (greater of NF unit cost, sale price) | event + 180d |
| `NEGATIVE_STOCK_AUDIT_UNRESOLVED` | negative adjustment × sales × returns × credit on `sku` | `adj − (sales+returns+credits)` after cool-off | event + 60d |
| `INBOUND_QUANTITY_DIFFERENCE` | declared × check-in on `shipment_id+sku`, vs NF-e `<det>` qty | `delta × NF_unit` | receipt + 30d |
| `CLAIM_ACTION_DEADLINE` | claims search: `available_actions.expiration` | preventive (save an approvable claim) | expiry − now; escalate ≤48h |
| `RETURN_CONDITION_REVIEW` | returns × refunds × restock on `order_id/claim_id` | refunded but not restocked | return + 30d |
| `APPROVED_CREDIT_NOT_RECEIVED` | approved claims × MP/billing on `claim_id` | `approved − posted` | approval + 90d |
| `DUPLICATE_OR_UNMATCHED_DEDUCTION` | billing × orders × inventory on `order_id+fee_type` | `fee_centavos` | charge + 180d |

**High-value discrepancy types the 7 rules under-cover** (add as the pilot proves them): reimbursement valued *below actual price/cost* (often the biggest single leak); storage-fee overcharge on unsellable/damaged units; cubagem (weight/dimension) misclassification inflating every shipment's freight tier; commission charged on freight/taxes; lost-in-carrier where only the buyer was refunded; duplicate returns/refunds; removal/disposal without credit.

**False-positive control is existential** — a wrong case burns the trust the whole pitch rests on. Six gates, in order:
1. **Cool-off suppression** — hold N days so ML's own auto-credit can fire first.
2. **Value floor + dedup** — drop sub-floor cases; collapse duplicates on the join key.
3. **Known-benign patterns** — a seller-scoped suppression list of causes/fee-types that historically auto-resolve.
4. **Confidence tiers (A/B/C)** = f(rule confidence × evidence completeness). Only **Tier A** is eligible for pre-approved auto-submission.
5. **Evidence-completeness gate** — a required-artifact checklist per rule; a missing artifact caps confidence and blocks submission.
6. **Human-review threshold** — any case ≥ R$5,000, any C→B promotion, or FP-rate breach routes to mandatory review.

New rule-versions always launch in **shadow mode** (compute, log, don't surface) until precision clears the bar; a version that breaches its FP budget is auto-demoted. Every case forever records which version fired. **Fully-matched cases auto-close as `RESOLVED_BY_PLATFORM` at zero human minutes** — a direct north-star lever.

---

## 9. Data Model & Reconciliation Ledger

**Two layers, one law:** raw is append-only, canonical is derived, money is a ledger, and the LLM never writes a number. Every seller is a logical partition (`seller_id` + RLS). Money is always integer `*_cents` + `currency='BRL'`. In the trust path nothing is ever `UPDATE`-d — corrections are new rows.

- **Layer 1 — immutable ingestion.** `raw_event(id, seller_id, provider, topic, external_id, payload jsonb, payload_sha256, received_at, seq, prev_hash, row_hash)`. Every webhook/poll lands here verbatim and is hash-chained per seller. No computed figure is trusted unless it traces to a `raw_event.id`.
- **Layer 2 — canonical projections.** `inv_movement`, `order`, `shipment/inbound`, `claim`, `return`, `mp_movement` — each carrying `source_raw_event_id`.
- **The NF-e store.** The legal proof is the **XML, not the DANFE**: `nfe(chave_44, xml_object_key, sha256, kind, emit_at)` + `nfe_item(sku, ncm, qty, unit_value_cents, total_value_cents)`. Inbound `nfe_item.qty` is ground truth for `INBOUND_QUANTITY_DIFFERENCE`.
- **The Case** — first-class, mirroring the brief's record exactly (case_type, detection_rule, status, confidence, baseline_date, deadline_at, quantity, documented_value_cents, expected_treatment_cents, matched_credit_cents, unresolved_cents, llm_explanation_pt, human_approval_id), with `case_source` citing every supporting record and `evidence` doubling as the checklist. No `submission` row exists without an `authorization_id`.

**The reconciliation ledger (the money engine):** `ledger_entry(expected_cents, observed_credit_cents, residual_cents, match_status, rule_version)`, append-only; the latest row per `(case_id, sku)` is the current view. `credit_match` binds observed MP credits to expectations. **`residual_cents = expected − Σ matched` *is* the recoverable claim.** A pre-existing credit that already covers the expectation closes the case at zero residual — that is how VOLTA honors "no fee for value already paid." `credit_reconciliation` fires only when a real credit posts and is the *sole* trigger for `fee_invoice` — fee is arithmetic on `confirmed_credit_cents`.

---

## 10. AI Operating Layer & Guardrails

**AI proposes. Code computes. A human approves.** The `case_facts` table — populated only by the deterministic rules engine — is the single grounding source the LLM may reference.

| Task | Output | Hard guardrail |
|---|---|---|
| NF-e / PDF read | JSON of extracted qty/value → `extraction_candidates` | Code reconciles vs ledger; the *case number is always the ledger number*. NF-e itself is parsed **in code** from the XML `<det>`; AI touches only degraded PDFs/images. |
| Explanation draft | PT-BR administrative text with `{{token}}` slots | Code injects money/dates; the model emits no digits |
| Evidence checklist | Ordered doc list per case | Template-bounded to the rule's required set |
| Missing-info request | Client email/WhatsApp draft | Queued, human-sent |
| Response summary | 3-line status + suggested next action | Action must map to a real API `available_action` |
| Client / partner report | Monthly PT narrative | Figures from `fee_calculation`, read-only |

**"No math from the model" is enforced, not requested,** by two mechanisms: (1) **templating** — drafts have slots (`{{unresolved_amount}}`) that code fills from `case_facts`, so the model literally can't see itself write "R$14.320"; (2) a **numeric linter** — before any draft persists, a validator regex-scans for currency/qty/date literals outside the injected-token allowlist; any hit auto-rejects and regenerates, logged as a `numeric_leak`. Repeat leaks block a prompt version's promotion.

**Guardrail stack:** structured/tool-constrained outputs (Pydantic-validated); retrieval scoped to one case in one tenant, buyer IDs pseudonymized before the prompt; five human-in-the-loop gates (eligibility, monetary basis, submission, seller comms, closure); a golden-set eval (~50 cases/rule) in CI where **numeric-leak rate must be 0**; full `llm_runs` audit (prompt hash, model+version, I/O, edit diff, approval ID); zero-retention endpoints — **no seller/buyer data trains public models.**

**The safe agentic frontier:** auto-run extraction, checklist, drafting, and prioritization the moment a case enters the queue, so operators open an already-drafted case; then **pre-approved operating rules** — confidence-and-value-gated autonomy (e.g. for `CLAIM_ACTION_DEADLINE`, auto-send a *standard* evidence bundle when the case matches a template exactly, deadline < 48h, value < a seller-set ceiling, and the seller pre-authorized that rule class in writing). **Never autonomous:** setting the monetary basis, accepting/declining an ML resolution, opening a ressarcimento claim, or any seller communication above the ceiling.

---

## 11. Integrations & the Unsafe-Access Boundary

Read-only, idempotent, per-seller ingestion. One `/connect` screen runs two OAuth 2.0 Authorization-Code (PKCE) handshakes. Default scope is `read` + `offline_access` — **never `write` at onboarding.** `write` is a separate per-seller consent requested only when a Managed Recovery contract is signed, and every write still passes the approval console.

**Resources pulled:** Full inventory + the key detection surface `/marketplace/stock/fulfillment/operations/search` (movement ledger); orders/shipments; claims/returns (`available_actions`, `mandatory`, `expiration`); Mercado Pago Release ("Liberações") and Account-Money reports; seller-uploaded NF-e XML. **Backfill vs incremental** share one windowed worker (the stock endpoint caps at 15-day windows, so backfill is chunked and resumable via `sync_cursors`). **Webhooks are the trigger, polling is the safety net** — a 6h reconciliation sweep re-pulls near-deadline claims and detects missed notifications by comparing counts. Every external write carries an `X-Idempotency-Key`; retries use exponential backoff; `429 local_rate_limited` is honored with a per-seller token bucket under the ~1,500 req/min ceiling.

**The unsafe-access boundary — the crux of the business:**

- **API-executable after human approval** (`write` scope, approval-gated): claim messaging and evidence — `send_message_to_complainant`, `add_shipping_evidence`, `send_attachments`, `send_tracking_number`, `open_dispute`, `allow_return`.
- **Manual / administrative only** (VOLTA detects, quantifies, and prepares; a human files in the seller dashboard): accepting/declining ML claim resolutions, ML Full-inventory reimbursement filing, and final dispute adjudication.
- Mercado Pago's `POST /refunds` moves money *out* — **blocklisted, never used for recovery.**

**No action executes under a seller's identity without explicit authorization or a pre-approved operating rule.** (Confirm target sellers are **not Model 6** — those get 403 on claims/returns endpoints. Verify current MELI developer policy on programmatic/bulk claim submission before automating filing.)

---

## 12. Security, Compliance & Trust (LGPD)

**Trust is the product** — a seller is handing VOLTA a live pipe into the data about their money. Threat model, ranked: token theft; cross-tenant leakage; rogue/compromised operator; unauthorized action under a seller's identity; buyer-PII exposure; LLM prompt-injection via a malicious invoice or claim message.

- **OAuth token vault** — per-tenant envelope encryption (AES-256-GCM DEK wrapped by a KMS CMK in sa-east-1); a narrow `TokenBroker` behind mTLS is the only holder of `kms:Decrypt`. Access tokens ~6h; refresh rotates server-side; stolen ciphertext without KMS is inert.
- **Least-privilege + revocation** — `read` + `offline_access` only at onboarding; a red *"Revogar acesso"* calls ML/MP revocation, purges tokens, and pauses jobs within seconds. Auto-revoke on termination, suspected compromise, or 3 consecutive `invalid_grant`.
- **Per-tenant isolation** — Postgres RLS on every table, per-request `SET app.tenant_id`, per-tenant S3 prefix, proven by a cross-tenant fuzzer in CI.
- **PII minimization** — buyer names/CPF become `buyer_ref` (per-tenant HMAC) at ingestion; reports and every LLM prompt see only `buyer_ref`.
- **Immutable audit + approval trail** — append-only, hash-chained; simultaneously the LGPD accountability record and the dispute asset.
- **LGPD posture** — VOLTA is *controller* of its own CRM/billing data and *operador* when querying marketplace/buyer data on seller instruction (mandatory signed **DPA** per client). Legal basis: seller data → *execução de contrato*; incidental buyer data → *legítimo interesse* + documented LIA. Retention: 5-year fiscal minimum for NF-e/case records, then hard purge. **Cross-border:** since the 23-Aug-2025 grace period closed, any US LLM/cloud requires ANPD Cláusulas-Padrão (SCCs) — execute them or keep processing in-region. LLM calls run under a zero-retention / no-training agreement behind a PII-redaction gateway.

VOLTA performs **administrative** recovery support only — not legal representation (reserved to OAB lawyers), accounting opinions, or litigation. *All legal/tax points to be confirmed with Brazilian counsel and an accountant before launch.*

---

## 13. Economics, Pricing & Go-To-Market

| Tier | Price | When | Why |
|---|---|---|---|
| **Founding** | 25% success-only | First ~15 pilot sellers | Zero-downside; buys proof + testimonials |
| **Historical Audit** | 20–25% of confirmed | Standard entry | Higher % — manual, high-value lump |
| **Continuous Protection** | R$1.490/mo + 15% | Post-audit conversion | Base covers cost floor; low % as volume automates |
| **White-Label** | 8–14% net to VOLTA | Partner portfolios (50–500 sellers) | Partner owns the client; ~R$0 CAC |

**Gross margin is a pure function of human-minutes-per-case** (the north-star denominator): ~60 min/case at pilot (thin margin) → **<20 min** at the gate (~70%) → **<5 min** at "hell yes" (~85%+), where one operator clears ~100 cases/hr. **Unit economics per qualified seller (R$300k+/mo GMV):** historical audit lump R$15k–40k confirmed → R$3k–10k one-time fee; continuous run-rate R$3k–8k/mo recovered → **R$1.940–2.690/mo.**

**CAC by channel — and why white-label wins:** direct outbound R$2–4k/seller (slow, founder-bound); inbound content R$800–1,500; **white-label ~R$0/seller** — one ERP/accountant/3PL partner unlocks 50–500 pre-qualified sellers with warm trust and no per-seller sales cost. *The agency channel is the acquisition engine; direct is the demo reel that closes partners.*

**Dispute-proof attribution:** the Fee Ledger locks five fields at case creation — `baseline_date`, `pre_existing_matched_credit`, `submitted_amount`, `confirmed_credit`, `fee`. Fee fires only when the credit is observed in the MP report, after baseline, excluding pre-existing credits: **`fee = fee_pct × (confirmed_credit − pre_existing_matched_credit)`.**

**Owner target:** ~R$50k/mo income ≈ ~R$70–80k/mo revenue ≈ ~R$280–320k/mo confirmed recoveries (e.g. 15 sellers × R$20k, 20 × R$15k, or 30 × R$10k). *Targets, not forecasts — the pilot must establish whether the recovery values are real.*

---

## 14. Build Roadmap & Phasing

**Sequencing principle:** prove the economics by hand before writing a schema; let the first ~50 real cases decide which rules deserve code; automate ingestion and arithmetic, never accountability. Each phase ships only after the prior one moved the north star.

| Phase | Duration / cost | Goal | Build (thinnest) | Exit gate |
|---|---|---|---|---|
| **0 · Pilot** | 45d · R$15–25k | *Does the money exist?* | Throwaway OAuth scripts, 5 sellers, 2 rules in notebooks (`FULL_DAMAGE`, `INBOUND_QTY_DIFF`), a Google Sheet case store, Claude drafts, founder files manually | ≥3 signed · ≥10 submitted · ≥1 confirmed · same case types repeat across ≥3/5 · prep < 20 min |
| **1 · Thin Workbench** | ~60d · R$40–70k | *Beat the spreadsheet* | FastAPI + Postgres + object storage; the 2 proven rules; 4 screens (Queue, Case Detail/Reconciliation, Approval Gate, Audit Log) | credits/human-hour ~2× the pilot · 3+ paying clients · prep < 10 min |
| **2 · Continuous Protection** | ~90d · R$60–100k | *Always-on; catch the window* | Webhooks + job queue; deadline monitor (`CLAIM_ACTION_DEADLINE`); +2 rules; monthly statements; fee/NFS-e automation. Ships Product C | FP rate < 5% · deadline-miss ≈ 0 · 10+ clients · MRR covers ops |
| **3 · White-Label Platform** | ~120d · R$150k+ | *Scale through partners* | Multi-tenant partner portal + revenue-share reporting; remaining rules + high-value extras; heavier evidence automation | 2+ signed partners · partner-sourced recoveries exceed direct |

**Defer aggressively:** no web app in Phase 0; no webhooks/partner portal in Phase 1; no self-serve signup until partner demand proves it. **No rule enters code until real cases prove it recurs.**

---

## 15. Risks, Kill Criteria & the One Pilot Test

Three genuinely existential risks, all attacking the north star — *confirmed credits per human operating hour* — from a different side:

| Risk | L | Impact | Leading indicator | Kill / redesign trigger |
|---|---|---|---|---|
| **R3 · The "no-API-action" wall** | H | Existential | `human_minutes_per_case` rising with volume; north star flat | Avg prep stays > 20 min after 45d, or every account needs bespoke steps → **redesign to white-label** (partner files) or narrow to auto-fileable types |
| **R1 · Pool auto-resolves / ToS** | H | Existential | Per-rule `auto_resolve_rate`; ML developer-terms change-log | > 60% of a rule's candidates auto-resolve → **pivot** to auditing ML's *payout correctness* (below-cost delta) + the Mercado Pago pool. ToS bans programmatic claims → keep human-approved only |
| **R2 · False positives kill trust** | M-H | Existential | `false_positive_rate` on seller-visible cases | FP > 5% on surfaced cases → **halt seller-facing surfacing**, raise the confidence gate |
| R6 · Values too small at steady state | M-H | High | candidate value/seller/mo after backlog cleared | < 3/5 pilot sellers show meaningful opportunity → drop Continuous, keep Historical only |
| R7 · Goodwill / partner concentration | M | High | app-review status; top-partner % of credits | any partner > 30% of portfolio; app suspended → diversify + hold seller-level OAuth |
| R5 · LGPD / contingency legal | L-M | High | ANPD SCCs; OAB scope line | no ANPD SCCs with LLM vendor by processing start → keep processing in-region; never touch judicial representation |
| R4 · Attribution disputes | M | Med | disputed-invoice rate | > 10% invoices disputed → tighten baseline evidence |

**The single pilot test that decides everything (from the adversarial review):** across the 5 pilot sellers, run a **controlled A/B** — VOLTA submits half the qualifying cases and deliberately *holds* the other half. If submitted cases pay materially more, and faster, than the held (auto-resolving) ones — **and** average case-prep stays under 20 minutes as volume rises — the value is real, causally attributable, and leverageable. **If the held cases pay out on their own at similar rates, VOLTA is billing for Mercado Livre's own process and there is no business.** Everything else in the 45-day plan is secondary to that one test.

**Honest verdict:** the engineering is genuinely strong, but strong architecture around an unproven core is over-engineering, not a moat. The "Recovery OS / multi-marketplace / white-label rail" ladder is a fantasy until the first rung pays. **Do not build the platform until the A/B test proves the recovery is real, large, recurring, and causally VOLTA's.**

---

## 16. How I'd Build It — Recommendation

1. **Yes — build the system, not the chatbot.** The workbench (deterministic engine + append-only case/evidence ledger + operator console) is the moat; the LLM is an assistant that must never compute a number. That single invariant is what makes the success-fee model safe.
2. **But earn the right to build it.** Run Phase 0 first — scripts, sheets, and a human — on 5 real sellers, and treat the controlled A/B (§15) as the go/no-go. It costs ~R$15–25k and answers the only question that matters.
3. **The most important architectural decision is the append-only, hash-chained event spine.** Everything — audit, LGPD, dispute defense, replayability — follows from it. Get it right on day one of Phase 1.
4. **Reconcile both pools from one OAuth.** Mercado Livre Full *and* Mercado Pago. The payments layer is VOLTA's edge over the FBA analog and is the natural hedge if ML auto-resolution shrinks the logistics pool.
5. **Design for the north star, not for impressiveness.** Confirmed client credits per human operating hour is the one number. If it doesn't rise with volume after 45 days, redesign — don't push harder.

---

## Appendix — Platform Notes (verify before building the write path)

- **Full stock movements** — `GET /marketplace/stock/fulfillment/operations/search` is the key detection surface (filters `inventory_id`, `date_from/to`, `type`; 15-day default window). Push via `stock-fulfillment` topic.
- **Claims/returns** — `/post-purchase/v2/claims/search`; `available_actions` carry a `mandatory` flag and `expiration`. API actions are messaging + evidence only; **refund acceptance and final adjudication are dashboard-only.** Model-6 sellers 403 on these endpoints.
- **Mercado Pago reports** — Release ("Liberações") and Account-Money reports (config → create → poll → download; schedulable). `POST /v1/payments/{id}/refunds` requires `X-Idempotency-Key` — and is *blocklisted* for VOLTA (moves money out).
- **Auth** — OAuth 2.0 Authorization Code; access token ~6h; refresh rotates; scopes `read`/`write`/`offline_access`. Rate limit ~1,500 req/min per seller.
- **Legal/tax** — NF-e **XML** (not DANFE) is the legal evidence; 5-year retention. VOLTA's success fee is a taxable service (issue NFS-e). Contingency ("ad exitum") recovery is a lawful, established model in Brazil for administrative work.

*Sources include Mercado Livre / Mercado Pago developer documentation, ANPD Resolução CD/ANPD 19/2024, and public data on the Amazon FBA reimbursement-recovery industry (GETIDA, Seller Investigators, Refully). All platform, legal, and tax specifics to be verified with primary sources and Brazilian counsel before launch.*
