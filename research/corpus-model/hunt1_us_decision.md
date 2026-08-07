**Re-checked this session (the three facts the recommendation rests on):**
1. `arxiv.org/abs/2509.18400` — fetched, HTTP 200. The ATLAS paper is real and is built from CROSS. Verbatim: the fine-tuned model achieves *"40 percent fully correct 10-digit classifications and 57.5 percent correct 6-digit classifications,"* reported as **+15 points over GPT-5-Thinking and +27.5 points over Gemini-2.5-Pro-Thinking** — i.e. frontier models land at roughly **25% and 12.5% 10-digit accuracy**. [VERIFIED]
2. `rulings.cbp.gov/api/search?term=apparel` — fetched, HTTP 200, **54,117 hits**, each record carrying `rulingNumber, subject, categories, rulingDate, tariffs, relatedRulings, modifies, modifiedBy, revokes, revokedBy, operationallyRevoked`. The revocation-chain fields the product depends on are really there. [VERIFIED]
3. `rulings.cbp.gov/api/ruling/F87174` — fetched, HTTP 200, full ruling text: a 51% acrylic / 49% polyester women's knit sweater classified **6110.30.3020, duty 32.9% ad valorem**. Full text is retrievable one call per ruling, and a single ruling shows the duty magnitude at stake. [VERIFIED]

Also checked, because it changes the legal section: **CBP HQ H350722 (Jan 16, 2026)** exists at `rulings.cbp.gov/ruling/H350722` and is discussed by multiple trade firms. It holds that an AI classification tool offered to importers is permissible as a suggestion aid only if it is separated from the entry portal, disclaimed meaningfully, and **does not direct the importer or broker on the code that appears on an entry**; an automated tool is not a "person" under 19 CFR 111, and a licensed broker must make the actual entry classification when acting for others. [PLAUSIBLE — firm summaries fetched via search, ruling text itself not fetched]

No candidate is a just-a-prompt. The winner is the one where the model's failure rate is *measured* rather than argued.

---

# THE WINNER: The Apparel & Footwear Classification Defense Corpus (CROSS edition)

## 1. THE BUSINESS

A small US clothing or footwear brand that imports from Asia must tell the US government a 10-digit tariff code for every product it brings in, and the legal responsibility for that number sits with the brand, not its shipping agent. Getting it wrong costs duties, penalties, and a CBP letter with a 30-day clock — and frontier AI models get the 10-digit code right only about a quarter of the time, inventing supporting citations as they go. Sol sells a US$297 downloadable folder containing every published CBP classification ruling for clothing and footwear, normalized and marked with which ones have been revoked, so the importer's own ChatGPT or Claude answers with real ruling numbers instead of plausible fiction.

## 2. WHAT IS IN THE FOLDER, FILE BY FILE

- **`START-HERE.md`** — 2 pages. How to make a Project, which files to attach, the three prompts to paste, and the information-not-advice framing repeated in the buyer's own words.
- **`INSTRUCTIONS.md`** — the interface file. Forces the AI through a fixed sequence: (a) elicit the physical facts that decide apparel codes — knit vs woven, fiber content by weight, gender/size range, garment construction, closure, footwear upper and outer sole material; (b) walk General Rules of Interpretation 1–6 and the Section XI / Chapter 61-62-64 notes in order; (c) **retrieve** candidate rulings from the corpus by heading and product features — never recall from memory; (d) check each cited ruling's `revokedBy` / `modifiedBy` field before relying on it; (e) output a classification memo listing the chosen code, the runner-up code, the fact that decides between them, and the ruling numbers on both sides; (f) refuse to state a code where the corpus contains no on-point ruling, and say so explicitly.
- **`/rulings/ch61-knit/`, `/ch62-woven/`, `/ch64-footwear/`** — the corpus. Every CROSS ruling in these chapters as one markdown file each: ruling number, date, issuing office, subject, full text, the tariff numbers ruled, and a `STATUS:` line (`active` / `revoked by HQ______` / `modified by ______`). Sharded by heading (`6110/`, `6109/`, `6203/`, `6402/`…) so a Project retrieves the right hundred files, not all sixty thousand.
- **`/rulings/INDEX-by-heading.md` and `INDEX-by-feature.md`** — the retrieval layer, and the single most valuable file. Every ruling reduced to one line: heading, code assigned, the deciding feature, date, status. `INDEX-by-feature.md` inverts it: "fiber content 50/50 breakpoint → these 41 rulings"; "knit vs woven, sleeve panels differ → these 17"; "footwear, external surface area of upper is textile with rubber overlays → these 63."
- **`/hts-notes/`** — current HTSUS Section XI notes, Chapter 61, 62 and 64 legal notes and subheading notes, plus statistical suffixes, from USITC. These are what GRI 1 actually requires and are where the fiber-content and knit/woven definitions legally live.
- **`/worked-examples/`** — 50 annotated GRI analyses written by Sol from the rulings: hoodie at 55/45 cotton-poly, matched two-piece "set," garment with a knit body and woven sleeves, sneaker with textile upper and rubber toe cap, festive-article exception, samples marked "not for resale." Each shows the decision path and the ruling that decided it.
- **`/cf28-cf29/`** — what to do when CBP asks. Form 28 Request for Information and Form 29 Notice of Action response procedure, the 30-day timeline, extension practice, prior-disclosure mechanics, and the published penalty mitigation guidelines (19 CFR Part 171, Appendix B) in table form.
- **`/reasonable-care/`** — CBP's own reasonable-care checklist and Informed Compliance Publications for apparel and footwear, plus a records template so the buyer's classification memos become the documented evidence of care that reduces 19 USC 1592 culpability.
- **`/erulings/`** — how to file a free binding ruling request when the corpus shows genuine ambiguity, including what a well-formed request contains, and the honest warning that a binding ruling binds you even when it goes against you.
- **`CHANGELOG.md`** — dated. What was added, which rulings changed status, which tariff actions moved rates, since the last edition.

**Source count and assembly:** five source systems, tens of thousands of documents. CROSS (54,117 apparel hits and 8,947 footwear hits verified by API; 1,427 under heading 6110 alone), the USITC HTSUS notes, ~10 CBP Informed Compliance Publications, Court of International Trade classification opinions, and 19 CFR Part 171 App. B. Three to four weeks. **Not rebuildable in an afternoon:** an afternoon gets you one heading's keyword search. The value is tens of thousands of individual `api/ruling/{number}` fetches, normalized, revocation-chained, and indexed by deciding feature — plus 50 hand-written worked examples.

## 3. WHY A PROMPT CANNOT DO IT — the decisive section

This is the only candidate in the set where the model's failure is **measured, published, and quantified on exactly this task.** ATLAS (arXiv 2509.18400, fetched) benchmarks 10-digit HTS classification against CROSS rulings and reports frontier reasoning models at roughly **25% (GPT-5-Thinking) and 12.5% (Gemini-2.5-Pro-Thinking)** ten-digit accuracy. A purpose-built fine-tune reaches only 40%. [VERIFIED]

So a bare model is wrong about **three times out of four** at the digit level where the duty rate lives — and the two named errors are the ones that cost money:

- **The wrong statistical suffix at a different duty rate.** F87174 (fetched) classifies a 51% acrylic knit sweater at **6110.30.3020, 32.9% ad valorem**. Change the fiber breakpoint and the code moves to 6110.20 (cotton) or 6110.10 (wool) at materially different rates. The model produces one confident code and no indication that a single percentage point of fiber content flipped it.
- **The invented ruling number.** Asked to support its answer, a model will name a plausible "NY N-series" ruling that does not exist, or cite a real ruling that was **revoked** — and CROSS's own `revokedBy` field, which the corpus carries, is the only way to know. A wrong code in a CF-28 response is a duty bill; a fabricated citation in a CF-28 response is a credibility loss with the officer deciding your culpability level.

The corpus does not make the model smarter. It converts the task from recall (25% accurate) into retrieval-and-check against 63,000 real documents with revocation status attached. That is a different task, and it is the one the folder is for.

## 4. THE BUYER AND THE MOMENT

The owner or operations lead of a US apparel, footwear or accessories brand importing from Asia — revenue in the low seven figures, no in-house trade compliance, a customs broker who files whatever codes the brand supplies. Two moments:

- **The letter.** A CBP Form 28 Request for Information arrives questioning a code. Thirty days. Non-response escalates to a Form 29 Notice of Action and a rate advance. They search that night. [PLAUSIBLE — broker/law-firm CF-28 guide ecosystem verified to exist]
- **The season.** Post-2025 tariff layering makes a 10-point rate difference between two adjacent codes existential, and they need to know which one survives scrutiny before they place the order.

The day they buy: they unzip, drop `INSTRUCTIONS.md` plus the relevant heading folder into a Claude or ChatGPT Project, paste the product spec, and get a memo naming a code, the runner-up, and the real rulings on both sides — within twenty minutes, with no software installed and no admin permission (H5). E-commerce operators are the most AI-saturated small-business cohort there is (H8).

## 5. THE MONEY AT STAKE

- **32.9% ad valorem** on one verified ruling's product line (F87174, fetched). On US$400,000 of annual landed cost, a code error of even 8 points is **US$32,000/year**, recurring silently across every entry until CBP notices. [VERIFIED rate; arithmetic mine]
- **19 USC 1592** penalties for negligent misclassification run to 2× the lost duties, 4× for gross negligence, on top of the duties owed. [PLAUSIBLE — statute, not fetched]
- CBP collected **US$37.9M in trade-violation penalties in 2025**, misclassification a significant share. [PLAUSIBLE — search summaries]

US$297 against a five-figure recurring exposure is 1–2% of one year's error. That is the arithmetic that makes the price feel small.

## 6. PRICE AND VOLUME

**US$297.** Target US$7,400–8,300/month = **25–28 sales/month.** Add a US$147/year renewal for quarterly updates; renewals raise revenue without raising unit count, which matters because support load scales with units (H6/support). At 26 units/month one person with a good FAQ is fine.

At US$297 the price clears the paid-acquisition threshold comfortably, which matters more here than for any other candidate: a business buyer with a five-figure exposure and a 30-day deadline is the one buyer type where a click can profitably cost US$8–15.

## 7. THE CHANNEL

Three engines, all faceless, all in writing, none needing an audience.

1. **Written cold email to findable businesses.** This is the primary engine and the reason this candidate beats the consumer ones. DTC apparel and footwear brands importing from Asia are enumerable — Apollo (which she already has access to), Shopify store databases, importer trade-data lists. The subject line writes itself and is not a pitch: *"NY ruling F87174 classified a 51% acrylic knit sweater at 32.9% — here are the 1,427 rulings under heading 6110."* Business buyer, in writing, no calls (fits her constraints exactly). 1,500–2,500 sends/month at a 0.5–1% send-to-sale rate is 8–25 sales; this needs real deliverability setup (own domain, warmed inbox, strict opt-out) and is the number the first demand test must measure.
2. **Paid search at US$297.** Exact-match commercial intent: `cbp form 28 response`, `hts code for hoodie`, `apparel tariff classification ruling`. Viable at this ticket per the established asymmetry; not viable at US$97.
3. **Customs brokers and 3PLs as affiliates.** Brokers are told constantly by clients "just pick a code for me" and must legally refuse to own that decision — and after HQ H350722 they are *more* careful, not less. They have no product to hand the client. A 30% affiliate cut on US$297 is US$89 for forwarding a PDF. Written outreach only; brokers are businesses.

Organic content (free per-heading explainer pages that actually contain the tables, funneling to the corpus) is engine four and slow — it compounds but does not launch this.

## 8. WHO GIVES IT AWAY FREE, AND WHY THE BUYER PAYS ANYWAY

- **CROSS itself is free and public** — and it is where the corpus comes from. Verified by API: 54,117 apparel hits behind a bare keyword search, no synthesis, no GRI walkthrough, no feature index, and no way to see revocation status without opening each ruling. The buyer is paying for the normalization and the index, not for secret data, and the copy must say so plainly. Saying "assembled from CBP's free public rulings" *increases* trust; pretending it is proprietary destroys it.
- **CBP eRulings** issues free binding rulings, ~30 days — per product, slow, and binding against you if unfavorable. It cannot answer "which of my 40 SKUs are wrong." [PLAUSIBLE; cbp.gov returns 403 to direct fetch]
- **USITC HTS lookup** free — gives the tree, not which branch a real officer chose.
- **CBP Informed Compliance Publications** free — good, general, no ruling corpus.
- **No Nolo title, no nonprofit, no trade association** publishes an assembled classification corpus. This is the one candidate where the free-substitute check comes back genuinely **CLEAR** — a striking contrast with the health-appeal candidate, where two well-funded nonprofits give away the whole job including free human case management.
- **Paid adjacent: SaaS classifiers** (Zonos Classify, Gaia Dynamics, digicust, TariffLens). They classify *for* the user — which is precisely the shape HQ H350722 just constrained. They do not hand the importer a citable reference library that lives inside the AI the importer already pays for.

## 9. THE LEGAL LINE

Customs brokers are licensed under 19 CFR Part 111, and "customs business" — classifying merchandise for *others* in connection with entry — requires a license. **An importer classifying its own merchandise is not customs business; it is the importer's own statutory reasonable-care duty under 19 USC 1484.** HQ H350722 sharpens this: a tool may suggest, must be disclaimed, and must not *direct* the code on an entry. A published reference library that the importer reads and applies to its own goods sits on the safe side of that line more comfortably than the SaaS classifiers do.

**Permitted, verbatim, for the sales page:**
- "This folder contains every published CBP classification ruling for Chapters 61, 62 and 64, with the tariff number each one assigned and whether it has since been revoked or modified."
- "NY ruling F87174 classified a 51% acrylic, 49% polyester women's knit sweater under 6110.30.3020 at 32.9% ad valorem. Heading 6110 alone has 1,427 rulings in this folder."
- "Independent published benchmarks put frontier AI models at roughly 25% accuracy on 10-digit HTS classification. This folder gives your AI the actual rulings to retrieve instead of recalling."
- "Reference material for importers classifying their own merchandise. Information, not advice. Not legal or customs-brokerage services. Your licensed broker files your entry."

**Forbidden, verbatim — never write these:**
- "Send us your product spec and we'll tell you your code." (customs business, and violates H6)
- "Guaranteed CBP-compliant classification."
- "This code is correct for your product."
- "We'll handle your CF-28 response."
- "Replaces your customs broker."

She never sees a buyer's product, never assigns a code, never reviews a CF-28. The buyer's own AI does the applying. And `INSTRUCTIONS.md` must itself instruct the model to refuse when the corpus has no on-point ruling — a product that teaches the AI to say "I don't know" is the single strongest legal and reputational asset here.

## 10. PIRACY — the honest answer

A markdown folder is trivially copyable and one buyer can hand it to a Slack group of twenty brands. Four real, partial limits, in order of strength:

1. **It decays visibly and fast.** CBP adds rulings continuously and revokes older ones; 2025–26 tariff actions moved rates repeatedly. A copy from six months ago carries rulings marked `active` that are now revoked — and relying on a revoked ruling is worse than having no ruling, because it *looks* like documented reasonable care and isn't. `CHANGELOG.md` with dated editions is the anti-piracy mechanism, and the renewal is what she actually sells after month one.
2. **Business buyers in a compliance posture share less than consumers in support groups.** Nobody documents their reasonable care on a zip file a competitor emailed them.
3. **Bulk.** Sixty thousand files, multi-gigabyte. Awkward to repost, impossible to paste into a thread.
4. **Per-buyer watermarking** — order ID in every file footer and in the index headers. It does not stop sharing; it discourages public posting.

Honest residual: a copy will leak. She should price and plan as if 10–20% of eventual users didn't pay, and treat the update stream, not the initial download, as the product.

## 11. THE BUILD — four weeks, Claude Code doing the work

**Week 1 — the spine, one heading.** Script CROSS retrieval: paginate `api/search`, then one `api/ruling/{number}` call per hit, cache raw JSON. Do heading 6110 only (1,427 rulings, verified count). Build the markdown converter, the `STATUS:` resolver from `revokedBy`/`modifiedBy`/`operationallyRevoked`, and the one-line index format. Write `INSTRUCTIONS.md` v1. **This week's output is what the First Test measures — build nothing further until it passes.**

**Week 2 — scale out.** Run the same pipeline across all of Chapters 61, 62 and 64. Shard by heading. Generate both indexes. Pull HTSUS Section XI and Chapter 61/62/64 notes from USITC. Spot-audit 50 random rulings by hand against the live CROSS page.

**Week 3 — the human layer.** The 50 worked examples (this is Sol's writing, informed by the rulings — it cannot be scripted). The CF-28/29 playbook and 19 CFR 171 App. B mitigation tables. The reasonable-care files. The eRulings guide.

**Week 4 — the shell.** Gumroad or Lemon Squeezy listing, watermarking at delivery, FAQ that pre-answers the support email (this is what keeps 26 units/month manageable), the sales page carrying the benchmark number, and the cold-email domain warmed and the first 300 sends queued.

Claude Code does the retrieval scripting, the tens of thousands of conversions, the revocation chaining, the index generation and the audit sampling. Sol writes the worked examples, the instruction file, and the copy.

## 12. THE FIRST TEST

**The measurement:** does the corpus actually raise 10-digit accuracy? Replicate ATLAS's method on her own slice.

**How:** pull 100 CROSS rulings in heading 6110 issued *after* the model's training cutoff (the API returns `rulingDate`, so this is a filter, not a guess). Strip each ruling to its product description. Run each twice: (A) bare model, no corpus; (B) same model with the Week-1 6110 corpus and `INSTRUCTIONS.md` attached, with the ruling under test excluded from the corpus. Score exact 10-digit match, 6-digit match, and — critically — **citation validity**: does every ruling number the model names exist and is it correctly marked active?

**Cost:** roughly US$30–60 in API tokens plus the Week-1 build. **Duration:** two days after Week 1, so a decision by day 9.

**Stop threshold:** corpus-assisted 10-digit accuracy must beat bare-model accuracy by **at least 20 percentage points** (i.e. bare ~25% → assisted ~45%+), *and* citation validity in condition B must be **at least 95%**. Miss either and stop: the product's whole claim is that retrieval beats recall, and if it doesn't on the easiest chapter, three more weeks of scraping buys nothing.

This is genuinely runnable today with data that exists, and its output is also the headline number on the sales page — a measured claim she owns, not a borrowed statistic.

## 13. WHAT MUST BE TRUE

**Before building (settle in days, cheaply):**
- *The accuracy lift is real.* → The First Test above. US$60, 2 days. **Gates everything.**
- *Anyone will pay US$297 for a reference library rather than a tool that does it for them.* This is the genuine unknown — nobody has sold this shape. → Cheapest settlement: 150 cold emails to DTC apparel brands offering the 6110-only edition at US$197 as a "first edition" with the full chapters promised free on release. Cost: US$60 of Apollo credits and a warmed domain. Threshold: **fewer than 2 sales and fewer than 8 substantive replies from 150 sends → the channel does not clear 26/month, stop.**
- *Bulk CROSS retrieval is permitted at volume.* Public government records, non-copyrightable facts, and a documented public API — but rate-limit politely and check for terms of use on rulings.cbp.gov before running 60,000 calls. → An afternoon of reading, plus throttling. [UNKNOWN — I fetched the API but not its terms page]
- *HQ H350722 does not reach a static reference publication.* → Read the actual ruling text at `rulings.cbp.gov/ruling/H350722` in full (I have only firm summaries) and, if any doubt survives, have a US customs attorney review one page of sales copy for a few hundred dollars. This is the highest-value few hundred dollars in the whole plan.

**After the first customer:**
- *Do buyers succeed, or does the AI still miss and they blame the folder?* → Ask every buyer one question by email 14 days later: "did your AI's memo hold up?" Ten answers reshapes `INSTRUCTIONS.md`.
- *Do they renew for updates?* → The renewal rate at month 12 decides whether this is a business or a one-time cash pulse. If renewals are under 20%, the answer is to widen chapters (electronics, houseware, toys — the same pipeline, a new corpus per chapter) rather than to chase the same buyers.
- *Which chapter is next?* → Whichever heading the inbound questions name most. The build pipeline is chapter-agnostic; the second corpus costs one week, not four.

**The weakest link, stated plainly:** demand for this exact shape is inferred, not proven. Importers demonstrably search the panic queries and demonstrably pay SaaS to classify for them — but nobody has yet sold a bring-your-own-AI ruling corpus, so the 150-email pre-sell must run before Week 2. Second: a diligent buyer *can* DIY on free CROSS, so the pitch is assembled-and-current, never secret.