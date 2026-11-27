"""Reproducible research scenario. KRW bn except shares and KRW/share.

Not a target price: vehicle allocation, NCI and preferred allocation need review.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
forecast = [
    # revenue, EBIT margin, tax, depreciation/amortisation, capex, working-capital increase
    (2027, 145500., .055, .24, 4000., 8500., 500.),
    (2028, 151500., .060, .24, 4200., 8500., 450.),
    (2029, 157000., .062, .24, 4400., 8000., 450.),
    (2030, 162000., .061, .24, 4600., 7800., 400.),
    (2031, 167000., .060, .24, 4800., 7800., 400.),
]
wacc, growth, roic = .095, .02, .10
rows=[]
for i,(year,revenue,margin,tax,da,capex,delta_wc) in enumerate(forecast,1):
    ebit=revenue*margin
    nopat=ebit*(1-tax)
    fcff=nopat+da-capex-delta_wc
    rows.append(dict(year=year,revenue=revenue,ebit_margin=margin,ebit=ebit,tax=tax,nopat=nopat,da=da,capex=capex,delta_wc=delta_wc,fcff=fcff,present_value=fcff/(1+wacc)**i))
terminal_fcff=rows[-1]['nopat']*(1+growth)*(1-growth/roic)
pv_terminal=terminal_fcff/(wacc-growth)/(1+wacc)**5
pv_explicit=sum(x['present_value'] for x in rows)
vehicle_ev=pv_explicit+pv_terminal
# Pre-elimination segment figures from 2026 Q3; indicative only, not a fully reconciled valuation.
finance_parent_equity=23740.274
other_equity=7530.495
group_equity_elimination=-2635.414
vehicle_cash=8253.939
vehicle_borrowings=4057.933+3615.917
vehicle_associates_book=35847.785
# Applying group-consolidated carrying values to pre-elimination vehicle segment
# is an approximation and may misallocate associates between segments.
selected_books=[22045.085,3182.405,600.729,844.698,352.179]
selected_9m_market=[15489.499,2740.970,3201.471,359.156,106.369]
associates_proxy=vehicle_associates_book-sum(selected_books)+sum(selected_9m_market)
equity=vehicle_ev+finance_parent_equity+other_equity+group_equity_elimination+vehicle_cash-vehicle_borrowings+associates_proxy
common=203466492-1047534
pref_counts=[22839037,34257047,2321926]
preferred=sum(pref_counts)
shares=common+preferred
price=equity*1e9/shares
# Separate dated market-price assumptions: asset holdings still use Q3 share counts.
price_20261126=[93700,67000,349000,49000,6690]
owned_20260930=[137318251,23327400,8664334,6893596,13707293]
market_20261126=[p*n/1e9 for p,n in zip(price_20261126,owned_20260930)]
associates_20261126=vehicle_associates_book-sum(selected_books)+sum(market_20261126)
equity_market_scenario=equity+associates_20261126-associates_proxy
common_price_20261126=259000
pref_prices_20261126=[140200,146000,140600]
weighted_shares=common+sum(n*p/common_price_20261126 for n,p in zip(pref_counts,pref_prices_20261126))
market_weight_price=equity_market_scenario*1e9/weighted_shares
# 2026 year-end equity: Q3 parent book + assumed Q4 NI - one declared 2,500 KRW dividend.
book=116222.002+2000-(shares*2500/1e9)
initial_book=book
coe=.11
nis=[7600.,8200.,8800.,9300.,9700.]
payout=.45
rim=[]
for i,ni in enumerate(nis,1):
    ri=ni-coe*book
    rim.append(dict(year=2026+i,opening_book=book,net_income=ni,residual_income=ri,pv=ri/(1+coe)**i))
    book+=ni*(1-payout)
terminal_roe=.08
rim_terminal=book*(terminal_roe-coe)/(coe-growth)/(1+coe)**5
rim_equity=initial_book+sum(r['pv'] for r in rim)+rim_terminal
eps_proxy=nis[0]*1e9/shares
out=dict(status='illustrative scenario; not an investment rating or target',unit='KRW bn except shares and KRW/share',scenario_valuation_date='2026-09-30 accounts, 2026-11-26 listed marks, year-end discounting assumption',forecast=rows,dcf=dict(wacc=wacc,growth=growth,incremental_roic=roic,pv_explicit=pv_explicit,pv_terminal=pv_terminal,vehicle_ev=vehicle_ev,finance_parent_book_proxy=finance_parent_equity,other_parent_book_proxy=other_equity,group_equity_elimination_proxy=group_equity_elimination,vehicle_cash=vehicle_cash,vehicle_borrowings=vehicle_borrowings,associates_proxy_9m=associates_proxy,equity_9m_marks=equity,common_price_equal_share_claim=price,listed_prices_20261126=price_20261126,listed_holdings_20260930=owned_20260930,listed_values_20261126=market_20261126,associates_proxy_20261126=associates_20261126,equity_20261126_marks=equity_market_scenario,common_price_using_market_weighted_claims=market_weight_price),shares=dict(common=common,preferred=preferred,equal_claim_total=shares,pref_counts=pref_counts,pref_prices_20261126=pref_prices_20261126,common_price_20261126=common_price_20261126,weighted_shares=weighted_shares),per=dict(earnings_2027_assumption=nis[0],eps_equal_claim_proxy=eps_proxy,multiples={'6x':eps_proxy*6,'8x':eps_proxy*8,'10x':eps_proxy*10},note='Illustrative multiple scenarios; not observed peer multiples.'),rim=dict(opening_2026e=initial_book,cost_of_equity=coe,payout=payout,terminal_roe=terminal_roe,terminal_retention=growth/terminal_roe,terminal_payout=1-growth/terminal_roe,forecast=rim,pv_terminal=rim_terminal,equity=rim_equity,price_equal_share_claim=rim_equity*1e9/shares,price_market_weighted_claims=rim_equity*1e9/weighted_shares),warnings=['Segment values before consolidation; eliminating equity adjustment may not map fully to owners.', 'Vehicle associates proxy assumes all five investments are included in vehicle segment; verify overlap.', 'Vehicle cash includes potentially restricted and operational cash; lease/pension and NCI not fully allocated.', 'Market-weighted claims assume observed preferred/common price ratios persist, a circular and uncertain allocation assumption.', 'Standalone capital forecast and terminal ROIC are analyst assumptions, not company guidance.', 'Accounts and holdings are 2026-09-30; five market marks and preferred ratios are 2026-11-26; discounting is 2026 year-end.'])
(ROOT/'model/scenario_rebuild_20261126.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
