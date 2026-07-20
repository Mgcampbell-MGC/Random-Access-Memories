# RUN PROGRESS — Rental Equipment Play Evaluation

Goal: Pick ONE rental-equipment business (asset-owner, near-passive, huge KISS cash flow, forced demand, defensible niche) and deliver a clear Word doc to execute it.

## Status
- [x] Read & extract all 9 source `.docx` plays
- [x] Pre-filter (kill on-sight plays that fail a hard filter — no tokens wasted verifying them)
- [x] **Phase 1** — Analyst + Red-Team + Score the 6 contenders (18 agents, done). Result: 5 of 6 KILLED; only SilicaShield survives at 4.15/10. Raw: `scratchpad/phase1_clean.json`.
- [x] Write Phase 1 kill list (verification kills recorded in 02_KILL_LIST.md)
- [~] **Phase 2** — Prospector fleet → pre-filter → same treatment on net-new plays  ← RUNNING (workflow wf_15566e0e-250)
- [ ] **Phase 3 — Final Kill Gauntlet** (armed: `scratchpad/wf_phase3_gauntlet.js`). Fires on Phase-2 survivors + SilicaShield. 6 assassins/finalist: market-death, obsolescence, PE roll-up, rent-vs-own, passivity-trap, resale-cliff → DEAD/FRAGILE/FUNDABLE. No hype; kill first.
- [ ] Write all 5 markdown deliverables in ./output/
- [ ] Produce the final execution Word doc for the #1 pick
- [ ] Commit & push to branch `claude/rental-equipment-evaluation-s9xphh`

## Phase 1 scorecard (existing 9 → 6 verified)
| Play | Verdict | Weighted | Honest CoC | Net/unit/yr |
|---|---|---|---|---|
| SilicaShield | SURVIVE | 4.15 | 55% | $15,500 |
| Aquifer-as-a-Service | KILL | 2.85 | ~50%* | $99,000 |
| SpurSafe/QuickRack | KILL | 2.75 | 23% | $7,500 |
| ConcreteWash | KILL | 2.55 | 15% | $2,000 |
| ColdBox | KILL | 2.00 | −61% | −$3,303 |
| RailWatch Virtual Gate | KILL | 1.90 | 10% | $3,000 |

Bar for Phase 2 to beat: **4.15**. Kill patterns now hard pre-filters: invented rates, rent-vs-own, dispatch-route/secret-job, commodity/Tier-1, toothless demand.

## User preference — AI edge layer (secondary, applied AFTER niche is chosen)
Niche selection stays on merit (forced demand + passivity + moat + cash flow). THEN, on the winning pick(s), add an explicit "AI / Agent Edge" layer in the deep-dive + Word doc: AI compliance-doc agent (software moat, automated), AI dispatch/ops agent (makes "no 2am phone" literal → kills the dispatch-route failure mode), AI outbound/lead-gen, predictive-maintenance/telemetry anomaly detection, AI billing/collections/support. Flag per pick whether AI is a real moat or cosmetic. Do NOT let "must have AI" drive niche choice.

## Pre-filter decisions (on-sight kills — see 02_KILL_LIST.md)
- Rail Tank-Car Heat/Steam Pedestals — KILL: buys a job (owner runs crew + dispatch board; $360k/yr staffing).
- Specialized Industrial Services (transformer oil, MV cable, SF6, helium) — KILL: owner = the technician; not passive, not rental.
- Specialty Trade Tools rental — KILL: sub-scale cash flow, commodity, no moat.
- Environmental-Control rental — KILL: rents the same gear as Sunbelt/UR with no structural edge; demand is overflow nice-to-have.

## 6 contenders sent to full verification
ConcreteWash · SilicaShield · ColdBox · Aquifer-as-a-Service · SpurSafe · RailWatch Virtual Gate
