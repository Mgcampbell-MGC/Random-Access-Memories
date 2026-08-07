I verified all six candidates by direct fetch. Here are the results.

## 1. FETCH VERIFICATION

| Candidate | source_a | source_b | Verdict |
|---|---|---|---|
| **CertGap** | ENERGY STAR Socrata **200**, no key. 4,748 fridges / 748 DW / 394 CW / 538 dehum. 90 datasets total | DOE CCMS Solr **200** (needs browser UA). **4,595,423** records, **73** product groups, **7,227** distinct brands — all exact | **CONFIRMED, every number** |
| **990 Integrity** | IRS index_2025.csv **200**, content-length 93,053,080 | ProPublica **200**; EIN 364478169 = Illinois Legislative Black Caucus Foundation, FY2022 totrevenue **966,836** confirmed | CONFIRMED |
| **PublicFile Guard** | facility.zip **403** — Akamai "Access Denied" on `www.fcc.gov`, `enterpriseefiling`, `data.fcc.gov` from this network; `docs.fcc.gov` and `publicfiles.fcc.gov` return 200, so this is **my network being blocked, not a dead endpoint** | OPIF **200**. Folder IDs scrapeable from profile HTML (WNYC-FM Issues folder `7c37a2c3-…`); API returns `create_ts` per file — the "2014Q2 … stamped 2022-01-21" claim reproduces **exactly** | source_b CONFIRMED; **source_a UNCONFIRMED (network-blocked, not disproven)** |
| **LDA Reconcile** | **200** after redirect to `lda.gov` (needs `-L`). registrants count **17,440** confirmed | contributions **200**. Voegtlin id 46300 → count **0** for 2025; name search → 7 records, none after 2023 | CONFIRMED (counts differ from claim: Q4-2025 filings **27,155**, not 20,940) |
| **RangeGap** | Greenhouse **200**, Lever **200** | **Detector is broken — see below** | **source_b INVALID** |
| **Provider Record** | NPPES **200** | CMS DAC **200**, count **3,387,942** confirmed | CONFIRMED |

## 2. D3 — AND ONE KILL

**RangeGap dies, on verified grounds — two independent failures.**

Its flagship named defect does not reproduce. I fetched Vivvi job **7595127003** ("Head Preschool Teacher (2-Year-Olds)", New York City). The ad body contains **"Competitive hourly pay: $23–$29.40 per hour"** — while `pay_input_ranges` is `[]`. All 6 Vivvi NYC ads disclose a range in the body. The candidate's rule that "Greenhouse-hosted pages are safe to judge from the API alone" is **false**; `pay_input_ranges=[]` carries almost no signal. Its "11/11 confirmed" evidence is therefore 11 unconfirmed flags, and the 31% rate is built on it. The remaining flags at Dotmatics were **"Remote - United Kingdom"** (not a covered jurisdiction — a loose `remote` regex matched it) and **"Join our Talent Community!"** (not a requisition).

Second, independently: the finding is *"this ad violates NYC LL32"* — a legal conclusion needing borrowed authority. That is the exact pattern the brief says killed a candidate last round. **STRUCTURAL. Killed.**

Everyone else passes D3. CertGap passes cleanest: if one federal record says 249 kWh and the other says 354 kWh for the same model number, they cannot both be right — that is arithmetic, not legal opinion. Sol should **drop the DOE-penalty sentence** from the email; it is secondary-sourced garnish that imports authority she doesn't have, and the two numbers don't need it.

## 3. T4 / 4. T6

No candidate dies on T4 — in all six the buyer doesn't know. For CertGap specifically: DOE and EPA share **physical verification test results**, not database-consistency comparisons, and DOE "validates every CCMS submission primarily as a check for basic compliance with data requirements" — format, not cross-reference against ENERGY STAR. **No free official cross-validator exists. T6 survives.** No commercial incumbent surfaced.

## 5. I REPRODUCED CERTGAP'S CORE MEASUREMENT — IT CAME OUT BETTER

I ran the join myself (exact normalized model-string match, both DOE model fields):

| Category | Matched | Mismatch | Rate |
|---|---|---|---|
| Refrigerators | 2,336 | 145 | **6.2%** |
| Dishwashers | 466 | 27 | **5.8%** |
| Clothes washers | 279 | 17 | **6.1%** |
| **3-cat combined** | **3,081** | **189** | **6.1%** (claim was 5.3%) |
| Dehumidifiers (my 4th category) | 329 | 32 | **9.7%** |

Two of the candidate's named examples reproduce exactly: **Avanti AV1081VFK0W, 249 kWh (ENERGY STAR) vs 354 kWh (DOE)**, and **Hisense WF5S2845BW, IMEF 2.92 vs 1.84**. Two do **not**: the Bosch SHX78DC** case is an *internal ENERGY STAR duplicate* (two ES rows, 215 and 240; DOE says 240, agreeing with one), and the Maytag case compares **MHW5630H\*\* to MHW5630M\*\*** — two different models, not a contradiction.

**Two findings that change the picture, both against the candidate's own stated fears:**

- **The defect concentrates in card-payers, not legal departments.** Mismatch brands are overwhelmingly small importers and private labels: Summit (12 big-delta), Commercial Cool, Premium Levella, Avanti, Zephyr, Insignia, Vissani, Criterion, Icebox, Upstreman, Waykar/Kesnos/Yaufey. Exactly **one** Whirlpool record and **one** LG across everything. The candidate's "routes to legal at giant brands" worry is refuted by the data.
- **Large deltas defeat the "databases just lag" brush-off.** 72 findings across 4 categories carry deltas too big to be version skew — Zephyr 69 vs 330 kWh, Premium Levella 314 vs 493, Commercial Cool 286 vs 429.

**Demoted, not killed:** 990 Integrity (1.7%, annual, $250 nonprofits — fails on X, the most valuable axis, by its own measurement). Provider Record (20/20 naive mismatch = ambient, not scarce; incumbent credentialing vendors = real T3 pressure). LDA Reconcile (the API has **no global person identifier** — lobbyist IDs are registrant-scoped, so every flag needs name dedupe with real false-positive risk; and the Senate sends its own noncompliance letters, so the buyer learns free eventually).

**PublicFile Guard is the genuine runner-up** and the only one I'd hold in reserve: quarterly-by-statute is the best repeat structure in the set, and I verified the OPIF timestamp mechanism works exactly as described. I am not picking it because **I could not reproduce its load-bearing number** — the 57% defect rate depends on station enumeration I couldn't reach. That is a blocked network, not a dead source, so this is a discount, not a kill.

---

# COMMIT: CertGap

**What it is.** Every appliance brand sold in the US files its energy numbers twice with the federal government — once to get the ENERGY STAR label, once to certify compliance with DOE. Both are public, both were filled in by the same manufacturer, and they routinely disagree; CertGap is a pre-computed PDF showing a named brand, model by model, exactly where its own two federal filings contradict each other.

**The defect, as the cold email says it:**

> The federal ENERGY STAR database lists your Avanti AV1081VFK0W at **249 kWh/year**. Your own DOE compliance certification at regulations.doe.gov lists the same model number at **354 kWh/year**. Both links are below — they're your filings, not mine. I found 5 more like it across your line.

**Verified list size and how I counted it.** 7,227 distinct brand names, counted by Solr facet `numBuckets` on `Brand_Name_s__s` over 4,595,423 records in 73 DOE product groups (fetched, HTTP 200). Brands roll up to fewer owning companies — realistically 2,000–4,000 [UNKNOWN, I did not resolve ownership]. **The number that actually matters is the pre-qualified pool: 46 brands with ≥1 mismatch and 21 brands with ≥1 large non-explainable delta, from just 4 of 73 categories, computed by me.** Extrapolating to ~15–20 workable overlapping categories suggests a few hundred pre-qualified named prospects — not thousands. I am stating that plainly because it is the real constraint.

**Price and honest volume.** $650 for the initial brand audit, $350/quarter monitoring. At $650 pure one-off that's 12–13 sales/month, which the pre-qualified pool will not sustain for long. The business only works as the subscription: **~60 recurring customers at $350/quarter ≈ $7,000/month**, plus new initials. Reaching 60 requires the category expansion, not just the 4 I tested.

**Does it beat ADV-Check?**
- **X (repeat) — YES, and this is the reason to pick it.** DOE CCD updates roughly biweekly and holds only models certified within the past year; certification is required per model *annually* plus on any redesign; brands ship new SKUs continuously across up to 73 product groups. Quarterly monitoring is honest here. ADV-Check is annual per firm.
- **Y (list) — NO, it loses.** A few hundred pre-qualified prospects vs ADV-Check's 15,445 advisers with websites.
- **Z (price) — TIE at $650**, unproven both ways.
- **Bonus, and it matters most: it retires ADV-Check's W3.** ADV-Check's mismatch rate is unmeasured and could be 5% or 0%. CertGap's is **measured at 6.1–9.7% by independent reproduction**, stable across four unrelated categories.

So: a real improvement on the most valuable axis plus the biggest unknown de-risked, at the cost of a smaller universe.

**Cheapest test — under 2 weeks, under $200.** Expand the join from 4 to ~12 overlapping categories (free, one day of compute), then **hand-verify the top 40 big-delta findings to strip the two artifact classes I found** (internal ENERGY STAR duplicates; model-family suffix collisions), and email those 40 named brands with two values and two links, penalty language removed. Cost: sending domain + one inbox, ~$20–50. **Pass: ≥4 replies that engage with the numbers (10%) and ≥1 paid $650 within three weeks.** Below 2 replies and zero sales, fall back to PublicFile Guard — and test its enumeration from an unblocked network first.

**Weakest link, one sentence.** The headline 6.1% is inflated by artifacts — two of the candidate's own four named examples turned out to be an ENERGY STAR internal duplicate and a model-family confusion rather than genuine contradictions, so the clean quotable rate is likely 2–4% and every report needs manual curation before it goes out.