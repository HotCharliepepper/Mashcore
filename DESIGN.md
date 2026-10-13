# Mashcore — Scene & Spatial v4

상태: 사용자가 GitHub 반영과 운영 배포를 승인한 구현 버전. 실제 배포 결과는 PR과 Netlify 기록으로 확인한다.
기록: 2026-10-14 KST. 출발점: Editorial Review v2 + 기존 GitHub 연구 콘텐츠 + Editorial Research v3.

## 근거의 상태

**CONFIRMED**
- 사용자가 짧은 철학·이미지 중심 랜딩, 장면별 스크롤 연출, Chore to Play 3D/기울기, 모바일 별도 보기, Mashcore 푸터, 공란 사업자 정보, 향후 mashcore.kr을 요청했다. 이번 과정의 반영·배포를 승인했다.
- 기존 Chore to Play 연구는 여덟 단계의 단일 발달축을 보류하고 있다. 여섯 관점은 동시에 존재하는 범주이며, 사람의 등급이 아니다.
- 기존 연구 6개 경로, Weplace 역할, 공개 이메일, 파비콘은 유지한다.
- 운영 호스트는 mashcore.netlify.app이고 GitHub main이 Netlify 배포와 연결되어 있다.

**NEED VERIFY**
- 실제 iPhone Safari / Android Chrome에서 센서 허용·회전·배경 전환, 320/390/820/1440px 렌더링, 글자 확대 200%.
- 사업자 등록 완료 정보와 mashcore.kr 소유권·DNS·TLS. 공개 DNS 조회는 NXDOMAIN이었으며 이것만으로 미등록 여부를 단정하지 않는다.
- Mashcore 전용 이메일 여부. 현재는 기존 공개 주소 weplace25@gmail.com을 유지한다.

**HYPOTHESIS**
- 첫 문장과 구성 이미지가 긴 소개보다 브랜드의 관찰 태도를 빠르게 전할 수 있다.
- 여섯 관점을 직접 선택하고 시점을 바꾸는 경험이 단일 성장 사다리보다 현재 연구의 다층적 구조를 잘 설명할 수 있다.
- 장면 단위 등장 연출이 자연스러운 읽기를 해치지 않으면서 집중을 도울 수 있다. 이용 반응으로 재검토한다.

## A. 화면의 목표와 고객 심리

“어떤 생각을 하는 곳인가?”를 먼저 느끼고, 연구를 만진 뒤 필요할 때 깊이 읽고 자기 장면을 남긴다.

1. **보다**: 문 앞에 멈춘 사람의 구성 이미지. “보이는 것 너머, 사람의 이유를 봅니다.”
2. **다시 놓다**: Chore to Play의 여섯 관점. 현재 연구의 핵심을 직접 선택한다.
3. **이어 가다**: Mashcore의 질문과 Weplace의 실행, 현장 반응의 순환. Market Interpretation 연구로도 이어진다.
4. **묻다**: 한 줄 입력 → 이메일 앱에서 확인·직접 전송 또는 복사.

첫 이미지의 사람과 공간은 설명을 위한 벡터 구성 이미지이며, 실제 고객·사례·현장 사진이 아니다. 성과 수치·고객 평가·확정 상품은 만들지 않는다.

## B. 유지·개선한 부분

| 대상 | 유지 | v4 변경 |
|---|---|---|
| 홈페이지 | Mashcore 정체성·연구와 현장 관계·질문 복사/메일 | 긴 소개를 네 장면으로 압축, SVG 장면과 입체 연구 모형 |
| 이전 홈 내용 | 관점 탭 3개, 주제 탭 5개, 에세이, 로그 | `/explore/`로 보존. 이전 #way/#rooms/#archive는 해당 내용으로 연결 |
| Chore to Play | 역사적 가설·재분류·의미/즐거움·조건 탐색·L0–L1 | 6개 관점 3D 모형을 추가. 기존 조건 4개 조합과 초기화 유지 |
| 모바일 | 같은 철학·콘텐츠·연구 경로 | `/mobile/` 전용 세로 구성, 큰 조작 영역, 컨테이너 기준 모형 크기 |
| 비교 | 실제 운영 코드 | `/preview/?view=desktop` 1440×960, `?view=mobile` 390×844 비교 및 새 창 |
| 푸터 | 연구·소개·연락 경로 | Mashcore 워드마크, 사업자 정보는 빈 문자열로 준비 |
| 검색 주소 | 현재 유효한 Netlify 주소 | 모바일은 루트 canonical 공유, 비교 페이지 noindex, DNS 연결 전 임의 전환 안 함 |

코드가 구현의 기준이다. Figma 캔버스를 변경하거나 자동 동기화했다고 주장하지 않는다. 기존 Figma 파일은 후속 시각 협업에 사용할 수 있으며 프레임 인계는 `docs/FIGMA_HANDOFF_v4.md`에 기록한다.

## C. 디자인 레퍼런스와 채택 이유

- **승인 전후 기존 자산 / Editorial Review v2–v3**: 차콜 표지·따뜻한 종이·절제된 모래색, 한국어 세리프와 편집적 여백을 이어 간다. 새 로고로 교체하지 않는다.
- **기존 GitHub 연구 문서**: 현재의 재분류 원리가 3D의 내용과 관계를 결정한다. 장식 오브젝트보다 연구 그 자체를 시각화한다.
- **이전 조사 Design Threads** ([원본](https://www.designthreads.report/)): 질문·방법·한계를 구분해 깊이 읽는 원리만 유지한다. 레이아웃·문구·연구 실적을 복제하지 않는다.
- **문턱 구성 이미지**: 실사처럼 오인할 합성 사진 대신 정확히 설명할 수 있는 SVG 구성을 선택했다. ‘멈춤’은 관찰이며 이유는 확정하지 않는다는 브랜드 태도를 표현한다.
- **MDN [기기 방향](https://developer.mozilla.org/en-US/docs/Web/API/Device_orientation_events/Detecting_device_orientation) / [touch-action](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action)**: 사용자 제스처 후 센서 허용, 기능 감지, 세로 스크롤과 핀치 확대 보존의 기술 근거.

토큰: ink `#202124`, paper `#f3f0e8`, sand `#c7bba8`; Gowun Batang / EB Garamond / Noto Sans KR. 외부 폰트가 없으면 시스템 폰트로 읽는다.

## D. 복사 가능한 Google Stitch 실행 프롬프트

```text
Refine the implemented Mashcore Scene & Spatial v4 site in HotCharliepepper/Mashcore. Use current index.html, mobile/index.html and assets as the source of truth.
Create comparable 1440px desktop and 390px mobile Figma-ready screens. Keep all screen copy Korean, except the existing brand and research names. Keep the current wordmark and favicon.
Art direction: human-centered, clean editorial, quiet premium. Use graphite #202124, warm paper #F3F0E8 and restrained sand #C7BBA8. Preserve Gowun Batang Korean display typography and readable sans-serif text.
Create four distinct scenes with natural vertical document scrolling, not a carousel:
1. “보이는 것 너머, 사람의 이유를 봅니다.” An editorial vector scene of a person pausing at a doorway. This is an illustrative composition, not a client case.
2. “같은 일 안에, 다른 층위가 있습니다.” The Chore to Play spatial model places six simultaneous lenses around one activity: action, obligation, economic structure, relational role, practice, meaning/experience. This is research in progress, not a developmental ladder or score.
3. “질문은, 현장을 만나 깊어집니다.” Connect Mashcore interpretation, Market Interpretation research and Weplace field practice.
4. “지금, 어떤 장면이 마음에 남아 있나요?” One short input, copy action and email drafting.
Compose each scene as a focused presentation, with staggered object entrance rather than sliding the whole page. Keep normal scroll, keyboard access, reduced-motion mode and all content available without animation.
Mobile: vertical composition, touch controls, portrait/landscape behavior, no hover dependency. Include states for tilt off, permission request, permitted, denied, unsupported and reduced motion. Tilt changes camera pose only. Never auto-request permission.
Footer: Mashcore. Leave all business registration values empty. Keep all existing research routes and the preserved Explore page. No invented outcomes, testimonials, addresses or SEO/GEO promises.
Return changes with rationale; this is a visual proposal, not an instruction to overwrite production.
```

## E. 시안 생성 후 수정 프롬프트

```text
Create a quieter alternative for the same four scenes using a predominantly warm-paper cover. Keep the exact Korean content, doorway meaning, research scope, interactions and navigation. Compare graphite-cover vs paper-cover rhythm and explain the tradeoff. Do not introduce a new logo, decorative 3D objects or a stage-based growth claim.
```

```text
Refine only the 390px and 320px Chore to Play scenes. Show all six labels without clipping at the allowed camera angles. Keep native vertical scrolling and pinch zoom, keyboard-equivalent controls, an explicit tilt opt-in and readable static alternatives. Reduce controls' visual density without deleting any interaction or research qualification.
```

## F. 디자인 평가표·개발 인계

| 평가 기준 | 구현 / 확인 | 남은 실기기 검수 |
|---|---|---|
| 짧은 철학·장면 위계 | 홈을 4개 장면으로 구성, 기존 긴 글은 Explore에 보존 | 첫 방문자가 브랜드 역할을 어떻게 이해하는지 |
| 개념의 정확성 | 여섯 관점, 서열·최종 Play·진단 점수 없음 | 연구자의 후속 의미 검토 |
| 3D 입력 동등성 | 선택 버튼·가로 드래그·방향키·초기화·기울기 | 실제 기기 센서와 CSS3D 시각 결과 |
| 모바일 | 전용 경로·컨테이너 폭·세로 스크롤·화면 비교 | 320/390px, 가로 회전, 200% 확대 |
| 움직임 | 자연 스크롤·장면별 요소 등장·reduced-motion | 멀미·피로·빠른 스크롤 상태 |
| 접근성 | 문서 순서·한 개 H1·ARIA 참조·키보드·이미지 대체 설명 | VoiceOver/TalkBack 및 대비 실측 |
| 기존 기능 | 메뉴·탭·조건 4조합·복사·메일·글 읽기 | 실제 메일 앱·모바일 복사 메뉴 |
| SEO/GEO | 제목·설명·canonical·JSON-LD·sitemap, 비교 noindex | mashcore.kr TLS 연결 후 주소 전환 |
| 운영 | 사업자 설정 한 파일, 기존 Git CD | 등록 사실 확인 후 실제 값 입력 |

정적 HTML 9개 경로의 링크·자산·ID/ARIA·JSON-LD 검사 및 JS 구문 검사를 실행했다. Node DOM 시뮬레이션으로 메뉴·탭·복사·메일·조건 탐색·비교 모드·사업자 텍스트 렌더링과 센서 권한/실패/회전/중단/모션 감소 9개 시나리오를 확인했다. 이것은 브라우저 렌더링 또는 물리 센서 검증이 아니다. 현재 환경에는 Sites 스킬이 요구하는 control-browser 기능이 없어 브라우저 QA를 생략했다.

- 사업자 입력: `assets/js/site-config.js`의 빈 값만 실제 등록 내용으로 채운다. 모든 페이지가 공유하고 빈 필드는 표시하지 않는다.
- 홈 수정 후: `python3 scripts/sync_mobile.py` 실행. 모바일은 루트 콘텐츠를 공유하되 전용 모바일 레이아웃을 쓴다.
- 도메인: `docs/DOMAIN_AND_OPERATIONS.md`의 소유권·DNS·HTTPS 확인 후 metadata 전환.
- 센서는 브라우저 메모리에서만 사용하며 수집·전송·저장하지 않는다. 문장 입력도 자동 저장·전송하지 않는다.
- 기존 v3 기록은 `docs/DESIGN_v3_archive.md`에 보존한다.
