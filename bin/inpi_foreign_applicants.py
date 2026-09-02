#!/usr/bin/env python3
"""Count foreign trademark applicants and their Brazilian procuradores in INPI's weekly RPI marks XML.

Source: https://revistas.inpi.gov.br/txt/RM<edition>.zip  (one XML per weekly edition; free, no login).
Usage: python3 bin/inpi_foreign_applicants.py rm2901/RM2901.xml rm2902/2902.xml ...
Needs lxml (the gazette contains invalid character references; parse with recover=True).

What it measures, for the REPRESENTANTE candidate:
  - distinct foreign titulares per edition, and on NEW filings (IPAS009 or a <protocolo>)
  - how many procuradores serve foreign titulares, how concentrated, how many look like individuals
  - Madrid Protocol designations (<dados-de-madri>) whose holder has NO Brazilian procurador printed —
    the population that must appoint one under LPI art. 217 the moment INPI or an opponent acts.
"""
import sys, re, collections
from lxml import etree

FIRM = re.compile(r"(LTDA|ADVOG|ASSOC|S/A|S\.A|PROPRIEDADE|MARCAS|PATENT|CONSULT|AGENTE|INTELLECT|LEGAL|LAW|SOCIEDADE|EIRELI|\bME\b|EPP|\bIP\b|ESCRIT|SERVI|CONSUL|GROUP|PARTNERS|&)", re.I)

def main(files):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    country = collections.Counter(); proc_foreign = collections.Counter()
    foreign_all, foreign_new, madri_noproc_names, madri_names = set(), set(), set(), set()
    madri = madri_noproc = 0; madri_codes = collections.Counter()
    print("edition | date | processos | w/ foreign titular | new filings w/ foreign | distinct foreign titulares | distinct procuradores | Madrid w/ foreign | Madrid no procurador")
    for f in files:
        root = etree.parse(f, parser).getroot()
        n = fp = fn = m = mnp = 0; ft, pf = set(), set()
        for p in root.iter("processo"):
            n += 1
            for_t = [t for t in p.iter("titular") if (t.get("pais") or "") != "BR"]
            if not for_t:
                continue
            fp += 1
            names = [t.get("nome-razao-social") for t in for_t]
            pr = p.find("procurador"); pname = (pr.text or "").strip() if pr is not None else ""
            codes = [d.get("codigo") for d in p.iter("despacho")]
            for t in for_t: country[t.get("pais")] += 1
            ft.update(names); foreign_all.update(names)
            if pname: proc_foreign[pname] += 1; pf.add(pname)
            if p.find("protocolo") is not None or "IPAS009" in codes:
                fn += 1; foreign_new.update(names)
            if p.find("dados-de-madri") is not None:
                m += 1; madri += 1; madri_names.update(names)
                for c in codes: madri_codes[c] += 1
                if not pname: mnp += 1; madri_noproc += 1; madri_noproc_names.update(names)
        print(f"{root.get('numero')} | {root.get('data')} | {n} | {fp} | {fn} | {len(ft)} | {len(pf)} | {m} | {mnp}")
    print("\nDISTINCT foreign titulares, any event:", len(foreign_all))
    print("DISTINCT foreign titulares on NEW filings:", len(foreign_new))
    print("Madrid designations w/ foreign holder:", madri, "| no Brazilian procurador printed:", madri_noproc,
          f"({madri_noproc/max(madri,1)*100:.0f}%) | distinct holders w/o procurador:", len(madri_noproc_names))
    print("Madrid despachos:", madri_codes.most_common(5))
    print("Countries (titular rows):", country.most_common(12))
    vals = sorted(proc_foreign.values(), reverse=True); s = sum(vals)
    print(f"\nprocuradores serving foreign titulares: {len(proc_foreign)} distinct over {s} processos | top10 share {sum(vals[:10])/s*100:.1f}% | top50 {sum(vals[:50])/s*100:.1f}% | with <=3: {sum(1 for v in vals if v<=3)}")
    indiv = [(k, v) for k, v in proc_foreign.items() if not FIRM.search(k)]
    print(f"procuradores that look like individuals: {len(indiv)}, handling {sum(v for _, v in indiv)} processos")
    for k, v in proc_foreign.most_common(12): print(f"  {v:5d}  {k[:70]}")

if __name__ == "__main__":
    main(sys.argv[1:])
