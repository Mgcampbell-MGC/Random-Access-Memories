# FINAL PROPOSAL: DECKPROOF

**The decision: build DeckProof — a buyer-meeting numbers audit for CPG brands — at US$750, wedged on the supplement/HBC sellers named on ECRM's published session rosters. Parser test starts this week. First outbound lands before the 25–28 Oct 2026 rosters go stale.**

One line on the runner-up: LICENCEPROOF (UK sponsor-licence evidence pack) is the switch if DeckProof's parser fails — its trigger stream is verified and fires daily, but it sells authority into a fear market where a credentialed firm gives away a close substitute for free [VERIFIED, https://iasservices.org.uk/uk-home-office-compliance-audit-checklist-template/], and DeckProof is the only candidate whose authority rests on nothing: the buyer can check the arithmetic themselves.

---

## 1. THE PRODUCT AND THE PURCHASE TRIGGER

**What the buyer downloads.** One self-contained .html file, opened with a double-click. No install, no account, no upload — pdf.js and SheetJS inlined in a single classic script so it works over file:// (permitted format 3). The buyer file-picks their pitch-deck PDF and their cost/price spreadsheet. Everything computes in-page; their COGS never leaves their machine. Output, printable:

1. **A findings report** — "31 checks run, 5 discrepancies a buyer will catch": retailer margin recomputed at stated wholesale/SRP, case-pack and pallet math, promo/scan-deal math, every figure that appears in both deck and cost sheet cross-checked.
2. **A corrected one-page buyer-facing economics sheet** — SRP, wholesale, margin, case/pallet config, formatted the way retailers ask for it. They carry this *into* the room. This is the reposition that earns $750: a document, not a critique.
3. **A per-retailer required-fields checklist**, driven by a corpus compiled from public retailer supplier guides.

**The exact observable event that makes them buy today.** Their company's name appears on a published ECRM seller roster for a dated session they have already paid US$7,000 (10-min Discovery), US$11,000 (10-min Innovation) or US$16,900 (20-min Planning) to attend [VERIFIED, https://ecrm.marketgate.com/Sessions/2026/10/LatinAmericaBeautyPersonalCare]. The seller roster is public, no login, at the `rt=S` parameter: https://ecrm.marketgate.com/Sessions/2026/10/LatinAmericaBeautyPersonalCare/Attendees?rt=S&a=1 [VERIFIED by direct fetch, 6 Aug 2026 — names Beauty Creations Cosmetics (US), Timeless Skin Care (US), Ordo (UK), Coscentra BV (NL), and others].

**Where published, and lead time.** ECRM's public calendar (https://ecrm.marketgate.com/sessions [VERIFIED]) shows 93 sessions Aug 2026–Sep 2027; 15 have published seller rosters today, 78 read "posted in the near future" — rosters appear roughly 1–6 months ahead [VERIFIED by enumeration of all 93 pages]. The October example gives **11 weeks of lead time**. This is a rolling stream, not one event.

## 2. THE BUYER, AND HOW SOL REACHES THEM

**Who.** Founder or Head of Sales at an indie CPG brand, 5–50 staff. USA primarily, UK/EU secondarily. This person owns the company card; $750 against a sunk $7,000–16,900 meeting is not a procurement event. B2B only — EU sales invoice under reverse charge (Art. 44/196), zero VAT, no registration.

**The list.** 475 unique seller companies named on the 15 live rosters right now; 473 carry a clickable company website in the roster markup; ~445 are USA/UK/EU addressable (292 US-domestic, 70 explicit USA, 58 EU, 25 UK) [VERIFIED by enumeration script, data on disk at `ecrm_rosters.json` in the session scratchpad]. Run-rate: ~32 sellers/session × ~80 sessions/yr ≈ **2,300–2,600 named, domained, dated brands/year** [derived from VERIFIED 475/15; the sessions-per-year figure is PLAUSIBLE]. Warm tier: public exhibitor lists — Expo West ~3,000 exhibitors [PLAUSIBLE; mechanism VERIFIED via a live no-login sub-directory at exhibitor.expowest.com], Fancy Food, Cosmoprof NA — ~8,000–12,000/yr [PLAUSIBLE].

**The legal line, stated plainly.** ECRM's Terms of Use prohibit scraping and harvesting contact information [VERIFIED, https://ecrm.marketgate.com/UserTerms]. So: no automated scraping of ECRM, ever. Sol reads ~30 names per roster by hand, takes the company domain from the roster's own link, and sources the *person* from Apollo or the company's website. Contract risk only (no login, no clickwrap); worst practical case is an IP block. Expo West's list carries a similar no-solicitation term [VERIFIED] — same manual discipline.

**The outbound motion.** All written English, fully scripted — no calls, no camera, no name. USA is CAN-SPAM opt-out: legal. UK is PECR corporate-subscriber: workable. **Germany is excluded from email entirely** (UWG §7(2)) — German firms are a small slice of the 58 EU sellers and are simply skipped. Volume: HOT tier needs ~200 emails/month against a new domain's safe 600–1,000/month — comfortable. Warm tier from month ~5 adds 2 warmed domains at ~700/month each. The sending physics fit with room to spare; the constraint is list size, not deliverability, which is why the warm tier exists.

## 3. WHY IT BEATS THE COMPETITION — AND WHY A PROMPT CANNOT DO IT

**No identical product exists.** Searched in the buyer's own language; everything AI-adjacent in CPG pitch prep is data/analytics (what to say), not verification of the brand's own numbers [PLAUSIBLE — multiple searches, no matching product surfaced].

**Cheapest substitutes, honestly priced:**
- Free single-purpose margin/case-pack calculators (BoxNCase, CPG Guy, Margin Velocity) [PLAUSIBLE, e.g. https://www.boxncase.com/resources]. They compute one number you type in. They do not read your deck, cross-check it against your cost sheet, or find the contradiction between slide 9 and row 40.
- US$199 "pitch deck review" [PLAUSIBLE, pitchdeckcost.com] — VC fundraising decks, subjective design feedback, wrong market.
- Emily Anne Page, US$300 live ECRM pitch coaching [VERIFIED, https://www.emilyannepage.com/ecrm-special-offer/] — a real ex-buyer, distributed inside the exact channel. **She coaches delivery. She does not machine-verify arithmetic.** She is the competitor for BuyerRoom's rehearsal half — which is exactly the half this product discarded.
- Brokers sanity-check economics free (they take 3–7% commission) [PLAUSIBLE, foodbevy.com]. But ECRM's model is brands paying five figures to meet buyers *directly* — the roster self-selects for brands going without a broker. This caps the warm tier, not the HOT tier, and is tracked as a kill-signal in the test.

**Why the buyer pays anyway:** none of the above does the whole job — recompute every number in *their* documents and hand back a corrected sheet — and the gap is precisely what a wrong margin recited to a Kroger buyer costs.

**The R3 defence, concretely.** (1) Arithmetic across a 30-slide deck plus a workbook is where LLMs are measurably unreliable, and a confident-but-wrong number in a buyer meeting is worse than no answer — determinism is the product. (2) The retailer-requirements corpus is assembled from many separate public supplier guides; one prompt does not contain it. (3) The cost sheet is confidential — the prompt route requires pasting COGS into a chatbot; the local HTML never sends a byte.

## 4. THE ECONOMICS

Price **US$750** (top of band; 4–9% of the sunk session fee). Target R$30.000/month net ≈ US$7,400–8,300/month revenue ≈ **10–11 sales/month**.

**Capital at risk before the first sale: under US$220.** Domain ~$12, email tooling ~$20/mo, Apollo credits $50–100, Wise Business free. The build costs days of Claude Code time, not money.

**The ramp, month by month** (conversion rates are the brief's triggered band, 1.5–3% [PLAUSIBLE]; list sizes as tagged above):

| Month | Motion | Sales/mo | Revenue/mo |
|---|---|---|---|
| Aug 26 | Build + parser test on 20 real decks | 0 | $0 |
| Sep 26 | 200-email test vs Oct rosters | 2–4 presales | $1,500–3,000 |
| Oct–Dec 26 | HOT stream only, ~200–250 sends/mo | 4–7 | $3,000–5,250 |
| Jan–Apr 27 | + warm tier, 2 extra warmed domains, 600–900 sends/mo | 8–14 | $6,000–10,500 |
| May–Jul 27 | Steady state if both tiers hold | 10–16 | $7,500–12,000 |

**The honest number:** ECRM alone is a US$24–36k/year business (2,400 triggered × 2–3%) — worth running, not target. Target requires the warm tier converting at ~1.5%. **Year one plausibly averages US$4,500–6,500/month revenue ≈ R$18–26k/month net — below the R$30.000 target**, crossing it as a run rate around months 8–10 if the warm tier performs. Steady state at 192 sales/yr ≈ US$12,000/month. That is the full honest range; the previous plan's honesty about R$27–32k against R$40k was valued, so: this one likely lands under target for most of year one.

## 5. THE BUILD — IN ORDER

1. **Days 1–5: the parser.** pdf.js + SheetJS extraction inside one inline classic script. Test corpus: 20 real sell sheets pulled from the 473 verified company domains already on disk. This is the gate — see Section 7.
2. **Days 3–7 (parallel): the free giveaway.** A single-page local-HTML margin & case-pack checker. Proves the mechanism in 30 seconds, makes the cold email a gift, and builds the standing-presence half that survives if outbound disappoints.
3. **Days 6–14: sell before the build is finished.** 200 hand-read sellers from the Aug/Sep/Oct rosters, subject line naming their actual session and date, free checker attached, $750 presale with delivery date. The full product does not need to exist to run this.
4. **Weeks 3–4: the corpus and the full report.** Retailer required-fields and margin norms compiled from public supplier guides — confirm all six guides are freely obtainable *before* naming them in copy (only Walmart's is currently [PLAUSIBLE]). Findings report + corrected one-pager + checklist output. Wedge vertical: **supplements/HBC** — the `VitaminDietSportsNutrition` roster alone has ~100+ named sellers with domains [VERIFIED], and supplements carry the nastiest margin/case-pack/claims math, so most findings per deck.
5. **Ongoing:** roster watcher (manual reads on ECRM per its ToS), per-retailer editions (Walmart, Ulta, Kroger), annual corpus refresh.

**Claude Code stays on Sol's side of the transaction:** it builds the parser, compiles the corpus, drafts the personalised emails, generates the per-retailer editions. The buyer receives a file that works with a double-click.

## 6. HOW IT BEATS BUYERROOM

| Axis | BuyerRoom (the bar) | DeckProof |
|---|---|---|
| Output | a rehearsal the buyer must perform | a finished checked document + corrected economics sheet |
| Repeat purchase | once per meeting | per event + per-retailer editions + annual corpus refresh |
| Trigger frequency | ~6–9 beauty sessions/yr | rolling rosters across ~80 sessions/yr, all categories [VERIFIED calendar; per-year count PLAUSIBLE] |
| Proof of value | subjective | "found 5 errors in your own deck" — screenshottable |
| Buyer population | 240–540/yr → 25–80% penetration needed | ~2,400/yr HOT + 8–12k WARM → 3% + 1.5% needed |
| Adoption | wants a paid AI account (approval step) | double-click HTML, no LLM, no account |
| Human competitor | Emily Anne Page, $300, inside the channel | she coaches delivery; nobody sells machine-verified arithmetic |

**Where it is weaker, honestly:** the loss it prevents is the wasted value of a *sunk* five-figure meeting, not a new cost or a fine — a softer anchor than a regulatory deadline. And ECRM alone misses target, so it inherits a diluted version of BuyerRoom's volume wound, fixed only by the warm tier. Both are acceptable: the sunk cost is still five figures and the numbers *are* the substance of the pitch, and the warm-tier requirement is measurable within the first 90 days.

## 7. THE ONE NUMBER THAT DECIDES IT

**Paid orders per 200 triggered emails, measured in 14 days. Threshold: 2.**

Gate first (week 1, $0): the parser must cleanly extract SRP, wholesale, case pack and margin from **≥15 of 20** real sell sheets, and find ≥1 genuine arithmetic discrepancy across them. **≤12/20 → stop, switch to LICENCEPROOF** — the deterministic promise collapses into a data-entry form and the R3 defence dies with it.

Then (days 6–14, <$200 total): 200 hand-read sellers from the published Oct rosters, $750 presale. **PASS = 2+ paid orders, or 6+ replies asking price. 0–1 orders AND <6 price replies → stop.** Kill-signals inside the replies: >30% saying "my broker handles this"; any saying the retailer's own portal already checks the numbers.

## 8. WHAT IS STILL UNVERIFIED — AND THE TEST FOR EACH

**Must be settled before building anything: nothing.** The build *is* the first test and costs $0. That is the point of this founder's cost structure.

**Settled during the first two weeks (by the build and the $200 test):**
1. **Parser reliability on Canva/InDesign decks** [UNKNOWN] — 20 real decks; pass ≥15/20.
2. **Willingness to pay $750 sight-unseen from an unknown Brazilian vendor** [UNKNOWN] — the 200-email test; pass = 2 paid or 6 priced replies.
3. **Broker substitution rate** [PLAUSIBLE risk] — count "my broker handles this" replies; kill-signal >30%.

**Only matter after the first paying customer (most items live here — say so, so nothing above blocks the start):**
4. **~80 ECRM sessions/yr and ~32 sellers/session run-rate** [PLAUSIBLE; 475/15 VERIFIED] — watch the calendar monthly as the 78 pending rosters publish; pass = ≥25 sellers/session average.
5. **All six retailer supplier guides freely obtainable** [only Walmart PLAUSIBLE] — one day of checking; pass = 6/6 without a login wall, *before* they are named in marketing copy.
6. **Expo West ~3,000 exhibitors and warm-tier ToS handling** [PLAUSIBLE; ToS bar VERIFIED] — count the directory manually when building the warm tier in month 4–5.
7. **Warm-tier conversion at 1.5%** [PLAUSIBLE benchmark] — this is the number that decides whether the business hits target or plateaus at $24–36k/yr; measurable only by sending, from month 5.
8. **Repeat-purchase rate on per-retailer editions** [UNKNOWN] — measurable only with customers.

## 9. WHY THIS COULD BE BIG, IF IT WORKS

Factual upside, then marked speculation.

- The 78 not-yet-published rosters are real sessions already on the calendar [VERIFIED]; if they publish at the observed rate, the HOT list alone is 2,300–2,600 dated brands/yr, refreshed forever, at zero list cost.
- The engine is a platform: deterministic numbers-audit + bundled requirements corpus + local-HTML delivery. BidProof (UK tender pricing audit, verified free enumeration via Find a Tender award notices) is the same engine pointed at a different corpus — already vetted as the #2 build. Per-retailer editions (Walmart, Ulta, Kroger) turn one customer into three purchases.
- The free checker compounds: every download is a standing-presence asset that works while Sol sleeps, in a category with no incumbent.
- *Speculation:* coaches and consultants in the channel (the Emily Anne Pages) check delivery, not numbers — a bundle or affiliate deal is complementary, not competitive. *Speculation:* ECRM itself, or RangeMe, could become a distribution partner, since a brand with clean numbers makes their sessions look better. Neither is needed for the plan to work; either would roughly double it.

**Commitment: the parser gets built this week against 20 real sell sheets from the 473 verified domains. 15/20 → the 200-email test runs against the October rosters. The window on those rosters closes in eleven weeks.**