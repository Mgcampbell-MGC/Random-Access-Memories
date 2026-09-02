const d = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
        ShadingType, BorderStyle, AlignmentType, PageBreak, HeadingLevel, Footer, PageNumber } = d;
const fs = require('fs');

const NAVY="1F3A5F", SLATE="4A5568", INK="1A1A1A", MUTED="6B7280", LINE="C9D2DD", ROW="EEF2F7", ACCENT="8C6D3F";
const W = 10080;
const FONT = "Calibri";

const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };

function P(text, o={}) {
  return new Paragraph({
    alignment: o.align, spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 264 },
    indent: o.indent, border: o.border, keepNext: o.keepNext,
    children: (Array.isArray(text) ? text : [{ t: text }]).map(r => new TextRun({
      text: r.t, bold: r.b ?? o.bold, italics: r.i ?? o.italics,
      size: (r.size ?? o.size ?? 21), color: r.color ?? o.color ?? INK,
      font: FONT, allCaps: r.caps ?? o.caps, characterSpacing: o.spacingChar
    }))
  });
}
function H1(t){ return P(t, { size: 27, bold: true, color: NAVY, before: 0, after: 180,
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } } }); }
function H2(t){ return P(t, { size: 22, bold: true, color: NAVY, before: 260, after: 120, keepNext: true }); }
function KICKER(t){ return P(t, { size: 17, bold: true, color: ACCENT, caps: true, spacingChar: 20, after: 60 }); }
function BULLET(t){ return new Paragraph({ bullet: { level: 0 }, spacing: { after: 90, line: 264 },
  children: (Array.isArray(t)?t:[{t}]).map(r => new TextRun({ text: r.t, bold: r.b, italics: r.i, size: 21, color: r.color ?? INK, font: FONT })) }); }

function cell(runs, o={}) {
  return new TableCell({
    width: { size: o.w, type: WidthType.DXA },
    shading: o.shade ? { type: ShadingType.CLEAR, fill: o.shade, color: "auto" } : undefined,
    margins: { top: 90, bottom: 90, left: 130, right: 130 },
    verticalAlign: "center",
    borders: { top:{style:BorderStyle.SINGLE,size:2,color:LINE}, bottom:{style:BorderStyle.SINGLE,size:2,color:LINE},
               left:{style:BorderStyle.SINGLE,size:2,color:LINE}, right:{style:BorderStyle.SINGLE,size:2,color:LINE} },
    children: [ new Paragraph({ alignment: o.align, spacing: { after: 0, line: 250 },
      children: (Array.isArray(runs)?runs:[{t:runs}]).map(r => new TextRun({
        text: r.t, bold: r.b ?? o.bold, italics: r.i, size: r.size ?? o.size ?? 19,
        color: r.color ?? o.color ?? INK, font: FONT })) }) ]
  });
}
function table(widths, rows) {
  return new Table({ columnWidths: widths, width: { size: widths.reduce((a,b)=>a+b,0), type: WidthType.DXA }, rows });
}
// two-column fact table
function facts(pairs) {
  const ws = [2600, 7480];
  return table(ws, pairs.map(([k, v], i) => new TableRow({ children: [
    cell(k, { w: ws[0], shade: ROW, bold: true, color: NAVY, size: 19 }),
    cell(v, { w: ws[1], size: 19 })
  ]})));
}

const doc = new Document({
  creator: "Business search", title: "Ten Business Candidates", description: "Candidate profiles",
  styles: { default: { document: { run: { font: FONT, size: 21, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1100, bottom: 1000, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [ new Paragraph({ alignment: AlignmentType.CENTER,
      children: [ new TextRun({ text: "Ten business candidates  ·  September 2026  ·  page ", size: 16, color: MUTED, font: FONT }),
                  new TextRun({ children: [PageNumber.CURRENT], size: 16, color: MUTED, font: FONT }) ] }) ] }) },
    children: BODY()
  }]
});

function BODY() {
  const c = [];
  // ---------- COVER ----------
  c.push(P("", { after: 900 }));
  c.push(P("TEN BUSINESS CANDIDATES", { size: 48, bold: true, color: NAVY, after: 60, spacingChar: 10 }));
  c.push(P("Screened, costed and ranked for a single operator in São Paulo", { size: 24, color: SLATE, after: 260 }));
  c.push(new Paragraph({ spacing: { after: 300 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 4 } }, children: [] }));
  c.push(P("Each candidate below is described as a business a reader outside the project can assess: what it sells, who buys it, at what moment, for how much, and what would kill it. The order is a ranking, and the reasoning behind the order is given on the next page.", { size: 22, color: SLATE, after: 200 }));
  c.push(P("Every figure that is measured is marked as measured, with its source named. Every figure that is an estimate is marked as an estimate. Nothing here has a paying customer yet, and the document says so on each page rather than once at the end.", { size: 22, color: SLATE, after: 900 }));
  c.push(P("September 2026", { size: 20, color: MUTED }));
  c.push(new Paragraph({ children: [ new PageBreak() ] }));

  // ---------- HOW TO READ ----------
  c.push(H1("How to read this"));
  c.push(KICKER("The operator"));
  c.push(P("One person, in São Paulo, working roughly ten hours a week on the business. She writes English and Portuguese fluently. Her background is in fashion and modelling, which is treated here as knowledge of how an industry works rather than as a public profile: she is not building an audience and does not appear in any of these businesses."));
  c.push(KICKER("The target"));
  c.push(P("Two thousand to two thousand five hundred US dollars a month in net take-home pay, within twelve to eighteen months. In Brazilian terms, roughly twelve to fifteen thousand reais a month in gross revenue for a business with no cost of delivery."));
  c.push(P([{t:"This number matters more than it looks. "},{t:"An earlier target of ten thousand dollars a month was tested against roughly a hundred and thirty candidates and none survived",b:true},{t:", because ten hours a week at observed prices cannot produce it. The target was cut to the figure above, and that single change is what makes the list below possible. Several of these businesses were designed at this number, killed when the target was raised, and are now alive again."}]));
  c.push(KICKER("The rules the businesses have to obey"));
  c.push(BULLET([{t:"Capital: ",b:true},{t:"three thousand US dollars, once. That buys an entity, tooling and a small test. It does not buy paid advertising at scale or an acquisition."}]));
  c.push(BULLET([{t:"No employees. ",b:true},{t:"Contractors and suppliers are allowed; a payroll is not."}]));
  c.push(BULLET([{t:"Roughly ten hours a week. ",b:true},{t:"This is a hard limit, not a preference, and it is the reason several otherwise good businesses are ranked low: they work, but only by consuming every hour she has."}]));
  c.push(BULLET([{t:"Written delivery. ",b:true},{t:"She will take a call to open a supplier account or sign a partner. She will not run a business whose daily operation is a telephone."}]));
  c.push(BULLET([{t:"She is never the expert. ",b:true},{t:"No candidate may depend on a stranger believing her professional judgement. Either the product proves itself, or the customer supplies the expertise and she supplies the capacity."}]));
  c.push(KICKER("How the ten are ordered"));
  c.push(P("Four questions, in this order. Does it reach the target at a price somebody actually charges? Is that price observed in the market or estimated? Can she reach the buyers for nothing, from a public list? And could she still be doing this, alone, in three years — the question that killed the highest-scoring candidate this project ever produced, after it had passed every other test."));
  c.push(KICKER("The honest state of the evidence"));
  c.push(P([{t:"One of the ten has an observed market price. "},{t:"The rest are priced from comparable products or from estimates, and that is the single largest gap in the work. ",b:true},{t:"No candidate has been put in front of a paying stranger. Each one below carries a test that costs under fifty dollars and returns a number rather than an opinion."}]));
  c.push(new Paragraph({ children: [ new PageBreak() ] }));

  // ---------- SUMMARY TABLE ----------
  c.push(H1("The ten at a glance"));
  const sw = [600, 1900, 2380, 1500, 1440, 2260];
  const head = ["", "Business", "Who buys it", "Price", "Volume needed", "Evidence"];
  const rows = [ new TableRow({ tableHeader: true, children: head.map((h,i)=>cell(h,{w:sw[i],shade:NAVY,bold:true,color:"FFFFFF",size:18})) }) ];
  const data = [
    ["1","Conformidade","Brazilian dental practices","R$1.500 once","8–10 a month","Deadline verified; buyer list measured"],
    ["2","Representante","Small foreign companies entering Brazil","US$400–800 a month","3–7 clients","Price observed; buyer pool counted"],
    ["3","Scan Keepsake","Parents, and ultrasound studios","US$149, or wholesale","2–4 studios","Software built and running"],
    ["4","Before You","Baby-shower gift buyers","US$149","16–21 a month","Mechanic proven by three incumbents"],
    ["5","Vera","A brand-protection firm, as its Brazil layer","US$2.500–3.000 a month","One partner","Problem verified; price estimated"],
    ["6","Sinal","Brazilian clinics","R$600 a month","21–26 clinics","Pain measured; category crowded"],
    ["7","Catalogue Repair","Merchants launching on a new channel","£2.500 a job","One a month","Price from an interview, not a sale"],
    ["8","The Memorial Book","Funeral homes, wholesale","US$400–500","5–6 a month","Market prices verified at both ends"],
    ["9","Conferência de Crédito","Suppliers to companies in restructuring","R$12–25.000 a job","10–13 a year","Buyer list published free by courts"],
    ["10","Brazil Desk","Foreign companies with Brazilian customers","Per seat","2–3 seats","Works on paper; poor fit"],
  ];
  data.forEach((r,i)=> rows.push(new TableRow({ children: r.map((v,j)=>cell(v,{w:sw[j],shade: i%2?ROW:undefined, bold: j===1, size:18, color: j===0?MUTED:INK })) })));
  c.push(table(sw, rows));
  c.push(P("", { after: 200 }));
  c.push(P([{t:"Two further candidates sit just outside this list. ",b:true},{t:"Both have stronger evidence than most of the ten — one has a defect rate independently reproduced at six to ten per cent, the other an enumerable list of nearly seventeen thousand buyers. They are held back for one reason only: both are industrial and regulatory data products, and the operator rejected a business of exactly that shape after it had passed every economic test. They are described at the end."}], {size:20, color: SLATE}));
  c.push(new Paragraph({ children: [ new PageBreak() ] }));

  // ---------- PROFILES ----------
  const profiles = [
    {
      n: 1, name: "CONFORMIDADE", sub: "The compliance document set every Brazilian dental practice now has to hold",
      what: "In December 2025 Brazil's health regulator published a new national standard for dental services. It requires every practice in the country to hold a defined set of seventeen operating documents — architectural approval, staff records and training plans, water monitoring, pest control, equipment maintenance, waste management, contracts with outsourced services, and the rest. Existing practices were given three hundred and sixty days. That runs out in December 2026. Operating without the set is a sanitary offence.",
      biz: "A structured questionnaire about the practice — its rooms, equipment, staff, suppliers and procedures — feeds a generator that produces the complete document set already filled in with that practice's own details, ready for its technical director to review and sign. It is delivered as files. Nothing is printed, shipped or installed.",
      facts: [
        ["What it sells","The seventeen-document set, generated from a questionnaire"],
        ["Who buys","Dental practices in Brazil"],
        ["Price","R$1.500 once (under test)"],
        ["Volume needed","8–10 a month"],
        ["Her time","Two to thirteen hours a month, if the generator holds"],
        ["Reaching buyers","Free. Measured below"],
      ],
      strong: [
        [{t:"The deadline is real and was verified at source, not from a blog. ",b:true},{t:"The regulator's own guidance, published in July 2026, restates the three-hundred-and-sixty-day term. This matters because compliance deadlines are quietly deferred more often than the industry press notices, and one earlier candidate in this project died exactly that way."}],
        [{t:"The buyer list is free, and it is better than a commercial one. ",b:true},{t:"Brazil's public health-establishment register publishes each practice's own registered email address. Measured in São Paulo city: one thousand nine hundred and eighty-six dental establishments, seventy per cent with a working email, seventy per cent with a phone. One fifth of them are sole practitioners with no company registration, which makes them invisible on every commercial prospect list."}],
        [{t:"A dated statutory deadline is the only cold-email subject line that does not read as spam."}],
      ],
      risk: "A kit of a hundred and eighty-six editable Word templates for this exact standard already sells online for about twenty US dollars. So this cannot be sold as compliance — compliance is available for twenty dollars. What is sold is the ten to twenty hours of filling those templates in with a specific practice's real data, against a fixed date. If a dental council, the regulator or a dental supply company publishes a free model pack, the business ends. The price has never been tested, and testing it is the first action.",
    },
    {
      n: 2, name: "REPRESENTANTE", sub: "The Brazil-resident representative every foreign company is required by law to appoint",
      what: "Brazilian law obliges foreign parties to name a representative resident in Brazil in at least three separate situations: a foreign-owned company registering for tax, a foreign holder filing or defending a trademark, and any foreigner registering a Brazilian domain name. The qualification required is residence in Brazil and full civil capacity. There is no licence, no examination and no professional body.",
      biz: "She is named as the representative, receives official notices, signs within the scope of a power of attorney, and reports to the client. It is a standing role rather than a project, billed monthly or annually.",
      facts: [
        ["What it sells","A legal qualification the buyer cannot supply for itself"],
        ["Who buys","Small foreign companies entering Brazil"],
        ["Price","US$400–800 a month — the only observed price on this list"],
        ["Volume needed","Three to seven clients"],
        ["Her time","One to three hours per client per month"],
        ["Cost of delivery","None"],
      ],
      strong: [
        [{t:"The price is published, not estimated. ",b:true},{t:"A São Paulo provider publishes a tier table: eight hundred to nine hundred US dollars a month for a startup, up to one thousand three hundred for a mid-size company, on annual contracts. Others operate at four hundred. This is the only candidate on the list whose price was read off a seller's own page."}],
        [{t:"A large compelled population is sitting unserved, and it was counted. ",b:true},{t:"Four consecutive weeks of Brazil's official trademark gazette were parsed. In that month, two thousand five hundred and twenty-nine international trademark registrations designated Brazil with a foreign holder, and eighty-two per cent of them had no Brazilian representative on record — roughly twenty thousand a year. The regulator's own manual gives such a holder sixty days from any action before the office to appoint one, or the filing is thrown out."}],
        [{t:"No credential protects the incumbents. ",b:true},{t:"Of seven hundred and seven representatives serving foreign holders in that month, three hundred and sixty-nine are individual people rather than firms, and they handle twenty-nine per cent of the work."}],
      ],
      risk: "Distribution is the weak point: law firms and accountants own the referral channel and there is no directory of buyers to email. And a compelled role can be repealed — Brazil's central bank abolished a comparable representative requirement for small foreign investors in 2025. The duties above are separate and untouched, but they go on a quarterly watch. Personal liability is limited by statute to acts beyond the granted powers, and that reading needs one lawyer's confirmation before the first client.",
    },
    {
      n: 3, name: "SCAN KEEPSAKE", sub: "Printed keepsakes made automatically from a family's own ultrasound images",
      what: "Parents upload their own scan images and a short form. A pipeline produces print-ready artwork: an enhanced portrait, a heartbeat waveform print, a star chart for the date, and typeset names and dates. It is then printed and shipped by a print-on-demand partner. No text is written for any order.",
      biz: "Two routes to the same product. Direct to parents at a hundred and forty-nine US dollars, or wholesale to private ultrasound studios, which already sell keepsakes at the emotional peak of the appointment — one UK franchise alone has thirty-five clinics and sells a twenty-five pound heartbeat bear as an in-scan add-on.",
      facts: [
        ["Status","Built and running. Seven stages, a quarter of a second per unit"],
        ["Who buys","Expectant parents; private ultrasound studios"],
        ["Price","US$149 direct, or wholesale per unit"],
        ["Volume needed","Two to four studios, or 16–20 direct sales a month"],
        ["Her time","Checking output and handling exceptions"],
      ],
      strong: [
        [{t:"It is the only candidate on this list that already exists. ",b:true},{t:"The software is written and runs. The question of whether this is a machine or her hands on every order is settled by architecture rather than argued."}],
        [{t:"Two steps a catalogue seller cannot copy: ",b:true},{t:"it removes patient data burned into the image by reconstructing from the surrounding picture rather than blurring it, and it separates the subject using a method suited to the particular noise an ultrasound produces."}],
        [{t:"The subject cannot be photographed by the customer. ",b:true},{t:"This is what separates it from every other keepsake. A pet, a house or a wedding competes with the phone in the customer's pocket from the first minute. A fetus has no free substitute."}],
        [{t:"It is the best personal fit on the list ",b:true},{t:"— warm, aesthetic, and in a world she would choose."}],
      ],
      risk: "One processing step has never been tested on a real two-dimensional scan with patient details burned into it, and that is the step most likely to break. Image resolution limits the product to small formats, which caps the price. Signing studios is slow, and a competitor with a print integration could add the same line.",
    },
    {
      n: 4, name: "BEFORE YOU", sub: "A written pregnancy memoir, bought as a baby-shower gift",
      what: "Bought by the expectant mother's mother or closest friend as a gift and redeemed by the mother herself. She answers a sequence of prompts; a draft is produced and edited; a hardcover book arrives. Printing and shipping are handled white-label with no inventory and no minimum order.",
      biz: "A hundred and forty-nine US dollars for the book, sixty-nine for a second copy — and the second copy is the best margin in the business, because it is the same work.",
      facts: [
        ["Who buys","Gift buyers, in the weeks before a baby shower"],
        ["Price","US$149, second copy US$69"],
        ["Volume needed","16–21 orders a month"],
        ["Her time","Six to eight hours a month once the process settles"],
        ["Fulfilment","Print-on-demand, no inventory, no minimum"],
      ],
      strong: [
        [{t:"The mechanic is proven at scale by three companies. ",b:true},{t:"StoryWorth sells prompted questions into a hardcover at fifty-nine to a hundred and ninety-nine dollars a year; Remento at ninety-nine; Storii at seventy-nine over messaging. People already pay for exactly this transaction."}],
        [{t:"It produces a paying stranger faster than anything else here. ",b:true},{t:"Three books and one print run costs about thirty dollars and answers a question no further research can."}],
        [{t:"A consumer cannot demand a meeting. ",b:true},{t:"Every business-to-business candidate in this project eventually met a buyer who wanted a call before signing. A gift buyer never does."}],
      ],
      risk: "It is a writing business: every unit needs her hands, which caps it permanently at the volume above. The category is occupied at forty-eight to a hundred and twenty-nine dollars, so competitors cap the price, and the thing that justifies the premium — editorial quality — is invisible in a thumbnail. It also repeats a shape this project has explored more than any other, which is a reason for caution rather than a defect.",
    },
    {
      n: 5, name: "VERA", sub: "A dated record of who sold counterfeit aesthetic products in Brazil, sold to the firms that enforce",
      what: "Counterfeit injectable aesthetic products circulate in Brazil in waves. In recent months the regulator ordered the seizure of counterfeit lots of two separately branded products, each time after the manufacturer itself raised the alert. One police operation dismantled a scheme that moved twelve million reais through a hundred and fifty-four online storefronts.",
      biz: "A continuously maintained record of who is offering what, under which storefront identity, on which date, with the listing preserved. Storefronts vanish, so this is a history a manufacturer cannot reconstruct after the fact at any price. It is sold not to the brands directly but under the name of an established brand-protection firm, as its Brazil layer.",
      facts: [
        ["What it sells","Seller-identity history that cannot be rebuilt later"],
        ["Who buys","A brand-protection or intellectual-property firm"],
        ["Price","US$2.500–3.000 a month (estimate)"],
        ["Volume needed","One partner"],
        ["Why wholesale","The partner owns the client relationship and the credibility"],
      ],
      strong: [
        [{t:"The problem is real, recurring and documented, ",b:true},{t:"with two separate branded products seized in a single recent period, each on the manufacturer's own alert."}],
        [{t:"It is her own field. ",b:true},{t:"Aesthetics and beauty are the world she knows, and here that knowledge is used to spot where the gap is, not to be believed as an authority."}],
        [{t:"Selling through a partner solves the credibility problem structurally: ",b:true},{t:"the partner has the name, the client and the enforcement capability; she supplies the one thing that has to be collected locally and continuously."}],
      ],
      risk: "On the first day the archive is empty, so the thing being sold does not yet exist — it has value only after it has been running. Test purchases of prescription products require a licensed partner. And no brand-protection firm publishes a partner programme, so this has to be negotiated firm by firm rather than applied for.",
    },
    {
      n: 6, name: "SINAL", sub: "Turning missed appointments back into revenue for Brazilian clinics",
      what: "A no-show costs a clinic a procedure. Measured at one procedure of about three hundred and fifty reais a day, that is roughly seven thousand seven hundred reais a month per clinic. The fix is not a mystery — reminders, an active waiting list, and a small deposit taken at the moment of booking. What is new is that Brazil's instant payment system made those deposits free and immediate.",
      biz: "Sold as a layer on top of whatever booking system the clinic already runs. Clinics will not change systems; they will bolt something on.",
      facts: [
        ["What it sells","Recovered appointments"],
        ["Who buys","Brazilian clinics"],
        ["Price","R$600 a month"],
        ["Volume needed","21–26 clinics"],
        ["Why now","Free, instant deposits at booking"],
      ],
      strong: [
        [{t:"The loss is measured rather than asserted, ",b:true},{t:"and it is roughly ten times the monthly price."}],
        [{t:"Because the recovered bookings can be observed, ",b:true},{t:"the service can be priced on the result rather than on a subscription."}],
      ],
      risk: "The category is crowded and an incumbent anchors it at a hundred and sixty to three hundred and seventy reais a month, well below the price above. Messaging is billed per message, so the flow has to be designed so reminders travel inside a free conversation window rather than as paid sends. Twenty-six clinics is also a real sales operation, even with a free list. The improvement figures quoted by vendors in this category are marketing, and they flatter.",
    },
    {
      n: 7, name: "CATALOGUE REPAIR", sub: "Getting a merchant's product catalogue to import cleanly onto a new sales channel",
      what: "When a merchant launches on a new marketplace or in a new country, its product catalogue has to import cleanly: product variants, parent and child relationships, attribute schemas, category mapping, dimensions, weights, barcodes, image relationships. The free artificial-intelligence tools now built into every platform generate text into products that already exist. None of them repairs structural data, resolves contradictions between two supplier spreadsheets, or fixes a file that will not upload at all.",
      biz: "Sold to the launch — a fixed date with a real consequence — rather than to the ongoing mess. The deliverable is a repaired file plus a verified import with the ability to roll back.",
      facts: [
        ["What it sells","A catalogue that imports, on the day it has to"],
        ["Who buys","Merchants launching on a new channel or in a new country"],
        ["Price","£2.500–3.000 a job"],
        ["Volume needed","One a month"],
        ["Her time","Twelve to thirteen hours a job"],
      ],
      strong: [
        [{t:"The boundary is structural, not a matter of quality. ",b:true},{t:"The free platform tools fill empty fields in products that are already loaded. They cannot act before the product is in the platform, cannot touch structural data, and will not overwrite data that is already wrong."}],
        [{t:"The price came from a merchant describing what it would pay ",b:true},{t:"for the repair plus a verified import — not from a competitor's rate card."}],
      ],
      risk: "It needs roughly a hundred and ninety hours to build, which is either four months of her available time or most of the start-up capital spent on a contracted developer. The price came from a research interview rather than a transaction. And offshore providers have done catalogue data for twenty years at fractions of a dollar per product, so this can never compete on price — only on turnaround and on the guaranteed import.",
    },
    {
      n: 8, name: "THE MEMORIAL BOOK", sub: "A printed life story, sold wholesale through funeral homes",
      what: "A personalised printed memorial book, produced from a written questionnaire completed by the family, sold to funeral homes as an add-on at the moment arrangements are made.",
      biz: "Wholesale at four to five hundred US dollars, with the funeral home retailing it and keeping a margin. Around six partner homes supply the volume.",
      facts: [
        ["Who buys","Funeral homes, wholesale"],
        ["Price","US$400–500"],
        ["Volume needed","5–6 a month, roughly six partner homes"],
        ["Her time","About five to six hours a month"],
      ],
      strong: [
        [{t:"The market has a gap in exactly this place, and both ends of it were verified. ",b:true},{t:"Printed booklets start at under five dollars in a supplier catalogue; a full-service tribute book runs to about five thousand and explicitly includes client meetings. The middle is occupied by the funeral home's own software vendor, which gives its personalisation tool away free. A hands-on product at four to five hundred dollars sits between them."}],
        [{t:"The volume is exogenous ",b:true},{t:"— it is set by deaths, not by anybody's marketing budget — and the buyer is at their least price-sensitive at the moment of purchase."}],
      ],
      risk: "This is not primarily a commercial risk. The work is emotionally heavy on every single unit, permanently, with no quiet months. The question is not whether the idea appeals but whether she could still be opening files about strangers' dead parents, alone, in year three. That question has ended a candidate in this project before, after it had passed everything else.",
    },
    {
      n: 9, name: "CONFERÊNCIA DE CRÉDITO", sub: "Reconciling what a supplier is owed when a Brazilian customer enters restructuring",
      what: "When a Brazilian company files for judicial reorganisation it must publish a list of its creditors, compiled from its own accounts-payable ledger. The list is routinely wrong — invoices omitted, values stale, claims in the wrong class. A supplier's claim is frozen at the debtor's number unless it formally objects within fifteen days of publication.",
      biz: "The supplier's own receivables data is reconciled line by line against the published list, and delivered as an evidence-linked file with every source document attached. The supplier's own lawyer files it. She never advises, classifies or appears.",
      facts: [
        ["What it sells","A line-by-line reconciliation with sources attached"],
        ["Who buys","Trade suppliers to companies in restructuring"],
        ["Price","R$12.000–25.000 per engagement"],
        ["Volume needed","10–13 a year"],
        ["Reaching buyers","The list is published free, by court order"],
      ],
      strong: [
        [{t:"The lead list is published, dated, free, and carries the amount at stake on every row. ",b:true},{t:"Nine published cases were machine-parsed: large cases carry a median of two hundred and four qualifying trade creditors, and roughly twenty thousand qualifying creditors arise nationally each year. She needs ten."}],
        [{t:"Only one side is the client. ",b:true},{t:"The counterparty's number is published by court order, so she never has to persuade two parties to cooperate."}],
        [{t:"Filings are at a record level ",b:true},{t:"and rose thirteen per cent in the most recent year measured."}],
      ],
      risk: "One thing has never been measured: whether Brazilian law firms already do this work on a success fee. If they do, the service competes with free. That question can be answered by reading twenty published cases and counting. The fifteen-day window is also tight for a cold approach, and the work is legally adjacent, which requires a carefully drawn line about what is and is not being supplied.",
    },
    {
      n: 10, name: "BRAZIL DESK", sub: "Portuguese-language customer operations for foreign companies, sold by the seat",
      what: "Foreign companies with Brazilian customers need Portuguese-language customer operations and do not want to hire in Brazil to get them. Sold as dedicated seats, delivered by contractors, invoiced in dollars.",
      biz: "Two or three seats reach the target. The buyer is foreign, so the revenue is in hard currency and the domestic cost structure works in its favour.",
      facts: [
        ["Who buys","Foreign companies with Brazilian customers"],
        ["Price","Per seat, monthly"],
        ["Volume needed","Two to three seats"],
        ["Why it is last","It is a staffing business"],
      ],
      strong: [
        [{t:"It is the one candidate in three structured searches that was killed by the revenue target alone ",b:true},{t:"and by nothing else. At the target above, it works."}],
        [{t:"Hard-currency revenue against a Brazilian cost base ",b:true},{t:"is a genuine and durable advantage."}],
      ],
      risk: "It is the opposite of what the operator asked for. It means a screen all day and managing contractors who talk to strangers all day, and its margin is a markup on a wage that anybody can look up. It is listed because it honestly works, not because it should be chosen.",
    },
  ];

  profiles.forEach((p, idx) => {
    c.push(P([{t:String(p.n).padStart(2,"0")+"  "},{t:p.name}], { size: 30, bold: true, color: NAVY, after: 40 }));
    c.push(P(p.sub, { size: 22, italics: true, color: ACCENT, after: 160,
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 8 } } }));
    c.push(KICKER("The situation"));
    c.push(P(p.what));
    c.push(KICKER("The business"));
    c.push(P(p.biz, { after: 180 }));
    c.push(facts(p.facts));
    c.push(P("", { after: 140 }));
    c.push(KICKER("What makes it work"));
    p.strong.forEach(s => c.push(BULLET(s)));
    c.push(P("", { after: 60 }));
    c.push(KICKER("What would kill it"));
    c.push(P(p.risk, { after: 0 }));
    if (idx < profiles.length - 1) c.push(new Paragraph({ children: [ new PageBreak() ] }));
  });

  // ---------- BELOW THE LINE ----------
  c.push(new Paragraph({ children: [ new PageBreak() ] }));
  c.push(H1("Two candidates held just outside the ten"));
  c.push(P("Both of these have harder evidence behind them than most of the ten above. Both are held back for a single reason, and it is not commercial."));
  c.push(H2("CertGap"));
  c.push(P("Every appliance brand sold in the United States files its energy figures with the federal government twice — once for the efficiency label, once for compliance certification. Both filings are public, both were completed by the same manufacturer, and they routinely disagree. The product is a report showing a named brand, model by model, exactly where its own two federal filings contradict each other."));
  c.push(P([{t:"The defect rate was independently reproduced at six to ten per cent across four unrelated product categories ",b:true},{t:"— which makes it the best-evidenced claim in this entire document. Six hundred and fifty US dollars for the initial audit and three hundred and fifty per quarter to monitor; three to four audits a month reaches the target."}]));
  c.push(H2("ADV-Check"));
  c.push(P("Registered investment advisers in the United States file two public documents that must agree with each other, and often do not. The regulator publishes the full roster free: sixteen thousand seven hundred and seventy-nine firms, fifteen thousand four hundred and forty-five of them with a website. The product is a report on a named firm's own inconsistencies, at six hundred and fifty dollars."));
  c.push(H2("Why they are not in the ten"));
  c.push(P([{t:"Both are industrial and regulatory data products. ",b:true},{t:"The operator was previously offered a business of exactly that shape — it had passed every economic and structural test in the project, and it was rejected in four words as not being anything she recognised as herself. A business she will not still be running in three years is worth nothing whatever its arithmetic says, so these two are recorded rather than recommended. One word from her moves either into the top three on evidence alone."}]));

  // ---------- WHAT HAPPENS NEXT ----------
  c.push(new Paragraph({ children: [ new PageBreak() ] }));
  c.push(H1("What happens next"));
  c.push(P("Nothing on this list has been put in front of a person who could pay for it. That is the honest state of the work, and it is the only thing worth fixing next. Three tests are ready. Together they cost under a hundred dollars, none of them requires a telephone, and each returns a number rather than an opinion."));
  const tw = [520, 3100, 3400, 3060];
  const trows = [ new TableRow({ tableHeader: true, children: ["","The test","What it costs","What counts as a pass"].map((h,i)=>cell(h,{w:tw[i],shade:NAVY,bold:true,color:"FFFFFF",size:18})) }) ];
  [
    ["1","Sixty emails to dental practices: thirty asked what they paid for their compliance documents, thirty offered the set at the test price","One domain, about ten dollars, five days","Three replies naming a figure at or above a hundred and fifty dollars"],
    ["2","Twenty requests to existing Brazilian representatives, as a prospective foreign client, asking for a monthly fee","Nothing","Five quotes with a median at or above three hundred dollars a month"],
    ["3","Twenty real ultrasound images through the pipeline, timed with a stopwatch","Nothing","Three minutes or less per unit, and eighteen of twenty shippable without rework"],
  ].forEach((r,i)=> trows.push(new TableRow({ children: r.map((v,j)=>cell(v,{w:tw[j],shade: i%2?ROW:undefined, size:18, color: j===0?MUTED:INK})) })));
  c.push(table(tw, trows));
  c.push(P("", { after: 200 }));
  c.push(P([{t:"One further test costs about thirty dollars and is worth running alongside them: ",b:true},{t:"three copies of the memoir in candidate four, printed and timed honestly. It answers a question no amount of further research can, which is whether a stranger will pay a hundred and forty-nine dollars for a book they cannot see before it is made."}]));
  c.push(P("Until one of these returns a number, every ranking in this document — including this one — is an argument rather than a finding.", { italics: true, color: SLATE, before: 160 }));
  return c;
}

Packer.toBuffer(doc).then(b => { fs.writeFileSync("/tmp/claude-0/-home-user-Random-Access-Memories/9aef20de-742c-52a2-b11a-a33d815230ea/scratchpad/doc/Ten_Business_Candidates.docx", b); console.log("written", b.length); });
