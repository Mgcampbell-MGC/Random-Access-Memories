# COUNCIL — THE COMPETITOR'S SEAT

**Seat taken: the operator of Matrixify.** Riga, 8 people, ~$880K revenue, no funding, 4,9 stars
over 1.021 reviews, $20/month. *"That seat gives the sharpest attack because I am the thing she is
positioning against, and because my constraints are real."*

> **VERDICT: SHE IS A THREAT IN A NARROW SEGMENT.**

---

## 1. He will not compete for it, and he says why

> *"To deliver her service I need a human who understands apparel sizing and Amazon product-type
> schemas. In Riga that's €3.500–4.500/month loaded, ~$55.000/year… That's a ~50% gross-margin
> services line bolted onto an 85%-margin software business. It drags my blended margin, it creates
> a hiring dependency, and it consumes the founder's time. **I will not build it. That decision is
> exactly the door she walks through, and I want the council to see that I'm making it deliberately
> rather than out of ignorance.**"*

### Where he does not compete — the seven exclusions

1. Anything that isn't Shopify. 2. **Pre-migration — *"a merchant leaving Magento has a Magento
export and no Shopify store. That's a window of days to weeks where I am structurally
unavailable."*** 3. Anyone who won't install an app. 4. Under ~200 products. 5. Non-English support.
6. **The genuinely filthy file — *"my honest answer is 'clean it up and come back.' I want files that
are almost right."*** 7. **Any engagement where he's accountable for a business outcome.**

> **"Stack those and you have her address: a non-Shopify or pre-Shopify merchant, 200–5.000 SKUs,
> with a genuinely filthy file, who cannot or will not install an app, and who needs a person to be
> accountable for the result. That is a real place. It is smaller than she thinks. But nobody in my
> seat is standing on it, and I'm not coming."**

## 2. The market, sized from inside it

| Filter | Rate | Remaining |
|---|---|---|
| Merchants worldwide, 500–10.000 SKUs | — | 400.000–500.000 |
| Catalogue crisis this year (replatform, supplier change, channel launch, ERP swap) | ~12% | 55.000 |
| Severe enough that the file genuinely won't import | ~35% | 19.000 |
| Nobody in-house, no agency, no developer cousin, no VA will just do it | ~50% | 9.500 |
| **Will email their whole catalogue to an anonymous stranger and pay by card before speaking to a human** | **5–10%** | **500–950/year** |

**$450K–850K of total addressable spend annually. At a realistic 10–20% share: $45K–170K/year
against a $69.360 burn.**

> *"**The market is big enough for her and only for her.** It supports one person comfortably and a
> second marginally. It does not support a company — **which is exactly why nobody in my seat has
> taken it, and exactly why it's still sitting there.** That's not a dismissal. A business that
> reliably clears $120K on a $69K cost base is a good business. **It's just a job with unusually
> good margins, not a market.**"*

**The number to stress-test above all others is that last filter.** *"At 20% this is a $1,5M market
and I would have to think much harder. At 2% there are 150 buyers on Earth per year."*

## 3. The judgement claim — conceded as genuinely hard, then blunted three ways

**He refuses to dismiss it:** *"Plainly: it is genuinely hard. Harder than a fortnight. I'm not
going to pretend otherwise, because pretending is how I'd lose to it."*

- **[WDC Products benchmark](https://arxiv.org/html/2301.09521):** best systems reach **72–80 F1** on corner cases.
- **[GPT-4o zero-shot: 63,45 F1 on Amazon-Google, 70,67 on Walmart-Amazon](https://arxiv.org/html/2409.08185)** — the dirtiest product datasets. *"63 F1 means roughly one in three hard decisions is wrong."*
- Fine-tuning helps but **cross-domain transfer degrades** — there is no one model to point at every catalogue.
- **[Splink](https://github.com/moj-analytical-services/splink) and dedupe emit clusters and scores. *"A cluster is the input to the decision, not the decision."***

**But three commercial blunts, and the third is the one that matters:**

**(a) Her job is easier than the benchmark.** She resolves *within one merchant's export*, where a
supplier SKU stem, GTIN or shared image URL usually exists. Block on those and 80–90% resolve
deterministically. **"She is charging $899 for a file whose hard part is forty rows."**

**(b) She is conflating two problems.** Variant-family reconstruction is easier than entity matching:
tokenisation, a controlled colour/size vocabulary, and **an option-grid completeness test — *"the
single most powerful heuristic in this entire problem space, and it is genuinely about forty
lines."*** He will ship it.

**(c) The kill, and it is not technical:**

> **"If she adjudicates forty canonical rows wrong, the merchant cannot tell — the file imports
> cleanly either way. That is fatal to a $2.999 transaction with no conversation, no name and no
> reviews. Buyers of unverifiable judgement buy the *person*; she has deliberately removed the
> person."**

**The merchant seat reached the identical conclusion from the buyer's side.** Two seats, opposite
chairs, same finding.

## 4. Two of her claimed advantages fail

**Amazon's hidden rules — 30% real and decaying.** The [SP-API Product Type Definitions API](https://developer-docs.amazon.com/sp-api/docs/product-type-definitions-api)
returns machine-readable JSON Schema including `parentageLevel=PARENT/CHILD` variation requirements.
What survives is the soft layer — which nominally-required attributes the pipeline *actually*
enforces. *"Real knowledge, but it decays — a maintenance liability she has to keep re-earning
rather than an asset that compounds."*

**The Brazilian cost base is aimed at the wrong enemy.** *"My marginal cost is a few cents. Against
the Indian BPO at $4–7/hour, **her cost advantage is negative** — they put three people on a
2.500-SKU catalogue for a week for under $900 all-in."*

**Operational flag:** [Stripe restricts cross-border activity for Brazil-registered accounts](https://support.stripe.com/questions/transaction-declined-stripe-brazil-accounts).
Charging $4.999 in USD may require a US or UK entity — *"that puts a real name on a public registry."*

## 5. What would worry him — five things

1. **She sells migration exception handling to Shopify agencies, white-labelled** — upstream of him, degrading his funnel invisibly.
2. **A free diagnostic that is specific and correct** — *"row 1.847 collapses into row 1.203; these nine variant families have incomplete option grids; these thirty-one rows fail Amazon's LUGGAGE schema."* **"It converts an unverifiable purchase into an obvious one. If she lands it first, I take her seriously that week."**
3. **One named, dated, screenshotted case study.** *"Not a testimonial — an artefact. For a $2.999 transaction, one of those outweighs fifty reviews, and it costs her nothing but the anonymity she's overvaluing."*
4. **She goes vertical** — apparel, or **auto-parts fitment (ACES/PIES)**: *"the version I would genuinely fear: the judgement really is un-automatable, the buyers are large, and nobody blinks at a $5.000 invoice."*
5. **The one he would not see coming:** *"she becomes the quiet default subcontractor for two or three PIM vendors' onboarding teams. Plytix and its peers sell 'we'll import your data for you' and then discover the customer's data is unimportable. **That is a recurring, funded, and completely invisible pipeline.**"*

**What would not worry him at all: SEO against failure phrases.** *"A two-year grind for a channel
that pays badly."* — independently confirming the red team.

## 6. THE CHANNEL NOBODY HAD FOUND

> **"I'd list her under 'Trusted Matrixify Experts' tomorrow. It costs me nothing, and it lets me
> close 'can you just clean this for me?' support tickets by pointing at her. Ten to twenty
> qualified, pre-frustrated, pre-diagnosed leads a month, and I'd pay nothing and take nothing.
> That is the single best channel available to her and it isn't on her plan."**

Free. Warm. High intent. From the competitor.

## 7. The fork she must choose before starting

**As an agency subcontractor:** **$0,35–0,60/SKU on 500+.** A 2.500-SKU job = **$875–1.500 — a
third to a half of her published $2.999.** 3–8 jobs/month = $3.000–8.000/month.

> **"The partner channel pays like the agency deal, not like her price list. Her realised price
> drops from $1,20/SKU to about $0,45, her direct sales stop because she has no time left, and she
> becomes a dependent contractor with two customers. That is a genuinely decent $60–100K/year
> freelance career on a Brazilian cost base. It is not the business on the page, and **the two
> channels are mutually exclusive in practice. She should pick before she starts.**"**

## 8. What he would do if he were her

Sell **the diagnosis, not the fix** — free, no-login, specific and numbered, because *"that single
artefact solves both of her real problems at once: it's **verifiable**, so it substitutes for the
reviews and the face she refuses to provide, and it's **automatable**, so it costs nothing to run."*
**Abandon merchant SEO.** Get onto three or four Shopify Plus agencies' and one PIM vendor's
subcontractor list — *"cashflow starting in week six instead of month nine, and the only way she
ever actually accumulates the per-category rule library she's currently claiming she already has."*
**Narrow to one vertical** — apparel or auto-parts fitment — *"own one vertical's judgement
completely, and charge $5.000 without anyone blinking."*

And the sentence that will need a decision from the founder:

> **"The faceless part is the first thing I'd drop — she has it filed as a cost advantage and it is
> in fact the single largest tax on her price."**
