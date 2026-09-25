# DD1 — source log. Hunt 6 deep-dive: "THE PLATFORM PAYS THE AGENT" (O ELENCO, the TikTok Affiliate Partner model). 25 Sep 2026

All pages fetched with curl and a browser User-Agent unless marked otherwise. Raw files are in `work/dd1/`: `d_*.json`/`d_*.txt` for partner-centre docs, `u_*.html`/`u_*.txt` for seller-br academy pages, `h_*.html`/`h_*.txt` for everything else. "Search summary" means only the WebSearch summary was read, not the page.

## A. TikTok Shop Partner Center (partner.tiktokshop.com, document API, workspace_id=3). The doc tree is `work/w2e/tree_3.json` (965 nodes).

- **64f1989064ed2e0295f3c1b5, "Partner service categories"** (updated 30 Oct 2025)
  - Affiliate Partner, Brazil → Brazil: "Seller and Scalable Creator Match-up — Connect scalable creators with sellers/supply chains to help both parties improve efficiency and optimize creator level up."
  - MCN/CAP "Creator Management" is also listed for Brazil → Brazil.
  - The BR TSP rows are Shop Operation, LIVE Stream Management, Short Video, Affiliate Management ("help sellers … set competitive commissions … launch seller-initiated campaigns"), Paid Media, Mass Recruiting and Mass Tutoring.
- **64f19899cb677b0286e75d67, "Partner registration application requirement"** (updated 14 Sep 2026)
  - A TAP needs a full company name, a company registration number and a company document ("Selection based on company entity"; the guidance is on Feishu and was not readable). It also needs business-owner ID, a logo and an address, and TikTok may ask for UBO documents.
  - Proof: "Please upload at least 1 of the following 4 kinds of ability certificates": a signed creator contract or a cooperated creator's profile · a seller partnership agreement, or 7 days of sales data on another platform · another e-commerce affiliate platform account with 7 days of sales · a self-developed affiliate tool.
  - There is no minimum creator count and no minimum GMV.
- **64f198679495ef028184fa10, "Non-US TAP"** (updated 7 May 2025): "The Affiliate Partner program is currently available in Indonesia, Malaysia, Philippines, Thailand, Vietnam, United Kingdom". It does not list Brazil (stale). It confirms TAPs "earn commissions based on the sales of all products promoted by creators".
- **650a395adefece02be63046f, "Partner Collaboration"** (updated 30 Apr 2026)
  - The mechanism, verbatim: sellers "register for products, and define the product commission rate (commission should be a package)". The TAP's "Commission rate requirement … is the total of affiliate partner commission rate and creator commission rate … 1-80%".
  - "You can only cooperate with sellers in the same market."
  - The local-partner list is SEA only. Bank-linking instructions exist for SEA and UK only.
- **659e026753c4d402e1682ad4, "US TAP"** (6 May 2025)
  - "Sellers … determine the commission they would like to offer to the agency. Then the agency chooses the commission they would like to set for the … Creators".
  - "The agency can only collect commission from the Seller. The agency cannot collect commission from the Creator, as this would be considered 'double dipping.'"
  - Creators get an alert if a campaign rate is lower than the rate they already receive on that product.
- **69c3d3c26453bb04a3ed0513, API "Search Tap Affiliate Orders"** (updated 24 Sep 2026)
  - `partner_standard_commission_rate`: "Between seller & TAP"; `creator_standard_commission_rate`: "Between TAP & creator".
  - `partner_tap_bonus_commission_rate`: "The additional commission rate TikTok Shop offers to affiliate partners for driving product sales in specific campaigns". This is a PLATFORM-FUNDED bonus.
  - `settle_status` includes INELIGIBLE (refund/cancel) and FROZEN (fraud).
  - It has tax fields for MEXICO partners (ISR/IVA) but NONE for Brazil.
- **650a33f2c16ffe02b8e4c4c4, "Finance (Non-US)"** (16 Jun 2025)
  - "Available Market: UK, ID, MY, VN, TH, PH, SG". No BR.
  - Fields: "Commission bonus rate — Rate of the commission bonus funded by TikTok".
- **67e1390ae2bca304a1450a92 (UK) and 67dcd083cfbe6c04a15be01d (US) finance guides**: payout "15 days after the order delivery date", thresholds £1 / US$1. No Brazilian equivalent exists in the tree.
- **650a34b4f1fd3102b9206dbc, "Fee Agreement/Commission Sharing"** (MCN/CAP): "Available Market: UK, ID, MY, VN, TH, PH, SG". No BR.
- **6506bbf2de672602b7bc0697, GLOBAL Partner Center ToS** (updated 15 Sep 2026)
  - §6: "TikTok is not obligated to determine Your tax obligations … You are responsible for the issuance of tax invoices".
  - Section B (SEA) and Section C (UK) contain Affiliate-Partner PAYMENT-SERVICE clauses: PIPO / Stripe "collecting Affiliate Partner Commissions from a seller … transferring the Creator Commission … to the Creator".
  - **Section E Brazil contains only E1 language and E2 anti-corruption. It has NO payment-service clause for TAP campaigns.**
  - §20.7: governed by Brazilian law, Central Courts of São Paulo.
- **6506bc5ede672602b7bc0efb, Violation Management**: a 120-point system. Termination can follow "Leakage of key business information (GMV data etc.) … accepting interviews with the media".
- **68411b45314d2504a1a7c407, [US] Partner Tiering**: tiers are 80% GMV-weighted and apply to TSPs.
- **Leaderboard API**: `seller-br.tiktok.com/api/v1/open/portal/leaderboard` returned code 98001004 on every parameter set tried; `/open/market/leaderboard` returned 98001002 ("You must log in"). `/partners/br/leaderboards` is JS-rendered only. ⇒ **The BR TAP leaderboard exists (see W2E's i18n string) but its data is not publicly readable.**

## B. TikTok Shop BRASIL, seller/creator academy (seller-br.tiktok.com), "Aplica-se a: Brasil"

- **knowledge_id=7846364793341713, "Programa de tráfego de afiliados da plataforma"** (12/08/2026)
  - "Se um produto estiver inscrito somente na Colaboração direcionada, apenas criadores convidados podem promovê-lo. **A mesma condição se aplica a produtos inscritos em uma campanha de TAP.**" ⇒ TAP campaigns are LIVE in Brazil. This is the primary BR evidence.
  - The same page says TikTok's own accounts (@earnorn4934, @cutcut9040, @searchbr2, @feedsyou, @bigbonus44) earn affiliate commission on every open-collaboration product: "você pagará uma comissão à campanha da plataforma … inscrição será automática". The platform is itself a competing affiliate.
- **knowledge_id=3355295847515925, "Alteração … taxa de comissão predeterminada do criador na colaboração aberta"** (21/09/2026, effective 23 Sep 2026). 167 subcategory rows. Beauty:
  - Fragrâncias 12,0% → 10,0%
  - Cuidados com a pele 12 → 10
  - Cuidados e modelagem do cabelo 12 → 10
  - Cuidados masculinos 12 → 10
  - Maquiagem 10 → 8
  - Cuidados com banho e corpo 10 → 8
  - Unhas 10 → 8
  - Aparelhos 8 → 7
  - Fashion subcategories 10 → 8
  - ⇒ **TikTok cut default creator commission by 2 points across beauty two days ago.**
- **knowledge_id=6872849933141776, "Opt-In Automático para Colaboração Aberta"** (10/04/2025)
  - All future products are auto-added to Open Collaboration at "a taxa de comissão sugerida média de acordo com a categoria".
  - Worked example: a 10–15% suggested range yields about 13%.
- **knowledge_id=6583987620562705, "Configurações de Comissão"** (10/04/2025)
  - A commission cut applies to existing creators only after 30 days.
  - Worked example: 15% → 12%.
- **knowledge_id=3275818982590224, "Termos de Uso para Criadores"** (BR, 23/07/2025)
  - "(b) Parceiros de Afiliados — agências que prestam serviços a Vendedores por meio da criação e gestão de campanhas … **Nas Campanhas de Parceiros de Afiliados, você presta seus Serviços do Criador aos Parceiros de Afiliados e recebe comissão dos Parceiros de Afiliados, e não dos Vendedores.**" ⇒ The creator is legally the TAP's service provider. This is a C3 grey area and a tax-base question.
  - "Você atua como contratante independente, prestando os Serviços do Criador diretamente a Vendedores, Parceiros de Afiliados…".
  - The PSP for BR creators is EBANX Instituição de Pagamentos Ltda., CNPJ 21.018.182/0001-06, paying "a parte dos pagamentos feitos por compradores que é devida a você, conforme acordado entre você e o Vendedor, Parceiro de Afiliado".
  - MCN/PAC "atuará como seu agente pelo período mínimo de vigência indicado no convite".
  - The TAP "poderá visualizar e exportar seus dados de desempenho".
- **knowledge_id=3268441302615809, "Termos de Serviço do Vendedor"** (BR; the page shows 26/05/2026; the text is dated 21 Jan 2026)
  - "Serviços de Parceiros … rede multicanal, prestador de serviços independente, parceiro afiliado ou caçador de talentos … registrado no CPTTS".
  - Creator commissions are deducted from buyer payments by the PSP.
  - The seller's PSPs are PIPO Brasil IP Ltda. (CNPJ 46.683.038/0001-07) and dLocal Brasil.
  - The intermediary is ByteDance Brasil Tecnologia Ltda.
  - The terms say nothing on how a TAP's partner commission is settled.
- **knowledge_id=1517752301717265, "Comissão afiliada para criadores"** (01/07/2026), per W2E: commission is paid after the order settles, and refunds reverse it.
- **knowledge_id=6580476438529809, "Colaborações do Affiliate"** (14/04/2025)
  - The seller's "Descobrir criadores" has an "Agência do criador" filter: "filtre os Criadores se eles forem gerenciados por uma agência".
  - The menu has a section "Gerenciar Criadores Afiliados e Agências". Its child articles are collapsed and were not retrieved.
- **knowledge_id=1487157475673872, "Perguntas Frequentes sobre Impostos"**: "a Bytedance Brasil Tecnologia Ltda. … emitirá mensalmente notas fiscais referentes aos serviços cobrados de você". This covers sellers; nothing covers TAPs.
- **knowledge_id=3901287218562833, "Guia de Compartilhamento de Links de Afiliados para Criadores"** (20/01/2026): the External Traffic Programme, and campaign links.

## C. Earlier-verified TikTok pages re-used (fetched by W2E; quotes re-read in the saved HTML)

- **seller-us.tiktok.com knowledge_id=6543118107477774, "[TAP] Creator Matchmaking"** (05/14/2026)
  - "+5% commission above Open Plan"; "pay more only when creators drive new sales".
  - "Agencies can choose how to split the added commission between themselves and the creators".
  - "Merchants are the source of income … (some may receive rebates and marketing expenses from merchants)"; fulfilment rate "75-80%".
- **newsroom.tiktok.com/tiktok-shop-cresce-102-vezes-em-seu-primeiro-ano-no-brasil** (Jun 2026)
  - GMV ×102 and active affiliates ×46; lives ×20 and live GMV ×161; top lives are in cosméticos.
  - Beauty top 3: bodysplash feminino, bodysplash masculino, perfume masculino.
  - BigHome: R$17 M in 2026, 300 active affiliates per 28 days. Moderna: >9.000 active affiliates, >10.000 units/day.
  - Lua Blossom: >R$1 M GMV from fragrance lives. Vitória Merlos: R$2,8 M (R$2,4 M from lives, >200 lives, >R$400 k in one live).
- **seller-br.tiktok.com/partners, i18n string**: "sc_leaderboard_partners_list_page_sub_ranking_name12_br_explanation": "This leaderboard ranks TAPs (TikTok Affiliate Partners) based on their monthly GMV from partner collaborations". The label is "Creator Sales Ranking".

## D. TikTok LIVE Agências (entertainment/gifting)

- **https://www.tiktok.com/live/creator-networks/pt-BR**
  - "bônus dos programas de incentivo"; "as Agências podem participar de programas de incentivo exclusivos para bônus mensais"; recruiting "nos Bastidores da LIVE … lista de possíveis criadores … programas de indicação".
  - The application needs a "Certificado de incorporação ou registro · Informações sobre acionistas · Principais informações sobre a gestão e o pessoal". Review takes 5–7 business days.
  - Global stats: 240 mi+ creators went LIVE; agencies +90%/yr.
- **…/pt-BR/article/incentive-policy** (the redirect from 7312093162964210693): generic; no rates published.
- **…/pt-BR/article/tiktok-live-creator-networks-guide** (29 May 2026): agencies are "organizações terceirizadas e independentes do TikTok"; "Milhares de Agências em todo o mundo".
- **…/pt-BR/blog/diamonds-for-tiktok-live** (17 Aug 2026): Diamonds come from gifts. This is gifting, not Shop.
- **https://hotstage.com.br/agencia-de-live-tiktok/** (a BR agency; seller claim): "Uma agência não pode descontar nada de seus ganhos … O próprio TikTok remunera essas agências".
- **https://www.mouraagency.com/tiktok.htm** (a BR agency; seller claim): "até cerca de 50% do que o público gasta"; "tabela de pagamentos da agência por metas atingidas por dias, horas e diamantes"; "a agência não cobra nenhuma taxa".
- The agency's own share of the incentive is published NOWHERE. UNVERIFIED.

## E. Other Brazilian platforms that pay an agent

- **Shopee — https://help.shopee.com.br/portal/10/article/124094 (Programa de Afiliados Shopee — Termos e Condições)**
  - "redes multicanais registradas ('MCNs') podem ganhar determinadas taxas e/ou comissões por colaborarem com Afiliados e Vendedores Participantes".
  - §2.4.2–2.4.3: the MCN invites affiliates with a "Divisão MCN-Afiliado", and creates "Campanha MCN" where sellers register products at a "Taxa de Comissão do Vendedor Modelo MCN". The commission is "deduzida automaticamente do valor pago pelo comprador … distribuída entre o MCN e o afiliado conforme a divisão previamente acordada".
  - §3.4: paid "dentro de sessenta (60) dias após a aprovação do sistema".
  - §3.4.1/3.9: a PJ is paid only against an NFS-e, codes 10.08 / 17.06 / 17.25.
  - §3.4.2: "a Nota Fiscal deverá ser emitida diretamente para o Vendedor" (one NF per seller).
  - §3.5(ii): Shopee acts "exclusivamente como mandatária do Vendedor".
  - ⇒ The Brazilian MCN/agency payout is DOCUMENTED here, unlike TikTok's TAP.
- **Shopee — https://help.shopee.com.br/portal/10/article/147083 (Hub ↔ Afiliados)**: first partnership 15–90 days, then 15–360. The affiliate is exclusive to one Hub. The entry requirements for a Hub are not published (UNVERIFIED).
- **Shopee — https://help.shopee.com.br/portal/10/article/124095 (Comissionamento)**: "3% para compras realizadas por clientes existentes"; lives 3%; Shopee Vídeo 3%; with seller extra "podem chegar até 30%".
- **Mercado Livre — https://www.mercadolivre.com.br/l/afiliados-home**: "Você pode receber até 16% pelas vendas aprovadas". No agency/MCN split found on the page. The T&C page https://www.mercadolivre.com.br/ajuda/30228 returned 403 to WebFetch, and curl got a JS shell. ⇒ pays_agency is false as far as seen; UNVERIFIED.
- **Amazon.com.br Associados — https://associados.amazon.com.br/help/node/topic/GRXPHT8U84RAYDXZ**: "Tabela 1 – Comissão Padrão Fixa … Bebê | Beleza | Beleza de Luxo | Saúde e Cuidados Pessoais … 13%". Paid to the account holder; there is no agency split.
- **Kwai Shop — https://seller-shop.kwai.com/pages/home**: i18n strings show a seller-referral field ("Pela recomendação de parceiro da Kwai Shop", "Nome do parceiro da Kwai Shop") and a "comissão para iniciantes … tão baixa quanto 2%". No affiliate-agency/MCN payout programme was found. UNVERIFIED.
- **Magalu Parceiro**: the official page returned an empty shell. The search summary says 2–12% and 11% INSS on pessoa física (SECONDARY; contabilidade.com, divulganinja). This is an individual storefront, not an agency tier. UNVERIFIED.

## F. Occupancy: Brazilian agencies already in the seat

- **https://china2brazil.com.br/iest-group-lanca-agencia-especializada-no-tiktok-shop-em-nova-era-do-e-commerce/** (26 Jun 2025): IEST Group's ECN.
  - "A ECN apoia os criadores por meio de duas frentes principais: o CAP … e o TAP … No TAP, o modelo é baseado em comissionamento".
  - It is also a TSP with "sete serviços oficiais", and "casting próprio e modelo de marketplace". Chinese-backed.
- **https://lp.amplifyugc.co/comunidade** (© 2026): Amplify.
  - "500+ Creators · 80+ Marcas · R$2M+ em GMV"; "Top 4# do TikTok Shop"; "Mais da metade da comissão" (to the creator); "Acesso a campanhas — amostras grátis especiais toda semana"; an app, a group and events.
  - Contact is a Gmail address. ⇒ This is O ELENCO, already running.
- **https://www.agenciatokz.com/**: "PARCEIRA OFICIAL DO TIKTOK BRASIL"; "Curadoria e Recrutamento de Afiliados e Criadores"; "Gestão de Lives com Afiliados e Live Sellers"; bespoke pricing.
- **https://accessagencia.com.br/sou-marca/**: "Gestão de afiliados e UGC | Shopee, TikTok One e TikTok Shop … Recrutamento de creators · Organização de comissionamento … Ecossistema próprio de criadores".
- **https://www.portaldapropaganda.com.br/noticias/32882/…** (12 May 2025): Snack Content, homologated by TikTok Shop US in May 2024; BR "clientes Always-On (AON), com parcerias contínuas baseadas em compartilhamento de GMV".
- Continuum ("parceira oficial … recrutamento, gestão e escala de afiliados"): search summary only, UNVERIFIED.
- MindgruveMacarta + Outlandish: prnewswire, search summary only.
- **https://centraldovarejo.com.br/tiktok-shop-registra-alta-de-154-em-moda-e-151-em-beleza/** (3 Sep 2026)
  - Beauty is +151% H1 2026 vs H2 2025.
  - "A Amend reuniu mais de 700 criadores no Amend Lab … 30 mil vídeos". This is a BRAND recruiting creators in-house.
  - INSIDER: "90% da receita … influenciada por conteúdos de criadores".

## G. Market size (SECONDARY)

- **https://www.seudinheiro.com/2026/economia/tiktok-shop-mira-r-20-bilhoes…** (29 Aug 2026): BTG Pactual estimate, "cerca de R$ 20 bilhões em vendas anualizadas no Brasil ainda em 2026"; 134 M users.
- Momentum Works: "R$5,3 bi GMV H1 2026 · 110.200 lojas ativas · 2,3 M influenciadores cadastrados · ~200 creators >R$1 M". Search summary only, UNVERIFIED.
- Shakers blog (per W2E): beauty 21% of sales. SECONDARY.
- **https://www.administradores.com.br/noticias/tiktok-shop-transforma-descoberta-em-compra-e-abre-nova-frente-para-o-mercado-de-afiliados**: restates the newsroom figures.

## Not reachable / not used
- The BR TAP leaderboard data (login/JS-gated) and the seller-br academy search API (98001004 / login).
- Feishu/Lark guidance docs linked from the partner centre (bytedance.feishu.cn), including the company-document-type list, so whether a MEI is accepted is UNVERIFIED.
- themuse.com TikTok job pages (404/empty); ML T&C (403); the Amazon fee schedule node (error page; the alternate node was used).
- Etsy and Faire were not attempted, per the brief.
