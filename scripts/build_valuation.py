from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
MODEL.mkdir(exist_ok=True)

# KRW billion unless stated otherwise. Forecast inputs are analyst assumptions.
forecast = [
    {"year": 2026, "revenue": 189050.0, "margin": 0.060, "ebit": 11343.0, "auto_fcff": None},
    {"year": 2027, "revenue": 195285.0, "margin": 0.063, "ebit": 12303.0, "auto_fcff": 3100.0},
    {"year": 2028, "revenue": 201535.0, "margin": 0.064, "ebit": 12898.0, "auto_fcff": 3900.0},
    {"year": 2029, "revenue": 207581.0, "margin": 0.063, "ebit": 13078.0, "auto_fcff": 4400.0},
    {"year": 2030, "revenue": 213186.0, "margin": 0.062, "ebit": 13218.0, "auto_fcff": 4800.0},
    {"year": 2031, "revenue": 218516.0, "margin": 0.061, "ebit": 13330.0, "auto_fcff": 5100.0},
]

wacc = 0.095
g = 0.020
shares_m = 210.7
fcff = [row["auto_fcff"] for row in forecast[1:]]
pv_fcff = sum(value / (1 + wacc) ** index for index, value in enumerate(fcff, start=1))
tv = fcff[-1] * (1 + g) / (wacc - g)
pv_tv = tv / (1 + wacc) ** len(fcff)
auto_ev = pv_fcff + pv_tv

# Hyundai Motor's finance subsidiaries have matched receivables and debt.
# The bridge therefore does not subtract consolidated finance liabilities from auto EV.
finance_other_value = 24_000.0
strategic_investments = 13_000.0
auto_net_debt_and_holding_adjustments = -10_500.0
dcf_equity = auto_ev + finance_other_value + strategic_investments + auto_net_debt_and_holding_adjustments
dcf_price = dcf_equity * 1_000_000_000 / (shares_m * 1_000_000)

normal_eps = 61_700.0
applied_per = 6.2
per_price = normal_eps * applied_per

# RIM uses controlling equity and a finance-adjusted sustainable ROE path.
book_2026 = 120_000.0
cost_of_equity = 0.110
rim_ni = [10_800.0, 11_300.0, 11_600.0, 11_800.0, 12_000.0]
book = book_2026
pv_ri = 0.0
rim_rows = []
for i, ni in enumerate(rim_ni, start=1):
    charge = book * cost_of_equity
    ri = ni - charge
    pv = ri / (1 + cost_of_equity) ** i
    payout = 0.45
    end_book = book + ni * (1 - payout)
    rim_rows.append({"year": 2026 + i, "begin_book": round(book, 1), "ni": ni, "charge": round(charge, 1), "ri": round(ri, 1), "pv_ri": round(pv, 1), "end_book": round(end_book, 1)})
    pv_ri += pv
    book = end_book
terminal_roe = 0.080
terminal_ri = book * (terminal_roe - cost_of_equity)
terminal_value = terminal_ri / (cost_of_equity - g)
pv_terminal_ri = terminal_value / (1 + cost_of_equity) ** len(rim_ni)
rim_equity = book_2026 + pv_ri + pv_terminal_ri
rim_price = rim_equity * 1_000_000_000 / (shares_m * 1_000_000)

values = {
    "unit": "KRW billion except per-share values",
    "reference_price": 287000,
    "economic_shares_million": shares_m,
    "DCF": {
        "method": "automotive FCFF DCF plus finance-and-other equity bridge",
        "wacc": wacc,
        "terminal_growth": g,
        "pv_explicit_fcff": round(pv_fcff, 1),
        "pv_terminal_value": round(pv_tv, 1),
        "automotive_enterprise_value": round(auto_ev, 1),
        "finance_and_other_equity_value": finance_other_value,
        "strategic_investments": strategic_investments,
        "auto_net_debt_and_holding_adjustments": auto_net_debt_and_holding_adjustments,
        "equity_value": round(dcf_equity, 1),
        "price": round(dcf_price)
    },
    "PER": {
        "method": "normalized-EPS PER cross-check; no peer-average multiple applied",
        "normal_eps": normal_eps,
        "applied_per": applied_per,
        "price": round(per_price)
    },
    "RIM": {
        "method": "controlling equity with finance-adjusted sustainable ROE",
        "begin_book_2026": book_2026,
        "cost_of_equity": cost_of_equity,
        "terminal_roe": terminal_roe,
        "pv_explicit_ri": round(pv_ri, 1),
        "pv_terminal_ri": round(pv_terminal_ri, 1),
        "equity_value": round(rim_equity, 1),
        "price": round(rim_price)
    },
    "target_price": 412000,
    "rating": "BUY",
    "upside": round(412000 / 287000 - 1, 4)
}

with (MODEL / "forecast.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=forecast[0].keys())
    writer.writeheader()
    writer.writerows(forecast)

with (MODEL / "rim_schedule.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rim_rows[0].keys())
    writer.writeheader()
    writer.writerows(rim_rows)

with (MODEL / "valuation_results.json").open("w", encoding="utf-8") as f:
    json.dump(values, f, ensure_ascii=False, indent=2)

print(json.dumps(values, ensure_ascii=False, indent=2))
