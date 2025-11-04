import os
import json
from pathlib import Path
from typing import Dict, Any, List
import requests
import shutil

API_BASE = "https://fake-api-vycpfa6oca-uc.a.run.app"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")


def _headers() -> dict:
    if not AUTH_TOKEN:
        raise RuntimeError("AUTH_TOKEN env var is not set")
    return {"Authorization": AUTH_TOKEN}


def _fetch_page(report_date: str, page: int) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/sales"
    params = {"date": report_date, "page": page}

    resp = requests.get(url, headers=_headers(), params=params, timeout=20)

    if resp.status_code == 404:
        return []

    resp.raise_for_status()
    data = resp.json()
    return data if isinstance(data, list) else data.get("items", [])


def _ensure_clean_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    for child in p.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    return p


def save_sales_to_local_disk(date: str, raw_dir: str) -> dict:
    out_dir = _ensure_clean_dir(raw_dir)

    total_records = 0
    page = 1
    files = 0

    while True:
        items = _fetch_page(date, page)
        if not items:
            break

        total_records += len(items)
        files += 1

        out_file = out_dir / f"sales_{date}_{files}.json"
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        page += 1

    return {"pages": files, "records": total_records, "path": str(out_dir)}