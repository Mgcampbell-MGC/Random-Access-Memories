# THE RETRIEVAL ANSWER — AI answer engines as a channel, 19 Aug 2026

**The founder's correction: *"SEO is dead or dying fast, really needs to be some kind of AIEO to survive in
2026 and on."* Taken seriously rather than waved away. Seven questions, primary sources only, and a topic
whose literature is ~95% content marketing.**

> **It matters more for her than for almost anyone, because BEING CITED BY AN AI ASSISTANT REQUIRES NO FACE,
> NO NAME, NO AUDIENCE AND NO VOICE. It is the only discovery channel found in this project that is NATIVELY
> compatible with C1 and C2 rather than merely tolerant of them.**

---

## 1. THE CRUX — retrieval, not training. The lag is DAYS, not years.

**Every provider runs a SEPARATE crawler fleet for retrieval than for training, and documents them
separately.**

| Product | The provider's own words | Citation bot | Training lag? |
|---|---|---|---|
| **ChatGPT search** | `OAI-SearchBot` *"is used to surface websites in search results in ChatGPT… Sites that are opted out of OAI-SearchBot **will not be shown in ChatGPT search answers**."* `GPTBot` is a **different** bot, for training | `OAI-SearchBot`, `ChatGPT-User` | **No** |
| **Claude web search** | *"direct access to **real-time** web content… **beyond its knowledge cutoff**."* `Claude-SearchBot` vs the separate training `ClaudeBot` | `Claude-SearchBot`, `Claude-User` | **No** |
| **Perplexity** | `PerplexityBot` is for *"search results indexing only"* and is *"**not** used to crawl content for AI foundation models"* | `PerplexityBot`, `Perplexity-User` | **No** |
| **Google AI Overviews / AI Mode** | *"a page **must be indexed and eligible to be shown in Google Search with a snippet**."* Google-Extended (training) *"does not impact a site's inclusion in Google Search"* | **Googlebot** | **No — but index-gated** |

### ★ The natural experiment that settles it empirically

**The agent found, by accident, a site that was retrieved FIRST for a specification query — and then pulled
its robots.txt:**

```
User-agent: GPTBot           Disallow: /
User-agent: ClaudeBot        Disallow: /
User-agent: Google-Extended  Disallow: /
User-agent: CCBot            Disallow: /
```

> **It blocks every major TRAINING crawler in existence and blocks none of the RETRIEVAL bots — and it was
> cited first anyway. A site provably absent from the training corpora of OpenAI, Anthropic, Google and Common
> Crawl was still the top source.**

**Second confirmation:** content published **two days** before the test — a personal Substack with no public
profile — was retrieved alongside CNN. **No training cycle explains that.**

### The one real asterisk, and it forces a correction to this file

Google's AI surfaces are **index-gated**. But **Xu, Iqbal & Montgomery (arXiv:2605.14021, 55.393 queries over
40 days)** measured that **29,8% of AI-Overview reference domains do not appear anywhere on the corresponding
first page**, concluding the system draws on *"a source pool and prioritization system distinct from its own
ranking algorithm."*

> ### CORRECTION TO `CLAUDE.md` — "SEO is dead" is too strong, and the two halves must not be collapsed. **BEING INDEXED by Google and Bing is a hard prerequisite, and it is free, fast, written-only and takes an afternoon. RANKING is what stays out of reach.** Indexation ≠ ranking.

---

## 2. IS IT BIG ENOUGH? No — and the prior was right, in exactly those terms

| | |
|---|---|
| AI-platform referral visits, June 2025 | **1,13 bn** |
| Google search referrals, same month | **191 bn** |
| **AI share** | **~0,6%**, growing **+357% YoY** |

*(Similarweb's own measurement. Panel-derived, and Similarweb sells in this category — **order of magnitude
only**.)*

> **A channel growing 10× off a base of 0,6% is at 6% in eighteen months, and 6% of a channel she was never
> going to win outright is not a business. Anyone calling AI search "the new SEO" in TRAFFIC terms is wrong
> by roughly 100×.**

**The displacement is real, large and causally demonstrated, even though the replacement is small.**
**Pew Research**, browsing-panel measurement of 68.879 real Google searches: with an AI summary present,
**8% clicked a result versus 15% without**, and **26% ended the session there versus 16%**. A randomised field
experiment (Agarwal & Sen, SSRN 6513059, n=1.065, Chrome extension) measured **−38% to −40% organic clicks**
*(version discrepancy unresolved — SSRN returned 403)*.

**And Cloudflare's server-side logs show what being cited is worth:** crawl-to-refer ratios of **OpenAI
1.091:1**, **Anthropic 38.066:1**, **Google 5,4:1**. **AI platforms take vastly more than they send back.**

---

## 3. WHAT MECHANICALLY WINS — and one widely-sold tactic is worse than doing nothing

**The GEO paper (Aggarwal et al., KDD 2024, arXiv:2311.09735), 10.000 queries across 25 domains:**

| Method | Impression score |
|---|---|
| **Quotation Addition** | **27,8** |
| **Statistics Addition** | **25,9** |
| Fluency Optimization | 25,1 |
| Cite Sources | 24,9 |
| Technical Terms / Easy-to-Understand / Authoritative | 23,1 / 22,2 / 21,8 |
| Unique Words | 20,7 |
| **KEYWORD STUFFING** | **17,8 — WORSE THAN BASELINE. Classic SEO actively fails** |

**And the finding that matters most:** optimising all sources at once, **Cite Sources gave +115,1% visibility
to the rank-5 site while the rank-1 site LOST 30,3%.** The authors' reasoning is exactly the point —
*"traditional search engines rely on… backlinks and domain presence, which are challenging for small
creators… since Generative Engines utilize generative models conditioned on website content, factors such as
backlink building should not disadvantage small creators."*

> **TWO CAVEATS, STATED LOUDLY.** The engine was **simulated** (top-5 Google results + GPT-3.5); the
> "commercially deployed" validation uploaded source text as **files**, so it tested SYNTHESIS ONLY, NEVER
> RETRIEVAL. And "lower-ranked" means **rank 5, not rank 5.000.** **The paper is real evidence about what wins
> once retrieved. It is NOT evidence that an unknown domain gets retrieved. Do not let it be quoted as if it
> were.**

### llms.txt is noise. Zero minutes of her thirty hours.

**Google's own documentation:** *"You don't need to create new machine readable files, AI text files, markup,
or Markdown to appear in Google Search (including its generative AI capabilities), as **Google Search itself
doesn't use them**."* It lists creating *"unnecessary AI text files (like llms.txt)"* among tactics to ignore.
**OpenAI's, Anthropic's and Perplexity's crawler docs describe robots.txt only; none mentions llms.txt.**

**Measured:** across **137.210 domains**, 28% published a valid llms.txt — and **97% of those files received
zero requests.** *(Ahrefs' own server logs; they sell SEO tooling, but this AGREES with the providers' own
docs rather than contradicting them.)*

**The trap:** OpenAI, Anthropic and Google *publish* llms.txt for their developer docs. **Publishing is not
consuming** — those exist to be read by coding agents pointed at the docs.

### The only technical work that matters, and it is an afternoon

**Allow `OAI-SearchBot` · `ChatGPT-User` · `Claude-SearchBot` · `Claude-User` · `PerplexityBot` ·
`Perplexity-User` · `Googlebot` · `Bingbot`. Blocking the TRAINING bots (`GPTBot`, `ClaudeBot`,
`Google-Extended`, `CCBot`) does NOT affect citability — §1 proves it.** Then submit to Google Search Console
and Bing Webmaster Tools. **Free, written-only, no C1/C2/C3 conflict.**

---

## 4. ★ THE SPLIT — the single most useful sentence produced today

**Two studies appear to contradict each other. They do not. They measured different question types.**

| | Study | Finding |
|---|---|---|
| **A** | **Xu et al.**, 55.393 queries, 61.212 references, 7.479 unique hosts | **Top 5 domains = 20% of citations, versus 39,1% for first-page organic.** Measurably flatter than search. **56,3% of unique citation hosts appeared exactly ONCE.** Question-form queries triggered an AI Overview **64,7%** of the time versus 9,5% for non-questions |
| **B** | **Kumar**, 102.025 responses, 5 engines, 102 brands, 149.912 citations | **Tier-3 (small/niche) brands appear in 11% of unbranded answers versus 73% for Tier-1.** *"Small brands are a floor problem on every engine"* |

> ### THE SOURCING/REPUTATION SPLIT — **Xu measured *"what is the answer to this question"* — a SOURCING problem, won by whoever holds the data. Kumar measured *"which vendor should I use"* — a REPUTATION problem, won by whoever has stature.**
>
> **She loses the reputation query permanently — it requires exactly what her veto forbids, being believed as
> an expert. She can win the sourcing query, because IT DOES NOT ASK WHO SHE IS.**

### What the winners actually look like — the agent opened the top result and read it

The site that beat Grainger and McMaster-Carr on an O-ring specification query is **one page per part number**,
carrying dash number, ID and CS in **both** inch and mm, OD **with the formula shown**, series membership, a
400-row sortable table, a groove calculator and a compatibility chart.

> **No author. No byline. No photograph. No "about me." A company mark and nothing else.**
>
> **It is a compounding structured dataset with one URL per entity — and that is precisely shape S4.**

### The NEGATIVE result, which is worth more than the positive ones

On two of four test queries, **not one retrieved page actually answered the question.** They were generic
guides and vendor blogs — and per this file's own **COMPLIANCE COSTUME** law, vendor blogs are the exact class
of source that overstates mandates to sell services.

> **Where specific data does not exist in retrievable form, retrieval FILLS THE SLOT WITH GENERIC CONTENT
> MARKETING. Those slots are UNOCCUPIED, and they go to the first party to publish the actual number. That is
> the opening — and it also means the retrieval layer does not fact-check, so correctness is not what wins the
> slot. THE PRESENCE OF A SPECIFIC NUMBER IS.**

---

## 5. ★★ THE CONVERGENCE — two agents, two questions, one answer

**The S4 agent, hunting datasets, concluded the only opening is a clock-start dataset.
This agent, hunting a channel, concluded the channel selects hard FOR structured numeric data and AGAINST
prose.**

> ### **For an S4 object, THE PRODUCT AND THE DISTRIBUTION ARE THE SAME ARTEFACT.** The pages that constitute the dataset are the pages that get cited. Publishing *is* the marketing. **This is the only structure found in seventy-two candidates that NEUTRALISES C2 rather than merely tolerating it — because the thing that makes her invisible as a person is irrelevant to an object that answers a question with a number.**

**And it dissolves THE DISTRIBUTION SCISSORS.** The scissors said: faceless pushes toward many small self-serve
customers, no-audience pushes toward few large ones, and the two point in opposite directions. **A cited
dataset escapes the dilemma — it is discovered by strangers at zero marginal cost without a face, an audience
or a budget.**

---

## 6. THE MIRROR BUSINESS — KILLED, and the cause of death is reusable

**"Am I visible in AI answers?" as a monitoring product.**

**Observed prices:** Profound **Starter $99/mo** (ChatGPT only, 50 prompts) · **Growth $399/mo** ·
Enterprise quote-only. **Peec AI publishes no prices at all.** *(Otterly and Scrunch pricing pages could not be
loaded — **UNVERIFIED**, and the figures the comparison blogs give were NOT repeated.)*

**Funding:** Profound alone has raised **$3,5M seed → $20M Series A → $35M Series B → $96M Series C at a $1bn
valuation.** *And it spends its content budget publishing competitive teardowns of the long tail.*

**Margins are actually fine** — 50 clients × 50 prompts × 4 engines weekly costs ~$880/month in API against
$4.950 of revenue at $99. **Everything else is fatal:**

### ★ The measurement is 98% noise, and this is quantified

**Żatuchin, arXiv:2607.13304 — 12.933 responses, 20 brands, 8 languages, 3 models, ~5 repetitions:**

| Source of variance | Share |
|---|---|
| Within-prompt resampling | **34,8%** |
| Query language | **26,5%** |
| Brand × language interaction | 8,6% |
| **BRAND IDENTITY ITSELF** | **1,5%** |

**Brand-ranking reliability reaches only 0,36 at the full crossed design, and *"a repeat past the fifth
reduces error by only 0,0003."***

> **Under 2% of the measured variance is the thing the customer is paying to measure. The industry-standard
> "run it five times and average" is measuring almost nothing.**
>
> ### THE NOISE-FLOOR FILTER — **a product whose measured construct is a small fraction of its own variance cannot be sold honestly. Ask it of every monitoring or scoring product this project meets again.** And note the tell: *the one honest version of this product — "your number is noise, here is the variance decomposition" — talks its own customer out of buying.*

**And full coverage requires breaching terms.** OpenAI's rest-of-world terms — the ones governing a Brazilian
user — forbid *"any automated or programmatic method to extract data or output from the Services… except as
permitted through the API."* Google's ToS makes its own robots.txt operative, and **there is no commercial API
for AI Overviews or AI Mode.** *(The API `web_search` tool is a different product from consumer ChatGPT search
— different index, different system prompt. **A compliant monitor measures a proxy; a monitor that measures
the real thing must scrape in breach. Every vendor is on one horn or the other.**)*

---

## 7. The free test this deserves

> **Pick 20 factual queries in a candidate vertical where the specific number is NOT currently retrievable.
> Publish the 20 answers as 20 structured pages on one indexed domain. Count how many are cited within 60
> days.**
>
> **Measure the RATE, not the win. It costs a domain and hosting, needs no phone, no name and no face, and it
> directly tests the one thing no public data can answer** — because **there is no reliable public data on
> time-to-first-citation for a new domain**, and the agent's two natural experiments are n=2 observations,
> not a study.

---

## 8. What is carried forward

1. **The channel is real, fast, faceless-compatible — and too small to carry the business alone on this
   clock.** A compounding SECONDARY channel, never the primary revenue path.
2. **Indexation is not ranking.** Being indexed by Google and Bing is a free afternoon and a hard
   prerequisite. Ranking is what remains out of reach.
3. **THE SOURCING/REPUTATION SPLIT.** She loses "which vendor should I use" permanently and can win "what is
   the answer."
4. **THE CONVERGENCE.** For an S4 dataset the product and the distribution are one artefact — the first
   structure that neutralises C2.
5. **THE NOISE-FLOOR FILTER**, from the mirror business's death.
6. **llms.txt is noise; keyword stuffing is worse than nothing; statistics and quotations are what win.**

**Sources refused and named:** every *"GEO statistics 2026"* roundup, seven named AI-visibility vendors'
comparison posts, and the SEO trade press. **Where those pointed at something real, the agent fetched the
primary source and cited that instead.**
