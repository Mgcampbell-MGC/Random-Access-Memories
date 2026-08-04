// PRUMO — Canonical Business Blueprint
// Mirrors the REAVER document's structure and depth, rebuilt ground-up.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType,
  LevelFormat, PageBreak, Header, Footer, PageNumber, TableOfContents,
} = require('docx');

const ACCENT = '1B4965';        // deep blue
const ACCENT_LIGHT = 'E4EEF4';
const GREY = '595959';
const RED = '9E2A2B';
const GREEN = '1E5631';
const AMBER = '8A6100';
const BODY = 21;
const FONT = 'Calibri';
const CW = 9026;

function runs(spec) {
  if (typeof spec === 'string') spec = [spec];
  return spec.map(s => {
    if (typeof s === 'string') return new TextRun({ text: s, size: BODY, font: FONT });
    return new TextRun({
      text: s.t, bold: !!s.b, italics: !!s.i, size: s.size || BODY,
      font: s.mono ? 'Consolas' : FONT, color: s.color || undefined,
    });
  });
}
function P(spec, opts = {}) {
  return new Paragraph({
    children: runs(spec),
    spacing: { after: opts.after ?? 140, before: opts.before ?? 0, line: 264 },
    alignment: opts.align,
    ...(opts.numbering ? { numbering: opts.numbering } : {}),
    ...(opts.border ? { border: opts.border } : {}),
    ...(opts.shading ? { shading: opts.shading } : {}),
    ...(opts.indent ? { indent: opts.indent } : {}),
  });
}
function H1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 340, after: 170 },
    children: [new TextRun({ text: text.toUpperCase(), bold: true, size: 30, font: FONT, color: ACCENT })],
  });
}
function H2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 230, after: 120 },
    children: [new TextRun({ text, bold: true, size: 24, font: FONT, color: '0E2C3F' })],
  });
}
function H3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 90 },
    children: [new TextRun({ text, bold: true, size: 22, font: FONT, color: GREY })],
  });
}
const bullet = spec => P(spec, { numbering: { reference: 'bul', level: 0 }, after: 80 });
const numbered = (spec, ref) => P(spec, { numbering: { reference: ref, level: 0 }, after: 80 });

function callout(spec, color) {
  return P(spec, {
    shading: { type: ShadingType.CLEAR, fill: ACCENT_LIGHT },
    border: {
      left: { style: BorderStyle.SINGLE, size: 24, color: color || ACCENT },
      top: { style: BorderStyle.NONE, size: 0 }, bottom: { style: BorderStyle.NONE, size: 0 },
      right: { style: BorderStyle.NONE, size: 0 },
    },
    indent: { left: 200, right: 160 }, before: 140, after: 160,
  });
}
function tbl(widths, rows, opts = {}) {
  const scale = CW / widths.reduce((a, b) => a + b, 0);
  const w = widths.map(x => Math.round(x * scale));
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: w,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0 && !opts.noHeader,
      children: r.map((cell, ci) => new TableCell({
        width: { size: w[ci], type: WidthType.DXA },
        shading: (ri === 0 && !opts.noHeader)
          ? { type: ShadingType.CLEAR, fill: ACCENT }
          : (opts.zebra && ri % 2 === 0 ? { type: ShadingType.CLEAR, fill: 'F2F7FA' } : undefined),
        margins: { top: 70, bottom: 70, left: 110, right: 110 },
        children: [new Paragraph({
          spacing: { after: 0, line: 250 },
          children: (Array.isArray(cell) ? cell : [cell]).map(c => {
            const isStr = typeof c === 'string';
            return new TextRun({
              text: isStr ? c : c.t,
              bold: (ri === 0 && !opts.noHeader) || (!isStr && c.b),
              italics: !isStr && c.i,
              color: (ri === 0 && !opts.noHeader) ? 'FFFFFF' : (!isStr && c.color ? c.color : undefined),
              size: opts.small ? 19 : 20, font: FONT,
            });
          }),
        })],
      })),
    })),
  });
}
const PB = () => new Paragraph({ children: [new PageBreak()] });

const c = [];   // document children

/* ────────────────────────── COVER ────────────────────────── */
c.push(new Paragraph({ spacing: { before: 2400, after: 0 }, children: [
  new TextRun({ text: 'PRUMO', bold: true, size: 96, font: FONT, color: ACCENT })] }));
c.push(new Paragraph({ spacing: { before: 60, after: 420 }, children: [
  new TextRun({ text: 'Canonical Business Blueprint', size: 32, font: FONT, color: GREY })] }));
c.push(new Paragraph({ spacing: { after: 200 }, children: [
  new TextRun({ text: 'Prestação de contas operations for Brazilian cultural producers financed by Lei Rouanet.', size: 24, font: FONT })] }));
c.push(callout([
  { t: 'DECISION STATUS: ', b: true },
  'APPROVED FOR FACTUAL VALIDATION. BLOCKED FROM PAID OPERATIONS, SOFTWARE BUILD, AND ANY HIRE UNTIL GATES 0A–0D HAVE PASSED.',
]));
c.push(new Paragraph({ spacing: { before: 900 }, children: [
  new TextRun({ text: 'Version 1.0  ·  Built ground-up after LÍQUIDO was killed by an incumbent.', size: 19, font: FONT, color: GREY })] }));
c.push(new Paragraph({ children: [
  new TextRun({ text: 'Method and governance structure harvested from the REAVER blueprint.', size: 19, font: FONT, color: GREY })] }));
c.push(PB());

/* ────────────────────────── TOC ────────────────────────── */
c.push(H1('Contents'));
c.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
c.push(PB());

/* ══════════════════════════ 1. TL;DR ══════════════════════════ */
c.push(H1('TL;DR'));

c.push(H2('The Idea in One Sentence'));
c.push(P('PRUMO keeps every Lei Rouanet project’s spending documentation reconciled against its approved planilha orçamentária in real time, so the prestação de contas is assembled continuously instead of excavated at the deadline, and no diligência ever expires unanswered.'));
c.push(P([
  'PRUMO does not sign the prestação de contas, does not practise contabilidade, does not move money, does not access SALIC with the client’s credentials, and does not promise approval. ',
  { t: 'The producer’s CRC-registered contador continues to sign; the legal representative continues to submit.', b: true },
]));

c.push(H2('Why It Deserves to Be Tested'));
c.push(bullet([{ t: 'The buyer census is already done, not estimated. ', b: true }, '933 Brazilian companies run 3+ concurrently funded Lei Rouanet projects; 448 run 4+; 246 run 5+. Counted from official SALIC open data, with names and CNPJs extracted.']));
c.push(bullet([{ t: 'The work is universal, not a rare event. ', b: true }, 'Every project that raises money must be documented line-by-line. 10.945 projects raised R$ 8,45 bilhões in 2023–26. There is no version of this that a funded producer can skip.']));
c.push(bullet([{ t: 'The expense category is named in primary law. ', b: true }, 'IN MinC 29/2026, Art. 22, inciso IX admits “contratação de serviço de elaboração de prestação de contas” as a project cost. The client can plausibly pay from the project’s own approved budget rather than their own pocket.']));
c.push(bullet([{ t: 'The incumbent is a human consultancy, not a funded startup. ', b: true }, 'Repeated targeted searches found courses and advisory firms — no proponente-side prestação de contas product.']));
c.push(bullet([{ t: 'It never touches money. ', b: true }, 'No payment rail, no custody, no Banco Central perimeter, no Asaas dependency. Structurally simpler than every prior candidate.']));
c.push(bullet([{ t: 'It fits one person. ', b: true }, 'At the target book, the entire operation is 38–57 working hours per month if per-project time holds at 30–45 minutes.']));

c.push(H2('What Has Not Yet Been Proven'));
c.push(bullet('Whether a MinC/SALIC analyst accepts PRUMO’s fee in the planilha when the nota fiscal describes a service delivered through software — and what NF wording and service code survive audit.'));
c.push(bullet('Whether the item can be added by readequação to already-executing projects, or only at proposal stage. Most of the 933-company pool already has live projects.'));
c.push(bullet('How many hours a producer actually spends per project on prestação de contas today. The entire labour-substitution case rests on this and it is unmeasured.'));
c.push(bullet('Whether assembling the Relatório de Execução Financeira brushes against activities reserved to CRC-registered contadores under Decreto-Lei 9.295/1946.'));
c.push(bullet('Whether producers will let a brand-new CNPJ near documentation whose failure carries a three-year ban.'));
c.push(bullet('Whether an existing consultancy already bundles this well enough at a comparable price.'));

c.push(H2('The Four Gates Before Charging Anyone'));
c.push(tbl([13, 87], [
  ['Gate', 'What must be true before it opens'],
  [[{ t: '0A', b: true }], 'RUBRICA. A contador who files Lei Rouanet prestações de contas confirms in writing: the correct Art. 22-IX framing, the NF wording and service code, whether it fits inside the 15% administrative envelope, and whether readequação can add it to a live project.'],
  [[{ t: '0B', b: true }], 'INVOICING ARCHITECTURE. One nota fiscal per PRONAC, carrying that project’s number and name, paid from that project’s own conta vinculada. Confirm Art. 6º §3º (distinct budgets, no overlapping items) does not obstruct it.'],
  [[{ t: '0C', b: true }], 'PROFESSIONAL PERIMETER. A written opinion separating document organisation and reconciliation (permitted to a non-contador) from the preparation of accounting statements (reserved). If no safe line exists, PRUMO ships as an organiser and deadline monitor only.'],
  [[{ t: '0D', b: true }], 'DATA AND LGPD. DPA, PII minimisation, per-client separation, retention and deletion schedule, MFA, no cross-client reuse. Project files contain personal data of contracted artists and suppliers.'],
], { zebra: true }));
c.push(callout([
  { t: 'If 0A or 0C fails: ', b: true },
  'do not force the model. PRUMO becomes a document-organisation and deadline-monitoring tool sold to the producer’s existing contador as a workflow, priced lower, or sold to the producer as operating-expense software rather than a project-budget line.',
], AMBER));

c.push(H2('Initial Scope'));
c.push(bullet([{ t: 'Mechanism: ', b: true }, 'Lei Rouanet (federal, Mecenato / Art. 18 and Art. 26) only. No state or municipal incentive laws, no Lei Paulo Gustavo, no editais at launch.']));
c.push(bullet([{ t: 'Client hypothesis: ', b: true }, 'a Brazilian pessoa jurídica proponente running 5 or more concurrently funded projects, at least one above R$ 700.000.']));
c.push(bullet([{ t: 'Geography: ', b: true }, 'São Paulo state first — 293 of the 933 qualifying companies, the largest single cluster, and the founder’s home city.']));
c.push(bullet([{ t: 'Product family: ', b: true }, 'execução financeira — matching comprovantes to approved budget lines, and never missing a diligência.']));
c.push(bullet([{ t: 'Out of launch scope: ', b: true }, 'writing project proposals, captação de recursos, choosing rubricas, tax advice, signing anything, and any activity reserved to a contador or advogado.']));

c.push(H2('Entry Offer'));
c.push(bullet([{ t: 'Diagnóstico (free, capped): ', b: true }, 'one finished or nearly finished project, its approved planilha, and its folder of comprovantes. PRUMO returns a reconciliation showing which budget lines are covered, which are short, and which would draw a diligência. Maximum two hours. No SALIC access, no credentials.']));
c.push(bullet([{ t: 'Piloto (paid, one project): ', b: true }, 'one live project, one PRONAC, one nota fiscal, ninety days. Priced by project size band.']));
c.push(bullet([{ t: 'Carteira (the business): ', b: true }, 'all of the producer’s live projects, one per-project line each, invoiced per PRONAC.']));

c.push(H2('Financial Target — Without a Solo-Operator Fantasy'));
c.push(P([
  'R$ 40.000 monthly personal net is the floor. On the modelled cost structure that requires ',
  { t: '11 client companies at an average of 6,3 active projects each', b: true },
  ' — roughly R$ 63.200 of collected monthly revenue, and about 70 active project-lines. This is a one-person business at that size and a two-person business at roughly double it. It is not a business that ever needs 100 customers.',
]));

c.push(H2('Investment Limits'));
c.push(bullet('Pre-proof cap: R$ 6.000. This buys the contador opinion (Gate 0A/0C), a domain, and travel.'));
c.push(bullet('No software written before three producers have accepted a manual diagnóstico and two have said they would pay.'));
c.push(bullet('No database, no portal, and no automation before ten paying project-lines are invoiced and collected.'));
c.push(bullet('No second incentive mechanism before 40 paying project-lines and three consecutive months of stable per-project minutes.'));
c.push(bullet('No hire before collected recurring revenue covers 2,5× the fully loaded cost of the role for three consecutive months, with three further months of payroll held in cash.'));

c.push(H2('The Decision That Ends Validation'));
c.push(P('Proceed only if every condition is met: Gate 0A returns a workable rubrica in writing; Gate 0C draws a safe professional line; five producers give a real planilha and comprovante folder; three say the current process costs them more than eight hours per project per month; two sign a paid pilot; and the first full month of operation runs at or under 45 minutes per project.'));
c.push(P([{ t: 'Kill or pivot if: ', b: true }, 'the fee cannot be booked to the project budget in any defensible form; the professional perimeter cannot be drawn; producers report under four hours per project per month; per-project time stays above 75 minutes after three months; or an existing consultancy already delivers this bundled at a comparable price.']));

c.push(H2('Next Step'));
c.push(P('The first two weeks buy nothing and build nothing. They are spent entirely on Gate 0A and Gate 0C — one paid hour with a contador who files Lei Rouanet prestações de contas — and on five conversations with producers drawn from the extracted list, asking how the last prestação de contas actually went.'));
c.push(PB());

/* ══════════════════════════ 2. THE BUSINESS ══════════════════════════ */
c.push(H1('The Business'));

c.push(H2('What PRUMO Is'));
c.push(P('PRUMO is an operations desk for the financial execution of incentivised cultural projects. It joins three activities that are currently fragmented across a spreadsheet, an email inbox, and a folder of PDFs:'));
c.push(bullet('holding the approved planilha orçamentária as the ledger of record for each project;'));
c.push(bullet('matching every comprovante — nota fiscal, recibo, comprovante de pagamento, contrato — to the specific budget line it belongs to, and flagging the ones that do not match;'));
c.push(bullet('tracking the calendar that the producer cannot afford to miss: execution windows, the deadline to submit, and the twenty-day clock on any diligência.'));
c.push(P('The product is not a report. It is a continuously maintained state of readiness, per project, with an audit trail.'));

c.push(H2('Safe Commercial Promise at Launch'));
c.push(callout([{ t: '“', i: true }, { t: 'Organizamos e conferimos a documentação da execução financeira dos seus projetos contra a planilha aprovada, em tempo real, e controlamos os prazos. Seu contador continua assinando; você continua enviando. A prestação de contas deixa de ser uma escavação e vira um botão.', i: true }, { t: '”', i: true }]));
c.push(P('This is deliberately narrower than “we do your prestação de contas.” It preserves the economic appeal without claiming a professional act PRUMO is not licensed to perform or an approval MinC controls.'));

c.push(H2('The Client’s Problem'));
c.push(P('A producer running five concurrent projects is running five separate accounting universes. Each has its own approved budget with its own rubricas, its own dedicated bank account opened by the Ministry, its own execution window, and its own pile of comprovantes that must each carry that project’s PRONAC number. Nothing is shared. Nothing can be pooled.'));
c.push(P('The producer may already have a contador and a spreadsheet. Those reduce the work but do not remove the human labour of:'));
c.push(bullet('deciding which of five budgets a given expense belongs to, and whether the approved rubrica actually covers it;'));
c.push(bullet('discovering, months later, that a nota fiscal is missing the PRONAC number and is therefore unusable;'));
c.push(bullet('noticing that a line is over budget before the ministry does;'));
c.push(bullet('answering a diligência within twenty days while running three other productions;'));
c.push(bullet('assembling, at the end, a coherent narrative from a year of scattered documents.'));
c.push(P([
  'The central hypothesis is that ',
  { t: 'an economically meaningful share of this work has no owner', b: true },
  ' — the contador books what arrives, the producer produces, and nobody is continuously reconciling. That must be proven in conversation, not asserted.',
]));

c.push(H2('What the Client Receives'));
c.push(bullet('A per-project ledger built from the approved planilha, with every rubrica and its committed, spent, and documented balance.'));
c.push(bullet('A live status for every budget line: covered, missing a document, mismatched, or over budget.'));
c.push(bullet('A document vault where each comprovante is attached to its line, checked for the PRONAC number, the value, the date inside the execution window, and the supplier CNPJ.'));
c.push(bullet('A deadline board: execution end, submission window, and a twenty-day countdown on any open diligência.'));
c.push(bullet('A monthly one-page readiness report per project, and a portfolio view across all of them.'));
c.push(bullet('An export pack the contador can work from directly, in the order SALIC expects.'));

c.push(H2('Why the Client Cannot Solve This With ChatGPT'));
c.push(P('A language model can summarise the rules. On its own it does not hold:'));
c.push(bullet('the approved planilha for each specific PRONAC, with its exact rubrica names and values;'));
c.push(bullet('the deterministic link between a comprovante and the budget line it must land on;'));
c.push(bullet('the state of what is already documented versus still open;'));
c.push(bullet('the deadline clocks, or anything that fires when one is about to expire;'));
c.push(bullet('an audit trail showing who attached what, when, and against which rule version.'));
c.push(P('The value is the maintained state and the calendar, not the text generation. AI is a classification and drafting tool inside that system.'));

c.push(H2('Where Defensibility Emerges'));
c.push(tbl([16, 84], [
  ['Stage', 'What exists'],
  [[{ t: '1 — None', b: true }], 'At launch there is a hypothesis and a manual process. Anyone could copy the idea; almost nobody wants this market.'],
  [[{ t: '2 — Rubrica library', b: true }], 'After real projects, PRUMO accumulates the mapping between real-world expenses and approved rubrica names across segments — the thing that is genuinely tacit and slow to rebuild.'],
  [[{ t: '3 — Switching cost', b: true }], 'A producer mid-execution with three years of documents in one system does not move it. The cost of switching rises every month of a project’s life.'],
  [[{ t: '4 — Referral density', b: true }], 'This is a small, tightly networked professional world. Reputation among contadores who serve cultural producers compounds faster than advertising ever could.'],
], { zebra: true }));

c.push(H2('What PRUMO Is Not'));
c.push(bullet('It is not an accounting firm and does not practise contabilidade. The client’s CRC-registered contador signs.'));
c.push(bullet('It is not a law firm and gives no opinion on what MinC will accept.'));
c.push(bullet('It does not write project proposals or raise money — captação is explicitly a vedação under Art. 33 and is not PRUMO’s business.'));
c.push(bullet('It does not hold funds and never touches the project’s conta vinculada.'));
c.push(bullet('It does not access SALIC with the client’s credentials.'));
c.push(bullet('It does not guarantee approval of any prestação de contas.'));
c.push(bullet('It does not support state or municipal incentive laws at launch.'));

c.push(H2('The Business Model in One Sentence'));
c.push(P('One free diagnostic on a finished project opens the door; one paid pilot on one live project proves the workflow; then every other live project in the producer’s portfolio is added as its own invoiced line — so revenue grows with the client’s project count without adding a single new sales conversation.'));

c.push(H2('Name and Brand'));
c.push(P('A prumo is the plumb line — the simple tool that tells you whether something is true or out of alignment. It states the product exactly: a budget line that fails a check is fora de prumo. The word is metaphorical rather than descriptive of the field, which makes a stronger mark at INPI than a domain term like “rubrica” or “confere” would. Before spending on brand or domain, run an INPI availability search in classes covering software and business-support services, and check prumo.com.br and variants. The brand must never imply MinC endorsement or certification.'));
c.push(P([{ t: 'Alternates held in reserve: ', b: true }, 'RÉGUA (from “tá na régua” — up to spec), CONFERE, ESTEIO. Any of them can replace the name without changing a word of the model.']));
c.push(PB());

/* ══════════════════════════ 3. CUSTOMER & LAUNCH WEDGE ══════════════════════════ */
c.push(H1('Customer and Launch Wedge'));

c.push(H2('Golden Rule'));
c.push(P('The initial segment is defined by concurrent project count and documentation surface — not by artistic prestige, project glamour, or how appealing the cultural output is.'));

c.push(H2('The Universe — Measured, Not Estimated'));
c.push(P('Source: SALIC open data API, all projects with ano_projeto 2023–2026. 45.863 project records pulled and analysed.'));
c.push(tbl([62, 38], [
  ['Measure', 'Value'],
  ['Projects registered 2023–26', '45.863'],
  ['Projects that actually raised money', '10.945 (23,9%)'],
  ['Total captado, those projects', 'R$ 8.448.892.045'],
  ['Funded and not archived', '9.663'],
  ['Distinct proponentes with funded live projects', '5.690 (PJ 4.981 / PF 709)'],
], { zebra: true }));
c.push(P([{ t: 'Note the 23,9%. ', b: true }, 'Three of every four registered Lei Rouanet projects never raise a centavo. Only funded projects generate a prestação de contas, and only funded projects have a budget to pay from. The addressable market is the funded quarter — everything below is computed on that basis.']));

c.push(H3('Addressable buyers, by concurrent funded projects (PJ only)'));
c.push(tbl([30, 20, 26, 24], [
  ['Concurrent funded projects', 'Companies', 'Their captado', 'Avg projects each'],
  ['≥ 2', '1.939', 'R$ 6,18 bi', '—'],
  [[{ t: '≥ 3', b: true }], [{ t: '933', b: true }], 'R$ 4,06 bi', '4,1'],
  [[{ t: '≥ 4', b: true }], [{ t: '448', b: true }], 'R$ 2,64 bi', '5,0'],
  [[{ t: '≥ 5  — the target', b: true }], [{ t: '246', b: true }], 'R$ 1,52 bi', '6,3'],
  ['≥ 6', '140', 'R$ 990 mi', '—'],
  ['≥ 8', '38', 'R$ 338 mi', '—'],
  ['≥ 10', '18', 'R$ 138 mi', '—'],
], { zebra: true }));

c.push(H3('Geography'));
c.push(P('Of the 933 companies running 3+ funded projects: SP 293, RS 139, RJ 111, MG 105, PR 79, SC 76, CE 29, ES 19, PE 18, BA 13.'));
c.push(callout([
  { t: 'São Paulo alone holds 145 companies running four or more funded projects concurrently, with R$ 1,067 bilhões captado between them. The business needs eleven customers.', b: true },
]));

c.push(H3('Project size distribution — the basis for pricing'));
c.push(P('Across the 3.823 funded live projects held by the 933 qualifying companies: median captado R$ 444.655; p25 R$ 200.000; p75 R$ 988.433; p90 R$ 2.158.101.'));
c.push(tbl([40, 20, 40], [
  ['Project size (captado)', 'Share', 'Note'],
  ['Até R$ 200.000', '24,7%', 'IN 29/2026 allows simplified analysis'],
  ['R$ 200.000 – 700.000', '39,5%', 'The core of the market'],
  ['R$ 700.000 – 1,5 mi', '19,9%', ''],
  ['R$ 1,5 mi – 6 mi', '13,3%', 'Above the standard PJ per-project cap; exception category'],
  ['Acima de R$ 6 mi', '2,5%', 'Special monitoring under IN 29/2026'],
], { zebra: true }));

c.push(H2('Initial ICP — Measurable Hypothesis'));
c.push(P('A Brazilian pessoa jurídica that:'));
c.push(bullet('holds five or more concurrently funded Lei Rouanet projects;'));
c.push(bullet('has at least one project above R$ 700.000;'));
c.push(bullet('is based in São Paulo state for the first cohort;'));
c.push(bullet('has an internal producer or administrative coordinator, but no dedicated prestação de contas person;'));
c.push(bullet('uses an external contador who receives documents rather than chasing them;'));
c.push(bullet('has at least one project whose execution window closes within the next nine months;'));
c.push(bullet('has a director or founding partner who can approve a pilot in one meeting.'));
c.push(P('These are prospecting hypotheses. The pilot must show which of them actually predicts hours saved and willingness to pay.'));

c.push(H2('Who Buys'));
c.push(bullet([{ t: 'Founding partner / diretor: ', b: true }, 'feels the risk personally — the inabilitação sanction attaches to the gestores, not only the company. Can decide alone.']));
c.push(bullet([{ t: 'Coordenador administrativo / produtor executivo: ', b: true }, 'owns the pain daily and will be the actual user. Their enthusiasm is the leading indicator.']));
c.push(bullet([{ t: 'The contador: ', b: true }, 'not the buyer, but holds veto power. If the contador says it makes their life harder, the deal dies. Design the export pack for them first.']));

c.push(H2('“Hell Yes” Signals'));
c.push(bullet('Five or more funded projects running at once.'));
c.push(bullet('A project ending within nine months whose documentation is visibly behind.'));
c.push(bullet('They have received a diligência in the past twelve months.'));
c.push(bullet('The phrase “we found out at the end” appears unprompted.'));
c.push(bullet('Comprovantes live in a shared drive with no link to budget lines.'));
c.push(bullet('One person can name the total of every project but not the balance of any single rubrica.'));
c.push(bullet('They run ações continuadas — a festival or season with recurring editions, where the next edition’s approval is conditioned on the previous edition’s prestação de contas.'));

c.push(H2('Immediate Disqualification'));
c.push(bullet('Fewer than three funded projects — the arithmetic does not reach the floor.'));
c.push(bullet('Pessoa física or MEI proponentes — capped at 2 and 4 projects and far too small.'));
c.push(bullet('An organisation with a full internal controladoria already doing this well.'));
c.push(bullet('A producer expecting PRUMO to sign, to give tax advice, or to tell them which rubrica to use.'));
c.push(bullet('A producer already inabilitado — the sale is moot until the sanction lapses.'));
c.push(bullet('A producer who wants help raising money. Captação is a vedação and not the business.'));

c.push(H2('Qualification in Twelve Questions'));
[
  'How many funded projects are running right now, and when does the earliest one end?',
  'Who assembles the prestação de contas today — you, an employee, or the contador?',
  'How many hours did the last one take, end to end, across everyone involved?',
  'Have you received a diligência in the last twelve months? What happened?',
  'Have you ever discovered a nota fiscal was unusable because it lacked the PRONAC?',
  'How do you know, today, the remaining balance of a specific rubrica?',
  'Where do comprovantes live between the expense and the prestação de contas?',
  'Has a budget line ever gone over without anyone noticing until the end?',
  'Do you run ações continuadas whose next edition depends on the previous prestação?',
  'Who would use this daily, and would they welcome it or resist it?',
  'Is your contador comfortable receiving an organised export instead of a box?',
  'If this cost R$ 690 per project per month, paid from the project’s own approved budget, would that be a decision you make alone?',
].forEach(q => c.push(numbered(q, 'q12')));

c.push(H2('Accessible Market — Bottom-Up'));
c.push(P('Do not quote 4.981 companies as the market. The honest funnel:'));
c.push(tbl([58, 42], [
  ['Stage', 'Count'],
  ['PJ proponentes with funded live projects', '4.981'],
  ['With 3+ concurrent funded projects', '933'],
  ['With 4+ concurrent funded projects', '448'],
  ['With 4+ and based in São Paulo', [{ t: '145', b: true }]],
  ['Contactable with a real named person', '~100 (to be proven)'],
  ['Qualified conversations', '20'],
  ['Free diagnostics delivered', '8'],
  ['Paid pilots signed', '3'],
  ['Customers needed for the R$ 40.000 floor', [{ t: '11', b: true }]],
], { zebra: true }));
c.push(P('If fewer than 20% of qualified prospects will hand over a planilha and a comprovante folder, the trust problem is real and the channel must change before anything is built.'));
c.push(PB());

/* ══════════════════════════ 4. OFFER & PRICING ══════════════════════════ */
c.push(H1('Offer and Pricing'));

c.push(H2('The Architecture That Determines Everything'));
c.push(P('Two regulatory facts set the shape of the entire commercial model, and getting either wrong makes the product unsellable.'));
c.push(callout([
  { t: 'Fact 1 — the named rubrica. ', b: true },
  'IN MinC 29/2026, Art. 22 caps custos de administração at 15% of project value and lists admitted expenses as a closed, numbered list I–X. Inciso IX admits “contratação de consultorias especializadas em gestão para a execução de projetos culturais, bem como contratação de serviço de elaboração de prestação de contas.” No inciso names software, licença de uso, assinatura, or SaaS.',
]));
c.push(callout([
  { t: 'Fact 2 — costs are PRONAC-siloed. ', b: true },
  'Every comprovante must carry the specific project’s PRONAC number and name and match an approved rubrica. Each project has its own Ministry-opened conta vinculada. Art. 6º §3º requires concurrent projects to have distinct budgets with no overlapping items. There is no rateio mechanism in this system.',
]));
c.push(P([
  { t: 'Therefore: PRUMO is sold as a service, never as a software subscription, and it is invoiced per project, never per company.', b: true },
  ' A single portfolio subscription has no documentary home and would create exactly the glosa risk no producer will accept from a new vendor.',
]));

c.push(H2('The KISS Commercial Packaging'));
c.push(P('One relationship, one contract, one negotiation — many invoices.'));
c.push(bullet('The producer has one conversation and agrees one price: R$ X per active project per month.'));
c.push(bullet('Behind that, PRUMO issues a separate nota fiscal per PRONAC, each carrying that project’s number and name, each payable from that project’s own conta vinculada.'));
c.push(bullet('The NF describes a service — “serviço de apoio à elaboração da prestação de contas” — not a software licence.'));
c.push(bullet('A project ends, its line ends. A project starts, a line starts. Churn and growth are mechanical and need no renegotiation.'));
c.push(P('The founder gets a single decision-maker. The producer’s contador gets N clean, boring, precedented invoices that look exactly like the ones they already approve.'));

c.push(H2('Price'));
c.push(P('Flat monthly fee per active project, banded by project size, because size drives the number of budget lines and therefore the work.'));
c.push(tbl([26, 26, 20, 28], [
  ['Faixa', 'Project captado', 'Preço / mês', 'Over an 18-month execution'],
  ['Simplificado', 'até R$ 200.000', 'R$ 290', '3,5% of project'],
  ['Padrão', 'R$ 200 – 700 mil', 'R$ 690', '2,8% of project'],
  ['Ampliado', 'R$ 700 mil – 1,5 mi', 'R$ 1.190', '2,1% of project'],
  ['Grande', 'R$ 1,5 – 6 mi', 'R$ 1.900', '1,1% of project'],
  ['Especial', 'acima de R$ 6 mi', 'R$ 2.900', '0,7% of project'],
], { zebra: true }));
c.push(P([
  'Every band lands at or below the ',
  { t: '2–5% of project value', b: true },
  ' that specialised accounting and consulting customarily costs on these projects — so the price is defensible to the producer, to their contador, and to a MinC analyst reading the planilha.',
]));
c.push(P([{ t: 'Weighted average across the real size distribution: R$ 906 per project per month.', b: true }, ' A producer with 6,3 active projects pays approximately R$ 5.745 per month in total, across roughly six separate invoices.']));

c.push(H2('The Three Stages'));
c.push(H3('Stage 1 — Diagnóstico (free, strictly capped)'));
c.push(bullet('Scope: one finished or nearly finished project, its approved planilha, its comprovante folder. Maximum two hours. No SALIC access. No credentials.'));
c.push(bullet('Output: a reconciliation showing covered lines, lines missing documents, mismatches, and anything likely to draw a diligência.'));
c.push(bullet('Honest binary outcome: “your documentation is in good order” or “here are the gaps.” Say the first one when it is true; it buys more credibility than a sale.'));
c.push(bullet('Capacity: no more than two per week until the conversion rate is known.'));
c.push(H3('Stage 2 — Piloto (one project, ninety days)'));
c.push(bullet('One live project, one PRONAC, one invoice at the band price, ninety days.'));
c.push(bullet('Success is defined before starting: every comprovante attached to a line within five business days of the expense, and a readiness report the contador confirms is usable.'));
c.push(bullet('Founder price locked for twelve months for the first three pilots.'));
c.push(H3('Stage 3 — Carteira'));
c.push(bullet('Every other live project added as its own line, at its own band price.'));
c.push(bullet('Ninety-day initial term, then month to month. No lock-in used to hide weak value.'));
c.push(bullet('Band is reviewed when a project’s captação changes materially.'));

c.push(H2('Billing Rules'));
c.push(bullet('One nota fiscal per PRONAC, always carrying the project number and name.'));
c.push(bullet('Invoice only for months in which the project was actually active.'));
c.push(bullet('Never invoice a project whose fee is not in its approved planilha — that puts the client at glosa risk and destroys the relationship.'));
c.push(bullet('If a project is archived or suspended, the line stops that month.'));
c.push(bullet('Administrative costs are payable proportionally to funds actually captured; a project that has captured nothing pays nothing.'));

c.push(H2('Unit Economics per Client'));
c.push(P('Before any renewal, compute: monthly revenue across the client’s project lines; minutes spent per project on ingestion, matching, chasing, and reporting; contribution margin; and concentration risk. Minimum target: contribution margin above 70%, achievable because there is no payment rail and no variable transaction cost. If a client consistently exceeds 75 minutes per project per month, reprice or reduce scope.'));
c.push(PB());

/* ══════════════════════════ 5. OPERATIONS ══════════════════════════ */
c.push(H1('End-to-End Operations'));

c.push(H2('Onboarding a Project (one-time, target 90 minutes)'));
[
  'Receive the approved planilha orçamentária and the portaria/PRONAC data from the client. No SALIC login.',
  'Import the planilha; every approved rubrica becomes a budget line with its approved value.',
  'Record the project’s key dates: execution window start and end, and the submission deadline.',
  'Record the supplier list already contracted, with CNPJ, so comprovantes can be matched automatically.',
  'Back-load existing comprovantes and reconcile to date. This produces the first readiness report — and is where the client first sees value.',
  'Agree the monthly rhythm and who sends what.',
].forEach(s => c.push(numbered(s, 'onb')));

c.push(H2('The Monthly Cycle (target 30–45 minutes per project)'));
[
  'Client drops comprovantes into the project folder as expenses happen, or forwards them by email.',
  'PRUMO extracts supplier, CNPJ, value, date, and document number, and proposes the budget line.',
  'Deterministic checks run: is the PRONAC on the document; is the value within the line’s remaining balance; is the date inside the execution window; does the CNPJ match a contracted supplier; is the document type acceptable for this rubrica.',
  'Exceptions are queued for human review — the founder’s only recurring manual work.',
  'The client sees a live board: lines covered, lines short, lines over, documents rejected and why.',
  'Any diligência received is logged with a twenty-day countdown and an alert schedule.',
  'Month-end: a one-page readiness report per project and a portfolio summary.',
].forEach(s => c.push(numbered(s, 'cyc')));

c.push(H2('Budget-Line States'));
c.push(tbl([30, 70], [
  ['State', 'Meaning'],
  ['Aprovada', 'In the planilha, nothing spent yet'],
  ['Comprometida', 'Contract signed, expense expected'],
  ['Documento recebido', 'A comprovante is attached, not yet validated'],
  ['Divergente', 'Attached but failing a check — missing PRONAC, wrong value, out of window, wrong CNPJ'],
  ['Conforme', 'Documented and passing every check'],
  ['Excedida', 'Spend above the approved line — needs readequação before it becomes a finding'],
  ['Em diligência', 'MinC has questioned it; twenty-day clock running'],
  ['Encerrada', 'Closed and included in a submitted prestação de contas'],
], { zebra: true }));

c.push(H2('Internal SLAs'));
c.push(bullet('Comprovante processed and attached: within two business days of receipt.'));
c.push(bullet('Divergence flagged to the client: same day it is detected.'));
c.push(bullet('Diligência logged and client alerted: within four hours of the client forwarding it.'));
c.push(bullet('Monthly readiness report: by the fifth business day.'));
c.push(P('MinC timelines are never guaranteed, and PRUMO never states a date for ministry action.'));

c.push(H2('Volume Controls'));
c.push(bullet('The first ten comprovantes of every new project are reviewed individually before any automated matching is trusted.'));
c.push(bullet('No automatic matching rule is trusted below 90% precision on that project’s own history.'));
c.push(bullet('A rubrica whose matches fail twice in a row is suspended to manual until reviewed.'));
c.push(bullet('If a client sends more than 150 comprovantes in a month for one project, reprice — that is outside the band assumption.'));

c.push(H2('Monthly Deliverable'));
c.push(P('One page per project: percentage of approved budget documented and conforme; value pending documentation; divergences open with reasons; lines at risk of exceeding; days remaining in the execution window; any diligência and its deadline; and what PRUMO needs from the client this month.'));
c.push(PB());

/* ══════════════════════════ 6. RULES, QA & ATTRIBUTION ══════════════════════════ */
c.push(H1('Rules, QA and Validation'));

c.push(H2('The Three Rule Families'));
c.push(H3('R1 — Document conformity'));
c.push(P('Does the comprovante itself satisfy the formal requirements: PRONAC number present, project name present, supplier identification, service description compatible with the approved rubrica, and a legible value and date. This is the rule that prevents the most common and most avoidable failure — a document that was always going to be rejected, discovered a year too late.'));
c.push(H3('R2 — Budget conformity'));
c.push(P('Does the expense fit the approved line: within the remaining balance of that rubrica, inside the execution window, within the 15% administrative envelope where applicable, and not in a category prohibited by Art. 33.'));
c.push(H3('R3 — Completeness and calendar'));
c.push(P('Is every approved line either documented, formally cancelled, or explained; and is every deadline — execution, submission, diligência — visible with enough lead time to act.'));

c.push(H2('Rule Contract'));
c.push(P('Every rule carries: the IN version and article it derives from; the eligible universe; required source fields; the deterministic test; mandatory exclusions; the confidence threshold; the human-review trigger; and its suspension conditions. When MinC publishes a new IN, every rule is re-versioned before it is applied to a live project.'));

c.push(H2('Metrics Governing Each Rule'));
c.push(bullet([{ t: 'Precision: ', b: true }, 'proportion of flagged divergences the client agrees are genuine. Below 80% the flag is noise and the rule is suspended.']));
c.push(bullet([{ t: 'Catch rate: ', b: true }, 'proportion of problems found by PRUMO rather than by the client, the contador, or MinC.']));
c.push(bullet([{ t: 'Time to attach: ', b: true }, 'median days between an expense and its comprovante being conforme.']));
c.push(bullet([{ t: 'Minutes per project-month: ', b: true }, 'the number that decides whether this is a one-person business. Target median under 45, P90 under 75.']));
c.push(bullet([{ t: 'Diligência response margin: ', b: true }, 'days remaining when a response is ready. Never below five.']));

c.push(H2('Two-Layer QA'));
c.push(P([{ t: 'Deterministic. ', b: true }, 'Code performs every comparison of value, date, and balance. Totals reconcile against the planilha on every run. Rule versions are logged.']));
c.push(P([{ t: 'Human. ', b: true }, 'The founder reviews every exception and every divergence before it reaches the client. AI never decides that a document is compliant and never performs arithmetic on money.']));
c.push(PB());

/* ══════════════════════════ 7. TECHNOLOGY ══════════════════════════ */
c.push(H1('Technology and Automation'));

c.push(H2('Non-Negotiable Principle'));
c.push(callout([{ t: 'Code calculates. AI reads, classifies, and drafts. AI never calculates money, never decides compliance, never submits anything, and never receives credentials.', b: true }]));

c.push(H2('The Build Is Small — On Purpose'));
c.push(P('Three tables carry the entire product:'));
c.push(tbl([24, 76], [
  ['Table', 'Contents'],
  ['projetos', 'PRONAC, name, proponente, execution window, submission deadline, size band, status'],
  ['linhas', 'One row per approved rubrica: name, approved value, committed, documented, state'],
  ['comprovantes', 'File, extracted fields, the linha it attaches to, validation result, reviewer, timestamp'],
], { zebra: true }));
c.push(P('Everything the client sees is a view over those three tables. There is no workflow engine, no rules DSL, and no integration with SALIC.'));

c.push(H2('Phased Build'));
c.push(tbl([14, 30, 56], [
  ['Phase', 'When', 'What'],
  [[{ t: 'A', b: true }], 'Before any code', 'Google Sheets, one per client, formulas visible. Run three real diagnostics manually. Learn where documents actually break.'],
  [[{ t: 'B', b: true }], 'After 2 paying pilots', 'Next.js + Supabase. Upload planilha, upload comprovantes, deterministic checks, readiness report. Roughly four weeks.'],
  [[{ t: 'C', b: true }], 'After 10 paying project-lines', 'Document extraction (OCR + LLM field extraction) to cut manual entry, with human confirmation on every field that affects a number.'],
  [[{ t: 'D', b: true }], 'After 40 project-lines', 'Client portal, contador export pack, WhatsApp alerts for diligência countdowns.'],
], { zebra: true }));

c.push(H2('Technical Flow'));
c.push(P([{ t: 'PLANILHA APROVADA → LINHAS DE ORÇAMENTO → COMPROVANTE RECEBIDO → EXTRAÇÃO DE CAMPOS → CONFERÊNCIA DETERMINÍSTICA → FILA DE EXCEÇÕES → REVISÃO HUMANA → ESTADO CONFORME → PAINEL E RELATÓRIO → PACOTE PARA O CONTADOR', mono: true, size: 18 }]));

c.push(H2('Honest Automation'));
c.push(P('Expect 40–55% of total hours automated at launch and perhaps 70% at maturity. Field extraction, checking, and reporting automate well. Chasing a producer for a missing document, judging an ambiguous rubrica, and holding the client relationship do not. Plan capacity on measured minutes, never on the phrase “it’s automated.”'));

c.push(H2('Build Triggers'));
c.push(bullet('Do not write code before three manual diagnostics are complete and two clients have paid.'));
c.push(bullet('Do not add OCR before manual entry is demonstrably the binding constraint on minutes per project.'));
c.push(bullet('Do not build a portal before clients ask for one twice.'));
c.push(bullet('Do not integrate anything with SALIC. It is the client’s system, accessed with the client’s credentials, and PRUMO stays out of it.'));
c.push(PB());

/* ══════════════════════════ 8. LEGAL ══════════════════════════ */
c.push(H1('Legal, Professional Perimeter and LGPD'));

c.push(H2('Starting Position'));
c.push(P('PRUMO carries operational, contractual, and data responsibility. It is not a zero-risk business. This blueprint defines commercial controls; the professional perimeter and the rubrica question both require Brazilian professional review before a single real invoice is issued.'));

c.push(H2('Gate 0A — The Rubrica'));
c.push(P('Art. 22 of IN 29/2026 lists admitted administrative expenses as a closed list I–X, capped at 15% of project value and payable proportionally to captação. Inciso IX names “contratação de serviço de elaboração de prestação de contas.” No inciso names software. Art. 33, inciso V separately prohibits payments that lack a “relação direta, necessária e comprovada” with the cultural object.'));
c.push(P('A contador who files Lei Rouanet prestações de contas must confirm, in writing: the NF wording and service code that survive audit; whether the fee sits inside the 15% envelope and how it interacts with the producer’s existing accounting fees in that same envelope; and whether the item can be added by readequação to an already-approved planilha or only at proposal stage.'));
c.push(callout([
  { t: 'No published TCU or CGU precedent was found blessing or rejecting a software-delivered service under Lei Rouanet. That absence is itself the finding: this is untested ground, and it must never be sold as settled.', b: true },
], AMBER));

c.push(H2('Gate 0C — The Professional Perimeter'));
c.push(P('Contabilidade is a regulated profession in Brazil under Decreto-Lei 9.295/1946, reserved to CRC-registered professionals. Organising documents, checking a value against an approved budget line, and tracking a deadline are plainly not accounting acts. Preparing formal accounting statements is. The boundary between them is where PRUMO must be careful, and the same logic that governs the OAB perimeter in adjacent businesses applies here: a CNAE code is not a safe harbour.'));
c.push(P('A written opinion must classify each activity as permitted to PRUMO, permitted only to the client’s contador, or prohibited. If a safe boundary cannot be drawn, PRUMO ships as a document organiser and deadline monitor and prices accordingly.'));

c.push(H2('Operational Traffic Light'));
c.push(tbl([16, 84], [
  ['', ''],
  [[{ t: 'GREEN', b: true, color: GREEN }], 'Import an approved planilha. Attach comprovantes to budget lines. Run deterministic checks on value, date, PRONAC, CNPJ. Flag divergences. Track deadlines. Produce readiness reports. Hand the client an organised export.'],
  [[{ t: 'AMBER', b: true, color: AMBER }], 'Depends on Gates 0A/0C: describing the fee as a prestação de contas service on the NF; assembling the Relatório de Execução Financeira itself; advising which rubrica an expense belongs to.'],
  [[{ t: 'RED', b: true, color: RED }], 'Signing anything. Practising contabilidade. Accessing SALIC with client credentials. Advising on tax. Interpreting whether MinC will accept an expense. Raising money or assisting captação. Touching the project’s conta vinculada.'],
], { zebra: true, noHeader: true }));

c.push(H2('Contract — Mandatory Provisions'));
c.push(bullet('Scope stated as document organisation, conference against the approved planilha, and deadline monitoring, with explicit professional exclusions.'));
c.push(bullet('The client’s contador signs and the legal representative submits; PRUMO never does either.'));
c.push(bullet('Best-efforts obligation with no guarantee of approval by MinC.'));
c.push(bullet('Client responsibility for the authenticity and completeness of documents supplied.'));
c.push(bullet('Per-PRONAC invoicing, with the fee payable only when it exists in that project’s approved planilha.'));
c.push(bullet('Liability cap with a meaningful floor; carve-outs defined by counsel.'));
c.push(bullet('Immediate suspension on a change of IN or a change in the project’s regulatory status.'));

c.push(H2('LGPD'));
c.push(P('Project documentation contains personal data of contracted artists, technicians, and suppliers — names, CPF, bank details, addresses. PRUMO is an operator processing on the producer’s instructions; the producer is controller.'));
c.push(bullet('DPA in every contract, with documented purpose, categories, duration, and instructions.'));
c.push(bullet('Strict per-client separation; no cross-client reuse, benchmarking, or model training.'));
c.push(bullet('PII removed before any content is sent to a language model; enterprise no-training configuration where offered.'));
c.push(bullet('MFA, least privilege, encryption at rest, and access logging from day one.'));
c.push(bullet('Retention through the project’s defence period, then deletion on a documented schedule. Comprovantes must be retained at least five years.'));
c.push(PB());

/* ══════════════════════════ 9. ECONOMICS ══════════════════════════ */
c.push(H1('Economics and Capacity'));

c.push(H2('What R$ 40.000 Net Means'));
c.push(P('Personal cash in hand after company costs, business taxes, and personal taxes. Not revenue, not margin, not a pre-tax distribution.'));

c.push(H2('Base Case — Eleven Clients'));
c.push(P('Eleven client companies averaging 6,3 active projects each, at the weighted average of R$ 906 per project per month, is roughly 70 active project-lines and R$ 63.198 of collected monthly revenue.'));
c.push(tbl([58, 42], [
  ['Line', 'Monthly'],
  ['Revenue — ~70 project-lines', 'R$ 63.198'],
  ['Operating costs — infra, tools, contador, legal amortised, travel', '(R$ 6.500)'],
  ['Simples Nacional DAS — Anexo III via Fator R, effective 11,30%', '(R$ 7.142)'],
  ['Pró-labore (gross)', '(R$ 19.500)'],
  [[{ t: 'Distribuição de lucros (isenta)', b: true }], [{ t: 'R$ 30.056', b: true }]],
  ['Pró-labore net of INSS and IRPF', 'R$ 14.383'],
  [[{ t: 'PERSONAL NET', b: true }], [{ t: 'R$ 44.439  ✓', b: true }]],
], { zebra: true }));

c.push(H2('Sensitivity'));
c.push(tbl([18, 22, 22, 20, 18], [
  ['Clients', 'Project-lines', 'Revenue', 'Personal net', 'Verdict'],
  ['9', '~57', 'R$ 51.707', 'R$ 34.580', 'Below floor'],
  ['10', '~63', 'R$ 57.452', 'R$ 39.550', 'Just below'],
  [[{ t: '11', b: true }], '~70', 'R$ 63.198', [{ t: 'R$ 44.439', b: true }], [{ t: 'FLOOR', b: true }]],
  ['12', '~76', 'R$ 68.943', 'R$ 49.265', 'Comfortable'],
  ['14', '~89', 'R$ 80.433', 'R$ 58.917', 'One person, stretched'],
  ['18', '~114', 'R$ 103.414', 'R$ 78.221', 'Needs a second person'],
], { zebra: true }));

c.push(H2('Tax Classification — Part of Gate 0A'));
c.push(P('The plan assumes Simples Nacional Anexo III via Fator R, which requires payroll of at least 28% of trailing twelve-month gross revenue. At eleven clients the RBT12 is roughly R$ 758.000, so qualifying payroll must exceed about R$ 17.700 per month; the modelled R$ 19.500 pró-labore clears it, but with little slack. If Fator R fails, Anexo V applies and the effective rate rises materially. The CNAE, corporate purpose, and invoice description must be set by an accountant before the first invoice — and the service description that satisfies Art. 22-IX must be consistent with the CNAE chosen.'));
c.push(P('Distributions above R$ 50.000 per month engage the 10% IRRF introduced by Lei 15.270/2025. At the base case the distribution sits below that; at eighteen clients it does not. Model it before it arrives.'));

c.push(H2('The Unit of Capacity Is the Project-Month'));
c.push(tbl([40, 60], [
  ['Minutes per project-month', 'Total monthly hours at 76 project-lines'],
  ['30 minutes', '38 hours — comfortably one person'],
  ['45 minutes', '57 hours — one person'],
  ['60 minutes', '76 hours — one person, fully occupied'],
  ['90 minutes', '114 hours — no longer viable solo'],
], { zebra: true }));
c.push(callout([
  { t: 'This single number decides whether PRUMO is the one-to-two person business it is designed to be. ', b: true },
  'Every engineering decision should be judged against whether it moves minutes per project-month down. If the measured median exceeds 75 minutes after three months of real operation, the product design is wrong — not the market.',
]));

c.push(H2('Cash and Working Capital'));
c.push(P('Unlike a success-fee model, this business invoices monthly for work already delivered, so the cash cycle is short. The risk is different: a project’s administrative costs are payable proportionally to captação, so a project that captures slowly pays slowly. Hold three months of operating costs in reserve, and never let one client exceed 20% of revenue.'));

c.push(H2('Hiring Triggers — Staying a One-to-Two Person Shop'));
c.push(bullet('No hire before collected revenue covers 2,5× the fully loaded cost for three consecutive months, with three further months of payroll in cash.'));
c.push(bullet('The first hire is a part-time operations assistant for document intake and chasing — not a salesperson, and not a developer.'));
c.push(bullet('Trigger: sustained above 90 active project-lines, or measured minutes above 60 for two consecutive months.'));
c.push(bullet('Reserve at least half the founder’s time for sales, QA, and client relationships. Never plan on 160 hours of delivery capacity from one person.'));

c.push(H2('Conditional Ramp'));
c.push(tbl([22, 30, 48], [
  ['Period', 'Revenue', 'What is happening'],
  ['Months 1–2', 'Zero', 'Gates 0A and 0C. Five producer conversations. Three manual diagnostics. No code.'],
  ['Months 3–4', 'R$ 1.500 – 4.000', 'First two paid pilots, one project each. Build v0 only if pilots convert.'],
  ['Months 5–9', 'R$ 12.000 – 28.000', 'Pilots expand to full portfolios. 4–6 clients.'],
  ['Months 10–16', 'R$ 35.000 – 55.000', '8–10 clients. Referral engine starts.'],
  ['Months 17–24', 'R$ 63.000+', '11+ clients. Floor reached.'],
], { zebra: true }));
c.push(P('This is a consequence of evidence and capacity, not a promised calendar.'));

c.push(H2('Economic Kill Criteria'));
c.push(bullet('The fee cannot be booked to a project budget in any defensible form, and producers will not pay from operating cash.'));
c.push(bullet('Measured minutes per project-month stay above 75 after three months of real operation.'));
c.push(bullet('Producers report spending under four hours per project per month today.'));
c.push(bullet('Contribution margin falls below 60%.'));
c.push(bullet('Fewer than 20% of qualified prospects will hand over a planilha.'));
c.push(bullet('Churn exceeds project completion — clients leaving for reasons other than a project simply ending.'));
c.push(PB());

/* ══════════════════════════ 10. SALES ══════════════════════════ */
c.push(H1('Sales'));

c.push(H2('The Buyer List Already Exists'));
c.push(P('This is the rarest advantage in the entire sequence of candidates: the prospect list is public, official, and already extracted. SALIC open data gives every proponente’s legal name, CNPJ, state, city, project count, and captação. There is no list to buy and no audience to build.'));
c.push(P('What the API does not give is a contact — no email, phone, or website field exists. Converting a CNPJ into a named human is the one unsolved mechanical step, and it is solved with public CNPJ lookup services and the producers’ own websites and Instagram pages, which cultural producers maintain actively because their business is public-facing.'));

c.push(H2('Channel Priority'));
c.push(tbl([8, 34, 58], [
  ['', 'Channel', 'Why'],
  ['1', 'Contadores who serve cultural producers', 'They hold the relationship, they feel the pain directly, and each one serves many producers. One good relationship introduces several qualified buyers. They are not a reseller — they refer, and the producer contracts PRUMO directly.'],
  ['2', 'Warm introductions from the São Paulo brand-sponsored cultural circuit', 'The founder’s events background touches brands that sponsor culture. A sponsor can name the producer who executes their project.'],
  ['3', 'Direct approach to named producers from the SALIC list', 'The list is real and qualified, but this is genuinely cold. Use it to fill gaps, not as the primary motion.'],
  ['4', 'Producer associations and sector events', 'Density is high but timing is annual.'],
], { zebra: true, noHeader: false }));
c.push(callout([
  { t: 'Honest warning: ', b: true },
  'messaging 145 companies found in a public database is cold outbound wearing a disguise, and cold outbound has been rejected. Channel 1 is the answer precisely because it converts a list into introductions. If after twenty attempts no contador relationship forms, the channel assumption is wrong and the plan needs revisiting before more effort is spent.',
], AMBER));

c.push(H2('The Entry Asset'));
c.push(P('One finished project. One planilha. One folder. Two hours. A reconciliation they have never seen before, showing exactly which lines are exposed. No credentials, no commitment, no software to install.'));

c.push(H2('First-Contact Script'));
c.push(P([{ t: 'To a producer:', b: true }]));
c.push(callout([{ t: '“Na última prestação de contas que vocês fecharam — quantas horas alguém passou juntando nota fiscal e conferindo contra a planilha aprovada? E já aconteceu de descobrir no fim que faltava o número do PRONAC em alguma nota?”', i: true }]));
c.push(P([{ t: 'To a contador:', b: true }]));
c.push(callout([{ t: '“Quando seus clientes de projeto cultural te mandam a documentação da execução, ela chega organizada por rubrica ou chega uma caixa? Quanto do seu tempo vai embora só organizando antes de conseguir trabalhar?”', i: true }]));
c.push(P('Open with the pain question. Never open with the product. The first call has no demo.'));

c.push(H2('Objections'));
c.push(tbl([38, 62], [
  ['Objection', 'Answer'],
  ['“Meu contador já faz isso.”', '“Ótimo — ele assina e continua assinando. A pergunta é se ele recebe a documentação organizada por rubrica ou monta tudo no fim. Se já chega pronta, você não precisa da gente.”'],
  ['“Não vou pagar por software.”', '“Você não paga por software. É serviço de apoio à prestação de contas, que é rubrica prevista, com nota fiscal por PRONAC — do jeito que você já paga a assessoria contábil.”'],
  ['“E se o MinC glosar essa despesa?”', '“Só faturamos contra projeto onde o item está na planilha aprovada. Se não estiver, não cobramos daquele projeto. Seu contador confirma antes.”'],
  ['“Não vou dar acesso ao meu SALIC.”', '“Não pedimos. Você exporta a planilha aprovada e nos manda os comprovantes. Nunca entramos no seu SALIC.”'],
  ['“Somos pequenos, tenho dois projetos.”', '“Então provavelmente ainda não vale a pena. Volta a fazer sentido a partir de uns quatro ou cinco projetos simultâneos.”'],
], { zebra: true }));

c.push(H2('Mandatory Competitive Check — Before Building'));
c.push(P('Before claiming differentiation, obtain a demonstration or proposal from at least three specialised consultancies serving this market — Squadra, Cultura e Mercado, and one regional firm. Ask each: do they organise documentation continuously or only at the end; do they charge per project or per hour; what do they actually charge; do they monitor diligência deadlines; and would they welcome a tool that delivered them organised documents. If a trusted consultancy already delivers continuous organisation at a comparable price, the offer must change or die.'));
c.push(P('This check runs first, not last. It is the discipline that the previous candidate’s failure bought.'));

c.push(H2('Sales Dashboard'));
c.push(bullet('Contador relationships opened, and introductions each produced.'));
c.push(bullet('Conversations per introduction; diagnostics per conversation.'));
c.push(bullet('Diagnostics delivered, and the share that found a real problem.'));
c.push(bullet('Pilots per diagnostic; portfolio expansion per pilot — the key ratio, because it is where revenue actually comes from.'));
c.push(bullet('Project-lines per client over time.'));
c.push(bullet('Losses by reason.'));
c.push(PB());

/* ══════════════════════════ 11. VALIDATION ══════════════════════════ */
c.push(H1('Validation and Roadmap'));

c.push(H2('Cap and Discipline'));
c.push(P('Pre-proof spending cap: R$ 6.000. No code, no brand, no tooling, no second mechanism until the gates pass and three producers have accepted a manual diagnostic.'));

c.push(H2('Stage 0 — The Two Questions That Decide Everything (Weeks 1–2, ~R$ 3.000)'));
c.push(bullet([{ t: 'Gate 0A: ', b: true }, 'one paid consultation with a contador who files Lei Rouanet prestações de contas. Bring Art. 22-IX and ask precisely: how would you book this fee, what must the nota fiscal say, does it fit the 15% envelope alongside your own fee, and can it be added by readequação to a live project?']));
c.push(bullet([{ t: 'Gate 0C: ', b: true }, 'in the same consultation or with a lawyer — where is the line between organising documents and practising contabilidade?']));
c.push(bullet([{ t: 'Outcome: ', b: true }, 'PASS proceeds to Stage 1. CONDITIONAL narrows scope and reprices. FAIL means selling to contadores as a workflow tool, or killing it.']));

c.push(H2('Stage 1 — Five Conversations (Weeks 2–4, ~R$ 300)'));
c.push(P('Five producers from the extracted São Paulo list, reached preferably through a contador introduction. The four questions, in order:'));
[
  '“Quantos projetos financiados vocês têm rodando agora, e quando termina o mais próximo?”',
  '“Na última prestação de contas, quantas horas isso tomou e de quantas pessoas?”',
  '“Já receberam diligência? Conseguiram responder no prazo?”',
  '“Se custasse R$ 690 por projeto por mês, pago pelo orçamento aprovado do próprio projeto, seria decisão sua sozinha?”',
].forEach(q => c.push(numbered(q, 'q4')));
c.push(P([{ t: 'Stop conditions — any one alone ends it: ', b: true }, 'three of five report under four hours per project per month; three of five say their contador already handles it end to end and they are satisfied; three of five will not pay from the project budget and will not pay from operating cash; or three of five run only one or two funded projects.']));

c.push(H2('Stage 2 — Three Manual Diagnostics (Weeks 4–8, R$ 0)'));
c.push(P('Three real projects reconciled by hand in a spreadsheet. Measure everything: minutes to onboard, minutes per comprovante, how many divergences were genuine, and whether the client considered the result valuable. This is where the minutes-per-project assumption is either confirmed or destroyed — before a line of code exists.'));

c.push(H2('Stage 3 — Two Paid Pilots (Weeks 8–20)'));
c.push(P('Two live projects, one PRONAC each, invoiced at band price against the approved planilha. Prove that the invoice is accepted, that the contador finds the export useful, and that measured minutes hold. Build v0 only once both pilots are paid.'));

c.push(H2('The Decision'));
c.push(P('Expand to full portfolios only when: both pilot invoices were paid without a rubrica problem; measured minutes per project-month are at or under 45; both clients ask to add more projects unprompted; and at least one contador has referred a second producer.'));
c.push(PB());

/* ══════════════════════════ 12. HONESTY ══════════════════════════ */
c.push(H1('What Is Not Yet Verified'));
c.push(P('Every item below is a known unknown, listed so that it cannot quietly become an assumption.'));
c.push(tbl([34, 66], [
  ['Unknown', 'Why it matters and how it gets resolved'],
  ['Whether the fee is accepted in the planilha', 'The entire frictionless-yes premise. Gate 0A, week one. No published TCU or CGU precedent exists either way.'],
  ['Hours currently spent per project', 'The whole labour-substitution case. Stage 1, question 2.'],
  ['Minutes per project-month at scale', 'Decides whether this is a one-person business. Stage 2 measures it manually before any build.'],
  ['The professional perimeter', 'Whether assembling the execution report is a reserved accounting act. Gate 0C.'],
  ['Readequação into live projects', 'Most of the 933-company pool already has projects running. If the item can only be added at proposal stage, the sales cycle lengthens by a year.'],
  ['Whether a consultancy already bundles this', 'Mandatory competitive check, before building.'],
  ['Contador channel viability', 'The entire go-to-market rests on it. Twenty attempts is the test.'],
  ['Producer trust in a new CNPJ', 'The sanction is severe and the vendor is unknown. The free diagnostic exists to solve this and may not be enough.'],
  ['Political durability of Lei Rouanet', 'Mitigating evidence: R$ 3,41 bi captado in 2025, third consecutive record, and the mechanism survived a CPI. Still a real, permanent risk outside anyone’s control.'],
], { zebra: true }));

c.push(H2('The Honest Weakness'));
c.push(P('The catastrophic sanction is real and rare. Across 45.863 projects, 84 prestações de contas were reproved — 0,18%, roughly one in 550. Selling this as insurance against a three-year ban would be selling protection against a loss that almost never lands, and that is precisely the mistake that killed three earlier candidates.'));
c.push(callout([{ t: 'PRUMO must be sold on throughput and calm, never on fear. The pitch is “your prestação de contas is always ready and you never miss a prazo” — not “you could be banned.” The ban is a footnote in the contract, not a line in the sales deck.', b: true }]));
c.push(P('The second honest weakness is network fit. Cultural producers are not the founder’s modelling and luxury-events world. The contador channel and the São Paulo brand-sponsored cultural circuit are bridges, not existing relationships. This is the single biggest reason PRUMO is a candidate under validation rather than a decision already made.'));

/* ────────────────────────── DOC ────────────────────────── */
const doc = new Document({
  creator: 'PRUMO', title: 'PRUMO — Canonical Business Blueprint',
  description: 'Prestação de contas operations for Lei Rouanet cultural producers',
  numbering: {
    config: [
      { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 340, hanging: 200 } } } }] },
      ...['q12', 'onb', 'cyc', 'q4'].map(ref => ({
        reference: ref,
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 360, hanging: 220 } } } }],
      })),
    ],
  },
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  sections: [{
    properties: { page: { margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: 'PRUMO — Canonical Business Blueprint', size: 16, font: FONT, color: GREY })],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: ['', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], size: 16, font: FONT, color: GREY })],
      })] }),
    },
    children: c,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/home/user/Random-Access-Memories/PRUMO_Canonical_Business_Blueprint.docx', b);
  console.log('WROTE', b.length, 'bytes');
});
