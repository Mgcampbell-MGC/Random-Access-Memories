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
