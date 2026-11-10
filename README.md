# 과점시장 모형 시뮬레이터

산업조직론 1장(과점시장) 모형을 슬라이더로 조절하며 파이썬으로 시각화·시뮬레이션하는 정적 웹페이지입니다.
브라우저 안의 Pyodide(파이썬 + numpy + matplotlib)가 계산하므로 서버가 필요 없습니다.

모형: 쿠르노(담합 붕괴) · 베르트랑(역설) · 스타켈베르크 · 제품 차별화(가격 vs 수량, 순차 가격) · 자유진입 · 행태 모수 · 모형 비교

## GitHub Pages로 올리기
저장소 Settings → Pages → Branch: `main` / `(root)` 선택. 곧 `https://profguclass.github.io/Oligopoly/` 에서 열립니다.

## 로컬 실행
`python3 -m http.server 8000` 후 http://localhost:8000

## 구조
- `py/models.py` 각 모형의 계산·그래프 (모형마다 함수 하나)
- `app.js` 탭·슬라이더 정의 (새 모형은 `MODELS`에 항목 추가)
