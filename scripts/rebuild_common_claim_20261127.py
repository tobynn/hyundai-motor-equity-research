"""Share-class allocation and a forward peer comparison, KRW bn and KRW/share."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'model/scenario_rebuild_20261126.json').read_text())
ordinary_q3=202_418_958;treasury_disposal=915_660
ordinary=ordinary_q3+treasury_disposal;pref1=22_839_037;pref2=34_257_047;pref3=2_321_926
shares=ordinary+pref1+pref2+pref3
ke=.11;extra=50.;extra_pv=extra/ke
opening_book=116222.002+2000-shares*2500/1e9
book=opening_book;pvri=0.
for i,ni in enumerate([7600.,8200.,8800.,9300.,9700.],1):
    pvri+=(ni-ke*book)/(1+ke)**i
    book+=ni*(1-.45)
terminal=book*(.08-ke)/(ke-.02)/(1+ke)**5
rim_equity=opening_book+pvri+terminal
rim_common=(rim_equity*1e9-pref1*extra_pv)/shares
earnings2027=source['per']['earnings_2027_assumption']
eps27=(earnings2027*1e9-pref1*extra)/shares
price_kia=93700;eps_kia=21311;peer=price_kia/eps_kia
price=eps27*peer
out={'status':'research scenario with explicit assumptions','price_date':'2026-11-26','valuation_date':'2026-12-31 estimated','shares':{'ordinary_q3':ordinary_q3,'treasury_disposal':treasury_disposal,'ordinary':ordinary,'preferred_1':pref1,'preferred_2':pref2,'preferred_3':pref3,'sum':shares,'counts_as_of':'2026-11-20 subject to later changes','disposal_source':'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20261124000343'},'preferred':{'pref1_extra_dividend_krw_per_year':extra,'discount_rate':ke,'pv_increment_per_pref1':extra_pv,'other_classes_extra_assumed_zero':True,'assumption':'Equal participation in residual earnings and distributions, no voting-control premium, minimum preferred thresholds non-binding; not a legal claim valuation.'},'rim':{'opening_book_bn':opening_book,'equity_bn':rim_equity,'common_price':rim_common,'pref1_price':rim_common+extra_pv},'per':{'earnings_2027_bn':earnings2027,'common_eps_proxy':eps27,'kia_price_20261126':price_kia,'kia_eps_2027_analyst':eps_kia,'kia_analyst_date':'2026-11-02','kia_2027_forward_multiple':peer,'scenario_common_price':price,'source':'https://imfnsec.tistory.com/229','limitation':'One related-company observation, analyst forecast date differs from valuation date; no automatic target multiple.'},'dcf':{'old_scenario_price_market_weighted':source['dcf']['common_price_using_market_weighted_claims'],'status':'earlier proxy superseded by final_scenario_20261127.py'},'forecast_inputs':{'opening_book_bn':opening_book,'annual_net_income_bn':[7600,8200,8800,9300,9700],'payout':.45,'cost_of_equity':ke,'terminal_roe':.08,'growth':.02},'reference':'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20261116001437'}
(root/'model/common_claim_rebuild_20261127.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':'research scenarios, not a final target','reference_price':259000,'reference_date':'2026-11-26','valuation_date':'2026-12-31 estimate','DCF':{'price':None,'method':'unresolved finance and associate overlap'},'PER':{'price':round(price),'method':'single Kia peer FY2027 analyst estimate; sensitivity only'},'RIM':{'price':round(rim_common),'method':'estimated residual income; preferred dividend allocation'},'target_price':None,'rating':'under review','detail':'model/common_claim_rebuild_20261127.json'}
(root/'model/valuation_results_interim_20261127.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
