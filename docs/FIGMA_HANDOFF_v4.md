# Mashcore v4 — Figma 인계

기존 협업 파일: https://www.figma.com/design/e2C0JjYTRiwiW9Fxh3f8X7
이번 구현에서는 Figma 캔버스를 수정하거나 Code Connect를 구성하지 않았다. 배포 코드와 아래 상태 목록이 다음 Figma 편집의 기준이다.

| 프레임 | 실제 코드 | 확인할 상태 |
|---|---|---|
| Desktop 1440×960 | `/preview/?view=desktop` → `/` | 네 장면·메뉴·질문 입력 |
| Mobile 390×844 | `/preview/?view=mobile` → `/mobile/` | 세로 구성·좁은 화면·터치·입력 |
| Chore spatial | 홈 및 `/research/chore-to-play/#spatial-relations` | 6선택, 기울기 off/pending/on/denied/unavailable, reduced motion |
| Research reading | 기존 연구 5개 경로 및 `/explore/` | 읽기·탭·목차·조건 탐색 |
| Footer | 모든 콘텐츠 페이지 | business-info empty/populated |

컴포넌트: SiteHeader / ChapterIntro / ThresholdIllustration / SpatialModel / LensSelector / SpatialReading / SpatialControls / ResearchLink / QuestionDraft / Footer.
토큰·철학·Stitch 프롬프트·검수 기준은 루트 DESIGN.md를 따른다. 기울기 화면은 실제 동작 코드로 검토하고 Figma에서 센서 작동이 검증됐다고 기록하지 않는다.
