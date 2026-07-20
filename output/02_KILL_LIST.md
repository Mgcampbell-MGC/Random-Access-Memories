# 02 — KILL LIST

Every play that died, and the one-sentence reason. On-sight kills failed a **hard filter** (usually passivity) on their face and cost zero verification tokens. Verification kills (from Phase 1/2 adversarial red-teaming) are appended after the swarm runs.

> Status: on-sight kills recorded. Verification kills pending Phase 1 & Phase 2 completion.

## On-sight kills — original 9 (failed a hard filter immediately)

| Play | Source file | Verdict | One-sentence reason |
|---|---|---|---|
| **Rail Tank-Car Heat/Steam Pedestals** | `05_Rail Tank-Car Heat_Steam Pedestals` | KILLED (passivity) | The doc itself says "you're the guy who runs the operation day-to-day — hire and schedule 4 operators, run the daily dispatch board"; $360k/yr crew is the largest line item. This is a staffed steam-service business, not passive asset rental. |
| **Specialized Industrial Services** (transformer-oil processing, MV cable testing, SF6 handling, helium leak detection) | `09_specialized industrial service businesses` | KILLED (passivity) | Explicitly framed as "operator-as-technician — you're the skilled technician, not a brand"; all four are day-rate service jobs where the owner is on-site running the rig. Not rental, not passive. |
| **Specialty Trade Tools rental** (FLIR/thermal, pipe cameras, GPR) | `08_rentals` | KILLED (scale + moat) | ~$150–250/day on a $12k unit = trivial absolute cash flow; commodity gear any local shop can stock; no forced demand and no structural moat. Fails Rule 1 and Rule 4. |
| **Environmental-Control rental** (dehumidifiers, HEPA, spot cooling, temp heat) | `07_Environmental-control Equipment` | KILLED (demand + moat) | Genuinely passive and cash-flowy, but it rents the *exact gear Sunbelt/United Rentals already rent*, with no structural reason to win and no forced demand (overflow gear is a nice-to-have, not a must-rent). Fails Rule 3 and Rule 4 head-on. A defensible "boring cash flow" fallback — but it cannot clear the demand/moat bar, so it's out. |

## Verification kills — Phase 1 (original 9)

The adversarial swarm (Analyst → Red-Team → Score, with real 2026 web verification) killed **5 of the 6 contenders**. Only SilicaShield survived, and only weakly (4.15/10). Honest, utilization-adjusted numbers replaced every promoter figure.

| Play | Verdict | Honest CoC | Honest net/unit/yr | One-sentence cause of death |
|---|---|---|---|---|
| **Aquifer-as-a-Service** | KILLED | ~50%* | $99,000 | The "524%" is fantasy — honest net margin is ~25% on a complex live cooling-loop splice with a water-quality SLA; **no actual shutdown mandate exists** (Arizona/Virginia/Illinois rules are disclosure/ESG only), Nalco/Veolia disintermediate instantly, and any steady customer just buys the ~$1.2M unit (≈4-yr payback). *High CoC % is a mirage on tiny equity; absolute net is real but the demand and passivity legs fail. |
| **SpurSafe / QuickRack** | KILLED | 23% | $7,500 | An active 24/7 dispatch-and-liability job dressed up as asset ownership, plus a **rent-vs-own kill switch** — a customer buys the platform for ~$16–20k, which pays back faster than the 90-day contract minimum, leaving no durable rental customer beyond a sub-8-week episodic sliver. |
| **ConcreteWash** | KILLED | 15% | $2,000 | The EPA rule is durable but only mandates **cheap containment a $50 washout bag or $595 commodity rental already satisfies**; the touted 58% margin lives entirely on an unvalidated 3–5× premium with zero moat, while the owner works a full-time sales-and-dispatch job. Honest per-unit cash is near breakeven. |
| **ColdBox** | KILLED | −61% | −$3,303 | The entire spread rests on a **fabricated $4,300/mo buy-rate that is 3–8× verified retail reefer rent** ($550–$1,400/mo); on honest inputs every unit is cash-negative, with no moat and no true passivity. Textbook invented-pricing failure. |
| **RailWatch Virtual Gate** | KILLED | 10% | $3,000 | A monthly compliance-inspection **route** (hard passivity fail) selling optional camera "evidence" for a **voluntary, cosmetic, fully bypassable OCS audit that no regulation requires**, inside a commodity surveillance-trailer lane Sunbelt already owns. |

**Survivor (barely):** SilicaShield — SURVIVE, 4.15/10, honest 55% CoC, ~$15,500 net/unit/yr. Durable private-mandate leg ("no Written Exposure Control Plan = off the job"), but the pricing power lives in low-capex compliance *software* while the fleet you own is commoditized (Sunbelt rents the whole pod), it's non-passive due to life-safety liability, and absolute cash per unit is thin. It advances to the master ranking but is not a fundable #1.

> **Bottom line on your original 9:** none is a clean fund-it-tomorrow winner. Phase 2 must beat a 4.15 bar — and the kill patterns above (invented rates, rent-vs-own, dispatch routes, commodity gear, toothless demand) are now hard pre-filters.

## Verification kills — Phase 2 (net-new plays)

40-agent prospector swarm surfaced 36 candidates; 10 cleared the pre-filter and got the full Analyst → Red-Team → Score. **All 10 were killed.** (Full backlog incl. pre-filter rejects: `03_NEW_PLAYS_RAW.md`.)

| Play | Weighted | Honest CoC | Cause of death |
|---|---|---|---|
| Bridge Substation Fleet (transmission-class mobile substations to data centers) | 5.35 | 6% | Best-sourced demand teeth of any play (data center earns $0/day until energized, 2–4yr transformer lead times, can't-buy-in-time renter), but the entire revenue line rests on an unpublishable RFQ rate — margin collapses to ~8%, CoC ~6%. |
| Turnaround/Blowdown Rental Flare fleet (midstream/refinery) | 5.1 | 8.8% | Bulletproof code-based demand and a real capital/engineering moat — but the moat belongs to the vertically integrated incumbents, the rate is unverifiable, and the only passive structure has no customer (you can be passive or paid, not both). |
| Mobile Substation / Large Power Transformer Bridge-Rental (utility) | 4.55 | −3% | Genuinely near-passive bare-asset HV lease, but the revenue line is an unverifiable RFQ estimate, Tier-1 majors own the 20–50 MVA lane, and customers buy used surplus for $367k–$1M and amortize in <1yr — honest levered case is cash-negative. |
| USP <800> Mobile Compounding-Cleanroom Swing Space | 4.25 | 19% | Genuinely passive, real license-revocation teeth — but a new entrant lands BEHIND two GPO-backed specialist incumbents into a closing 2024–27 retrofit window; ~12% net, ~$30k/unit on a $1M single-purpose asset. |
| PSD / Air-Permit Preconstruction Ambient Monitoring fleet | 3.95 | 2% | Best-in-class passivity (9/10) can't rescue a razor-thin, owner-not-renter demand base (the 7 named contractors own their own fleets); unpriceable quote-only core asset; ~break-even. |
| SmallSystemBridge — interim PFAS compliance skids | 3.85 | 10% | Cash flow built on a $168k/yr lease rate that exists in no quotable form; on a defensible lease the unit barely clears debt+opex; target small/rural systems are handed $5B grants to buy/build, not rent. |
| GSU Power-Island fleet (mobile generator step-up transformers) | 3.45 | −70% | Real bleeding need for power, but the $530k/yr rate is fabricated (HV/GSU is RFQ-only) and rent-vs-own runs backwards — continuous base-load hyperscalers buy the iron; cash-negative on honest inputs. |
| SnooperFleet — Under-Bridge Inspection Unit rental | 3.45 | −31% | Real NBIS backdrop, but demand is two discretionary steps removed from the owner and the passive bare-rental slice is a minority of an operator-service-dominated market; levered unit runs cash-negative. |
| Mobile/Relocatable LINAC interim radiation-oncology | 3.05 | −122% | Genuinely passive with a real barrier, but the 60% margin rests on a ~$70–100k/mo rent that's 4–6× the only verifiable price ($16k/mo bare-LINAC floor); rebuilt on real rates it bleeds ~$514k/yr. |
| Mobile Cath-Lab interim dry-lease | 2.9 | −90% | Structurally cash-negative single-unit entrant; debt + a real $110–280k/yr angiography service contract exceed achievable revenue; enters as highest-cost, lowest-utilization player in an Atlas/DLP oligopoly. |

## Final Kill Gauntlet — Phase 3 (the 5 finalists)

Six independent sourced assassins per finalist (market-death, obsolescence, PE roll-up, rent-vs-own, passivity-trap, resale-cliff). **All five ruled DEAD.** Four lenses killed every single finalist: PE-rollup (5/5), rent-vs-own (5/5), passivity-trap (5/5), financeability (5/5). Market-death killed 0/5 — the demand is real; the *structure* is fatal.

| Finalist | Verdict | K/W | The single fact that ends it |
|---|---|---|---|
| SilicaShield | **DEAD** | 5K/1W | OSHA's own Table 1 safe harbor: a $300–1,500 owned shroud + HEPA-vac kit ($370 at Harbor Freight) delivers identical legal compliance and exempts the sub from the air monitoring the $25k pod is built around — obsolete at origination. |
| Bridge Substation Fleet | **DEAD** | 4K/2W | Cannot be financed as near-passive (SBA bars passive equipment-leasing), forcing recourse debt against custom, non-interchangeable iron with a scrap-metal liquidation floor; and the rate is unverifiable. |
| Turnaround Rental Flare | **DEAD** | 4K/1W | The moat IS the labor and the incumbents own it: a rented turnaround flare is a 24/7 attended life-safety device (API 537 continuous pilot, pilot-out alarms — the literal 2am phone) and only integrated OEM/PE platforms engineer, staff, and stage it. |
| USP <800> Cleanroom | **DEAD** | 4K/2W | You're a retail-buying middleman between hospitals and the OEMs — and the OEMs already run their own GPO-backed rental fleets at cost for the identical swing-space use case, so there's no rental premium left to capture. |
| Mobile Substation (utility) | **DEAD** | 4K/0W | The customer is a regulated utility earning ~9–11% ROE on assets it OWNS in rate base and zero on a rental — so for any durable bridge need the rational utility buys and rate-bases the unit; for true emergencies it draws on member-owned spare pools. |

## The five structural laws this sweep proved (why *nothing* survived)

1. **SBA won't finance passive leasing.** 13 CFR 120.110/120.111 bars passive/equipment-leasing businesses from SBA 7(a). The "SBA hack" in your original 9 (esp. Aquifer) is fiction for a pure asset-owner. To be financeable you must be an *active* operator — which breaks passivity.
2. **PE already rolled up every good niche.** Flares, transformers, cleanrooms, imaging — all consolidated by PE platforms or the OEMs. A solo from-scratch entrant is late and out-gunned on price, national accounts, and OEM allocation. (Killed 5/5.)
3. **Rent-vs-own is an iron law.** Cheap asset → customer buys it. Expensive-but-continuously-used asset → customer buys and amortizes/rate-bases it. Only episodic users truly rent — and episodic use kills utilization. (Killed 5/5.)
4. **Passivity and moat are mutually exclusive.** Every real moat here IS non-delegable labor (attended flare, competent-person inspection, validated cleanroom). Passive = commodity; moated = you bought a job. (Killed 5/5.)
5. **"Forced demand" is usually softer than the pitch.** Safe-harbor alternatives (silica Table 1), disclosure-only rules (data-center water), or the customer's own ability to own defuse the "must-rent" claim. Real teeth are rarer than headlines suggest.
