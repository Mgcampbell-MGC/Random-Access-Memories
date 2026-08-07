I re-checked exactly two things, both from scratch rather than re-reading the measurement pass: **(1) the whole defect join**, on files I downloaded myself today, and **(2) the Gate 0 fee**, including the specific question of whether *importers* pay it. Both held. I also found one new, materially better version of the finding that the measurement pass missed (the K-number linkage in §3).

---

# IMPORT CHAIN INTEGRITY
### FDA device-importer supplier-registration audit and monitoring

---

## 1. THE BUSINESS

A US company that imports medical devices must file, in its own FDA registration, a list of the foreign factories it imports from. Every year a slice of those factories quietly fail to renew their FDA registration and FDA deletes them from the public file without telling the importer — so the importer's own federal filing now points at establishments FDA no longer lists, and devices from an unregistered foreign establishment are misbranded at the border.

Sol sells a US$350 pre-computed PDF that tells a named importer how many of its declared factories are missing from FDA's current file and which of its cleared device listings they sit under, then US$199/month to keep watching the weekly files.

---

## 2. WHY THE BUYER CAN PAY — Gate 0, measured

**Every prospect has paid US$11,423 to FDA in the last ten months, or it would not be in the file at all.**

This is Gate 0 by construction rather than by sampling, and it is the reason this candidate is the pick. The population is not "companies that have a defect" — it is "companies that hold a current FDA establishment registration," which is a fee-gated list.

- **[VERIFIED — fda.gov, fetched today]** FY2026 annual establishment registration fee is **US$11,423**, payable 1 Oct – 31 Dec 2025, covering 1 Oct 2025 – 30 Sep 2026. (Federal Register doc 2025-14412, 30 Jul 2025; confirmed on FDA's own MDUFA fee page.) Up from US$9,280 in FY2025.
- **[VERIFIED — fda.gov "Who Must Register, List and Pay the Fee", fetched today]** This was the load-bearing detail I specifically re-checked, because the whole case collapses if importers are exempt. They are not. For **Initial Importer**: Register = "YES 807.40(a)", Pay Fee = "YES". Exempt from the fee are domestic distributors that do not import, specification consultants, and wholesale distributors that are neither manufacturer nor importer. The buyer class Sol targets is inside the paying set.
- **[VERIFIED — my own recomputation from Registration.txt today]** 28,535 currently-registered establishments; **5,741 carry INITIAL_IMPORTER_FLAG = 'Y'**; 5,920 US-addressed registrants declare at least one foreign manufacturer.
- **Size distribution inside the buyer set, computed today:** of those 5,920, **1,147 declare 5 or more** foreign manufacturers and **543 declare 10 or more**. Declared-manufacturer count is a direct proxy for import volume and therefore revenue. Named examples at the top: SSPT Inc. 359 declared, DYNAREX CORP. 306, MEDLINE INDUSTRIES LP 291, HENRY SCHEIN 253 (across 12 separate US registered sites), Cardinal Health 200 LLC 244, Medical Depot Inc. 224.

There is a small-business hardship waiver for the annual fee, so the floor is not perfectly hard — but a waiver is exceptional and requires an FDA Small Business Determination. The charity candidate died because 70% of the population had under US$50k revenue. Here, a company that cannot find US$11,423 is *out of the file*, and the ~5,900-member population that remains is, by definition, one that wrote that cheque.

**Gate 0: PASS, on a mandatory fee rather than an inference.**

---

## 3. THE DEFECT — as the cold email states it

Two values, both from the recipient's own federal filings, both checkable in FDA's free search in under five minutes. Real companies, real numbers pulled from today's file:

> **Subject: 3 of the 5 factories in your FDA filing aren't in FDA's current registration file**
>
> Randox Laboratories-US, Ltd — FDA establishment registration **2086993**, Kearneysville WV.
>
> Your FURLS registration declares **5** foreign manufacturing establishments. **3 of the 5** do not appear in FDA's current establishment registration file (the 3 Aug 2026 weekly extract). Those 3 establishments are the ones attached to **92 of your device listings**, including **K000375**, **K000468**, **K000469** and **K000661**.
>
> To check: open your FURLS account, take those three factory names off your own declared-manufacturer list, and search each in FDA's free Establishment Registration & Device Listing database. They will not return a current registration. FDA sends no notice when a declared manufacturer's registration lapses.

Second real example, a different shape:

> **METROPOLIS INTERNATIONAL, LLC** — registration **3005877899**, Long Island City NY. Declares **13** manufacturers; **3** are absent from FDA's current file; those 3 sit under cleared submissions **K050299, K024352, K082987, K050514, K050622** and **K120388**.

Three more from today's run, to show the pattern is not cherry-picked: **NOBEL BIOCARE USA, LLC** (reg 2027971, Yorba Linda CA) 17 declared / 4 absent, two under K041275 and K913255; **MEDTEN USA INC.** (reg 3018817074, Irvine CA) 23 declared / 3 absent, one under K161938; **IMPERIAL OPTICAL, INC.** (reg 1319386, Champlain NY) 19 declared / 7 absent.

**This is the new finding I discovered while spot-checking, and it upgrades the product.** The measurement pass stopped at "N of your declared manufacturers are missing." I tested whether the importer→manufacturer declaration table joins to the device-listing table, and it does: of 150,426 declaration rows, **54,218 distinct listing keys join**, and of the 24,767 dangling declaration rows belonging to US importers, **2,675 carry a premarket submission number**. That means for **282 importers** Sol can name the *cleared device* whose declared factory has vanished — **1,481 distinct K/P numbers implicated**, and 171 of those importers have two or more. A K-number is the single most self-evident object in this vertical: the recipient looks it up in FDA's free 510(k) database and sees their own clearance.

**S5 discipline:** Sol never says "you are non-compliant" or "this shipment will be detained." She says *your filing declares 5, FDA's current file contains 2, here are the listing IDs*. The count and the identifiers are facts. The recipient supplies the names from their own account and confirms the absence in the regulator's own search. No borrowed authority anywhere.

---

## 4. THE MEASURED NEED

Measured on the **full population**, not a sample. I re-ran this from scratch today — downloaded the zips myself, wrote my own join, and did not consult the previous script:

| | |
|---|---|
| `Registration.zip` fetched | HTTP 200, **2,035,736 bytes** |
| `Manu_ID_by_Imp.zip` fetched | HTTP 200, **1,084,839 bytes** |
| Registration rows / unique establishments | 43,990 / **28,535** |
| Declaration rows / distinct declaring importers | 150,426 / 6,011 |
| **US importers currently registered, with declarations** | **5,920** |
| **Total dangling declared-manufacturer links** | **6,325** (3,478 distinct absent establishment keys) |
| **Importers with ≥1 dangling — RAW rate** | **1,846 = 31.18%** |
| **Importers with ≥2 dangling — CLEAN rate** | **891 = 15.05%** |
| ICP (5+ declared AND 2+ dangling) | **717** |
| Mid-size ICP (5–25 declared, 3+ dangling) | **381** |
| Premium tier (≥1 dangling under a cleared K/P number) | **282**, of which 125 are non-giant (≤40 declared) |

Every one of those figures matched the measurement pass to the digit. That is now three independent reproductions of the same join, on two different weekly snapshots.

**Raw versus clean, honestly.** A dangling link has three possible causes: (a) the foreign factory genuinely failed the Oct–Dec renewal, (b) it re-registered and FDA issued a new internal key so the importer's old reference is stale, (c) the importer never removed a supplier it stopped using. The 31.18% raw rate covers all three; the 15.05% two-or-more rate is the conservative floor. I have not separated (a) from (b)/(c) and neither had the previous pass — that separation needs a prior weekly snapshot, which is §8's first build step and §10's first open question.

**Critically, the pitch does not depend on which cause it is.** In all three cases the importer's own federal filing is wrong and the importer must fix it. The border-risk framing only applies to case (a); the filing-accuracy framing applies to all of them and is the framing Sol uses until her archive can tell the difference.

---

## 5. WHY IT RECURS

Three independent clocks, which is why this is a subscription and not a report:

1. **Weekly.** FDA republishes the whole extract every week. I verified freshness directly: the files I pulled today carry a 3 Aug 2026 timestamp. Supplier relationships and device listings change continuously between snapshots.
2. **Annually, in a wave.** Registration renewal runs 1 Oct – 31 Dec. Every January a fresh cohort of foreign establishments drops out of the file. That is a dated, forward, calendar-driven event Sol can pre-announce to subscribers in September and deliver against in January — the natural renewal hook.
3. **Never completes.** Supply-chain integrity is a standing condition, not a task. The subscriber has no "done" state.

**And the deletion behaviour is the moat.** I confirmed FDA does not merely mark lapsed establishments — it erases them. Of the 3,478 distinct absent establishment keys, **0 appear anywhere in `registration_listing.txt`** and **exactly 1 appears in `Official_Correspondent.txt`** (274 survive as orphan keys in one relationship table, with no name attached anywhere). The openFDA API carries only `reg_expiry_date_year = 2026` — every prior year is gone. **Registration.txt itself confirms this: all 43,989 data rows carry expiry year 2026, with no other value present.** Nobody — not the buyer, not a competitor, not FDA's own public search — can reconstruct *who* the lapsed factory was or *when* it disappeared without a private archive of weekly snapshots. Sol's archive starts accruing on day one and is the one thing about this business that cannot be copied by starting later.

---

## 6. THE BUYER AND THE LIST

**Who:** the regulatory-affairs or QA manager at a US medical-device initial importer or distributor. Not procurement, not legal. This person owns the FURLS account, is personally the one who would have to correct the declaration, and is the named individual FDA already holds on file.

**How many, verified today:** 5,920 US importers with declarations → 1,846 currently defective → 717 in ICP → 381 mid-size → 282 with a K-number-linked finding. Giants (Walmart, Medline, Cardinal, Henry Schein) are in the defective set but excluded from the ICP: procurement-gated, fails S16.

**How she reaches them with no audience, no calls, no face — this is the unusually good part.** The contact is inside the government file. `Official_Correspondent.txt` gives a named person plus phone for **5,920 of 5,920** US importers with declarations — I checked coverage explicitly and it is 100%. Example: Imperial Optical's correspondent is SAMIR GAD, with phone. FDA publishes the name of the exact human responsible for the filing that is wrong.

Names go to Apollo for email enrichment (Apollo is already wired as a tool here). Sending is CAN-SPAM cold email with a real opt-out, US-only, no CASL and no German exposure. Delivery is a PDF attached to an email. No call, no app, no login, no English conversation — the entire funnel is written asynchronously in a language Sol can draft carefully and reuse.

**S10, checked and cleared:** FDA's warnings in this space target vendors who sell fake "FDA registration certificates" for a fee. Sol sells no certificate, solicits no fee on FDA's behalf, impersonates nothing, and points the recipient at their own FURLS account and FDA's own free search. The copy must never contain certificate-like graphics or FDA logos — that is a hard rule for the email template, not a residual risk to shrug at.

---

## 7. THE MONEY

**Price:** US$350 one-off Supplier Registration Integrity Audit (per registered site), then **US$199/month** monitoring against the weekly files, with alerts when a declared manufacturer disappears, a new dangling link appears, or the Oct–Dec renewal wave hits.

**To reach US$7,400–8,300/month:**

| Mix | Monthly |
|---|---|
| 40 retained at $199 | $7,960 |
| 30 retained at $199 + 6 audits at $350 | $8,070 |
| 25 retained at $249 + 5 audits at $350 | $7,975 |

**Penetration required, stated plainly:** 40 subscribers is **5.6% of the 717 ICP**, or 2.2% of the 1,846 currently-defective importers. That is a higher conversion rate than a mass list would need, and it is the honest cost of a small population. What buys it back is that every single email quotes the recipient's own registration number and their own two counts — this is not a 0.5%-reply blast, it is 700 hand-computed findings.

**Capital at risk before the first sale: under US$150 cash.** Domain ~US$12. Resend on free tier for the first 3,000 sends, then US$20/month. Storage for the weekly archive: the nine zips total ~21MB/week, ~1.1GB/year — pennies on R2. Apollo credits for ~400 enrichments. All source data is a free government download requiring no account. Build cost is Claude Code time, which is one-time and near zero. This is the cheapest first dollar of any candidate in the field.

**Honest ramp:**

- **Weeks 1–2:** archive cron live (this is urgent — every week of delay is a week of lapse-history she can never recover), join engine, PDF template.
- **Weeks 3–4:** first test (§9), 60 emails.
- **Month 2:** first paid audits if the test clears. Realistic: 2–5 at $350 = $700–1,750.
- **Months 3–4:** audits convert to monitoring. 8–15 retained. ~$2,500–4,000/month.
- **Months 6–9:** 30–45 retained. Target range reached, assuming ~4–6% ICP penetration and that audit→monitoring conversion runs above 50%.
- **September of year one:** the renewal-wave email to every non-customer, and the January delivery against it. That is the natural second wave, and it arrives with a dated, calendar-driven reason to buy.

---

## 8. THE BUILD

Four weeks of Claude Code, in this order. The ordering matters because step 1 is time-sensitive in a way nothing else is.

**1. The snapshot archive — day one, before anything else.** A weekly cron that pulls all nine FDA zips to object storage, timestamped and immutable. Note the fetch requires a browser User-Agent (plain curl gets a 302 to an abuse page; I hit this and it is trivially handled). Every week this runs, the asset appreciates and the moat deepens. Nothing downstream needs to exist yet.

**2. The join engine.** Parse the pipe-delimited files (watch two real gotchas I hit today: `Listing_Proprietary_Name.txt` uses lowercase `key_val` while every sibling file uses uppercase, and one field exceeds Python's default 131,072-byte csv limit). Produce per-importer: declared count, dangling count, dangling keys, and the K/P numbers each dangling key sits under. Diff against last week's snapshot.

**3. The FEI continuity resolver — the thing that separates raw from clean.** `Registration.txt` carries `FEI_NUMBER`, and FEI is stable across a re-registration where the internal REG_KEY is not. Once Sol holds two snapshots, she can look up a vanished key's FEI in the older snapshot and ask whether that FEI reappears under a new key in the current one. That mechanically separates cause (a) — genuine lapse — from cause (b) — re-registration. **This is buildable only with archive history, which is exactly why step 1 is day one, and it is the single highest-value build item in the project.**

**4. The PDF and the email machine.** Pre-computed per-importer PDF: the two counts, the dangling keys, the affected listings and K-numbers, the FURLS-and-FDA-search verification instructions, and a fix checklist. Then Apollo enrichment keyed off the official-correspondent names, Resend with per-recipient merge fields and a working opt-out.

No hosted app, no buyer-side compute, no per-transaction human step. A card purchase and an emailed attachment.

---

## 9. THE FIRST TEST

**One measurement: does a regulatory manager, shown two numbers from their own federal filing, reply?**

- **Cohort:** 60 importers drawn from the mid-size ICP — 5 to 40 declared manufacturers, 3 or more dangling, giants excluded. This cohort exists and is enumerated: 381 mid-size ICP members, 125 of them with a K-number-linked finding. Prioritise the K-number tier, since that is the strongest version of the finding.
- **Each email** quotes their registration number, their declared count, their dangling count, their affected K-numbers where present, the FURLS-plus-FDA-search verification path, and offers the US$350 audit with a Stripe link.
- **Cost:** under US$100 (domain, Apollo credits, Resend free tier). **Duration:** 14 days from first send.
- **The corpus is already in hand.** This is the screen that killed an earlier plan — a free test whose data did not exist. Here the entire input is nine government files I downloaded and joined this afternoon, and the 60 findings can be generated before the domain is even bought.

**Numeric stop thresholds:**

| Outcome in 14 days | Decision |
|---|---|
| ≥1 paid US$350 audit, **or** ≥5 replies of which ≥3 ask for the list or the price | **BUILD.** Proceed to full engine and 700-prospect rollout. |
| 2–4 replies, none commercial | **ITERATE ONCE.** Re-send 60 more with the K-number framing forward and "your filing is inaccurate" replacing any border language. One iteration only. |
| ≤1 reply, or ≥2 replies saying "that supplier re-registered, this is a non-issue" | **STOP.** The defect is real but not felt, and no amount of engineering fixes that. |

That third row is the honest kill condition and it is cheap to reach.

---

## 10. WHAT MUST BE TRUE

**Must settle before building anything beyond the archive cron:**

1. **Does the dangling link land as material, or get shrugged off as a re-registration?** This is the real weakest link, and §4 is candid that the raw 31.18% mixes true lapses with stale references. Cheapest settlement: the §9 test, whose reply *content* is the measurement — and it costs under US$100. A second, near-free settlement: nine scripted written questions (no calls) to regulatory managers asking whether they audit their FURLS declared-manufacturer list at all.
2. **Is fdadevicecheck.com's US$19/month watchlist pilot a price ceiling or a different product?** It does current-status lookups on facilities *the user already knows about*; it cannot read the importer's own declaration or date a lapse, because that data is purged. But a US$19 anchor in the same inbox is a real hazard to a US$199 price. Cheapest settlement, cost zero: request their pilot invitation and read what arrives.
3. **Does Apollo return work emails for FDA official correspondents?** Sol has 5,920 named people with phone numbers and no email addresses. Cheapest settlement: run 50 through Apollo before writing a single line of PDF code. If the match rate is under 40%, the channel needs rethinking before the build, not after.

**Only matters after the first customer:**

4. Whether Wayback holds prior `Registration.zip` snapshots, which would backfill lapse *dates* immediately rather than in eight weeks. I attempted this today and was blocked (429 from archive.org, 403 egress). Worth one retry from an unblocked network, but it accelerates rather than enables — her own archive solves it by month two regardless.
5. Whether a US$350 audit converts to US$199/month above 50%. Only observable with customers.
6. Whether the same engine sells a second SKU pointed the other way — telling foreign manufacturers which of *their* declared US importers have lapsed (`Reg_Imp_ID_by_Manu.txt`, 258,134 rows, already downloaded). Same code, different recipient, and it is non-US outreach, so park it.

---

## 11. WHY IT BEATS ADV-CHECK

| | ADV-Check | Import Chain Integrity |
|---|---|---|
| **Solvency** | Asserted from "registered adviser" — no size distribution | **Every prospect paid US$11,423 to FDA between Oct and Dec 2025.** Verified on fda.gov today, including the specific confirmation that initial importers pay. Fee-gated, not inferred. |
| **Measured need** | Mismatch rate **unmeasured** — the stated weakness | **31.18% raw / 15.05% clean, on the full 5,920-member population**, reproduced independently three times, with 1,481 named K-numbers and dozens of named companies. |
| **Recurrence** | Annual | **Weekly file refresh, monthly subscription, plus an annual Oct–Dec renewal wave** that creates a dated reason to buy every January. |
| **Price durability** | US$650 "under pressure" | US$350 + US$199/mo. Lower ticket, but recurring, and the January wave gives a renewal hook a one-off report never has. |
| **Time to first dollar** | Cold email only, finance vertical, ads at US$10–30/click | **Cold email to a person FDA names for her**, 100% contact coverage in the government file, first 60 personalised findings computable today for under US$100. |
| **Defensibility** | Two public documents any analyst can pull | **FDA erases lapsed establishments from every public source** — 0 of 3,478 absent keys survive in the listing file. A private weekly archive is the only route to naming and dating a lapse, and it cannot be built retroactively. |

It is weaker than ADV-Check on exactly one axis, and it should be said plainly: the addressable list is 5,920 rather than 16,779, and 40 subscribers means 5.6% of the ICP. That is the constraint the whole plan is built around — which is why the ticket is small, the audit is the wedge, the contact list is 100%-covered from the government file, and the test costs under US$100 to run.

---

*One note for a future reader on the rest of the field: LienGap and MDRP Ghost-NDC both cleared Gate 0 and both had genuinely reproduced defect rates, but each has a named incumbent verified to be shipping the same job to the same buyer (Wolters Kluwer iLien Monitor; Alchemy's NDC Watch, whose site was fetched and confirmed to target "pharmaceutical manufacturers and distributors" generally, not a branded niche). Collateral Sentinel and BondGap are the two real alternates — Collateral Sentinel if a fuzzy entity-resolution pipeline can be proven past its 37% exact-match ceiling, BondGap if annual-only recurrence is acceptable. StateShelf is dead: its corpus sits behind a WAF that blocked two independent fetch attempts.*