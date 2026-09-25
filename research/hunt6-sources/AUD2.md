# AUD2: audit of the contract-manufacturer launch-kit channel (Hunt 6)
Auditor AUD2, 25 Sep 2026. Every page listed below was fetched from this session with curl or WebFetch. Working files are in `hunt6/work/aud2/` (pages/, holders_12m.csv, mfr_launch_events.csv, build.py).

**Verdict: DEAD as a resale channel (refuted = true).** One referral leg survives as an add-on. Its floor is US$0–300/month, and its ceiling is about US$1.200–1.900/month net with 4–6 partners, which is still below the bar.

## The ANVISA data, recomputed from H6A's files

Source file: `TA_CONSULTA_COSMETICOS.CSV` (from H6A's `hs_brand.pkl`).

**Ranking of hair/skin holders, 12 months to 23 Sep 2026** (`aud2/holders_12m.csv`)
- Holders with ≥100 notifications and ≥10 brand keys: **56 holders, 12.205 notifications, 29,3%** of 41.595.
- Removing four own-brand multi-line houses (Unilever 216, Boticário 210, Natura 152, Gram/Haskell 103) leaves **52 holders, 27,7%**. H6A reported 58 / 30,1%.

**The "73% made by manufacturers" share**
- With 12-month brand keys, holders with ≥10 keys hold **917 of the 1.667** brand keys that have ≥6 new notifications, which is **55%**. H6A reported 73%, using a different key count.
- The share is definition-sensitive, and the multi-key group still includes own-brand houses (Boticário, Dahuer, Farmax).

**Launch events per manufacturer** (`aud2/mfr_launch_events.csv`)
- Method: electronic rows only; midnight-stamped legacy rows dropped; exact-name re-notifications dropped; brand-key windows split at gaps of more than 21 days.

| Manufacturer | Windows/month | New brand keys/month |
|---|---|---|
| Veneza | 35,2 | 21 |
| Briefing/Suportt | 28,2 | 15 |
| Império | 22,2 | 14,9 |
| SDK | 21,1 | 14,3 |
| TCI | 15,5 | 6,1 |
| HF/Vonshér | 14,3 | 9,9 |
| Alfahair | 13,8 | 7,5 |
| DC Beauty | 9,6 | 6,1 |
| Século | 9,2 | 3,7 |
| Pack to You | 7,7 | 5,7 |
| JK | 5,8 | 4,6 |
| WB | 2,8 | 1,3 |
| Cosmo | 2,5 | 0,7 |
| Florus | 1,0 | 0,9 |

- Across all 158 manufacturer-like holders (≥50 notifications, ≥10 keys, own-brand houses excluded): **8.261 windows a year and 5.098 new brand keys a year.** Both are upper bounds.

**Two sanity checks**
- Most of Veneza's brand keys first appear in 2025–26: 198 in 2025 and 156 in 2026, against about 9 in earlier years. So Veneza only recently began notifying in its own name.
- Sampled new keys are real micro-brands (Mivoa, Biomelan, Gomic, Lummi, Plenna, Natasha Azarany Beauty, Chenchen Kosme, SAL7…). About half the keys are noise words, but the rows behind them are still distinct brands (JC Estética, IntimaUp, Frutae Derm, YVY…).

**CNPJ records** from https://publica.cnpj.ws/cnpj/{cnpj}, 42 lookups (list in `aud2/cnpj_mfr.txt`)
- Almost every top notifier self-declares ME/EPP. Veneza says Micro Empresa with R$100k of capital, although it claims 1.177 brands, so the porte field is stale.
- The #1 holder's legal name is **"+ BRIEFING AGENCIA DE PUBLICIDADE E REPRESENTACOES LTDA"**, trading as SUPORTT PROJETOS EXCLUSIVOS, Guarapari/ES. Its email is maisbriefingagencia.adm@gmail.com.

## Manufacturer services pages (one line per URL: what it said)

**Veneza**
- https://vnz.ind.br/ : "+28 anos · +1.177 marcas já criadas · +9.777 produtos". Plans: TERC linha pronta from R$5.000 (24 units/SKU); personalizada R$10.000 (240 units); fórmula exclusiva R$20.000; escala R$50.000. It also claims "Construção de marca: Do produto à identidade" and "o prazo … Até 30 dias corridos após a entrega dos rótulos".
- https://vnz.ind.br/termos-terceirizacao/ : "o custo do rótulo não está incluso no orçamento dos produtos … o cliente pode contratar designer/agência de preferência para um projeto mais completo"; "O rótulo é negociado diretamente entre cliente e gráfica"; "Taxa por produto: R$ 437,50 por item" for ANVISA; "o prazo começa a contar somente após a aprovação do rótulo".
- https://vnz.ind.br/clinicas/ : a lead form asking clinics for capital to invest (R$10–100k) and whether they already have a logo.
- https://vnz.ind.br/catalogo-de-embalagem/ → catalogo-embalagens-premium.pdf : 11,3 MB, 30 pages, image-only (no extractable text).
- https://vitturia.com.br/ : Veneza's own line: "mais de 400 produtos em linha" for people starting a brand.

**Pack for You / Pack To You**
- https://www.packforyou.com.br/servicos/ : "Somos Full Service! … Criação da Marca · Desenvolvimento da Identidade Visual · Criação do Rótulo · Publicidade"; "equipe de marketing especializada para desenvolver embalagens e rótulos"; "Flyers e catálogos; Material de promoção".
- https://www.packforyou.com.br/terceirizacao-de-cosmeticos/ : "Marketing … oferecemos assessoria de marketing completa para sua empresa".
- Its WhatsApp number (14) 99821-3630 matches the CNPJ record of PACK TO YOU (42773644000162), so they are the same company.

**SDK and Vonshér (HF)**
- https://sdkcosmeticos.com.br/ : "DESIGN Oferecemos uma assessoria integral no design de embalagens, incluindo layout, rótulos, silk ou hot e cold stamping, além de materiais promocionais".
- https://lp.vonsher.com.br/ (HF, CNPJ 06195970/0001-76): "Aprove o design do produto"; "suporte de marketing e conformidade com a ANVISA"; "Transforme sua Influência em uma Marca de Sucesso".

**Século**
- https://seculocosmeticos.com.br/marca-propria-de-cosmeticos-influencer : "Criação completa de marca e design. Desde a escolha da embalagem até a criação dos rótulos". The WhatsApp link text reads "Vi seu anúncio no Google Ads", so it buys Google Ads.
- https://seculocosmeticos.com.br/terceirizacao-de-cosmeticos-capilares-dono-de-marca : "Criação completa do design do seu produto".

**DC Beauty**
- https://dcbeautycosmetics.com/inicio/ : the terceirização steps are "INDUSTRIALIZAÇÃO · AGÊNCIA DE PUBLICIDADE · AGÊNCIA DE MARKETING DIGITAL".
- http://portfolio.dcbeautycosmetics.com/ : "Agência de Publicidade / Marketing Digital … Desenvolvimento de MARCA, PRODUTOS e CAMPANHAS. Profissionais de ilustração em 3D, ilustração convencional, produtora de vídeos e animações, retoque de imagens". **This is the launch kit itself, bundled in-house by the #12 notifier.**
- https://dcbeautycosmetics.com/sobre/ : "Design e Branding … feito por profissionais gráficos".

**Other manufacturers, in order of notification volume**
- https://www.wcosmeticos.com.br/ : "Design profissional de rótulos e identidade visual"; "Criamos os rótulos e identidade visual dos produtos".
- https://naturallybios.com.br/ : the white-label flow is "Escolha do Produto · Desenvolvimento do rótulo · Registro ANVISA · Produção".
- https://athenascosmeticos.com.br/ : no design or marketing mention. Its clients (WePink, Jequiti, Eurofarma) are established brands.
- https://stoaindustria.com/ : "criação de marca, identidade visual e marketing digital".
  - /blog/como-funciona-o-setor-de-criacao-de-marca-da-stoa/ : the service covers "Estratégia de Marca, Identidade da Marca e Marketing de Conteúdo … posts publicados nas redes sociais".
  - /influenciadores/ : "Criação de marca … trabalham lado a lado com você pra capturar toda a magia dos seus produtos".
- https://amoscosmeticos.com.br/terceirizacao-de-cosmeticos-marca-propria/ : no design offer. The brand is told to focus on "posicionamento, vendas, marketing".
- https://cosmeticgroup.com.br/ : production starts "Com embalagens, rótulos e matérias-primas em posse" (client-supplied).
- https://nossafabrica.ind.br/como-funciona-o-sistema-full-service/ : "Identidade Visual Inigualável: Criamos uma embalagem e rotulagem personalizadas … Marketing estratégico".
- https://frosinicosmeticos.com.br/ : "Desenvolvimento de identidade visual … Branding: Contamos com uma equipe de marketing capacitada".
- https://lewcosmeticos.com.br/ : consultoria and marketing olfativo; "rótulos personalizados de acordo com sua identidade visual".
- https://www.mzcosmeticos.com.br/informacoes/terceirizacao-de-cosmeticos : terceirização keeps "o foco do contratante em branding, distribuição". No design offer.

**Florus**
- https://www.florus.com.br/ : "Identidade Visual: Design de logotipo e rótulo"; "Parcerias estratégicas e indicações de fornecedores … Designers" (referral).
- https://www.florus.com.br/blog/como-lancar-uma-marca-de-cosmeticos-com-pouco-dinheiro/ : "Ferramentas como o Canva permitem criar logotipos, embalagens e materiais de marketing de forma gratuita ou a baixo custo"; send kits to micro-influencers. **The manufacturer's own advice to budget clients is do-it-yourself.**
- https://www.florus.com.br/blog/como-divulgar-marca-de-cosmeticos/ : "Se necessário, contrate um profissional ou agência especializada em marketing digital".
- https://www.florus.com.br/blog/custo-para-lancar-marca-propria-de-cosmeticos/ : no visual-cost figures.

**Private, Multlabel, BeHub**
- https://privatecosmeticos.com.br/ : "Se ainda não tem identidade visual ou rótulo definido, indicamos parceiros especialistas em branding e design gráfico" (referral). A testimonial says the factory "ainda ajudou com o design da embalagem".
- https://privatecosmeticos.com.br/blog/quanto-custa-criar-marca-de-cosmeticos : no figures for visuals.
- https://multlabel.multquimica.com.br/ : "Criamos fórmulas, rótulos e embalagens sem custo adicional". **This is the free front door, verbatim.**
- https://behub.com.br/servicos-de-design : a design service whose deliverables include "Mockups 3D fotorrealistas" and "Versões digitais (PNG/JPG otimizados)"; "Mockups 3D fotorrealistas inclusos"; regulatory review is folded in.
- https://behub.com.br/terceirizacao-cosmeticos : Full Service; "O contratante foca exclusivamente em marca, marketing e vendas".

**Suportt, and matchmaking services**
- https://portaldorepresentante.com.br/empresas/38009-suportt-projetos-exclusivos-/ (WebFetch): "Fabricamos marcas próprias na forma de terceirização"; Guarapari/ES; recruits representatives.
- https://www.casadacosmetologia.com.br/terceiriza-beauty : ABC's free programme matching brands with member terceiristas. It sells no design.
- https://www.ingredientescosmeticos.com.br/terceiristas : a directory of terceiristas (Florus, Lipson, Pack for You, Athenas…).

**Sites that could not be read**
- gruposuportt.com.br: DNS failure.
- imperiocosmeticos.com.br, alfahair.com: connection reset, then 503.
- jkformulas.com.br, dcbeauty.com.br: DNS failure (DC Beauty was read at dcbeautycosmetics.com instead).
- wbbeauty.com: HTTP 500.
- ctecindustria.com.br, ecopluscosmeticos.com.br, carpeind.com.br, higiafytos.com.br: reset or 502.
- jhscosmeticos.com.br: 403. liegecosmetics.com.br: certificate host mismatch. multlabel.com.br: expired certificate (read through the multquimica host instead).
- TLS was never bypassed.

## Client-side prices (observed listings)
- https://orbelabel.com.br/ : label R$200, "Mockup 3D incluso"; a line of 3 labels R$450; logo + label R$420; identity from R$800; 50% upfront.
- https://www.estudiofabrica.com.br/servicos-e-precos/ (São Paulo, centro expandido):
  - AI "Imagem Conceito/ Campanha/Redes sociais" R$53 per image.
  - AI video of 15–20 s R$260.
  - Still on white R$25 per image (1–49), falling to R$18 (100+).
  - Studio half-day R$1.250 including 50 images.
  - AI lookbook R$35 for 3 images.
- Vintepila gigs (Brazilian gig marketplace, asking prices):
  - https://www.vintepila.com.br/servicos/video-e-animacao/eu-vou-criar-videos-com-ia-para-anuncios-reels-tiktok/ : "Fazer o comercial do seu produto em até 24 horas" R$20 (★5,0, 340 reviews, 700 sold); another at R$40 (170 sold); another at R$60 (177 sold).
  - …/eu-vou-vou-criar-video-de-produto-profissional-com-ia/ : AI product video R$29, plus R$20 per extra video.
  - …/eu-vou-videos-ugc-com-ia-para-produtos-de-beleza/ : AI UGC video for beauty brands R$20 (new seller).
  - …/eu-vou-fazer-uma-modelo-ia-para-seu-produto/ : AI model with the client's product R$100 (★5,0, 125 reviews, 170 sold).
  - …/eu-vou-melhorar-fotos-dos-seus-produtos-com-ia/ : R$20 (104 sold).
  - …/eu-vou-criar-imagens-profissionais-com-ia-4/ : R$20.
- https://influenciadoria.com/usos/criar-video-de-produto-com-ia/video-lancamento-produto : Brazilian AI-video SaaS at R$67 / R$117 / R$297 per month, paid by PIX.
- Higgsfield: US$49 a month (HIGGSFIELD_FACTS.md). Product Shot 2K ≈US$0,075; 15 s 720p video ≈US$4,46 (https://higgsfield.ai/blog/new-marketing-studio-higgsfield, via H6D).
- https://fotografiasdeprodutos.com.br/fotografias-de-produtos-tabela-de-preco.html : "R$ 7,00 por fotografia" appears in the page title only. The page gave a reset and then 503, so this is **UNVERIFIED**.
- https://www.cronoshare.com.br/quanto-custa/fotografia-produto : aggregator, secondary, not used.

## What the audit changes
1. **The free front door is confirmed in the manufacturers' own words.**
   - 13 of the 20 pages read bundle label or identity design.
   - At least 7 bundle marketing beyond the label.
   - DC Beauty already sells the kit itself: 3D, video, animation and campaigns.
   - Multlabel gives design away: "sem custo adicional".
   - Label designers include a photorealistic 3D mockup at no extra cost (Orbe, BeHub), so the packshot layer is also free.
2. **No manufacturer resells a third party's creative service.**
   - The ones that do not bundle design refer out (Florus, Private) or push the cost to the client (Veneza).
   - In a referral, every client is a fresh sale, so ORIGINATION-ONCE fails.
   - The one precedent for an add-on line is Veneza's own R$437,50-per-item ANVISA fee.
3. **Price.** The observed replacement for 6 lifestyle images plus a short film runs from R$149 (Vintepila) to R$578 (a São Paulo studio).
   - A micro-brand whose first production order is R$5.000 will not pay H6A's R$1.500–2.500.
   - A manufacturer with an in-house designer will not pay much more than that designer's time plus US$49 a month.
4. **Arithmetic.**

| Kit price | Kits/month needed for the bar | Referral partners needed |
|---|---|---|
| R$300 | 42–53 | 10–20+ |
| R$500 | 25–32 | 6–12 |

   - Partners can only come from the roughly one-third of manufacturers that do not design in-house.
   - Capacity after sales calls is about 67–72 hours a month, which fits 22–48 kits at 1,5–3 hours each.
5. **Treadmill.** Each frontier model release makes the manufacturer's in-house designer, who already holds the label file and the bottle geometry, able to do this alone. That moves the business toward OBSOLETE. It is THE REPLACEMENT-COST CEILING in its purest form: **the channel partner owns every input.**
6. **Corrections to H6A.**
   - The share of brands made by multi-brand holders is 55%, not 73%, with 12-month keys. The figure is definition-sensitive.
   - The top concentration is 52 holders = 27,7% once own-brand houses are removed, not 58 = 30,1%.
   - H6A's R$1.500–2.500 kit price is 3–17 times the observed band.
