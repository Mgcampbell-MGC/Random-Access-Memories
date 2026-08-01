#!/usr/bin/env python3
"""Pull SALIC (Lei Rouanet) projects for recent years, keeping only fields
needed to count active projects per proponente. Resumable: writes one shard
per (year, offset-block) so a restart re-fetches only what is missing."""
import json, os, sys, time, subprocess, glob
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://api.salic.cultura.gov.br/api/v1/projetos"
YEARS = ["23", "24", "25", "26"]
LIMIT = 100
SHARD = "shards"
KEEP = ["PRONAC", "cgccpf", "proponente", "situacao", "UF", "municipio",
        "segmento", "ano_projeto", "data_inicio", "data_termino",
        "valor_solicitado", "valor_aprovado", "valor_projeto",
        "valor_captado", "mecanisnmo", "enquadradmento", "tipologia"]


def get_json(url, timeout=120):
    out = subprocess.run(
        ["curl", "-sSL", "--max-time", str(timeout),
         "-H", "Accept: application/json", url],
        capture_output=True, text=True, timeout=timeout + 30)
    if out.returncode != 0:
        raise RuntimeError(f"curl rc={out.returncode}: {out.stderr[:200]}")
    return json.loads(out.stdout)


def fetch(year, offset, tries=4):
    path = os.path.join(SHARD, f"{year}_{offset:06d}.json")
    if os.path.exists(path):
        return 0  # already have it
    url = f"{BASE}?limit={LIMIT}&offset={offset}&ano_projeto={year}"
    for a in range(tries):
        try:
            d = get_json(url)
            rows = [{k: p.get(k) for k in KEEP}
                    for p in d.get("_embedded", {}).get("projetos", [])]
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(rows, fh, ensure_ascii=False)
            os.replace(tmp, path)
            return len(rows)
        except Exception as e:
            if a == tries - 1:
                print(f"FAIL y={year} off={offset}: {e}", file=sys.stderr, flush=True)
                return 0
            time.sleep(2 * (a + 1))
    return 0


def main():
    os.makedirs(SHARD, exist_ok=True)
    jobs = []
    for y in YEARS:
        t = get_json(f"{BASE}?limit=1&ano_projeto={y}").get("total", 0)
        print(f"ano {y}: {t} projetos", flush=True)
        jobs += [(y, off) for off in range(0, t, LIMIT)]

    todo = [(y, o) for y, o in jobs
            if not os.path.exists(os.path.join(SHARD, f"{y}_{o:06d}.json"))]
    print(f"total pages {len(jobs)}, already have {len(jobs)-len(todo)}, "
          f"fetching {len(todo)}", flush=True)

    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch, y, o): (y, o) for y, o in todo}
        for f in as_completed(futs):
            f.result()
            done += 1
            if done % 40 == 0:
                print(f"  {done}/{len(todo)} pages fetched", flush=True)

    rows = []
    for p in sorted(glob.glob(os.path.join(SHARD, "*.json"))):
        with open(p, encoding="utf-8") as fh:
            rows.extend(json.load(fh))
    with open("projetos.json", "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False)
    print(f"DONE: {len(rows)} rows -> projetos.json", flush=True)


if __name__ == "__main__":
    main()
