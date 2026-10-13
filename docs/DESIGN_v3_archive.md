# Mashcore Lab — Editorial Research v3

상태: **구현·검토 제안 / 디자인 승인 전**  
기록일: 2026-10-14 (Asia/Seoul)  
기준 코드: `9b3878bc9c9225926b279eeebbeb1ecb992201fa`  
디자인 출발점: `Mashcore_Editorial_Review_v2.html`

## 결정

이번 단계는 TGK가 기존 GitHub 코드에 직접 통합한다. 6개 공개 경로와 기존 연구 내용을 유지하면서 누락된 자산, 서로 다른 페이지 셸, 연결되지 않은 읽기 경로를 함께 정리할 수 있기 때문이다.

Figma는 배포 소스나 자동 양방향 동기화 대상으로 삼지 않는다. 기존 Figma 파일은 화면·컴포넌트 협업 기준으로 유지하고, 검토된 코드의 토큰과 상태를 다음 디자인 반영의 출발점으로 삼는다. 이번 변경은 Figma 캔버스를 수정하지 않는다.

| 방식 | 얻는 것 | 비용·한계 | 이번 판단 |
|---|---|---|---|
| Figma에서 전체 화면 재구성 후 구현 | 편집 가능한 화면 비교와 디자인 협업 | 기존 6개 경로·기능을 다시 코드와 맞춰야 함 | 후속 시각 조정 단계 |
| 기존 저장소에 직접 통합 | 실제 콘텐츠·URL·동작을 한 번에 검토 | 브라우저 화면 검수와 디자인 승인 필요 | **우선 실행** |

## 근거 상태

**CONFIRMED**

- Netlify `mashcore`의 공개 배포와 GitHub `main`이 위 기준 커밋을 가리킨다.
- 저장소에는 Home, Research, Chore to Play, Market Interpretation, Research Log, About의 6개 HTML이 있다.
- 홈에서 참조하던 CSS 5개와 JS 2개가 기준 저장소에 없다. 운영 HTTP 점검에서도 `assets/css/tokens.css`, `assets/js/navigation.js`는 404다.
- 현재 공개 연구는 Chore to Play와 Market Interpretation이다. 2026.06.16 및 2026.08.17 기록은 기준 저장소에서 가져왔다.
- 현재 홈페이지의 연락처 `weplace25@gmail.com`, 워드마크 `MASHCORE LAB`, 인라인 파비콘을 이어받았다.
- Figma 파일 `e2C0JjYTRiwiW9Fxh3f8X7`에는 `01 — Homepage`, `02 — System & Handoff` 페이지가 있다.

**NEED VERIFY**

- 새 헤드라인·배치·팔레트의 최종 디자인 승인.
- 실제 브라우저에서 1440 / 820 / 390 / 320px 및 확대 200%의 시각·터치 검수.
- Mashcore 전용 연락처로 분리할지 여부. 이번에는 기존 공개 이메일을 유지한다.
- Sense OS / FIELD OS를 이 홈페이지에서 공개할 범위. 확인되지 않은 별도 상품·프로그램 페이지는 이번에 만들지 않는다.

**HYPOTHESIS**

- 관점 탐색 뒤 실제 연구로 이동하면 추상적인 브랜드 소개가 구체적인 읽기 경험으로 이어질 수 있다.
- Chore to Play의 조건 탐색이 자신의 반복 업무를 돌아보는 질문을 만들 수 있다. 진단·심리 측정·효과 입증 도구는 아니다.

## A. 목표와 고객 심리

첫 방문자는 철학의 용어를 배우기 전에 자신의 장면을 떠올린다. 이후 연구를 읽고, 생각이 바뀐 이유와 열려 있는 질문을 확인한다. 필요하면 자기 장면을 한 줄 정리한다.

흐름: 첫 문장 → 같은 장면의 다른 관점 → 현재 연구 2개 → 살피는 5개 주제 → 현장 실행과 연결 → 연구 기록·글 초안 → 질문 정리.

Chore to Play는 Mashcore 전체의 정의가 아니라 대표 연구 프로그램이다. 사람을 여덟 등급으로 나누거나 Play를 보장된 최종 단계로 표시하지 않는다.

## B. 유지와 개선

| 영역 | 유지 | 변경 |
|---|---|---|
| Home | v2 관점 탭·주제 탭·읽기 패널·질문 복사 | 실제 연구 2개·변경 기록·이메일 작성 연결 |
| Research | 기존 섹션 내용·Market 판단 구조·열린 질문 | 상세 연구로 직접 이동, 공통 읽기 디자인 |
| Chore to Play | 초기 가설·재분류·매트릭스·모델·L0–L1·열린 질문 | 긴 영어 본문 한국어 정리, 독립 조건 2개 탐색 |
| Market Interpretation | 기존 모든 연구 섹션과 목차 앵커 | 공통 디자인, 읽기 폭, 작은 화면 배열 |
| Research Log | 2026.06.16 기존 기록 | Research Index의 2026.08.17 기록 통합 |
| About | 기존 소개·역할·원칙·경계·앵커 | 저장소 작업 사진, 실제 Weplace 연결 |

기존 워드마크·파비콘·이메일을 보존한다. 헤르메스 신규 로고나 임의 사무실·연구 실적은 만들지 않는다. 원문의 6–8주 소그룹 문구는 확정된 상품 일정으로 오해하지 않도록 탐색 상태를 명시했다. 효과 수치와 성과 약속은 추가하지 않는다.

## C. 시각 원리와 참고

- v2의 차콜 표지와 밝은 읽기 공간을 유지한다. 기존 저장소의 한국어 Gowun Batang / 읽기용 산세리프 원칙을 반영한다.
- 본문은 16px 이상, 긴 문장은 최대 약 720–780px. 영문은 연구명·짧은 편집 라벨에 사용한다.
- 정보는 구분선과 여백으로 나누고, 연구 항목은 반복 카드 대신 편집 행으로 구성한다.
- 기존 조사 참고: [Design Threads](https://www.designthreads.report/)의 방법·한계·질문별 읽기 구조. 연구 실적이나 고유 레이아웃은 가져오지 않는다.
- 움직임은 상태 전환과 읽기 진행에만 사용한다. 스크롤을 가로채거나 본문을 등장 효과 뒤에 숨기지 않는다.

## D. Stitch 실행 프롬프트

```text
Use the current design/editorial-research-v3 branch of HotCharliepepper/Mashcore as the content and interaction source of truth.
Refine the existing six-page Korean editorial website; do not replace it with a single marketing page.
Preserve the MASHCORE LAB wordmark, current favicon, all public paths, Korean research content, working tabs, copy fallback, email drafting, and the Chore to Play condition exploration.
Keep a graphite cover (#202124), warm paper (#F3F0E8), restrained sand (#C7BBA8), Gowun Batang display text, and readable sans-serif body text.
Show 1440px desktop and 390px mobile candidates for Home and Chore to Play.
Chore to Play is a research program in progress, not a validated eight-stage development theory. Preserve the distinction between historical hypothesis, current interpretation and illustrative exploration.
Do not invent research outcomes, offices, publications, testimonials, prices, reply times or automatic diagnosis.
Refine hierarchy, reading width, spacing and navigation. Return proposed visual changes and their reasons. Do not deploy or alter content facts.
```

## E. 수정 프롬프트

```text
Refine only the mobile Chore to Play condition exploration. Keep the two independent native radio groups, all four qualitative question states, reset behavior, no-JavaScript explanation and illustrative-example label. Reduce visual density without turning the interaction into a score, level or personality diagnosis. Keep the remaining pages unchanged.
```

```text
Refine only the homepage transition from the viewpoint experience to Current Research. Make the link to Chore to Play and Market Interpretation easy to notice without repeating their full articles. Preserve all research status labels, paths and existing functionality. Avoid decorative motion or generic SaaS feature cards.
```

## F. 평가와 개발 인계

평가 기준: 사실·가설 구분 20 / 자기 발견 20 / 브랜드 역할과 문장 20 / 의미 있는 동작 15 / 모바일·접근성 15 / 기존 자산·경로 연속성 10. 각 항목 0–5점으로 비교하되 실제 검토 전 점수를 임의로 채우지 않는다.

### 구현 구조

- `assets/css/editorial.css`: v2의 기본 편집 디자인.
- `assets/css/research.css`: 공통 셸, 연구 페이지, 폭별 조정. 현재 디자인 값의 코드 기준.
- `assets/js/site.js`: 메뉴·탭·질문 복사/이메일 초안·조건 탐색·읽기 진행.
- `sitemap.xml`, `robots.txt`: 기존 6개 공개 경로. Netlify Deploy Preview의 noindex는 호스팅이 제공하며 운영본의 검색 설정을 임의로 막지 않는다.
- 외부 실행 스크립트와 런타임 Tailwind CDN 제거. 폰트 CDN이 실패해도 시스템 폰트로 본문을 읽을 수 있다.
- 새 서버·폼 수집·DB·분석 전송 없음. 이메일 링크는 사용자의 메일 앱을 열며 자동 발송하지 않는다.

### 검수

- 6개 HTML의 내부 경로·앵커·로컬 자산·고유 ID·ARIA 참조·이미지 alt·JSON-LD 검사 통과.
- JavaScript 구문 검사 통과.
- Node DOM 모의 실행: 6개 페이지 초기화·메뉴 열기/Escape 닫기, 관점 탭·방향키/Home/End, 주제 탭, 질문 복사 성공/실패/빈 값, 이메일 본문 인코딩, 조건 4조합/초기화 통과.
- **브라우저 렌더링과 실제 클릭·터치 검수는 미완료.** 현재 환경에 허용된 control-browser가 없어 Sites 스킬의 규칙에 따라 다른 브라우저 경로로 우회하지 않았다.
- 운영 반영 전: 가로 넘침·제목 줄바꿈·폰트 실패·메뉴 초점·200% 확대·모바일 표·이메일 앱 연결 확인.

### 운영 반영

현재 작업은 검토 브랜치/PR까지다. 사용자의 디자인 선택 후 `main`에 병합해 기존 Netlify 연동으로 배포한다. 운영 도메인 변경, 사이트 재생성, 수동 운영 배포는 하지 않는다. 운영 반영을 위해 별도 플랫폼으로 이전할 필요가 없다.

구형 `docs/01`–`05` 문서는 이력이다. 이번 변경의 판단 기준은 이 문서와 `docs/FIGMA_HANDOFF_v3.md`를 우선한다.
