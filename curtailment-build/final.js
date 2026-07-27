const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, BorderStyle, AlignmentType, LevelFormat, PageBreak,
        ShadingType } = require('../curtailment/node_modules/docx');
const fs = require('fs');

const NAVY='1F3864', RULE='BFBFBF', GREY='595959', RED='C00000', GREEN='1E6B34',
      BOXBG='EEF3FA', AMBERBG='FFF7E6', W=9360;

const PR=(runs,o={})=>new Paragraph({
  spacing:{after:o.after??110, before:o.before??0, line:274},
  alignment:o.align, indent:o.indent, numbering:o.numbering,
  children:runs.map(r=>new TextRun({
    text:r.text, bold:r.bold, italics:r.italics, allCaps:r.caps,
    size:r.size??o.size??21, color:r.color??o.color??'000000', font:'Calibri'}))});

const H1=t=>new Paragraph({spacing:{before:300,after:130},
  border:{bottom:{style:BorderStyle.SINGLE,size:6,color:NAVY,space:4}},
  children:[new TextRun({text:t,bold:true,size:27,color:NAVY,font:'Calibri'})]});
const H2=t=>new Paragraph({spacing:{before:200,after:80},
  children:[new TextRun({text:t,bold:true,size:22,color:NAVY,font:'Calibri'})]});
const H3=t=>new Paragraph({spacing:{before:150,after:60},
  children:[new TextRun({text:t,bold:true,size:20,color:'000000',font:'Calibri'})]});
const B=t=>PR([{text:t}],{numbering:{reference:'bullets',level:0}});
const N=t=>PR([{text:t}],{numbering:{reference:'steps',level:0}});
const SAY=t=>PR([{text:'“'+t+'”',italics:true,color:'21406E'}],{indent:{left:340},before:50,after:110});

const box=(title,body,colour=NAVY,fill=BOXBG)=>new Table({
  columnWidths:[W], width:{size:W,type:WidthType.DXA},
  borders:{top:{style:BorderStyle.SINGLE,size:4,color:colour},
           left:{style:BorderStyle.SINGLE,size:18,color:colour},
           bottom:{style:BorderStyle.SINGLE,size:4,color:colour},
           right:{style:BorderStyle.SINGLE,size:4,color:colour},
           insideHorizontal:{style:BorderStyle.NONE,size:0,color:'FFFFFF'},
           insideVertical:{style:BorderStyle.NONE,size:0,color:'FFFFFF'}},
  rows:[new TableRow({children:[new TableCell({
    shading:{type:ShadingType.CLEAR,fill:fill,color:'auto'},
    margins:{top:130,bottom:130,left:190,right:150},
    children:[PR([{text:title,bold:true,size:22,color:colour}],{after:70}),
      ...body.map((t,i)=>PR([{text:t}],{after:i===body.length-1?0:90}))]})]})]});

const cell=(t,o={})=>new TableCell({
  shading:o.head?{type:ShadingType.CLEAR,fill:NAVY,color:'auto'}
        :(o.fill?{type:ShadingType.CLEAR,fill:o.fill,color:'auto'}:undefined),
  margins:{top:64,bottom:64,left:95,right:95},
  children:[PR([{text:t,bold:o.head||o.bold,
    color:o.head?'FFFFFF':(o.color??'000000'),size:o.size??18}],{after:0,align:o.align})]});
const table=(cols,rows)=>new Table({
  columnWidths:cols, width:{size:cols.reduce((a,b)=>a+b,0),type:WidthType.DXA},
  borders:{top:{style:BorderStyle.SINGLE,size:2,color:RULE},
           bottom:{style:BorderStyle.SINGLE,size:2,color:RULE},
           left:{style:BorderStyle.NONE,size:0,color:'FFFFFF'},
           right:{style:BorderStyle.NONE,size:0,color:'FFFFFF'},
           insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:RULE},
           insideVertical:{style:BorderStyle.NONE,size:0,color:'FFFFFF'}},
  rows:rows.map(r=>new TableRow({children:r}))});
const note=t=>PR([{text:t,size:17,color:GREY,italics:true}],{before:50,after:130});

const c=[];

/* ─────────────────────────── COVER ─────────────────────────── */
c.push(PR([{text:'SUTPHIN — INTERNAL',bold:true,size:18,color:GREY}],{after:36}));
c.push(PR([{text:'The Curtailment Desk',bold:true,size:46,color:NAVY}],{after:30}));
c.push(PR([{text:'Portaria Normativa MME nº 140/2026 — the complete brief',size:24,color:GREY}],{after:36}));
c.push(PR([{text:'Prepared for GC  ·  26 July 2026  ·  final, standalone',size:19,color:GREY,italics:true}],{after:200}));

c.push(box('HOW TO USE THIS',[
 'This is written to be read once, straight through, and to leave you able to hold three different conversations without preparation: with a GENERATOR (our client), with a FINANCIER (our capital), and with a LAWYER (our structure).',
 'Sections 1–7 build the understanding. Sections 8, 9 and 10 are the three conversations — each one is a script you can work from directly. Section 12 is the one-page cheat sheet; if you read nothing else before a call, read that.',
 'It supersedes every earlier draft. Where an earlier number is still circulating, section 2 says what changed and why, so you are not caught out by someone quoting an old figure back at you.'
]));

/* ─────────────────── 1. THE WHOLE THING ─────────────────── */
c.push(H1('1.  The whole thing, in one page'));

c.push(PR([{text:'Brazil built more wind and solar than its grid can carry. In 2025 the system operator ordered generators to stop producing 20.6 per cent of everything they could have made — about R$6.5bn of lost revenue. That is called ',},
{text:'curtailment',bold:true},{text:', or ',},{text:'constrained-off',italics:true},{text:'. Until now, almost none of it was compensated.'}]));

c.push(PR([{text:'On 21 July the federal government published the rulebook for paying part of it back. Every wind and solar generator in the country now has to make two decisions, and — this is the part almost the entire market has wrong — they are ten months apart.'}]));

c.push(table([1500,2400,5460],[
 [cell('',{head:true}),cell('When',{head:true}),cell('What it actually is',{head:true})],
 [cell('DECISION ONE',{bold:true}),cell('10 August 2026',{bold:true}),
  cell('File a form. It waives NOTHING. It preserves eligibility and — more valuable right now — suspends CCEE’s collection of what you already owe. Almost everyone should file.')],
 [cell('DECISION TWO',{bold:true,color:RED}),cell('mid-2027',{bold:true,color:RED}),
  cell('Sign the settlement. Irreversible. You surrender every curtailment claim through 25 Nov 2025, drop your lawsuits, and lose any injunction protecting you. This is the real decision, and it is taken with the numbers in hand.')]
]));

c.push(PR([{text:'Everything of commercial value happens in the gap between those two dates. Four things have to be worked out in that window, none of which a generator can do alone, and none of which anyone is currently selling. That gap is the business.'},],{before:80}));

c.push(box('WHAT WE HAVE THAT NOBODY ELSE DOES',[
 'The system operator publishes curtailment per plant, every half hour, back to 2021 — and separately publishes the reason code that decides whether each hour gets paid. Nobody had joined the two and rebuilt the claim.',
 'We have. 267 complexes. 25,326 GWh of eligible claim over exactly the compensated window, reconciled to the operator’s own published percentages within 0.2 points. Ownership joined through the regulator’s register at a 98.9 per cent match rate.',
 'So the first call is not a pitch. It is: “here is your own number, computed before you told us anything.” That is why the door opens.'
],GREEN));

/* ─────────────────── 2. WHAT CHANGED ─────────────────── */
c.push(H1('2.  What changed from the earlier drafts'));
c.push(PR([{text:'Four corrections, because people are still quoting the old versions and you need to be the one in the room who is current.'}]));

c.push(table([2600,3300,3460],[
 [cell('Point',{head:true}),cell('Earlier draft said',{head:true}),cell('Correct position',{head:true})],
 [cell('When money arrives',{bold:true}),cell('H2 2027'),
  cell('Late 2027 base case, H1 2028 outer limit. The Portaria fixes no calendar date — only a chain of relative deadlines gated on the operator’s final database around April 2027.')],
 [cell('What 10 August is',{bold:true}),cell('The decision point — waive or lose'),
  cell('It waives nothing. Filing is cheap optionality. The waiver happens at signature, mid-2027. This is the single most valuable insight we have.')],
 [cell('Garantia física',{bold:true}),cell('An extra cost — curtailment erodes it'),
  cell('The opposite. Art. 10 counts curtailed volume as generated, which PROTECTS the plant’s future contractable volume. It is a benefit and belongs on the positive side.')],
 [cell('The capital line',{bold:true}),cell('R$20–60m of gross spread'),
  cell('Withdrawn. It applied a discount to gross compensation, and gross compensation is not what anyone receives. Section 6 explains why, and section 7 explains what we do instead.')]
]));

c.push(note('If someone quotes “R$3.3bn” at you as fact: no primary document states any pool figure. MME says values are not yet defined. Independent estimates run R$2.7–3.5bn. Use it as an order of magnitude, never as a number.'));

/* ─────────────────── 3. THE SITUATION ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('3.  The situation — what you need to know cold'));

c.push(H2('How bad the problem is'));
c.push(table([1900,2000,2200,3260],[
 [cell('Year',{head:true}),cell('Curtailed',{head:true,align:AlignmentType.RIGHT}),
  cell('Share of output',{head:true,align:AlignmentType.RIGHT}),cell('Lost revenue',{head:true,align:AlignmentType.RIGHT})],
 [cell('2023'),cell('3,150 GWh',{align:AlignmentType.RIGHT}),cell('3.6%',{align:AlignmentType.RIGHT}),cell('—',{align:AlignmentType.RIGHT})],
 [cell('2024'),cell('12,336 GWh',{align:AlignmentType.RIGHT}),cell('9.3%',{align:AlignmentType.RIGHT}),cell('R$1.6bn',{align:AlignmentType.RIGHT})],
 [cell('2025',{bold:true}),cell('36,168 GWh',{bold:true,align:AlignmentType.RIGHT}),cell('20.6%',{bold:true,align:AlignmentType.RIGHT}),cell('R$6.5bn',{bold:true,align:AlignmentType.RIGHT})],
 [cell('2026 to 25 Jul'),cell('17,362 GWh',{align:AlignmentType.RIGHT}),cell('18.8%',{align:AlignmentType.RIGHT}),cell('—',{align:AlignmentType.RIGHT})]
]));
c.push(note('Volumes computed by us from ONS half-hourly open data. Revenue figures are Volt Robotics — the only continuous published series in Brazil, and worth knowing that every R$ number in the market traces back to that one consultancy. 84% of the damage is in the Northeast; Rio Grande do Norte alone is 44% of the eligible claim.'));

c.push(H2('The three reason codes — this is the heart of it'));
c.push(PR([{text:'The system operator codes every curtailed hour into exactly one of three buckets. Only two get paid. Learn these three Portuguese terms; they are the vocabulary of every conversation you will have.'}]));
c.push(table([3300,1300,1400,3360],[
 [cell('Code',{head:true}),cell('Share',{head:true,align:AlignmentType.RIGHT}),cell('Paid?',{head:true}),cell('What it means',{head:true})],
 [cell('Indisponibilidade externa',{bold:true}),cell('13%',{align:AlignmentType.RIGHT}),cell('YES, in full',{bold:true,color:GREEN}),cell('A fault on the transmission network outside the plant.')],
 [cell('Confiabilidade elétrica',{bold:true}),cell('41%',{align:AlignmentType.RIGHT}),cell('YES, in full',{bold:true,color:GREEN}),cell('Grid stability or loading limits — no equipment failure.')],
 [cell('Sobreoferta',{bold:true}),cell('46%',{align:AlignmentType.RIGHT}),cell('NO. Nothing.',{bold:true,color:RED}),cell('Too much power, nowhere to put it. Excluded by statute.')]
]));
c.push(note('Split for 1 Sep 2023 – 25 Nov 2025, from ANEEL’s own voto in Processo 48500.000231/2026-56. By the first half of 2026 the non-compensable share had risen to roughly 65%. One favourable detail worth knowing: where codes collide in the same hour, indisponibilidade externa wins, then confiabilidade — sobreoferta loses (Art. 5º §5º).'));

c.push(H2('Where the money comes from — and why it is often not cash'));
c.push(PR([{text:'This is the single most misunderstood mechanic, and understanding it is what will mark you out as having actually read the instrument.'}]));
c.push(PR([{text:'The compensation is not funded by the Treasury or by consumers. It is funded by cancelling debts the generators themselves already owe. Many wind and solar farms under-delivered against their regulated contracts precisely because they were curtailed — and they owe CCEE penalties for that shortfall. The settlement first treats the curtailed energy as if it had been delivered, which wipes out those penalties.'}]));
c.push(PR([{text:'So for a large part of the market, this is a book entry, not a cheque. Sector-wide, roughly R$3.3bn of credit nets against roughly R$6bn of penalties owed — the sector stays net owing even after full compensation.',bold:true}]));

c.push(H3('The waterfall, in order (Cláusula Quinta)'));
c.push(table([700,3400,5260],[
 [cell('',{head:true}),cell('Tranche',{head:true}),cell('What the generator actually gets',{head:true})],
 [cell('1'),cell('Volume committed to CCEAR-D / CER'),cell('DEBT RELIEF. Treated as delivered, cancels the shortfall penalty. No money moves.',{color:RED})],
 [cell('2'),cell('Contractual residual'),cell('Valued on the contract’s own terms. May or may not be cash.')],
 [cell('3'),cell('UNCOMMITTED volume',{bold:true}),cell('CASH, at the spot price (PLD) of that submarket. This is the only tranche anyone can lend against.',{bold:true,color:GREEN})],
 [cell('4'),cell('Proinfa volume'),cell('CASH, at the Proinfa contract price, paid via ENBPar.',{color:GREEN})],
 [cell('5'),cell('Set-off'),cell('Anything already received under existing rules is deducted.')]
]));
c.push(box('THE QUESTION THAT OPENS EVERY CALL',[
 'Whether a generator gets cash or a book entry depends entirely on how much of its curtailed volume was committed to regulated contracts. That sits in CCEE data behind a login. It is unobtainable from outside — no consultant, no bank, no rating agency can see it.',
 'Only the generator knows. Which is exactly why they have to talk to us, and why this is the first question on every call.'
]));

/* ─────────────────── 4. THE FOUR THINGS ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('4.  The four things worth money in the gap'));

c.push(H2('4.1  The classification is a black box — and it decides everything'));
c.push(PR([{text:'Whether an hour is coded confiabilidade or sobreoferta is the difference between full payment and nothing. The method is not published in a form anyone can reproduce.'}]));
c.push(B('Volt Robotics tested the Ministry’s own SOSIN formula against the operator’s calculation and found it produced 143 per cent more sobreoferta.'));
c.push(B('The share coded non-compensable rose from 27% in 2023 to 65.5% in the first half of 2026. Either the physics changed dramatically, or the coding did.'));
c.push(B('There is a formal contestation window — ten days after the operator’s consistency analysis, around March 2027. After that the generator accepts the classification irretratavelmente.'));
c.push(PR([{text:'So there is a dated, adversarial window in which a well-evidenced challenge converts straight into cash, and essentially nobody is preparing for it. On a R$200m claim, moving five points of volume from sobreoferta to confiabilidade is worth about R$10m to the client.',bold:true},],{before:70}));
c.push(note('Honest limit: the procedure for rebuilding wind and solar reference data covers events only to 10 February 2025, while the compensated window runs to 25 November 2025. That constrains the reference-data half of the work. It does not constrain the classification challenge, which is a separate mechanism and is where the value is.'));

c.push(H2('4.2  Nobody knows which PLD applies'));
c.push(PR([{text:'Uncommitted volume is paid at the spot price. The settlement never says whether that means the price at the time of the cut or at the date of payment. Lefosse flagged it; nobody has resolved it.'}]));
c.push(PR([{text:'Not a technicality. Northeast spot price sat at its floor of about R$58/MWh through most of early 2025 and averaged R$227/MWh across 2026. On a large book the answer is worth nine figures, and it should be settled before signature.'}]));

c.push(H2('4.3  Signing turns a suspended liability into an enforceable one'));
c.push(PR([{text:'The most dangerous clause in the instrument, and the one that will most impress a CFO when you raise it unprompted.'}]));
c.push(PR([{text:'On signing, the generator authorises CCEE to resume billing the shortfall penalties it owes, and undertakes not to oppose provisional court orders against the Union or CCEE. Simultaneously it surrenders the protective effect of any injunction it currently holds.'}]));
c.push(PR([{text:'For a generator whose court order is the only thing keeping a nine-figure liability off its balance sheet, signing means accepting an enforceable debt today against a credit that pays in late 2027. Worse: if it then fails to prove it filed the required court petition within ten days, the compensation is suspended while every other obligation survives. It is possible to end up having waived, being billed, and not being paid.',bold:true}]));

c.push(H2('4.4  The veto is still alive, and signing surrenders it for nothing'));
c.push(PR([{text:'When the law was sanctioned in November 2025, the government vetoed a much broader provision that would have compensated all externally caused curtailment except sobreoferta, retroactively. Congress pulled the override from its agenda on 18 June 2026 and has still not voted. As of today it is neither maintained nor overridden.'}]));
c.push(PR([{text:'The waiver is bounded by the date of the event, not by which law creates the right. A generator that signs and then watches Congress override the veto has given away the enlarged claim for free. Nobody is pricing that option.'}]));

c.push(H2('4.5  On the other side of the ledger — Article 10 helps'));
c.push(PR([{text:'Curtailed volume counts as generation verificada for the annual garantia física revision, expressly whether compensable or not. That PROTECTS the plant: it stops the physical guarantee — and therefore the volume it may contract in future — being cut for energy it was ordered not to produce. It covers sobreoferta too, so it is the one place uncompensated volume still earns something.'}]));
c.push(PR([{text:'The methodology is unpublished, so it cannot be quantified yet. Treat it as an option with a favourable direction, on the positive side of the decision.'}]));

/* ─────────────────── 5. OUR DATA ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('5.  Our data edge, and where the claim sits'));
c.push(PR([{text:'We computed the eligible claim — indisponibilidade externa plus confiabilidade elétrica only, over exactly the compensated window — for every complex in the country. 267 complexes, 25,326 GWh. We also quantified the 23,213 GWh of sobreoferta they are being asked to waive and will never be paid for.'}]));

c.push(table([2700,1500,1500,3660],[
 [cell('Group',{head:true}),cell('Eligible GWh',{head:true,align:AlignmentType.RIGHT}),
  cell('Est. claim',{head:true,align:AlignmentType.RIGHT}),cell('How to read it',{head:true})],
 [cell('Casa dos Ventos',{bold:true}),cell('4,754',{align:AlignmentType.RIGHT}),cell('R$619m',{align:AlignmentType.RIGHT}),
  cell('Largest holder in Brazil, 18.8% of the pool. Raised US$1.1bn in June — needs advice, not our money.')],
 [cell('Engie Brasil'),cell('1,776',{align:AlignmentType.RIGHT}),cell('R$231m',{align:AlignmentType.RIGHT}),
  cell('Discloses curtailment only in percentages, never an R$ figure. Its São Pedro IV project is the most distressed credit we found.')],
 [cell('Enel Green Power'),cell('1,616',{align:AlignmentType.RIGHT}),cell('R$211m',{align:AlignmentType.RIGHT}),cell('Decision may sit in Rome. Find who signs in Brazil.')],
 [cell('Echoenergia / Equatorial'),cell('1,092',{align:AlignmentType.RIGHT}),cell('R$142m',{align:AlignmentType.RIGHT}),
  cell('Already litigating — two of the twelve suits. Must actively choose to abandon them.')],
 [cell('Serena'),cell('1,057',{align:AlignmentType.RIGHT}),cell('R$138m',{align:AlignmentType.RIGHT}),cell('Highest proportional EBITDA hit of any rated name — 11%.')],
 [cell('Voltalia'),cell('920',{align:AlignmentType.RIGHT}),cell('R$120m',{align:AlignmentType.RIGHT}),
  cell('THE ONLY COMPANY TO HAVE BOOKED REAL MONEY — R$175m recognised in Q2 2026. Call to learn, not to sell.')],
 [cell('Elera / Brookfield'),cell('419',{align:AlignmentType.RIGHT}),cell('R$54m',{align:AlignmentType.RIGHT}),
  cell('Holds an actual injunction, so has the most to surrender by signing.')]
]));
c.push(note('Estimates apply the R$130/MWh implied by the reported pool — modelled, not disclosed. The full ranking of all 267 complexes with ownership confidence flags is in the accompanying workbook. Ownership is inferred from naming conventions in some cases; respect the confidence flags before naming a group as fact.'));

/* ─────────────────── 6. THE MONEY ─────────────────── */
c.push(H1('6.  The money, honestly'));
c.push(H2('Three things that make this smaller than the headline'));
c.push(N('It is mostly a book entry. Only uncommitted volume produces cash. Sector-wide the credit does not even cover what generators owe.'));
c.push(N('Nobody outside can tell who gets cash. It is the decisive variable and it is invisible without the generator’s own contract book.'));
c.push(N('The litigation being waived is weak. Twelve suits, none with a surviving injunction; the one appellate win was suspended by the Superior Court six weeks later and never implemented. So for most generators the honest advice is that the waiver is cheap — which is useful, correct, and not what a vendor would tell them.'));

c.push(H2('What the business earns'));
c.push(table([2600,1900,1700,3160],[
 [cell('Line',{head:true}),cell('When',{head:true}),cell('Range',{head:true}),cell('What has to be true',{head:true})],
 [cell('Advisory — classification audit, waiver analysis, contestation'),cell('Aug 26 – mid 27'),cell('R$5–15m'),
  cell('8–15 mandates at R$300k–1.5m. We win the first five on the strength of the data.')],
 [cell('Success fee on reclassified volume'),cell('Mar–Jun 2027'),cell('R$3–12m'),
  cell('10–20% of value created. The contestation window works as drafted.')],
 [cell('Capital — lending against the cash tranche'),cell('From mid-2027'),cell('NOT YET SIZED',{bold:true,color:RED}),
  cell('Deliberately blank. The denominator is positive net cash after the waterfall, and nobody has measured it. Five real books fix that.')]
]));

c.push(H2('Who we lend to, and who we only advise'));
c.push(table([2200,3600,3560],[
 [cell('Segment',{head:true}),cell('Test',{head:true}),cell('What we sell',{head:true})],
 [cell('Cash-rich',{bold:true}),cell('Over ~60% converts to cash — merchant, ACL or Proinfa heavy'),cell('Advisory plus financing')],
 [cell('Mixed'),cell('20–60% converts'),cell('Advisory; finance only the cash tranche')],
 [cell('Debt-relief dominant'),cell('Under 20% converts'),cell('Advisory and success fee. Lend nothing.')],
 [cell('Net payer',{bold:true,color:RED}),cell('Liability survives and the injunction is gone'),cell('Sign / do-not-sign advice only. Our highest-value advice, our worst loan.')],
 [cell('Encumbered'),cell('Lender lien, RJ, disputed title'),cell('Advisory until resolved')]
]));
c.push(PR([{text:'Note the order this creates: cashability comes before distress. A distressed generator with no cash tranche is a good mandate and a terrible loan. A solvent merchant generator with R$30m of expected spot-priced cash is the better transaction even with no liquidity problem at all.',bold:true},],{before:70}));

/* ─────────────────── 7. THE STRUCTURE ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('7.  How we actually get paid — the structure'));

c.push(box('THE UNLOCK — CCEE NEVER HAS TO PAY US',[
 'Every earlier version asked: can CCEE be made to recognise Sutphin as payee? That is genuinely unresolved and may stay that way for months — CCEE’s rules for this scheme are not final until September 2026, and the payment is a netting entry inside the generator’s own settlement account, not an invoice a lockbox intercepts.',
 'We do not need it. CCEE pays the generator, into the generator’s own account, same CNPJ, exactly as today. We take a security interest OVER THAT ACCOUNT rather than redirecting the payment. That turns an unresolved regulatory question into ordinary Brazilian secured lending — which is work this desk already knows how to do.'
],GREEN));

c.push(H2('No, it cannot be sold on a secondary market — and that is exactly why the structure above is the answer'));
c.push(PR([{text:'Worth stating plainly, because it will come up: there is no secondary market for this credit today, and CCEE’s own systems will not create one. Its GSF settlement mechanism — the one real precedent for a litigant-generator renouncing a lawsuit in exchange for value, run in August 2025 and moving R$1.4bn — expressly bars any payment except into the buyer’s own registered account, and restricted eligible buyers to registered CCEE hydro agents only. No fund, bank or outside financier has ever been let in. No FIDC, CRI or CRA has ever held a credit of this type as collateral.'}]));
c.push(PR([{text:'That is not a reason to stand down — it is confirmation that the right move is the one in the box above: never ask CCEE to pay a third party. We do not need a market, because CCEE keeps paying the registered agent exactly as always.',bold:true}]));
c.push(PR([{text:'And the structure itself is not a theory — CCEE has already built it, for its own financing. In April 2022 CCEE raised R$5.5bn against its own reimbursement right from the CDE, using a cessão fiduciária, a dedicated blocked account at Bradesco, a servicer, and an irrevocable mandate. That is the identical shape of what we build around a generator. CCEE proved the mechanism works inside its own ecosystem; we are applying it one level down, to an agent’s account rather than CCEE’s own.'}]));

c.push(H2('Three instruments, all standard'));
c.push(N('A cessão fiduciária over the specific settlement receivable — Lei 4.728/1965 art. 66-B — perfected by registration and notice to CCEE and MME.'));
c.push(N('A conta vinculada in the generator’s own name and CNPJ, blocked at the account bank. This is exactly what satisfies CCEE’s same-holder requirement, because the account holder does not change.'));
c.push(N('An irrevocable mandate letting us sweep that account the moment CCEE settles into it.'));

c.push(PR([{text:'We advance only against the ',},{text:'Verified Net Cash Receivable',bold:true},
{text:' — the uncommitted volume at spot plus Proinfa, IPCA-adjusted, net of prior payments and deductions. Never against the debt-relief tranche, because there is no cash behind it to secure.'}],{before:70}));

c.push(H2('The one open legal question — and it is narrow'));
c.push(PR([{text:'Cessão fiduciária is extraconcursal: it survives if the generator enters recuperação judicial during the wait (Lei 11.101/2005 art. 49 §3). But that protection is contested when the secured creditor is not a financial institution (STJ REsp 1.833.824/RS).'}]));
c.push(PR([{text:'So the question is not the open-ended “is this claim assignable”, which the Portaria’s silence makes unanswerable. It is: does our protection hold if we lend directly, or do we need a licensed institution as formal secured party with us behind it economically? One lawyer, one week. If yes, we lend directly. If uncertain, a bank sits in front — that costs a spread, not the deal.',bold:true}]));

c.push(H2('The worst case is more reassuring than it sounds'));
c.push(PR([{text:'One precision worth having exactly right. The Termo being a título executivo extrajudicial does not, by itself, keep it out of the federal precatório queue forever — that is a slight overstatement in how this has been described up to now. What actually matters is which path is in play.'}]));
c.push(PR([{text:'On the intended path — CCEE’s administrative recontabilização — no court is ever involved, so precatório never enters into it; this is a private clearing process, not a judicial payment order. Only if the União ever breached and a generator had to sue to enforce the Termo would CPC art. 910 apply, and unpaid amounts would ultimately be requisitioned as a precatório.'}]));
c.push(PR([{text:'That fallback is the reassuring part, not the risk: assignment of a credit that is already in a precatório is expressly permitted without the debtor’s consent, under art. 100 §13 of the Constitution, and is a mature, well-precedented market in Brazil. So the one scenario where enforcement genuinely gets difficult — a breach by the União — is also the one scenario where assigning the resulting credit becomes easiest.',bold:true}]));

c.push(H2('Risks we accept and price, rather than solve'));
c.push(B('The generator’s own ongoing compliance. It must file the renunciation within ten days of signing, never oppose a provisional order, and cure any default within five days — or the compensation is suspended while every other obligation survives. We are underwriting eighteen months of the borrower’s behaviour, not just the Union’s credit. Priced and monitored like any covenant.'));
c.push(B('Which is precisely why we do not lend into a generator with live recuperação judicial exposure. Rio Alto is the obvious example: a real claim, and no ability to survive to collect it.'));
c.push(B('If we ever use an FIDC, whether this credit qualifies as an eligible direito creditório under CVM Resolução 175 is untested. A wrapper choice does not resolve it — so start with a simpler vehicle.'));

/* ─────────────────── 8. GENERATOR ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('8.  Conversation one — talking to a generator'));
c.push(PR([{text:'Your client. Call the ',},{text:'Diretor de Regulação',bold:true},
{text:', not the CEO — in almost every company there is one named person who owns dealings with ONS, ANEEL and CCEE, and they will know within thirty seconds whether you have read the instrument or a law-firm summary.'}]));

c.push(H2('Open with the correction, not the offer'));
c.push(SAY('You have until 10 August to file under Portaria 140. I am not calling to sell you anything. I am calling because most people are treating 10 August as the decision, and it is not — filing waives nothing, the waiver only bites when you sign, and that is mid-2027. What matters in between is whether your cut hours are correctly classified, and almost nobody is auditing that.'));
c.push(PR([{text:'That single paragraph does three things: it is true, it is useful to them immediately, and it proves you have read the primary text.'}]));

c.push(H2('The four questions to ask'));
c.push(N('What share of your curtailed volume was committed to CCEAR-D or CER? (Decides cash versus book entry — the whole conversation turns on this.)'));
c.push(N('What do you currently owe CCEE in delivery-shortfall ressarcimentos? (We need the net position, not the gross claim.)'));
c.push(N('What is your sobreoferta volume across the window, and what have you assumed it is worth? (What they are giving up.)'));
c.push(N('Are you in any of the twelve suits, or in the ABEEólica/ABSOLAR collective action? (Decides how expensive the waiver is for them specifically.)'));

c.push(H2('The four objections, and the answers'));
c.push(H3('“Our lawyers are on it.”'));
c.push(SAY('Only two firms have published anything on this, and nobody has filed for clarification. Ask your lawyers one question: which PLD applies to our uncommitted volume — the date of the cut, or the date of payment? If they have an answer, you do not need me.'));
c.push(H3('“ABEEólica is handling it.”'));
c.push(SAY('Elbia Gannoum has said publicly she cannot guarantee adhesion of 100 per cent or of 50 per cent. And the settlement excludes you from the collective action individually, by name. Whether that trade works for you depends on your contract mix and your classification split — no association can answer that member by member.'));
c.push(H3('“Why do you care?”'));
c.push(SAY('We finance receivables against solvent obligors in Brazil. This creates a large one with a two-year wait attached. The fastest way to understand it properly is to work through real books with people who own the assets.'));
c.push(H3('“Send me a deck.”'));
c.push(SAY('I would rather send you your own numbers. We have already built the eligible-volume base for every complex in the country from public grid data. Tell me which complexes are yours and you will have your line by the end of the week.'));

c.push(box('WHAT NOT TO SAY',[
 'Do not offer to buy their claim. There is no settlement, no quantified amount and no enforceable title until mid-2027 — there is nothing to buy yet.',
 'Do not say the credit is assignable. The Portaria contains zero references to cessão, transferência, oneração, penhor or caução. If asked, say exactly that, then explain we take security over their account instead.',
 'Do not quote R$3.3bn as fact, and do not quote a purchase price. We do not have one until we see their book.',
 'Do not tell them whether to sign. We quantify both sides. For most, the honest answer today is: file in August, audit your classification in between, decide in 2027.'
],RED,AMBERBG));

/* ─────────────────── 9. FINANCIER ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('9.  Conversation two — talking to a financier'));
c.push(PR([{text:'For a capital partner, a private-credit fund, or an internal committee. They will care about exactly four things: what the asset is, who owes it, how you get paid, and what kills it.'}]));

c.push(H2('The asset, in their language'));
c.push(table([2600,6760],[
 [cell('What',{head:true}),cell('Position',{head:true})],
 [cell('Obligor'),cell('The União, via a Termo de Compromisso that is expressly a título executivo extrajudicial under art. 784 II/III of the Civil Procedure Code. Forum: Federal Court in Brasília.')],
 [cell('Indexation'),cell('IPCA from the date of each curtailment event through to actual payment. No interest — the instrument is silent on juros.')],
 [cell('Credit enhancement'),cell('Expressly carved out of the short-term market’s default-sharing pool, so it cannot be eroded by other agents’ defaults. That is unusual and worth stating.')],
 [cell('Tenor'),cell('Payment late 2027 base case, H1 2028 outer limit — roughly 16–24 months from a mid-2027 signature.')],
 [cell('Our security'),cell('Cessão fiduciária over the receivable plus a blocked account in the borrower’s own name, swept irrevocably. We never need CCEE to recognise us as payee.')],
 [cell('What we lend against'),cell('Only the Verified Net Cash Receivable — uncommitted volume at spot plus Proinfa. Never the debt-relief tranche.')]
]));

c.push(H2('The three questions they will ask'));
c.push(H3('“Why is this not just a discounted receivable trade at 15%?”'));
c.push(PR([{text:'Because at a 15% discount over 18 months the gross return is about 11%, and Selic is around 14.25%. It does not clear the risk-free rate before legal cost, servicing, timing risk or the borrower-compliance risk below. Pricing has to reflect a novel, illiquid, legally untested instrument — and we will not set it until we have seen a real contract book.'}]));
c.push(H3('“What actually kills this?”'));
c.push(PR([{text:'Two things, and we should name them first. One: the borrower breaches its own ongoing obligations under the settlement — misses the ten-day court filing, opposes a provisional order — and the compensation is suspended while its debts survive. Two: our security is not extraconcursal because we are not a bank, and the borrower enters recuperação judicial. The first is priced and monitored; the second is the one legal question we are resolving now.'}]));
c.push(H3('“How big is the market?”'));
c.push(PR([{text:'Honest answer: unknown, and anyone who gives you a number is guessing. The eligible claim base is 25,326 GWh and we have computed it complex by complex. But the portion that converts to cash rather than debt relief cannot be seen from outside. Five real contract books turn that from a guess into a number, and that is what the next fortnight is for.'}]));
c.push(H3('“Can we just buy this on a secondary market instead of structuring a loan?”'));
c.push(PR([{text:'No, and we checked properly rather than assumed. CCEE ran a comparable litigant-renunciation-for-value mechanism in August 2025 for hydrological-risk credits — R$1.4bn, and it restricted eligible buyers to registered CCEE agents only, paying value through a concession extension rather than cash to an outside financier. No FIDC, CRI or CRA has ever held a credit of this type. There is no market to buy into, which is exactly why we structure a secured advance instead — it requires no market and no cooperation from CCEE at all.'}]));

c.push(box('THE LINE THAT LANDS',[
 'Fitch put 13 Brazilian renewable project financings on Rating Watch Negative explicitly on curtailment, downgraded six, and left eleven on negative outlook to 2030 — and its rating cases ASSUME ZERO COMPENSATION.',
 'So every real these vehicles actually collect is upside no rating currently credits. For Tupi at a 1.03x minimum coverage ratio, barred from distributing below 1.25x, or Engie’s São Pedro IV at 0.49x with negative operating cash flow, that is the difference between a downgrade and a stabilisation.',
 'That is why a project-finance CFO will pay for this and a healthy holding company will not.'
],GREEN));

/* ─────────────────── 10. LAWYER ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('10.  Conversation three — instructing a lawyer'));
c.push(PR([{text:'Do not ask for a general opinion on assignability. The Portaria is silent, so the answer will be long, expensive and inconclusive. Scope it narrowly. This is what to send.'}]));

c.push(box('THE INSTRUCTION',[
 'We intend to advance cash to a wind or solar generator, secured by a cessão fiduciária over its compensation claim under Portaria Normativa MME 140/2026, plus a conta vinculada in the generator’s own name and CNPJ, plus an irrevocable sweep mandate. CCEE continues to pay the generator exactly as today — we are NOT asking CCEE to recognise us as payee.',
 'QUESTION: Lei 11.101/2005 art. 49 §3 makes cessão fiduciária extraconcursal. That protection is reported as contested where the secured creditor is not a financial institution (STJ REsp 1.833.824/RS). Does it hold for us lending directly? If not, what is the minimum structure that restores it — a licensed institution as titular secured party with us behind it economically, or something else?',
 'Also confirm: (a) that a conta vinculada in the generator’s own CNPJ satisfies CCEE’s existing same-holder requirement, since ownership does not change; and (b) whether the obligor being the União, operationalised through CCEE recontabilização, changes the analysis versus an ordinary commercial receivable.',
 'Useful precedent to pull first: CCEE itself executed a cessão fiduciária of its own CDE reimbursement right in April 2022, to finance R$5.5bn of Escassez Hídrica lending — dedicated blocked account at Bradesco, a servicer, an irrevocable mandate. It is a public instrument and a working template for exactly this structure, one level up from where we are applying it.',
 'One week. This is a scoping question, not a transactional opinion — the documentation work happens once we have a book to lend against.'
]));

c.push(H2('Two further questions worth commissioning at the same time'));
c.push(N('Which PLD applies to uncommitted volume — the price at the time of the cut, or at the date of payment? The instrument does not say, and on a large book the answer is worth nine figures. Whoever answers this first has something to sell to the whole market.'));
c.push(N('Does the waiver in Cláusula Sétima, drafted as covering all “eventos de restrição de geração”, extend to sobreoferta claims even though sobreoferta is expressly excluded from compensation? The object clause is narrower than the waiver wording. Assume the broader reading until told otherwise.'));

c.push(H2('What to tell them we already know, so they do not bill for it'));
c.push(B('The Portaria contains zero occurrences of cessão, cedente, cessionário, transferência, oneração, penhor, caução or alienação. We have run the search. It is silent, not prohibitive.'));
c.push(B('The Termo is a título executivo extrajudicial under art. 784 II/III CPC, forum Federal Court in Brasília, and the hierarchy is Termo > Portaria > CCEE rules.'));
c.push(B('Compensation is carved out of short-term-market default sharing under Art. 6º §6º.'));
c.push(B('There is no secondary market for this credit and CCEE will not pay a non-agent third party directly — confirmed against CCEE’s own GSF settlement mechanism (Edital 01/2025), which restricted buyers to registered agents. We are not asking for a market; we are asking to secure our position on the generator’s own account after CCEE pays it as usual.'));
c.push(B('On the intended administrative path (CCEE recontabilização) no court and no precatório is involved at all. Precatório only becomes relevant if the União breaches and the Termo has to be enforced by suit under CPC art. 910 — and even then, a credit inside a precatório is freely assignable without the debtor’s consent under CF art. 100 §13, which is a reassuring fallback, not a new risk.'));

/* ─────────────────── 11. FIRST TWO WEEKS ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('11.  The first two weeks'));
c.push(PR([{text:'The objective is not capital and it is not ten calls. It is mandates and data — five complete contract books that let us measure cash conversion for the first time.'}]));
c.push(N('Work the list properly — forty to sixty groups, not ten. The workbook ranks 40 named groups covering 73% of the pool, each with its own computed number. Target twenty senior conversations and ten to fifteen signed mandates.'));
c.push(N('Sell option preservation, not analysis. A short engagement: confirm eligibility, get the filing right, check the correct titular, CNPJ, CEG and outorga, inventory litigation and liens, and secure exclusivity on the decision work. R$25–40k per group, credited in full against the later mandate. Waive it for a multi-plant group that signs exclusivity on the spot.'));
c.push(N('Get five books of five different shapes — one CCEAR-D/CER-heavy, one merchant-heavy, one hybrid, one Proinfa, one judicially protected. Everything downstream depends on these.'));
c.push(N('One call to Volt Robotics. They own the classification data and the sector’s credibility on it; they have no capital. Decide whether they are partner or competitor before someone else does.'));
c.push(N('One lawyer on the narrow question in section 10. Nothing waits on it — all three outcomes leave the advisory business intact.'));

c.push(H2('The five calls to make first'));
c.push(table([2500,2900,3960],[
 [cell('Who',{head:true}),cell('Where',{head:true}),cell('Why them first',{head:true})],
 [cell('Elbia Gannoum',{bold:true}),cell('Presidente Executiva, ABEEólica'),
  cell('One call reaches ~40 member companies. She has said publicly that adhesion is uncertain and company-by-company — that sentence is your opening.')],
 [cell('Paulo Abranches',{bold:true}),cell('CEO, Ibitu Energia'),
  cell('Its audited accounts already state R$54.7m of expected compensation and its Tupi vehicle runs a 1.03x coverage ratio. They have done the work and cannot distribute. Open with their own number.')],
 [cell('Priscila Rochinha Lino'),cell('Diretora Regulatório, Auren'),
  cell('Auren has publicly said it expects R$250m. Best-quantified conversation available.')],
 [cell('Cristiano de Lima Logrado'),cell('Diretor de Regulação e Mercado, Equatorial'),
  cell('Covers both Equatorial and Echoenergia, including the two filed lawsuits. One call, two books.')],
 [cell('Donato da Silva Filho'),cell('CEO, Volt Robotics'),
  cell('Owns the classification data the whole market quotes. Partner or competitor — decide early.')]
]));

/* ─────────────────── 12. CHEAT SHEET ─────────────────── */
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(H1('12.  Cheat sheet — read this before any call'));

c.push(H2('The dates'));
c.push(table([3000,6360],[
 [cell('10 August 2026',{bold:true}),cell('Deadline to file the manifestação prévia de interesse, via the CELEBRA portal. Waives nothing.')],
 [cell('1 Sep 2023 – 25 Nov 2025',{bold:true}),cell('The curtailment window being compensated. Nothing outside it counts.')],
 [cell('~September 2026'),cell('CCEE publishes its adapted commercialisation rules.')],
 [cell('~November 2026'),cell('The system operator delivers its calculation tool.')],
 [cell('~March 2027',{bold:true}),cell('Contestation window — ten days. This is where classification is challenged.')],
 [cell('~April–May 2027'),cell('Operator’s final database, then CCEE publishes per-plant volumes.')],
 [cell('mid-2027',{bold:true,color:RED}),cell('Signature of the Termo. The irreversible act.')],
 [cell('late 2027 / H1 2028',{bold:true,color:RED}),cell('Payment. 180 days after the signature deadline.')]
]));

c.push(H2('The numbers'));
c.push(table([3000,6360],[
 [cell('20.6%',{bold:true}),cell('Share of available wind and solar curtailed in 2025.')],
 [cell('R$6.5bn'),cell('Lost revenue in 2025. R$1.6bn in 2024.')],
 [cell('25,326 GWh',{bold:true}),cell('Eligible claim across 267 complexes — our computation, the number nobody else has.')],
 [cell('23,213 GWh'),cell('Sobreoferta volume being waived and never paid for.')],
 [cell('46 / 41 / 13'),cell('Percentage split: sobreoferta (unpaid) / confiabilidade (paid) / indisponibilidade externa (paid).')],
 [cell('~R$130/MWh'),cell('Implied compensation price. Use as an order of magnitude only.')],
 [cell('R$3.3bn vs R$6bn',{bold:true}),cell('Credit versus what generators owe CCEE. The sector stays net owing.')],
 [cell('R$57.31'),cell('The 2026 spot-price floor in the Northeast. Midday hours sit there 56% of the time.')]
]));

c.push(H2('The five terms to use correctly'));
c.push(table([3000,6360],[
 [cell('Constrained-off / curtailment',{bold:true}),cell('Being ordered to stop generating because the grid cannot take it.')],
 [cell('Sobreoferta',{bold:true}),cell('Oversupply. The biggest category and the one that is never compensated.')],
 [cell('Confiabilidade elétrica',{bold:true}),cell('Grid stability limits. Compensated in full.')],
 [cell('Termo de Compromisso',{bold:true}),cell('The settlement. Signing it is the irreversible act, mid-2027.')],
 [cell('Garantia física',{bold:true}),cell('The volume a plant is allowed to contract. Article 10 protects it — a benefit, not a cost.')]
]));

c.push(H2('The three sentences that establish credibility fastest'));
c.push(B('“Filing on 10 August waives nothing — the renúncia only happens when you sign the Termo, and that cannot be before mid-2027.”'));
c.push(B('“The Termo never says whether uncommitted volume is valued at the PLD on the date of the cut or the date of payment. Has anyone told you which?”'));
c.push(B('“Cláusula Oitava means signing lets CCEE resume billing you while you wait until 2028 to be paid. Have you modelled that?”'));

/* ─────────────────── 13. WHAT THIS IS NOT ─────────────────── */
c.push(H1('13.  What this is not'));
c.push(B('It is not the answer to the original mandate. It does not compound, it has a defined end, and the capital line does not open until mid-2027. A good campaign, not a business that runs itself.'));
c.push(B('It is not recurring. Sobreoferta causes most curtailment and is excluded by statute, so nothing comparable is being created behind it.'));
c.push(B('It is not a distressed-debt trade today. No settlement, no quantified amount, no enforceable title until mid-2027.'));
c.push(B('It is not blue ocean forever. Only two firms have published on the Portaria and nobody has filed for clarification — but the classification audit is replicable by anyone with the same data and the will to build it.'));

c.push(H1('14.  The thesis, as you should state it'));
c.push(box('CANONICAL — use this wording with anyone',[
 'Sutphin uses the 10 August deadline to win exclusive mandates, not to buy unverified claims. We preserve generators’ eligibility, then build a plant-level model separating CCEE liability relief, contractual residuals, uncommitted volume valued at spot, Proinfa cash, resumed obligations, garantia física protection, and the value of the claims being surrendered.',
 'The product is a sign-or-do-not-sign decision and a recovery mandate. The operating company earns onboarding, success and uplift fees and never carries claim risk.',
 'A separate vehicle advances cash secured by a cessão fiduciária over the generator’s own blocked account — never by asking CCEE to redirect payment to us — against the Verified Net Cash Receivable, once a Termo is signed and the extraconcursalidade point is confirmed by counsel. Gross compensation and debt relief are never treated as purchasable face value.',
 'Mandate first. Fees first. Structure the security now — it does not depend on CCEE. Confirm the one narrow legal point. Lend against real cash once a Termo exists.'
]));

/* ─────────────────── APPENDIX ─────────────────── */
c.push(H1('Appendix — how far to trust each claim'));
c.push(table([2700,6660],[
 [cell('Claim',{head:true}),cell('Basis',{head:true})],
 [cell('Everything about what the Portaria says'),cell('VERIFIED against the primary text in the DOU of 21 July 2026, article by article, including the annexed model Termo. Article references here are exact.')],
 [cell('Curtailment volumes and eligible claim per complex'),cell('COMPUTED by us from ONS half-hourly open data. Reconciles to the operator’s own published percentages within 0.2 points. Not a company disclosure.')],
 [cell('Ownership of each complex'),cell('JOINED through ANEEL SIGA at 98.9% match. Group attribution partly inferred from naming conventions — confidence flags are in the workbook and should be respected.')],
 [cell('The R$3.3bn pool'),cell('PRESS ONLY. No primary document states any figure. MME says values are not yet defined. Estimates range R$2.7–3.5bn.')],
 [cell('The 46/41/13 split'),cell('ANEEL’s own voto, Processo 48500.000231/2026-56.')],
 [cell('Litigation census'),cell('Twelve suits per a trade-press survey of 31 Oct 2024; the appellate win was suspended by the Superior Court in January 2025. The STJ case number could not be verified in an accessible source and is deliberately not stated here.')],
 [cell('Fitch ratings and coverage ratios'),cell('Fitch release text, October 2025 to July 2026. The zero-compensation assumption is Fitch’s own stated basis.')],
 [cell('Company-level impact'),cell('Fitch via press, and company releases where they exist. Auren, CPFL and Ibitu disclose R$ figures; Engie does not.')],
 [cell('Named individuals'),cell('Published governance pages, filings and quotes ONLY. No contact database was used and no email address has been constructed or guessed.')]
]));
c.push(note('Accompanying workbook: Sutphin_Curtailment_Call_List.xlsx — ranked call list, all 267 complexes, named contacts, editable assumptions, full Portaria mechanics, call script, the Fitch cross-reference, and sources.'));

const doc=new Document({
  numbering:{config:[
    {reference:'bullets',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,
      style:{paragraph:{indent:{left:350,hanging:215}}}}]},
    {reference:'steps',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,
      style:{paragraph:{indent:{left:390,hanging:255}}}}]}]},
  sections:[{properties:{page:{margin:{top:960,bottom:960,left:1040,right:1040}}},children:c}]});

Packer.toBuffer(doc).then(b=>{
  fs.writeFileSync('Sutphin_Curtailment_Desk_FINAL.docx',b);
  console.log('wrote Sutphin_Curtailment_Desk_FINAL.docx',b.length,'bytes');
});
