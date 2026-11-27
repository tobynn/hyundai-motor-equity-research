from pathlib import Path
import csv,json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"data/peer_inputs_20261126.json").read_text())
rows=data["rows"]
for row in rows:
    eps=row["fy2025_eps"]/row["split_factor"]+row["nine_m_2026_eps"]-row["nine_m_2025_eps"]
    assert abs(eps-row["ttm_eps_approx"])<0.011
    assert eps>0 and abs(row["close"]/eps-row["ttm_per_approx"])<0.011
output=root/"model/peer_comparison_20261126.csv"
with output.open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(output)
