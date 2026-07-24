// Caixa Cheia v4 — canonical business plan (reactivation kernel) — docx generator
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  TableOfContents, PageNumber, Footer, LevelFormat, PageBreak,
} = require('docx');

const GREEN = '0B4A36', GREEN2 = '0A6E4C', INK = '141414', GREY = '5B6B66',
      RULE = '1D6B4F', LINE = 'C9D6D0', AMBER = '8A4B0B', RED = '8A1C1C';

const T = (t, o = {}) => new TextRun({ text: t, color: INK, ...o });
const B = (t, o = {}) => new TextRun({ text: t, bold: true, color: INK, ...o });
const I = (t, o = {}) => new TextRun({ text: t, italics: true, color: GREY, ...o });
const PT = (t) => I(`"${t}"`, { color: GREEN2 });

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
const H3 = (t) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text: t, color: INK, bold: true })],
  spacing: { before: 220, after: 120 },
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
      shading: isHead ? { type: ShadingType.CLEAR, fill: GREEN } : undefined,
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

const body = [];

// ---------- Cover ----------
body.push(
  new Paragraph({ children: [], spacing: { after: 2200 } }),
  new Paragraph({
    children: [new TextRun({ text: 'CAIXA CHEIA', color: GREEN, bold: true, size: 88 })],
    alignment: AlignmentType.CENTER, spacing: { after: 200 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'Prepaid win-back campaigns for Brazil’s premium beauty businesses', color: GREY, size: 30 })],
    alignment: AlignmentType.CENTER, spacing: { after: 120 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'Canonical Plan · v4 · The Reactivation Kernel', color: GREY, size: 24 })],
    alignment: AlignmentType.CENTER, spacing: { after: 2600 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'One product, one agreement, one fee, one importer, one sending mode, one PSP. She brings a salon’s lapsed clients back with a paid offer sent from the salon’s own WhatsApp — and earns 20% of only the money that actually settles through the campaign’s own checkout. Refunds reverse the fee. Nothing else.', color: INK, size: 24, italics: true })],
    alignment: AlignmentType.CENTER, spacing: { after: 400 },
  }),
  new Paragraph({
    children: [new TextRun({ text: 'São Paulo · July 2026', color: GREY, size: 22 })],
    alignment: AlignmentType.CENTER,
  }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- TOC ----------
body.push(
  H1('Contents'),
  new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART 0 ----------
body.push(partBanner('Part 0', 'TLDR — the whole business on one page'), spacer());

body.push(
  P([B('What it is. '), T('Premium beauty businesses lose clients to drift — she loved the place, hit friction, and quietly stopped coming. The owner has no time to chase her back. Caixa Cheia is a done-for-you campaign engine: it reads the salon’s own Trinks export, finds the genuinely lapsed clients with documented WhatsApp opt-in, sends them a warm '), B('prepaid offer'), T(' from the salon’s own number, and takes '), B('20% of only the money that settles through the campaign’s own checkout'), T('. If a payment is refunded, the fee reverses with it. No monthly fee, no custody, no invoices to chase.')]),
  spacer(),
  tbl(
    ['Element', 'Launch decision'],
    [
      ['Product', 'Prepaid win-back campaigns for genuinely lapsed clients (90–365 days)'],
      ['Customer', 'Non-medical premium beauty businesses on Trinks; core ICP: multi-unit groups / high-volume salons with 500+ eligible lapsed contacts, ticket ≥R$250'],
      ['Free door', 'Eligibility scan: send the Trinks CSV, get back “612 elegíveis · 214 com opt-in comprovado · potencial R$X” in an hour — same importer as the product, zero extra machinery'],
      ['Onboarding', 'Fully self-service for the owner: sign up, upload CSV, clickwrap contract+DPA, guided Asaas connect, Meta embedded-signup for WhatsApp, pick an offer from the gallery, approve — ~15 minutes once, then two taps per campaign. Zero founder minutes on the happy path; built for 100+ new salons/month.'],
      ['Fee', '20% of Asaas netValue actually settled through the campaign checkout · refunds reverse the fee · first 3 clients at 15% for testimonials'],
      ['Attribution', 'Only money paid through the campaign link. A R$100 deposit on a R$500 service earns fee on R$100. No agenda reconciliation, no bypass invoices, ever.'],
      ['Sending', 'One mode: WhatsApp Cloud API with Business-App coexistence, on the salon’s own number. One approved template family per salon, written in her tone, deterministic variables.'],
      ['Consent', 'The opt-in evidence gate: no documented marketing opt-in (value + captured_at + source + scope) = no send. No exceptions.'],
      ['Approval', 'The owner approves the exact final send manifest (recipients, rendered copy, links); manifest + approver + timestamp + hash stored. Nothing changes after approval.'],
      ['Payment', 'Salon-owned Asaas account; automatic split routes the 20% at settlement. She never holds a centavo of anyone else’s money. NFS-e still issued for every fee.'],
      ['Revenue shape', 'A campaign factory — backlog harvest, then quarterly/seasonal re-runs. Not MRR — v4 stops pretending otherwise.'],
    ],
    [1900, 7460],
  ),
  spacer(),
  callout([
    P([B('The spine, in three sentences. ', { color: GREEN }), T('“Eu trago suas clientes de volta — com oferta paga, não com promessa.” · “Você paga 20% só do que entrar pelo link da campanha.” · “Estornou? Nossa taxa volta junto.”')]),
  ]),
  spacer(),
  H3('The business model canvas — one table'),
  tbl(
    ['Block', 'Caixa Cheia v4'],
    [
      ['Customer segments', 'Non-medical premium Brazilian beauty businesses on Trinks. Core: multi-unit groups and high-volume salons with 500+ eligible lapsed contacts, ticket ≥R$250. Ordinary premium salons: welcome self-serve volume. Excluded: medical-adjacent, low-ticket, no digital records.'],
      ['Value proposition', 'Done-for-you prepaid win-back: lapsed clients (90–365d) brought back with a paid offer from the salon’s own WhatsApp. Fee only on money settled through the campaign checkout; refunds reverse it. Owner approves every send.'],
      ['Channels', 'Free eligibility scan as the only door; Beauty Fair live tablet scans; distributors; referral ask in every winning statement; published measured results; 48h scan follow-up.'],
      ['Customer relationships', 'Self-serve onboarding, owner-in-command execution: manifest approval on every send, monthly statements, POS opt-in kit growing each salon’s pool. White-glove only for multi-unit groups. Invisible to end clients.'],
      ['Revenue streams', 'One: 20% of Asaas netValue settled through the campaign checkout, split at settlement; refunds reverse symmetrically. First 3 clients at 15%. No monthly fee, nothing off-rail. A campaign factory — backlog, then quarterly re-runs.'],
      ['Key resources', 'The codebase (one repo, FastAPI, Postgres+outbox) built via Claude Code; encrypted salon Asaas keys; approved template families; opt-in evidence records; manifest archive; cross-salon aggregate results + her trust position — the durable moat.'],
      ['Key activities', 'Eligibility scans; offer gallery curation; template drafting/approval; manifest-gated sending; settlement/refund/quality monitoring; statements + NFS-e; POS opt-in capture; Friday five-number review; provider approvals maintained.'],
      ['Key partners', 'Asaas (salon-owned accounts, split, written classification); Meta/BSP (coexistence, templates); Trinks (data source — a dependency to manage); contador + lawyer; fair distributors; the 3 founding testimonial salons.'],
      ['Cost structure', 'Fixed ~R$1.5–3k/month solo (contador, tools, infra, WhatsApp conversation fees, Asaas per-charge). Scaling cost: campaign ops — her time, then the gated ops hire. Taxes: Anexo III effective ~16% at scale; 10% dividend WHT above R$50k/month.'],
    ],
    [2000, 7360],
  ),
  spacer(),
  P([B('Why v4 is more collectible than everything before it: '), T('100% of fee events are on-rail by definition. There is no invoice a salon can refuse, no attribution to argue, no evidence tribunal to run. The fee splits itself at the PSP the moment the client pays — and when it doesn’t, there is no fee.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART I ----------
body.push(partBanner('Part I', 'What changed and why — the honest ledger'), spacer());

body.push(
  H1('§1 · v2 → v4: two errors and the cut ledger'),
  P([T('v2 was four businesses disguised as one: a review-audit agency, a debt-collection company, a reactivation service, and a payments rail. Independent diligence caught two errors that change the design, and v4 owns both:')]),
  bullet([B('The accounting error (CPC 47). '), T('An unused prepaid package is not money owed TO the salon — the salon was already paid and owes the client '), B('service'), T(' (a contract liability). Charging a “recovery fee” when that client redeems a session would be charging the salon a fee on money it received months ago. Dead on arrival at the first accountant. The bucket dies as a fee event forever; clients with unused prepaid sessions are '), B('excluded from campaigns until their credit is honored'), T(' — only then do they re-enter the eligible pool, and the fee applies only to NEW prepaid money settled through the campaign checkout.')]),
  bullet([B('The consent error (Meta opt-in). '), T('Business-initiated WhatsApp marketing requires evidenced opt-in, and most salons’ historical lists don’t have it. “Reception sends manually” was a workaround that hides the exposure instead of removing it. v4 replaces it with the opt-in evidence gate — and honestly kills cold WhatsApp prospecting from CNPJ lists along with it.')]),
  spacer(),
  H3('Cut from v2 (and why)'),
  tbl(
    ['Cut', 'Reason'],
    [
      ['Auditoria de Voz factory + paid R$490 Raio-X', 'A second business; LGPD gray on public-data reuse; the free eligibility scan is a better door using code that must exist anyway'],
      ['Debt collection at launch', 'Meta policy puts debt collection in restricted territory; a third-party success-fee collector running debt campaigns risks the salon’s number. Phase-2 gate, not a launch feature.'],
      ['Fee on unused-package redemptions', 'CPC 47 — the salon owes the client, not the reverse'],
      ['Monthly bypass reconciliation + off-rail invoices', 'An evidence tribunal that turns her into a collections company against her own customers. On-rail only; leakage is a cost, priced in.'],
      ['Manual sending Mode 1 + graduation logic', 'Doesn’t escape Meta policy, just hides it. One mode: Cloud API + coexistence.'],
      ['Per-client AI prose (“every message uniquely in her voice”)', 'Incompatible with approved templates. The salon’s voice lives at the template-family level — one warm template, owner-approved, deterministic variables.'],
      ['The 2,9% general deposit rail as a product', 'A fourth business. Deposits survive as an OFFER TYPE inside campaigns — same checkout, fee on what settles.'],
      ['Hash-chained ledger, cross-salon row-level dataset, multi-system importers, backup PSP, invented pacing heuristics (“20/day, 5% replies”)', 'Complexity without evidence. Postgres outbox + idempotent webhooks is the right-sized integrity story; aggregate stats only; Trinks-only at launch; Meta publishes no such safety thresholds.'],
    ],
    [4200, 5160],
  ),
  spacer(),
  H3('Staged back in (deliberately, with gates)'),
  P([T('Three cuts return later, behind the evidence gates of §15: first-party payment reminders, active-base campaigns, and a second importer (Belasis/Avec) — each opened by proof, never by calendar.')]),
  spacer(),

  H1('§2 · The field, honestly — and the wedge that remains'),
  P([T('The lane is NOT empty. Retorne.app integrates with Trinks for reactivation; Retornax and Reativa Clientes sell win-back; Avec ships native AI reactivation; DIY WhatsApp CRM tools abound. What remains uncommon is the '), B('wrapper'), T(': done-for-you execution + a fee charged only on money that actually settled + owner-approved manifests. Uncommon pricing is not a moat — so the honest moats are operational: campaign craft measured in her own results data, referrals inside a dense owner community, and the discipline incumbents’ DIY tools can’t force on a busy owner. The core argument survives contact with the competition: '), B('owners already have reactivation buttons and don’t press them'), T('. She is the pressed button.')]),
  spacer(),

  H1('§3 · Why beauty, restated correctly'),
  P([T('v2 claimed “money owed by construction.” v4 claims what diligence left standing: beauty wins '), B('for reactivation'), T(' — visit cadence makes lapse computable from data alone (no survey, no guess); the lapsed client is not an adversary but a fan who hit friction, already replying to the salon’s WhatsApp; tickets (color, blonding, extensions, lashes, spa rituals) are high enough that one returned client pays for a whole campaign; records are exportable today (Trinks ships a “clients who did not return” report natively); and there is no health data in scope. Fitness has dunning incumbents and biometric drag; education has minors and regulated collections; pet has low tickets. '), B('ICP, sharpened by the economics: '), T('recurring premium maintenance businesses with spare capacity — multi-unit groups and high-volume salons with 500+ eligible lapsed contacts and ticket ≥R$250. Ordinary single salons are welcome fair-won volume, not the core. Excluded: anything medical/health-adjacent, bridal-only (no cadence), low-ticket general salons, and any owner without digital records.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART II ----------
body.push(partBanner('Part II', 'The product — door, campaign, money'), spacer());

body.push(
  H1('§4 · The free door — the eligibility scan'),
  P([T('No audits, no PDFs, no theater. The door is the product’s own first step, given free: the owner exports her Trinks client file (two clicks), sends it over, and within the hour gets back one message: ')]),
  callout([
    P([PT('Você tem 612 clientes sumidas há mais de 90 dias; 214 delas têm opt-in comprovado — só essas a gente pode contatar. Ticket médio delas: R$310 · potencial da campanha: ~R$8 mil. Quer rodar a primeira? Você só paga 20% do que efetivamente entrar pelo link.')]),
  ]),
  spacer(),
  P([T('The scan runs the same importer, eligibility engine and opt-in gate the product uses — zero extra machinery, and it doubles as qualification: it reveals the real contactable pool (the opt-in number) before anyone commits to anything; a prospect’s file runs in the same production app as a tenant-to-be, and if she doesn’t sign, her row-level data is deleted after the scan (only the summary counts survive). Small pool → honest advice and a POS opt-in kit, not a campaign. This is also the live demo for the Beauty Fair: scan a prospect’s file on the spot, show her the number.')]),
  spacer(),

  H1('§5 · The campaign — one loop, owner in command'),
  bullet([B('Audience: '), T('lapsed 90–365 days · documented WhatsApp marketing opt-in · no active booking · no open dispute · no outstanding debt · no unused prepaid sessions (those clients get nothing sold to them until their credit is honored — the CPC 47 lesson, applied as ethics).')]),
  bullet([B('Offer: '), T('a concrete prepaid deal the owner picks from a gallery of three proven formats with editable defaults — a discounted return package, a “volta com a gente” bundle, or a booking-with-deposit; offers are designed personally with her only in the white-glove tier (multi-unit groups). All formats settle through the same campaign checkout. The deposit format doubles as the salon’s no-show protection — an offer type, not a separate product.')]),
  bullet([B('Copy: '), T('ONE approved marketing-template family per salon, drafted once in the salon’s tone and approved by the owner, with deterministic variables ({{nome}}, {{oferta}}, {{link}}). No per-client AI prose, no customer row ever sent to an LLM.')]),
  bullet([B('The manifest gate: '), T('before sending, the owner sees the exact final payload — every recipient, the exact rendered copy, every link — and approves. Manifest + approver + timestamp + hash stored. What was sent is never in dispute; what the salon authorized is never in dispute.')]),
  bullet([B('Sending: '), T('the salon’s own number via WhatsApp Cloud API with Business-App coexistence — reception keeps answering in the app she already uses; campaigns go out through the API with approved templates. Sends respect Meta’s published messaging limits and quality signals (monitored per number), not invented thresholds. Opt-outs suppress instantly and forever.')]),
  bullet([B('The client’s experience: '), T('one warm message from the salon she already loves, a real offer, a Pix checkout, ten seconds. Caixa Cheia is invisible to her, always.')]),
  spacer(),

  H1('§6 · The money — split at the source, or no fee at all'),
  P([T('Every salon owns its own Asaas account (its CNPJ, its KYC, its money). At onboarding it issues a dedicated API key into encrypted storage. Campaign charges are created inside the salon’s account; an automatic split routes '), B('20% of netValue'), T(' (after PSP fees) to Caixa Cheia at settlement. Refunds and chargebacks reverse both portions symmetrically. Revenue is recognized only when payment AND split report DONE. Cancellation = the API key is disabled — clean exit, no hostages. She still issues an NFS-e for every fee earned: the split kills payment-chasing, not fiscal obligations.')]),
  P([B('The attribution rule that ends all arguments: '), T('only money settled through the campaign checkout counts. A nudged client who books nothing but shows up and pays cash next week? No fee. The plan accepts that leakage as a cost of simplicity — if telemetry later shows it is material, the response is changing one price number, never building a reconciliation tribunal. Post-termination: fees apply only to campaign charges created before termination that settle afterward.')]),
  P([B('Launch-blocking proofs (before the fair): '), T('(1) one real charge + refund through a salon-owned account with the split, in production, plus Asaas’s written classification of the topology; (2) coexistence onboarding — via Meta’s embedded-signup flow — working on one real salon number, completable by a non-technical owner. Both start day 1 — provider approvals run parallel to the build.')]),
  spacer(),

  H1('§7 · Self-service by design — 100+ salons a month'),
  P([B('The principle: self-service to enter, done-for-you to run. '), T('The thesis of this business is that owners don’t press buttons — so the owner is never asked to OPERATE anything. What is self-service is the entry and the control surface; the work stays with the machine. Her total lifetime effort: ~15 minutes once, then two taps per campaign.')]),
  P([B('The 15-minute onboarding (zero founder minutes on the happy path): '), T('(1) sign up from a link — distributor, content, or fair QR — with CNPJ + WhatsApp; (2) upload the Trinks CSV following a 40-second video → the eligibility scan renders on screen instantly; (3) accept the contract + DPA by clickwrap; (4) connect Asaas through a guided flow (their own account, their API key, video-led); (5) connect WhatsApp via Meta’s embedded-signup for coexistence; (6) pick an offer from the gallery and approve the manifest. The campaign runs.')]),
  P([B('Throughput math: '), T('100 salons/month is 5 per business day. The happy path costs the founder zero minutes; budgeting ~20% exceptions at ~15 minutes each is ~4 hours a week of exception handling at full flow. Support is help videos + an async WhatsApp line — no live onboarding calls on the self-serve tier. Her personal first-campaign review is sampled after account #50, once the template linter has fifty clean campaigns behind it; the owner’s manifest approval — the accountability gate — never goes away.')]),
  P([B('The two-tier motion this creates: '), T('self-serve for ordinary salons — which answers the economics honestly: at R$150–250/month steady they are only worth serving when servicing costs ~zero, and now it does, so the long tail becomes profitable volume and the referral engine; white-glove for multi-unit groups — the core revenue ICP still gets her personally, five conversations a month instead of a hundred.')]),
  P([B('Honest sequencing: '), T('the architecture is self-service-first from day 1, but for the first ~20 accounts she drives the same screens herself (concierge mode) — that is how the flow gets debugged. Public self-serve opens in month 2–3 once telemetry proves the happy path. Same code, zero rework. Two proofs join the launch-blocking list: the embedded-signup path works for a non-technical owner, and the guided Asaas connect survives contact with a real one.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART III ----------
body.push(partBanner('Part III', 'The machine — one transaction engine'), spacer());

body.push(
  H1('§8 · Architecture'),
  P([T('One repo, one FastAPI service, one Postgres, one server. WhatsApp Cloud API + Asaas + a dashboard, and nothing else without deleting something first. Built and maintained entirely by Claude Code from written specs; she operates it from two screens (hers, and the owner’s approval view).')]),
  tbl(
    ['Component', 'Job'],
    [
      ['Importer (Trinks CSV only)', 'Fixed field allow-list: internal ID, phone, visit dates, coarse service category, payment status, consent evidence. Forbidden columns (notes, free text, attachments) are discarded on ingest. Raw files deleted after normalization.'],
      ['Eligibility + opt-in engine', 'Computes lapse (90–365d), applies exclusions (active booking, dispute, debt, unused prepaid sessions), enforces the opt-in evidence gate: value + captured_at + source + scope, or no send.'],
      ['Campaign engine', 'Offer setup, recipient selection, template rendering with deterministic variables, the manifest approval gate, outbox-driven sending with retry + idempotency, opt-out suppression, and the WhatsApp webhook (signature-validated) that records delivery status, number-quality signals and every opt-out reply into a per-tenant suppression list — suppressed forever, checked at manifest build and again at send.'],
      ['Money engine', 'Asaas charge creation in the salon’s account (idempotent — one charge per manifest recipient, keyed by externalReference, so a retried job can never double-charge), split rule, payment/refund/chargeback webhooks (token-validated, idempotent, replay-safe — an unauthenticated or replayed event changes nothing), revenue ledger, salon statement, NFS-e export.'],
      ['Onboarding portal', 'Self-serve: signup, clickwrap contract + DPA, CSV upload → instant scan, guided Asaas connect (encrypted API key), Meta embedded-signup for coexistence, offer gallery. Concierge-driven for the first ~20 accounts, public once the flow is proven.'],
      ['Dashboard', 'Hers: pipeline, campaigns, settled GMV, fee revenue, refund rate, number quality. Owner’s: eligible pool, manifest approval, delivered/paid, her net — always net, always positive.'],
    ],
    [2600, 6760],
  ),
  spacer(),
  H3('The three rules (v4 edition)'),
  callout([
    P([B('1 — Numbers from code only. '), T('Every figure a client sees comes from deterministic computation. The AI drafts template copy and nothing else.')]),
    P([B('2 — No customer row ever reaches an LLM. '), T('Not names, not hashes, not histories. Templates are generic; variables merge locally.')]),
    P([B('3 — Nothing external fires without a stored human approval. '), T('The owner approves the exact manifest; she reviews each account’s first campaign, sampled after account #50. Automation does labour, never accountability.')]),
  ]),
  spacer(),
  H1('§9 · LGPD posture — narrow by construction'),
  bullet([T('Salon = controladora (decides purpose, audience, offer, approves the manifest); Caixa Cheia = operadora under a written DPA; she is controladora only of her own billing and aggregate statistics.')]),
  bullet([T('Data minimization is architectural, not aspirational: the allow-list importer cannot ingest what it cannot see. Tenant isolation, encrypted secrets and backups, MFA, no PII in logs.')]),
  bullet([T('Cross-salon learning only as irreversible aggregates (conversion by offer type/segment) — never row-level pooling.')]),
  bullet([T('Small-agent simplifications (ANPD Res. 2/2022) apply; she names herself as the privacy contact and publishes a salon-branded privacy notice. Deletion controls: raw exports post-normalization; full tenant data on termination, with written confirmation.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART IV ----------
body.push(partBanner('Part IV', 'The money — honest numbers, honest horizon'), spacer());

body.push(
  H1('§10 · Per-account economics, corrected'),
  P([T('The v2 forecast repeated the exact mistake this project was born to avoid: extrapolating a one-time backlog into permanent monthly recovery. The corrected picture:')]),
  tbl(
    ['Account type', 'Backlog campaign (once)', 'Steady state'],
    [
      ['Ordinary premium salon (~800 clients/yr, ticket R$300)', '~R$11–12k settled → ~R$2.3k fee', 'New-lapse cohorts ≈ R$150–250/month fee; quarterly seasonal re-runs can roughly double that'],
      ['Core ICP: multi-unit group / high-volume salon (500+ eligible)', 'R$25–60k settled → R$5–12k fee', 'R$1–2.5k/month blended, sustained by re-runs across units and seasons'],
    ],
    [3300, 2900, 3160],
  ),
  spacer(),
  P([B('The consequence, stated plainly: '), T('ordinary single salons are marginal on their own — good fair-won volume, good testimonials, not the core. The business is a '), B('campaign factory over a portfolio'), T(' whose center of gravity is multi-unit groups. Rough shapes of the destination: R$240k/month of fee revenue = R$1.2M/month of settled win-back GMV = 100 multi-unit groups averaging R$12k settled/month, or 200 mixed accounts at R$6k.')]),
  spacer(),
  H1('§11 · Taxes and the target, without flattering herself'),
  bullet([T('Simples Anexo III starts near 6% but is progressive: at R$2.4–2.8M annualized, the effective rate approaches ~16% — and holding Fator R at 28% of revenue would demand an unrealistic payroll at scale. Model with the Anexo III fifth-band effective (~16%) as the base case, treat a fall into Anexo V (effective ~19–21% beyond the first bands) as the downside when Fator R fails, and let the contador optimize, not the plan.')]),
  bullet([T('From 2026, dividends above R$50k/month from one company face 10% withholding — company profit is not personal cash 1:1.')]),
  bullet([T('Fixed costs stay tiny (contador, tools, infra, WhatsApp conversation fees, Asaas per-charge costs ≈ R$1.5–3k/month solo). The cost that scales is campaign operations — offer design, owner hand-holding, quality monitoring — which is why telemetry from the first ten campaigns, not this table, sets the hiring plan.')]),
  callout([
    P([B('The honest restatement of the goal: ', { color: GREEN }), T('R$150k/month personal net is the ambition, not the month-24 default. The evidence-backed path runs through ~R$240k/month fee revenue on a portfolio heavy in multi-unit groups — realistically a month-30+ outcome, faster only if large groups land early. Month-12 in a good-but-normal scenario: R$25–45k/month revenue. The first ten campaigns replace every number on this page with telemetry; that is production data, not a validation exercise.')]),
  ], 'F5EFE6', AMBER),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART V ----------
body.push(partBanner('Part V', 'Launch — four weeks to production, then the fair'), spacer());

body.push(
  H1('§12 · The build (production product, not an MVP)'),
  tbl(
    ['Week', 'Ships', 'Proof'],
    [
      ['1 · Aug 1–8', 'Entity + contador + contracts to lawyer · FastAPI/Postgres, tenants, auth · Trinks importer with allow-list · eligibility + opt-in engine · START Asaas + Meta production approvals (longest pole, day 1)', 'A real Trinks export is accepted; forbidden columns provably discarded; a non-opted-in row cannot enter a campaign'],
      ['2 · Aug 9–16', 'Campaign engine: template family, Cloud API coexistence onboarding, Postgres outbox with retry/idempotency, opt-out suppression, manifest approval', 'Coexistence proven end-to-end, live on the real salon number the day Meta verification clears (the clock started day 1 — week 2 is the target, launch is the gate); owner approves an exact manifest; opt-out suppresses instantly'],
      ['3 · Aug 17–24', 'Money: salon-owned Asaas connection, campaign checkout, 20% netValue split, payment/refund/chargeback webhooks, revenue ledger, salon statement, NFS-e export', 'A real Pix settles between two CNPJ accounts; split reaches both wallets; a real refund reverses both portions; webhook replay does not double-count'],
      ['4 · Aug 25–31', 'Hardening: tenant isolation, encrypted secrets, privacy notice + deletion controls, both dashboards · first real campaign end-to-end', 'One real lapsed client pays through a campaign link. The product is the proof.'],
    ],
    [1300, 5060, 3000],
  ),
  spacer(),
  H1('§13 · The 90 days'),
  tbl(
    ['Window', 'Do', 'Exit with'],
    [
      ['Weeks 1–4 · Aug', 'Build (above) · recruit the first 3 client salons for the first real campaigns (the first 3 clients at the 15% case-study fee, testimonial in writing) · Beauty Fair prep: live eligibility-scan demo on a tablet', 'Working product + first settled campaign + 2 case studies in motion'],
      ['Sep 5–8 · BEAUTY FAIR (Expo Center Norte, SP)', 'No booth. Live scans on a tablet: “manda seu CSV, te digo agora quantas clientes dá pra trazer de volta.” 10 distributor relationships. Close campaign #1 for 5–10 salons on the spot.', 'A pipeline of scanned, quantified prospects — each already holding their scan result'],
      ['Sep 9 – Oct 29', '48h follow-up on every scan · run campaigns weekly · publish first measured results (with permission) · referral ask built into every winning statement · POS opt-in kit for every client (grows the eligible pool every month)', '15–25 accounts run at least one campaign · real conversion/refund/settled-GMV telemetry · the M12 plan rewritten from data'],
    ],
    [2100, 5060, 2200],
  ),
  spacer(),
  H1('§14 · Operating it KISS'),
  P([B('Five numbers run the company: '), T('eligible opt-in pool (all accounts) · campaigns sent this month · settled GMV · fee revenue · refund rate. '), B('Three rituals: '), T('Monday 30-min pipeline; daily 2-hour growth block (mornings, untouchable); Friday close — read every salon statement, log the five numbers. '), B('Rule of one: '), T('one ICP, one fee, one template family per salon, one channel priority per quarter; new complexity must delete old.')]),
  P([B('Tripwires, responses pre-written: '), T('number quality rating drops → pause that account’s sends, review the template and audience. Refund rate >5% → redesign the offer, not the copy. Campaign conversion <5% twice → change the offer economics with the owner. Opt-in pool stagnant → push the POS opt-in kit before selling anything else. Every tripwire is visible on the dashboard before any client feels it.')]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- PART VI ----------
body.push(partBanner('Part VI', 'After launch — expansion gates and the endgame'), spacer());

body.push(
  H1('§15 · Phase-2 gates (opened by evidence, never by calendar)'),
  bullet([B('Gate A — first-party payment reminders: '), T('opens only with written BSP/Meta guidance that a salon reminding its own client of its own transaction, via utility template, is compliant at this operating scale. Then: same manifest gate, same rails, principal only, never “collections” branding.')]),
  bullet([B('Gate B — active-base campaigns: '), T('renewals, upsells, seasonal pushes to active clients. Opens when win-back telemetry proves the template/checkout machine on 20+ accounts. Same machinery, bigger pool — this is where per-account revenue stops depending on lapse alone.')]),
  bullet([B('Gate C — second importer (Belasis or Avec): '), T('opens the first time a signed prospect requires it.')]),
  bullet([B('Gate D — the ops hire: '), T('opens when campaign operations consume >60% of her week for a month — an ex-receptionist inheriting a written manual, CLT, exactly as the folder-is-the-manual pattern prescribes.')]),
  spacer(),
  H1('§16 · The endgame asset'),
  P([T('After 24 months of campaigns she owns the only dataset of its kind: measured win-back conversion by offer type, segment, ticket and season across hundreds of Brazilian beauty businesses — plus the trust position of the operator who only ever charged for money that landed. That funds the expansions (active-base campaigns, adjacent verticals with the same cadence shape) from a position of evidence, not hope. The moat was never the code; it is the results ledger and the name.')]),
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
            new TextRun({ text: 'Caixa Cheia · Canonical Plan v4 · ', color: GREY, size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 18 }),
          ],
        })],
      }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  require('fs').writeFileSync('/home/user/Random-Access-Memories/CAIXA_CHEIA_V4.docx', buf);
  console.log('written', buf.length, 'bytes');
});
