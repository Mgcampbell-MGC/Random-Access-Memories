// Caixa Cheia v2 — canonical business plan (docx generator)
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  TableOfContents, PageNumber, Footer, LevelFormat, PageBreak,
} = require('docx');

// palette
const GREEN = '0B4A36', GREEN2 = '0A6E4C', INK = '141414', GREY = '5B6B66',
      RULE = '1D6B4F', LINE = 'C9D6D0', AMBER = '8A4B0B', RED = '8A1C1C';

// ---------- helpers ----------
const T = (t, o = {}) => new TextRun({ text: t, color: INK, ...o });
const B = (t, o = {}) => new TextRun({ text: t, bold: true, color: INK, ...o });
const I = (t, o = {}) => new TextRun({ text: t, italics: true, color: GREY, ...o });

const P = (children, o = {}) => new Paragraph({
  children: Array.isArray(children) ? children : [children],
  spacing: { after: 160, line: 360 }, ...o,
});
const spacer = () => new Paragraph({ children: [], spacing: { after: 60 } });

const bullet = (children, level = 0) => new Paragraph({
  children: Array.isArray(children) ? children : [children],
  numbering: { reference: 'bul', level },
  spacing: { after: 100, line: 340 },
});

const H1 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text: t, color: GREEN, bold: true })],
  spacing: { before: 360, after: 200 },
});
const H2 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text: t, color: GREEN2, bold: true })],
  spacing: { before: 280, after: 160 },
});
const H3 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text: t, color: INK, bold: true })],
  spacing: { before: 220, after: 120 },
});

const hr = () => new Paragraph({
  children: [],
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE } },
  spacing: { after: 200 },
});

const callout = (children, fill = 'EEF5F1', edge = RULE) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  borders: {
    top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
    left: { style: BorderStyle.SINGLE, size: 24, color: edge },
    right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: 9360, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill },
      margins: { top: 140, bottom: 140, left: 220, right: 220 },
      children,
    })],
  })],
});

function tbl(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  if (total !== 9360) throw new Error(`widths sum ${total} != 9360`);
  const mk = (cells, isHead) => new TableRow({
    tableHeader: isHead,
    children: cells.map((c, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: isHead ? GREEN : (undefined) },
      margins: { top: 90, bottom: 90, left: 140, right: 140 },
      children: [new Paragraph({
        children: (Array.isArray(c) ? c : [isHead
          ? new TextRun({ text: String(c), bold: true, color: 'FFFFFF', size: 22 })
          : new TextRun({ text: String(c), color: INK, size: 22 })]),
        spacing: { after: 0, line: 300 },
      })],
    })),
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: widths,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 8, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 8, color: RULE },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      insideVertical: { style: BorderStyle.SINGLE, size: 4, color: LINE },
    },
    rows: [mk(headers, true), ...rows.map(r => mk(r, false))],
  });
}

const partBanner = (kicker, title) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  borders: {
    top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
    left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: 9360, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: GREEN },
      margins: { top: 260, bottom: 260, left: 300, right: 300 },
      children: [
        new Paragraph({
          children: [new TextRun({ text: kicker, color: 'BFE3D3', size: 22, bold: true, allCaps: true })],
          spacing: { after: 80 },
        }),
        new Paragraph({
          children: [new TextRun({ text: title, color: 'FFFFFF', size: 40, bold: true })],
          spacing: { after: 0 },
        }),
      ],
    })],
  })],
});

const PT = (t) => I(`"${t}"`, { color: GREEN2 });

// ---------- content ----------
const body = [];

// Cover
body.push(
  new Paragraph({ children: [], spacing: { after: 2200 } }),
  new Paragraph({
    children: [new TextRun({ text: 'CAIXA CHEIA', color: GREEN, bold: true, size: 88 })],
    alignment: AlignmentType.CENTER, spacing: { after: 200 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'The recovery engine for Brazil’s premium beauty businesses', color: GREY, size: 30 })],
    alignment: AlignmentType.CENTER, spacing: { after: 120 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'Canonical Plan · v2 · Launch, Tech, Money, Funnel, Scale', color: GREY, size: 24 })],
    alignment: AlignmentType.CENTER, spacing: { after: 2600 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'A business for one person: she finds the money sleeping inside a salon’s own client list, brings it back with software, and gets paid only from what actually lands. No monthly fee. No custody. No code written by her — ever.', color: INK, size: 24, italics: true })],
    alignment: AlignmentType.CENTER, spacing: { after: 400 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'São Paulo · July 2026', color: GREY, size: 22 })],
    alignment: AlignmentType.CENTER,
  }),
  new Paragraph({ children: [new PageBreak()] }),
);

// TOC
body.push(
  H1('Contents'),
  new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART 0 ----------
body.push(partBanner('Part 0', 'TLDR — the whole business on one page'), spacer());

body.push(
  P([B('What it is. '), T('Premium Brazilian salons sit on three piles of money they never collect: '), B('unpaid balances'), T(' (packages and comandas half-paid, never chased), '), B('dormant clients'), T(' (bought 10 sessions, did 6, drifted off), and '), B('no-shows never rebooked'), T('. The owner can’t chase any of it — she’s doing procedures all day, and chasing her own clients feels awful. Caixa Cheia is the machine that does it for her: it reads her own records, finds the money, runs tactful WhatsApp waves in her name, takes payment by Pix — and keeps ~25% of only what actually lands.')]),
  spacer(),
  tbl(
    ['Rung', 'Product', 'Price', 'What it does'],
    [
      ['0', 'Auditoria de Voz (free gift)', 'R$0 · unsolicited', 'Built from PUBLIC data only: what her clients say in reviews vs. what her brand projects — the gap, with real quotes, ending on the money bridge. Requires nothing from her. Lead magnet + voice calibration + recovery intelligence in one artifact.'],
      ['1', 'Raio-X do Caixa', 'R$490 once', 'Real audit of her real exports: "R$X is sleeping in your client list," name by name. Guarantee: find ≥R$3.000 recoverable or full refund.'],
      ['2', 'The Recovery Mandate', '25% success fee', 'The business. Backlog harvest, then monthly waves. Fee auto-collected via Pix split. No monthly fee, ever.'],
      ['3', 'The Deposit Rail', '2,9% per transaction', 'Sinal (booking-deposit) links that kill no-shows. Transactional, permanent, survives even a cured account.'],
    ],
    [700, 2400, 1800, 4460],
  ),
  spacer(),
  P([B('The money. '), T('A good account yields a one-time backlog fee of ~R$2.500–4.000, then ~R$1.000–2.500/month in steady success fees plus rail revenue. Honest ramp: ~R$35k/month net by month 6, ~R$65k net by month 12 (solo), R$150k+ net by month ~24 with ~140 accounts and two ops hires. Fixed costs under R$1.500/month. Break-even: two paid audits.')]),
  P([B('The three rules that make it trustworthy. '), T('(1) Every number comes from code — the AI never counts. (2) Client names never reach the AI — templates are drafted generically and mail-merged locally. (3) Nothing external fires without a human gate — the owner approves every wave with one tap.')]),
  callout([
    P([B('The spine, in three sentences. ', { color: GREEN }), T('“Eu encontro o dinheiro que já é seu.” · “Você só me paga do que voltar.” · “Seus números vêm do código; suas clientes, tratadas com carinho — sempre.”')]),
  ]),
  spacer(),
  P([B('Delivery chain, verified against the real world (July 2026): '), T('Trinks natively exports a client-debt report and a package-balance report — the audit’s two money buckets are ready-made files, not an integration project. Asaas split is live for Pix, boleto and card via API with subaccounts — the fee routes itself. Full Google-review histories are fetchable through licensed APIs for a few reais per salon. And the floor sending mode — reception sends a generated one-tap list from the salon’s own phone — works for any salon on day one, no platform required.')]),
  P([B('And the lane is verified open: '), T('Brazil is full of DIY reactivation tools (SocialHub, iZap, RobotiZap) and platform checkboxes — all things the owner must operate herself — and has no visible done-for-you, success-fee operator for beauty. In the US, Winback Engine proves the exact model at 20% of net recovered revenue. Demand proven, model proven, position unoccupied. (§2 has the full map and the positioning rules.)')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART I ----------
body.push(partBanner('Part I', 'The decision — what this is and why it wins'), spacer());

body.push(
  H1('§1 · The business in one page'),
  P([T('Every premium salon in Brazil sells forward: packages of sessions, treatment plans, comandas settled “depois”. Every one of them leaks the same three ways — balances that were never fully paid, clients who quietly stopped coming with sessions still owed to them, and no-shows nobody ever called back. The owner knows. She also knows why nothing happens: chasing your own clients for money is socially painful, and reactivating the vanished ones is a job nobody owns. The leak isn’t an information problem. It’s an ')]),
  P([B('awkwardness problem'), T(' — and that is why no software checkbox has ever fixed it. Booking platforms ship reminder features; features don’t do the uncomfortable thing for you. Caixa Cheia does the uncomfortable thing, gracefully, in the salon’s own voice, and charges nothing unless money actually moves.')]),
  P([T('The offer, as the owner hears it: ')]),
  callout([
    P([PT('Eu leio a sua agenda e as suas comandas, te mostro exatamente quanto dinheiro está dormindo na sua carteira de clientes — com nome e valor — e depois eu mesma vou buscar, com mensagens carinhosas no seu nome e link de Pix. Você não paga mensalidade. Eu fico com 25% só do que voltar.')]),
  ]),
  spacer(),

  H1('§2 · Why this wins — the four moats'),
  bullet([B('The awkwardness moat. '), T('Trinks, Avec and Belasis will keep shipping reminder checkboxes; owners will keep not pressing them. Done-for-you beats do-it-yourself in exactly the tasks people avoid. Her product is the avoided task, performed.')]),
  bullet([B('Success-fee accountability. '), T('Everyone else in the owner’s life charges her whether or not it works — the platform, the agency, the consultant. Caixa Cheia is the only line on her books that is pure profit by construction. That sentence closes deals and kills churn.')]),
  bullet([B('The recovery dataset. '), T('From wave one she measures what nobody in Brazil knows: which message, at which hour, to which segment, brings which % of money back — by service, by ticket, by city. Every account makes the next one better. Copyable method, uncopyable memory.')]),
  bullet([B('The rail. '), T('Once the salon’s booking deposits run through her Pix links, she is no longer a campaign — she is infrastructure. Even an account whose backlog is fully cured keeps paying the rail. This is the lock-in that survives her own success.')]),
  spacer(),
  H3('The field, honestly — verified July 2026'),
  P([T('Reactivation is not empty space — it is '), B('crowded with tools and empty of outcomes'), T('. DIY WhatsApp win-back tools (SocialHub, iZap, RobotiZap and a dozen more) sell segmentation and disparos as monthly SaaS the owner must operate herself. The platforms are commoditizing the feature — Trinks’ own blog teaches reactivation campaigns and ships birthday automations. Deposit and recurring-billing tools exist (Frizzar sells cobrança de sinal; Vindi and InfinitePay do recurrence). And in the US, '), B('Winback Engine proves the exact model'), T(' — done-for-you win-back at 20% of net recovered revenue, no monthly fee, aimed at multi-location service businesses — with no visible equivalent in Brazilian beauty.')]),
  P([T('Read that as a market saying yes: demand proven, money proven, model proven elsewhere — '), B('position unoccupied'), T('. Every Brazilian competitor sells a tool; the owner already had tools and didn’t use them, because the job was never information — it was the awkward work. Done-for-you plus success-fee is the entire difference. And the collections bucket is the least contested of all: nobody wants to chase salon debts for a living. She does — politely, in code.')]),
  H3('Positioning rules — never break these'),
  bullet([B('Never sell “software” or “automação”. '), T('She would be compared to R$99/month tools and lose. She sells: '), PT('eu faço, e você só paga do que voltar.')]),
  bullet([B('Never charge a mensalidade. '), T('The moment a monthly fee exists, she competes with every SaaS above on their terms.')]),
  bullet([B('Always lead with the voice audit. '), T('Nobody else in the market opens with “o que suas clientes estão dizendo”. It is the one unclaimed front door.')]),
  bullet([B('The moats are time-based — say so. '), T('The method is copyable in two months; the recovery-rate dataset, the distributor relationships, and a good name in a ~400-salon market are not. Speed is the strategy; month one being slow costs the only thing that can’t be bought back.')]),
  bullet([B('Who could kill it, watched openly: '), T('Trinks shipping done-for-you collections (unlikely — tool DNA, success-fee liability, and their analytics can never conclude “your platform setup is losing you money”); or a fast copycat cloning Winback Engine for salons (possible — which is exactly why she launches now and hoards the dataset).')]),
  H3('The pilot promise (ported from the US playbook)'),
  P([T('Winback Engine de-risks with “5× your fees in 30 days or your money back.” Her version, KISS: the R$490 audit already guarantees '), B('≥R$3.000 found — six times the price — or refunded'), T('. When the owner signs the mandate on the delivery call, '), B('the R$490 is credited against the first success fee'), T('. And if the first backlog wave recovers nothing, the audit is refunded too. Nobody can lose money trying her — and she can afford that promise because the finder is deterministic.')]),
  spacer(),

  H1('§3 · Why her, specifically'),
  P([T('The industry is run by women end to end — owner, manager, reception. A 26-year-old woman who speaks this world natively starts with the credibility a consultant in a suit has to earn. She never writes code: she commissions the entire machine from Claude Code in plain Portuguese and operates it from a dashboard. Her actual job is the human layer — selling, the audit-delivery call, taste in message tone — and every bit of it is learnable in weeks. The company is a laptop, a CNPJ, and a machine that works while she sleeps.')]),
  spacer(),

  H1('§4 · The ICP — and who she refuses'),
  tbl(
    ['Condition', 'Threshold', 'Why'],
    [
      ['Segment', 'Premium NON-medical beauty', 'Hair (mechas, mega hair, noivas), day spas, lash/brow studios. Packages and R$200+ tickets.'],
      ['Size', 'ME/EPP · 6+ professionals', 'MEI solo operators have no volume and no records.'],
      ['Records', 'Digital agenda + comandas', 'Trinks, Belasis, Avec, Salão99 or disciplined spreadsheets. No digital records → no audit → decline.'],
      ['Sells forward', 'Packages / plans / comandas', 'The leak lives in deferred value. Pure walk-in cash businesses leak less.'],
      ['Pain', 'Owner cannot state her leak', 'If she already runs collections + win-back with numbers, she does not need this.'],
    ],
    [1900, 2400, 5060],
  ),
  spacer(),
  P([B('Excluded from day one, permanently in year 1: '), T('medical aesthetics, harmonização, dentistry, dermatology, physio, nutrition — anything whose records touch health data (LGPD Art. 11, sensitive). Their money is real; their legal universe is different. Year 2, with a lawyer — or never. Also excluded: franchises needing head-office approval, businesses competing on price, and any owner who wants the machine to pressure her clients. The tone is the brand.')]),
  spacer(),

  H1('§5 · The ladder — pricing logic'),
  P([B('Rung 0 is free, unsolicited, and never for sale'), T(' — a gift built from public data that costs her prospects nothing and demonstrates the craft. '), B('Rung 1 costs R$490'), T(' because a decision an owner can make alone at her desk must stay under R$500 — and because a paid audit is acquisition that pays for itself. The guarantee (≥R$3.000 found or refunded) is safe: the finder is deterministic, and any qualifying salon’s records contain that much. '), B('Rung 2 is 25% flat'), T(' — one number, no tiers, no monthly. Simple enough to say in one breath, rich enough to build a company on. '), B('Rung 3 is 2,9% per deposit'), T(' — priced like a payment feature, adopted because it solves no-shows, kept because it’s invisible.')]),
  P([B('First three clients: '), T('15% success fee instead of 25%, in exchange for a written testimonial, anonymized before/after numbers, and one reference call. Capped at three, expiry in the contract. She is not selling cheap — she is buying the proof that closes the next thirty.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART II ----------
body.push(partBanner('Part II', 'The funnel — from stranger to infrastructure'), spacer());

body.push(
  H1('§6 · The funnel map'),
  tbl(
    ['Stage', 'Asset', 'Conversion target'],
    [
      ['Attention', 'Her content + distributors + direct outreach + fair', '—'],
      ['Capture', 'Free Auditoria de Voz (gift, from public data) → delivery chat qualifies', '30–50 leads/month by month 3'],
      ['Qualify + cash', 'Raio-X do Caixa (R$490)', '15–25% of leads buy'],
      ['Convert', 'Recovery mandate (25%)', '50–60% of audits sign'],
      ['Deepen', 'Deposit rail (2,9%)', '60%+ of mandates adopt in 90 days'],
      ['Multiply', 'Owner-to-owner referral + distributor loop', '≥1 referred lead per active account per quarter'],
    ],
    [1800, 4600, 2960],
  ),
  spacer(),

  H1('§7 · Rung 0 — the Auditoria de Voz (the gift that opens every door)'),
  P([T('Built entirely from '), B('public data'), T(' — the salon’s Google reviews (fetched in full via a licensed reviews API; the official API caps at 5, third-party APIs fetch all for a few reais per business), Instagram posts and comments, the WhatsApp greeting, the site. Because it needs '), B('nothing from the owner'), T(', it can be made unsolicited, as a gift — the perfect cold open, with zero LGPD friction. Five sections, Casulo-grade:')]),
  bullet([B('Como você se apresenta '), T('— the brand voice her channels project (warm? premium? playful?), with her own phrases quoted.')]),
  bullet([B('Como suas clientes te veem '), T('— the customer voice from reviews: what they love (by name — “a Carol é maravilhosa”), what they complain about, the normalized rating math (deterministic, code-computed).')]),
  bullet([B('O gap '), T('— where promise and experience diverge: '), I('“você vende acolhimento; 40% das queixas são resposta lenta.”')]),
  bullet([B('A prioridade '), T('— the one thing to fix first. One, not thirty.')]),
  bullet([B('A ponte '), T('— the gap named in money: '), PT('clientes que amam o método mas não conseguem usar o pacote, e somem. Isso é dinheiro dormindo. Quer o número real, com nome e valor? Raio-X do Caixa — R$490, com garantia.')]),
  P([T('Salons with too few public reviews (under ~40) still get a door: the brand-voice half plus the self-serve audio variant — eight questions answered by WhatsApp voice note, a deterministic calculator, the same PDF. The funnel never closes for lack of data.')]),
  P([B('Triple duty: '), T('(1) the lead magnet — magnetic, giftable, demonstrates the exact craft the business runs on; (2) '), B('voice calibration'), T(' — the brand-voice half becomes the tone profile the wave engine writes with, so recovery messages provably sound like her; (3) '), B('recovery intelligence'), T(' — the customer-voice half tells the engine WHY clients drift (favorite professional left, can’t book, price jump), so win-back messages address the real reason, never a generic “sentimos sua falta”.')]),
  P([B('The funnel is one truth at three resolutions: '), T('feeling ('), I('suas clientes dizem que não conseguem agendar o pacote'), T(') → number ('), I('são R$18.400 em pacotes parados'), T(') → money ('), I('recuperei R$11.200 esse mês'), T('). Each rung zooms in; the subject never changes. Delivery chat follow-up doubles as qualification: '), PT('qual sistema você usa — Trinks, Belasis, Avec?'), T(' answers the data question before the R$490 is ever offered. The audit stays free and internal forever — it is a door and an engine input, never a paid product; charging for it would drift into crowded salon-marketing consulting, exactly the red ocean this business avoids.')]),
  spacer(),

  H1('§8 · The four channels that feed it'),
  H3('1 · Her content engine (the compounding one)'),
  P([T('Three pillars, all pointing at the free audit link: '), B('found-money stories'), T(' (“salão de 8 cadeiras, R$23 mil dormindo — olha de onde saiu” — anonymized, real), '), B('teach-the-leak'), T(' (“por que você nunca cobra a cliente que ama”), and '), B('behind-the-machine'), T(' (“eu mando 40 mensagens carinhosas por dia e nenhuma sou eu digitando”). Reels/TikTok native, her face, her voice. One post a day, batched Sundays. The audience is small but perfectly dense: owners follow owners.')]),
  H3('2 · Distributors (the borrowed trust)'),
  P([T('A beauty-products rep walks into 30–40 salons a month and knows exactly which owners complain about money. The pitch: '), PT('eu não vendo nada que compete com você. Manda a dona fazer minha auditoria grátis de 3 minutos; se ela virar cliente, você leva 15% da minha taxa por 6 meses.'), T(' Ten distributor relationships outperform a thousand cold messages.')]),
  H3('3 · Direct outreach (the CNPJ method)'),
  P([T('Receita Federal’s open CNPJ registry, filtered: CNAE 9602-5, porte ME/EPP, active, city. Enrich with Google Maps (150+ reviews, premium services, multi-chair). Score; contact 7+ only. Message one goes to the salon’s number asking for the owner; message two offers the free audit — never a pitch: '), PT('te mando o link da auditoria grátis de 3 minutos; se não aparecer pelo menos R$5 mil dormindo, você me esquece.')]),
  H3('4 · Beauty Fair — 5–8 September 2026, Expo Center Norte, SP'),
  P([T('Day ~40 of the launch. No booth — a tablet, the sample audit, and a QR code to the voice audit. Goal: 10 distributor relationships, 50 owners through the free audit on the spot, 5 paid audits closed at the stand. The fair is the forcing function that makes the first 40 days honest.')]),
  spacer(),

  H1('§9 · The conversion plays'),
  P([B('The audit-delivery call is the whole sale. '), T('Twenty minutes, screen shared. She reads three real rows aloud — name, service, amount — and then stops talking. The owner is looking at her own clients and her own money. The close is one sentence: '), PT('quer que eu vá buscar? Você aprova cada leva com um toque, as mensagens saem no seu nome, e eu só ganho se voltar.')]),
  P([B('Objections, answered once, reused forever:')]),
  bullet([PT('Minhas clientes vão se incomodar.'), T(' — “Olha o tom.” She shows three real messages: warm, principal-only, easy opt-out. “E você aprova a lista antes de sair qualquer coisa. Quem você não quiser que eu toque, nunca recebe nada.”')]),
  bullet([PT('Posso fazer isso eu mesma.'), T(' — “Pode. Podia ter feito nos últimos dois anos também. R$18 mil continuam lá. Eu faço em 30 dias e você só paga do que voltar.”')]),
  bullet([PT('E a LGPD?'), T(' — “Contrato de operadora, anexo de proteção de dados, mensagens só no seu nome e no seu número, e nomes das suas clientes nunca entram em inteligência artificial. Quer ver o anexo?” The objection becomes the demonstration.')]),
  P([B('Retention is a ritual, not a feature. '), T('On the first business day of each month every account gets the '), B('Extrato de Recuperação'), T(': recovered this month · fee · net to you · running total since day one. A single number that only ever goes up. Owners photograph it and send it to their group chats — which is channel five, free.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART III ----------
body.push(partBanner('Part III', 'The tech — one machine, six modules, three rules'), spacer());

body.push(
  H1('§10 · Architecture'),
  P([T('One Python/FastAPI service, one Postgres, WhatsApp Cloud API, one PSP with Pix split, one PDF engine. Server-rendered dashboard. Built entirely by Claude Code from her plain-language specs; operated from two screens (hers and the owner’s approval view). Three rules bind every module:')]),
  callout([
    P([B('Rule 1 — numbers from code only. '), T('The AI drafts words and classifies situations. It never counts, sums, or computes a currency amount that reaches a client.')]),
    P([B('Rule 2 — names never reach the AI. '), T('Message templates are drafted against pseudonyms; a deterministic mail-merge inserts real names and Pix links locally, after the AI is done.')]),
    P([B('Rule 3 — a human gate before anything external. '), T('The owner approves every wave (one tap). She reviews every new account’s first wave and every dispute. Automation does labour, never accountability.')]),
  ]),
  spacer(),
  P([B('The stack is frozen — on purpose. '), T('One repo, one FastAPI service, one Postgres, one server, daily backup. WhatsApp + Asaas + a PDF engine, and nothing else without deleting something first. No microservices, no queues, no second database. Every module is a folder; every behavior is a written spec that Claude Code maintains (the SKILL.md pattern) — she changes the business by editing sentences, not code. Boring technology is a feature: the company must survive her taking a week off, and it will, because the machine’s whole shape fits in one person’s head.')]),
  spacer(),
  tbl(
    ['Module', 'Job', 'Runs'],
    [
      ['CAPTA', 'Auditoria de Voz factory: reviews ingestion (licensed API), brand-channel reader, deterministic rating math, gap analysis, branded PDF, voice-profile + drift-reasons extraction, lead scoring', 'Batch, ~R$5–15/audit'],
      ['RAIO-X', 'Intake exports (Trinks/Belasis/Avec/Salão99/CSV) → normalize → pseudonymize → reconcile agenda × comandas × packages → the three buckets → audit PDF', 'On demand, ~1h/audit of machine time'],
      ['ONDAS', 'Segments, message waves, pacing, opt-outs, never-list, owner approval, business-hours sending', 'Autonomous after owner tap'],
      ['PIX', 'Charges from the salon’s own PSP account; split routes her 25% (or 2,9% rail) at settlement; deposit links; refund/MED handling', 'Autonomous'],
      ['LIVRO', 'Attribution ledger: contact → reply → booking → payment → split, hash-chained; monthly reconciliation vs agenda export; bypass invoice with evidence; the Extrato', 'Autonomous, monthly close'],
      ['PAINEL', 'Her dashboard (pipeline, waves, recoveries, fees, alerts) + the owner’s one-tap approval and Extrato view', 'Always on'],
    ],
    [1300, 6000, 2060],
  ),
  spacer(),

  H1('§11 · The finder (RAIO-X) — how the money is computed'),
  bullet([B('Unpaid balances: '), T('for every package/comanda: sold value − payments received = saldo. Filter: > R$50, < 5 years old (prescription), client not deceased/blocked/disputed. Every row carries its source record ID.')]),
  bullet([B('Dormant value: '), T('clients with sessions remaining on a paid package, or a visit cadence that stopped (median interval × 2.5 = dormant). Value = sessions owed × session value, or historical monthly spend × conservative win-back coefficient. Labelled honestly: '), I('this is the playing field, not guaranteed money.')]),
  bullet([B('No-shows: '), T('appointments marked no-show/cancelled with no rebooking within 14 days. Value = service price. The smallest bucket and the fastest to recover.')]),
  P([T('Identity resolution: phone numbers normalized (strip +55, the 9th-digit inconsistency) then salted-hash pseudonymized — same salt across agenda and comandas so the join survives while names stay local. Ambiguous matches are marked '), I('indeterminado'), T(' and excluded from every total. Conservative always: ranges use the floor; the audit under-promises by design, so the recovery over-delivers.')]),
  spacer(),

  H1('§12 · The wave engine (ONDAS) — how money comes back'),
  tbl(
    ['Segment', 'Cadence', 'Template category'],
    [
      ['Saldo em aberto (owed money)', 'Wave 1 gentle note + Pix · Wave 2 (+7d) offer to split in 2–3 · Wave 3 (+14d) last friendly touch, then stop forever', 'Utility (existing transaction) — confirm current Meta rules'],
      ['Pacote dormindo (sessions owed)', '“Você ainda tem 4 sessões — vamos agendar?” + booking link with deposit', 'Marketing — paced'],
      ['Sumida 60–180d (lapsed regular)', 'Warm miss-you + light incentive chosen by owner + booking link', 'Marketing — paced'],
      ['Furo sem remarcação (no-show)', 'Within 48h: “vamos remarcar?” + deposit link', 'Utility/Marketing per rules'],
    ],
    [2400, 4160, 2800],
  ),
  spacer(),
  P([B('Hard safety rails, all enforced in code: '), T('≤20 sends/day per salon number, business hours only, stop-the-wave if reply rate <5%, PARAR opt-out honored instantly and forever, owner’s never-contact list checked before every send, principal only — no interest, no penalties, no shame language (CDC Arts. 42/71 compiled into the template linter), maximum 3 touches per debt per quarter, and every message goes out in the salon’s name from the salon’s number.')]),
  P([B('Two inputs from the Auditoria de Voz make the waves land: '), T('the '), B('voice profile'), T(' (tone, greetings, emoji habits, how she says “oi amor”) is the style config every template is written against — messages provably sound like her; and the '), B('drift reasons'), T(' (favorite professional left, booking friction, price jump) route each dormant client to a message that answers her actual reason for leaving — '), PT('a Duda saiu, mas a Carol assumiu as alunas dela — vem fazer uma aula por conta da casa?'), T(' — never a generic “sentimos sua falta”.')]),
  P([B('Two sending modes. '), B('Mode 1 (entry, any salon): '), T('the engine generates the day’s list — name, message, Pix link — and reception sends from the salon’s own WhatsApp in ten minutes. Zero platform risk, works everywhere. '), B('Mode 2 (scale): '), T('the system sends via the salon’s WhatsApp Business number after the owner’s one-tap wave approval. Same templates, same rails, zero reception labour. Accounts graduate from 1 to 2 when trust and volume justify it.')]),
  spacer(),

  H1('§13 · Money plumbing (PIX + LIVRO)'),
  P([T('The salon opens its own account at the PSP (Asaas-class: native Pix, split, white-label API). Every charge — saldo payment, package top-up, booking deposit — is issued '), B('by the salon’s account, in the salon’s name'), T('. A split rule routes Caixa Cheia’s share at settlement. She never holds a centavo of client money; the regulated PSP does the splitting. Deposits (sinal) are positioned as the salon’s own no-show policy — something premium salons already want — which routes future conversions through the rail naturally.')]),
  P([B('Bypass, handled honestly: '), T('a nudged client who pays cash in-store escapes the split. The mandate defines '), I('receita recuperada'), T(' as: payments through system links, bookings made through system links, and visits by contacted clients within 30 days of contact — reconciled monthly against the same agenda export the audit already uses. Bypassed conversions appear on a monthly reconciliation invoice with the evidence list attached. Expected leakage ~10–15%, priced into the 25%. The LIVRO ledger — append-only, hash-chained, every event from message to split — is why no fee is ever an argument: every real on the Extrato traces to records the owner can open.')]),
  spacer(),

  H1('§14 · The build — four weeks of Claude Code'),
  tbl(
    ['Week', 'She ships (by directing Claude Code)', 'Proof it works'],
    [
      ['1', 'Entity + contracts started · CAPTA: reviews ingestion, gap analysis, voice-audit PDF factory · pipeline sheet', 'Salão Aurora’s voice audit generates end-to-end from planted reviews'],
      ['2', 'RAIO-X: importers for Trinks/Belasis/Avec/CSV · reconciler · audit PDF · Salão Aurora sample (watermarked, fictitious)', 'Aurora’s audit finds the planted R$21.470 exactly'],
      ['3', 'ONDAS: segments, templates, linter, pacing, approval flow · PSP sandbox + split · deposit links', 'Test wave to her own 5 numbers; split lands in sandbox'],
      ['4', 'LIVRO: ledger, reconciliation, Extrato · PAINEL: her view + owner view · scheduled tasks', 'Month-end close runs end-to-end on Aurora unattended'],
    ],
    [800, 5560, 3000],
  ),
  spacer(),
  P([B('The autonomy map, at steady state: '), T('CAPTA, ONDAS, PIX, LIVRO and the Extrato run themselves on schedules. Her human floor, permanently: the sales call, each account’s first-wave review, dispute handling (target <1 per 50 accounts/month), and reading every Extrato before it ships for the first six months. Target: '), B('≤45 minutes of her time per account per month'), T(' — mature accounts, far less.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART IV ----------
body.push(partBanner('Part IV', 'The money — unit economics, ramp, legal spine'), spacer());

body.push(
  H1('§15 · Per-account economics'),
  tbl(
    ['Line', 'Typical premium salon (R$80–150k/month revenue)'],
    [
      ['Backlog harvest (month 1 of mandate)', 'R$10–16k recovered → her fee R$2.500–4.000, once'],
      ['Steady-state recovery (from month 2)', 'R$4–10k/month → her fee R$1.000–2.500/month'],
      ['Deposit rail', 'R$8–15k/month in deposits → R$230–440/month'],
      ['Her costs per account', 'Templates + PSP + AI + infra ≈ R$60–120/month · her time ≤45 min'],
      ['Account contribution', '≈ R$1.300–2.900/month steady + the backlog pop'],
    ],
    [3400, 5960],
  ),
  spacer(),

  H1('§16 · The ramp — honest and dated'),
  tbl(
    ['Month', 'Active mandates', 'Gross (≈)', 'Net (≈)', 'Team'],
    [
      ['M1 · Aug 26', 'build + funnel live', 'R$0', '−R$3k setup', 'her'],
      ['M2 · Sep (fair)', '3 (case studies @15%)', 'R$8k', 'R$5k', 'her'],
      ['M3 · Oct', '10', 'R$25k', 'R$18k', 'her'],
      ['M6', '28', 'R$49k', 'R$35k', 'her'],
      ['M12', '55', 'R$90k', 'R$65k', 'her'],
      ['M18', '95', 'R$160k', 'R$120k', '+1 ops'],
      ['M24', '140', 'R$230k', 'R$155k+', '+2 ops'],
    ],
    [1700, 2560, 1800, 1700, 1600],
  ),
  spacer(),
  P([B('What the table assumes'), T(' — 7–8 new mandates/month from month 3, ~3%/month churn (cured accounts retained by the rail), blended steady fee ~R$1.100–1.300, backlog fee ~R$2.500, rail adoption 60%. The ops hires mirror the blueprint’s Lever 4: the machine lives in a folder, so hire #1 (an ex-receptionist, CLT ~R$5.5k all-in) inherits onboarding + wave review from a written manual, and her pró-labore plus payroll keeps Fator R ≥ 28% → Simples Anexo III (≈6% vs 15,5% — raise it with the accountant in month 1). Fixed costs: contador R$300–400 · AI/work-plan R$300–500 · PSP/infra R$200–400 · domain/misc R$100 — under R$1.500/month. Break-even is two paid audits.')]),
  spacer(),

  H1('§17 · The legal spine (ported whole from the blueprint, adapted)'),
  bullet([B('Entity: '), T('ME or SLU · CNAE 7020-4/00 principal (+ 8291-1/00 cobrança as secondary — decide with the accountant) · Simples Nacional · contador from day 1 — premium salons require nota fiscal; the CNPJ is a precondition for the first sale.')]),
  bullet([B('Contract stack (lawyer-reviewed once, ~R$1.5–3k): '), T('service contract (mandate scope, the 25%, attribution definition, monthly reconciliation, liability cap, labour-law exclusion, '), B('post-termination window'), T(' — fees due on recoveries attributable to contacts made before cancellation, for 30 days after) · DPA (salon = controladora, she = operadora; AI provider named as sub-operator; international-transfer clause per ANPD Res. 19/2024; '), B('retention schedule'), T(' — raw exports deleted at delivery +30 days, pseudonymized working set +90, written deletion confirmation) · LIA template handed to the salon · mutual NDA.')]),
  bullet([B('Collections law, compiled into code: '), T('CDC Art. 42/71 — no embarrassment, no threats, no third parties, principal only, private 1:1 always, instant opt-out, 3-touch cap, 5-year prescription filter. The template linter blocks violations before any human sees them.')]),
  bullet([B('Lei do Salão Parceiro guardrail: '), T('messages and reports never score or direct profissionais-parceiras — reception process and client outcomes only. The eight-second version of this, said in the sales call, closes deals by itself.')]),
  bullet([B('Absolute prohibitions: '), T('never health data · never hold client money · never message without the owner’s standing instruction + wave approval · never mix one client’s data into another’s · never claim anonymization (it is pseudonymization) · never guarantee recovery amounts — guarantee the audit, never the result.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART V ----------
body.push(partBanner('Part V', 'Launch — 90 days, dated'), spacer());

body.push(
  H1('§18 · The calendar'),
  tbl(
    ['Window', 'Do', 'Exit with'],
    [
      ['Weeks 1–2 · Aug 1–14', 'Entity + contador + lawyer on contracts · Claude Code builds CAPTA + RAIO-X · Salão Aurora sample built and watermarked · CNPJ list pulled and scored · 20-min competitor scan (Instagram/Google: “recuperação de clientes salão”) to confirm the lane is still open', 'Working funnel front + the demo artifact'],
      ['Weeks 3–4 · Aug 15–28', 'Funnel live · content starts (1/day) · 20 owner conversations · 5 distributor meetings booked · ONDAS + PSP built', 'First 30 free audits done · first 3 paid Raio-X sold'],
      ['Week 5 · Aug 29–Sep 4', 'Deliver audits · close first 2–3 mandates at 15% · fair prep (tablet, QR, 60-second pitch)', 'First waves approved and sent · first Pix splits land'],
      ['Days 36–39 · Sep 5–8', 'BEAUTY FAIR: 10 distributor relationships · 50 free audits at the stand · 5 paid audits closed on the spot', 'A pipeline that outlives September'],
      ['Weeks 7–10 · Sep 9–Oct 2', '48h follow-up on every fair contact · audits → mandates · first monthly Extratos ship · first reconciliation invoices', '10+ active mandates · measured recovery rates'],
      ['Weeks 11–13 · Oct 3–23', 'Case-study pricing closed forever · full 25% for all new accounts · distributor loop paying · testimonials in every channel', '~15 mandates · ~R$25k month run-rate · the machine proven'],
    ],
    [2100, 5060, 2200],
  ),
  spacer(),
  P([B('Her operating week from month 4: '), T('Mon — pipeline + new-account onboarding. Tue–Thu mornings — sales calls (audit deliveries); afternoons — first-wave reviews and disputes. Fri — Extrato review + content batch. The machine sends, collects, splits, reconciles and reports without her. Twenty-five hours a week runs it; the rest is growth.')]),
  spacer(),

  H1('§19 · Running it KISS — five numbers, three rituals, one rule'),
  P([T('The whole company is managed on '), B('five numbers'), T(', read from one dashboard: leads this week · audits sold · active mandates · R$ recovered this month · fee collected. If a report doesn’t move one of the five, it doesn’t exist. No CRM, no project tool, no marketing stack — WhatsApp, the PAINEL, and one pipeline sheet.')]),
  bullet([B('Monday, 30 minutes — the pipeline: '), T('leads → audits → mandates; pick the week’s ten outreach targets. Done before coffee is cold.')]),
  bullet([B('Every morning, 2 hours — growth block: '), T('prospecting and sales only. Delivery never invades it; afternoons belong to audit-delivery calls and first-wave reviews.')]),
  bullet([B('Friday, 1 hour — the close: '), T('read every Extrato before it ships (first six months), batch next week’s content, log the five numbers. That log IS the board meeting.')]),
  P([B('The rule of one: '), T('one ICP, one city, one fee (25%), one channel priority per quarter, at most one new capability per month — and any new complexity must delete an old one. The moment operating the business needs a manual she hasn’t written, it has drifted; stop and simplify.')]),
  P([B('Tripwires, with responses pre-written: '), T('disputes >1 per 50 accounts/month → freeze new onboarding, fix templates first. Wave replies <5% two weeks running → pause that segment, rewrite with drift-reasons. First-wave review errors rising → push a delivery date, never the review. Churn >5%/month → stop selling, interview the last five losses. Overload reveals itself in these numbers before any client feels it — that is what the numbers are for.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART VI ----------
body.push(partBanner('Part VI', 'Scale — the levers and the endgame'), spacer());

body.push(
  H1('§20 · The levers, in order'),
  bullet([B('Lever 1 — Mode 2 everywhere. '), T('Graduating accounts from reception-sends to system-sends drops her marginal minutes toward zero and makes 100+ accounts a dashboard, not a job.')]),
  bullet([B('Lever 2 — the rail as default. '), T('Every mandate adopts deposit links in onboarding (“your new no-show policy”). Rail revenue is churn-proof and grows with the client’s success, not their leak.')]),
  bullet([B('Lever 3 — ops hire #1 at ~55 accounts '), T('(ex-receptionist, manual in a folder, CLT). Her hours shift to sales; the Fator R math makes the hire partially tax-self-funding.')]),
  bullet([B('Lever 4 — metro 2 via distributors. '), T('National distributors already cover Rio/BH; a rep who watched her make his SP salons money is a warm-introduction machine. Begin mapping month ~15.')]),
  bullet([B('Lever 5 — adjacent verticals, same machine. '), T('Barbershops premium, nail studios with packages, pet grooming, tattoo studios — anywhere value is sold forward and clients drift. Health-adjacent only in year 2+, with counsel, or never.')]),
  spacer(),

  H1('§21 · The endgame asset'),
  P([T('By month 24 she owns the only dataset of its kind in Brazil: measured recovery rates — message × segment × timing × ticket — across a hundred-plus salons, plus a deposit rail humming underneath the sector’s no-show problem. That unlocks year-3 options from a position of strength: the published '), B('Índice Caixa Cheia'), T(' (the sector’s benchmark for money left on the table), speaking slots at the fair she once walked with a tablet, licensing conversations with the booking platforms — who by then will want the one capability they structurally cannot build: the willingness to be accountable for results.')]),
  spacer(),
  callout([
    P([B('The three sentences, again — because they are the company. ', { color: GREEN })]),
    P([T('“Eu encontro o dinheiro que já é seu.”')]),
    P([T('“Você só me paga do que voltar.”')]),
    P([T('“Seus números vêm do código; suas clientes, tratadas com carinho — sempre.”')]),
  ]),
);

// ---------- document ----------
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 26, color: INK }, paragraph: { spacing: { line: 360 } } },
      heading1: { run: { font: 'Calibri', size: 40, bold: true, color: GREEN } },
      heading2: { run: { font: 'Calibri', size: 30, bold: true, color: GREEN2 } },
      heading3: { run: { font: 'Calibri', size: 27, bold: true, color: INK } },
    },
  },
  numbering: {
    config: [{
      reference: 'bul',
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 460, hanging: 260 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 920, hanging: 260 } } } },
      ],
    }],
  },
  features: { updateFields: true },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
      titlePage: true,
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: 'Caixa Cheia · Canonical Plan v2 · ', color: GREY, size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 18 }),
          ],
        })],
      }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  require('fs').writeFileSync('/home/user/Random-Access-Memories/CAIXA_CHEIA_V2.docx', buf);
  console.log('written', buf.length, 'bytes');
});
