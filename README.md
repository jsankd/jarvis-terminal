# JARVIS 터미널

외신 중심 시장 브리핑 터미널입니다. 같은 사건을 매체마다 어떻게 읽는지 비교하고, 세계 지도·국채 커브·경제 일정을 한 화면에 보여줍니다.

- 앱 주소: https://jsankd.github.io/jarvis-terminal/
- 크롬·엣지에서 열고 주소창 오른쪽의 설치 버튼을 누르면 데스크탑 앱처럼 설치됩니다. 폰에서는 "홈 화면에 추가"로 설치합니다.
- `data.json`은 평일 아침마다 자동으로 갱신됩니다.

## 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 앱 화면. `tools/build_pwa.py`가 `src/artifact.html`에서 만듭니다 |
| `src/artifact.html` | Claude 아티팩트용 원본 페이지 |
| `data.json` | 뉴스·시세·금리 데이터 (매일 갱신) |
| `map.json` | 세계 지도 점 데이터 |
| `manifest.webmanifest`, `sw.js`, `icons/` | 설치형 웹앱 설정, 오프라인 캐시, 아이콘 |

## 출처

- 뉴스 묶음 데이터: [Kagi News](https://news.kagi.com) (CC BY-NC 4.0)
- 지도: Natural Earth via world-atlas
- 요약과 "JARVIS VIEW"는 Claude가 정리한 내용입니다. 투자 조언이 아닙니다.
