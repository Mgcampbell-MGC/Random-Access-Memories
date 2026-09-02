#!/usr/bin/env python3
"""Enumerate dental establishments for one municipality from the Ministry of Health CNES open-data API,
with the email and phone each establishment registered, and print the fill rates.

Why CNES and not the Receita CNAE file: RDC 1.002/2025 applies to every service that provides dental
assistance, PF consultórios included, and CNES is the register the vigilância sanitária licenses against.
It carries `endereco_email_estabelecimento` and `numero_telefone_estabelecimento` directly, with no CNPJ join.
The Receita bulk host (arquivos.receitafederal.gov.br/dados/cnpj/...) returned 404 on 2 Sep 2026.

Usage: python3 bin/cnes_dental_list.py 355030 out.csv [max_pages]
  355030 = São Paulo capital (IBGE 7-digit code without the check digit). The API pages 20 rows at a time.
Output is personal data from a public register — keep it out of git, use it only for the probe.
"""
import json, urllib.request, time, re, csv, sys, collections
BASE = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos"
DENTAL = re.compile(r"ODONT|DENT|BUCAL|ORTODON|IMPLANT|SORRI|ENDODON|PERIODON|PROTES", re.I)
TIPOS = (22, 36)   # 22 = consultório isolado · 36 = clínica/centro de especialidade

def get(params, tries=4):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(f"{BASE}?{q}", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as ex:
            time.sleep(2 * (i + 1))
    return {"estabelecimentos": []}

def main(mun, out, max_pages=600):
    rows, seen = [], set()
    tipo_seen = collections.Counter()
    for tipo in TIPOS:
        off, pages = 0, 0
        while pages < max_pages:
            d = get(dict(codigo_municipio=mun, codigo_tipo_unidade=tipo, limit=20, offset=off))
            e = d.get("estabelecimentos", [])
            if not e:
                break
            for x in e:
                tipo_seen[x.get("codigo_tipo_unidade")] += 1
                nm = f"{x.get('nome_fantasia') or ''} {x.get('nome_razao_social') or ''}"
                if DENTAL.search(nm) and x["codigo_cnes"] not in seen:
                    seen.add(x["codigo_cnes"])
                    rows.append(dict(
                        cnes=x["codigo_cnes"], tipo=x.get("codigo_tipo_unidade"),
                        nome=(x.get("nome_fantasia") or x.get("nome_razao_social") or "")[:80],
                        razao=(x.get("nome_razao_social") or "")[:80],
                        cnpj=x.get("numero_cnpj") or x.get("numero_cnpj_entidade") or "",
                        natjur=x.get("descricao_natureza_juridica_estabelecimento") or "",
                        email=(x.get("endereco_email_estabelecimento") or "").strip(),
                        tel=(x.get("numero_telefone_estabelecimento") or "").strip(),
                        bairro=x.get("bairro_estabelecimento") or "", cep=x.get("codigo_cep_estabelecimento") or "",
                        atualizacao=x.get("data_atualizacao") or "",
                        sus=x.get("estabelecimento_faz_atendimento_ambulatorial_sus") or ""))
            off += 20; pages += 1
            time.sleep(0.15)
        print(f"tipo {tipo}: {pages} pages scanned, dental rows so far {len(rows)}", file=sys.stderr)
    n = len(rows)
    if not n:
        print("no rows"); return
    em = sum(1 for r in rows if "@" in r["email"]); tel = sum(1 for r in rows if r["tel"]); pj = sum(1 for r in rows if r["cnpj"])
    print(f"municipio {mun}: dental establishments (tipo 22+36, name-matched) = {n}")
    print(f"  email fill {em}/{n} = {em/n*100:.1f}%   phone fill {tel}/{n} = {tel/n*100:.1f}%   PJ (has CNPJ) {pj}/{n} = {pj/n*100:.1f}%")
    print("  tipo codes actually returned by the filter:", dict(tipo_seen))
    print("  natureza jurídica:", collections.Counter(r['natjur'] for r in rows).most_common(6))
    print("  record updated 2025–26:", sum(1 for r in rows if r['atualizacao'][:4] in ('2025', '2026')))
    dom = collections.Counter((r["email"].split("@")[-1].lower() if "@" in r["email"] else "-") for r in rows)
    print("  email domains:", dom.most_common(6))
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("  saved", out)

if __name__ == "__main__":
    mun = sys.argv[1] if len(sys.argv) > 1 else "355030"
    out = sys.argv[2] if len(sys.argv) > 2 else "cnes_dental.csv"
    mp = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    main(mun, out, mp)
