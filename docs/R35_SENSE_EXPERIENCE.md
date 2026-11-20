# MASHCORE R3.5 — 독립 SENSE EXPERIENCE

기록: 2026-11-03 KST. 검증된 사실과 설계 의도를 구분한다.

## 읽기 전용 기준선

| 대상 | 고정 참조 | 확인한 내용 |
|---|---|---|
| 운영 main / R3.1 | `a8dae1c4b6e69cd02e24b5e28bc9600f5a756fcf` | Origin 포스터·영상·질문·서비스 CTA, 관찰/다른 설명/다음 확인, 기존 상세 경로 |
| Draft PR #18 / R3.4 Phase 2 | `3dc53993473389ddaac037e7d9f82a512a4173cc` | R3.2–3.4가 쌓인 stacked Draft. LAB/NOTES/Studio 링크, native details, 가상 정보 전후 비교. 독립 병합 불가 안내 |
| Figma 보드 | [사용자 제공 FigJam](https://www.figma.com/board/lZuplMlNJ9eOM3fu93GYms) | S31 `5:95` 시선 경로 04, `5:143` 예측가능성 25·통제감 26. 관찰→가설→반례 원칙. 보드 수정 없음 |
| Netlify 운영 배포 | `6ae1f7c19ddb6a779b397b20` | 작업 시작 시 현재 배포. 끝에 다시 확인 |

로컬 브랜치는 main에서 새로 만들었다. PR #18의 파일을 가져와 누적하지 않았다. `index.html`, `mobile/index.html`, 모든 기존 자산과 상세 페이지, 기존 공개 패키징 코드는 변경하지 않았다.

## 실행과 배포 경계

- 원본: `experiments/sense-r35/`. 로컬: `node qa/r35/serve.mjs` → `http://127.0.0.1:8350/sense-r35/`.
- 배포 출력: Deploy Preview의 `/sense-r35/`만. `netlify.toml`의 deploy-preview 명령 끝에 새 전용 패키저를 추가한다.
- 원래 `prepare_public.py`와 `check_release.py`가 먼저 완료되어야 한다. 그 뒤 HTML/CSS/JS/폰트/폰트 라이선스 5개 파일만 복사한다. 문서·QA·캡처·실험 소스 트리 전체를 배포하지 않는다.
- production 및 branch-deploy의 명령과 결과는 기존 로직을 유지한다. 실험에는 `noindex,nofollow`가 있으며 Preview 전체의 X-Robots-Tag가 유지된다. 실험을 운영 canonical로 위장하지 않는다.
- 이번 산출물은 Draft/Preview 검토용이다. main 병합, 운영 배포, DNS 변경 없음.

## 개선 전후

| 관점 | R3.1 / R3.4에서 확인 | R3.5에서 구현 | 판단의 한계 |
|---|---|---|---|
| 첫 장면 | 기존 질문과 서비스 CTA, 영상 장면 | 포스터 기본 상태, 짧은 질문, 첫 화면 안의 서비스 설명과 CTA. 휴대폰에서는 질문→설명→CTA→장면 순서 | 이해가 실제로 빨라졌다는 측정 결과는 아님 |
| 다른 설명 | 관찰/다른 설명/다음 확인이라는 단계 선택 | 안내 찾기·기다림·생각 정리 세 가설을 방문자가 직접 선택. 각각 확인 질문과 반례 표시 | 어떤 선택도 사실·정답·진단이 아님 |
| 연구 경험 | Chore to Play 6관점 및 R3.4 정보 배치 전후 예시 | S31 04·25·26을 실제 native control로 만지는 세 예시 | 고객 심리·시선·전환 효과를 측정하지 않음 |
| 모션 | 기존 홈 및 PR의 장면/구절 연출 | 사용자 요청 영상과 읽기 순서 번호 예시만. 자동 진입/스크롤 모션 없음 | 화려함보다 설명과 통제 요구 우선 |
| JS 실패 | 기존 원본도 본문 fallback 보유 | 세 가설 전체·CSS 비교·details·길이 선택·reset·링크 유지 | 실제 AT 사용자 검수 별도 |

## Decision Log

| 결정 | 관찰·근거 | 가설 / 반례 | 선택·다음 확인 |
|---|---|---|---|
| main 기반 독립 브랜치 | PR #18은 stacked Draft | 누적 기반이면 R3.5의 효과와 범위를 분리하기 어려움 | 기존 main에서 분기; 보호 경로 diff 확인 |
| 영상·포스터 재사용 | R3.1에 68,196-byte WebP와 2,181,118-byte MP4 존재 | 새로운 이미지가 설명에 필수라는 근거 없음 | 원본 변경·복제 없이 URL 참조; 생성 장면 고지 유지 |
| 같은 장면을 두 크기로 반복 | 문 앞의 멈춤이 브랜드 고유 소재 | 다른 사진은 가설의 근거로 잘못 읽힐 수 있음 | 큰 Origin + 가까운 Second Look. 임의 stock 이미지 추가 안 함 |
| 기존 시각 언어 확장 | forest `#18241c`, paper `#f4efe6`, 고운바탕이 현재 원본에 존재 | 오래된 DESIGN.md에는 현재와 다른 연락처·영상 설명이 있음 | 현재 코드 우선; 전사 DESIGN.md 변경 안 함 |
| Taste 방향 선택 | 로컬 설치 확인, 세 방향 중 `uneven-photographs`, seed 1574312346 | 다수 사진·가림 모션 요구는 한 장면과 접근성 요구에 맞지 않음 | 비대칭 사진·단차 제목·반복 크기만 적용. 추가 사진·masked headline은 사용자 범위에 따라 제외 |
| 세 가설은 라디오 | 하나의 설명에 집중해도 바꿀 수 있어야 함 | 최초 선택을 정답처럼 보이게 하면 목적 손상 | 미선택 시작, 확인·반례 쌍, 정답·점수 없음 |
| S31 번호 유지 | FigJam의 04/25/26이 원본 식별자 | 장식 번호처럼 오해될 수 있음 | 개념 찾아가기 링크에만 S31 식별자로 표시 |
| 예측가능성 native details | 펼치기 전후가 바로 비교 가능 | 자동 펼침은 통제감을 약화할 수 있음 | 처음 닫힘, 직접 열고 닫음, JS 의존 없음 |
| 통제감 native form | 길이 선택과 reset으로 되돌림 제공 | 실제 예약/동의를 흉내 내면 오해 가능 | 개인정보·제출 버튼 없음. 화면 안의 예시만 변경 |
| GSAP 제한 | 기존 3.15.0 파일 존재. [공식 Timeline 문서](https://gsap.com/docs/v3/GSAP/Timeline/), [kill 문서](https://gsap.com/docs/v3/GSAP/Timeline/kill%28%29/) 확인 | 자동 장식 모션은 학습에 필요하지 않음 | 명시적 포인터 요청 시 번호 opacity 순서 1.59초. 텍스트는 움직이지 않음. 키보드·reduced motion은 즉시 정적 결과. 모드 변경 시 kill |
| 로컬 폰트 subset | 기존 고운바탕 400 사용, 배포 파일 47,796 bytes | 외부 폰트 장애 시 첫 장면 인상이 달라질 수 있음 | 필요한 364개 고유 글자 로컬 WOFF2 + OFL. 본문 OS 한국어 sans. 신규 글자 추가 시 subset 재생성 |
| 미리보기 전용 GEO 본문 | 사용자 요청은 읽을 수 있는 본문 | Preview 색인 노출이 성과·운영본으로 오해될 수 있음 | 정의·가설·한계·내부 링크를 서버 HTML에 배치. noindex 유지. GEO 효과 보장 없음 |

소유자: 구현 에이전트. 날짜: 2026-11-03. 실제 사용자 이해/현장 반례/효과의 다음 검토는 사용자 연구가 필요하며 이번 코드 QA로 대신하지 않는다.

## 고정된 실험의 디자인 계약

- **THESIS:** 멈춤은 관찰이고, 설명은 수정할 수 있는 가설이다.
- **OWN WORLD:** R3.1의 forest/paper/고운바탕과 문 앞 Runway 장면을 계승한다. 별도의 브랜드 세계를 만들지 않는다.
- **STORY:** Origin의 서비스 이해 → 세 설명과 반례 → S31 04/25/26 조작 → LAB·서비스로 이어진다.
- **FIRST VIEWPORT:** 읽을 수 있는 질문, 서비스 의미와 CTA를 기존 포스터와 함께 PC·모바일에 배치한다.
- **FORM:** 정적 시맨틱 HTML/CSS, native control, 로컬 subset, 명시적 영상 재생과 요청한 설명용 GSAP만. 자동 진입 모션 없음.

Impeccable new-work의 precisely specified narrow request 예외를 적용했다. 새 컨셉 승인, seed, QUALITY BAR card, comp를 생성했다고 주장하지 않는다.

## 디자인 도구 검수 해석

Taste, Impeccable, Emil 철학 기반 animate가 설치되어 있음을 먼저 확인했다. Taste draw/lint/inspect와 Impeccable context/detect를 실행했다. 기존 브랜드와 명시된 세 장면이 결정된 좁은 실험이므로 별도 컨셉 승인 라운드를 만들지 않았다.

Taste의 자동 모션 하한은 사용자 요구와 반대이므로 `still-page` 예외를 둔다. cream 경고는 기존 R3.1 palette 유지에 근거한다. native radio/details 경계와 forced-colors border는 조작·접근성 구분용이다. S31 예시는 data-ui로 표시한 실제 인터랙티브 HTML fragment이며 사진을 늘려 검사 수를 채우지 않는다.

Impeccable detect의 dark section padding 경고는 내부 `.frame`의 실제 20–80px 여백과 section의 60–116px 위아래 여백으로 검토한다. 기존 크림 palette 경고는 브랜드 계승 사유로 남긴다. 이것을 접근성 PASS와 혼동하지 않는다.

## QA 결과

로컬 Chrome 최종 검수: **112 PASS / 0 FAIL**. 영상 실제 재생 별도 검수: **4 PASS / 0 FAIL**. 320/390/768/1440 각각 가로 넘침, 첫 화면 서비스 CTA, H1/main/ARIA 참조, 포스터·폰트, 외부 요청 없음, 기본 및 확장 상태 axe WCAG A/AA, 세 가설, 두 배치, GSAP 예시·닫기, details, 길이 선택·reset, 내부 경로·fragment를 확인했다. 같은 네 폭에서 JS-off 본문·native control·넘침·불필요한 모션 버튼 제거를 확인했다. 동작 줄이기 초기/실시간 변경, 키보드 skip/radio/details/정적 번호, 200% CSS zoom, GSAP 실패, 영상 실패, uncaught error도 검사했다.

영상은 실제 디코딩·클릭 재생·멈춤 후 포스터·장면 이탈 정지·reduced-motion 실시간 전환을 확인했다. production 14개 경로, branch-deploy 14개 경로, 기존 deploy-preview 15개 경로의 원래 release check도 통과했다. 새 preview allowlist 5개 파일과 링크 검증을 추가 통과했다.

초기 자동 검수에서 발견한 대비 부족은 accent `#70552d`로 수정했다. 최초 lazy image 미로딩 판정은 두 번째 이미지가 화면 밖이었기 때문에, 실제 스크롤·decode 후 재확인하도록 테스트를 수정했다. 로컬 서버 루트 링크 오류, 200% 확대 시 이메일 줄바꿈, crop 캡처에 나타난 offscreen skip-link도 수정했다.

Taste lint: 0 FAIL / 2 WARN (forced-colors 경계). 최종 inspect: 기록된 `still-page,palette-cream,eyebrow` 예외로 0 FAIL / 3 WARN. eyebrow 예외는 앞 예시의 figcaption을 다음 제목 위 kicker로 오인한 항목이며 실제 eyebrow를 추가한 것이 아니다. 나머지 경고는 OS 글꼴 선언, fluid 크기 개수, 한국어 질문형 제목의 역할 판단이다. 첫 화면의 실제 서비스 설명과 CTA는 별도 위치 검사를 통과했고 직접 화면을 검토했다.

실행 아티팩트: `evidence/r35/qa-results.json`, 접근성 트리 `.txt`, PC/모바일 `.png`. CI는 같은 스크립트를 실제 `dist` 출력에 실행해 정확한 HEAD와 캡처를 artifact로 남긴다.

미실행 범위: 물리 iOS/Android 기기, 실제 스크린리더 사용자의 낭독·이해, 브라우저 자체 확대, 고객 이해/전환 테스트, 실사용 Core Web Vitals. Playwright WebKit과 CSS zoom은 실기기 Safari/브라우저 자체 확대와 다르다.

## 변경 파일

- `experiments/sense-r35/index.html` — 세 장면과 검색·보조기술이 읽을 본문.
- `experiments/sense-r35/styles.css` — 독립 토큰·반응형·상태·모션 감소·forced-colors.
- `experiments/sense-r35/app.js` — 영상 제어·가설 알림·제한된 GSAP·reset 알림.
- `experiments/sense-r35/fonts/gowun-batang.woff2`, `fonts/OFL.txt` — 기존 브랜드 서체의 로컬 subset과 라이선스.
- `experiments/sense-r35/README.md`, `PRODUCT.md` — 실행·제품 범위.
- `scripts/prepare_r35_preview.py` — Preview 전용 5파일 allowlist와 링크 검사.
- `netlify.toml` — deploy-preview 명령에 전용 패키저만 추가.
- `qa/r35/browser.mjs`, `media.mjs`, `references.mjs`, `capture-zoom.mjs`, `serve.mjs`, `fetch-font.mjs`, `package.json`, `package-lock.json` — 재현 가능한 QA·캡처·서버·폰트 생성.
- `.github/workflows/r35-sense-experience.yml` — 정확한 PR HEAD에서 패키징·Chromium/WebKit·artifact.
- `.gitignore` — QA dependencies, generated evidence, skill working files 제외.
- `docs/R35_SENSE_EXPERIENCE.md` — 비교·Decision Log·QA·파일 목록.

운영 원본 및 PR #18의 변경 파일 수는 0. 루트 DESIGN.md도 변경하지 않는다.

## 인계와 독립 검토

- [Draft PR #19](https://github.com/HotCharliepepper/Mashcore/pull/19) — `codex/r35-sense-experience-20261103`, main 기반 독립 브랜치. 병합하지 않는다.
- [Netlify Deploy Preview](https://deploy-preview-19--mashcore.netlify.app/sense-r35/) — HTTP 200, noindex 헤더와 세 장면, `r35-commit` 메타를 직접 확인했다. 최종 HEAD와 CI 링크는 PR 본문에 기록한다.
- Chromium 112 / WebKit 390px 37 항목으로 구성된 CI가 실제 dist 출력에서 실행된다. 최초 실행 [#41621534954](https://github.com/HotCharliepepper/Mashcore/actions/runs/41621534954)은 총 149 PASS / 0 FAIL. 아이콘·캡처 보완 후 최종 HEAD 재실행 결과는 PR에 갱신한다.
- Impeccable 독립 전체 검토에서 나온 문자 아이콘 지적 1건을 공통 SVG stroke 아이콘으로 수정했다. 최종 verdict pass는 그 1건을 **resolved / ship**으로 판단했다. 다른 범위의 추가 인증을 주장하지 않는다.
- 확대 full-page PNG의 브라우저 타일 중복은 11개의 390×2000 연속 viewport 캡처로 교체했다. 최종 타일에 전체 푸터가 존재하며 독립 검토에서 모두 유효함을 확인했다. CI에는 확대 첫 viewport 캡처를 남긴다.
- 로컬 캡처: `evidence/r35/fold-1440.png`, `fold-390.png`, `desktop-1440.png`, `desktop-390.png`, `before-main-r31-{1440,390}.png`, `before-pr18-r34-{1440,390}.png` 및 네 폭의 선택/확장·JS-off 화면. 비교 화면은 고정 SHA의 별도 사본에서 촬영했다.
- 운영 Netlify 배포는 시작/재확인 모두 `6ae1f7c19ddb6a779b397b20`. main 및 PR #18 SHA도 최종 인계 전에 다시 확인한다.

## Design-system verification

구현 후 documenter 검수는 새 시각 체계 확정이 아니라 기존 MASHCORE 안의 세 장면 확장 여부를 확인했다. 기준은 현재 `index.html`, `assets/r31/styles.css`와 실험의 `index.html`, `styles.css`, `app.js`이며, 제품 범위는 실험 폴더의 `PRODUCT.md`를 따른다.

- **계승한 색·장면:** forest/ink `#18241c`, paper `#f4efe6`, 고운바탕 400, MASHCORE 워드마크와 문 앞의 동일한 WebP/MP4 장면을 이어 쓴다. 종이색·숲색 면의 교대와 같은 장면을 다시 보는 구성은 기존 코드에서 확인된다.
- **실험 안의 색·문자:** accent `#70552d`는 보조 링크·라벨·포커스, wash `#e7e4d9`는 조작 예시 배경, soft `#c5cbbd`는 어두운 면의 보조 문장에 사용한다. 본문은 OS 한국어 sans `16px/1.8`, 보조 문자는 주로 `13px`; 고운바탕 제목은 데스크톱 H1 `clamp(52px,5.8vw,86px)/1.28`, H2 `clamp(34px,4.3vw,62px)/1.4`이다. 모바일 H1은 최종 덮어쓰기인 `clamp(24px,14cqi,65px)/1.3`을 따른다. 로컬 폰트 subset과 이 크기 체계는 실험의 구현 선택이다.
- **배치·형태:** 최대 폭 `1600px`, 좌우 여백 `clamp(20px,5vw,80px)`와 비대칭 열을 사용한다. `1050px`에서 열 비율을 조정하고 `700px` 이하에서 세로로 쌓으며 여백은 `24px`, `360px` 이하에서는 `20px`이다. 면은 그림자 없이 색 대비로 구분하고 버튼·예시 판은 직각이다. 읽기 순서 숫자의 원형은 해당 예시에만 쓰인다.
- **실제 구성요소:** 숲색/종이색 반전 CTA, 밑줄 텍스트 링크, 직접 재생 버튼, 세 가설 native radio, 배치·길이 radio, native details, reset이 존재한다. CTA의 기본 최소 높이는 `54px`; 링크·보조 버튼의 주요 조작 영역은 `44px`이다. 포커스는 `3px` outline과 `5px` offset, 밝은 면에서는 accent, 어두운 면에서는 paper를 사용한다. 최종 방향·펼침·되돌림 아이콘은 동일한 authored SVG stroke 세트(`18px`, `1.5`, round cap/join)이며 이 실험의 통일 규칙이다.
- **동작 범위:** 자동 진입 연출은 없고 영상은 직접 요청한다. 읽기 순서 예시만 포인터 요청 시 GSAP opacity를 사용하며 키보드·동작 줄이기에서는 정적 번호를 보여 준다. 이 세 장면의 동작 선택을 전사 모션 규칙으로 확장하지 않는다.

화면 근거는 `evidence/r35/fold-{320,390,768,1440}.png`와 `desktop-{320,390,768,1440}.png`이다. 이번 문서 검수에서는 320/1440 첫 화면을 직접 대조했고, 네 폭의 동작·접근성 검수 범위와 한계는 위 QA 결과를 참조한다. 확인 결과 기존 색·서체·장면의 연속성을 유지하는 독립 실험이며 새 브랜드 세계나 전사 디자인 시스템 교체로 기록하지 않는다.

기존 루트 `DESIGN.md`의 이전 색 토큰·영상 설명·연락처와 현재 코드 사이의 드리프트는 이번 범위에서 수정하거나 새 규칙으로 정당화하지 않았다. 루트 `DESIGN.md`를 그대로 보존하고 `.impeccable/design.json`도 생성·갱신하지 않았다. 실험 전용 배치·크기·아이콘 선택과 미사용 CSS 변수는 전사 토큰으로 승격하지 않는다.
