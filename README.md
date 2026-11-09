# JARVIS 터미널

외신 중심 시장 브리핑 터미널입니다. 같은 사건을 매체마다 어떻게 읽는지 비교하고, 세계 지도·국채 커브·경제 일정을 한 화면에 보여줍니다.

- 앱 주소: https://jsankd.github.io/jarvis-terminal/
- 크롬·엣지에서 열고 주소창 오른쪽의 설치 버튼을 누르면 데스크탑 앱처럼 설치됩니다. 폰에서는 "홈 화면에 추가"로 설치합니다.
- `data.json`은 평일 아침마다 자동으로 갱신됩니다.

## 화면

패널을 끌어서 옮기고 모서리로 크기를 바꾸는 워크스페이스입니다.

- 배치: `1` BRIEF · `2` MARKETS · `3` ALL · `4` MY(SAVE로 저장한 배치)
- 패널: MAP(세계 지도), TOP(주요 뉴스), DES(기사 상세), MTX(기사 × 매체 표), WIRE(매체별 오늘의 시각), WEI(지수), WB(국채 커브), ECO(경제 일정), HEAT(섹터), FLOW(수급)
- 명령줄: `/` 키로 열고 `TOP`, `US`, `N3`, `N 엔비디아`처럼 입력합니다. `HELP`로 전체 목록을 봅니다.
- 지도: 나라를 누르면 확대되고 그 나라 뉴스가 뜹니다. 여러 나라에 걸친 뉴스를 고르면 관련 나라가 모두 보이게 화면이 맞춰집니다.

## 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 앱 화면. `tools/build_pwa.py`가 `src/launchpad.html`에서 만듭니다 |
| `src/launchpad.html` | 앱 원본 페이지 (Claude 아티팩트 형식) |
| `src/artifact.html` | 예전 한 장짜리 화면. "JARVIS 터미널" Claude 아티팩트의 원본입니다 |
| `data.json` | 뉴스·시세·금리 데이터 (매일 갱신) |
| `map.json` | 세계 지도 점 데이터 |
| `vendor/` | 패널 배치 라이브러리 gridstack 10.3.1 (MIT) |
| `manifest.webmanifest`, `sw.js`, `icons/` | 설치형 웹앱 설정, 오프라인 캐시, 아이콘 |

## 출처

- 뉴스 묶음 데이터: [Kagi News](https://news.kagi.com) (CC BY-NC 4.0)
- 지도: Natural Earth via world-atlas
- 패널 배치: [gridstack.js](https://github.com/gridstack/gridstack.js) (MIT, `vendor/gridstack-LICENSE`)
- 요약과 "JARVIS VIEW"는 Claude가 정리한 내용입니다. 투자 조언이 아닙니다.
