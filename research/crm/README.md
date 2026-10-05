# The O LANÇAMENTO customer list: how it is built

The list is every Brazilian beauty brand that notified at least one genuinely new product with ANVISA in the
last 90 days. It covers hair, face, body, soap, deodorant, makeup and fragrance. Each brand gets its owner,
website and published contacts, and a grade.

**The spreadsheet itself is NOT in git.** It holds names, phone numbers and e-mails. Only the scripts and this
note are committed. Rebuild the sheet from the scripts.

## Run order

All scripts run from one working folder. `pipe3.py` and `assemble.py` import `excl.py` from
`../hunt6/work/ol6/`; it is committed here too, so point `sys.path` at this folder.

| Step | Script | What it does |
|---|---|---|
| 1 | download | `https://dados.anvisa.gov.br/dados/CONSULTAS/PRODUTOS/TA_CONSULTA_COSMETICOS.CSV` (latin-1, `;`, ~230 MB) |
| 2 | `load.py` | Notification date = `DT_VENCIMENTO` − 10 years. Electronic notifications are the `Notificado` rows whose expiry time is **not** midnight. Keeps the last 90 days. |
| 3 | `cats.py`, `pipe1.py`, `pipe2.py` | Category per product. Brand per holder, by voting on n-grams. Re-filings of old products removed (exact or Jaccard ≥ 0,75 inside the brand). |
| 4 | `pipe3.py` | Removes multinationals, large groups and a manual exclusion list. Flags importers, essential-oil suppliers, professional lines and untested pack shapes. |
| 5 | `disc*.py` | Guesses each brand's website and validates it. `disc2.py` is a second round of name variants for brands with no site. |
| 6 | `reval_all.py` | Re-fetches every found site and keeps it only if the holder CNPJ or ≥ 2 product names appear on the page. |
| 7 | `requeue.py` → `open_fetch.py` | Company registry for every candidate owner CNPJ (`worker.py cnpja` is optional; see below). |
| 8 | `disc_email.py` → `brandcheck.py` | The site at the registry e-mail's domain; owner kept only if the brand appears on it. |
| 9 | `assemble.py` → `make_meta.py` → `build_xlsx.py <out.xlsx>` | Owner rules, contact cleaning, grades, then the two-tab workbook (Painel + Lista). |

## Rules worth keeping

- **OpenCNPJ (`api.opencnpj.org/{cnpj}`) returns the registry e-mail with no quota.** BrasilAPI and
  minhareceita silently drop the e-mail field (CLAUDE.md, `THE POSTAL LIST LAW`). CNPJá (`open.cnpja.com`,
  ~5/min) marks an e-mail as the accountant's (`ownership: ACCOUNTING`). **Measured 5 Oct 2026: on 712
  companies it flagged 49 e-mails, and the address regex below had already caught all 49.** It adds nothing,
  so skip it.
- **Registry contacts are often the accountant's or the lawyer's.** Four signals: CNPJá's ACCOUNTING flag;
  the address itself (`contab`, `.cnt.br`, `.adv.br`, `jurídico`, `societário`, `admempresas`, `auditoria`…);
  the same e-mail or phone on ≥ 3 companies; a phone area code outside the company's state. A flagged contact
  is never the main contact.
- **The ANVISA holder is often a contract factory, not the brand owner.** The owner is taken, in order, from
  the CNPJ in the brand site's footer, a holder whose name contains the brand, a holder that files ≤ 2 brands,
  or a commerce company with few brands. A holder named for contract manufacturing, nationalisation,
  regulatory affairs, sales representation or "soluções integradas" is treated as a service provider: owner
  unknown, grade C.
- **Validation traps:** `body` matches every page's `<body>` tag; lookalike domains (bunny.com, adel.com.br)
  pass a name check, so require the CNPJ or product names on the page; a nonexistent `.com` takes ~10 s to fail
  while `.com.br` fails at once, so a long run stalls on a few brands — cap each shard's wall time.
- **Phones:** a mobile is 9 digits starting with 9; old 8-digit mobiles get the 9 added; placeholders
  (`0000`, `1234`…) and 0800 numbers never go into the WhatsApp column.

## The run of 5 Oct 2026

3.089 brands: **A 289 · B 849 · C 1.951.** Owner identified for 1.360, website for 817, WhatsApp for 834,
phone for 1.330 and e-mail for 1.179. Every brand was searched. The second round of name variants found 20
sites in 1.052 tries (2%) and was stopped there.

## Grades

- **A:** owner known, not an importer, oils or foreign brand, ≥ 3 new products, a contact, not large
  (`DEMAIS`), owner not inferred weakly.
- **B:** owner known and a contact.
- **C:** everything else. These rows carry Google and Instagram search links.

## LGPD

Lei 13.709/2018 art. 7º IX, §3º, §4º and art. 10, checked verbatim at planalto.gov.br. The legal basis is legitimate
interest for business-to-business prospecting, using public data and data the companies publish themselves.
The first message says where the contact came from and offers a way out. A row marked "Não contatar" is never
contacted again.

## The INPI feed (added 5 Oct 2026): new brands before they launch

INPI's trademark gazette (Revista da Propriedade Industrial, Marcas) is free, weekly and covers every product
category: `https://revistas.inpi.gov.br/txt/RM<number>.zip`, one XML of ~60 MB, published on Tuesdays.
New applications are the `processo` elements with despacho `IPAS009`.

| Step | Script | What it does |
|---|---|---|
| 1 | `inpi.py <xml> <rpi>` | Keeps Brazilian applicants in class 03 (cosmetics), class 05 with "suplement" in the specification, and class 04 with candles or diffusers |
| 2 | `match.py <rpi>` | Finds the CNPJ: a sole trader's (MEI) registered name starts with the CNPJ's first 8 digits, so the full number is root + `0001` + check digits; other applicants are matched by name against the ANVISA cosmetics, food and cleaning-product lists |
| 3 | `disc_inpi.py <rpi>` | Guesses the brand's website; a footer CNPJ counts only if its registered name shares a word with the trademark applicant |
| 4 | `inpi_rows.py <rpi> <date>` → `merge_all.py` | Builds list rows with the same contact rules, merges them with the ANVISA list (`final_all.pkl`), and flags ANVISA brands whose owner just filed a new mark |

**One week (RPI 2908, 29 Sep 2026):** 11.894 new applications. Brazilian applicants: cosmetics 415,
supplements and pharma 270, coffee/chocolate/sweets 367, beer and juices 82, wine and spirits 55, pet food
83, candles 49. After filtering: 602 filings, 547 rows, 7 already on the list. The rest had a CNPJ for 90
(31 of them sole traders, all 31 found in the registry) and a contact for 87.

**What doesn't work:** the gazette has no CNPJ, phone or e-mail. No free name-to-CNPJ search works:
Casa dos Dados returns a bot challenge, and OpenCNPJ and CNPJá look up by number only. So most new
brands get search links, not contacts.

**Other lists checked the same day:**
- **ANVISA food list** (`TA_CONSULTA_ALIMENTOS.CSV`): a real date, a brand field and the approved health
  claim on every row. 5.593 supplement filings in 90 days, from 380 companies; 181 of those companies
  file 6 or more brands (contract factories).
- **ANVISA cleaning products** (`TA_CONSULTA_SANEANTES.CSV`): no date or category columns; the year comes
  from the process number. Home fragrance is about 290–410 products a year.
- **Agriculture ministry SIPEAGRO files** (drinks, veterinary): lists of establishments, not product
  launches. The drinks file masks the CNPJ.

**Bug fixed:** `build_xlsx.py` loaded the Painel notes only when no output name was given. The first
workbook sent on 5 Oct had no subtitle and no notes.

## Monthly run (set up 5 Oct 2026)

`monthly_inpi.py` does the whole INPI job from an empty folder, so it doesn't need anything from a previous
session:

```
cd research/crm && python3 monthly_inpi.py --work /tmp/inpi_work
```

- **Gazettes:** it processes every gazette after the one recorded in `inpi_state.json`, up to the latest
  published one.
- **Lookups:** it downloads the three ANVISA lists for name matching, applies the same contact rules, and
  drops brands already on the CRM.
- **Output:** one tab, "Novas marcas YYYY-MM", with the Lista's 46 columns, to add to the sheet with
  File → Import → "Insert new sheet(s)". It never replaces the CRM, because Sol's notes live there.
- **Already on the CRM:** `seen_brand_keys.txt` holds SHA-1 fingerprints of every brand key and owner CNPJ
  already on the CRM. No names or contacts go into git. The run adds its new brands to it and updates
  `inpi_state.json`; `--dry-run` changes neither.
- **Tested 5 Oct 2026:** RPI 2908 gave 0 new brands, as expected (all already on the CRM). RPI 2907 gave
  365 new brands, 47 with a contact.

## Filter bug fixed 5 Oct 2026: match company names whole, never as fragments

The big-company filters matched fragments of names.
- **"NATURA"** (for Natura) removed every company with "Natural…" or "Naturais…" in its name: about 125
  small beauty brands, including Astera (17 new products) and Yasmin Sense (12).
- **"ARDEN"** (Elizabeth Arden) removed Garden Indústria de Cosméticos.
- **"COSMED"** removed K-Cosmedic.
- **"ARAUJO"** (Drogaria Araujo) removed two sole traders with that surname.

Every token is now a whole company name or bounded by `\b`. v3 of the CRM restores these brands: 3.759 in
all, A 293.
