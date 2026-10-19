#!/usr/bin/env python3
"""Atualiza 12 meses completos com séries oficiais SGS 4391 (CDI) e 433 (IPCA)."""
import datetime as dt
import json
import pathlib
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "indices.json"
TODAY = dt.date.today()
START = TODAY.replace(day=1) - dt.timedelta(days=480)

def read_series(code):
    base = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    query = urllib.parse.urlencode({
        "formato": "json",
        "dataInicial": START.strftime("%d/%m/%Y"),
        "dataFinal": TODAY.strftime("%d/%m/%Y"),
    })
    request = urllib.request.Request(base + "?" + query, headers={"User-Agent": "simulador-lucros-reais/1.0", "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                items = json.load(response)
            result = {}
            for item in items:
                day = dt.datetime.strptime(item["data"], "%d/%m/%Y").date()
                value = float(item["valor"].replace(",", "."))
                result[day.strftime("%Y-%m")] = value
            return result
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

def main():
    cdi, ipca = read_series(4391), read_series(433)
    # Somente meses encerrados; não incluir mês atual ainda incompleto.
    previous = TODAY.replace(day=1) - dt.timedelta(days=1)
    keys = []
    for i in range(11, -1, -1):
        year = previous.year
        month = previous.month - i
        while month <= 0:
            month += 12
            year -= 1
        keys.append(f"{year:04d}-{month:02d}")
    # CDI e IPCA devem existir para cada mês, inclusive o mais recente.
    # Se o IPCA ainda não tiver sido publicado, recuar o período.
    common = sorted(k for k in set(cdi) & set(ipca) if k < TODAY.strftime("%Y-%m"))
    if len(common) < 12:
        raise RuntimeError("Menos de 12 meses completos de CDI e IPCA; manter dados anteriores.")
    keys = common[-12:]
    # Verifica continuidade para evitar lacunas silenciosas.
    for a, b in zip(keys, keys[1:]):
        y, m = map(int, a.split("-"))
        expected = f"{y+1:04d}-01" if m == 12 else f"{y:04d}-{m+1:02d}"
        if b != expected:
            raise RuntimeError("Lacuna nos índices mensais oficiais.")
    data = {
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": {"cdi": "BCB SGS 4391", "ipca": "BCB SGS 433"},
        "months": [{"month": k, "cdi": cdi[k], "ipca": ipca[k]} for k in keys]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Dados oficiais: {keys[0]} a {keys[-1]}")

if __name__ == "__main__":
    main()
