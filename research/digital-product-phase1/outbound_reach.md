# OUTBOUND REACHABILITY ASSESSMENT — five B2B candidates

All Apollo figures below are from live queries I ran today (2026-08-06) and are marked VERIFIED as observed counts. Required volume throughout: **132–192 sales/year** (11–16/mo at US$497–750).

---

## RANKING (best → worst outbound reachability)

**1. BUYERROOM · 2. LINELOCK · 3. CREDIT LAB · 4. WRAPCHECK · 5. RIO BLOCKS**

Only BUYERROOM has a **dated, publicly published trigger**. LINELOCK has an invisible trigger but such high recurrence that standing presence works. The bottom three fail on trigger structure, and RIO BLOCKS additionally fails because the findable list is the wrong people.

---

## [3] BUYERROOM — THE ONLY CANDIDATE WITH A VISIBLE, DATED TRIGGER

**(a) Named findable list: YES, free, public, no login.**
- **ECRM session attendee pages** — e.g. `https://ecrm.marketgate.com/Sessions/2026/10/LatinAmericaBeautyPersonalCare/Attendees`. **VERIFIED by direct fetch:** publicly accessible without login, names both supplier brands (AJE Group/Peru, DROBELSA SAC/Peru) and retailer buyers (Alkosto/Colombia, Farmacias del Ahorro/Mexico, SMU/Chile), with separate Buyer/Seller filters. ~60+ companies on this one session. Companies only — **no individual names, no emails**.
- **ECRM beauty session calendar** — `https://ecrm.marketgate.com/sessions/category/Beauty`. VERIFIED: 6 beauty sessions listed across ~8 months (Frankfurt Oct 2026, Tampa Oct 2026, Chicago Jan 2027, Malta ×2 Jan–Feb 2027, Las Vegas Jun 2027), extrapolating to ~9/yr. All carry "View Participants."
- **Cosmoprof North America exhibitor list** — free public PDF, `https://cosmoprofnorthamerica.com/wp-content/uploads/CPNA-LV25_Preshow_exhibitors_WEB_040825.pdf`. I extracted it: **921 candidate company-name lines across 4 pages** (some are wrapped continuations, so realistically ~650–800 companies), alphabetised, updated weekly. VERIFIED by my own extraction. Names only, no contacts.
- **Apollo, for the person layer: 50,144** founders/co-founders/CEOs/heads-of-sales at 1–50-employee companies tagged skincare/cosmetics/beauty-brand/personal-care. VERIFIED (live query). This is where company names from ECRM/Cosmoprof become named humans with LinkedIn URLs.

The workflow is genuinely two-step and it works: **public list gives the company + the date → Apollo gives the named founder → enrichment gives the email.**

**(b) Trigger visible from outside: YES — uniquely so.** ECRM publishes the attendee roster *months before the event*. Today is 6 Aug 2026 and the 25–28 Oct 2026 Tampa roster is already public. Sol can see, by name, a brand that has committed to a specific dated buyer meeting, with ~11 weeks of lead time. No other candidate here has anything comparable. This converts BUYERROOM from a standing-presence problem into **transactional outbound with a deadline** — the outreach can literally reference the date.

**(c) Public signals, ranked by usability:**
| Signal | Status | Value |
|---|---|---|
| ECRM published attendee lists (dated) | VERIFIED public | **Highest — names brand + date** |
| Cosmoprof/Luxe Pack/Indie Beauty exhibitor PDFs | VERIFIED public | High — names brand + date |
| RangeMe Immediate Opportunities (`public.rangeme.com/immediate-opportunities`) | VERIFIED public — 22 live campaigns, each naming retailer, category, deadline | **Medium only — names the RETAILER, never which brands applied.** Tells Sol the category is hot, not who to email |
| Recent funding round (Apollo `latest_funding_date_range` filter, available) | Filter exists | Medium — correlates with going-to-retail |

**(d) Volume — the real constraint, and I will not soften it.** ECRM beauty alone supplies roughly **240–540 supplier brands/year** (~6–9 sessions × ~40–60 sellers). Needing 132–192 sales means **25–80% penetration of that exact list** — not plausible. BUYERROOM hits target only if the universe is widened to: all ECRM categories (not just beauty), Cosmoprof/Indie Beauty exhibitors (~700+/show), and funding-signal brands from the 50,144 Apollo pool. That takes required penetration to ~5–10%, which is demanding but real. **Honest finding: the trigger list is excellent and the volume list is a different, larger list.** The "Beauty Edition" framing is a marketing wrapper, not the addressable market.

**Approval threshold: passes decisively.** VERIFIED from the ECRM session page: Emerging Brands (Discovery Hub) **US$7,000** for 10-minute appointments; Challenger Brands (Innovation Pipeline) **US$11,000** for 10-minute appointments in a private 10×10 booth; Leading Brands (Planning Session) **US$16,900** for 20-minute appointments; extra attendees US$650/person/day. The dossier's figures are confirmed exactly. A founder who has already card-committed US$7,000–16,900 buying a US$497–750 rehearsal tool is spending **3–7% of a fee already sunk**. The payer is the founder of a 1–50-person brand — they *are* the approval threshold. No PO, no committee.

---

## [1] LINELOCK — GOOD LIST, INVISIBLE TRIGGER, SAVED BY RECURRENCE

**(a) Named findable list: YES, but the clean one is Clutch, not Dieline.**
- **Clutch** `https://clutch.co/agencies/packaging-design` — **VERIFIED by fetch:** free browsing, each listing publishes company website, location, **employee count**, avg hourly rate, min project size. **No phone numbers, no emails.** Critically, it is human-curated as *design agencies* and filterable by employee count and by industry (`/consumer-products-industry`, `/retail-industry`) — which is exactly the 2–20-person beauty-adjacent filter LINELOCK needs.
- **Dieline directory** `https://thedieline.com/directory/` — **VERIFIED by fetch: largely paywalled.** The page states "Get full access to our Directory with Dieline Pro" and returned only 2 visible results on the free tier. The "547 firms" figure is PLAUSIBLE (search snippet), not something Sol can freely enumerate. **The dossier over-rates this directory.**
- **Dieline Awards winners gallery** `https://dielineawards.com/winners-gallery.html` — PLAUSIBLE: 1,500+ entries and 170 winners across 41 categories for 2026 (search snippet). Free, public, names agencies. Good supplementary list of exactly the right kind of firm.
- **Apollo: 18,215** owners/founders/creative-directors/MDs/studio-directors at 1–50-employee companies tagged "packaging design." VERIFIED. **But I stress-tested this and it is contaminated** — the tag pulls in packaging manufacturers and converters, not just design studios (top hits included "Full Scale | Custom Packaging & Design"). Worse, filtering on `cosmetic packaging`/`beauty packaging` tags returns only **767** people and they are almost entirely **packaging suppliers, not design agencies** (Sunrise Cosmetic Packaging, Upmarket Cosmetic Packaging Company). VERIFIED. **Conclusion: Apollo cannot cleanly isolate beauty-specialist small packaging design agencies by keyword.** The list must be built Clutch/Dieline-Awards → domain → Apollo enrich for the named owner. That works, but it is manual sourcing, not a query.

**(b) Trigger visible from outside: NO. Fully private.** The send-to-print moment happens inside a shared drive and an email to a printer. There is no public feed, no filing, no announcement. Nothing Sol can see. A brand's new-variant launch announcement is *after* print and doesn't name the agency. An agency's Instagram post of finished work is also after.

**This makes LINELOCK a standing-presence business, not transactional outbound — and that must be priced into the plan.** The redeeming structural fact: unlike every other invisible-trigger candidate here, **the trigger recurs constantly** — every variant, potentially several per month per agency. So "be already-known when it fires" is achievable with one memorable email plus a free artifact (a proofing checklist), and the wait is weeks, not years. That is a survivable version of an invisible trigger. It is the difference between LINELOCK and RIO BLOCKS.

**(c) Public signals — weak, all of them.** Job postings for packaging artwork roles (~297 packaging-artwork jobs on ZipRecruiter, PLAUSIBLE from search snippet) signal artwork *volume* at brands, not a dated event, and mostly at brands rather than agencies. Dieline Awards entry lists signal an agency is active and serious. New-client-win posts on LinkedIn signal a project starting. None of these give a date. **Verdict: no usable dated signal exists. SEO on the problem ("packaging artwork proofing checklist", "variant artwork sign-off") is the more honest primary channel here, with outbound building the standing presence.**

**(d) Volume:** the addressable set of small beauty/personal-care packaging design agencies is realistically **low thousands globally** (Apollo can't isolate it; Clutch's curated packaging-design listings plus Dieline Awards entrants are the honest proxy). 132–192 sales/yr against low thousands is a few percent — plausible on paper, but note these are *repeat-use* buyers, so retention/multi-seat matters more than new logos.

**Approval threshold: passes.** The payer is the owner or creative director of a 2–20-person studio. They are the threshold. VERIFIED price ceiling context that supports the position: ManageArtworks Pro **US$399/mo**, Growth **US$499/mo**, and **barcode verification is restricted to the Custom (quote-only) plan** (`https://www.manageartworks.com/pricing`, direct fetch). Cway Starter **from €450/mo**, Pro from €1,200, Enterprise from €3,000 (`https://www.cwaysoftware.com/subscription-plans`, direct fetch). The dossier's "enterprise artwork management starts around US$400+/month" is **VERIFIED**, and the barcode gap is real and specific.

---

## [5] CREDIT LAB — BIG LIST, SEMI-INFERABLE TRIGGER, KILLED BY THE PAYER

**(a) Named findable list: YES for people, NO for the associations.**
- **Apollo: 9,354** credit officers / credit analysts / chief credit officers / directors of credit / underwriters at companies tagged asset-based-lending, equipment-finance, equipment-leasing. VERIFIED (live query — returned e.g. named credit officers at Commercial Equipment Finance Inc. and BEEQUIP Equipment Finance). This is the largest *precisely-targeted* list of the five.
- **SFNet public member search** `https://www.sfnet.com/home/membership/member-directory/member-search` — VERIFIED by fetch: public, no login, but **company names only**, and only **265 member company profiles**. The dossier over-states SFNet as a contact source.
- **SFNet employee profile pages** — VERIFIED: `https://www.sfnet.com/detail-pages/member-directory-employee-profile-detail/207` publicly shows a named individual with title and city ("Justin Forbrook, Relationship Manager / VP, Minnetonka, MN"), **no email or phone**. Sequentially-numbered and therefore enumerable. Useful for titles/verification, not for contacts.
- **ELFA member directory** — **VERIFIED by fetch: members-only.** "Please log in to search our member directory… Member Exclusive Content." Dead as a free source. (~575 member companies, PLAUSIBLE.)
- **IMN / Informa Connect** — publish **past-speaker** rosters publicly (`informaconnect.com/data-centers-east/past-speakers/`) and describe audiences ("350+ senior decision-makers"; ABS East "over 4,000 attendees" — PLAUSIBLE, search snippets). Speakers are public; **attendees are not.**

**(b) Trigger visible from outside: PARTIALLY — better than LINELOCK.** "This lender is moving into AI/data-centre finance" leaves public traces: press releases announcing a new vertical or facility, conference speaking slots on data-centre panels, and — usably — **job postings for data-centre/digital-infrastructure credit roles**, which Apollo can filter on directly (`organization_job_posted_at_range`, `q_organization_job_titles`). That is a real, datable, inferable signal. On trigger *inference* alone, CREDIT LAB ranks second behind BUYERROOM.

**(c) Public signals:** new-vertical press releases; data-centre conference agendas and speaker lists (public); job postings for digital-infrastructure credit roles (Apollo-filterable, VERIFIED capability); new fund/warehouse-facility announcements. Genuinely the second-best signal set.

**(d) Volume:** 9,354 findable individuals, dossier claims 2,000–4,000 plausible buyers. At US$749 with a manager licence for 5 learners, 132–192 unit-sales/yr against ~2,000–4,000 is **5–10% of the entire universe in year one, cold, from a faceless unknown seller with no endorsements.** The dossier's own honest note — that US$100k needs 134 sales *plus endorsements* — concedes this.

**Approval threshold: FAILS for the majority of the list, and this is decisive.** The payer is a credit professional *employed by a bank or a regulated lender*. US$749 of training software at such an institution routes through procurement, vendor onboarding, an infosec review, and a managed L&D budget. That is exactly the failure mode the brief describes: an approval step generates questions, questions generate a call, and Sol cannot take the call. Only the independent/non-bank lenders and boutique advisory shops inside that 9,354 pass self-serve — a minority slice, which further undermines (d). **Compounding kill risk:** the product requires the buyer to point *their own LLM* at synthetic deal rooms, in the single most LLM-restricted industry in the set. Many of these institutions block external LLMs outright. Best list, worst buyer.

---

## [2] WRAPCHECK BEAUTY — TRIGGER IS INVISIBLE, RARE, AND HOURS LONG

**(a) Named findable list: WEAK.**
- **Apollo: 3,384** producers / executive producers / production managers / studio managers / owners at 1–50-employee companies tagged product-photography, commercial-photography-studio, ecommerce-photography. VERIFIED — the smallest usable list of the five, and it is not beauty-specific or high-SKU-specific.
- **Production Paradise** `productionparadise.com` — **returned HTTP 403 to my fetch**, so whether profiles publish contact details is **UNKNOWN**. It is a paid membership showcase.
- **Wonderful Machine** — ~530–600 photographers in 56 countries, **invitation-only to join, ~US$2,000/yr** (PLAUSIBLE, search snippets). Browsable but tiny and skewed to editorial/advertising, not high-SKU e-commerce beauty.
- **LeBook** — a paid print/online sourcebook for the ad industry. Not a free enumerable list.
- **Dieline directory** does carry a "packaging photographers" category, but see the paywall above.

**(b) Trigger visible from outside: NO — and this is the worst trigger structure of any candidate.** Three compounding problems, not one: the wrap moment is (i) **completely private**, (ii) **low-frequency** per studio — a big multi-SKU beauty shoot is maybe monthly, so the standing-presence wait is long, and (iii) **the useful window is hours**, because the whole value proposition is catching gaps *while the set is still live*. Invisible + rare + hours-long is unworkable for outbound. Signals like casting calls or studio Instagram stories are noisy, unscalable, and require exactly the kind of manual real-time monitoring a faceless one-person operation cannot run.

**(c) Public signals:** essentially none usable. Casting calls and model bookings (noisy, not enumerable); brand product-launch calendars (only tells you *someone* shot it, months late); studio social posts (after the fact).

**(d) Volume:** 3,384 findable, of which the subset doing high-SKU beauty grids is much smaller. 132–192 sales/yr is an implausible share, and the product is per-shoot rather than per-seat.

**Approval threshold + payer ambiguity — a distinct problem the other candidates don't have.** Who physically pays is genuinely unclear: the **studio** bears the reshoot risk under a fixed-fee contract, but the **brand** bears it under cost-plus. An ambiguous payer is fatal to self-serve outbound, because Sol cannot write one email that lands on the person with both the pain and the card. Failure cost is real and VERIFIED — Squareshot model shoots start at **US$2,950/day** (own model US$5,950, Squareshot-cast US$7,450), **20-image minimum**, **US$900 per additional model** (`https://www.squareshot.com/model-photography`, direct fetch). The dossier's US$2,950 figure is confirmed; the "product shoots from US$750" figure is **PLAUSIBLE only** — I verified "from US$50/image," and 15 images × US$50 = US$750, but I did not see US$750 stated. Also note the deepest kill risk: the tool must be *adopted live on a working set under time pressure* by someone who has never installed an AI skill. That is the maximum-friction adoption scenario in this entire set.

---

## [4] RIO BLOCKS — THE FINDABLE LIST IS THE WRONG PEOPLE

**(a) Named findable list: exists, but points at the wrong buyer.**
- **Apollo: 2,879** founders / owners / designers / heads-of-design / product-developers at 1–50-employee companies tagged swimwear. VERIFIED (returned e.g. Monday Swimwear, Asherah Swimwear, Maia Swimwear).
- **Faire** publishes browsable swimwear/beachwear brand listings by category (`faire.com/category/Women/subcategory/Apparel/Swimwear%20&%20Beachwear`), free to browse.

**Here is the fatal mismatch.** Every name on both lists is an **operating swimwear brand that already ships product** — which means they **already have graded patterns and an established patternmaker**. The actual buyer for a *development library* is a **pre-launch brand or a freelance designer starting a swim line**: no company entity, no domain, no LinkedIn company page, not on Faire, not in Apollo. **The buyer is definitionally absent from every directory, and the people in the directories have already solved the problem.** No amount of list-building fixes this.

**(b) Trigger visible from outside: NO — invisible AND non-recurring.** "I have decided to develop a swim line" leaves no public trace before the fact, and it fires **once per buyer, ever**. LINELOCK survives its invisible trigger because the trigger repeats monthly; RIO BLOCKS has no such rescue. Standing presence against a once-in-a-lifetime, undatable, unobservable event is not a business a faceless seller with no audience can run.

**(c) Public signals:** none worth naming. Trademark filings and new-brand Instagram accounts are late, unenumerable, and dominated by hobbyists.

**(d) Volume:** 132–192 sales/yr from a population whose findable members don't need it and whose needful members can't be found. Fails.

**Independently killed on price ceiling (R2), which finishes it.** A custom, graded, production-ready pattern **to the buyer's own design** is available for **US$30–65** on Fiverr in DXF/AAMA/PLT/ASTM: `fiverr.com/creative_mani10/...` at **US$30**, `fiverr.com/dorellejoie/create-dxf-or-aama-pattern-for-a-sample-of-your-design` at **US$40**, `fiverr.com/designerisrat/...` at **US$65** (VERIFIED, with URLs). Smart Pattern Making sells a dedicated bikini pattern-making service (`smartpatternmaking.com/products/bikinis-pattern-making-service`). Minerva Patterns holds 3,000+ digital patterns in DXF(AAMA)/PLT/PDF adapted to custom measurements. **A US$497–750 library of generic blocks cannot be sold against a US$40 bespoke pattern.** The cheapest adequate substitute is 10–20× cheaper *and* better fitted to the buyer's actual design. This candidate is dead twice over, and it is also the one that requires surrendering the core craft to a named patternmaker partner.

---

## VERDICT

**Findable buyer + visible or inferable trigger: BUYERROOM only, unambiguously.** It is the sole candidate where Sol can look at a free public web page, read the name of a company and the *date* it will walk into a buyer meeting, resolve that company to a named founder via Apollo, and write to a person who has already committed US$7,000–16,900 and can pay US$497–750 on a card with no approval step. Its weakness is volume, not reachability — and the fix is widening beyond ECRM beauty to all ECRM categories, Cosmoprof/Indie Beauty exhibitor lists, and funding-signal brands.

**Findable buyer + invisible but high-frequency trigger: LINELOCK, viable as a standing-presence business.** The list must be hand-built from Clutch (free, curated, employee-count-filterable) and Dieline Awards entrants rather than the Dieline directory (paywalled) or Apollo keyword tags (contaminated with packaging manufacturers). Its primary channel is honestly **SEO on the buyer's problem**, with outbound establishing presence before the trigger fires. The approval-threshold test passes cleanly and the ManageArtworks barcode gap is verified and real.

**The other three fail on outbound, each for a different structural reason:** CREDIT LAB has the best-formed list and second-best signals but a payer sitting behind bank procurement and an LLM-blocked IT policy; WRAPCHECK has an invisible, infrequent, hours-wide trigger, an ambiguous payer, and the highest adoption friction in the set; RIO BLOCKS has a directory full of people who already solved the problem, a once-per-lifetime invisible trigger, and a price ceiling set at US$40 by Fiverr.

**Two dossier claims need correcting.** RangeMe: the **15,000 figure is BUYERS, not participating brands** — the platform holds ~90,000 brands, and 2025 saw 518 campaigns → ~55,000 submissions → ~10,500 approvals (all PLAUSIBLE, from search snippets, not directly fetched). More importantly, RangeMe Immediate Opportunities are a **retailer-side** feed: I fetched the public page and confirmed it names the retailer, the category, and the deadline, but **never which supplier brands applied or were selected**. It tells Sol which categories are hot; it does not tell her whom to email. **ECRM, not RangeMe, is the trigger list.**