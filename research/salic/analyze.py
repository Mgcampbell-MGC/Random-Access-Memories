#!/usr/bin/env python3
"""Census of Lei Rouanet proponentes: how many hold enough concurrent
active projects to clear the ARPU floor?"""
import json
from collections import Counter, defaultdict

rows = json.load(open("projetos.json", encoding="utf-8"))
print(f"rows loaded: {len(rows)}\n")


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0


print("=" * 78)
print("SITUACAO DISTRIBUTION (all rows)")
print("=" * 78)
for s, c in Counter(r.get("situacao") or "(vazio)" for r in rows).most_common(40):
    print(f"{c:7d}  {s}")

# --- classify ------------------------------------------------------------
# "Active" = still occupying a carteira slot: authorised to raise, raising,
# or in execution. Excludes archived / rejected / finished / accounts-done.
DEAD_KEYS = ["arquiv", "indeferi", "inabilit", "cancel", "extint",
             "encerrad", "conclu", "prestação de contas aprovada",
             "prest. contas aprovada", "não aprovado", "nao aprovado",
             "rejeit", "devolvid"]
LIVE_KEYS = ["autorizada a captação", "captação", "execução", "em execucao",
             "aguardando", "avaliação", "análise", "readequa", "assinatura",
             "homologa", "enquadrad", "admissib"]


def state(sit):
    s = (sit or "").lower()
    if any(k in s for k in DEAD_KEYS):
        return "dead"
    if any(k in s for k in LIVE_KEYS):
        return "live"
    return "other"


buckets = Counter(state(r.get("situacao")) for r in rows)
print(f"\nclassified -> {dict(buckets)}")
print("\n'other' situacoes (unclassified):")
for s, c in Counter(r.get("situacao") or "(vazio)" for r in rows
                    if state(r.get("situacao")) == "other").most_common(15):
    print(f"  {c:6d}  {s}")

# --- per-proponente ------------------------------------------------------
live = [r for r in rows if state(r.get("situacao")) == "live"]
by_prop = defaultdict(list)
for r in live:
    doc = (r.get("cgccpf") or "").strip()
    if doc:
        by_prop[doc].append(r)

pj = {d: v for d, v in by_prop.items() if len(d) > 11}
pf = {d: v for d, v in by_prop.items() if len(d) <= 11}

print("\n" + "=" * 78)
print("PROPONENTES WITH LIVE (SLOT-OCCUPYING) PROJECTS")
print("=" * 78)
print(f"live projects        : {len(live)}")
print(f"distinct proponentes : {len(by_prop)}   (PJ {len(pj)} / PF {len(pf)})")

print("\nPJ proponentes by number of concurrent live projects:")
dist = Counter(len(v) for v in pj.values())
cum = 0
for n in sorted(dist, reverse=True):
    cum += dist[n]
    print(f"  exactly {n:3d} projects: {dist[n]:5d}   (>= {n}: {cum})")

print("\n--- ADDRESSABLE BUYER COUNTS (PJ only) ---")
for threshold in (3, 4, 5, 6, 7, 8, 10):
    n = sum(1 for v in pj.values() if len(v) >= threshold)
    print(f"  PJ with >= {threshold:2d} concurrent live projects : {n}")

# --- money ---------------------------------------------------------------
print("\n--- CAPTACAO among multi-project PJ (>=4 live) ---")
big = {d: v for d, v in pj.items() if len(v) >= 4}
tot = sum(num(r.get("valor_captado")) for v in big.values() for r in v)
apr = sum(num(r.get("valor_aprovado")) for v in big.values() for r in v)
print(f"  proponentes: {len(big)}")
print(f"  soma valor_captado  : R$ {tot:,.0f}")
print(f"  soma valor_aprovado : R$ {apr:,.0f}")

print("\n--- UF of multi-project PJ (>=4 live) ---")
ufc = Counter(v[0].get("UF") for v in big.values())
for u, c in ufc.most_common(12):
    print(f"  {u}: {c}")

print("\n--- TOP 25 PJ BY LIVE PROJECT COUNT ---")
top = sorted(pj.items(), key=lambda kv: -len(kv[1]))[:25]
for doc, v in top:
    cap = sum(num(r.get("valor_captado")) for r in v)
    apv = sum(num(r.get("valor_aprovado")) for r in v)
    nm = (v[0].get("proponente") or "")[:44]
    print(f"  {len(v):3d} proj | captado R$ {cap:14,.0f} | aprovado R$ {apv:14,.0f} | "
          f"{v[0].get('UF')} | {nm}")

# --- segment mix ---------------------------------------------------------
print("\n--- SEGMENTS among multi-project PJ (>=4 live) ---")
seg = Counter(r.get("segmento") for v in big.values() for r in v)
for s, c in seg.most_common(12):
    print(f"  {c:5d}  {s}")
