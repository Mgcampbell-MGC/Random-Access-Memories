# -*- coding: utf-8 -*-
"""Call script content for the curtailment workbook."""

Q = '"'

SCRIPT = [
    ("THE SINGLE MOST IMPORTANT THING TO UNDERSTAND — AND ALMOST NOBODY HAS", None),
    ("", "There are TWO decisions, ten months apart, and they are constantly being confused with each other. "
         "The 10 August manifestação de interesse is NOT the waiver. ABSOLAR has said so publicly: filing the "
         "manifestation does not bind anyone to drop a lawsuit. The irrevocable renúncia happens at SIGNATURE "
         "of the Termo — and the convocação to sign cannot legally issue until ONS finishes its database around "
         "late April 2027. Signature therefore lands mid-2027, by which point CCEE has published the actual "
         "volumes. So filing by 10 August is cheap optionality and almost everyone should do it. The real "
         "decision is ten months later, with the numbers in hand. Anyone telling a generator to agonise over "
         "10 August has misread the instrument."),
    ("What this does to the engagement",
     "It is not a two-week campaign. It is a ten-month advisory position — a free and easy first call now, then "
     "the classification audit, then the ONS contestation window around March 2027, then the signature decision "
     "in mid-2027. That is a far better business than a fortnight of cold calls."),

    ("THE OPENING — 20 SECONDS", None),
    ("Say this",
     Q + "You have until 10 August to file the manifestação under Portaria 140. I am not calling to sell you "
         "anything. I am calling because most people are treating 10 August as the decision, and it is not — "
         "the waiver does not bite until you sign, and that is mid-2027. What matters between now and then is "
         "whether your cut hours are correctly classified, and almost nobody is auditing that." + Q),
    ("Why it works",
     "It is a date, it is true, and it tells them within one sentence that you have read the instrument rather "
     "than a law firm summary."),

    ("THE FOUR THINGS ACTUALLY WORTH MONEY TO THEM", None),
    ("1 — The classification is a black box, and it decides everything",
     Q + "Whether an hour is coded confiabilidade or sobreoferta decides whether you are paid for it. Volt "
         "Robotics tested MME's SOSIN formula and found it produces 143 per cent more sobreoferta than ONS's "
         "own calculation. The share coded non-compensable has gone from 27 per cent in 2023 to 65 per cent in "
         "the first half of 2026. There is a ten-day contestation window after ONS's consistency analysis, "
         "around March 2027. Every point you move from sobreoferta to confiabilidade is cash. Is anyone "
         "re-running your hours?" + Q),
    ("2 — Nobody knows which PLD applies",
     Q + "Cláusula Quinta values your uncommitted volume at PLD — but the Termo never says whether that is the "
         "PLD at the time of the cut or at the date of compensation. Lefosse have flagged it. Nordeste PLD sat "
         "at the R$58 floor for most of early 2025 and averaged R$227 across 2026. On a large book that "
         "ambiguity is worth nine figures. It should be resolved before you sign, not after." + Q),
    ("3 — Signing turns a suspended liability into an enforceable one",
     Q + "This is the one that gets missed. Cláusula Oitava: on signing you authorise CCEE to resume billing the "
         "CCEAR-D and CER ressarcimentos you owe, and you undertake not to oppose provisional orders against the "
         "União or CCEE. If a court decision is currently the only thing keeping a nine-figure CCEE liability "
         "off your books, you are converting it into an enforceable debt today, against a credit that pays in "
         "late 2027. That trade has to be modelled, not assumed." + Q),
    ("4 — But the near-term carrot is real, and it is not the credit",
     Q + "Article 6 paragraph 3: file the manifestação and CCEE's settlement of what you owe under CER and "
         "CCEAR-D stays suspended through the whole process. For anyone tight on cash that is worth more right "
         "now than the compensation itself. It is also why filing by 10 August is close to free." + Q),

    ("THE TWO STRUCTURAL POINTS TO HAVE READY", None),
    ("Most of it is not cash",
     "Cláusula Quinta treats curtailed MWh as delivered against CCEAR-D and CER first, which cancels a debt "
     "rather than paying anyone. Only uncommitted volume is paid at PLD. Sector-wide, ~R$3.3bn of credit nets "
     "against ~R$6bn owed, so generators stay net owing even after full compensation. ASK WHICH SIDE THEY ARE "
     "ON — it cannot be worked out from outside, and that is exactly why the question opens the conversation."),
    ("The veto is still alive",
     "The vetoed art. 1º-A would have compensated all externally-caused cuts except sobreoferta, retroactively. "
     "Congress pulled the override from the agenda on 18 June 2026 and has still not voted it. The Termo's "
     "waiver is bounded by event date, not by which law creates the right — so signing surrenders that option "
     "for nothing."),

    ("WHAT YOU ARE OFFERING ON CALL ONE", None),
    ("The offer",
     "Re-run their curtailment hours against ONS's own classification and tell them what share is being coded "
     "sobreoferta that should not be — plus the two-sided number: what the Portaria pays them, split cash "
     "versus debt relief, against what the waiver and the garantia física revision cost them. We have already "
     "built the eligible-volume base for all 267 complexes in the country from ONS open data, so their line "
     "already exists."),
    ("Price it or not?",
     "Free for the priority names. The analysis is what earns the right to the 2027 conversation, and that is "
     "where capital goes to work."),

    ("WHAT YOU DO NOT SAY ON CALL ONE", None),
    ("Do not",
     "Do not offer to buy the credit. There is no Termo, no quantified amount and no título executivo until "
     "mid-2027. There is literally nothing to buy yet."),
    ("Do not",
     "Do not claim the credit is assignable. The Portaria contains zero occurrences of cessão, transferência, "
     "oneração, penhor or caução. It is silent. If asked directly, say exactly that."),
    ("Do not",
     "Do not quote R$3.3bn as fact. No primary document states any pool figure, and MME says the values are "
     "not yet defined."),
    ("Do not",
     "Do not tell them whether to sign. You are quantifying both sides. For most of them the honest answer "
     "today is: file in August, audit your classification in between, decide in 2027."),

    ("WHERE THE CAPITAL ACTUALLY GOES", None),
    ("Not the holdcos",
     "Casa dos Ventos holds the largest eligible claim in the country and does not need us — it raised US$1.1bn "
     "in a US private placement in June 2026. Essentia is buying assets, not selling claims. Call them for "
     "information and relationship, not for a financing."),
    ("The project-finance SPEs — this is the population",
     "Fitch put 13 Brazilian renewable project financings on Rating Watch Negative in October 2025 explicitly "
     "on curtailment, downgraded 6 by May 2026, and left 11 on negative outlook with pressure projected to "
     "persist to 2030. Tupi (BRL 820m, sponsor Ibitu, PPAs with Cemig GT) runs a minimum DSCR of 1.03x and "
     "cannot distribute below 1.25x. ENGIE's São Pedro IV averages 0.75x. These vehicles cannot wait until "
     "2028 and cannot pay a dividend in the meantime. That is where a bridge is worth something."),
    ("The one acute name",
     "Rio Alto: extrajudicial recovery extinguished without resolution in June 2026, BTG enforcing Santa Luzia "
     "5, 7 and 9, a sale mandated to close by end-2026 with no buyer, Coremas averaging 52 per cent restricted "
     "and Santa Luzia 35.8 per cent. It cannot survive to late 2027 on this credit. Whatever the right answer "
     "is there, it is not a bridge loan."),
    ("Also worth knowing",
     "BNDES opened case-by-case debt standstills for curtailment-hit projects in October 2025, with parallel "
     "talks at BNB and Banco do Brasil. Atlas Renewable Energy suspended roughly 1.5 GW and US$1bn of Brazilian "
     "projects in June 2026 explicitly over curtailment. The distress is real and it is being managed quietly."),

    ("HANDLING THE OBVIOUS PUSHBACKS", None),
    (Q + "Our lawyers are on it" + Q,
     Q + "Only Lefosse and Mattos Filho have published anything on this, and nobody has filed a request for "
         "clarification in the days since publication. Ask your lawyers one question: which PLD applies to our "
         "uncommitted volume — the date of the cut, or the date of payment? If they have an answer, you do not "
         "need me." + Q),
    (Q + "ABEEólica is handling it" + Q,
     Q + "Elbia Gannoum has said publicly she cannot guarantee adhesion of 100 per cent or of 50 per cent. And "
         "the Termo excludes you from the collective action individually, by name. Whether that trade works for "
         "you depends on your contract mix and your classification split, and no association can answer that "
         "member by member." + Q),
    (Q + "Why do you care?" + Q,
     Q + "We finance receivables against solvent obligors in Brazil. This creates a large one with a two-year "
         "wait attached. The fastest way to understand it properly is to work through real books with people "
         "who own the assets. If something commercial follows later, it follows later." + Q),
    (Q + "Send me a deck" + Q,
     Q + "I would rather send you your own numbers. We have already built the eligible-volume base for every "
         "complex in the country from ONS data. Tell me which complexes are yours and you will have your own "
         "line by the end of the week." + Q),
]
