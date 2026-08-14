# COUNCIL — THE OPERATOR'S SEAT

> **VERDICT: SUSTAINABLE ONLY IF SCOPED DOWN.**
> **The single number: 21 hours** — the real cost of one 500-SKU job at job #10. **10,5× the 2,0
> assumed, and 1,75× the 12 hours she physically has inside a 48-hour window.**

---

## 1. The number that explains every other failure

> *"Every downstream failure is that one number propagating: it makes the SLA impossible, it forces
> utilisation to 45%, it collapses 86 delivery hours into 32 committable ones, and it puts the
> ceiling at 1,5 jobs a month — **R$7.000 against a R$30.000 target.** Cut the scope and the same
> number becomes 11. Nothing else in the business has to change."*

**And the build is 480 hours — 5,5 months at 20 h/week before the factory works at all.** I had not
priced that anywhere.

### The bad Tuesday, timed (500 SKUs, mixed encodings, scanned PDF, `IMG_2841.jpg`)

| Step | Hours |
|---|---|
| **PDF → table → join to CSV** | **3,5** — *"becomes 12 h when the supplier code is formatted differently in the two files"* |
| **Image → variant linking** | **3,0** — *"the most under-estimated step in the whole plan."* ~900 files, no metadata, 8 s each |
| Variant family reconstruction | 2,5 |
| Attribute review (flagged only) | 2,0 |
| Everything else | 10,3 |
| **Total** | **21,3 h** |

> *"When it goes wrong she has exactly two moves: eat the hours, or renegotiate mid-job in writing
> with a customer who has already paid. **There is no third option, because there is no colleague.**"*

## 2. The QA problem — solved, by abandoning sampling

**It corrected the red team's arithmetic in our favour.** Split the 4.000 values by *how they were
produced*:

| Class | Share | Mechanism | Residual error |
|---|---|---|---|
| Copied verbatim (GTIN, price, brand, SKU) | 40% | GS1 mod-10 check digit, price band, brand ∈ known set | **0,2%** |
| Rule-derived (units, case, crosswalk) | 25% | Range, enum, crosswalk-hit checks | **0,3%** |
| **LLM-extracted** | **35%** | *This is the only slice where 91% F1 lives* | **~126 wrong, not 360** |

**Four levers, ranked by hours saved per dollar:**

1. **Deterministic validators on every row** — eliminates 65% of values from human review. Near-zero cost.
2. **Cross-field consistency** — *"Size: XL" on a coffee mug; a dimension of 4.500 cm.* Extraction errors are usually type-wrong or range-wrong, not plausibly-wrong. **Catches ~40–50% of LLM errors deterministically.**
3. **Dual-pass agreement** — two extractions, different prompts, flag disagreements. **$0,80–1,60 per job. The single best hours-per-dollar lever in the design.**
4. **Provenance-or-blank** — every extracted value cites file, page and offset, or ships empty. *"Converts an unbounded error class (hallucination) into a bounded blank class."*

**Flagged queue ≈ 150 values ≈ 1 hour.** Compute is never the constraint — *"her eyeballs are."*

### The liability insight that should govern the whole product

> **"A blank required attribute fails at import — visible, immediate, cheap. A wrong attribute goes
> live, is invisible for months, and produces listing suppression and account-health damage — the
> failure mode that generates the dispute she cannot survive.**
> **Blanks are a KNOWN failure. Wrong values are an UNKNOWN one."**

So: **sell a process guarantee, not a sample guarantee** — *"every populated value cites its source;
everything unsourced is blank and enumerated."* Ship the blanks as a **Completeness Report** and
sell filling them as a separate priced pass. **The downgrade becomes a second product.**

## 3. Two arithmetic corrections

**Job size that maximises hourly rate: 700–800 SKUs** — the largest that fits one delivery slot.
Fixed overhead **3,4 h/job** regardless of size; variable **0,0152 h/SKU**.
**The $149/50-SKU tier earns $35/h against $124/h. Kill it or make it fully self-serve.**

**And the flat-cost assumption is not optimistic — it is inverted.** Dedup work scales with *pairs*:
**500 records ≈ 2.750 candidate pairs; 2.500 records ≈ 73.800. Five times the records, twenty-seven
times the pairs.**

## 4. The 48-hour promise costs her half the business

21 hours of work must fit inside 48 clock hours, in which she has **12 hours of capacity**. It
forces ~45% utilisation to stop the queue exploding.

> **Two booked delivery slots a week instead. Utilisation 45% → 80%. Committable hours 32 → 69.**
> ***"A +115% revenue increase from changing a sentence on a web page."*** No code, no price change.

**And the intake audit is named the single most important structural fix:**

> *"Fixed price on unseen input is **an unpriced option written to the customer on their own data
> quality.**"* → **$99 paid intake audit, credited to the job.** It converts an 18%-probability
> 40-hour blowout into a priced line item and gives her written grounds to decline.

## 5. Does R$30.000 exist?

| Design | Jobs/month | Revenue |
|---|---|---|
| **As proposed** (6 channels, 48h SLA, $899/500) | **1,5** | **R$7.000** ❌ |
| **Scoped down** (Shopify only, booked slots, $1.290) | **6,3** | **R$42.200** ✅ |
| Scoped down, *even at the old $899* | 6,3 | **R$29.400** — *the scope cut alone nearly gets there* |

**Also flagged:** R$360.000/year is **precisely the ME ceiling** under Simples Nacional (MEI is
R$81.000). She needs ME with a contador from day one, and stands on the EPP transition line.

## 6. The ruthless cut

**KEEP — Shopify only**, for operational reasons rather than commercial ones:

> **Free partner dev stores let her dry-run every single job end to end without ever holding a
> customer login. That is her entire QA story, and it exists only here.** Import errors are reported
> per row and reversible. Amazon is the inverse on all four axes.

**KEEP — variant/SKU-family reconstruction + image-to-variant linking**, because *"the defect is
visible at import"* — the product page either shows the right six colourways with the right photos
or it does not. **Attribute-filling is the opposite: unverifiable, silently wrong, and exactly where
the 91% lives.**

**THROW AWAY:** Amazon, eBay and the European marketplaces (**−60% of build, −70% of maintenance**,
and every channel where a bad file damages the *customer's account*) · the scanned-PDF path entirely
· the 2.500 and 5.000 tiers (**2.500 SKUs ≈ 74 hours; delivering 74 hours inside 48 has no
solution**) · the 48-hour promise · fixed price on unseen input · *"missing attributes filled"* ·
dedup as a headline promise · the $149 tier.

### The resulting offer

> **Shopify Variant Rebuild** — up to 500 products (800 tier available), one CSV + one image folder,
> delivered into a booked slot. **$1.290.**
> **10,4 hours → $124/hour. Build 480 h → 190 h. Maintenance 26 → 8 h/month. 6,3 jobs/month.**

---

## 7. THE COUNCIL'S FIRST REAL DISAGREEMENT — and it is the central problem

| Seat | Price at 500 products |
|---|---|
| **The merchant** | *"I'd have guessed $200–400… I'd pay ~**$399** without agonising. $899 is agency money from a vendor with no agency behind it."* |
| **The operator** | **$1.290** — *"below this the factory does not clear R$30.000 at any achievable volume."* |

> **The buyer will pay $399. The factory needs $1.290. That gap — 3,2× — is the business's central
> problem, and no amount of positioning closes it by itself.**

**Three ways it could close, and the blue team must pick:**
1. **Cut the hours further** until $399 works — the operator's floor is ~11 h, so $399 is $36/h. Not enough.
2. **Raise the value** until $1.290 is obvious — which is precisely the merchant's own list: *press the import* (£2.500–3.000), *localisation* (£1.500+), *a monitor* (£50/month). **All three sit above the operator's number.**
3. **Change the buyer** — sell to whoever the £1,2M merchant is not.

**Note that the merchant and the operator agree on more than they disagree:** both kill the 48-hour
promise, both keep the $149 entry as a *test* rather than a business, both say the value is in
certainty rather than speed, and both point at the same trigger — a channel move or a migration.
