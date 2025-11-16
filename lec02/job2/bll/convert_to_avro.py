import json
import shutil
from pathlib import Path
from typing import Dict, Any, List
from fastavro import writer, parse_schema


def _ensure_clean_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    for child in p.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    return p


def _load_json_files(raw_dir: str) -> List[Dict[str, Any]]:
    all_records = []
    for f in Path(raw_dir).glob("*.json"):
        with f.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                all_records.extend(data)
    return all_records


def save_avro_from_json(raw_dir: str, stg_dir: str) -> dict:
    out_dir = _ensure_clean_dir(stg_dir)
    records = _load_json_files(raw_dir)

    if not records:
        raise ValueError(f"No JSON files found in {raw_dir}")

    example = records[0]
    fields = [{"name": k, "type": ["null", "string", "int", "float"]} for k in example.keys()]
    schema = {
        "doc": "Sales data",
        "name": "SaleRecord",
        "namespace": "sales.avro",
        "type": "record",
        "fields": fields
    }

    parsed_schema = parse_schema(schema)
    out_file = out_dir / "sales_data.avro"

    with out_file.open("wb") as out_f:
        writer(out_f, parsed_schema, records)

    return {"records": len(records), "path": str(out_file)}