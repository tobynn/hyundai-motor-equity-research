"""Analyst SOTP scenario: explicit estimated overlap and share-class assumptions."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
old=json.loads((root/'model/scenario_rebuild_20261126.json').read_text())
claim=json.loads((root/'model/common_claim_rebuild_20261127.json').read_text())
f=old['forecast']; wacc=.095; g=.02; roic=.10
def operating_ev(w,gr):
    return sum(row['fcff']/(1+w)**i for i,row in enumerate(f,1))+f[-1]['nopat']*(1+gr)*(1-gr/roic)/(w-gr)/(1+w)**len(f)
vehicle_ev=operating_ev(wacc,g)
vehicle_owners=100168.904; finance=23740.274; other=7530.495; group_owners=116222.002
# Parent segment sums contain internal interests; the difference is only an aggregate proxy.
elimination=group_owners-(vehicle_owners+finance+other)
cash=8253.939; debt=4057.933+3615.917; vehicle_nci=.005
associates_vehicle_book=35847.785;kia_book_consolidated=22045.085
kia_shares=137318251;kia_price=93700;kia_market=kia_shares*kia_price/1e9
associate_proxy=associates_vehicle_book-kia_book_consolidated+kia_market
equity=vehicle_ev+finance+other+elimination+cash-debt-vehicle_nci+associate_proxy
shares=claim['shares']['sum'];pref1=claim['shares']['preferred_1'];preferred_pv=claim['preferred']['pv_increment_per_pref1']
def common_value(e):return (e*1e9-pref1*preferred_pv)/shares
base=common_value(equity); target=round(base/1000)*1000;current=259000
change=target/current-1
sensitivity=[]
for w in [.085,.095,.105]:
 for gr in [.015,.02,.025]:
  adjusted_equity=equity+operating_ev(w,gr)-vehicle_ev
  sensitivity.append({'wacc':w,'growth':gr,'common_price':common_value(adjusted_equity)})
out={'status':'conditional analyst estimate; allocation and market data are assumptions, not verified facts','price_date':'2026-11-26','account_date':'2026-09-30','discount_anchor':'2026-12-31','horizon':'2026-12-31; approximately one month from 2026-11-26','reference_price':current,'dcf':{'wacc':wacc,'growth':g,'incremental_roic':roic,'vehicle_ev':vehicle_ev,'finance_parent_book':finance,'other_parent_book':other,'owners_elimination_proxy':elimination,'vehicle_cash':cash,'vehicle_debt':debt,'vehicle_nci':vehicle_nci,'vehicle_associates_book':associates_vehicle_book,'kia_book_proxy':kia_book_consolidated,'kia_holding':kia_shares,'kia_price':kia_price,'kia_market':kia_market,'associates_after_kia_substitution':associate_proxy,'equity':equity,'common_price':base,'sensitivity':sensitivity},'rim':{'common_price':claim['rim']['common_price']},'per':{'common_price':claim['per']['scenario_common_price'],'peer_name':'Kia','forward_per':claim['per']['kia_2027_forward_multiple']},'target_price':target,'upside_price_only':change,'rating':'BUY' if change>=.15 else 'SELL' if change<=-.15 else 'HOLD','rating_rule':'price-only upside >=15% BUY, <=-15% SELL, otherwise HOLD; horizon 2026-12-31, not 12 months','preferred_claim':claim['preferred'],'warnings':['Q3 segment book and 26 Nov prices are mixed with a year-end DCF discount anchor; Q4 equity bridge omitted.', 'Consolidated Kia carrying amount is used as a proxy for its vehicle-segment amount; unverified overlap.', 'Owners elimination proxy includes intra-group ownership and other consolidation effects; not a fair-value adjustment.', 'Vehicle EV uses pre-consolidation EBIT and externally reported vehicle sales, an approximate mixture.', 'Finance and other parent equity at 1.0x are not valuation outcomes; vehicle financial assets besides cash are omitted.', 'Forecast capex is an accounting scenario and not company investment plan; terminal value dominates.', 'Preferred allocation assumes equal residual participation, no voting premium and preferred minimums are non-binding.']}
(root/'model/final_scenario_20261127.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':out['status'],'reference_price':current,'reference_date':out['price_date'],'valuation_date':out['discount_anchor'],'horizon':out['horizon'],'DCF':{'price':round(base),'method':'SOTP with owner elimination and Kia-only substitution proxies'},'PER':{'price':round(out['per']['common_price']),'method':'single Kia forward observation; cross-check only'},'RIM':{'price':round(out['rim']['common_price']),'method':'RIM with equal participation and extra preferred dividend'},'target_price':target,'rating':out['rating'],'upside_price_only':change,'detail':'model/final_scenario_20261127.json'}
(root/'model/valuation_results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
