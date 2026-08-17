# THE POSTAL LIST LAW — public registers are mailing lists, not email lists

**17 Aug 2026. S2 hunt, agent 3 of 6. Eight registers opened and field-inspected at scale.**

> **A direct correction to my own claim. I called the Australian celebrant register "the cleanest list
> source in this entire file." It survives — and it turns out to be the ONLY ONE OF EIGHT that publishes
> email at all.**

---

## 1. THE LAW

> **THE POSTAL LIST LAW — a public register gives you name, street address, phone and a licence expiry
> date. It does not give you email. Of eight registers field-inspected, exactly ONE publishes email
> addresses at scale. "Publicly enumerable" and "reachable in writing without a phone" are different
> properties, and the second one is rare.**

**This is not inference. The agent read the published record layouts:**

| Register | Fields | Email? |
|---|---|---|
| **TDLR** (Texas, ~150 free daily CSVs) | Its own spec file lists 23 fields — licence type, number, **expiration date**, county, name, mailing address 1–3, phone, business name, business address 1–3, business zip, business phone, subtype, CE flag | **No email field exists** |
| **FSA** (UK food, free API) | 25 fields returned. Phone field present but **0 of 200 populated in Aberdeen City and 0 of 200 in Amber Valley**. `LocalAuthorityEmailAddress` is the council's inbox, not the business's | **No** |
| **CQC** (UK health, free monthly CSV) | 14 columns. Phone 91,5%, **website 51,7%** | **No** |
| **FAA** (315.798 registrations, free 73MB zip) | N-number, name, street, street2, city, state, zip, county, country, expiration | **No email, no phone** |
| **Florida DBPR** | Main licensee file has no email and no phone. *(Two niche layouts DO carry it: Swimming Pool Licensed Examiners, and Cosmetology Applicants by School)* | Mostly **no** |
| **Chicago** (free Socrata API) | legal_name, DBA, address, licence description, status, expiration, ward, lat/long | **No email, no phone** |
| **TX tattoo & body piercing** | DBA, physical location, rank, expire date — **and no bulk export at all**, one-at-a-time search only | **No** |

> **The registers hand her a MAILING LIST.** A few hundred dollars buys roughly **150–400 international
> letters** — a real test, but a tiny one. The alternative is paying in crawling labour: CQC publishes a
> website for 51,7% of locations, and consumer-facing licensees usually publish an email on their own site.

**Every future "public register = free list" claim in this file must be field-inspected before it is
believed.** Enumerable is not the same as contactable.

---

## 2. THE ONE EXCEPTION — and it is the one already on the board

**Australia's Commonwealth marriage celebrant register, verified by fetching and parsing page 1:**

| | |
|---|---|
| Total records | **10.832** (217 pages × 50) |
| Fields | Name, registration date, status, ceremony type, **mobile phone**, **EMAIL** |
| Sample of 50 records | **29 unique emails (~58%)**, 22 mobiles (44%) |
| Implied reach | **~6.200 working email addresses of sole traders** |
| Bulk export | **No.** ASP.NET WebForms with VIEWSTATE, no JSON API — **217 paginated POSTs to scrape** |

> **Candidate 72's list-source claim holds up under inspection, and it is the only one that does.**

**The agent's honest caveat, which I am not going to soften:** the TAM is small — roughly **A$100–400 per
celebrant per year** across ~10.800 people, and **Australian celebrant-supply shops already sell exactly
the consumable** (commemorative presentation certificates, certificate folders, signing pens). *"This is a
small business, not a large one."*

---

## 3. THE REGULATION–COMMODITY VISE — the second structural finding

> **The more heavily licensed the buyer, the more regulated the thing they consume.**

Verified: **tattoo ink** is restricted under **REACH Annex XVII entry 75** since 4 Jan 2022, with per-batch
per-colour testing and importer obligations · **acupuncture needles** are FDA Class II devices ·
**pesticides** need EPA plus per-state registration · **dental consumables** need UKCA/CE marking.

> **And where the consumable IS unregulated — nail files, massage table paper — it is a commodity the buyer
> already imports direct from China at a price a Brazilian middleman cannot beat.**

**Both jaws close on the same family.** The surviving shape, in the agent's words:

> ***"An unregulated, boring, low-value, high-frequency consumable sold to a small, email-bearing,
> appointment-based population whose incumbent supply is local and lazy."***

That is the narrowest surviving description of an S2 business anywhere in this research, and it is worth
keeping as a filter.

---

## 4. The uncomfortable intersection

| The best… | …has the worst |
|---|---|
| **Registers** — TX beauty (71.302 establishments, 99,9% phone fill, daily CSV), UK food (611.521), FAA (315.798) | Contact data, or buyer |
| **Contact data** — celebrants, 58% email | Wallet — A$100–400/year each |
| **Receptivity** — tattoo artists, genuinely email and DM native, owner-operated, card-paying, continuous disposable burn | **No bulk register anywhere**, and a REACH-restricted consumable |

## 5. And my suspicion about the trades was correct

**Not email-native, and no cold letter fixes it:** HVAC (20.412 TX contractors), electrical, plumbing,
towing, well drilling, vehicle storage.

> *"These are dispatch-and-trade-counter businesses; the purchase is triggered by a job happening TODAY, so
> an international lead time is disqualifying before receptivity even matters."*

**They buy same-day at a trade counter** — Ferguson, Grainger — because the job is today. And the Texas
electrician file is mostly **individuals**: apprentices and journeymen who buy nothing, because they are
employees.

**Email-literate but procurement-gated:** care homes (10.428 residential + 4.493 nursing) and dental
practices (12.279 locations). *"A manager cannot put PPE on a personal card."* **They fail the
one-person-decides test, not the writing test.**

---

## 6. Where S2 stands — four of six agents, four laws, no business

| Agent | Finding |
|---|---|
| **1** | **The rail works.** Self-serve, no-minimum, blind, card-pay. THE CARD-PAY BYPASS |
| **2** | **THE COMPLIANCE COSTUME.** Real mandates exist; the good ones are owned by service companies with vans, and six widely-sold "requirements" are not in the rule text |
| **4** | **THE FREE FRONT DOOR.** "Knowing which part" is bait, not product |
| **3 (this one)** | **THE POSTAL LIST LAW** and **THE REGULATION–COMMODITY VISE** |

**Four for four negative on the business. Four for four productive on laws.**

---

## 7. The convergence worth noticing

**The only email-bearing register in eight is the same register candidate 72 already uses.**

And the consumable that celebrant population buys per ceremony is a **commemorative presentation
certificate** — printed, personalised from names, date and place, manufactured at the point of consumption.
**Same buyer, same list, same immovable deadline — a physical consumable instead of prose.**

> **That is a genuine S1/S2 convergence on one population, and it arrived from two independent directions.
> It is also occupied: the agent confirmed Australian celebrant-supply shops already sell it.**

**Two agents still out:** the merchant-of-record red team, and the director-signature statement family.
