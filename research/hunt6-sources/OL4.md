# OL4 — Do the tools' own terms let Sol sell the outputs, promise "no training", and say "as imagens são suas"?

**Agent:** OL4 · **Date:** 25 Sep 2026 · **Brief:** `BRIEF_OL.md` · **Raw fetches:** `work/ol4/` (every page below was
curled and read in full; where a site blocked curl, the page came through the `r.jina.ai` reader, which returns the
page text verbatim, and that is noted).

## Verdict: CLOSED, but only after five design changes. Two of today's three promises are false as written.

| Promise | As written today | After the changes below |
|---|---|---|
| (a) Sell the outputs for commercial and paid-ad use | **TRUE on paid plans.** Higgsfield, Adobe, the Gemini API (paid), Artlist AI, Kling (paid), Luma (paid) and Runway all allow it. Free tiers of Photoroom, Kling and Luma do not, and Higgsfield's free tier watermarks its output. | TRUE |
| (b) "Sua arte não entra em nenhuma IA antes do lançamento" / never trained on | **Holds only for the label**, because the label is composited locally. **Two things break it.** The design file tells Sol to upload the public packshot to Higgsfield after launch, and to build the PRÉVIA from a brand's public packshot. **Higgsfield trains on every upload, and training can't be switched off on PLUS or ULTRA.** The words "nenhuma IA" are also literally false: cutout, OCR and cloud storage all involve machine learning. | TRUE, once client art never goes to any generator at any stage, and the wording is narrowed to what she controls |
| (c) "As imagens são suas para usar no site, nas redes, em marketplaces e em anúncios" | **Overstated.** The tools don't claim the outputs and let her pass them to clients. But Brazilian law needs a **written** cessão that lists each use, AI elements may not be protectable, the tools warn that outputs "may not be unique", and stock music is licensed, not owned. | TRUE, reworded as a written cessão of her rights, a promise that she won't reuse the pieces, and an honest AI note |

---

## 1. Higgsfield — the founder's generator

**Source.** Terms of Use, https://higgsfield.ai/terms-of-use-agreement, *"Last updated: July 26, 2026. Effective:
immediately for users who register on or after July 26, 2026; on August 27, 2026 for users who registered before."*

**Output ownership and commercial use: YES, on every plan, and she may pass the outputs to clients.**
- §4.4: *"Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use
  of Outputs. Your rights in Outputs you have generated and exported survive cancellation of your subscription or
  deletion or termination of your Account, and you may transfer or sublicense your rights in Outputs to your clients
  or other third parties."*
- Help centre, *"Who owns my generations, and can I use them commercially?"* (Aug 2, 2026,
  https://higgsfield.ai/creator-hub/help-center/account/who-owns-my-generations-and-can-i-use-them-commercially):
  *"Commercial use includes advertising and paid campaigns, social media content for brands, client work and
  deliverables…"*
- The same page: *"Paid plans include watermark-free downloads."*
- The same page on indemnity: *"Legal indemnification, protection against third-party IP claims, is available on the
  Enterprise plan only."*
- Resale limit: §5.2(i) bars reselling *"the Service"*, not outputs. The same help page says: *"The restrictions in
  Section 5.2 apply to commercially exploiting the Service itself, not to downstream use of content you generate."*

**Training on inputs: CONFIRMED. There is NO opt-out on PLUS or ULTRA.**
- §4.4: *"You acknowledge and agree that Your Content, Inputs, and Outputs may be used by Company to train, develop,
  enhance, evolve, and improve its (and its affiliates') AI models… Different terms apply to enterprise and business
  customers who use the Service under an Enterprise Agreement… under those agreements, Company does not use the
  customer's content to train or improve its AI models, and that content is handled as confidential… You can stop
  this going forward by deleting Your Content or your Account."*
- §16.5(c)(iii): deletion does not reach *"content already used to develop or improve Company's AI models before
  deletion, which cannot feasibly be disassociated from models already trained."*
- Higgsfield's own summary of the update, https://higgsfield.ai/blog/terms-of-use-privacy-policy-update (Jul 25, 2026):
  - *"Does Higgsfield train on my content? Yes."*
  - *"If your clients require that their data never be used for training, an enterprise agreement can include that."*
- Privacy Policy (effective Aug 27, 2026), §2.3: uses Inputs and Outputs *"to train and improve our (and our
  affiliates') AI models"*.
- Privacy Policy §4: shares data with *"third-party AI model and compute providers."*
- The live plan widget (Higgsfield MCP `show_plans_and_credits`, 25 Sep 2026) lists no privacy or no-training
  feature on PLUS or ULTRA.
- Enterprise, https://higgsfield.ai/enterprise: *"contractual no-train guarantee… built for unreleased products,
  embargoed campaigns"*. Price: *"credit-based pricing on annual contracts… sized to your team's seats"*, via Contact
  Sales. **UNVERIFIED.**
- The terms have moved before. The previous version (https://higgsfield.ai/terms-of-use-agreement-23-07-2026) made
  the content licence *"transferable, perpetual, irrevocable"*.

**API and MCP: the same data terms, plus one more party in the chain.**
- §11.1: the developer terms apply *"in addition"*. None of them changes training.
- §11.13: when Sol drives Higgsfield from a chat assistant over MCP, that assistant is a *"Third-Party MCP Client…
  governed by its own terms of service… and privacy policy"*. Every prompt and file then also passes through the
  assistant vendor.

**Public visibility: private by default, but there is a toggle.**
- §3.2: *"If you do not choose a level of access, the Service may default to its most permissive setting."*
- Help centre (https://higgsfield.ai/creator-hub/help-center/getting-started/higgsfield-community-on-discord): *"Your
  Higgsfield generations are private by default… Turn off the Auto-publish new generations toggle in Manage Account →
  Personal Profile."*

**Content rules that bind her.**
- §5.2(xi): she may not *"represent that any Output is human-generated when it is not"*.
  - §11.7 repeats this for developer access.
  - So the offer sheet's *"6 fotos"* should read *"6 imagens"*. The sheet already says *"A IA cria o cenário e a
    luz"*, which is correct.
- §5.5: *"Where required by applicable law, you will disclose that Output is artificially generated… and you will not
  remove, alter, or obscure any provenance signals or markings Company applies under Section 6.4."*
- §6.4: the provenance marks are *"C2PA / Content Credentials"*.
- §5.1(ii)(a) bans deceptive content. The claim lock ("mood, never results") already complies.
- Real people:
  - §4.2(b) and §5.3 require documented consent from any real person whose face goes in. That covers a Soul ID
    trained on a real model's photos.
  - The Soul ID help page (quoted by H6F) says: *"Only upload photos of yourself, or of someone who has given you
    permission."*
- **§4.2(a) is the trap for the PRÉVIA.** By uploading anything, she warrants that she *"ha[s] all necessary rights
  to Your Content to grant the licenses set forth in Sections 4.3 and 4.4"*. That includes the **training** licence.
  - She cannot give that warranty for another brand's packshot the brand never authorised her to feed to an AI.
- §8: the providers of the underlying models (Nano Banana, Kling, Seedance, GPT Image) impose their own use policies,
  and *"the more restrictive terms govern"*.
- §14.2: the liability cap is the greater of 6 months' fees or US$100.

## 2. Artlist — music, and its AI plans

**Sources.**
- Licence: https://artlist.io/help-center/privacy-terms/artlist-license/ (Pro/Business licence *"Effective February 15,
  2026"*).
- Terms of Use: https://artlist.io/help-center/privacy-terms/terms-of-use/ (*"Last update: July 2, 2026"*).

**Stock music in a client's paid ad: allowed on Pro, with three traps.**
- Allowed, Pro licence §1 and §3:
  - *"Commercials"*, *"Paid & promoted videos"*.
  - *"If you're hired to create the Project, your client is covered by your license and can use the Project."*
  - The Social licence forbids it: *"you can't publish your Projects in paid media"*.
- **Trap 1: clients cannot re-edit the music.** Help article
  (https://help.artlist.io/hc/en-us/articles/29490991524253-Understanding-Artlist-s-license): *"Clients are not
  permitted to modify or use the assets independently."* The client may not recut the film with that track.
- **Trap 2: publish while subscribed.** Pro licence §2: *"When your subscription expires, those Projects can remain
  published in any media, but any new projects will not be covered."* Help: *"Artlist music… must be published or
  broadcast while your subscription is active."* A client who launches the film after Sol lapses is not covered.
- **Trap 3: an "agency" may need Max Business.**
  - Pro licence §11: *"if you work for an agency, broadcaster or for a company… that has more than 50 employees, you
    must have a Max Business plan… This requirement does not apply to subscription plans consisting solely of AI
    Services."*
  - The pricing FAQ (https://artlist.io/page/pricing/max) says Max Business is for *"agencies of any size"*.
  - The help article says *"company, organization, or agency has over 50 employees"*. The two contradict each other.
  - A one-person launch studio could be read as an agency. Max Business starts at **US$4.788/year** (plan catalogue
    embedded in the pricing page). **Classification UNVERIFIED.**
- **Inputs:** stock *"may not be used with AI services that claim ownership or rights in the generated output… not
  used to train"*. **Never feed Artlist stock into Higgsfield**, because Higgsfield trains on inputs.

**Artlist AI plans (AI-only): cleaner for music.**
- ToU §14: *"Artlist hereby assigns to you all of Artlist's right, title and interest, if any, in and to Output, and
  Artlist does not restrict your commercial use."*
- Help: *"You can use AI-generated outputs however you like, including for commercial purposes, even after your
  subscription expires… You therefore, can share your AI-generated outputs with clients."*
- The Max Business requirement does not apply to AI-only plans (licence §11, quoted above).
- Training by third-party model providers (§14): *"Artlist contractually prohibits most third-party Model providers
  from using data received from Artlist… However, certain models or features may permit such use. Artlist will
  identify those Models…"*
  - So Artlist AI is **not** a no-train route for client art.
  - It is fine for a music prompt Sol writes herself.
- Forbidden uses (ToU §15): *"Generate Output featuring real people, brands, or entities… without obtaining the
  necessary rights"*; *"generating content intended to deceive others into believing it was created by a human"*.
- Price: **AI Starter US$19,99/month** (US$11,99/month billed annually), *"Up to 110 AI songs"*, *"License covers
  commercial use"* (pricing page).

## 3. Photoroom

**Source.** Terms, https://www.photoroom.com/legal/terms-and-conditions (*"Effective date: July 29, 2026"*).

**Commercial use.**
- §2.1.b: paid customers use it *"for the Customer's own internal business purposes"*.
- Free accounts are *"personal, non commercial purposes"* only.
- §2.2.a: *"Customer will own all Customer Content."*

**Licence Photoroom takes (§2.2.c).**
- A *"royalty-free, sublicensable, transferable, perpetual, irrevocable, non-exclusive, worldwide license… solely for
  use in connection with our provision of the Services"*.
- Plus: *"you… expressly authorize Photoroom to use User Content to improve, train and develop Photoroom's products…
  You can opt-out of this at any time by changing the settings on your account in the app under Data Control."*

**How to opt out.** App toggle *"Improve model for everyone"*: gray = off
(https://help.photoroom.com/en/articles/8707489).

**The API pages contradict each other.**
- https://www.photoroom.com/platform/security says: *"API images are discarded after each call, never used for
  training without your consent"*.
- The same page also says: *"self-serve API plans do [train], with opt-out in settings."*
- The help article (Oct 20, 2025) says API images are *"neither stored nor used for training purposes unless
  explicitly requested."*

**Verdict.** Photoroom is not needed. A local Photoshop cutout does the job. If she uses it at all, switch Data
Control OFF first, and never use it on pre-launch art.

**Prices.**
- API: US$20 per 1.000 images on Basic (US$0,02 each); Plus calls cost US$0,10 each (pricing FAQ text).
- App: Pro **US$7,50/month** billed yearly. **UNVERIFIED** — the figure is a placeholder rendered in the page HTML.

## 4. Google Gemini API, paid tier (Nano Banana Pro, Veo, Lyria)

**Source.** https://ai.google.dev/gemini-api/terms (*"Effective March 23, 2026"*). Direct curl loops on OAuth, so this
page came through the reader.

**Data use: paid tier trains on nothing.**
- *"When you use Paid Services… Google doesn't use your prompts (including… files such as images, videos, or
  documents) or responses to improve our products… For Paid Services, Google logs prompts and responses for a limited
  period of time, solely for detecting and preventing violations of the Prohibited Use Policy."*
- **Google AI Studio (the no-code UI) counts as paid** *"as long as the account… has access to a Cloud Project with an
  associated and active Cloud Billing account."*
- Unpaid use trains on inputs: *"Do not submit sensitive, confidential, or personal information to the Unpaid
  Services."*

**Ownership.** *"Google won't claim ownership over that content. You acknowledge that Google may generate the same or
similar content for others."*

**Prohibited uses that touch ads** (https://policies.google.com/terms/generative-ai/use-policy, *"Last Modified:
December 17, 2024"*): *"Misrepresenting the provenance of generated content by claiming it was created solely by a
human, in order to deceive."*

**Paid-tier prices** (https://ai.google.dev/gemini-api/docs/pricing; each row carries *"Used to improve our
products: No"*):

| Model | Price |
|---|---|
| Nano Banana Pro image | **US$0,134** per 1K/2K image |
| Veo 3.1 Fast | **US$0,10–0,12** per second |
| Veo 3.1 Standard | **US$0,40** per second |
| Lyria 3.5 full song | **US$0,08** |

- The same Nano Banana Pro model reached **through Higgsfield** falls under Higgsfield's §4.4 training licence. **The
  route decides the terms, not the model.**

## 5. Adobe Firefly and Photoshop

**Source.** General Terms, https://www.adobe.com/legal/terms.html (*"Published October 3, 2025"*). Fetched through the
reader, because direct curl got HTTP/2 resets.

**No training on her content, including by partner models.**
- §2.2: *"We will not use your Local or Cloud Content to train generative AI models except for Content you choose to
  submit to the Adobe Stock marketplace."*
- §2.2: *"For Content stored locally on your device… we do not scan or review your Content."*
- §4.3: *"We will not use these rights to train generative AI models on your Content and will not use the sublicense
  rights to have anyone else train generative AI models on your Content."*
- Partner-model FAQ (https://www.adobe.com/products/firefly/partner-models.html): *"Adobe and our partners do not train
  on your personal or project data."* The partners named there include Google (Nano Banana), OpenAI (GPT Image),
  Kling, Runway, Luma and Black Forest Labs.
- The Content Analytics opt-out (§2.2) exists for cloud files. Switch it off.

**Ownership.** §4.2: *"you… retain all rights and ownership of your Content."*

**Indemnity.** https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html: *"Adobe provides intellectual property
indemnification for enterprise customers for content generated with Adobe Firefly"*. That is enterprise only.

**Partner-model outputs.** The Firefly partner FAQ puts the commercial-safety call on the user: *"it is the
responsibility of the creator to decide whether partner models are… safe for commercial use."*

**Provenance.** Gen-AI User Guidelines (*"Last Updated: May 15, 2026"*): *"You must not remove, alter, or disable any
Content Credentials."*

**Prices (US, annual billed monthly).**

| Plan | Price | Includes |
|---|---|---|
| Photography | **US$19,99/month** | Photoshop desktop + Lightroom, 1.000 credits |
| Photoshop alone | US$22,99 | |
| Firefly Pro | **US$19,99** | 4.000 credits, partner models, Photoshop web, *"Generate music up to 200 minutes"* |
| Creative Cloud Pro | US$69,99 | 20+ apps including the video apps, 4.000 credits |

Brazilian BRL prices were not fetched: **UNVERIFIED.**

## 6. Editors: CapCut and Canva

**CapCut: DO NOT USE for any client file.**
- The version served here is the US one (https://www.capcut.com/clause/terms-of-service, *"Last updated: April 15,
  2026"*, TikTok USDS Joint Venture). It says:
  - *"All User Content will be considered non-confidential. You must not upload or make available any User Content…
    that you consider to be confidential or proprietary to any other person."*
  - Plus an *"unconditional, non-exclusive, royalty-free, fully transferable, sub-licensable, perpetual and worldwide
    license to use your User Content… for the purposes of operating, developing and providing the Services."*
- That conflicts directly with unreleased artwork.
- **The Brazil / rest-of-world version is served by IP location and could not be fetched: UNVERIFIED.** Secondary
  reports on the June 2025 international version describe the same "non-confidential + perpetual" wording.
- CapCut's library assets (Materials Licence, Jan 22, 2026) allow ads only for items marked *"commercial"*.

**Canva: usable, with one setting.**
- Terms of Use (https://www.canva.com/policies/terms-of-use, through the reader). The licence is narrow: *"to display,
  host, copy, store and use your User Content to provide the Service to you."*
- Training is governed by Privacy Settings: *"Canva and its trusted partners may use this to develop and improve
  AI-powered features if this is consistent with your Privacy Settings."*
- https://www.canva.com/trust/privacy/: *"For users who have a Canva Business or Enterprise account… we don't use your
  business, team or enterprise content to improve AI-powered features."*
- The default for an individual Pro account is **UNVERIFIED**. Turn the toggle off, or use a Teams account.
- AI Product Terms (effective 26 Jun 2026):
  - *"you own your Output"*.
  - It forbids removing *"C2PA metadata"*.
  - AI-edited Canva library content is not owned.

## 7. Video generators, briefly

| Tool | Output rights | Training on her inputs |
|---|---|---|
| **Kling** (https://kling.ai/docs/user-policy, 2026/04/21; payment policy) | Paid: *"members' use of the Output for commercial purposes is not restricted"*. Free: *"you may not use… the Output for any commercial purposes."* | **Yes.** §4.7.3(f) *"create, test, improve, train…"*. §4.7.2 also allows use *"for the purposes of promotion"*. Revocation by e-mail (§4.7.4). |
| **Runway** (https://runwayml.com/terms-of-use, Sep 15, 2026; reader) | *"does not restrict your commercial use of your Outputs"* | **Yes**, *"irrevocable, perpetual… license… to train"* (§4.4) |
| **Luma** (https://lumalabs.ai/legal/terms-of-service, May 14, 2026) | Assigned to the customer. Commercial use only if produced *"during an active Subscription Term… allowing for the commercial use"*. | **Yes, even on paid plans**, *"train, or otherwise develop"* (Input and Output licences) |
| **Veo, via Gemini API paid** | Google claims no ownership | **No** |
| **Kling / Runway / Luma inside Adobe Firefly** | Adobe terms | **No** (Adobe §4.3 + partner FAQ) |

## 8. Brazilian law under "as imagens são suas"

Source: Lei 9.610/98, https://www.planalto.gov.br/ccivil_03/leis/l9610.htm.

- **Art. 11:** *"Autor é a pessoa física criadora de obra literária, artística ou científica."* **Art. 7:** protects
  *"criações do espírito"*.
  - So purely AI-generated scenery may carry no copyright for anyone to own.
  - How Brazilian courts treat an AI + human composite is **UNVERIFIED**.
- **Art. 49 II, IV, VI:**
  - *"somente se admitirá transmissão total e definitiva dos direitos mediante estipulação contratual escrita"*.
  - *"a cessão será válida unicamente para o país em que se firmou o contrato, salvo estipulação em contrário"*.
  - *"não havendo especificações quanto à modalidade de utilização, o contrato será interpretado restritivamente"*.
- **Art. 50:** *"A cessão total ou parcial… se fará sempre por escrito."* **Art. 4:** *"Interpretam-se restritivamente
  os negócios jurídicos sobre os direitos autorais."*
- ⇒ One sentence on an offer sheet plus a nota fiscal does not transfer anything durable. **A one-page written cessão
  listing each use, worldwide and with no end date, is required.**

---

## THE REPAIR

### Design changes

1. **One rule for every tier, before and after launch.** Client art never goes into any generator or editing cloud.
   - Client art means: the label PDF, the packshot, prototype photos, the logo and brand kit, unreleased product names
     and claims.
   - Generators receive only Sol's own generic prompts and a blank placeholder shape. The label is composited on her
     own computer.
   - **This replaces `O_LANCAMENTO.md` D1 rule 1's "Post-launch… the product can go in directly."**
     - That line breaks the "never trained" promise.
     - It breaks Higgsfield §4.2(a): she cannot warrant a training licence over the brand's art.
     - It breaks Artlist's ban on outputs *"featuring real… brands… without… rights"*.
   - It also bans Higgsfield's brand-kit / product-id features (DTC Ads, Marketing Studio) on client assets.
2. **The PRÉVIA also composites locally.** Generate the world with a blank bottle, then lay the public packshot over
   it offline. She has no right to hand another brand's packshot to a service that trains on it.
3. **Prompt hygiene and settings.**
   - Prompts never include the brand name, product name or claims.
   - Higgsfield *Auto-publish* is OFF.
   - Photoroom Data Control is OFF, or Photoroom is not used.
   - Canva's AI toggle is OFF, or a Teams account is used.
   - Adobe Content Analytics is opted out.
   - **CapCut is never used.**
   - If an assistant drives Higgsfield over MCP, client files stay out of the assistant too.
4. **Music is AI-generated, not stock.** Use Artlist AI Starter, Firefly music or Lyria (paid). The output is
   hers/assigned, survives cancellation and can be handed over, and it avoids all three Artlist stock traps. **Never
   put Artlist stock into Higgsfield.**
5. **Keep provenance and disclose it.**
   - Export composites with Content Credentials kept, for example Photoshop's Content Credentials export. Higgsfield
     §5.5, Adobe, Canva and Luma all forbid stripping them.
   - Tell the client that the pieces contain AI-generated scenery. Meta says it adds an "AI info" label *"when we
     detected industry standard AI image indicators"* (https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/,
     updated Feb 19, 2025, organic content). **Whether this applies to ads is UNVERIFIED.**

### The stack

| Step | Pre-launch | Post-launch |
|---|---|---|
| World stills and film plates (blank placeholder) | Higgsfield PLUS (generic inputs only). For a client who wants **"nada do meu lançamento treina IA"**: Adobe Firefly partner models or Google AI Studio with billing. | Higgsfield |
| Cutout, label composite, shading, export with Content Credentials | Photoshop desktop, working on local files (Photography plan) | Same |
| Label on a moving bottle in the 15 s film | Local tracking composite in a desktop editor. Feasibility for Sol is **UNVERIFIED** (another agent's hole). | Same |
| Music | Artlist AI Starter (or Lyria US$0,08/song on paid AI Studio) | Same |
| Fidelity report and OCR | Local script | Same |
| Layout of commerce assets | Photoshop, or Canva with the AI toggle off | Same |

**Monthly cost (published USD):**
- Higgsfield PLUS US$49 + Adobe Photography US$19,99 + Artlist AI Starter US$19,99 = **US$88,98/month ≈ R$463** at the
  file's PTAX 5,2037.
- With ULTRA (needed from about 2 full launches a month): **US$168,98 ≈ R$879**.
- The "sigilo total" add-on is Firefly Pro at US$19,99.

### Wording Sol can use safely

**Offer sheet, replacing "Sua arte não entra em nenhuma IA antes do lançamento":**
> *"Sua arte nunca é enviada a nenhum gerador de imagem ou vídeo — nem antes, nem depois do lançamento. A IA cria só o
> cenário, com uma embalagem em branco; o seu rótulo é aplicado no nosso computador, a partir do seu arquivo. Por
> isso, por nosso intermédio, a sua arte nunca é usada para treinar IA."*

**Offer sheet, replacing "As imagens são suas…":**
> *"Tudo o que entregamos é seu para usar, sem prazo e no mundo todo: site, redes, marketplaces, anúncios pagos,
> impressos e ponto de venda. Formalizamos isso num termo de cessão por escrito, junto com a nota fiscal, e não
> reutilizamos nem revendemos nada do seu projeto. A trilha do filme é criada para uso comercial e vai junto com o
> filme."*

Change *"6 fotos"* to *"6 imagens"*.

**In the cessão, the fine print that keeps it true:**
> *"As peças combinam a sua embalagem, aplicada a partir da sua arte, com cenários gerados por IA. A proteção autoral
> de elementos gerados por IA pode ser limitada, e ferramentas de IA podem gerar cenas parecidas para terceiros; por
> isso a exclusividade que garantimos é a nossa: não reutilizamos nem licenciamos essas peças a ninguém. As peças
> podem conter credenciais de conteúdo (C2PA) que plataformas usam para indicar uso de IA; não as removemos. Se
> qualquer peça receber reclamação de direitos, nós a substituímos sem custo. A responsabilidade total fica limitada
> ao valor do pedido."*

### What would make "as imagens são suas" false, even after the repair

- Anyone on the job uploads a client file to Higgsfield, Kling, Runway, Luma or CapCut.
- Artlist **stock** music goes into the film. The client can't re-edit it, and must publish while Sol's plan is active.
- The deliverables are made on a free tier:
  - Photoroom, Kling and Luma free tiers are non-commercial.
  - Higgsfield's free tier is watermarked.
- A real person's face is used (Soul ID) without a signed image release and consent.
- The written cessão is missing. Under Lei 9.610 art. 49 III–IV the transfer then defaults to **5 years, Brazil
  only**.
