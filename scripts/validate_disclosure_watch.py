from __future__ import annotations
import json
from pathlib import Path

state = json.loads((Path(__file__).resolve().parents[1] / "data" / "disclosure_watch.json").read_text(encoding="utf-8"))
assert {"company", "stock_code", "filings"} <= state.keys()
assert isinstance(state["filings"], list)
for item in state["filings"]:
    assert {"receipt_number", "receipt_date", "report_name", "filer", "url"} <= item.keys()
    assert item["url"].startswith("https://dart.fss.or.kr/")
print("disclosure watch: PASS")
