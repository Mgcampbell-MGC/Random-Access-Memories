const docx = require("docx");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, Footer, PageNumber, TableOfContents,
} = docx;
const fs = require("fs");

/* ---------- palette ---------- */
const GREEN = "0B4A36", GREEN2 = "0A6E4C", INK = "141414", GREY = "5B6B66",
      RULE = "1D6B4F", LINE = "C9D6D0", AMBER = "8A4B0B", RED = "8A1C1C";

/* ---------- helpers ---------- */
const T = (text, o = {}) => new TextRun({ text, ...o });
const B = (text, o = {}) => new TextRun({ text, bold: true, ...o });
const I = (text, o = {}) => new TextRun({ text, italics: true, ...o });
const P = (text, o = {}) => new Paragraph({ children: [T(text)], ...o });
const PR = (runs, o = {}) => new Paragraph({ children: runs, ...o });
const bullet = (runs, o = {}) =>
  new Paragraph({ children: Array.isArray(runs) ? runs : [T(runs)], bullet: { level: 0 }, spacing: { line: 340, after: 90 }, ...o });
const numItem = (n, runs) =>
  new Paragraph({ children: [B(n + "  ", { color: GREEN2 }), ...(Array.isArray(runs) ? runs : [T(runs)])], spacing: { line: 340, after: 110 }, indent: { left: 360, hanging: 360 } });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T(t)] });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [T(t)] });
const spacer = (h = 80) => new Paragraph({ spacing: { after: h }, children: [T("")] });
const hr = () => new Paragraph({ spacing: { before: 60, after: 160 }, border: { bottom: { color: LINE, space: 1, style: BorderStyle.SINGLE, size: 8 } }, children: [T("")] });
const partBanner = (kicker, title) => [
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ spacing: { before: 200, after: 40 }, children: [B(kicker, { color: GREEN2, size: 22, allCaps: true })] }),
  new Paragraph({ spacing: { after: 60 }, border: { bottom: { color: GREEN, space: 4, style: BorderStyle.SINGLE, size: 18 } }, children: [B(title, { color: GREEN, size: 46 })] }),
  spacer(120),
];
const callout = (children, fill = "E9F2ED", edge = GREEN2) =>
  new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [9360],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: "BCD8CC" }, bottom: { style: BorderStyle.SINGLE, size: 6, color: "BCD8CC" },
      left: { style: BorderStyle.SINGLE, size: 24, color: edge }, right: { style: BorderStyle.SINGLE, size: 6, color: "BCD8CC" },
      insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
    },
    rows: [new TableRow({ children: [new TableCell({ width: { size: 9360, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill, color: "auto" }, margins: { top: 130, bottom: 130, left: 180, right: 180 }, children })] })],
  });
function runsFrom(c) {
  if (typeof c === "string") return [new TextRun({ text: c, size: 22, color: INK })];
  if (Array.isArray(c)) return c.map(x => new TextRun({ size: 22, color: INK, ...x }));
  return [new TextRun({ text: c.t, bold: !!c.b, italics: !!c.i, color: c.color || INK, font: c.mono ? "Consolas" : undefined, size: c.size || 22 })];
}
function tbl(headers, rows, widths) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: LINE };
  const headRow = new TableRow({ tableHeader: true, children: headers.map((h, i) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: GREEN, color: "auto" },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ spacing: { line: 260, after: 0 }, children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 22 })] })],
  })) });
  const bodyRows = rows.map((r, ri) => new TableRow({ children: r.map((c, i) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA }, shading: ri % 2 ? { type: ShadingType.CLEAR, fill: "F2F6F4", color: "auto" } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ spacing: { line: 264, after: 0 }, children: runsFrom(c) })],
  })) }));
  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: widths, borders: { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border }, rows: [headRow, ...bodyRows] });
}
const RN = (name) => ({ t: name, mono: true, b: true, color: RULE, size: 18 });
const CODE = (t) => ({ t, mono: true, size: 20, color: INK });
const V = (verdict) => {
  const map = { GREEN: ["GREEN", GREEN2], YELLOW: ["PROVE", AMBER], RED: ["STOP", RED] };
  const [label, col] = map[verdict] || ["?", INK];
  return { t: label, b: true, color: col, size: 19 };
};

const body = [];
const push = (...x) => x.forEach(e => body.push(e));

/* ================= TITLE ================= */
push(
  new Paragraph({ spacing: { before: 1200, after: 0 }, children: [B("VOLTA", { size: 150, color: GREEN })] }),
  new Paragraph({ spacing: { before: 40, after: 60 }, children: [B("Business Plan & Technology Overview", { size: 40, color: INK })] }),
  new Paragraph({ spacing: { after: 240 }, children: [B("Version 3  ·  ", { size: 26, color: GREEN2 }), T("verified assumptions, stress-tested, pilot-first — engineered to find out, not yet proven", { size: 26, color: GREY })] }),
  new Paragraph({ spacing: { after: 120 }, children: [T("Managed, success-fee financial recovery for professional Mercado Livre ", { size: 28, color: GREY }), B("Full", { size: 28, color: GREY }), T(" sellers in Brazil.", { size: 28, color: GREY })] }),
  new Paragraph({ spacing: { after: 40 }, border: { top: { color: LINE, space: 6, style: BorderStyle.SINGLE, size: 8 }, bottom: { color: LINE, space: 6, style: BorderStyle.SINGLE, size: 8 } },
    children: [I("“Encontramos valores elegíveis que não voltaram para a sua operação, montamos a prova e acompanhamos o caso até o crédito cair. Você só paga sobre o que efetivamente receber.”", { size: 26, color: GREEN2 })] }),
  spacer(300),
  new Paragraph({ children: [B("The thesis.  ", { size: 26, color: INK }), T("Build the truth machine, not the company. First prove — on one real seller, with production-grade instrumentation — that the recoverable money is real, large, recurring, and causally VOLTA’s, at a margin that survives real cost. Code computes every centavo; a human authorizes every external action; the seller pays only on money that actually lands and stays. Everything else is earned one gate at a time.", { size: 26, color: INK })], spacing: { line: 360, after: 200 } }),
  spacer(160),
  new Paragraph({ children: [B("Prepared: ", { color: GREY, size: 24 }), T("23 July 2026  ·  Confidential working draft for the founder.", { color: GREY, size: 24 })] }),
  new Paragraph({ children: [B("Status, stated plainly: ", { color: GREY, size: 24 }), T("this is airtight as a PLAN — every load-bearing risk is named, bounded, instrumented, and cheap to falsify — but it is not a proven business, and it cannot be made one on paper. Four questions decide everything, and only a live pilot answers them: can VOLTA legally act, can it actually get paid, is the recovery causally its own, and does the money exceed the cost.", { color: GREY, size: 24 })], spacing: { line: 340 } }),
);

/* ================= TOC ================= */
push(
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ spacing: { after: 160 }, children: [B("Contents", { size: 40, color: GREEN })] }),
  new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-1" }),
);

/* ================= ORIENTATION ================= */
push(...partBanner("Orientation", "What Changed, and Why to Trust It"));
push(H1("0.  How This Version Was Built"));
push(P("Version 2 was a strong, ambitious plan. An external CTO/COO review found that several unverified assumptions were written as if they were confirmed system requirements. Rather than argue, VOLTA put the plan through four independent audits, each a fan-out of specialist agents: a verification pass (seven agents checking every external claim against primary sources, returning GREEN / PROVE-LIVE / STOP verdicts); a holdover scan (six agents hunting assumptions that were correct when the work was manual but go stale under automation); a stress and pre-mortem pass (six agents running a failure-injection red-team, a unit-economics model, and the pre-mortem); and a solutions pass (six agents designing a concrete fix for each open problem, plus a completeness critic and a consistency review of this document itself)."));
push(callout([
  PR([B("The single biggest change from v2.  ", { color: GREEN }), T("v2 said “validate the business by hand, then build the platform.” v3 says “validate the economics on a narrow, production-grade truth machine from day one, and do not build the company until the truth machine has told the truth.” Nothing here assumes the recovery works — the whole design exists to find out, cheaply, before a platform is built.")]),
]));

/* ================= PART I — THE BUSINESS ================= */
push(...partBanner("Part I", "The Business"));

/* 1 */
push(H1("1.  Executive Summary"));
push(P("VOLTA is a managed, success-fee recovery service for professional Mercado Livre “Full” (fulfilment) sellers in Brazil. It connects read-only to a seller’s Mercado Livre and Mercado Pago accounts, reconciles what happened operationally (Full inventory movements, inbound receiving, orders, returns, claims) against what happened financially (Mercado Pago releases, credits, fees), and surfaces money the seller is owed but never received. VOLTA assembles the evidence, pursues each case through permitted channels, and reconciles the credit when it lands. The seller pays only when a VOLTA-managed case produces a confirmed credit that appears — and stays — in their own records."));
push(P("This is the Amazon FBA reimbursement-recovery playbook, a proven US industry, brought to Mercado Livre, plus a second recoverable pool (Mercado Pago payments) the Amazon tools do not have. What is unproven is not the model but four things, and the pilot exists to answer them: that a third-party app can legally act; that VOLTA causes an incremental recovery rather than merely observing an automatic one; that credits can be matched cleanly enough to bill and collect; and that the money exceeds the cost."));
push(callout([
  PR([B("The shape of the whole system.  ", { color: GREEN }), T("One append-only, hash-chained event spine in one Postgres feeds exactly three consumers: the operator Workbench, the Dashboards, and the Automation layer. Two invariants hold everywhere — code computes every centavo, and every external action is either approved by a named human or, later, by a versioned delegated-authority policy a named human signed. In the pilot, a human approves every external action, full stop; automation earns its autonomy one action-class at a time.")]),
]));
push(spacer(60), H3("Snapshot"));
push(tbl(
  ["Dimension", "Position (v3)"],
  [
    ["What it is", "Managed, success-fee recovery of money Mercado Livre / Mercado Pago owe a Full seller — run from dashboards, executed with automation that earns autonomy gate by gate."],
    ["Target customer", [{ t: "Measured recoverable leakage above a computed cost-to-serve floor", b: true }, { t: ", with retrievable NF-e evidence, a non-Model-6 account, and standing to pay. Tiered: anchor + long-tail. The pilot serves anchors only." }]],
    ["Pricing", [{ t: "Pure success-only, one value-anchored fee", b: true }, { t: " (≈20–25%), plus a per-invoice minimum sized to transaction cost. No monthly base. White-label revenue share for distribution." }]],
    ["Scope", [{ t: "Brazil only, by choice.", b: true }, { t: " Growth is deeper Brazil + white-label + adjacent Brazilian marketplaces behind a KISS gate. Abroad is out of scope." }]],
    ["North-star metric", [{ t: "Net-attributable recovered BRL per seller and per R$ of fixed cost.", b: true }, { t: " Minutes-per-case is a health tripwire, not the north star." }]],
    ["Seller ramp", "Capability Proof on 1 live seller → access validated on ≥3 → the causal RCT across ≥5 anchor sellers. The tail opens only after the low-end metrics hold."],
    ["Kill test", "The immediate-vs-safely-delayed experiment. If delayed cases pay out on their own at similar rates, there is no business."],
  ],
  [2400, 6960],
));

/* 2 */
push(H1("2.  The Problem VOLTA Solves"));
push(P("A large Full seller generates thousands of operational and financial events every month. Each is visible somewhere on the platform, but knowing whether the seller received the correct financial treatment requires reconciling several data sources the platform never joins for them. No busy operations team does this by hand, so the losses — individually small, constant, easy to ignore — quietly stay with the platform."));
push(P("The questions a seller cannot answer at scale: Was damaged Full inventory credited, and at the right value? Did a negative stock adjustment ever get reimbursed? Was an approved claim actually deposited, in full? Was a returned item received in the condition claimed? Is there still an available seller action before a deadline closes the claim in the platform’s favour? Does a Mercado Pago credit actually match the event that should have generated it, or was a chargeback wrongly debited or a commission overcharged? VOLTA turns these disconnected records into one controlled recovery workflow — while being honest that some of these credits the platform now pays automatically, which is exactly why causality must be measured, not assumed."));

/* 3 */
push(H1("3.  The Customer — a Measured-Leakage Ideal, Not a Size"));
push(P("The v2 qualifier was “≥ R$300k/month GMV or ≥ R$250k in Full.” That threshold was a labor-cost floor in disguise: when a human assembled each case in 20–45 minutes, a seller had to be big enough to justify the hand-work, and GMV was a cheap proxy used to pre-qualify before spending any labor. Automation collapses that cost and removes the need for the proxy — the near-free audit itself becomes the qualifier. So the ideal customer stops being a size and becomes a signal."));
push(callout([
  PR([B("The corrected qualifier.  ", { color: GREEN }), T("A seller qualifies when: (1) measured recoverable leakage from the scan clears a "), B("computed cost-to-serve floor"), T(" (annualised per-seller fixed cost + per-case fiscal and payment cost + expected support minutes, divided by expected cases); AND (2) NF-e evidence is "), B("retrievable"), T(" (kept locally or pullable from SEFAZ) and data-completeness is above threshold; AND (3) the account is "), B("not Model-6"), T(" (which returns 403 on the claim endpoints); AND (4) the seller has "), B("standing to pay"), T(" (account age / solvency, and a signed collection mandate — see Section 26). Leakage alone is not enough — the old GMV screen was silently screening for data quality and solvency too, and dropping it invites adverse selection.")]),
]));
push(H3("Two tiers, one machine"));
push(
  numItem("Anchor —", [T("established mid-to-large Full sellers. Still ideal: high recoverable value per seller, low relative support burden, cleaner collection, and they produce the proof that unlocks white-label. Automation makes them "), I("cheaper"), T(" to serve, not less ideal. "), B("The pilot serves anchors only", { color: GREEN2 }), T(", to prove causality cheaply with fewer sellers and better documents.")]),
  numItem("Long-tail —", [T("smaller Full sellers, reachable because the marginal case is near-free. Served "), B("low-touch / self-serve / partner-distributed"), T(", qualified by measured leakage above the floor, and opened "), B("only after"), T(" the pilot proves that minutes-per-case and false-positive rate hold at the low end. The costs that do "), I("not"), T(" automate away — support, trust, collection, acquisition — all worsen down-market, so the tail opens deliberately, gated on measured cost-to-serve.")]),
);
push(callout([
  PR([B("Adverse-selection guard.  ", { color: AMBER }), T("“Connect and see the money you’re owed” preferentially attracts the worst-run, least-solvent sellers — the ones with the most leakage and the weakest evidence and collection. The qualifier’s data-completeness and standing screens exist specifically to catch this, and the tail free scan reveals magnitude and category counts only, never the case-level “how,” so it cannot become a self-filing playbook.")], "F7EFE0", AMBER),
]));

/* 4 */
push(H1("4.  Market Size & Income Scaling — Brazil"));
push(P("VOLTA is a Brazil-only business by choice. Scaling comes from distribution (white-label) and automation (falling cost-to-serve), not headcount. The figures below are order-of-magnitude estimates to replace with pilot measurement — and v3 corrects three v2 habits that flattered them: a single blended recovery %, a flat ARPU held across tiers, and one blended conversion rate."));
push(tbl(
  ["Layer (Brazil)", "Sellers (est.)", "Basis — and what the pilot must replace"],
  [
    [{ t: "TAM — professional NF-e sellers on ML", b: true }, "180k–220k", "CNPJ sellers issuing NF-e (modelo 55); excludes Model-6 and hobby sellers"],
    [{ t: "SAM — Full + real leakage, after filters", b: true }, "25k–40k", "On Full, leakage above the cost-to-serve floor, NF-e retrievable, non-Model-6 — wider than v2 because the labor floor is gone"],
    [{ t: "SOM — a 24–36 mo beachhead", b: true }, "600–1,500", "Anchors direct + first white-label partners; tail via partners once proven"],
  ],
  [3400, 1900, 4060],
));
push(spacer(60));
push(P("Recovery is not one percentage. The pilot must report recoverable value as an absolute BRL distribution per seller-decile, reported separately for the Full pool and the Mercado Pago pool, and net of what Mercado Livre pays spontaneously. Likewise ARPU is not flat: anchor, tail, and white-label carry three different numbers, and the blend falls as tail and partner share rise."));
push(tbl(
  ["Scenario (illustrative, mix-weighted)", "Anchor ARPU", "Blended ARPU", "≈ Monthly revenue"],
  [
    ["50 sellers, anchor-heavy", "~R$3,000", "~R$2,800", "~R$140k"],
    ["150 sellers, tail emerging", "~R$3,000", "~R$2,300", "~R$345k"],
    [{ t: "300 sellers, white-label led", b: true }, [{ t: "~R$3,000", b: true }], [{ t: "~R$1,900", b: true }], [{ t: "~R$570k", b: true }]],
    ["600 sellers, partner portfolios", "~R$3,000", "~R$1,600", "~R$960k"],
  ],
  [3400, 1980, 1980, 2000],
));
push(spacer(60));
push(callout([
  PR([B("Honest correction.  ", { color: AMBER }), T("v2 held blended ARPU flat or rising as sellers grew, over a tail-and-partner mix that is structurally lower-ARPU. v3 lets the blend fall. A few hundred good anchor books is still a strong Brazil-only company; the tail adds volume, not per-seller richness, and only pays if it is genuinely low-touch.")], "F7EFE0", AMBER),
]));

/* 5 */
push(H1("5.  Why Now — a Proven Analog, and the Causality Caveat"));
push(P("Marketplace reimbursement-recovery is a mature US industry. The “we only get paid when you get paid” structure is why it converts and why it exists."));
push(tbl(
  ["Player (US / Amazon FBA)", "Model", "Fee", "Signal"],
  [
    [{ t: "GETIDA (category leader)" }, "Automated audit + human case managers", "25%", "$1B+ recovery opportunities identified; waits ~90d to avoid billing auto-pays"],
    [{ t: "Seller Investigators" }, "Human-led weekly review", "25%", "High reported success rate; labor-priced"],
    [{ t: "Refully" }, "Software-first + dashboard", "18%", "Cheaper because less human labor — the tell"],
  ],
  [2500, 2900, 1160, 2800],
));
push(spacer(60));
push(P("Two lessons v3 takes from the analog. First, the software-first comp (Refully, 18%) already prices below the labor-heavy incumbents — evidence that VOLTA’s near-zero cost is a pricing weapon, not 25% margin to bank (Section 6). Second, GETIDA deliberately waits ~90 days before filing, because Amazon auto-reimburses most customer-return issues within ~64 days — filing sooner would bill for money that was already coming. That is the causality problem in one sentence."));
push(callout([
  PR([B("The causality caveat, stated plainly.  ", { color: AMBER }), T("Mercado Livre already auto-compensates some damaged-Full-inventory events (reportedly within ~10 business days at listed price). A residual difference plus one confirmed credit does "), B("not"), T(" prove VOLTA caused it. The pilot proves causality with a randomized immediate-vs-safely-delayed experiment (Section 29): a credit that appears only in the treated arm is attributable; one that appears in the delayed arm too was spontaneous. The transplanted “1–3% of revenue recoverable” figure is a hypothesis to test per pool and per decile, never a modelled input.")], "F7EFE0", AMBER),
]));

/* 6 */
push(H1("6.  Pricing & How VOLTA Gets Paid"));
push(H3("Pricing — one service, success-only, value-anchored"));
push(P("v3 collapses the v2 tier stack into one managed recovery service at a single, value-anchored success fee, with no monthly base. The fee is the share of recovered money a seller will happily cede for zero-effort recovery — not a pass-through of labor VOLTA no longer incurs. A per-invoice minimum fee, sized to transaction cost, protects against loss-making micro-recoveries; it is expressed once, per recovery cycle, never as a subscription. (The value-anchored % must be set net of VOLTA’s own tax — see Section 32 — so the headline rate is an input, not a given.)"));
push(tbl(
  ["Element", "v3 position", "Why"],
  [
    [{ t: "Success fee", b: true }, "One value-anchored % (≈20–25%), pure success-only", "Anchored to value, not competitors’ labor cost; near-zero cost is a tail weapon, not margin to bank"],
    [{ t: "Monthly base", b: true }, [{ t: "None — removed", b: true }], "The R$1,490 base only “covered a labor floor” automation deleted; it broke zero-downside and killed the tail"],
    [{ t: "Minimum fee", b: true }, "Per-invoice floor sized to fiscal + payment cost", "Prevents loss-making tiny recoveries; billed per cycle, not per case"],
    [{ t: "White-label", b: true }, "8–14% net to VOLTA", "Partner owns the client; near-zero acquisition cost (accounting model in Section 32)"],
  ],
  [1900, 3560, 3900],
));
push(spacer(60));
push(P("No setup fee, no charge for value merely identified, no fee on rejected or abandoned cases, no fee for credits already approved before VOLTA’s involvement, and no fee until the credit appears — and survives — in the seller’s own records."));
push(H3("Getting paid — the existential problem, and the honest answer"));
push(callout([
  PR([B("First, the hard truth: there is no custody, ever.  ", { color: RED }), T("The recovered credit lands in the seller’s "), B("own"), T(" Mercado Pago balance through Mercado Livre’s internal reconciliation; it never flows through a VOLTA-controlled rail. Payment-split (Mercado Pago / Asaas / Iugu) only divides a charge the splitting platform itself settles — ML’s payout is not such a charge — so "), B("source-capture is structurally impossible"), T(" and is ruled out, not architected around. Every collection mechanism is therefore a downstream pull or charge against the seller after the money has landed.")], "F7ECEC", RED),
]));
push(P("Because no single downstream mechanism is guaranteed, collection stacks four independent layers, so the failure of any one does not mean non-payment:"));
push(
  numItem("1.", [B("A pull rail, made an access-gate precondition. "), T("A variable-value Pix Automático mandate authorized at onboarding (Section 26) with a high payer-approved ceiling (sized ~3× the seller’s expected maximum fee), fired the "), I("same settlement day"), T(" the recovered credit hits the seller’s balance — before the nightly sweep to their bank — using the BCB-mandated retry ladder. Operated through a licensed PSP (Asaas / Iugu); VOLTA cannot be a Pix Automático receiver directly.")]),
  numItem("2.", [B("A legal rail. "), T("The seller contract makes each confirmed fee a "), I("título executivo extrajudicial"), T(" via a pre-agreed "), I("confissão de dívida líquida e certa"), T(" (CPC art. 784) plus a "), I("mandato em causa própria"), T(", so a stiff triggers fast execution, not a slow ordinary lawsuit (Section 33).")]),
  numItem("3.", [B("Staged trust. "), T("Fees below a threshold auto-pull; fees above it are invoice-first (NFS-e + short net term) backed by the título.")]),
  numItem("4.", [B("A white-label remit channel. "), T("A partner (accountant / ML agency) who already bills the seller — and often holds the login — collects and remits, moving VOLTA’s collection risk to a party with existing leverage.")]),
);
push(P("Attribution is settled contractually, not by a per-case causality claim: a fee is owed only on an “Attributable Credit,” defined by four booleans both sides sign at onboarding (Section 29). Billing fires only on money confirmed collected and matured past the settlement hold-back window, so VOLTA never bills a credit that later reverses."));
push(callout([
  PR([B("Bill per cycle, never per case.  ", { color: GREEN }), T("The fixed cost of a fiscal note plus a payment pull (~R$2.5–3.5 per charge) makes any standalone sub-R$30–50 case value-destructive. Billing bundles one NFS-e and one Pix pull per seller per cycle, above a per-invoice minimum (~R$49). "), B("Residual, stated honestly: "), T("a determined seller can cancel the mandate up to 23:59 the day before a debit, approve a low ceiling, or sweep the balance first — forcing VOLTA to execute the título. No instrument gives custody over funds sitting in the seller’s own account. This is the irreducible floor of the model.")]),
]));

/* 7 */
push(H1("7.  Go-To-Market & the Expansion Ladder"));
push(P("The wedge is an export-first compatibility + leakage scan: the seller uploads reports (or connects read-only), VOLTA validates the export’s integrity, and shows a hard number. Only after the seller sees verified evidence do they sign and connect OAuth. A qualification filter runs first (leakage above floor, retrievable NF-e, non-Model-6, standing) so effort is never spent on accounts that cannot be served or paid."));
push(P("The expansion ladder is deliberately Brazil-bounded, and each rung is earned by the one below paying for itself:"));
push(
  numItem("1.", [B("Deeper penetration — "), T("both recoverable pools (Full + Mercado Pago) worked from one connection; the Mercado Pago pool — chargebacks wrongly debited, commission/fee overcharges, held funds — may be under-weighted in v2 and is a first-class target.")]),
  numItem("2.", [B("White-label distribution inside Brazil — "), T("agencies, ERPs, accountants, and 3PLs bring whole portfolios. This is the scalable acquisition engine and the only economic path to the tail; direct sales mainly produces the proof that closes partners. Conversion is modelled per channel and per tier — never one blend. The remittance/tax model is fixed in Section 32.")]),
  numItem("3.", [B("Adjacent Brazilian marketplaces, only behind the KISS gate — "), T("Amazon Brazil, Shopee, or Magalu are admitted only as a new connector emitting into the same spine, reusing the same rules and dashboards, and only if the new source keeps minutes-per-case within ~20% of the Mercado Livre baseline.")]),
);

/* 8 */
push(H1("8.  Competitive Moat"));
push(
  bullet([B("vs. doing nothing: "), T("the seller’s money silently evaporates and claim windows close; every unaudited month finances the platform’s errors at face value.")]),
  bullet([B("vs. an in-house analyst: "), T("a hire reconciles one account slowly, with no cross-seller pattern library and no infrastructure. VOLTA is leverage, not headcount.")]),
  bullet([B("vs. a consultancy: "), T("consultants deliver slides; VOLTA delivers credited BRL and invoices only after the money shows up and stays.")]),
);
push(P("The durable moat is the truth machine plus the accumulating library of which case types the platform actually pays, net of what it pays spontaneously. Honestly stated: the software is clonable, Brazil already has adjacent conciliação/ERP tooling (Koncili, Citel, Mercado Pago’s own tools, Hunter HUB, Nubimetrics), and “no credible competitor” is too strong — no dominant contingency-recovery specialist appears to exist yet, but the category is not empty. The moat is earned by being first, fast, correct, and compounding attribution data — not by secret technology."));

/* 9 */
push(H1("9.  Risks & the Pre-Mortem"));
push(P("Airtight means naming how this dies. The pre-mortem below is written as if it is 18 months from now and VOLTA has failed; each row carries the earliest leading indicator (ideally already a dashboard tile) and the mitigation or kill-decision."));
push(tbl(
  ["Failure narrative", "Earliest leading indicator", "Mitigation / kill-decision"],
  [
    [{ t: "Pool erosion", b: true }, "Spontaneous-resolve rate per rule climbs; treated-vs-delayed gap shrinks", "Pivot to auditing payout correctness + the Mercado Pago pool; kill rules whose incremental value decays"],
    [{ t: "Margin too thin (F1 fails)", b: true }, "Net-attributable BRL/seller below the cost-to-serve floor for the median decile", "Hold anchors; do not open the tail; the pre-registered floor (≥ ~0.4% net-attributable) blocks scaling"],
    [{ t: "Access revoked / app banned", b: true }, "Rejection-rate drift; ToS version-diff; 429 rate rising", "Read-only API footprint; manual/copilot filing; per-app caps; route filing to white-label logins; diversify"],
    [{ t: "Systematic false positive", b: true }, "FP rate per Rule Card; share of sellers with any invalid case", "Fail-closed on low coverage; canary ratchet on every rule-version; tier-dependent FP tolerance"],
    [{ t: "Collection / clawback spiral", b: true }, "Reversal rate on collected fees; mandate ceiling-breach + cancellation rate", "Settlement hold-back sized past the measured clawback window; clawback reserve; cap/split large fees"],
    [{ t: "Founder key-person", b: true }, "Bus factor = 1 on the ML relationship, tax judgment, case intuition", "Shamir key escrow + runbooks + a backup approver (Section 34); the ML relationship stays the true concentration"],
    [{ t: "Go/no-go becomes theatre", b: true }, "Gate approaching with sunk cost; no failure branch", "Pre-committed kill/pivot/refund rule + an external gatekeeper who gates the money (Section 30)"],
  ],
  [2500, 3360, 3500],
));
push(spacer(80), H3("The blunt verdict"));
push(P("The engineering is strong, but strong architecture around an unproven core is over-engineering, not a moat. Do not build the company until the pilot proves the recovery is real, large, recurring, and causally VOLTA’s, at a margin that survives real cost. If it does, the ambitious version is justified; if not, that answer was bought for the price of a 45-day pilot instead of a platform."));

/* ================= PART II — THE TRUTH MACHINE ================= */
push(...partBanner("Part II", "The Truth Machine"));

/* 10 */
push(H1("10.  Design Principles & the Corrected Invariants"));
push(
  numItem("1.", [B("Code computes every number — tightened. "), T("Every centavo, quantity, deadline, and fee is computed in versioned code as integer centavos, from operands that are only (i) platform-API values or (ii) code-parsed NF-e XML. Any value an LLM extracts from a degraded scan is quarantined as low-confidence and never becomes a case number without code or human confirmation.")]),
  numItem("2.", [B("Authorization is two different things. "), T("“A human authorizes every external action” was doing two jobs: an accountability signature and error-catching review. Automation keeps the first and silently loses the second. In the pilot the authorization is also a real review, and it only graduates to a standing policy after the data shows the review caught nothing.")]),
  numItem("3.", [B("One spine, three consumers. "), T("A single append-only event spine feeds the Workbench, the Dashboards, and the Automation — nothing else is a “system.”")]),
  numItem("4.", [B("Detection is read-only; action is deliberate. "), T("VOLTA’s entire API footprint is read-only. No VOLTA software ever writes to the platform; every external filing is a human acting in the seller’s own session (Section 15). This severs detection from action and takes ban-risk to near-zero in the pilot.")]),
  numItem("5.", [B("Fail closed, not open. "), T("A missing data source degrades to “cannot surface / cannot bill,” never to “assume complete.”")]),
  numItem("6.", [B("Earn autonomy, gate by gate. "), T("Instrumentation is built from day one; autonomy is granted one action-class at a time, only after a labeled clean-outcome dataset and a canary ratchet say it is safe.")]),
);

/* 11 */
push(H1("11.  Architecture — One Spine, Three Consumers"));
push(P("VOLTA is one Postgres, one Python/FastAPI codebase, one deployable image, in the São Paulo region (sa-east-1). Everything hangs off a single append-only, hash-chained event spine — a small set of record families, each with a clear job, all in one database."));
push(H3("Record families (one Postgres)"));
push(tbl(
  ["Family", "Holds", "Pilot?"],
  [
    [RN("raw_observation"), "Every webhook / API / report / upload, unmodified, hash-chained", "Yes"],
    [RN("source_document"), "NF-e XML, reports, evidence — with content hashes", "Yes"],
    [RN("canonical_event"), "Normalized operational + financial facts", "Yes"],
    [RN("journal_entry"), "Expected and actual monetary entries (Section 12)", "Yes"],
    [RN("match_allocation"), "Partial / split / combined / reversed reconciliation", "Yes"],
    [RN("case / case_event"), "Recovery lifecycle + decisions (Section 13)", "Yes"],
    [RN("experiment_assignment"), "Immediate-vs-delayed causal-test assignment", "Yes"],
    [RN("command / action_attempt"), "Proposed + attempted external actions", "Deferred*"],
    [RN("outbox_message"), "Approved communications awaiting dispatch", "Yes"],
    [RN("work_session"), "Human effort measurement (idle-capped)", "Yes"],
    [RN("billing_event"), "Attribution, notice, invoice, charge, reversal", "Yes"],
    [RN("audit_checkpoint"), "Signed external integrity checkpoint", "Deferred*"],
  ],
  [2700, 5060, 1600],
));
push(spacer(50));
push(PR([{ t: "*Deferred = ", b: true }, "in the pilot, external submission is a guarded function with an idempotency key and a recorded human approval (not yet a full command bus), and integrity is a key-independent hash chain plus point-in-time recovery (KMS-signed external checkpoints add non-repudiation later — Section 23). The schema keeps the seed columns now so nothing is re-architected later."].map(x => new TextRun({ size: 20, color: GREY, ...x })), { spacing: { after: 140 } }));
push(H3("Standard event envelope"));
push(PR([T("Every event carries: "), ...runsFrom(CODE("event_id, tenant_id, seller_id, source_system, external_resource_id, source_schema_version, rule_version, occurred_at, observed_at, ingested_at, correlation_id, causation_id, idempotency_key, payload_hash, previous_hash, supersedes_event_id")), T(". The distinction between "), ...runsFrom(CODE("occurred_at")), T(" and "), ...runsFrom(CODE("observed_at")), T(" is essential: late-arriving and corrected reports must not produce false deadlines or rewrite historical dashboards.")], { spacing: { line: 340, after: 160 } }));
push(H3("The three consumers"));
push(tbl(
  ["Consumer", "What it is", "Rule"],
  [
    [{ t: "1 · Workbench", b: true }, "HTMX + Jinja + Tailwind, server-rendered. Reads projections; writes human-approval events.", "Never computes money; records the human decision"],
    [{ t: "2 · Dashboards", b: true }, "SQL materialized views over the spine (Section 19), rendered as in-app tiles.", "Only displays code-computed centavos; shows coverage + freshness"],
    [{ t: "3 · Automation", b: true }, "Event-triggered + scheduled jobs with the Section 17 guards.", "Drafts and sends the routine; gates the irreversible"],
  ],
  [1900, 4760, 2700],
));
push(spacer(50));
push(P("Deployment is one image with process roles (web, webhook_receiver, worker, scheduler). A single scheduler lease (pg_cron, verified to fire once cluster-wide) prevents APScheduler double-firing inside every web replica. Splitting the roles onto separate machines is deferred until measured queue lag demands it."));

/* 12 */
push(H1("12.  Reconciliation — a Journal, Not a Subtraction"));
push(P("v2’s “expected − matched = residual” is too weak for how money behaves: credits arrive partial, split across movements, combined across cases, posted under a different reference, net of fees, duplicated, or reversed later. v3 replaces the single residual with an immutable recovery journal and many-to-many match allocations."));
push(
  bullet([T("An "), ...runsFrom(RN("expected_receivable")), T(" entry and a "), ...runsFrom(RN("platform_money")), T(" entry are both immutable journal rows.")]),
  bullet([T("A "), ...runsFrom(RN("match_allocation")), T(" connects some or all of one money movement to one or more expected receivables — supporting partial, split, and combined credits.")]),
  bullet([T("A reversal is a "), B("new reversing entry"), T(", never a mutation of the original.")]),
);
push(H3("Hard invariants (property-tested)"));
push(
  bullet([T("Σ allocations against a money entry ≤ that money entry; Σ allocations against an expected entry ≤ that expected entry.")]),
  bullet([T("No allocation is billed twice; a reversed credit reduces attributable and billable value.")]),
  bullet([T("Every invoice line traces to one or more allocations; every customer-visible amount traces to a source.")]),
);
push(P("Each amount carries an explicit basis, because “qty × NF unit price” is not universally right — a SKU may have several NF-e purchase lots at different costs. Every Rule Card states whether the basis is specific-lot, weighted-average, FIFO approximation, platform reference value, or a contractual fallback. The pilot implements only the bases its rules actually use."));

/* 13 */
push(H1("13.  The Case State Machine"));
push(P("States that v2 blended are now explicit, so “the platform approved an amount” is never confused with “a credit landed,” and “a credit landed” is never confused with “it is billable.”"));
push(PR([...runsFrom(CODE("detected → cooling_off → evidence_complete → verified → experiment_assigned → approved_for_action → submitted → platform_approved → credited → attribution_confirmed → billable → invoiced → charged → collected"))], { spacing: { line: 340, after: 60 } }));
push(PR([T("with side-paths "), ...runsFrom(CODE("reversed")), T(" and "), ...runsFrom(CODE("closed")), T(". A credit becomes "), B("billable"), T(" only after "), ...runsFrom(CODE("attribution_confirmed")), T(" AND the settlement hold-back has matured. The pilot collapses this to the ~8–10 causally load-bearing states.")], { spacing: { line: 340, after: 140 } }));
push(callout([
  PR([B("Cross-source verification gate.  ", { color: GREEN }), T("A case cannot pass "), ...runsFrom(CODE("verified")), T(" while quantity or value disagree across the NF-e XML, the marketplace record, and the Mercado Pago movement. Self-contradictory evidence is held for review — this alone stops a large class of confidently-wrong claims.")]),
]));

/* 14 */
push(H1("14.  Recovery Rules & Rule Cards"));
push(P("A rule never enters code from a one-line table row. Each rule is a versioned Rule Card carrying: the business hypothesis; required sources and minimum data coverage; the canonical joins; known exclusions and benign patterns; the cool-off rule; the amount basis; the deadline basis; the evidence checklist; the action path and its authorization level; experiment eligibility; the expected spontaneous-resolution behaviour; failure modes; synthetic and anonymized regression fixtures; a precision threshold and a false-negative audit method; promotion and demotion triggers; billing eligibility; and an owner."));
push(tbl(
  ["Rule (Rule Card)", "Reconciliation (join)", "Amount basis", "Deadline"],
  [
    [RN("APPROVED_CREDIT_NOT_RECEIVED"), "approved claims × MP/billing on claim_id", "approved − posted", "approval +90d"],
    [RN("CHARGEBACK_DEBIT_PROTECTION_MET"), "chargeback debits × protection eligibility (MP pool)", "wrongly-debited amount", "debit +window"],
    [RN("FULL_DAMAGE_NO_MATCHED_CREDIT"), "warehouse-damage op × credit on inventory+movement", "qty × lot/ref basis", "event +180d"],
    [RN("NEGATIVE_STOCK_AUDIT_UNRESOLVED"), "negative adjustment × sales × returns × credit", "adj − offsets", "event +60d"],
    [RN("INBOUND_QUANTITY_DIFFERENCE"), "declared × check-in on shipment+sku vs NF-e qty", "delta × NF unit", "receipt +30d"],
    [RN("RETURN_CONDITION_REVIEW"), "returns × refunds × restock on order/claim", "refunded, not restocked", "return +30d"],
    [RN("DUPLICATE_OR_UNMATCHED_DEDUCTION"), "billing × orders × inventory on order+fee_type", "fee amount", "charge +180d"],
  ],
  [2700, 3560, 1700, 1400],
));
push(spacer(70));
push(P("The pilot starts with two or three of the highest-value, highest-confidence rules — including one deterministic Mercado-Pago-pool rule (chargeback-debit-with-protection or a commission/freight overcharge), because a pure-arithmetic financial-pool rule is the cleanest first proof and does not depend on the murkier Full write path. A rule is only built when all three kill conditions clear: the source is ingestable, its completeness is measurable, and there is an administratively permitted path to act (Section 26)."));
push(H3("Outcome taxonomy and recall"));
push(P("A valid case rejected by the platform is not necessarily a false positive. Outcomes are classified precisely (valid-credited, valid-partially-credited, valid-platform-rejected, valid-auto-resolved, invalid-logic, invalid-source-data, duplicate, insufficient-evidence, policy-ineligible, deadline-expired, seller-declined, unknown). Precision is measured among reviewed cases; recall is estimated by periodically sampling events that produced NO case — without that negative sampling, the system could optimise precision by finding almost nothing."));
push(callout([
  PR([B("Shadow, canary, and the allocation engine.  ", { color: GREEN }), T("New rule-versions launch in shadow until precision clears the bar. v3 extends the same discipline to the "), B("allocation and fee-basis engine"), T(" — “code computes every centavo” is only safe if that code is itself shadow-tested and canary-gated. The first N auto-eligible cases of any rule-version require human confirmation and must clear clean before the auto-cap lifts.")]),
]));

/* 15 */
push(H1("15.  Delegated Authority & the Action Path"));
push(P("“A human approves everything” and “billing runs automatically” are both true only under an explicit authority model. Actions are classified by level, and every automatic action must cite the versioned policy that authorized it:"));
push(tbl(
  ["Level", "Example", "Authorization"],
  [
    [{ t: "0 · Internal", b: true }, "Reconciliation, scoring, dashboard refresh", "Automatic"],
    [{ t: "1 · Routine / reversible", b: true }, "An approved-template status email", "Pre-approved policy"],
    [{ t: "2 · Customer-visible", b: true }, "Document request; non-material reply", "Named human until graduated"],
    [{ t: "3 · Financial / claim", b: true }, "Case submission; fee above threshold", "Named human; optional second approver"],
    [{ t: "4 · Prohibited", b: true }, "Refund endpoint; credential impersonation; unsupported filing automation", "Never executed by VOLTA"],
  ],
  [2100, 4460, 2800],
));
push(spacer(60));
push(callout([
  PR([B("The action path that also solves ban-risk.  ", { color: GREEN }), T("VOLTA’s only API footprint is "), B("read-only"), T(" — everything the matcher needs comes from read scopes. No VOLTA software ever writes to the platform. Every filing is a "), B("submission copilot"), T(": VOLTA prepares the exact evidence package and text; the authorized human opens the marketplace page in the seller’s own session, a guided workflow fills the permitted fields, and the human performs the final click; VOLTA records the receipt. No credential-sharing, no headless impersonation. This severs detection from action, so there is no automated cross-account signature for the platform to flag, and it makes the unverified programmatic-submission ToS irrelevant to the pilot. Per-app and per-account pacing caps, plus quality-gating (only high-confidence, well-evidenced, human-varied claims filed), keep the footprint benign.")]),
]));

/* 16 */
push(H1("16.  AI Guardrails"));
push(P("AI proposes, code computes, a human approves — enforced by architecture, not instruction. The model may produce a template ID, a reason code, evidence references, a missing-document classification, an internal summary, and Portuguese prose for approved slots. It may never produce a monetary basis, an eligibility decision, a submission command, a destination account, a deadline, or an unbounded recipient list."));
push(
  bullet([B("Numbers cannot enter through the model — including in words. "), T("A digit-only scrubber is not enough: a model can write “mil quatrocentos e noventa reais.” The external-message assembler is structurally unable to accept a numeric field from the model; every amount and date is a code-rendered token, and a validator rejects both digits and spelled-out Portuguese cardinals in free slots.")]),
  bullet([B("Prompt injection is treated as real. "), T("Marketplace messages and uploaded documents are untrusted; their text never routes into action-selection or into the approval-summary the human relies on. The AI worker has no cross-tenant retrieval, no arbitrary-query tool, no external-action tool, and no secret access.")]),
  bullet([B("Drift is watched in production. "), T("Model and version are pinned; golden-set evals (numeric-leak rate must be zero) run continuously in production, not only in CI, and alert on any version change.")]),
);

/* 17 */
push(H1("17.  Automation Safety — the New Money-Out Actions"));
push(P("Near-full automation removed the human who used to silently catch errors, and created irreversible money-OUT actions the human-scale design never had. Each gets a specific, cheap guard — the price of letting anything run unattended."));
push(tbl(
  ["New risk (human circuit-breaker gone)", "Guard"],
  [
    ["A bad rule-version mis-fires across every seller at once", "Per-rule-version canary ratchet (first N human-confirmed) + a global and per-rule daily volume circuit-breaker"],
    ["Pix Automático debits the seller’s own account on a false premise", "Settlement hold-back + 1:1 fee↔credit map + suppress any debit on ambiguity; cap/split large fees"],
    ["Automated dunning fires at a paying customer wrongly", "Suppress dunning on any account/case with an open exception; deterministic-from-confirmed-credit only"],
    ["Mass NFS-e replicates one bug into thousands of legal documents", "Issue every NFS-e to an internal pending state first; reconcile fee-as-%-of-credit against the locked ledger; hold outliers"],
    ["Charge succeeds but NFS-e fails (money taken, no invoice)", "Charge↔NFS-e saga with a charged_awaiting_nfse state that alerts past SLA; never silently leave it"],
    ["Coverage % is computed but unread; gaps look complete", "Fail-CLOSED: no surfacing, submission, or billing while inputs are below a coverage threshold; alert on the SLO"],
    ["Late / out-of-order fetch regresses a newer state", "Monotonic guard: append the raw observation; advance canonical state only when occurred_at/version ≥ stored"],
  ],
  [4360, 5000],
));

/* 18 */
push(H1("18.  Metrics & the Return-Efficiency North Star"));
push(P("Because code owns every number, metrics are deterministic SQL projections off the one spine — never LLM-estimated. v3 changes the north star. “Per human minute” trends toward infinity as automation removes labour: an auto-cleared case adds credit to the numerator and nothing to the denominator, so the metric reads best exactly when a rule stops needing humans, regardless of whether it makes money. A metric you have to floor cannot steer."));
push(callout([
  PR([B("North star: net-attributable recovered BRL, per seller and per R$ of fixed cost.  ", { color: GREEN }), T("It stays meaningful at zero labour, cannot be gamed by automating a step, and rewards money, not activity. Attributable = credited − expected-spontaneous − reversals − pre-existing/duplicate.")]),
]));
push(P("Three distinct truths are tracked. Note: the per-human-minute ratios below are read only as bounded health metrics alongside the absolute net-attributable figure — they are diagnostics, never efficiency objectives, and minutes-per-case is the early-warning tripwire for the “minutes don’t collapse” risk."));
push(tbl(
  ["Truth", "Metric (how it is read)"],
  [
    ["Product truth", "Incremental net recovery per eligible GMV (is the money there and causally ours?)"],
    ["Operating truth", "Net-attributable BRL per active human minute — a bounded health metric, read only beside the absolute"],
    ["Business truth", "Contribution margin per seller and per fully-loaded human hour (does it pay?)"],
  ],
  [2600, 6760],
));
push(spacer(60));
push(P("Guardrail metrics sit beside the north star: invalid seller-visible case rate, missed irreversible deadlines, unauthorized external actions, credit-reversal rate, invoice-dispute rate, data coverage by seller and source, platform complaint/suspension rate, churn after a submitted case, and P50/P90 active minutes per case. Active minutes come from lightweight work_session events with automatic idle caps — not from the spacing between case events."));

/* 19 */
push(H1("19.  Dashboards — Running the Business on Glass"));
push(P("The business lives and dies by its dashboards, so all eight are in from day one — but as read-projections over the verified spine, never as a second system. Every tile reads the one Postgres; nothing computes money in the browser or the LLM; every money tile shows its own data-coverage % and freshness; and “The Number” always renders as four figures, never as one collectible sum. Only two dashboards are load-bearing for the go/no-go (Operations and Owner/Experiment); the other six ship on day one as named SQL views, with full tile UIs built when a consumer asks. There is no separate BI stack."));
push(tbl(
  ["Dashboard", "Load-bearing?", "Key tiles (all coverage- and freshness-stamped)"],
  [
    [{ t: "1 · Owner / Experiment", b: true }, [{ t: "Yes", b: true, color: GREEN2 }], "North star (net-attributable per seller & per R$ fixed cost); treated-vs-delayed gap; collected success fees (run-rate); cash collected vs outstanding; go/no-go gate status"],
    [{ t: "2 · Operations", b: true }, [{ t: "Yes", b: true, color: GREEN2 }], "Queue by stage; deadline-risk swimlane; minutes-per-case tripwire; cases awaiting human approval; coverage SLOs"],
    [{ t: "3 · Recovery Funnel", b: true }, "View day-one", "candidate→verified→submitted→collected value & conversion, by rule and pool; spontaneous-rate by category"],
    [{ t: "4 · Financial / Billing", b: true }, "View day-one", "Fees invoiced/collected/outstanding; reversal & clawback rate; per-invoice economics; NFS-e vs charged reconciliation"],
    [{ t: "5 · System Health", b: true }, "View day-one", "Ingestion lag & coverage per source; webhook signature health; token status; gap detection; deadline-miss risk"],
    [{ t: "6 · Client Health", b: true }, "View day-one", "Recovered-to-date; open cases; pending doc requests; churn-risk; per-seller (not per-case) support minutes"],
    [{ t: "7 · Partner (white-label)", b: true }, "View day-one", "Recovered value across a partner’s sellers; payout owed; branded statement export; tenant-scoped"],
    [{ t: "8 · Growth", b: true }, "View day-one", "Leads; scans run; scan→signed by channel & tier; CAC; activation time; cohort retention"],
  ],
  [2100, 1500, 5760],
));
push(spacer(60));
push(P("Dashboards only display. Every external action they surface routes through the human-approval gate and the append-only log, never the tile itself. Cheap second-derivative and cohort tiles (spontaneous-rate and per-case yield by category and onboarding cohort, rejection-rate, FP-rate per Rule Card) are added as read-projections because they are what steer rule and tier decisions."));

/* 20 */
push(H1("20.  Failure-Safe Ingestion & Jobs"));
push(P("A webhook is a notification, not truth. The flow is: receive → verify the signature → store the raw envelope → acknowledge fast → enqueue a canonical fetch → retrieve → normalize → deduplicate → project → reconcile. VOLTA expects duplicates, missed notifications, out-of-order delivery, retries, late reports, and temporary API inconsistency."));
push(
  bullet([B("Mercado Pago webhooks are signed "), T("(x-signature, ts + v1 HMAC); unsigned or invalid events are rejected, and source_news=webhooks avoids duplicate legacy IPN delivery. Subscribe to payments, merchant_order, and chargebacks.")]),
  bullet([B("Idempotency on both sides "), T("— ingestion and external submission. A client-generated key is sent to the platform where supported; on an ambiguous outcome the worker enters submitted_unknown and reconciles-by-read before any retry.")]),
  bullet([B("Coverage as a first-class signal "), T("— per-source high-water marks, backfills, gap detection, per-seller coverage; Mercado Pago reports chunked at 60 days per pull and stitched.")]),
  bullet([B("Adaptive limits, not hardcoded ones "), T("— Mercado Livre publishes dynamic quotas, so exponential backoff with jitter on 429 and per-seller queues; refresh tokens are single-use and rotating, so refreshes are single-flighted under a per-tenant lock and the newest token stored atomically.")]),
  bullet([B("Evidence has a fetch deadline. "), T("For returns, NF-e XML must be captured within the SEFAZ availability window (a manifestação do destinatário / “Ciência da Operação” is registered under an e-CNPJ procuração so the full XML is pulled and stored before SEFAZ purges it — VOLTA treats SEFAZ as ephemeral, its own store as durable).")]),
);

/* 21 */
push(H1("21.  Security, Tenant Isolation & LGPD"));
push(P("Trust is the product: a seller is handing VOLTA a live pipe into the data about their money. Every control exists to kill the “can I trust you?” objection before value is even shown."));
push(callout([
  PR([B("RLS alone does not isolate tenants.  ", { color: AMBER }), T("Supabase’s service_role carries BYPASSRLS, and a table owner bypasses RLS unless FORCE ROW LEVEL SECURITY is set. v3: run each non-web process as a dedicated least-privilege, non-owner, non-BYPASSRLS role; scope every unit of work with an in-transaction tenant claim (SET LOCAL); set FORCE ROW LEVEL SECURITY on tenant tables; add a cross-tenant leak test to CI. For the single-seller pilot the cheap guard is never touching tenant data via service_role; full RLS + advisory-lock append is a hard requirement before seller #2.")], "F7EFE0", AMBER),
]));
push(
  bullet([B("Token vault + PII minimization: "), T("per-tenant envelope encryption; short-lived tokens; one click revokes access and pauses jobs; buyer identifiers become a pseudonymous reference at ingestion, and reports and prompts see only that reference.")]),
  bullet([B("Backups in two plans: "), T("Supabase database backups exclude Storage-API objects, so evidence and fiscal files get a separate versioned backup to an independent bucket; PITR is enabled (a paid plan from day one); a restore is drilled quarterly and the restored object hashes reconciled.")]),
);
push(H3("LGPD, operationalized before the first fetch"));
push(
  bullet([B("Encarregado (DPO) appointed and publicly published "), T("with a contact channel, because VOLTA holds live ML/MP data — Art. 37 processing register (ROPA) is mandatory now, not “before scale.”")]),
  bullet([B("Lawful basis + DPA + consent per pilot seller, "), T("and the ANPD Resolution 19/2024 standard clauses incorporated for the international transfer to US processors (Resend email, Anthropic inference). The seller promise is precise: “the primary database is in Brazil, and every processor, transfer mechanism, retention period, and access path is disclosed and contractually controlled.”")]),
  bullet([B("Incident-response playbook "), T("with an explicit clock (report to ANPD and affected parties within the required window, tracked from detection), a breach register, and credential-rotation-first containment.")]),
  bullet([B("A retention matrix, not blanket five years: "), T("fiscal artifacts kept for the statutory period under the legal-obligation basis (LGPD arts. 7 II, 16 I); non-fiscal personal data (buyer identifiers, prompts, logs) minimized and deleted earliest; a data-subject-deletion request destroys the identity mapping and non-fiscal PII while retaining the non-identifying fiscal and audit facts the law requires. Buyer PII inside NF-e XML is handled by this matrix, never blindly deleted.")]),
);

/* 22 */
push(H1("22.  Billing & Collections Subsystem"));
push(P("The fee is a state machine that never gets ahead of the money: attribution_confirmed → (hold-back matures) → billable → statement → seller review window → NFS-e → charge → collected, with side-paths for reversal and charge-failure. It integrates a fiscal API to issue the NFS-e and a payment processor to debit the mandate."));
push(
  bullet([B("Charge on collected-and-matured, never on approval. "), T("The settlement hold-back is sized to EXCEED the clawback window measured in the pilot, not guessed — so VOLTA rarely bills a credit that later reverses.")]),
  bullet([B("NFS-e is issued only on confirmed fee settlement, "), T("competência = the settlement month, so tax never precedes cash. A post-billing clawback triggers an NFS-e cancelamento/substituição runbook and a reversing billing entry.")]),
  bullet([B("Bundle per cycle, above a per-invoice minimum. "), T("One NFS-e and one Pix pull per seller per cycle.")]),
  bullet([B("An invoice-notice window "), T("— attribution → statement → a 48–72h dispute window → NFS-e → charge — so new accounts do not auto-debit their first fee; trusted accounts graduate via a documented policy.")]),
  bullet([B("A fallback dunning ladder "), T("for when the mandate is unavailable/cancelled/capped: reminders → suspension of new submissions → formal notice → protesto / execution of the título (Section 33). Receivables are aged and a bad-debt provision is taken in the monthly close (Section 32).")]),
  bullet([B("Fiscal reality for 2026. "), T("NFS-e Nacional is live; the Emissor Nacional becomes mandatory for Simples ME/EPP from 1 September 2026. VOLTA uses a provider adapter (Focus NFe / PlugNotas) behind an internal interface, stores every tax identifier as a string with CNPJ check-digit validation, versions the NFS-e schemas, and runs homologation + production contract tests. (The exact DANFSe-generation path and any deprecation timeline is a Phase-1 item to confirm with the provider, not an assumption.)")]),
);
push(P("Every fee row is immutable and traces to the confirming Mercado Pago movement, the matched allocation, the rule-version, and the approval — so any dispute is answered by replay. Billing is not “done” until the pilot has run one real credit → statement → valid NFS-e → successful charge, plus one failed charge + retry and one simulated reversal + fee correction."));

/* 23 */
push(H1("23.  Audit & Integrity"));
push(P("Day one: an append-only hash chain where each entry embeds the prior hash, so anyone can verify the chain WITHOUT any key — this decouples audit readability from key custody, so a lost signing key never makes the history unreadable. The append is serialized per tenant (an advisory lock allocates the next sequence, reads the chain head, and writes the event and new head in one transaction) so two concurrent workers cannot fork the chain. Point-in-time recovery and a separate versioned evidence-object backup complete the day-one picture."));
push(callout([
  PR([B("Deferred to a named hardening milestone (first dispute, first non-founder operator, or second tenant): ", { color: GREEN }), T("KMS-signed external Merkle checkpoints stored outside the database and verified daily. They add non-repudiation against a privileged insider rewriting history — a real but not-yet-present threat. A future dispute then has a defensible path: invoice → fee basis → allocation → credited movement → case → rule-version → canonical event → raw report → file hash → signed checkpoint.")]),
]));

/* 24 */
push(H1("24.  Release Engineering for Money Logic"));
push(P("Code generation is fast now, which makes the release gate more important, not less. Any change touching monetary basis, matching, eligibility, deadline, attribution, billing, or tenant scoping requires: a versioned rule or policy; two-person review; unit and property tests; replay against the historical regression corpus; a case-level before/after diff; shadow deployment; measured precision; and an explicit promotion event."));
push(P("The critical invariants are property-tested, not hoped for: no source movement is allocated beyond its amount; no expected amount is recovered beyond its amount; no credit is billed twice; no tenant reads or writes another tenant’s data; no external action exists without current authority; no action executes after its authorization expires; no correction deletes prior history; every customer-visible amount traces to a source; every billable amount traces to an attributable allocation. A red-team scenario pack (duplicate/out-of-order events, token expiry mid-ingest, partial/split/reversed credits, crash-after-submit, seller-revokes-mid-dispatch, restore-and-reverify) must pass before any real external action is enabled."));

/* 25 */
push(H1("25.  The KISS Stack + What We Deliberately Do Not Build Yet"));
push(tbl(
  ["Layer", "KISS choice", "Deferred / cut"],
  [
    ["Language + API", "Python 3.12 + FastAPI, one deployable image", "Microservices"],
    ["Database + spine", "PostgreSQL via Supabase (sa-east-1)", "Any second datastore; a warehouse"],
    ["Storage", "Supabase Storage + separate versioned evidence backup", "—"],
    ["Queue + scheduler", "In-Postgres queue + single scheduler lease (pg_cron)", "Redis until real burst load; 4-machine split until CPU demands"],
    ["Workbench + dashboards", "HTMX + Jinja + Tailwind tiles", "A separate frontend build; a BI stack; Metabase until an analyst needs it"],
    ["LLM", "Anthropic API, template-slot outputs", "Any model with money authority"],
    ["Comms", "Transactional email (Resend), versioned templates", "A marketing-automation platform"],
    ["Fiscal + payments", "Provider adapter (Focus/PlugNotas) + PSP (Asaas/Iugu/Pix)", "Direct municipal integrations; card rails until needed"],
    ["Deploy", "One container (Fly.io / Render, GRU)", "Kubernetes; multi-region"],
  ],
  [2000, 3760, 3600],
));
push(spacer(60));
push(callout([
  PR([B("Deferred to explicit unlock milestones (to keep the pilot KISS):  ", { color: GREEN }), T("KMS-signed Merkle checkpoints → first dispute / operator / second tenant; full RLS + advisory-lock append → second seller; the 5-level authority policy engine → first standing-automation class; the command bus → first non-human-clicked dispatch; the 4-process split → measured queue lag; DLQ replay tooling → first recurring failure class; unused allocation bases and the full state machine → when a rule needs them; the recall-sampling apparatus → after the first credit. "), B("Parked entirely: "), T("cross-seller benchmarking (premature), recovery-advance financing (a regulated-lender trap), and any paid standalone scan (a price gate in front of “The Number” kills the zero-downside conversion).")]),
]));

/* ================= PART III — VALIDATION ================= */
push(...partBanner("Part III", "Validation"));

/* 26 */
push(H1("26.  Phase −1: Platform Capability Proof (the Hard Gate)"));
push(P("Before implementing any recovery rule, VOLTA proves the required inputs, permitted actions, AND the collection mandate on one consenting live seller. This is a gate, not a research task alongside development. Each capability is GREEN (proven on a real account), PROVE (needs a live pull), or STOP (unavailable)."));
push(tbl(
  ["Capability", "What must be recorded"],
  [
    ["Seller / account type", "Full status; whether the account is CBT / Model-6 (403 on claim endpoints)"],
    ["Authentication", "OAuth grant, refresh, rotation (single-use), and revocation work for a delegated token"],
    ["Financial data path", "A delegated token returns THAT seller’s Mercado Pago reports (settlement/release), 60-day chunks stitched"],
    ["Operational data path", "Full stock movements and claims retrievable; historical lookback probed (default 15 days — how far back?)"],
    ["Evidence completeness", "Row counts reconciled against the seller’s own UI/export; coverage measurable; SEFAZ XML retrievable"],
    ["Collection mandate", [{ t: "A high-cap variable Pix Automático mandate is authorized via the PSP", b: true }, { t: " — a HARD precondition; no mandate, no service" }]],
    ["Action path", "Which actions are permitted for the read-only + copilot model under current ToS"],
    ["Policy basis", "Current primary documentation or written confirmation the workflow is permitted"],
  ],
  [2600, 6760],
));
push(spacer(60));
push(callout([
  PR([B("Kill conditions — do not build a rule unless all three are true.  ", { color: GREEN }), T("(1) the source can be ingested reliably; (2) its completeness can be measured; (3) there is an administratively permitted path to act. A rule with excellent arithmetic but no usable action path is analytics, not a recovery product.")]),
]));
push(callout([
  PR([B("Day-3 STOP condition.  ", { color: RED }), T("Stop the whole project if there is no administratively permitted path to convert a detected discrepancy into a landed credit — i.e. no sanctioned action path AND the guided-human copilot is prohibited or infeasible. Everything downstream assumes an action path exists.")], "F7ECEC", RED),
]));

/* 27 */
push(H1("27.  The Executable Pilot — Day-One Build Scope"));
push(P("The day-one build is the smallest system that makes the pilot trustworthy — no more. Honest timeline: the build begins on Day 10 and runs in parallel across roughly Days 10–40, with only the minimum core for the first cleared Rule Cards needed by Day 17 to start the RCT ramp — about four to six weeks of engineering in total for a competent solo engineer, layered onto the live pilot, not a clean pre-build. Do not promise a working truth machine “in days.”"));
push(tbl(
  ["Build (Days 10–40, core by Day 17)", "Deferred (with unlock)"],
  [
    ["Tenant/seller model; raw_observation + source-document hashes; canonical events", "KMS-signed external Merkle checkpoints → first dispute / operator / tenant"],
    ["Recovery journal + reversible match-allocations (only the bases the pilot rules use)", "Full RLS + advisory-lock append + cross-tenant tests → second seller"],
    ["Case state machine (~8–10 states) + cross-source verification gate", "5-level authority policy engine → first standing-automation class"],
    ["Idempotency on ingestion AND submission; reconcile-by-read on ambiguity", "Command bus / dispatcher → first non-human-clicked dispatch"],
    ["Recorded named-human approval before every external action (who/when/payload)", "4-process split → measured queue lag"],
    ["Settlement hold-back; one full credit→invoice→collection loop", "DLQ replay tooling → first recurring failure class"],
    ["Webhook-as-trigger; monotonic upsert; high-water marks; gap detection; coverage %", "Recall-sampling apparatus → after first credit"],
    ["Number-word scrubber; fail-closed on coverage; canary ratchet; charge↔NFS-e saga", "The 6 non-gating dashboard UIs → when a consumer asks (SQL views exist now)"],
    ["2–3 rules incl. one Mercado-Pago-pool rule; work_session events; the RCT harness", "Unused allocation bases + full state machine → when a rule needs them"],
    ["Operations + Owner/Experiment dashboards as UIs; the other 6 as SQL views", "Cross-seller benchmarking, financing, paid scan → parked"],
  ],
  [4680, 4680],
));

/* 28 */
push(H1("28.  The Kill-Test Sequence & 45-Day Plan"));
push(P("The pilot is ordered to falsify the business as cheaply and early as possible — hardest, cheapest-to-test questions first. The 45 days are needed for marketplace outcome latency and causal observation, not because the software takes 45 days to write."));
push(tbl(
  ["Window", "What it proves (or kills)", "Exit"],
  [
    [{ t: "Days −5..0 · Desk kill", b: true }, "No seller, no code: read ML/MP developer + partner ToS for whether third-party managed recovery is sanctioned; secure LGPD basis + DPA", "A permitted-in-principle path + signed pilot seller + mandate"],
    [{ t: "Days 1–3 · Capability Proof", b: true }, "Data ingestable + completeness measurable + a permitted action path + a live collection mandate, on one seller", [{ t: "HARD GATE; day-3 STOP if no action path", b: true }]],
    [{ t: "Days 4–9 · Historical kill block", b: true }, "Pure analysis on pulled history: ONE decision number — net-of-spontaneous recoverable BRL per seller/month, per pool, per decile", [{ t: "Clears the pre-registered ≥ ~0.4% net-attributable floor", b: true }]],
    [{ t: "Days 10–16 · Build pilot core", b: true }, "The day-one scope, only for Rule Cards that cleared the net-of-spontaneous gate and have a permitted path", "Identical fixtures → identical cases, amounts, provenance"],
    [{ t: "Days 17–32 · Controlled live RCT", b: true }, "Immediate vs safely-delayed (delay > measured spontaneous lag), every action human-approved", "Incremental BRL appears only in the treated arm"],
    [{ t: "Days 33–45 · Attribution + collection", b: true }, "One real credit → invoice → NFS-e → charge that actually CLEARS; failed-charge and reversal paths tested", "End-to-end proof, and willingness to PAY (not just authorize)"],
  ],
  [2500, 4560, 2300],
));

/* 29 */
push(H1("29.  The Experiment & the Contractual Definition of Attribution"));
push(P("Causality is proven with a small stepped-wedge design: every qualifying case is eventually worked, but timing is randomized. Treatment submits immediately; control submits after a predefined delay that still clears every safe deadline; deadline-sensitive and irreversible cases are never placed in control; sellers consent to the experimental timing in the pilot agreement. Assignment happens automatically at detection — before an operator sees the value or quality — stratified within seller, rule type, value bucket, and evidence quality, and recorded as an immutable event."));
push(callout([
  PR([B("Attribution is contractual and categorical, never causal-per-case.  ", { color: GREEN }), T("The counterfactual cannot be run per case, so a fee is owed only on an "), B("“Attributable Credit,”"), T(" defined by four booleans the seller signs at onboarding: (1) reference-bound to a claim VOLTA opened; (2) posted after the baseline snapshot, with no ML-initiated resolution already in flight; (3) net of any later reversal; (4) not a pre-existing or duplicate credit. Ambiguous or batched credits that cannot be joined 1:1 fall to a lower tier and are "), B("not"), T(" billed. The spontaneous base rate is measured with the delayed arm and subtracted at the metric layer — reported as a bounded range with its assumptions, never as false precision.")]),
]));
push(
  bullet([B("Two gates, never conflated. "), T("A technical-feasibility gate (one end-to-end case) and an economic/causal gate (enough comparable cases show meaningful incremental net value). One confirmed payment satisfies the first, never the second.")]),
  bullet([B("Honest about n. "), T("Ten submitted cases prove the workflow, not causality; the pilot pre-registers its analysis before seeing results so rule and case selection cannot manufacture a positive outcome.")]),
);
push(PR([T("Each eligible case carries: "), ...runsFrom(CODE("experiment_id, protocol_version, eligible_at, assignment, assignment_seed, stratum, delay_until, latest_safe_submission_at, exclusion_reason, submitted_at, auto_resolved_at, credited_at, net_credit, clawback"))], { spacing: { line: 340, after: 120 } }));

/* 30 */
push(H1("30.  Hard Go/No-Go Gates & Pre-Registered Floors"));
push(P("These are pre-registered before the pilot starts and are not redefined after seeing the numbers. Four numeric floors gate any scaling, and — crucially — they are escrowed with a named independent gatekeeper who also pre-approves the metric definitions (including the spontaneous-baseline method), so the gates are not theatre under sunk-cost pressure."));
push(tbl(
  ["Floor", "Threshold", "Meaning"],
  [
    [{ t: "F1 · Net-attributable %", b: true }, "≥ ~0.4% of GMV (existential)", "Below this, the recovery cannot cover fixed cost — do not scale"],
    [{ t: "F2 · Minutes-per-case", b: true }, "≤ a pre-set ceiling (e.g. ≤2 min blended)", "The operator-leverage thesis; above it, headcount economics break"],
    [{ t: "F3 · Detected→collected yield", b: true }, "≥ a pre-set floor", "Assessment cost is paid on all detected; revenue only on collected"],
    [{ t: "F4 · Net contribution / seller-month", b: true }, "≥ fixed cost × a safety multiple (≈3×)", "The composite: the seller is genuinely profitable, not marginal"],
  ],
  [3000, 3160, 3200],
));
push(spacer(60));
push(tbl(
  ["Dimension", "Continue", "Stop or redesign"],
  [
    [{ t: "Access", b: true }, "Path works for ≥3 sellers + a usable fallback", "Core sources unavailable or completeness unmeasurable"],
    [{ t: "Causality", b: true }, "Submitted cases show credible positive incremental net value vs delayed", "Similar payout and timing without intervention"],
    [{ t: "Economics", b: true }, "F1–F4 clear after labour, software, payment, tax, support", "Any existential floor (F1) fails"],
    [{ t: "Collection", b: true }, "One real credit→statement→NFS-e→payment clears; reversal handled", "Provider, fiscal, or mandate path undependable"],
    [{ t: "Platform", b: true }, "Read-only + copilot path remains supportable at low volume", "Workflow needs impersonation, scraping, or prohibited automation"],
  ],
  [1700, 4160, 3500],
));
push(spacer(60));
push(P("The gatekeeper holds a signed, dated one-page pre-registration (the four floors, the composite target, the approved metric definitions, and the kill/pivot/refund rule) and is empowered to enforce a no-go. The founder’s pre-commitment is a Ulysses clause — a moral and reputational commitment, and only as enforceable as the money is genuinely gated through the gatekeeper."));

/* 31 */
push(H1("31.  “The Number,” Redesigned"));
push(P("A single big recoverable figure is attractive and dangerous — it blends verified and speculative value. VOLTA shows four, plus context, and never presents potential value as collectible:"));
push(tbl(
  ["Figure", "Meaning"],
  [
    [{ t: "Verified & actionable", b: true }, "Evidence complete, cool-off passed, a valid action path exists — the headline number"],
    [{ t: "Pending evidence", b: true }, "A deterministic discrepancy exists, but documentation is incomplete"],
    [{ t: "Cooling off", b: true }, "A discrepancy exists, but the platform may still auto-resolve it"],
    [{ t: "Unreconciled / low coverage", b: true }, "Data is missing or cannot yet be matched"],
  ],
  [2900, 6460],
));
push(spacer(60));
push(P("Alongside the figures: data coverage %, and “sources current through …” with a timestamp. Down-market, the tail sees only the verified-actionable figure (and, in the free scan, magnitude and category counts — never the case-level evidence that would teach self-filing)."));

/* ================= PART IV — OPERATING, LEGAL & REFERENCE ================= */
push(...partBanner("Part IV", "Operating, Legal & Reference"));

/* 32 */
push(H1("32.  Fiscal & Corporate Structure — VOLTA’s Own Money"));
push(P("VOLTA’s own tax is an input to the fee, not an afterthought — the value-anchored success % must be set net of it. This section fixes the structure the completeness review flagged as the single highest-leverage missing piece."));
push(
  bullet([B("Register under a clean technology CNAE "), T("(e.g. 6311-9/00 tratamento de dados, or 6209-1/00 suporte técnico) — never a cobrança/collections CNAE, which would invite a debt-collection reading (Section 33).")]),
  bullet([B("Model the all-in effective rate before setting the fee. "), T("Compare Simples Nacional (which annex applies, and the effect of fator R) against Lucro Presumido, including ISS, PIS/COFINS, IRPJ/CSLL; the chosen regime changes the effective take materially, so it is decided with an accountant before pricing is fixed.")]),
  bullet([B("NFS-e timing = settlement, not accrual. "), T("Issue the NFS-e only on confirmed fee settlement, competência = settlement month, so ISS/PIS/COFINS never precede the cash. A post-settlement clawback runs the cancelamento/substituição runbook and a reversing entry.")]),
  bullet([B("A monthly close (D+5) with a three-way match: "), T("success-fee accrual ↔ NFS-e issued ↔ bank/Mercado-Pago receipt; revenue recognised only at collected-and-matured; reversals and a bad-debt provision booked; everything reconciled back to the immutable journal.")]),
  bullet([B("White-label remittance is one documented model: "), T("either VOLTA bills the seller and pays the partner against the partner’s NFS-e with correct service withholdings, or the partner bills the seller and VOLTA invoices the partner — one is chosen, its municipality/ISS locus fixed, and the withholdings automated. Not left ambiguous.")]),
);

/* 33 */
push(H1("33.  The Seller Contract & Onboarding Legal Flow"));
push(P("The contract is the root of the entire delegated-authority and collection chain. It is one dual-nature Brazilian instrument: a Contrato de Prestação de Serviços de Recuperação Administrativa/Operacional de Créditos combined with a Mandato (Código Civil arts. 593–609 and 653–692), with an express clause that it is NOT advocacia or assessoria jurídica."));
push(
  bullet([B("Fee & security: "), T("a contingency % of net-attributable collected credit, net of reversals, with the settlement hold-back; each confirmed fee is a título executivo extrajudicial via a confissão de dívida líquida e certa, reinforced by a mandato em causa própria and a signed-but-unregistered assignment of the fee slice held in escrow — so a stiff is executed quickly, not litigated slowly.")]),
  bullet([B("Scope: "), T("read access plus the specific permitted actions; reversal/clawback obligations; termination AND the treatment of credits that land after termination (the tail clause); a limitation-of-liability cap (e.g. trailing-12-month fees) with indemnity carve-outs.")]),
  bullet([B("LGPD: "), T("the DPA, lawful basis, consent, and encarregado contact are part of the same signing flow (Section 21).")]),
  bullet([B("Dispute resolution: "), T("foro or arbitragem, with a CDC-inapplicability recital reciting both parties are professionals (the STJ has refused CDC in near-identical B2B payment disputes absent proven vulnerability).")]),
);
push(H3("Onboarding legal flow — a strict, gated order"));
push(P("The delegated-authority chain collapses if artifacts are captured out of order, so onboarding is a sequence, each step blocked until the prior artifact is signed and stored as an immutable consent receipt:"));
push(
  numItem("1.", [B("Service contract + procuração "), T("(scope of authority established first).")]),
  numItem("2.", [B("DPA + LGPD consent "), T("(lawful basis before any data is fetched).")]),
  numItem("3.", [B("Pix Automático mandate authorization "), T("(the collection precondition — no mandate, no service).")]),
  numItem("4.", [B("Read-only OAuth connection "), T("(only now is data pulled).")]),
);
push(H3("Offboarding & regulatory classification"));
push(
  bullet([B("Offboarding runbook: "), T("freeze submissions on notice, revoke ML/MP OAuth and cancel the Pix mandate, export/return the seller’s evidence journal, then apply the retention matrix. Stale tokens and live mandates are never left dangling.")]),
  bullet([B("A standing “not-a-collections-agency” memo: "), T("VOLTA is a technology service with no custody, no purchase of receivables, and no handling of third-party money — outside COAF/AML, factoring, and BCB licensing. A product design-review checklist prevents a future feature (e.g. holding funds) from silently crossing that line.")]),
  bullet([B("Insurance: "), T("Seguro RC Profissional (E&O) plus cyber liability, sized to portfolio GMV, paired with the contractual liability cap.")]),
);

/* 34 */
push(H1("34.  The Operating Model & Key-Person Resilience"));
push(P("The business is legibly runnable by a handful of people because everything important is on a dashboard and everything repetitive is automated — but capacity is a measured function, not an assertion. Seller capacity = productive operator minutes × target occupancy ÷ (touches per seller × median active minutes per touch), including onboarding, evidence-chasing, support, billing disputes, and exceptions — not just case approval."));
push(P("The daily loop: clear every red deadline-risk card; drain triage at a target of a few minutes per case; sweep the approval queue, each click an immutable authorization releasing a code-drafted submission; resolve credit-reconciliation exceptions. The weekly loop: one review on Rule Health + Owner — demote any rule-version over its FP ceiling, promote shadow versions that beat the incumbent on submit-to-collect yield, review recovery per cohort and cash/dunning. You hire when the triage queue’s median age — a tile on the Operations dashboard — persistently exceeds SLA, not when seller count crosses a line."));
push(callout([
  PR([B("Honest on headcount, and on key-person risk.  ", { color: AMBER }), T("“One operator serves 400–500 sellers” assumes ~1 minute of blended human time per case — the single biggest unproven assumption in the business. Until sub-2-minute blended time is measured (floor F2), headcount is stated as a curve gated on that metric, not a planning input. On resilience: a Shamir 3-of-5 split of the KMS recovery seed (sealed envelopes) plus the key-independent audit chain removes the “lost key = unreadable history” risk, and documented runbooks + a designated backup approver reduce operational bus-factor. What stays concentrated — honestly — is the founder’s ML/MP working relationship, tax/regulatory judgment, and case intuition; that is a real, un-engineered-away risk.")], "F7EFE0", AMBER),
]));

/* 35 */
push(H1("35.  What v3 Changes From v2"));
push(tbl(
  ["Topic", "v2", "v3"],
  [
    ["Build posture", "Build the full platform now", "Build a narrow, instrumented executable pilot first; scale only after gates pass"],
    ["Access", "Assumed", "Proven in a Phase −1 Capability Proof with a hard day-3 STOP"],
    ["Reconciliation", "expected − matched = residual", "Immutable journal + many-to-many match allocations with explicit basis"],
    ["Pricing", "25% + a R$1,490/mo base + tiers", "One value-anchored success % only; no base; per-invoice minimum; set net of VOLTA’s tax"],
    ["North star", "Credited BRL per human hour", "Net-attributable BRL per seller & per R$ fixed cost; minutes = tripwire"],
    ["Getting paid", "Mandate ‘eliminates collection risk’", "Source-capture ruled out; a four-layer downstream stack; título executivo; honest residual"],
    ["Attribution", "Residual + one credit = proof", "A four-boolean contractual definition + a holdout-measured spontaneous baseline"],
    ["Action path", "API submission assumed", "Read-only footprint + human copilot; severs detection from action; solves ban-risk"],
    ["Tenant isolation", "RLS on every table", "Non-superuser roles + SET LOCAL + FORCE RLS + CI leak test (service_role bypasses RLS)"],
    ["LGPD", "Before scale; ‘all in Brazil’", "In Phase −1: DPA + SCCs + ROPA + encarregado + breach IR; transfers disclosed"],
    ["VOLTA’s own tax", "Unspecified", "A fiscal/corporate section; the fee is set net of the modelled effective rate"],
    ["Contract", "Unspecified", "A dual-nature instrument making each fee a título executivo; a gated onboarding order"],
    ["Governance", "Gates listed", "Four pre-registered floors escrowed with an independent gatekeeper"],
  ],
  [1800, 3130, 4430],
));

/* 36 */
push(H1("36.  The Verification Ledger"));
push(P("Every external assumption VOLTA depends on, with its verdict from the seven-agent verification pass. GREEN = verified from a primary source; PROVE = plausible but must be confirmed on a live account (a Phase −1 item); STOP = unverified or blocked, treat as a gate."));
push(tbl(
  ["Assumption", "Verdict", "Note & day-one action"],
  [
    ["MP Reports API supports the ingestion design (~60-day pulls, async)", V("GREEN"), "Chunk ≤60d and stitch; handle the async pattern"],
    ["MP recommends signed webhooks; IPN being discontinued", V("GREEN"), "Validate x-signature; subscribe payments/merchant_order/chargebacks"],
    ["Model-6 (CBT) sellers get 403 on claim endpoints", V("GREEN"), "Keep the guard; verify which onboarded sellers are CBT"],
    ["service_role bypasses RLS (and owner bypasses without FORCE)", V("GREEN"), "Non-superuser roles + SET LOCAL + FORCE RLS + CI leak test"],
    ["sa-east-1 region + pg_cron fires once cluster-wide", V("GREEN"), "Pin the region; single scheduler lease"],
    ["NFS-e Nacional; Emissor Nacional mandatory for Simples 1 Sep 2026", V("GREEN"), "Provider adapter; string identifiers; versioned schemas"],
    ["B2B contract ENFORCEABLE (CDC won’t attach; no BCB licence)", V("GREEN"), "Draft as B2B Código Civil + título executivo (Section 33)"],
    ["A delegated token returns THAT seller’s MP financial reports", V("YELLOW"), "Phase −1: confirm scopes read+offline return real report data"],
    ["Recovery is real, large, recurring, causally VOLTA’s (~1–3%)", V("YELLOW"), "The immediate-vs-delayed RCT; measure per pool/decile"],
    ["Pix Automático collects a variable fee end-to-end", V("YELLOW"), "Prove on a live PSP: mandate, arbitrary charge, cap, cancel, retry"],
    ["ML Full stock history offers meaningful lookback (default 15d)", V("YELLOW"), "Design for continuous polling; probe date_from live"],
    ["ML rate limits (the ~1500/min figure is third-party)", V("YELLOW"), "Adaptive backoff + per-seller queues; never hardcode"],
    ["A non-lawyer paid recovery service: administrative vs judicial line", V("YELLOW"), "Professional-practice question (not contract validity); confirm with counsel"],
    ["Platform PERMITS a monetized third-party recovery product", V("YELLOW"), "ML app certification + legal confirmation before monetizing"],
    ["Programmatic/automated claim submission is permitted by ML ToS", V("RED"), "Bot-blocked ToS: keep submission manual/copilot; read authenticated ToS first"],
  ],
  [4460, 900, 4000],
));

/* 37 */
push(H1("37.  Residual Risks — the Honest Irreducible Floor"));
push(P("Airtight is not risk-free. These remain even after every solution, and VOLTA goes in clear-eyed:"));
push(
  bullet([B("No custody, ever. "), T("Recovered money lands in the seller’s own account; every collection mechanism is a downstream pull the seller can defeat (cancel the mandate at 23:59, approve a low cap, sweep the balance), forcing execution of the título.")]),
  bullet([B("Total, opaque platform dependency. "), T("Mercado Livre controls the read APIs, the reimbursement rules and windows, and the undocumented ban-trigger thresholds. One policy change can break detection or flag seller accounts.")]),
  bullet([B("The attribution counterfactual is estimated, not proven. "), T("The spontaneous baseline is measured with a holdout and drifts as ML changes; batched credit notes are not always 1:1 joinable; a determined seller or Procon can contest it — mitigated by the contractual definition, not eliminated.")]),
  bullet([B("Core economic viability is unproven and may simply fail. "), T("Whether net-attributable lift exceeds fixed cost (F1) is unknown until pilot data exists, and the floor values themselves are informed guesses. No pricing or architecture fixes a business whose underlying recovery is too small.")]),
  bullet([B("Founder non-key capital stays concentrated. "), T("The ML/MP relationship, tax/regulatory judgment, and case intuition remain single-person even with key escrow and a backup operator.")]),
  bullet([B("Governance teeth are only as real as the money-gating, "), T("and the legal administrative-vs-judicial question remains a PROVE item until counsel settles it.")]),
);

/* 38 */
push(H1("38.  Recommendation"));
push(
  numItem("1.", [B("Build the truth machine, not the company. "), T("Run the desk kill and the Phase −1 Capability Proof first; treat the day-3 action-path check and the immediate-vs-delayed RCT as the real go/no-go.")]),
  numItem("2.", [B("Make the event spine and the journal the first thing you build. "), T("The workbench, every dashboard, and every automation are consumers of it; audit, LGPD, and dispute defence all follow from it.")]),
  numItem("3.", [B("Gate access, then economics, then autonomy. "), T("No rule without a permitted action path; no scaling until F1–F4 clear; no autonomy on an action-class until a clean-outcome dataset earns it.")]),
  numItem("4.", [B("Price on value net of tax, collect with the four-layer stack, bill per cycle. "), T("One success %, no base fee, settlement hold-back, título-backed collection — and never present potential value as collectible.")]),
  numItem("5.", [B("Keep it Brazil-only and KISS. "), T("Defer the platform-scale subsystems to named milestones; add nothing until a real, repeated pain forces it.")]),
);
push(P("The prize, if the pilot passes, is the first credible, verified, causally-honest automated recovery layer for Brazilian Mercado Livre sellers. But the honest verdict stands: this is airtight as a plan — every load-bearing risk is named, bounded, instrumented, and cheap to falsify — and it becomes a business only when a live pilot answers the four questions no document can: can VOLTA legally act, can it actually get paid, is the recovery causally its own, and does the money exceed the cost."));

/* 39 */
push(H1("39.  Appendix — Glossary"));
push(
  bullet([B("Full / Mercado Envios Full — "), T("Mercado Livre’s fulfilment programme; the FBA analog.")]),
  bullet([B("Mercado Pago — "), T("Mercado Livre’s payments arm; source of the financial reports VOLTA reconciles against.")]),
  bullet([B("NF-e / DANFE — "), T("the Brazilian electronic invoice; the XML is the legal document, retrievable from SEFAZ within a window.")]),
  bullet([B("NFS-e / Emissor Nacional — "), T("the municipal service invoice VOLTA issues for its own fee; the national emitter becomes mandatory for Simples ME/EPP from 1 Sep 2026.")]),
  bullet([B("Model-6 (CBT) seller — "), T("a cross-border classification that returns 403 on the claim/return endpoints VOLTA needs.")]),
  bullet([B("Título executivo extrajudicial — "), T("a debt instrument enforceable by fast execution rather than an ordinary lawsuit; VOLTA’s fee is structured as one.")]),
  bullet([B("Attributable Credit — "), T("the four-boolean contractual definition of a billable credit (Section 29).")]),
  bullet([B("Settlement hold-back — "), T("the window a confirmed credit must survive before its fee becomes billable, sized past the measured clawback window.")]),
  bullet([B("Event spine — "), T("the append-only, key-independent hash-chained record families that are VOLTA’s system of record.")]),
  bullet([B("Capability Proof — "), T("the Phase −1 gate proving data ingestion, completeness, a permitted action path, and a live mandate before any rule is built.")]),
);
push(spacer(120), hr());
push(P("Version 3 — confidential working draft, 23 July 2026. Verdicts reflect a July 2026 multi-agent verification pass against primary sources; PROVE/STOP items must be confirmed on a live account and with Brazilian counsel before launch. This document describes a plan and an architecture; it is not legal, tax, or investment advice."));

/* ================= DOCUMENT ================= */
const doc = new Document({
  creator: "VOLTA",
  title: "VOLTA — Business Plan & Technology Overview (v3)",
  description: "v3: verified, stress-tested, pilot-first — the truth machine before the company.",
  styles: {
    default: { document: { run: { font: "Calibri", size: 26, color: INK }, paragraph: { spacing: { line: 360, after: 160 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Calibri", size: 40, bold: true, color: GREEN }, paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Calibri", size: 30, bold: true, color: GREEN2 }, paragraph: { spacing: { before: 260, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Calibri", size: 27, bold: true, color: INK }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: { titlePage: true, page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, border: { top: { color: LINE, space: 6, style: BorderStyle.SINGLE, size: 4 } },
        children: [new TextRun({ text: "VOLTA  ·  Business Plan & Technology Overview (v3)  ·  Confidential  ·  ", size: 17, color: GREY }), new TextRun({ children: [PageNumber.CURRENT], size: 17, color: GREY })] })] }),
      first: new Footer({ children: [new Paragraph({ children: [T("")] })] }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/tmp/claude-0/-home-user-Random-Access-Memories/9aef20de-742c-52a2-b11a-a33d815230ea/scratchpad/VOLTA_Business_Plan.docx", buf);
  console.log("WROTE v3 docx:", buf.length, "bytes");
});
