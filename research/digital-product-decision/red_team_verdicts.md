## RED TEAM VERDICTS

I re-verified the load-bearing claims myself. Two of them were wrong in ways that matter — one against a candidate, one **in favour** of the top candidate. I also caught and corrected a false kill of my own mid-analysis.

---

### 1. ANNEXCHECK — **STRUCTURAL-KILL (A5, reinforced by R4)**

**BUCKET A fact.** A Responsible Person is *legally mandatory* — "Selling cosmetics without a Responsible Person is illegal in the EU and UK" — and RP service is published at **£490/year for EU (up to 5 products), +£200/year to add UK** [VERIFIED, https://euverify.com/eu-uk-responsible-person-for-cosmetics/]. The RP's contracted scope already includes **"ongoing horizon scanning for new legislation, guidance, and data that impacts product compliance"** [VERIFIED quote, https://www.cosmesure.uk/uk-and-eu-responsible-person-service], plus cosmetovigilance and liaison with competent authorities. Industry RP offerings are described as including "complete post-market surveillance… an annual report on any regulatory changes which might impact you or your products" [PLAUSIBLE, search aggregation].

So the target buyer cannot *not* buy the substitute. ANNEXCHECK's entire deliverable — "which of my SKUs dies on which date under the annexes" — is the contracted output of a legally compulsory service costing about the same money, delivered annually rather than once. That is A5 literally: a substitute at comparable-or-lower cost doing the whole job. Two segments, no third: a brand selling into the EU/UK **must** retain an RP whose job this is; a brand not selling into the EU/UK **does not need the product at all**.

R4 compounds it rather than standing alone: the RP is a named legal role and the Art. 10 safety assessor is a qualifications-gated one. Even a correct ANNEXCHECK report must be re-blessed by the credentialed party before the brand acts — so the artefact does not finish the job, which is the whole premise of the format ranking.

Two further nails, both already in the verification pass: the headline dated triggers are **in the past** as of today (Omnibus VIII applied 1 May 2026; allergen phase 1 was 31 Jul 2026), and the enumeration list fails R7 — Cosmoprof's directory is registration-gated and the 10times mirror returns 403.

Do not resurrect this one.

---

### 2. DeckProof — **UNPROVEN-TESTABLE. Ranked #1. This is the angle I commit to.**

I did the work the verification pass left undone, and the result flips in DeckProof's favour.

**The trigger is real, and better than the brief claimed.** The seller roster is public at an undocumented parameter:

```
https://ecrm.marketgate.com/Sessions/2026/10/LatinAmericaBeautyPersonalCare/Attendees?rt=S&a=1
```

HTTP 200, no login [VERIFIED by direct fetch]. It names supplier brands — Beauty Creations Cosmetics (US), Timeless Skin Care LLC (US), Ordo (England, UK), Coscentra BV (Netherlands), Parsa Beauty (Germany), Industrias Beter (Spain) — for a session on **25–28 Oct 2026, eleven weeks out**. The default `/Attendees` view shows only *buyers*, which is exactly how this could have been mis-scored as another RangeMe (names the retailer, never the supplier). It isn't. `rt=S` is the seller roster.

**I enumerated the whole calendar** [VERIFIED, script at `/tmp/claude-0/-home-user-Random-Access-Memories/9aef20de-742c-52a2-b11a-a33d815230ea/scratchpad/ecrm2.py`, output `ecrm2.out`, data `ecrm_rosters.json`]:

- 93 sessions on the public calendar (Aug 2026 – Sep 2027)
- **15 sessions have published seller rosters; 78 read "Attendees will be posted in the near future"** — rosters appear roughly 1–6 months ahead, so this is a rolling stream, not a one-off
- **475 unique named seller companies right now — and 473 of them carry a clickable company website in the roster markup** (`<a href="http://www.21stcenturyvitamins.com">21st Century HealthCare, Inc.</a>`)
- Country mix: 292 from US-domestic sessions, 70 explicitly USA, 58 EU, 25 UK → **~445 of 475 are USA/UK/EU addressable**

**A correction to my own analysis, stated because it nearly caused a false kill:** my first parser required a `(Country)` suffix, which US-domestic sessions omit. It returned "sellers=0" for every US session and I was one step from killing DeckProof on volume. Manual inspection of `VitaminDietSportsNutrition` showed a full roster (21st Century HealthCare, AceBiome, ACEND, Advocare, AN Supps…). The zeros were my bug. **The brief's ~2,400–4,800 triggered brands/year estimate is approximately right**: 475 visible from 15 sessions ≈ 32/session × ~80 sessions/yr ≈ **2,300–2,600 named, domained, dated brands/year**.

**BUCKET B — the volume gap, with numbers.** ECRM alone does not reach target. 192 sales/yr at $497 against 2,400 triggered = **8% conversion required**, against the brief's own triggered benchmark of 1.5–3%. At 2–3% ECRM alone yields 48–72 sales/yr = **$24k–36k/yr**. Sending is *not* the constraint (200/month against 600–1,000 capacity) — list size is. Fix: price at **$750** and add a warm tier (below).

**BUCKET B — the substitute the verification pass missed: brokers.** "Food brokers handle approximately 80% of all product introductions to major retailers," and the sell sheet "is the document that travels into every buyer meeting your broker has on your behalf," carrying pack size, case configuration, SRP, wholesale cost and margin offer; brokers take 3–7% of net wholesale, so they are commission-motivated to sanity-check the economics for free [PLAUSIBLE, https://www.foodbevy.com/the-ultimate-guide-to-cpg-brokers/, https://www.jdallthomas.com/blog/retail-launch-checklist-cpg-brands]. **This mostly defuses itself against this specific list:** ECRM's model is brands paying $7,000–16,900 to sit down with buyers *directly*. The roster is self-selected for brands going direct rather than through a broker. But it caps any widening into general "CPG brands" — outside the ECRM roster, 80% have a free human doing the sanity check. *Test:* in the 200-email test, track how many replies say "my broker handles this." KILL-SIGNAL: >30% of replies.

**BUCKET B — the parser. This is the only question that matters first.** Indie decks are Canva/InDesign exports; numbers sometimes live in flattened images pdf.js cannot read as text. If extraction fails on a third of real decks, the deterministic R3 defence collapses into a paste-your-numbers form.

**BUCKET B — ECRM's Terms of Use, stated precisely** [VERIFIED, https://ecrm.marketgate.com/UserTerms, last updated 13 July 2020]. Prohibited: "(vii) engages in data mining or similar data gathering or extraction activities or retrieve data or other content from the ECRM Services for purposes of creating or compiling that content"; "(viii) accessing, using, or copying any portion of the ECRM Services… through the use of indexing agents, spiders, scrapers, bots, web crawlers, or other automated devices"; "(vi) harvests or otherwise collects information about others, including names, e-mail addresses, other contact information… without their consent." This is broader than Expo West's clause and it covers the intended use. It is contract, not law, and there is no login and therefore no clickwrap assent — but it means: **do not build automated scraping infrastructure on ECRM.** Read ~30 names off a public page by hand per session (a human reading a web page is not a spider), take the company website from the roster link, and source the *person* from Apollo or the company's own site so no contact data is ever taken from ECRM. Practical downside is an IP block or a letter, not meaningful exposure for a Brazilian CNPJ.

**R3 — honest in both directions: passes.** Recomputing retailer margin, case/pallet math and promo math across a 30-slide deck and a workbook, and cross-checking every figure appearing in both, is arithmetic across long documents — measurably unreliable from an LLM, and a confidently wrong margin recited to a Kroger buyer is worse than no answer. The retailer-requirements corpus is a genuine bundled dataset. And COGS is confidential, so the prompt route requires pasting your cost sheet into a chatbot. **R4: clean — this is the only candidate whose authority rests on nothing.** The output is self-verifying: the buyer can check the arithmetic themselves. That is decisive, because R4 is the axis that killed the most candidates. **Approval threshold: clean** — the ECRM attendee at a 5–50 person brand is the founder, who owns the card, and $750 against a sunk $7,000–16,900 is not a procurement event.

**Second-order trap, honestly:** the five figures are *already sunk*, so what is avoided is the wasted value of a meeting, not a new cost. That is a weaker anchor than a fine — but stronger than it looks, because the numbers *are* the substance of the pitch (retailers expect 30–38% gross margin on shelf-stable, and the economics span MSRP, wholesale, retailer margin, distributor margin, broker commission, freight, promotions and deductions — abundant room for internal inconsistency). Whether founders pay to remove that risk is Bucket B, tested below.

---

### 3. LICENCEPROOF — **UNPROVEN-TESTABLE. Ranked #2. Best physics in the set, worst credential exposure.**

**Physics are the best of all six.** I parsed the register on disk [VERIFIED, `sponsors.csv`, 10.9MB]: 142,712 rows, **127,241 unique organisations**, 122,771 Skilled Worker rows. At ~1,000–2,000 new sponsors/month the trigger stream *exceeds* one domain's sending capacity — meaning conversion can land at the low end and still work: 700 emails/month × 12 × 1.5–3% = 126–252 sales/yr = **$63k–125k/yr at $497**. No seasonality. Urgency is stronger than the brief claimed: 3,000+ revocations in 2025 and 1,917 employers losing licences between 13 Feb and 20 Apr 2026 — ~29/day [PLAUSIBLE, tarve.co.uk blog + Russell-Cooke analysis; not primary Home Office data].

**BUCKET A checks — all pass.** The list exists and is free. s.82/s.84 Immigration and Asylum Act 1999 confirmed: the restriction bites only on advice "relating to a particular individual," so generic published templates are lawful.

**BUCKET B — the enrichment tax, which the brief understated.** The register carries **exactly five fields: Organisation Name, Town/City, County, Type & Rating, Route** [VERIFIED by parse]. No company number. No website. No contact person. No grant date. So: (a) the trigger date must be manufactured from Sol's own daily diffs, meaning **she has zero history today and the outbound stream starts empty**; (b) every single record needs domain resolution from a bare name plus a town ("ALT, Glasgow"), which is materially harder than the GPG register's company-number-keyed rows; (c) no person at all. *Test:* take 100 organisations that are new in a 7-day diff, attempt domain + HR-contact resolution via Apollo; PASS = 60+ resolved to a plausible named HR/ops contact at under $0.50/record.

**BUCKET B — the substitute the verification pass missed, and it is the strongest substitute in the whole set.** IAS (a credentialed immigration firm) gives away a free, email-gated **10-section Home Office compliance audit checklist that includes an Action Plan template and an Internal Audit Summary with Low/Moderate/High risk ratings** [VERIFIED, https://iasservices.org.uk/uk-home-office-compliance-audit-checklist-template/]. That is uncomfortably close to LICENCEPROOF's core, from an authoritative source, at £0. Also newly found: **Rakenne ships a "UK Sponsor Licence Auditor"** — record-keeping, SMS reporting, visa-expiry monitoring, plus SOC-code and salary-threshold validation — as a Claude Skill inside their SaaS [VERIFIED, https://rakenne.app/skills/sponsor-license-auditor/]. Not identical (upload-based SaaS), but the space is being entered. What the free checklist cannot do: filled templates, deterministic 10/20-working-day SMS deadline arithmetic, automated gap scoring, version-dating to a specific guidance release. Real gap — but narrower than the brief assumed.

**The reason I rank it below DeckProof: R4 asymmetry.** In sponsor compliance the buyer's purchase criterion *is* authority, because the downside is existential (revocation curtails every sponsored worker's visa). Sol is selling a $497 anonymous download into a market whose ceiling is a credentialed £4,500 audit (A Y & J "Compliance Shield" [VERIFIED]) and whose floor is a *free credentialed checklist*. Buyers under existential fear buy credentials. That is not a Bucket A kill — it is a genuine, testable willingness-to-pay question — but it is the exact structural disease the filter set exists to catch, and DeckProof does not have it.

*Test (as designed, sound):* 4 weeks, <$150. 200 companies new in the register diff, free 2-page "the 10 records UKVI asks for on day one," $497 pack. PASS = 3+ card purchases; secondary PASS = 15%+ free-PDF download rate.

---

### 4. PAYGAP FILEKIT — **UNPROVEN-TESTABLE. Ranked #3. Best list in the set; weakest reason to buy.**

**The list is extraordinary and the brief undersold it.** I parsed both CSVs [VERIFIED, `gpg2025.csv` / `gpg2024.csv`]. Every count in the brief is exact: 11,163 filers, 8,109 in the target bands, 655 late, 46.6% with no narrative link. But nobody noticed the `ResponsiblePerson` column:

- **6,996 of 8,109 target-band employers (86%) name the individual who signed the statement, with job title** — "Julie Barrett (HR Manager)", "Azhar Farooq (Head of Payroll)", "Tracy Channell-Napier (Group Finance Director)"
- Title mix: **42% HR/People/Reward, 24% owner/exec, 19% finance/payroll**
- 7 rows even publish the person's email outright
- Plus company number, postcode, SIC codes, DueDate, DateSubmitted, late flag, and **9 years of history for a benchmark corpus**

This is the only candidate where the free list names *the person with the problem and their job title*, and where ~24% of those people are directors who can obviously card $497. It answers both the "person not company" test and the approval-threshold test better than anything else here. Volume also fits: 8,109 × 2–3% = 162–243 sales/yr = **$80k–121k/yr at $497**, and 8,109 sends/yr ≈ 676/month, almost exactly one domain's capacity.

**BUCKET B — the second-order trap, and it is real.** The dated deadline exists; the penalty does not land. The EHRC issued **~1,900 warning notices across the 2023–2025 deadlines and imposed not a single fine**, and confirmed it "did not take formal enforcement action" [PLAUSIBLE→strong, https://www.lewissilkin.com/insights/2026/03/26/gender-pay-gap-reporting-enforcement-zero-fines-to-date-but-rising-checks]. 655 companies filed late in 2025-26 and nothing happened to them. So "avoid a fine" is an empty anchor and must not be the pitch. The salvageable framings: (a) EHRC wrote to 30 employers in 2024 and 42 in 2025 about *data accuracy* — small but the only real fear population; (b) **the honest value is the narrative and peer benchmark**, which 3,984 target-band filers currently publish nothing for — a "help me look good to my board" purchase, not a compliance-fear one. Reframe or the price will not hold against the £99 calculator.

**BUCKET B — seasonality is a physics constraint, not just an inconvenience.** The 2026 cycle closed in March; the next deadline is **5 April 2027**. Concentrating 8,109 sends into a Jan–Apr window is ~2,700/month, well above one new domain's 600–1,000. Needs 3–4 warmed domains, or a Nov–Apr ramp. Cheap to solve, but it must be planned, and **there is no revenue from this candidate before roughly January 2027.** That alone disqualifies it as the first test.

*Off-cycle test available now:* 690 employers filed in 2024-25 but not 2025-26, and 655 filed late [both VERIFIED by parse] — segments emailable today with a personalised opener citing their actual `DateSubmitted`. PASS = 3+ paid pre-orders per 150 emails.

---

### 5. BidProof — **UNPROVEN-TESTABLE. Ranked #4.**

**BUCKET B — the trigger is weaker than labelled, and this is the specific distinction the task asked for.** Find a Tender shows *authorities* publishing dated deadlines, and *award notices* naming past winners. The proposed email — "a tender in your CPV category closes on date X" to a company that won a category-X contract before — is **"I can see this company does this kind of work" plus a public date that may not apply to them**. It is not "I can see this company has this problem on this date." Reclassify from visible-dated to **invisible-but-high-frequency** (R6 permits this, as a standing-presence business: SEO plus one memorable email plus a free artefact — not dated outbound). Volume and sending physics are comfortable either way.

**BUCKET B — R5 heterogeneity is the live risk.** Every authority formats its pricing schedule differently; if per-tender configuration exceeds 30–45 minutes, the product breaks its own rule. *Test as written is good:* download 5 real ITT + pricing-schedule packs (free, no login), build, time the configuration. PASS = <30 min config AND 3+ genuine findings on a realistic mock submission.

Credit where due: the substitute analysis here was the best in the pack. Lucius AI's free checker does narrative compliance only, human bid reviewers cost £250–800/day (more, not less, than $597), and the deterministic pricing-workbook recompute has no found substitute at any price. R4 clean, second-order anchor genuinely real (arithmetic slip → disqualification or being bound to a wrong price). It is a legitimate #2 build after DeckProof; it is not first because the trigger will not carry dated outbound.

---

### 6. PACKCHECK — **UNPROVEN-TESTABLE, but volume-capped. Ranked #5. Cannot be the primary business.**

I parsed the register on disk [VERIFIED, `register.csv`, "Report created at 11:35 PM on 05 Aug 2026"]: 11,823 rows; 11,072 Large; **1,906 with no compliance scheme, 1,733 Large-and-direct**; of those, 261 flagged "Required to pay disposal fee = Yes", 403 "Subject to recycling and certification obligations = Yes", **438 with either**. Scheme concentration is heavy (Valpak 2,707, Wastepack 1,623, Beyondly 1,100).

**Do the division.** 192 sales/yr needs **11% of the 1,733 direct registrants, or 44% of the 438 fee-exposed**. The brief already ruled BuyerRoom "not plausible" at 25–80% penetration — 44% sits inside that dead band, and 11% is 4–7× the 1.5–3% triggered benchmark. Realistic ceiling: 1,733 contacts × 2 deadline cycles × 2–3% ≈ 35–70 sales/yr ≈ **$17k–35k/yr**. Widening to all 11,072 large producers restores the arithmetic but destroys the premise, because scheme members submit their data *to the scheme*, which handles the portal — the file-preflight has no purchase for them.

Not a kill: the register is the cleanest enumeration asset here (company numbers included), the semiannual trigger is regulator-published and permanent, and the fee anchor is real money. But it is a **portfolio product at roughly a third of target**, and it should not be tested first. The one free check worth doing regardless: confirm the 1 Oct 2026 deadline and the 1.2×/1.6×/2.0× modulation schedule against the primary PackUK PDF — currently PLAUSIBLE only.

---

## RANKED

| # | Candidate | Verdict | Binding constraint |
|---|---|---|---|
| 1 | **DeckProof** | UNPROVEN-TESTABLE | Parser reliability; then volume → needs a warm tier |
| 2 | LICENCEPROOF | UNPROVEN-TESTABLE | R4 trust vs free credentialed checklist; enrichment from a 5-field list |
| 3 | PAYGAP FILEKIT | UNPROVEN-TESTABLE | Toothless enforcement; no revenue before Jan 2027 |
| 4 | BidProof | UNPROVEN-TESTABLE | Trigger is high-frequency, not dated; R5 setup time |
| 5 | PACKCHECK | UNPROVEN-TESTABLE (capped) | List too small: ~$17–35k/yr ceiling |
| 6 | ANNEXCHECK | **STRUCTURAL-KILL** | A5: mandatory RP at £490–690/yr already does the job |

**All unproven. None is dead except ANNEXCHECK. Here is the one I would test first and why.**

---

## THE STRONGEST VERSION OF DECKPROOF — not as designed

Seven changes, each earning its place:

1. **Price $750, not $497.** Top of band, 11 sales/month. The anchor is the $7,000–16,900 the brand has *already wired* for a 10–20 minute meeting. A 4–9% insurance premium on a sunk five-figure cost is easier to justify than $497 is, and $497 leaves a third of the revenue on the table for identical work. It also cuts required penetration from 8% to 5.5%.

2. **Reposition from audit to pre-meeting pack.** Do not sell a critique. Ship three things: the findings report, **a corrected one-page buyer-facing economics sheet** (SRP, wholesale, retailer margin, case/pallet config, promo math) formatted the way retailers ask for it, and a per-retailer required-fields checklist. Buyers pay more for a document they carry *into* the room than for a list of their mistakes.

3. **Wedge on supplements/HBC first.** `VitaminDietSportsNutrition` has a published roster of ~100+ named sellers with domains [VERIFIED], and supplements carry the nastiest combination of margin tiers, case-pack math and claim-substantiation fields. Worst math = most findings = most provable value.

4. **The corpus is the moat, so build it as the product.** Retailer-required sell-sheet fields and margin norms by channel, compiled from public supplier guides. This is what a prompt does not contain, what makes "31 checks" credible, and what justifies an annual edition. Confirm all six retailer guides are freely obtainable *before* naming them in copy (only Walmart's is currently PLAUSIBLE).

5. **Two-tier list.** HOT = ECRM published seller rosters (~2,400/yr, dated meeting, sunk five figures, domain supplied). WARM = public exhibitor lists — Expo West, Fancy Food, KeHE, Cosmoprof NA (~8,000–12,000/yr, named and dated, lower intent). Manual reading only on ECRM, per its ToS.

6. **Give away a single-page local-HTML margin & case-pack checker, free.** It proves the mechanism in 30 seconds, makes the cold email a gift rather than a pitch, and builds the standing-presence half that survives if outbound conversion disappoints.

7. **Repeat purchase:** per-retailer editions (Walmart, Ulta, Kroger) plus an annual corpus refresh.

## THE ONE THING TO TEST FIRST

**The parser — not willingness to pay.** Everything downstream is conditional on a deterministic engine actually reading numbers out of real CPG sell sheets. If it cannot, the product becomes a data-entry form, the R3 defence evaporates, and no amount of pricing work saves it. It is also the only question that costs $0 and the only one Sol's build speed makes nearly free.

**Test, days 1–5, cost $0.** The 473 company domains I already extracted (`ecrm_rosters.json`) are a ready corpus of real triggered brands — pull 20 public sell sheets/one-pagers/line-review decks from their own sites. Build the pdf.js + SheetJS extraction inside the single inline classic `<script>`. **PASS = clean numeric extraction of SRP, wholesale, case pack and margin on ≥15 of 20 with no manual correction, AND ≥1 genuine arithmetic discrepancy found across the 20.** Fail at ≤12/20 → stop and switch to LICENCEPROOF.

**Then, days 6–14, cost under $200.** 200 hand-read named sellers from the published Aug/Sep/Oct 2026 rosters. Subject line names their actual session and date. Free checker as the opener, $750 as the price. Domain ~$12, Resend free tier or ~$20, Apollo credits ~$50–100. **PASS = 2+ paid presales, or 6+ replies asking price, in 14 days.** Watch for the two kill-signals: >30% of replies saying "my broker handles this," and any reply saying the numbers are already checked by the retailer's own portal.

## WHAT WOULD HAVE TO BE TRUE FOR $7,400–8,300/MONTH

11 sales/month at $750, or 16 at $497. Given a verified ~2,400 HOT named/dated/domained brands/yr plus ~8,000–12,000 WARM exhibitor-list brands/yr, and 2–3 warmed domains at ~700 sends/month each: **3% on HOT (72 sales) + 1.5% on WARM (120 sales) = 192 sales/yr ≈ $12,000/month at $750, ≈$8,000/month at $497.** Both conversion rates sit inside the brief's own triggered band rather than above it, and the sending arithmetic fits inside what one faceless operator with a few warmed domains can physically send.

So: **plausible, not certain.** ECRM alone is a $24–36k/yr business — worth launching, not target. Target requires the warm tier, and the warm tier is where the broker substitute bites. That is the real open question, and the $200 test measures the leading indicator of it in fourteen days.

**Commitment: build the DeckProof parser this week against 20 real sell sheets. If it clears 15/20, run the 200-email test against the published October rosters before they go stale — the Oct 25–28 window closes in eleven weeks.**