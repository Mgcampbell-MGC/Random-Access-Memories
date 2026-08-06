```markdown
## Graveyard

### LINELOCK — packaging artwork proofing
**Cause of death:** the checking job it promised is already sold, at three price points, by tools already inside the buyer's workflow.
**Cheapest adequate substitute:** free diff-pdf + Artwork Flow free tier (US$0). Also present: Acrobat Pro Compare Files, US$19,99/mo. Also present, and fatal on its own: ManageArtworks, US$399/mo, self-serve, 14-day trial, no card — markets the exact "check artwork against approved pack copy" feature as a named capability.
**Rule broken:** R1 (identical product to identical buyer already shipped, by ManageArtworks) and R6 (trigger — an agency about to send a proof to print — is invisible from outside).
**Never resurrect because:** the differentiator was already a line item in a competitor's feature list, and there was no way to see, from outside, that any specific agency had a proof going to print today.

### RIO BLOCKS — swimwear pattern library
**Cause of death:** the identical downloadable product is already on the market at commodity prices, and the plan depended on a named human Sol would owe a royalty to.
**Cheapest adequate substitute:** Stella Luna & Co's downloadable swimwear production package (whole job, identical format). Also present: Minerva DXF files at US$3; Etsy bundles at US$15-25.
**Rule broken:** R1 (identical product, identical buyer, already shipped) and R6 (the trigger — a buyer needing a swimwear pattern — fires once per buyer, ever, not recurring).
**Never resurrect because:** a US$3 Minerva DXF file already does the whole job, and even without that, the pattern-library purchase is a single lifetime event per buyer, not a repeat trigger.

### AI INFRASTRUCTURE CREDIT LAB
**Cause of death:** established credentialed publishers sell the identical analysis cheaper, and the delivery mechanism requires infrastructure (a Python runtime, an LLM) the buyer's own employer often blocks.
**Cheapest adequate substitute:** ELFA Financial Statement Analysis, US$475-500/licence. Also present: CFI All Access, US$497/YEAR — an order of magnitude cheaper per unit of coverage.
**Rule broken:** R1 (ELFA and CFI already sell this to this buyer) and the delivery-format rule (needs a Python runtime and the buyer's own LLM access, which the buyer's employer — a bank — frequently blocks by policy), which is also the worst approval-threshold exposure of the six candidates.
**Never resurrect because:** CFI already sells broader coverage for US$497/year against a candidate priced at US$250-750 for less, and the product cannot even run inside a bank's locked-down environment.

### PITCH & PAID
**Cause of death:** it was a prompt file wearing a price tag, sold to consumers, against free substitutes.
**Cheapest adequate substitute:** identical script packs on Etsy at US$20,55; free rate-card templates also exist.
**Rule broken:** R3 (fully reproducible by one competent prompt) and the B2B-only constraint (it was B2C, which the EU VAT/reverse-charge rails and the whole business model exclude).
**Never resurrect because:** a single paste-and-one-paragraph prompt delivers the same output reliably, and free templates already exist for the parts that aren't just prompting.

### WRAPCHECK BEAUTY
**Cause of death:** genuinely no SaaS competitor undercuts it, but a free spreadsheet does the same job, and the trigger window is invisible and only hours wide.
**Cheapest adequate substitute:** free Google Sheet grid + COUNTIF against the filename export (US$0). Named non-substitute for context only: no SaaS competitor exists under US$3.583/mo.
**Rule broken:** R3 (reproducible in one prompt/one spreadsheet formula) and R6 (trigger is invisible, at best monthly, and only live for a few hours per occurrence — the worst trigger shape in the whole set).
**Never resurrect because:** even with zero SaaS competition, a free COUNTIF formula finishes the job, and there is no external signal that tells Sol which brand has a live set right now.

---

## What these five deaths add to the filter set

1. **"No SaaS competitor" is not evidence of an opening — it can mean the job is too small or too cheap to formalize into software.** WRAPCHECK had zero competitors above a free spreadsheet precisely because the underlying task (a COUNTIF-shaped check) doesn't justify SaaS-level tooling for anyone. Absence of competition at the SaaS layer should trigger the question "can a free primitive already do this?" before it's read as whitespace.

2. **A named feature inside someone else's platform kills a standalone product just as dead as a dedicated competitor.** LINELOCK didn't die to a rival "artwork checker" — it died to one bullet point in ManageArtworks's feature list. For downloadable digital products specifically, check not just "who sells this" but "who lists this as a sub-feature of something bigger," because that buyer has already paid for the capability as a rounding error.

3. **Lifetime-frequency triggers (buy-once-ever) are a structural death for a downloadable product even absent any competitor.** RIO BLOCKS would have died on trigger frequency alone — a pattern purchased once per swimwear buyer, ever, can't sustain repeat revenue no matter how defensible the artefact. Screen every candidate for "does this buyer ever need this again" before checking competitors at all.

4. **Regulatory/institutional buyer constraints on the delivery environment are a distinct kill from price or competition.** The Credit Lab candidate died partly because banks block LLM access by policy — a structural fact about the buyer's environment, not about the market. For any candidate whose delivery format assumes buyer-side compute (a runtime, an LLM, a plugin), check what the buyer's own IT policy permits, not just what the buyer would prefer.
```