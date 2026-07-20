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

_Pending — populated from the Phase 2 pre-filter and red-team verdicts._
