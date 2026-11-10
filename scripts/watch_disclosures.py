"""Detect new Hyundai Motor earnings-related DART filings and update the repository log."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

COMPANY = "현대자동차"
STOCK_CODE = "005380"
CORP_CODE = "00164742"
KEYWORDS = ("사업보고서", "반기보고서", "분기보고서", "영업(잠정)실적")
ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "disclosure_watch.json"
LOG_PATH = ROOT / "report" / "DISCLOSURE_UPDATE_LOG.md"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def main() -> int:
    api_key = os.environ.get("DART_API_KEY")
    if not api_key:
        raise RuntimeError("GitHub Actions secret DART_API_KEY가 설정되지 않았습니다.")
    today = datetime.now(timezone.utc).date()
    params = {
        "crtfc_key": api_key,
        "corp_code": CORP_CODE,
        "bgn_de": (today - timedelta(days=21)).strftime("%Y%m%d"),
        "end_de": today.strftime("%Y%m%d"),
        "last_reprt_at": "Y",
        "page_count": "100",
        "sort": "date",
        "sort_mth": "desc",
    }
    payload = get_json("https://opendart.fss.or.kr/api/list.json?" + urllib.parse.urlencode(params))
    if payload.get("status") == "013":
        print("새 공시가 없습니다.")
        return 0
    if payload.get("status") != "000":
        raise RuntimeError(f"DART 공시 검색 실패: {payload.get('status')} {payload.get('message', '')}")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    known = {item["receipt_number"] for item in state.get("filings", [])}
    new_items = []
    for row in payload.get("list", []):
        name = row.get("report_nm", "")
        receipt = row.get("rcept_no", "")
        if receipt and any(keyword in name for keyword in KEYWORDS) and receipt not in known:
            new_items.append({
                "receipt_number": receipt,
                "receipt_date": row.get("rcept_dt", ""),
                "report_name": name,
                "filer": row.get("flr_nm", ""),
                "url": f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={receipt}",
            })
    if not new_items:
        print("새 실적 관련 공시가 없습니다.")
        return 0
    state["filings"] = sorted(new_items + state["filings"], key=lambda x: (x["receipt_date"], x["receipt_number"]), reverse=True)[:100]
    state["last_update_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# [공시 갱신 기록]", "", "대상 회사: 현대자동차 (005380)", "", "이 로그는 새 정기보고서와 영업잠정실적 공시를 기록한다. 실제치, 전망, 목표주가는 공시 원문과 IR 자료를 대조한 뒤 수정한다.", "", "| 접수일 | 공시명 | 제출인 | 원문 |", "| --- | --- | --- | --- |"]
    for item in state["filings"][:20]:
        lines.append(f"| {item['receipt_date']} | {item['report_name']} | {item['filer']} | [DART 원문]({item['url']}) |")
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"새 공시 {len(new_items)}건을 기록했습니다.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
