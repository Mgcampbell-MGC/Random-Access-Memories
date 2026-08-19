# THE DATASET HUNT — S4 hunted, 19 Aug 2026

**Shape S4 (a compounding dataset) hunted for the first time. Statutes fetched at source, two data
marketplaces' eligibility pages read, live HTTP probes run against Brazilian registers.**

> **Three laws, one structural wall, and one candidate. The laws are worth more than the candidate.**

---

## 1. THREE LAWS, AND THE FIRST ONE SHOULD BE THE OPENING SCREEN FOR EVERY S4 IDEA

### ★ THE HEAD-START ASYMMETRY

> **The property that makes a dataset defensible — it compounds — is the SAME property that makes it
> un-enterable. If a dataset is worth accumulating, someone already started accumulating it, and their moat
> then points AT HER.** Every mature compounding dataset is, by construction, closed to a new entrant.
> **Screen for this FIRST — before buyer, before price, before legality.**

**And the legal system says so out loud.** UK SI 1997/3032 **reg. 17(3)**: *"Any substantial change to the
contents… **including a substantial change resulting from the accumulation of successive additions**… shall
qualify the database… for its own term of protection."* **A continuously-updated database is effectively
perpetually protected. That is Law 1 written into statute.**

### ★ THE CLOCK-START RULE

> **The only moment at which a solo entrant and an incumbent are LEVEL is the moment the recording opportunity
> comes into existence** — a register that opened this year, a statutory regime that has just taken effect, a
> mandate whose first filings are landing now. **Hunt CLOCK-STARTS, not datasets.**

### ★ THE STATE KEEPS STATE, NOT HISTORY

> **A register publishes what it needs to OPERATE. It has no operational need for last year's snapshot, so it
> overwrites.** The change-log of a current-state-only register is **the one artefact the register-holder will
> never produce — and it cannot be back-filled by anyone, including an AI agent, because the prior state is
> gone.** The only genuinely non-re-assemblable class found in this hunt.

---

## 2. THE STRUCTURAL WALL — she cannot sell data on the data marketplaces

**Both verified by direct fetch of the platforms' own eligibility documentation:**

| | |
|---|---|
| **AWS Marketplace / AWS Data Exchange** | Eligible seller jurisdictions are exactly: Australia, Bahrain, Colombia, EU member states, Hong Kong, India, Israel, Japan, New Zealand, Norway, Qatar, South Korea, Switzerland, UAE, UK, US. **The word "Brazil" does not appear anywhere on the page** — verified by string count |
| **Snowflake Marketplace** | Paid listings require a provider billing address in one of twenty named countries. **Brazil absent.** And Snowflake requires *"contact your business development partner at Snowflake"* before a paid listing — **a conversation, so C1 fails twice over** |

> **Consequence: distribution for any S4 product must be HER OWN SITE with a self-serve checkout. The
> marketplace shortcut does not exist for her.** *(And per `THE_TAX_ANSWER.md`, a card checkout costs ~8% —
> so invoicing a small number of business subscribers beats a consumer-style card funnel twice over.)*

**A second filter, and it is cheap to apply:** the most instructive comparables in this category —
**Nubimetrics** (*"entre em contato com o parceiro"*) and **OpenSanctions** (contact sales) — **publish no
price at all.**

> **If the nearest comparable hides its price, the category is SALES-LED and she cannot enter it.**

---

## 3. OBSERVED PRICES — and the split that keeps Brazil alive

| International, self-serve, published price | |
|---|---|
| **Instrumentl** (grant/RFP deadlines) | **$299/mo** annual · $499 · $999 |
| **ImportGenius** (US customs bills of lading) | **$229 · $449 · $1.999 /mo** |
| **Wappalyzer** (website technology data) | **$250 · $450 · $850+** |
| **Coresignal** (firmographic) | $49 · $199 · $499 · $1.000 · $1.500 · $3.000 · $5.000 |
| **Docket Alarm** | $39,99/mo + per-use · **$99/user/mo** |
| **HolidayAPI** | $249 · $399 per year |

| Brazil | |
|---|---|
| **AlertaLicitação** (tender monitoring) | **R$44,90–54,90/month** |
| **★ Speedio** (B2B company/contact data) | **R$719 · R$1.079 · R$1.379 /month**, 12-month lock-in |
| **Escavador** (court monitoring) | R$9,90–49,90 *(SECOND-HAND — page 403s)* |

**The arithmetic, against the corrected target of ~US$11.100/month gross:**

| Band | Subscribers needed |
|---|---|
| Brazilian consumer/SMB monitoring at ~US$8 | **~1.390 — dead** |
| International self-serve niche data at $99–299 | **37–112** |
| **Brazilian B2B data at US$130–250** | **44–85** |

> **The Brazilian CONSUMER monitoring market prices at the floor, exactly like Fiverr. The Brazilian B2B market
> does not — Speedio's observed R$1.079/month is a real, published, on-target band. That single data point is
> what keeps Brazil alive as a market for this shape.**

---

## 4. THE CANDIDATE — the IBS rate-and-effective-date register (2026–2033)

**Chosen for one reason: it is the only dataset found whose ACCUMULATION CLOCK HAS NOT STARTED YET.**

**The source material is Brazil's tax reform.** **EC 132/2023 art. 156-A §1º:** *"V — cada ente federativo
fixará sua alíquota própria por lei específica"* and *"VII — será cobrado pelo somatório das alíquotas do
Estado e do Município de destino da operação."* **LC 214/2025 art. 14** (as amended by LC 227/2026) details it:
each State and each Município fixes its own IBS rate, may peg to the *alíquota de referência* or set a rate
free of it, **and §3º applies the reference rate where no specific law exists.**

> **5.570 municipalities + 26 states + DF, each passing its own rate law, on its own calendar, published in
> its own diário oficial, mostly as PDF — and the tax on any invoice is the SUM of the destination
> municipality's and the destination state's rates.**

**The dataset is not "the rates."** It is **(rate, ente, effective date, source law, source URL, date
observed)**. A tax engine recomputing or defending a 2029 invoice in 2032 needs the 2029 rate.

> **Nobody can back-fill that. It is THE STATE KEEPS STATE, NOT HISTORY in its purest form.**

| | |
|---|---|
| **Buyer** | Brazilian fiscal-software vendors — ERPs, emissores de NF-e, e-commerce tax engines, retail POS, accounting-tech |
| **What breaks without it** | **They compute the wrong tax on every invoice to that destination.** A product defect with fiscal liability attached to their own customers |
| **Constraint side** | Volume set by a statutory calendar they do not control **(EXOGENOUS-VOLUME SPEC satisfied)**; the cost of being wrong is not hours, it is indemnity |
| **Arithmetic** | **~54–85 vendor subscriptions** at the observed Speedio band |
| **Capital** | **Under $500** |
| **Why it cannot be trivially copied** | 5.597 separate legislative acts, in 5.597 publication venues, in Portuguese, over seven years of phase-in. An AI agent can scrape one município; the labour is doing all of them, weekly, for seven years, **and being able to prove what you saw and when** |

### The two honest objections — and the second one is the one to watch

**OBJECTION 1 — THE MOAT-IS-A-CONTRACT TEST: who is paid to abolish this fragmentation?** The **Comitê Gestor
do IBS**, a constitutional body created by **EC 132 art. 156-B** and funded to administer the tax nationally.
It cannot split revenue without a rate table, so it will have one. **The probability that a free official
current rate table appears is high.**

**The residue that survives it, and it is the whole case:** the CGIBS has an operational need for *today's*
rate and **none whatsoever for a version-controlled history with the underlying municipal law attached.**
The state keeps state. **The archive is the product.**

**OBJECTION 2 — and this single number decides the candidate.** LC 214 art. 14 §3º makes the reference rate
the default. **If 95% of municipalities simply legislate nothing, the interesting dataset is only the few
hundred that deviate — thin, and cheap for a rival to replicate.**

> **The deviation rate is UNVERIFIED AND UNKNOWABLE TODAY. No município has set a rate yet.**

**THE TEST, and it costs nothing:** every week, pull the diários of the 100 largest municipalities and count
how many have passed an IBS rate law and how many deviated from the reference. **Twenty weeks of that answers
the entire question before she builds anything** — and it is the twenty-instances-with-a-numeric-bar design
this file already trusts.

---

## 5. THE LEGAL PERIMETER — she gets none of the shield and all of the sword

| | |
|---|---|
| **United States** | **17 U.S.C. §105** — no copyright in US Government works. **No sui generis database right** (*Feist*, 499 U.S. 340). **The safest raw material on earth** |
| **UK / EU** | **SI 1997/3032 reg. 13** creates the right on "substantial investment"; **reg. 18 restricts it to UK nationals, residents and UK-incorporated bodies.** Directive 96/9/EC Art. 11 does the same for the EU *(**SECOND-HAND** — EUR-Lex served a JS challenge and returned 0 bytes to every method; the UK text WAS fetched directly and is the identical structure)* |
| **Brazil** | **Lei 9.610/98 art. 7º XIII** protects a database only where selection or organisation is "uma criação intelectual", and **§2º: *"A proteção… não abarca os dados ou materiais em si mesmos."*** Art. 87 protects only "a forma de expressão da estrutura". **Brazil has NO sui generis database right. Investment alone earns nothing** |
| **LGPD** | **art. 7º §4º** waives *consent* for manifestly-public data — **not the rest of the statute.** Purpose limitation, transparency and data-subject rights survive. A product built on CNPJ *sócios* data is exposed |

> ### THE ASYMMETRY SHE IS ON THE WRONG SIDE OF — a Brazilian resident **cannot acquire** EU or UK database right in anything she builds, **but EU and UK databases are fully protected against her.** She gets none of the shield and all of the sword. **Do not source from EU or UK private databases, and do not expect legal protection for anything she builds.**

**And the correct reading of the scraping cases, which this file had not stated:** *hiQ v. LinkedIn* ended with
the Ninth Circuit reaffirming that scraping public pages is **not** CFAA "without authorization"
(31 F.4th 1180, 2022) — **and then a district court holding hiQ had breached LinkedIn's User Agreement,
followed by a stipulated $500.000 judgment and a permanent injunction to destroy the data and derived
algorithms** *(consent-judgment terms **SECOND-HAND**, corroborated across four firms, docket not pulled)*.

> **The CFAA is not the barrier. THE TERMS OF SERVICE ARE. Public + no login ≠ permitted — and a scraper that
> never registers an account is in a very different position from one that does.**

**The safe raw material, therefore:** US federal works · **UK OGL v3** *(verified: permits commercial
exploitation and expressly licenses "copyright **and database right**")* · EU Open Data Directive 2019/1024 ·
Brazilian *dados abertos* under LAI. **Government open data is the only material that is simultaneously free,
licensed for commercial re-use, and outside the terms-of-service trap.**

---

## 6. WHAT DIED, AND TWO OF THEM WERE MY OWN ASSUMPTIONS

| Killed | Cause |
|---|---|
| **INPI RPI structuring — MY BRIEF WAS WRONG, TWICE** | I told two agents the RPI was "a large weekly PDF and the difficulty IS the moat." **INPI has published structured TXT/XML since 31 Jan 2017, and the archive persists** — `RM2902.zip`, `RM2400.zip` and `RM2000.zip` all return HTTP 200 today. **There is no structuring labour to sell and no head start to gain** |
| **Municipal diário unification** | **THE MOAT-IS-A-CONTRACT TEST, decisively.** Querido Diário / Open Knowledge Brasil is a philanthropically funded nonprofit shipping an open-source crawler fleet and a **free public API** serving PDFs *and* extracted text with no authentication. Its live API lists **5.570 municipalities, 510 already collected.** She would race a funded nonprofit whose entire mission is to give away the thing she wants to sell, **and every município they add deletes part of her inventory** |
| **CNPJ-derived products** | Free bulk CSV, monthly, **with email and phone included.** The government did the work and gave it away; Casa dos Dados, CNPJá, BigDataCorp, Econodata and Speedio hold the head start |
| **Franchise document archives** | **THE HEAD-START ASYMMETRY.** 30+ years and 50.000+ documents already held *(SECOND-HAND)* |
| **Any US federal-data product** | Free, bulk, machine-readable, with weekly deltas already published. **Re-assemblable in an afternoon** |
| **EU-sourced listings data** | Sui generis right + **CJEU C-762/19 *CV-Online Latvia v Melons***, which makes infringement turn on whether extraction deprives the maker of the income needed to redeem its investment |
| **Alt-data to investment funds** | The one buyer segment that pays real money for a small dataset — **and onboarding is diligence calls. C1** |
| **ESG / CSRD statement corpus** | A genuine clock-start, **and THE MOAT-IS-A-CONTRACT TEST with a date on it**: the **European Single Access Point** (Reg. (EU) 2023/2859) begins collection **10 July 2026** *(dates SECOND-HAND)* |

**Third independent confirmation of the CNPJ email field** *(after the S6 agent and the distribution brief)* —
**and the honest verdict on it: it is a genuine asset for any Brazil-facing business in this file, and worth
NOTHING as an S4 product, precisely because it is a free CSV that everybody already has.** It belongs in the
parts bin as a distribution asset, not in a candidate as a product.

---

## 7. THE ONE-LINE VERDICT

> **S4 is not a shape with many doors. Almost every dataset worth owning is already owned by whoever started
> first, and almost every dataset a solo person could start today is either given away free by a government or
> is being centralised by a funded body. The single opening is a CLOCK-START — a dataset that does not exist
> yet because the statute creating it has only just passed. Brazil's IBS transition is the largest clock-start
> in the world right now, in her native language, on her doorstep, closing in 2033.**
