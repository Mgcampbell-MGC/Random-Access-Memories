#!/usr/bin/env python3
"""Honest buyer census: proponentes with MULTIPLE projects that actually
raised money. Authorised-to-raise is not a buyer; captado > 0 is."""
import json
from collections import Counter, defaultdict

rows = json.load(open("projetos.json", encoding="utf-8"))


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0


DEAD = ["arquiv", "indeferi", "inabilit", "cancel", "extint",
        "encerrado por excesso de prazo sem captação",
        "não executado por insuficiência", "expirado o prazo",
        "duplicidade", "desist"]


def is_dead(s):
    s = (s or "").lower()
    return any(k in s for k in DEAD)


funded = [r for r in rows if num(r.get("valor_captado")) > 0]
print(f"total projects 2023-26      : {len(rows)}")
print(f"projects with captado > 0   : {len(funded)}  "
      f"({100*len(funded)/len(rows):.1f}%)")
print(f"total captado               : R$ {sum(num(r.get('valor_captado')) for r in funded):,.0f}")

# live & funded = the real work-in-flight population
live_funded = [r for r in funded if not is_dead(r.get("situacao"))]
print(f"funded AND not dead/archived: {len(live_funded)}")

by = defaultdict(list)
for r in live_funded:
    d = (r.get("cgccpf") or "").strip()
    if d:
        by[d].append(r)
pj = {d: v for d, v in by.items() if len(d) > 11}
pf = {d: v for d, v in by.items() if len(d) <= 11}

print(f"\ndistinct proponentes w/ funded live projects: {len(by)} "
      f"(PJ {len(pj)} / PF {len(pf)})")

print("\n=== PJ BUYER COUNTS by concurrent FUNDED live projects ===")
for t in (2, 3, 4, 5, 6, 8, 10):
    sel = {d: v for d, v in pj.items() if len(v) >= t}
    cap = sum(num(r.get("valor_captado")) for v in sel.values() for r in v)
    print(f"  >= {t:2d} funded projects : {len(sel):5d} proponentes | "
          f"captado R$ {cap:,.0f}")

print("\n=== SIZE OF THE PRIZE: PJ with >=3 funded live projects ===")
big = {d: v for d, v in pj.items() if len(v) >= 3}
print(f"  proponentes: {len(big)}")
caps = sorted((sum(num(r.get("valor_captado")) for r in v)
               for v in big.values()), reverse=True)
if caps:
    import statistics
    print(f"  median captado/proponente : R$ {statistics.median(caps):,.0f}")
    print(f"  mean   captado/proponente : R$ {statistics.mean(caps):,.0f}")
    for q, lbl in ((0, "max"), (len(caps)//10, "p90"), (len(caps)//4, "p75"),
                   (len(caps)//2, "p50")):
        print(f"  {lbl}: R$ {caps[min(q, len(caps)-1)]:,.0f}")

print("\n=== UF (PJ >=3 funded live) ===")
for u, c in Counter(v[0].get("UF") for v in big.values()).most_common(10):
    print(f"  {u}: {c}")

print("\n=== TOP 30 PJ BY FUNDED LIVE PROJECT COUNT ===")
for d, v in sorted(pj.items(), key=lambda kv: -len(kv[1]))[:30]:
    cap = sum(num(r.get("valor_captado")) for r in v)
    print(f"  {len(v):3d} proj | R$ {cap:13,.0f} | {v[0].get('UF')} | "
          f"{(v[0].get('proponente') or '')[:46]}")

print("\n=== PAIN SIGNALS (all 45.863 rows) ===")
pat = {
    "submitted, awaiting analysis": "apresentou prestação de contas",
    "prazo started to submit": "iniciado prazo para apresentar",
    "INADIMPLENTE": "inadimplente",
    "contas DESAPROVADA": "desaprovada",
    "archived: no answer to diligencia": "não atendimento à diligência",
    "under diligencia now": "diligenciado",
    "suspenso": "suspenso",
}
for lbl, k in pat.items():
    n = sum(1 for r in rows if k in (r.get("situacao") or "").lower())
    print(f"  {n:6d}  {lbl}")
