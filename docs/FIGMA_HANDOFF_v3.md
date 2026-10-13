# Figma ↔ Code — v3 인계

## 현재 연결 범위

[MASHCORE — Official Website / 2026 Renewal v0.1](https://www.figma.com/design/e2C0JjYTRiwiW9Fxh3f8X7)

메타데이터 확인: `01 — Homepage` (0:1), `02 — System & Handoff` (2:2).

이번 구현은 코드 직접 통합을 선택했다. **Figma 캔버스 수정, Code Connect 설정, 자동 동기화를 완료했다는 뜻이 아니다.** 기존 디자인 파일의 방향과 실제 코드의 변경 근거를 서로 찾을 수 있게 한 인계 기록이다.

## 다음 디자인 반영 범위

기존 화면을 덮어쓰기보다 `Editorial Research v3 / Candidate` 페이지에 아래 두 화면을 비교한다.

1. Home 1440 / 390: 표지, 관점 탐색, 현재 연구, 주제, 현장, 기록, 질문.
2. Chore to Play 1440 / 390: 초기 가설, 개념 지도, 조건 탐색, 의미·즐거움 표, 현재 연구 상태.

## 코드 값과 디자인 이름

| 디자인 이름 | 코드 기준 | 값 |
|---|---|---|
| Color / Ink | `--ink` | `#202124` |
| Color / Paper | `--paper` | `#F3F0E8` |
| Color / Accent | `--accent` | `#C7BBA8` |
| Color / Rule | `--rule` | `#D8D2C7` |
| Type / Display Korean | `--serif` | Gowun Batang; Batang fallback |
| Type / Reading | `--body` | Pretendard or Noto Sans KR; system fallback |
| Type / Editorial Latin | `--latin` | EB Garamond; Georgia fallback |
| Layout / Reading Max | `--reading-width` | 720px |
| Layout / Narrow navigation | media rule | 820px |

정확한 값은 `assets/css/editorial.css`, 이후 적용되는 `assets/css/research.css`를 함께 확인한다. 토큰을 변경하면 실제 구현과 화면을 같은 변경 단위로 검토한다.

## 상태를 함께 그릴 컴포넌트

| 요소 | 상태 | 코드 |
|---|---|---|
| Header | desktop / mobile closed / mobile open | `.site-header`, `#main-nav` |
| Viewpoint | person / brand / place | `#lens-*` |
| Research row | Chore to Play / Market Interpretation | `.research-row` |
| Research rooms | people / brand / space / relation / technology | `#room-*` |
| Condition exploration | agency low/high × feedback low/high | `.condition-lab` |
| Working note | collapsed / expanded | `details.essay` |
| Question | empty / typed / copied / manual-copy fallback | `#question`, `#copy-status` |

관찰 장면을 고정하고 질문·가설·확인할 일을 바꾸는 구조를 보존한다. 네 가지 조건을 점수나 성장 등급으로 표현하지 않는다. 접근성 상태·키보드 행동은 그림만으로 확정하지 않고 실제 코드 검수와 함께 확인한다.
