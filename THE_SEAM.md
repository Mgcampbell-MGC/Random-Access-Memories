# THE SEAM — what the archive was hiding, 19 Aug 2026

**Eight Brazilian regulatory-clock business plans mined for components rather than evaluated as candidates.
The finding is not in any one of them. It is in the shape all eight share.**

---

## 1. ★★ THE SEAM

**Every one of the eight plans splits cleanly at the same joint, and none of them notices:**

| | **THE CLOCK HALF** | **THE EXECUTION HALF** |
|---|---|---|
| Cost shape | **FIXED — one harvester serves every CNPJ in Brazil** | **PER-CUSTOMER — 2 to 30 founder-hours per unit** |
| Credential | **None. Reads only public records** | Council-registered *Responsável Técnico* signature → **EXPERT VETO** |
| Access | **None. Free public consultation + free DOU feed** | Portal login + the client's *Caixa Postal Eletrônica* → **CREDENTIAL VETO** |
| Conversation | **None. Computed and delivered** | Scope, onboarding, exigência escalation → **SPEECH VETO** |
| Verdict | **Clears all four constraints** | **Breaks all four at once** |

> ### **SEVEN OF THE EIGHT PLANS PRICE ONLY THE EXECUTION HALF — AND GIVE THE CLOCK HALF AWAY FREE AS A LEAD MAGNET.**
>
> **The agent's closing line, and it is the most valuable sentence in the archive:**
> ***"Nobody in the archive ever tested whether the free Raio-X is itself the product."***

**The one file that DID price detection separately — ORIGEM — is also the only one that solved *"may never
opine"*, and it solved it with a closed vocabulary rather than a credential.** Those two facts are the same
fact.

---

## 2. THE THREE CLOCKS, RANKED BY CONSTRAINT COMPATIBILITY

### ★ CLOCK 3 · PROVA DE PORTE — the cleanest object found anywhere in the archive, treated as a throwaway line

| | |
|---|---|
| **The window** | **Opens 1 January, closes 30 April** for ME/EPP *(Junta Comercial simplified certificate)*; 30 June and the ECF deadline for other tiers. All three dates the file marks VERIFIED |
| **Consequence of missing it** | *"Automatic reclassification to Grupo I – Grande, no discount, no reimbursement"* |
| **Priced exactly** | TFVS for *Registro de cosméticos* is **R$2.500**, with reductions of **30% medium / 60% small / 90% micro** *(Lei 9.782/1999 Anexo II)* → **R$1.750 / R$1.000 / R$250**. For a Grupo III client that is **R$1.750 versus R$2.500 per registro, multiplied across a portfolio** |
| **How you know it started** | **It is a FIXED CALENDAR DATE, not an event. No gazette, no notification, no lookup, no data access of any kind** |
| **Recurrence** | **Annual, per company, forever** |
| **Who supplies the document** | **The client's own ACCOUNTANT** — so no credential of hers is involved at any point |

> **Fully fixed-cost. Clean on all four constraints. No expert judgement — the date is in a statute and the
> arithmetic is division. And the archive mentions it as a line item inside someone else's retainer.**

### CLOCK 1 · CONTINUIDADE DECENAL — the biggest pool, and the detection half is free

**RDC 907/2024 art. 41 and RDC 312/2019 art. 2 §2º.** The window **opens at `termo_fim − 6 months`** and closes
at `termo_fim` — the last six months of each product's ten-year term. **One clock per SKU, not per company**,
so a portfolio of 100 SKUs with staggered launches opens windows continuously, every month, forever.

> **Missing it CANCELS THE REGULARIZAÇÃO** — art. 2 §3º. The product loses its right to be sold in Brazil.
> **And nobody is notified.**

**The detection source is free and public:** ANVISA's consultation is **searchable by titular CNPJ and by
process-expiration period** — *the expiry-period filter is literally a "whose clock is running out" query.*
The DOU is the durable second source: **free daily PDF and XML via INLABS since 01/01/2020, with official
download scripts published by Imprensa Nacional.**

**Two honest limits:** the consultation is a JavaScript SPA with no documented public API *(a third-party
wrapper died after a redesign)*, and **INLABS only covers the DOU from 01/01/2020, so acts granted 2016–2019
sit outside the machine-readable window.**

### CLOCK 2 · MIGRAÇÃO SGAS — a real deadline that manufactures its own future pipeline, and a fatal unknown

**RDC 951/2024 art. 3:** migration must happen inside the legacy system's validity *or the regularização is
cancelled.* **Art. 6** grades the commercial consequence: migrate by 31/12/2026 and the old label may be used
six years; by 31/12/2028, four; from 01/01/2029, two. **Migration costs nothing in government fees, and
migrated products receive a fresh ten-year term.**

**Killed as a business by two things the file states itself:** *"Migration is once per SKU… the annuity the
plan describes is a decade away,"* and **nobody — including ANVISA — publishes how many unmigrated
regularizações remain.** *(VERIFIED negative: ANVISA publishes 23 analytical panels and none covers cosmetics.)*

---

## 3. THE FOUR MECHANISMS WORTH MORE THAN ANY OF THE EIGHT BUSINESSES

### ★ MECH-3 · THE CLOSED VOCABULARY — the artefact that lets a non-expert ship a paid deliverable

**From ORIGEM. The purest answer to the expert veto found anywhere in this project.**

**A closed set of permitted final statuses:** `DEFINED DIFFERENCE EXPLAINED` · `DEFINED DIFFERENCE REMAINS` ·
`EVIDENCE MISSING` · `NOT FOUND IN NAMED DATASET` · `SOURCE UNAVAILABLE` · `FIELD OR LEGAL REVIEW REQUIRED` ·
`OUT OF SCOPE`

**Paired with an explicit banned-word list:** *"Never use: 'No embargo,' 'no forced labor,'
'deforestation-free,' 'legal,' 'compliant,' 'low risk,' 'cleared,' 'approved,' or 'sufficient.'"*

**And the safe form, quoted:**
> ***"No matching record was found in the named dataset and edition as of the recorded retrieval time."***

**Every statement also carries eight provenance fields** — observed fact · named source and edition ·
retrieval timestamp · query key · method version · coverage limitation · documentary status · operator-review
reminder — **plus a list of what public sources cannot prove, handed to the buyer up front.**

### MECH-1 · THE COMPUTED FREE DIAGNOSTIC

From **nothing but a CNPJ**: every SKU in the public record, its process number, which system it sits in,
status, term end date, **every computed statutory window with days remaining**, misclassification flags and
DOU enforcement history. *"Deliberately free because it is computed, not laboured."*

**Transplantable to literally any register with a per-entity expiry field.**

### MECH-7 · THE DEADLINE ENGINE AS A PURE FUNCTION

`RegraModulo × Regularizacao → Janela[]`, **idempotent, so a corrected rule retro-corrects every case.**
Business-day versus calendar-day is **stored on the rule, never inferred**, backed by a maintained national
holiday table. **The idempotence is the point: rules can be wrong and later fixed without touching cases.**

### MECH-8 · SUCCESS VERIFIED ONLY AGAINST THE PUBLIC RECORD

*"`VERIFIED_SUCCESS` is set only when a machine check finds the expected identifier with the expected status
and a publication date consistent with the filing. A human saying 'it went through' does not set this state,
and neither does an AI reading a screenshot."*

> **It converts an unfalsifiable service claim into a third-party-verifiable artefact — which is exactly what a
> seller who cannot be believed requires.**

*(Also kept: **MECH-11**, the client pays every government fee directly in their own name — which removes the
merchant-of-record and custody problem by design rather than by argument. And **MECH-16 Rule 5**, client-caused
delay pauses the case: *"ENTRA does not maintain an infinite human follow-up loop."*)*

---

## 4. THE CAUSES OF DEATH THAT NOW SCREEN EVERY FUTURE CANDIDATE

**★ COD-4 · TEST THE CONSEQUENCE'S FREQUENCY, NOT ITS SEVERITY.** From PRUMO, verbatim: *"Across 45.863
projects, **84 prestações de contas were reproved — 0,18%, roughly one in 550.** Selling this as insurance
against a three-year ban would be selling protection against a loss that almost never lands, and that is
precisely the mistake that killed three earlier candidates."*

**COD-13 · THE RIGHT TO ACT WAS ASSUMED, NOT VERIFIED.** VIGENTE's own attack A21, which it rates fatal:
*"OPEN: what representation the portal requires for a third party to petition; OPEN: whether delegated access
to a client's Caixa Postal Eletrônica is legally clean."* **That is the C4 credential constraint appearing,
unrecognised, as the plan's most serious unaddressed risk.**

**COD-6 · THE PRIVATE TRIGGER.** *"The event happens inside a franchisor's legal team and a WhatsApp
negotiation."* **Three independent files died on this same defect** — VIRA, ENTRA and PRATELEIRA.

**COD-9 · THE REGULATOR'S OWN PAGES ARE WRONG.** *"ANVISA's own frequently-asked-questions pages still cite
[a resolution] revoked in full… and still instruct users to petition through SGAS, a system retired on
07/04/2025."* → *"any tool, adviser or language model that trusts the official pages is wrong about the current
rules."* **The asset is knowing the current rule. The liability is that no source is authoritative, including
the authority.**

**COD-10 · THE DIRECTION OF TRAVEL IS DEREGULATION, and there is no mitigation for one thing.**
Lei 15.154/2025 exempts artisanal cosmetics from registration; RDC 949/2024 gives until 2030. And the flat
statement: **"Against ANVISA publishing a cosmetics expiry panel, there is no mitigation."**

**COD-14 · THE QUALIFYING VARIABLE IS PORTFOLIO SIZE, NOT REVENUE.** *"A R$5m company with 60 legacy SKUs is
a better client than a R$40m company with eight."*

**COD-1 · AND THE ONE SURVIVING CRACK, quoted:** *"Legacy SKUs from vanished suppliers and former employees
are unowned. That crack, and only that crack, is the business."*

---

## 5. WHAT THIS OPENS — the question the archive never asked

**If the clock half is fixed-cost, credential-free, conversation-free and computed from a free public source —
then the clock half is the only part of these eight businesses she can actually own.**

**And there is a buyer for detection who is not the buyer for filing.** The archive enumerates **38 Brazilian
regulatory consultancies by name, and records that 20 of 20 examined publish no price, no online checkout, no
dashboard and no SLA.** They are relationship-sold firms with the credential, the portal access and the client
relationship — **and no systematic way of knowing whose clock is running out.**

> **That is THE WHOLESALE ESCAPE, arriving from a completely different direction: she supplies the detection
> machine; they supply the face, the signature and the liability.**

**Three things must be settled before this is a candidate rather than a hypothesis, and all three are cheap:**
1. **Is the universe big enough?** 3.630 sector companies and 3.280 active CNPJs are the denominators — but
   **how many SKU windows are open in any given month is `[OPEN]` and settleable directly from the
   expiration-period filter.** One afternoon.
2. **Is the buyer the consultancy or the brand?** 38 consultancies at $11.100/month is ~$300 each at 100%
   penetration — **tight, and possibly too small.** The brand-side universe is 100× larger and pays less.
3. **Can the SPA actually be harvested at scale, lawfully?** No documented API, and MECH-5's source-access
   matrix is the discipline that answers it.

**Three miners and the capability agent are still out. This is the first half of an answer, not the answer.**

---

# PART TWO — THE RECOVERY FAMILY. Same seam, different direction.

**Eight money-recovery plans mined. The structural finding is independent of the regulatory slice and lands in
the same place.**

## ★★ THE RECOVERY COUPLING

> **Credential access and action path are INVERSELY COUPLED.**
>
> - **The variants with a real claim against a third party who owes money REQUIRE A LOGIN.** VOLTA needs OAuth
>   into the seller's Mercado Livre and Mercado Pago; DisputeKit *is* a Stripe App with OAuth into the
>   merchant's account. *(Note VOLTA's own defence — "sellers never provide VOLTA with their passwords" —
>   **OAuth is standing access. The doc does not notice this.**)*
> - **The variants that are genuinely FILE-ONLY have NO THIRD PARTY WHO OWES ANYTHING.** The Raio-X and Escopo
>   Pago "recover" money by asking the customer's own customer for it.
> - **Exactly one file breaks the coupling, and it does it with one move: THE CREDENTIAL IS GRANTED TO A
>   PARTNER PROFESSIONAL, NOT TO THE OPERATOR.** Caixa de Volta works from NF-e XML and SPED files she is
>   emailed; a partnered *contador* holds the e-CAC *procuração* and files.

**That is the wholesale escape again — third independent arrival today.** *"The AI does the dreaded 90%; the
partner does the signature, not the labour."*

**⚠ And its load-bearing legal claim is UNVERIFIED.** The file asserts *"the restitution request can be made
by any professional with the technical knowledge — it does not strictly require an accountant or lawyer"* and
**cites no statute, IN or regulation.** That single sentence carries the only variant that beats the
credential problem.

---

## THE MECHANISMS WORTH MORE THAN THE EIGHT BUSINESSES

### ★★ M24 · BLIND MODE — privacy as a PRODUCT, not a promise

**A single HTML file the client runs on their own computer.** It hashes phone numbers and strips names before
anything is uploaded; **the same salt goes on the second export so the join still works;** she never receives
an identifier.

Offered as the answer to what the file calls the best objection in the sales process — *"'I can't send
customer conversations' — the best objection, it means they're serious"* — with the line:

> ***"I never see who they are, and I can still cross-reference. You keep the key."***

**This is the strongest object in the archive for a founder forbidden from holding customer data. It is
build-once, ship-to-everyone, and it converts C4 from a limitation into a differentiator.**
*(Mechanically: `sha256(SALT + normalised_phone)[:10]`, per-client salt never reused. **And the gotcha the file
flags: normalise before hashing — strip +55, spaces, parens, and handle the Brazilian mobile 9th-digit
inconsistency, "or the join silently fails on a third of rows and she won't notice."**)*

### ★★ M14 · THE FEE THAT TAKES ITSELF

Her fee is a **split executed at settlement inside the client's own payment account** — a `walletId` and a
percentage, applied when the money actually lands, **refund-symmetric** (a refund reverses the fee, a partial
refund reverses it pro-rata). Rail fees are read live from the API, never hardcoded.

> ***"There is no reconciliation fight, no 'that client would have come back anyway' invoice dispute, no
> chasing. The fee takes itself, only when money actually lands."***

**For a founder who cannot get on a call to argue an invoice, this may be the single most valuable component
in the entire archive.** *(Its own kill gate is honest: test an unlinked split to an **independently
registered** account — *"never via POST /v3/accounts — that tests the wrong thing"* — sandbox then R$5 live.
A 400/403 is a NO-GO.)*

### ★ M16 · THE MARGIN GATE — *"The refusal is the trust product"*

Software that **refuses to propose any campaign** leaving the customer under 15% net after commission,
consumables, taxes, rail fee and her own fee.

> *"Every incumbent and agency will happily run a campaign that loses the salon money, because they are paid
> either way. Caixa Cheia is the only vendor whose software says 'não' to a bad package."*

**And the Raio-X prints the refusal rather than hiding it. That is a credibility substitute for an expertise
she is not allowed to claim.**

### ★ M11 · THE BLANK-COLUMNS RITUAL — an S4 engine hiding inside an S1 deliverable

The recoverables spreadsheet ships with its last three columns — `enviado_em`, `respondeu`, `agendou` —
**deliberately blank. The client fills them in.**

Three effects: it turns the report into a work tool · it creates the reason to return in 30 days · **and it
generates her measured recovery rate, "the asset nobody else has."** *"If she implements nothing else,
implement this."*

> **A compounding dataset harvested for free from the customer's own follow-through.**

### ★ M19 · PICK THE ROUTE WHERE THE HOLDER ADJUDICATES BEFORE PAYING

*Compensação* offsets immediately — fast, but an un-homologated offset can draw an **isolated fine of 50%**.
*Restituição* asks for cash and the authority reviews first.

> *"With restitution, the worst realistic outcome is a reduced or denied claim, or a clarification request —
> **never 'recovered, then clawed back with a penalty.'**"*
>
> **Generalised: prefer the claim route where the money-holder adjudicates BEFORE releasing, so a wrong claim
> costs a "no" rather than a clawback plus a penalty.** The most portable risk-shaping idea in the slice.

### ★ M4 · THE A/B/C MODEL — never blended

**A — gross unconverted opportunity**, labelled verbatim *"This is NOT lost money. It is the size of the
playing field."* · **B — loss attributable to a specific named failure**, every row defensible against a
conversation ID · **C — still credibly recoverable.** Absolute rules: never present B or C as guaranteed ·
every value traces to **the client's own price list, never a market average** · **where a price is a range,
use the floor.**

**The cleanest anti-fabrication device found anywhere in the archive.**

### ★ M22 · GUARANTEE THE DIAGNOSIS, NEVER THE OUTCOME — and know why it is safe

*"If I don't document at least 3 actionable booking failures in the sample, I refund the R$490."*

> **And the file explains why that is safe to offer: three of the four commonest failures are DETERMINISTIC,
> so in a real 40-conversation sample the probability of finding fewer than three is near zero. She is
> guaranteeing something she can COMPUTE.**

### M26 · RISK-BASED REVIEW — the only card that costs the hours down

First three runs: review ≥20 cases, every failure category, every ambiguous join, best and worst, 5 random
controls. **Mature monthly: only low-confidence labels, disputed joins, the top 10% of value, a 5-case random
control — target 3–7 MINUTES per client.** Rejection rule: *"more than 2 errors in a 10-case check → reject
and re-run the batch (do not hand-patch — a 20% error rate is systemic)."*

> **Everything else in the slice that reviews each case by hand is dead on hours. This is the difference
> between a desk and a job.**

### And four more kept in one line each

**M1 — *"The model may label. Only code calculates."*** *(Three files re-derive this independently.)* ·
**M23 — score the FUNCTION, never a named individual**: *"O fluxo de agendamento tem atrito"* never *"a
Profissional C converte mal"* — *"same finding, same actionability, completely different legal artifact"* ·
**M28 — the anonymised sample artefact**, a fully built watermarked report for a fictional client:
*"converts 'I do reception audits' into an object an owner understands in 90 seconds. Build it before selling
anything"* — **it replaces credibility-by-person with credibility-by-object** · **M10 — schema fingerprints
plus 150–200 golden fixtures**, which is what makes audit #12 cost a fraction of audit #1.

---

## THE TWO DEATHS THAT GENERALISE

**★ THE INTAKE DEATH — the deal dies AFTER the sale.**
> *"WhatsApp's native export works on one chat at a time. There is no 'export all conversations' button. There
> never has been. Do the arithmetic: 400 conversations at ~45 seconds each is five hours of receptionist
> labour to produce the input file. **Nobody will do that. The deal dies at intake — after she's sold it.**"*

**Ask of every file-in candidate: how many minutes of the CUSTOMER'S labour does the input cost?**

**★ THE JOB WITH BETTER MARGINS.**
> *"Twelve hours of her judgment per client, R$3.900 a time, caps at roughly R$33k/month and never moves.
> **That's a job with better margins, not a business.**"*

*(And one buyer-qualification line worth stealing outright — the disqualifying question is "what is your
conversion rate?": **"a number → disqualify, they have a system; a pause or a laugh → the sale just closed
itself."**)*

---

## WHERE THE TWO SLICES AGREE

**Two miners, sixteen plans, two unrelated industries, one conclusion:**

| | Regulatory slice | Recovery slice |
|---|---|---|
| **The constraint-clean half** | Compute the statutory window from a free public register | Compute the discrepancy from a file the customer emails |
| **The half that breaks everything** | File the petition — needs a signature, a portal login, a conversation | Claim the money — needs a login, or there is nobody who owes it |
| **The one file that escaped** | ORIGEM — solved *"may never opine"* with a **closed vocabulary** | Caixa de Volta — solved the credential by **giving it to a partner** |

> **Both slices independently found that the COMPUTATION is ownable and the ACTION is not. And in both, the
> archive priced the action and gave the computation away.**
