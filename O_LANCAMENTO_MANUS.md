# O LANÇAMENTO × Manus 2.0 — read 4 Oct 2026

**The question.** On 4 Oct the founder reported that the Climate Rescue UGC ad and the Climate Rescue case study were
both made with Manus, and that Manus has just relaunched as 2.0. The request: *"deep dive … seeing how Sol can use it
to do amazing in this business."*

**Scope.** Two research agents fetched Manus's own blog, help centre, docs, API docs, app-store pages and the Chinese
regulator's notice with `curl`. The load-bearing quotes were re-checked against the raw captures. **The founder set
aside the terms and confidentiality question (*"don't care about this"*). This file records that decision and does not
re-argue it.**

## The verdict

1. **Use Manus 2.0 as Sol's studio and her back office.** It is the fastest route to the world, the film and the UGC
   ad, and it already made both of the founder's Climate Rescue pieces.
2. **One rule makes it compatible with the guarantee. The brand's real pack goes in as its own layer, never
   regenerated, and every exported frame goes through `relatorio_fidelidade.py`.** The 2.0 Video Editor supports this
   directly: *"Drag in your own product shot to replace a generated one."*
3. **It changes her cost and speed, not what she sells.** Manus has no label-lock. It says its own first cut is
   *"80 to 90 percent there"*, and that AI image text *"often produc[es] garbled results"*.

## What 2.0 is (released 28 Sep 2026)

**The architecture.** *"Manus 2.0 is not a version update. It's a new architecture, new products, and new
capabilities."* (manus.im/blog/introducing-manus-2-0).
- **Cascade** is the new agent harness. In one tested configuration it used 23,2% fewer tokens and finished 28,2%
  faster. Manus adds that this is *"not an overall average"*.
- **The model tiers** are now *Manus 2.0 Lite / 2.0 / 2.0 Max*.

**Video Editor**, in the Manus Studio desktop app (Mac and Windows only):
- **Models:** *"Seedance 2.5, Seedance 2.0, Seedance 2.0 Fast, and MiniMax H3"*. Canvas also has Google Veo 3.1
  Standard (help 11711172).
- **Layers:** *"Every ingredient… sits on its own layer… You don't get a flattened MP4."* (blog/introducing-video-editor,
  1 Oct 2026).
- **The use case it names:** *"The functionality I'd recommend most for small teams is the AI UGC ad."*
- **It writes its own code:** motion graphics, *"Python to locate pixels"*, FFmpeg for slow motion.

**Images:**
- Design View runs on *"Google's Nano Banana Pro"* (docs/features/design-view).
- GPT Image 2 has been in Slides since 29 Apr 2026.

**Automations** run on a schedule, or when something happens in Gmail, Outlook, Notion, Google Calendar, Shopify,
RSS, a webhook and others. Pro allows 20 of them (docs/automations).

**Wide Research:**
- 20 subtasks run in parallel, each capped at 50 credits (help 11960169).
- Listed uses include *"Research 200 prospects, find contact info"*, tested up to 250 items.

**Connectors and channels:**
- Gmail (drafts reply; the tutorial has a person approve each send), Drive, Calendar, Notion, HubSpot and Stripe.
- Higgsfield (19 May 2026) and ElevenLabs.
- A **WhatsApp Business** channel (help 14178631).

**The sandbox:**
- Each task runs on its own Ubuntu VM with root access. Python and FFmpeg are documented.
- Skills can bundle scripts that Manus *"execute[s]"*.
- An idle sandbox is recycled after 21 days on Pro.
- The paid Cloud Computer is a persistent machine at US$30 or US$50 a month (help 15392078).

**API:** REST v2 at `api.manus.ai`, with `task.create` limited to 10 requests a minute (open.manus.ai/docs/v2).

## How Sol uses it, job by job

| Job | Manus 2.0 feature | The rule that keeps the guarantee |
|---|---|---|
| The world: scenes, light, people | Design View (Nano Banana Pro), Canvas | Prompt the blank blue stand-in, or let it generate a pack and replace it |
| The 15 s film and the 2 cuts | Video Editor, layered timeline | **The real packshot sits on its own layer in every shot where the pack is still** (hero, table, shelf, end card) |
| The UGC ad (new rung, not yet in the ladder) | Video Editor, *"AI UGC ad"* | Same layer rule. Moving in-hand shots are regenerated, so check each one and cut or redo any that fails |
| Captions and on-screen text | Video Editor text layers | All text is added as a layer, never asked of the model (Manus's own advice: *"clean, editable text overlays"*) |
| The proof | Export, then `relatorio_fidelidade.py` on every frame (locally, or as a Manus Skill) | REPROVADA is never delivered |
| The prospect list (ANVISA + site contacts) | Wide Research plus a monthly Automation | One personal message at a time. Manus's own terms ban *"unsolicited communications"* in bulk, and the plan already forbids them |
| First messages and follow-ups | Gmail connector drafts; Sol approves and sends each one | Follow the plan's contact order and add *"responda SAIR"* |
| The free PRÉVIA per prospect | Design View plus the layer swap | Watermarked and never posted (§6.4) |
| Case studies and offer decks | Slides, exported to PDF or PPTX | This is how the Climate case study was made |
| Clients' messages | WhatsApp Business channel, Mail Manus | Every quote and promise comes from the ladder, and Sol approves it |

**What it does not do:** keep a label exact by itself, issue an NFS-e, or take Pix.

## The evidence, against Manus's own work

**The pre-2.0 Climate UGC ad** (Manus):
- *RESSCUE* in every frame of the hero shot.
- *RESCUE* on the end card.
- The name smeared in hand.

Our recut fixed it the same way 2.0's editor now allows: the real pack laid over the hero shot.

**The Climate case study** (Manus):
- Every still reads CLIMATE RESCUE correctly.
- **Two of the five film frames smear the label** (O_LANCAMENTO_AIRTIGHT.md §4.7).

The pattern holds both times: stills are fine, and a pack that moves gets redrawn. **2.0's layered editor and the
checker together close exactly that gap**, wherever the pack can stand still.

## What it costs

These are published prices only (help 11711111, modified 2 Oct 2026):
- **Free:** 300 credits a day, Lite only.
- **Pro:** US$20 a month for 4.000 credits, US$40 for 8.000, US$200 for 40.000.
- **Team:** from US$20 per seat.

**The cost of one image or one video in credits is not published.** Manus calls the agent's own estimates
*"hallucinations"* (help 13185575).
- A free-access campaign allowed 10 videos and 200 images a day on paid plans. Its article still names an August end
  date, so whether it is running now is unclear.
- **Payment is in USD by card only, with no Pix.** BRL prices exist only through Apple in-app purchases.

⇒ **The cost per launch has to be measured in the dry runs.** It cannot be read off a page.

### My estimate per launch (4 Oct 2026; an ESTIMATE, not a measurement)

**Anchors I checked at the source:**
- **One Manus credit = US$0,005 ≈ R$0,026.** Every Pro tier prices at the same rate: 4.000 for US$20, 8.000 for US$40,
  40.000 for US$200.
- **On iPhone it costs 2,5× more:** R$129,90 for 2.000 credits, or R$0,065 a credit. Buy on the web, never in the app.
- **The model makers' own prices** (ai.google.dev/gemini-api/docs/pricing, fetched 4 Oct):
  - Nano Banana Pro: **US$0,134 per 1K/2K image**, US$0,24 per 4K image.
  - Veo 3.1 at 1080p: **US$0,40 per second** on Standard, **US$0,12** on Fast, **US$0,08** on Lite.
- **Seedance 2.5 / 2.0**, Manus's main video model: ByteDance's price page needs a login, so its price is
  **UNVERIFIED**. I assume it falls inside Veo's US$0,12–0,40 per second band.

**My assumptions** (UNVERIFIED; they cover anything Manus adds to the model makers' prices):
- Manus charges **about 1,5–2× the model's own price**, plus 200–900 credits of agent work per task. That range comes
  from its only published task examples, which are web and data tasks.
- **A launch needs about 40 image generations:** about 10 final stills, ~4 tries each, plus the three looks.
- **A generated film is about 15 s of motion, generated ~3–4 times**, so 45–60 s of output.
- **A UGC ad is 30–40 s across ~10 shots, generated ~3 times**, so 100–120 s of output.

| Launch | Credits | US$ | R$ | Share of R$2.990 |
|---|---|---|---|---|
| **A. The plan's method:** stills from Manus, film built locally from the stills | 2.000–5.000 | 10–25 | 52–130 | 2–4% |
| **B. The film's motion generated in Manus** (Seedance) | 3.600–14.600 | 18–73 | 94–380 | 3–13% |
| **C. B plus a UGC ad** | 7.200–33.800 | 36–169 | 187–880 | 6–29% |

*(How the rows add up: A = 40 images × US$0,134 × 1,5–2, plus 400–2.700 credits of agent work. B adds 45–60 s of video
× US$0,12–0,40 × 1,5–2. C adds 100–120 s more at the same rates.)*

**A month of 4 launches:**
- Method A: about 8.000–20.000 credits, **US$40–100**.
- Method B: about 14.400–58.400 credits, **US$72–292**.

Method A is the same order of cost as the tool line already in §9.

⇒ **For the launch itself, cost is not the risk:** 2–13% of the price on methods A and B. The risks stay Sol's hours and
the label.
⇒ **A UGC ad is the exception.** At the top of the range it could take almost a third of R$2.990. So it is priced as
its own product, never thrown into O LANÇAMENTO.

**Two things would replace this estimate with a fact:**
1. **The founder's own Manus usage page.** It shows the credits the Climate case study and the UGC ad actually used.
2. **The free-access campaign**, if it is still running. It allowed 200 images and 10 videos a day on paid plans at no
   credit cost, which would push the generation cost near zero. Its article names an August end date, so this is
   unconfirmed.

### Against Higgsfield (its own live pricing, read through the connected Higgsfield tool, 4 Oct 2026)

**Plans:**
- **Plus:** US$49 a month, or US$39 a month billed yearly, for **1.000 credits**. Higgsfield says that is *"= 600 Nano
  Banana Pro Generations"* or *"~200 Kling 3.0 videos"*.
- **Ultra:** US$129, or US$99 yearly, for **3.000 credits**.

**What one credit buys:**
- **One credit costs US$0,033–0,049**, depending on the plan.
- **One Nano Banana Pro image costs about 1,7–2 credits ≈ US$0,065–0,098.** The trial's own line, *"100 credits = 50
  Nano Banana Pro images"*, gives the 2.
- That is **cheaper than Google's own US$0,134**, and about a third of what I estimated Manus charges.
- **One Seedance 2.0 clip costs about 25 credits ≈ US$1,0–1,2** (from *"~4 Seedance 2.0 videos"* per 100 trial
  credits). That is for the default 5 s at 720p; 1080p is UNVERIFIED.

**A promotion, which is marketing and needs re-checking:** Plus bought by 5 Oct includes **365 days of unlimited
generations** on GPT Image, Seedream 4.5, Nano Banana (not Pro), Flux.2 Pro and Kling O1 Image. These work on the
website only, not through the connector.

| Per launch | Higgsfield | Manus (my estimate above) |
|---|---|---|
| A. Stills only (~40 images) | ~70–80 credits ≈ US$3–4 ≈ **R$14–20** | R$52–130 |
| B. Plus ~45–60 s of generated film | ~290–380 credits ≈ US$11–19 ≈ **R$59–97** | R$94–380 |

| Per month, 4 launches | Higgsfield | Manus |
|---|---|---|
| A | fits inside Plus: **US$39–49** | US$40–100 |
| B | needs Ultra: **US$99–129** | US$72–292 |

**What this means:**
- ⇒ **Per image and per clip, Higgsfield is roughly half to a third of Manus.** The monthly bills come out closer,
  because subscriptions are sold in fixed blocks.
- ⇒ **The gap is at most ~US$150 a month against R$12–15k of revenue (≤5%). The tool choice should be made on SOL'S
  HOURS, not on credits.**
  - Manus edits, assembles and also runs the sales jobs.
  - Higgsfield only generates. Sol, or this session through the connector, does the assembly.
- **Decide in the dry run:** time the same Climate film made both ways.

## The company behind it

- Meta acquired Manus on 29 Dec 2025.
- China's NDRC prohibited the deal on 27 Apr 2026 and ordered it withdrawn (zfxxgk.ndrc.gov.cn, id 20623).
- On 23–24 Aug Manus deleted some users' data in *"specific jurisdictions"*.
- It has run independently again since 1 Sep 2026.

**The pipeline must stay swappable**, which was already a rule (§13.4).

## "Brazilian buyers don't know Manus"

**App Store ratings, fetched 4 Oct:** Brazil **61.907**, US 38.602, UK 4.453, Mexico 2.622. Brazil is Manus's largest
iPhone storefront of the four.

**The founder: *"you can check but won't change anything real"*, and that is right.** 10 of the 40 prospect brands
already post ChatGPT- or Gemini-named images. **Knowing a tool is not the same as a launch with a proven label, one
visual world and a guarantee in 5–7 days.** Sol sells the result, not the secret.

## The test, with the bars set before it runs

Remake the Climate Rescue 15 s film and the UGC ad in Manus 2.0's Video Editor. Put the packshot on its own layer in
every shot where the pack is still. Export, then run the checker on every frame.

- **Pass:** every frame APROVADA, with the planted control caught.
- **Pass:** 3 h or less of Sol's time.
- **Pass:** a vertical 1080×1920 export. The only published resolution is a stale *"1080×720"*.
- **Record:** the credits used.
- **If an in-hand moving shot fails:** cut it, or replace it with a still-pack shot. Do not deliver it.

## Sources (fetched 4 Oct 2026)

- manus.im/blog/introducing-manus-2-0
- manus.im/blog/introducing-video-editor
- manus.im/blog/introducing-manus-flex
- manus.im/blog/manus-sandbox
- manus.im/blog/manus-joins-meta-for-next-era-of-innovation
- manus.im/blog/a-note-to-our-users
- manus.im/blog/manus-resumes-independent-operations
- help.manus.im/en/articles/:
  - 17190150 (what is new in 2.0)
  - 11711172 (video models)
  - 11711111 (pricing)
  - 13185575 (credit estimates)
  - 11960169 (Wide Research)
  - 15392078 (Cloud Computer)
  - 16312548 (free-access campaign)
  - 11711239 (video resolution)
  - 14178631 (WhatsApp Business)
- manus.im/docs/automations.md
- manus.im/docs/features/design-view.md
- manus.im/tools/ai-design
- open.manus.ai/docs/v2/introduction.md
- open.manus.ai/docs/v2/rate-limits.md
- apps.apple.com/{br,us,gb,mx}/app/manus-ai/id6740909540
- zfxxgk.ndrc.gov.cn/web/iteminfo.jsp?id=20623
