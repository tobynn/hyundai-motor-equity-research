"""Share-class allocation and a forward peer comparison, KRW bn and KRW/share."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'model/scenario_rebuild_20261126.json').read_text())
ordinary=202_418_958;pref1=22_839_037;pref2=34_257_047;pref3=2_321_926
shares=ordinary+pref1+pref2+pref3
ke=.11;extra=50.;extra_pv=extra/ke
rim_equity=source['rim']['equity'];rim_common=(rim_equity*1e9-pref1*extra_pv)/shares
earnings2027=source['per']['earnings_2027_assumption']
eps27=(earnings2027*1e9-pref1*extra)/shares
price_kia=93700;eps_kia=21311;peer=price_kia/eps_kia
price=eps27*peer
out={'status':'research scenario; not a final target','price_date':'2026-11-26','valuation_date':'2026-12-31 estimated','shares':{'ordinary':ordinary,'preferred_1':pref1,'preferred_2':pref2,'preferred_3':pref3,'sum':shares,'counts_as_of':'2026-09-30'},'preferred':{'pref1_extra_dividend_krw_per_year':extra,'discount_rate':ke,'pv_increment_per_pref1':extra_pv,'other_classes_extra_assumed_zero':True,'assumption':'Equal participation in residual earnings and distributions, no voting-control premium, minimum preferred thresholds non-binding; not a legal claim valuation.'},'rim':{'equity_bn':rim_equity,'common_price':rim_common,'pref1_price':rim_common+extra_pv},'per':{'earnings_2027_bn':earnings2027,'common_eps_proxy':eps27,'kia_price_20261126':price_kia,'kia_eps_2027_analyst':eps_kia,'kia_analyst_date':'2026-11-02','kia_2027_forward_multiple':peer,'scenario_common_price':price,'source':'https://imfnsec.tistory.com/229','limitation':'One related-company observation, analyst forecast date differs from valuation date; no automatic target multiple.'},'dcf':{'old_scenario_price_market_weighted':source['dcf']['common_price_using_market_weighted_claims'],'status':'unresolved segment allocation, lease/NCI and equity-method overlap; must not be used as final target'},'book_and_forecast':source['rim'],'reference':'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20261116001437'}
(root/'model/common_claim_rebuild_20261127.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':'research scenarios, not a final target','reference_price':259000,'reference_date':'2026-11-26','valuation_date':'2026-12-31 estimate','DCF':{'price':None,'method':'unresolved finance and associate overlap'},'PER':{'price':round(price),'method':'single Kia peer FY2027 analyst estimate; sensitivity only'},'RIM':{'price':round(rim_common),'method':'estimated residual income; preferred dividend allocation'},'target_price':None,'rating':'under review','detail':'model/common_claim_rebuild_20261127.json'}
(root/'model/valuation_results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
