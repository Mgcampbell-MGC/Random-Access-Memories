# GateLedger capture — canonical layout

Capture with `bin/capture_ledger.py`. Nothing else writes to this directory.

## Frozen slugs

A source is identified by its **slug**, never by a filename. Day 0 wrote
`yti_gate_schedule.html`; day 1 wrote `yti_gate.html`. A differ keyed on filename reads that
as a deletion plus a creation — i.e. it invents a change that never happened, in a product
whose entire value is knowing exactly what changed.

| slug | source |
|---|---|
| `its_empty_receiving` | itslb.com empty-receiving updates |
| `maersk_us_empty_return_directory` | Maersk US empty-return directory (.xlsx) |
| `pnct_empty_return` | pnct.net empty return |
| `trapac_la_empty_returns` | losangeles.trapac.com empty returns |
| `yti_closed_area_matrix` | lynx.yti.com closed-area matrix |
| `yti_gate_schedule` | yti.com gate schedule |

## Root construction (v2, authoritative)

```
leaf_i = SHA256(raw bytes of source i)   ordered by SLUG ascending (ASCII)
parent = SHA256(left || right)           over 32-byte binary digests
odd node at any level is PROMOTED unchanged, never duplicated
root.txt = lowercase hex of root + "\n"  RFC 3161 tokens are taken over root.txt
```

Odd nodes are promoted rather than duplicated because duplication lets two distinct trees
produce one root (CVE-2012-2459).

**Why a Merkle root and not a digest of everything.** A customer buys *one terminal on one
day*. A Merkle root proves that one source belongs to that day's timestamped root using
`log2(n)` sibling hashes and **without disclosing the other five captures**. Each
`MANIFEST.json` carries the sibling path per source, so a proof ships with the sale.

## v1 → v2: what changed and why it was wrong

The captures of 19–21 Aug 2026 were run by hand and recorded a field named
`daily_merkle_root_sha256`. **It was not a Merkle root.** Recovered by search on 21 Aug:

```
v1 root = SHA256( maersk ‖ its ‖ pnct ‖ trapac ‖ yti_closed ‖ yti_gate )   # raw bytes, capture order
        = a0da4396fc8183bb7459337591bb8455d47d2737fbb0de2860ac884ec6c20aa6
```

A flat concatenation cannot prove one member without revealing every member, so under v1
every sale would have leaked the whole day's asset. The four RFC 3161 tokens of 19 Aug remain
valid over that value and are retained — they are simply weaker than the field name claimed.

`INDEX.json` restates all three banked days on the frozen slugs with true Merkle roots and
per-source proofs. The original tarballs are **not** rewritten; they are the evidence as banked.

## Token honesty

`INDEX_ROOTS.txt` (the three daily roots) was timestamped by freetsa.org, DigiCert and Sectigo
on **21 Aug 2026 16:15 UTC**. That proves the 19 and 20 Aug bytes existed **by the 21st** —
it does not and cannot prove they existed on their own capture dates. Only 19 Aug carries a
same-day token. Days captured from 22 Aug onward are tokenised same-day by the tool.

## Known gap

The **Maersk directory was not captured on 20 or 21 Aug** and is unrecoverable: the publisher
keeps exactly one live edition and 404s every predecessor permanently. This is the asset's own
premise demonstrated against itself. `capture_ledger.py` now discovers the live edition by
walking back up to 21 days, so the gap cannot recur silently.
