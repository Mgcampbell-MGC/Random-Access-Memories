# AUD5 — source log, audit of A BANCADA (W2E's live-host casting desk). Hunt 6, 25 Sep 2026

All pages were fetched with curl and a browser User-Agent unless marked otherwise. Raw files are in `work/aud5/`.

## Demand: live-host hiring, measured

- **br.trabajo.org**, four queries paginated to the end: `empregos-apresentadora+live+tiktok` (29 pages), `apresentador+de+live` (6), `live+seller` (8), `host+de+live` (7).
  - Together they return **792 unique listing URLs**. Filtering by title leaves **84 genuine live-host listings**. The "728 vagas" headline is the aggregator's fuzzy keyword count.
  - Collapsing aggregator duplicates (Netvagas, vagas.sc, Confidencial) leaves **~54 distinct hiring entities**: 51 with a post ≤30 days old, 45 ≤14 days.
  - Parsed data: `work/aud5/tj_rows.json`, `tj_sel.json`, `tj_detail.json`. Detail pages: `work/aud5/jd/`.
- **Intermediaries among the ~54**: Talent & Tech, Comunica RH, RHEVO, Lestars, Jobbol, and possibly RH Shopping. That is **5–6 (≈10–12%)**. Everyone else posts directly.
- https://br.trabajo.org/emprego-2251-f17bef3dd189c96531bdba348ef3a6b6 — Tec-Do "TikTok Live Streaming Host": "Sem experiência necessária. Salário: R$4.000 a R$5.500 + comissão + treinamento", Berrini/SP.
- https://br.trabajo.org/emprego-5234-d1bb84d3c05860a6eef8ade0c50c41c5 — Commerce Lab Lives "Seller Tiktok": "Treinamento completo em vendas ao vivo, sem necessidade de experiência prévia"; R$1.800–2.400.
- https://br.trabajo.org/emprego-2251-c4b21be3b45a4aff0bd3b6314cd05ede — Agência Fuzze "Apresentador de Live Shop": in-house ad; experience is a "diferencial".
- https://br.trabajo.org/emprego-2251-b9c84ff867f8481c0c3ddc3d8f72d862 — iGoal Media "Live Streamer": in-house ad, with KPIs (retention, conversion).
- https://br.trabajo.org/emprego-2251-a61dc124da9c6006fea564b50cecdf8e — "Recruta Simples Solucoes Digitais" listing for StarLive's Live Seller.
  - Recruta Simples is a posting tool, not a recruiter (see below).
- https://br.trabajo.org/emprego-5470-8f14846f480670015793ebc4feaf0e3c — Malibu Glasses: daily lives Mon–Sat, 13–17h or 17–21h; experience is a "diferencial".
- https://br.trabajo.org/emprego-5470-f42cb32ba506bfccf5eccd427a2b1698 — Perfumistta: "1.900 Base + Comissão… Entre R$2.000 a R$ 7.000".
- Talent & Tech listing, detail page in `jd/`: "consultoria especializada em recrutamento e seleção… Streamer de Lives no TikTok Shop em um grupo de empresas focado em marcas de cosméticos". A beauty buyer is paying an intermediary here; the fee is unpublished.
- Comunica RH listings, detail pages in `jd/`:
  - "SALARIO: 2.300,00… Seg á Sex = 08h ás 17h45", listed as "Temporário".
  - A second role: "R$ 2.500,00 + comissão de 1,5% a 3%… Contratação: PJ".
- Lestars Management Consultancy LLC, detail pages in `jd/`: "On behalf of our client, a fast-growing iGaming company… Live Streamer Host"; aggregator range R$90–130 k/yr.
- IT Bolsa, in `jd/`: R$4.200–5.000 PJ; "O estúdio transmite 8 horas por dia, com dois apresentadores se revezando".
- BIGBR, in `jd/`: "disponibilidade para fazer lives… entre 3 e 5 horas ou mais por live".
- Oceanix, in `jd/`: "Não é necessário ter experiência"; R$3.000–5.000.
- Speed Agency, in `jd/`: "Dançarina – LIVE TIKTOK", R$3.100, PJ. An entertainment live agency.
- Synco Live, in `jd/`: its own careers page, "Talentos Host + Moderador(a)", with its own studio in SP.
- **Counts across the 84 ad bodies**:
  - ~41 call live experience "desejável/diferencial".
  - 16 mention PJ; 18 mention CLT; 26 mention commission; 14 mention training.
- **Reposting**:
  - Preçolandia: 6 postings, aged 2 h to 2 weeks.
  - Fantasias Carol: 3 over a month.
  - Malibu: 3 within 3 days.
  - Perfumistta: 2 within a week.
  - Dahuer: 2.
  - Legend Parfum: 11 months old on trabajo, and again on InfoJobs (next line).
- https://www.infojobs.com.br/vaga-de-vendedor-live-tiktok-shop-apresentador-vendas-live-tiktok-shop-em-sao-paulo__11597224.aspx — the original ad is expired. The page shows Legend Parfum "Live Streamer", R$2.000–3.000, "Sem experiência".
- https://employability-portal.gupy.io/api/v1/jobs?jobName=… — Gupy public API; queries live, lives, apresentador(a), tiktok, streamer, "live commerce/shop/seller", host.
  - Only 2 live-host roles in 60 days: **Pacco** "Apresentadora de Live Commerce – TikTok Shop" (Barueri, 23 Sep 2026) and **DAFYNE** "Streamer / Apresentador(a) de Live" (Mooca, 27 Jul 2026).
  - Hinode, Snack Content and a confidential firm post affiliate/TikTok Shop analyst roles on Gupy.
  - Larger employers barely hire hosts; the hosts are hired by small ones. Data: `work/aud5/gupy_all.json`.

## Placement-fee reality

- https://empregga.com.br/recrutadores — Empregga (SME recruitment marketplace):
  - "Cada vaga que você fecha são R$758 no seu bolso… Cálculo ilustrativo, baseado no ticket médio de R$1.516 por vaga e no seu split de 50%. A plataforma custa R$490/mês".
  - "4 vagas → R$ 3.032… É onde a maioria das Recrutadoras começa".
  - "3.000+ Empresas".
- https://empregga.com.br/pricing.md (July 2026):
  - "Publicar vaga é gratuito: sem checkout, sem cartão e sem limite… decisão permanente".
  - Managed service: "Pagamento único por vaga… valor é de tabela, definido pela faixa salarial do cargo… 2 finalistas… Opcionais por vaga: garantia de reposição… (+30 ou +60 dias)".
- https://empregga.com.br/quero-contratar — managed R&S: "especialista de RH dedicada, com apoio de IA… entrega os 2 finalistas… garantia de reposição em até 30 dias e pagamento único".
  - It compares itself with "Consultoria tradicional: Percentual do salário anual do contratado".
- https://empregga.com.br/llms.txt — "marketplace brasileiro de recrutamento e seleção para PMEs… portal de vagas gratuito".
- http://atle.com.br/Proposta_R&S_Atle.pdf, cached at `work/w2e/atle.txt`, re-read:
  - "Salários entre R$ 2.000,01 a R$ 4.000,00 55% do valor do salário"; 60% below R$2.000; 50% above R$4.000.
  - "30% na ABERTURA DA VAGA… 70% na FINALIZAÇÃO".
  - Old (~2015). Seller asking price.
- https://www.recrutasimples.com.br/ and https://www.recrutasimples.com.br/faq:
  - "Anuncie sua vaga em +100 sites com um clique"; "15.000+ empresas".
  - "O período de 5 dias grátis… o pagamento acontece no sexto dia". No price is shown on the page.
  - ⇒ It is a self-serve job-posting tool, not a recruiter.
- https://www.catho.com.br/empresas/ — "Infinitas vagas gratuitas… anunciar vagas gratuitamente e de forma ilimitada"; "pré-seleção inteligente".
- https://br.trabajo.org/publish — "Publique vagas gratuitamente".
- https://www.99freelas.com.br/project/hunter-para-recrutamento-juridico-783983 — "Orçamento: Aberto… Propostas: 68 Interessados: 86… Valor Mínimo: R$ 50,00". Freelance recruiter supply is abundant.
- https://www.99freelas.com.br/projects?q=apresentadora%20live — 0 projects.
- https://www.getninjas.com.br/consultoria/recrutamento-e-selecao — SEO text only, no per-placement price. Not used.
- Workana (https://www.workana.com/jobs?query=recrutamento…) returned 403. br.indeed.com/hire returned 403.
- Vendor and SEO blogs were retrieved by search and not used as evidence, because they are generic "3–4× salary" cost claims:
  - https://www.verorh.com.br/blog/consultoria-de-recrutamento-e-selecao-preco-justo-e-eficiente
  - https://hr4.com.br/blog/servicos-de-recrutamento/

## Free front door: platform and agencies

- https://www.tiktok.com/live/creator-networks/pt-BR — TikTok LIVE "Agências":
  - "bônus dos programas de incentivo… suporte operacional dedicado, treinamento oficial".
  - "As Agências podem recrutar criadores usando ferramentas nos Bastidores da LIVE… ver uma lista de possíveis criadores e aproveitar os programas de indicação".
  - This is platform-funded recruitment of live talent.
- https://www.tiktok.com/live/creator-networks/en — the same, in English.
- https://egobrazil.com.br/tiktok-live-impulsiona-uma-nova-geracao-de-artistas-streamers-e-grandes-agencias/ (19 Sep 2026) — Bellucci Assessoria, "recrutamento, desenvolvimento e gerenciamento de streamers, hosts…". Press piece; SECONDARY.
- `work/w2e/d_64f1989064ed2e0295f3c1b5.json`, the partner.tiktokshop.com "Partner service categories" doc saved by W2E, re-read. Brazil rows:
  - "LIVE Stream Management — … host training";
  - "Mass Recruiting — TTS onboarding service for mass sellers, such as shop registration"; this is SELLER onboarding, not host recruiting;
  - "Mass Tutoring — … classes for … hosting EC live".
  - "Host/Operations Recruitment and Training" appears only in the cross-border and UK rows.
- `work/w2e/lv_5635030781101840.html` (https://seller-br.tiktok.com/university/essay?knowledge_id=5635030781101840&lang=pt-BR), re-read: "Não use interações verbais que não sejam em tempo real, como vozes geradas por IA, gravações de áudio ou rádio."
- https://www.ecommercebrasil.com.br/noticias/tiktok-shop-alcanca-50-mil-lojas-e-500-mil-criadores (16 Sep 2025) — TikTok's fashion lead: "50 mil lojas ativas e 500 mil criadores". Press quoting the platform.
- https://economicnewsbrasil.com.br/2026/09/18/live-commerce-no-brasil-escala-diaria/ — "A Shopee… já realiza mais de 10 mil lives por dia; No TikTok Shop… cresceu 20 vezes". Press; SECONDARY.
- https://livetiktokshop.scoremedia.com.br/ — Score Media, "Agência Oficial TikTok"; page is JS-only. Live commerce management; no price.
- https://www.agenciatokz.com/ — Tokz, per W2E's log: "Live Sellers (apresentadores) Internos", bespoke "planos personalizados".

## Law (planalto.gov.br unless noted)

- https://www.planalto.gov.br/ccivil_03/leis/l6533.htm
  - art. 2 I: an artist "interpreta ou executa obra de caráter cultural… através de meios de comunicação de massa".
  - art. 3: applies to those employing artists for "mensagens publicitárias"; par. único covers those "que agenciem colocação de mão-de-obra".
  - art. 4: "deverão ser previamente inscritas no Ministério do Trabalho".
  - arts. 6–8: the artist's DRT registration.
- https://www.planalto.gov.br/ccivil_03/decreto/1970-1979/d82385.htm — **art. 5 par. único: "Somente as empresas organizadas e registradas no Ministério do Trabalho, nos termos da Lei nº 6.019… poderão agenciar colocação de mão-de-obra de Artista"**.
- https://satedma.wordpress.com/decreto-lei-n%C2%BA-82-385/ — the Decreto 82.385 quadro anexo, full text (D.O.U. 06-10-78).
  - No "apresentador" function is listed.
  - "Manequim — Representa e desfila usando seu corpo para exibir roupas e adereços".
- https://www.planalto.gov.br/ccivil_03/leis/l6019.htm — art. 6 III (Lei 13.429/2017): an empresa de trabalho temporário needs "capital social de, no mínimo, R$ 100.000,00".
- https://www.andersenballao.com.br/pt/artigos/adpf-293-nao-extingue-regulamentacao-legal-de-profissoes-artisticas/ (08 Jan 2020):
  - ADPF 293 (PGR) challenges the Lei 6.533 / Decreto 82.385 registration requirements.
  - It was withdrawn from the STF agenda. Current status UNVERIFIED.
- https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm
  - §5-I (Anexo V) XI: "agenciamento, exceto de mão de obra".
  - art. 17 XII bars "cessão ou locação de mão-de-obra".
  - ⇒ Recruitment of labour is carved out of Anexo V, so the residual Anexo III is likely. UNVERIFIED with an accountant.
- https://www.conjur.com.br/2024-nov-27/justica-do-trabalho-julgara-acao-contra-cobranca-de-taxa-por-agencia-de-emprego/ — returned 60 bytes (blocked). Search summary only: the MPT treats fees charged to candidates as unlawful. SECONDARY/UNVERIFIED.
- ILO NORMLEX Brazil page (C96/C181 status) returned a stub. UNVERIFIED.

## Synergy check against O LANÇAMENTO (ANVISA daily file, `work/TA_CONSULTA_COSMETICOS.CSV`, dated 24/09/2026)

- Notification date is taken as DT_VENCIMENTO − 10 years; "last 12 months" means notified on or after 25 Sep 2025.
- VIZZELA: 213 rows, **51 notified in the last 12 months**; holder DDP Indústria e Comércio (08267165000136).
- PERFUMISTTA: 33 rows, **23 in the last 12 months**; holder Antunes Cosméticos (17228147000136).
- FLEURITY: 12 rows, 0 recent.
- "MALIBU" (135 rows) is **Malibu Premium haircare** (Século Indústria), not Malibu Glasses.
- PACCO: 9 rows, unrelated products.
- LEGEND PARF, HYDRAFIT, DAFYNE: 0.
- ⇒ ~2 of ~54 host-hiring employers are active launchers (~4%).
- Cross-read: `out/AUD3.json` (launch-kit audit) for the ~300-launcher pool and its 20-call test.

## Not reachable / not used
- Workana 403; br.indeed.com 403; Conjur blocked; ILO NORMLEX stub.
- Etsy and Faire not attempted, per the brief.
- No observed price for recruiting a live host was found anywhere.
