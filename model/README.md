# [모델 사용 안내]

`forecast.csv`에는 매출, 영업이익률, 자동차 FCFF의 Base 가정이 있다.

`valuation_results.json`은 `scripts/build_valuation.py` 실행 결과다. 자동차 FCFF DCF에 금융·기타 사업 가치와 전략 지분을 연결했다. 연결 금융부채를 제조업 순차입금으로 일괄 차감하지 않는다.

`rim_schedule.csv`에는 지배주주 자본, 순이익, 자본비용, 잔여이익 계산이 들어 있다.


`Hyundai_Motor_Equity_Research_Model.xlsx`에는 Summary, Forecast, Valuation, Sources 시트를 넣었다. 실제치와 분석 입력값을 분리했고, DCF·정상화 PER·RIM의 주요 산식을 확인할 수 있다.
