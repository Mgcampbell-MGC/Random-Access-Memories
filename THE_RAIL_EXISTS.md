# THE RAIL EXISTS — S2 does not die on plumbing. It dies on value.

**17 Aug 2026. S2 hunt, agent 1 of 6. Twenty-plus suppliers checked with primary-source fetches.**

> **I expected the supply rail to be the structural kill — no trade account for a Brazilian sole trader
> with no credit history. It is not. Self-serve, no-minimum, blind-drop-ship, card-pay rails exist and
> are verified. That relocates the failure precisely: S2's problem is not the plumbing, it is that
> "knowing which part" is bait rather than product (agent 4). The two findings together are a sharper
> diagnosis than either alone.**

---

## 1. TIER 1 — rails with genuinely zero human quoting

### Global O-Ring and Seal — the winner

O-rings, backup/X/square rings, oil seals, U-cups, **wiper seals**, T-seals, gaskets, cord stock. *"Master
distributor … servicing industrial distributors **worldwide**."*

| | Their own words |
|---|---|
| **Blind ship, self-serve** | *"We remove our company name, logos and other identifying marks from all paperwork, product labels, and shipping labels."* … *"You can also select the option to **Blind Drop Ship** when checking out in our online store. Simply select **Ship to a different address?**, fill in the shipping details, and then select **Blind Drop Ship**."* |
| **Minimum** | *"Minimum invoice is **$1.00 USD net per line, $5.00 USD total invoice**… orders placed on the website [have] a $5.00 minimum."* And: *"If only **17 o-rings** are required, 17 o-rings can be added to your cart"* |
| **The credit bypass** | **Net 30 requires credit approval. Card does not.** |
| Setup fee | None. 15% restocking on returns |
| Language | The site offers **Português** |

**Honest caveat, and it matters less than it looks:** their e-commerce page says *"Your designated Inside
Salesperson carefully reviews every e-commerce order."* **A human reviews on their side — but the price is
already fixed, so it is a review step, not a quoting step.** That distinction is exactly what the business
needs. Prices do render as `$ -` when logged out.

### BuyRegisterRolls — thermal receipt and register paper

> *"All shipments are **blind shipped** without the invoice included. Invoices are sent to email address
> given at the time of check-out."*

**Blind shipping is the DEFAULT on every order** — no request, no note, no negotiation. **Public prices with
no login** (the only supplier reached where net prices are visible to an anonymous browser), free shipping,
reseller SKUs at 50-roll cases for $29,99–84,99.

**Two problems:** *"does not ship outside the U.S. and U.S. Territories,"* and a boilerplate ToS clause
reserving the right to *"limit or prohibit orders that… appear to be placed by dealers, resellers or
distributors"* — **which directly contradicts their own reseller collection.** Settle by email before
building on it.

### Copylite — and this is the single most encouraging artefact for her specific constraint

Printer and copier consumables, 5.000+ parts, warehouses in FL, TX, PA, NV.

> *"As a reseller, **we never sell to end users. Your customers are yours, always.**"*
> *"Every package is unbranded and packed to perfection, keeping your business front and center."*

**And the finding:** their reseller registration form is headed *"APPLY FOR ACCESS — RESELLERS ONLY PLEASE"*
and **its required Country dropdown lists BRAZIL**, with dedicated *"Reseller ID"* and *"State(Other/INTL)"*
fields.

Blind drop-ship is currently requested by **a fixed string in the order Notes field** — trivially
automatable. Prices and minimums are behind login: **UNVERIFIED.**

---

## 2. THE FOUR CROSS-CUTTING BLOCKERS — the real content of this report

### Blocker 1 — the wall is the CREDIT GATE, not the blind-ship policy

Blind-ship policies are abundant and generously worded. **Account opening is what kills.**

**DLS (teamdls.com)** is the best-worded trade-only blind-ship label converter in the category —
*"We sell ONLY through OEMs and value-added resellers like you… we don't compete with you on bids"* —
and its credit application demands **a US resale or tax-exemption certificate, a DUNS number, years in
business, a bank name and account number, and at least three trade references, signed by a company officer.**

**She has none of the five.**

> **THE CARD-PAY BYPASS — the workaround is not negotiation. It is choosing suppliers whose CARD-PAY
> account skips credit approval entirely.** Global O-Ring states it outright: Net 30 is *"upon credit
> approval,"* card is not.

*(Tax nuance: a resale certificate only exempts her from sales tax. A supplier can sell to a non-exempt
buyer and charge it — a margin problem, not a hard block. But HEPA Filter Sales makes the tax-exempt form a
listed step, so for some it IS a block.)*

### Blocker 2 — net prices are published almost nowhere, and there is no API

**Of everything reached, exactly ONE supplier shows net reseller prices to an anonymous browser.** Global
O-Ring renders `$ -`. IMP's portal is gated on *already being a customer*. ARMOR-IIMAK issues credentials
through an account manager. Advanced Safety Devices releases prices only *"after your application accepted
and the Dealer's agreement has been signed."*

> **No public ordering API was found in any of the seven categories. Automation means an authenticated
> session against a web store, not a documented API.**

### Blocker 3 — blind shipping is a DOMESTIC guarantee that breaks at the border

Two independent mechanisms:

- **Dangerous goods:** DG documentation must name the manufacturer origin, so **lithium cells cannot ship
  blind by air at all.**
- **Export filing: 15 CFR 30.6** requires the USPPI's name, address of origin and identification number on
  the Electronic Export Information — and **the USPPI is the party receiving the primary benefit, i.e. the
  supplier, not her.**

Plus **Gentek**: blind drop-ship *"offered only for shipments to businesses and are not available for
residential addresses."*

> **She needs ONE DOMESTIC RAIL PER TARGET COUNTRY, not one global rail. Launch USA-only.** UK, EU, Canada
> and Australia each require their own domestic supplier later.

### Blocker 4 — explicit non-US-seller exclusion is live

**Crystal Quest, flatly:** *"we do not have a drop shipping program for international sellers,"* and
*"our drop shippers may be located only in the United States and Canada."*

**Copylite is the counter-example** — and the only one found that names Brazil in a registration form.

---

## 3. Verified kills

| | |
|---|---|
| **Donaldson** | From their own Terms of Sale PDF: *"Seller will not make any 'drop shipments' to Buyer's customers unless Seller, **in its sole discretion**, deems it necessary."* The category's biggest name contractually refuses |
| **Batteries** | Worst fit of the seven. BatteryClerk: *"we typically reserve wholesale orders for anyone spending over $1000,"* quoted through an account manager. Plus lithium DG paperwork must name the manufacturer |
| **Safety / calibration consumables** | Move exclusively through brand-authorised distributor networks — 3M, Honeywell, MSA, Industrial Scientific. The one blind-drop-shipper found runs a **competing retail storefront** and won't publish prices |
| **Lab, dental, veterinary** | **Kill the category.** The one $0-fee programme with visible prices explicitly does not drop-ship, and distributors gate on proof of professional licence |
| **Filters — split verdict** | The **identification half is solved and free**: Baldwin Filter Finder, Donaldson cross-reference, FilterXRef, parts-crossreference.com. **The supply half is not**: Pleatco, Permatron, HEPA Filter Sales and Smith Filter all confirm private-label drop-ship in writing but **none publishes net prices**, most are made-to-order with multi-week lead times, and Permatron and HEPA Filter Sales **sell direct to end users** |

**Unreachable, recorded:** dlsonline.com is parked at HugeDomains (the real DLS is teamdls.com) · Valley Forge
blocked by captcha, and its own indexed text says *"they are not a 'to the trade only' label company"* — i.e.
**it competes with resellers** · Supplies Network 301s to a domain that does not resolve in DNS · SCN
Industrial, Smith Filter and Certified Safety all bot-blocked.

---

## 4. What this does to the S2 verdict

**Three findings now sit together and they do not contradict — they localise the failure:**

| Agent | Finding |
|---|---|
| **1 (this one)** | **The rail works.** Self-serve, no-minimum, blind, card-pay, Brazil-tolerant in at least one case |
| **4** | **The value proposition does not.** "Knowing which part" is the free front door to a stocking distributor's product margin. Grainger sells it as a service line; CrossFilters gives away *manual* crossing in one business day and advertises *"Real inventory, not just data"* |
| **2** | Real mandates exist, but the good ones are owned by service companies with vans, and six widely-sold "requirements" are not in the rule text |

> **So S2 does not die on plumbing. It dies on the same thing that has killed everything else in this file:
> she can buy, she can ship, she can be invisible — and there is no reason for the customer to buy from her
> rather than from the source.** The rail is necessary and nowhere near sufficient.

**What genuinely survives, and it is a capability rather than a business:** with BuyRegisterRolls she could
run a storefront with **literally zero setup, zero inventory and blind shipping by default.** The plumbing is
free. **The missing piece is a buyer who cannot or will not reach the source — which is distribution, the
constraint that has killed seventy-two candidates.**

---

## 5. The one question no website will answer

**Every finding above is UNVERIFIED on a single point: whether a Brazilian-issued card and a Brazilian
company registration are accepted.**

**It is a five-line email per supplier, and it should be tested before anything else**, because it is the
constraint most likely to kill the whole structure. The agent's recommended order, all written, no calls:

1. **Global O-Ring** — apply as a Brazilian entity, card-pay not Net 30. Ask: can a Brazil-domiciled company
   hold a commercial account · will a Brazilian card be accepted · does the Blind Drop Ship checkbox work for
   **residential** US ship-to · what appears as shipper on international ship-tos
2. **Copylite** — register selecting BRAZIL; ask minimums, whether a Reseller ID is mandatory, and whether
   the Notes-field blind-ship instruction can become a **standing account default**
3. **BuyRegisterRolls** — will they accept a Brazilian billing address with US ship-to, and does the
   anti-reseller ToS clause apply to their own reseller SKUs
4. **IMP** — portal access as a *new* reseller, plus carton counts per stocked size
5. **ARMOR-IIMAK** — partner onboarding in writing; can credentials be issued without a call
6. **Skip entirely:** DLS (credit-app wall) · Crystal Quest (bans international sellers) · Donaldson (refuses
   drop-ship) · lab, dental and veterinary (licence gate)
