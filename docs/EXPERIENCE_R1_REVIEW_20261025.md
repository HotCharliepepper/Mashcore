# Mashcore Experience R1 — 화면 검토 기록

2026-10-25. 기존 사이트 생성기와 런타임을 이어 만든 조작 가능한 검토본이다. main 병합·운영 배포는 하지 않았다. 사용자 화면 피드백을 받아 이 PR에서 계속 수정한다.

## 작업 기준과 검토 위치

- 저장소: `HotCharliepepper/Mashcore`
- 열린 후속 작업을 재조회한 결과: Draft PR #6과 #2. #6 이후의 열린 후속 PR 없음.
- 유지한 원격 브랜치: `review/mashcore-renewal-20261023`, PR #6 Draft.
- 변경 전 PR #6: `a3c81d821f4bcbe542bb0aee332a1803fd8ae8a4`
- main: `b31a55cea32cd83113624f9cdc27bd8d8bc36926` (변경 없음)
- PR #2: `9e857fdca62b66bd7d81ecc3492940124a02c08a` (변경 없음)
- R1 구현 커밋: `2585b11b5d59c1b6ef43d49b9b55523242e5f365`
- 구현 tree: `866df09736fe6025778479f4d3bed44101298430`. 로컬 검수 tree와 GitHub tree가 일치한다.
- 구현 커밋 대응 배포: `6ade057424cd7fdda7398c2e`, `ready`, `deploy-preview`, `published_at: null`.
- 고정 배포: https://6ade057424cd7fdda7398c2e--mashcore.netlify.app/
- PR 검토: https://github.com/HotCharliepepper/Mashcore/pull/6
- 화면 비교: https://deploy-preview-6--mashcore.netlify.app/preview/?view=desktop&page=%2F

로컬 Git HTTPS push에는 자격증명이 없어 GitHub 연결의 tree/commit/ref API를 사용했다. 기존 HEAD를 부모로 유지하고 `force:false` 및 예상 HEAD 검사를 적용했다. 로컬 임시 커밋 `cad2ee6`과 원격 구현 커밋은 같은 tree이며, 위 원격 SHA가 정식 검토 기준이다. 이 문서와 검수 증거를 추가하는 후속 커밋은 사이트 구현을 변경하지 않는다. 최종 PR HEAD/배포는 PR 본문에 별도로 기록한다.

## 구현한 경험

| 위치 | 실제 변경 | 보존한 내용 |
|---|---|---|
| 홈 첫 화면 | 사람과 문 앞의 장면, v0.2 H1·역할·설명, 즉시 로드하는 picture, 얇은 가로선·↓, 서비스 직접 탐색 | 기존 문 앞 인물 모티프, 장면 ID·문의 진입 |
| 관찰 | 짧은 도입, 상세 질문은 native details, 가설/실측 구분은 항상 표시 | 3관점 A/B 원문·동일 노드·상태·정지 비교 대안 |
| 현장과 작업 | 질문→기여→선택 이유, Weplace 상세로 연결 | 독립 실행 브랜드 관계, 재구성 표시, 실제 성과 미검증 상태 |
| 서비스 | v0.2 제목·설명, 상황별 앵커, 여섯 업무 축·남기는 결과·FAQ | 두 가격 트랙·금액·PROPOSED·VAT 미정·상품별 문의 |
| 소개 | 함께 하여 강화한다, 경험·설계·분석 역할을 설명하는 문단 | 기존 세 역할, 이름·고용관계·경력의 사실 경계 |
| 연구·협업 상세 | 짧은 도입과 한국어 제목, 근거·선택에 도달하는 탐색 | 연구 본문·한계·날짜, 여섯 동시 관점/3D·목록·초기화 |
| 문의·하단 | v0.2 안내 문안, 자동 접수/저장하지 않는 동작의 명시 | 기존 mailto·수동 복사·1,001자 보존, 사업자·정책 |

SSOT는 `content/strategy.json`, `content/hero-media.json`, 기존 상품 JSON과 사업자 설정이다. `scripts/build_public.py → dist`가 실제 출력이다. 루트 legacy HTML을 결과물로 배포하지 않는다. 기존 `site.js`, `observations.js`, `chore-spatial.js`, `chapters.js`, `site-config.js`와 상품 JSON의 바이트가 기준 커밋과 같다.

## 임시 자산과 최종 자산

- 현재: 기존 `index.html`의 threshold-art SVG를 데스크톱/모바일 구도로 편집한 **composition study**. 화면에 `히어로 구도 시안 · 실제 촬영 아님` 표시.
- 포스터: 데스크톱 1,549 bytes, 모바일 1,339 bytes. 승인된 실제 현장 사진으로 주장하지 않는다. `rights_verified:false`, `public_use_approved:false`.
- 최종 영상: 미제공. 두 video 경로는 `null`; 실제 출력에는 video 요소·빈 src·재생 버튼이 생성되지 않으며 포스터와 모든 탐색이 바로 표시된다.
- 준비된 영상 연결: 로컬 경로가 있을 때만 로드. 실제 `playing` 이후 opacity 전환, 수동 재생/정지·종료/다시 보기·환경 정지·오류·reduced-motion 처리. 사용자 정지와 종료 상태는 스크롤/탭 복귀로 자동 초기화하지 않는다.
- 별도 TEST FIXTURE: 로컬 QA만 사용하는 2.5초 색상 패턴 WebM. 브랜드 영상·현장 증거가 아니며 `dist`와 원격 배포에 포함되지 않는다.

## 실제 검수

환경: Linux의 Python/Node, 격리 설치한 `linkedom@0.18.12`, Cloud Chromium. 실물 모바일 기기 아님. 브라우저는 생성된 dist를 실제 iframe에서 렌더링했다. 테스트 코드와 증거는 공개 dist 밖에 둔다.

```sh
python scripts/build_public.py --context deploy-preview
python scripts/check_public.py
python scripts/check_r1.py
NODE_PATH=/workspace/scratch/f924b8ad2b7d/qa-deps/node_modules node scripts/check_review_interactions.cjs
NODE_PATH=/workspace/scratch/f924b8ad2b7d/qa-deps/node_modules node scripts/check_spatial.cjs
node --check assets/js/hero-media.js
python scripts/prepare_r1_qa.py
# 관리형 로컬 preview에서 /qa/browser.html의 두 검사 버튼 실행
python qa/r1/check_preview.py --url https://deploy-preview-6--mashcore.netlify.app --deploy-id 6ade057424cd7fdda7398c2e
```

| 검사 | 실제 결과 | 증거/제한 |
|---|---|---|
| 정적 출력·로컬 링크·사업자·가격 | PASS: 12 HTML, 11 푸터, 362 참조 | `qa/r1/static-public.json`; 미승인 production은 예상대로 차단 |
| R1 SSOT·포스터·기존 런타임 보존 | PASS | `qa/r1/static-r1.json` |
| 문의/A·B 런타임 | PASS: 9 묶음 | `qa/r1/interactions.json`; Node VM |
| 3D 선택·권한·대안·정리 | PASS: 9 묶음 | `qa/r1/spatial.json`; linkedom, 실물 센서 아님 |
| 11경로 × 320/390/768/1440 | PASS: 44 | `qa/r1/browser-layout.json`; 실제 Chromium 가로 넘침 검사 |
| 390px 글자 200% | PASS: 11 | CSS 텍스트 확대. 브라우저 자체 zoom과 다름 |
| JS 비활성 홈·서비스·Chore to Play | PASS: 3 | 실제 sandbox 스크립트 차단; 정지 정보/연락처 유지 |
| 미디어·문의·A/B 브라우저 검사 | PASS: 21 | `qa/r1/browser-media.json`; 영상 재생은 실제 WebM, 거부·선호·visibility는 명시 주입 |
| 키보드 메뉴·A/B | PASS: 직접 Enter/Escape/Space | 메뉴 닫힘·트리거 초점 복귀, B 선택 확인 |
| ↓·서비스 상황 앵커 | PASS: 직접 조작 | 도착 제목 top 292px, axis-2 top 224px로 고정 헤더 아래 표시 |
| Field→협업 상세→하는 일 | PASS: 직접 조작 | 목적지 H1과 화면 확인 |
| 문의 복사 실패 | PASS: 직접 조작 | HTTP 환경의 복사 불가 시 원문 선택·직접 복사 안내. mailto 수신자/내용 인코딩 확인 |
| 원격 HTTP/산출물 | PASS: 24 | 12 HTML + 7 자산 HTTP 200, 내부 경로 5개 404. 정확한 Netlify toolbar 한 블록만 제외하면 local dist와 동일 |
| 원격 실제 화면 | PASS: 홈·↓·A/B B·서비스 | `remote-desktop.jpg`, `services-desktop.jpg`. 원격 전체 58개 행렬을 다시 실행했다는 뜻은 아님 |

검수 중 수정: 768px에서 제목과 장면이 가까워지는 구성을 900px 이하 세로 배치로 조정했다. 영상 종료 후 seek 과정에서 readyState가 낮아지면 수동 재생 요청이 사라지는 결함을 발견해 준비 완료까지 요청을 보존했다. 이전 play promise가 새 요청을 정지시키지 않도록 세대 검사를 보완했다. 최종 연속 검사에서 재재생·사용자 정지 유지·환경 복귀·404를 모두 통과했다.

## 캡처 안내

[MASHCORE_R1_SCREENSHOTS_20261025.zip](https://chatgpt.com/library?file_id=libfile_80b476cd86b88191ae8033d966581340&account_id=personal)에 원본 JPEG 13장과 `SCREENSHOTS.json`을 제출한다. 각 이미지의 SHA-256, 원본 픽셀, 실제 사이트 iframe 폭/높이, 소스 커밋, 상태와 환경을 함께 기록했다. ZIP은 별도 제출 첨부이며 공개 사이트에 포함하지 않는다.

| 파일 | 검토 장면 | 사이트 viewport / ref |
|---|---|---|
| before-desktop.jpg / after-desktop.jpg | 첫 화면 전후 | 1440×960 / 기준 a3c81d8 → 구현 2585b11 |
| before-mobile.jpg / after-mobile.jpg | 첫 화면 전후 | 390×844 / 기준 a3c81d8 → 구현 2585b11 |
| after-tablet.jpg | 태블릿 간격 수정 | 768×960 / 구현 |
| research-a.jpg / research-b.jpg | 동일 정보의 배치 A→B | 390×844 / 구현 |
| services-desktop.jpg | 상황별 서비스 진입 | 1440×960 / 구현 원격 |
| field-desktop.jpg / work-desktop.jpg | 현장 작업→협업 상세 | 1440×960 / 구현 |
| inquiry-fallback-mobile.jpg | 문의 원문 선택·복사 실패 안내 | 390×844 / 구현 |
| reduced-motion-mobile.jpg | 정지 포스터·탐색 | 390×844 / 선호 설정 주입, OS 설정 아님 |
| remote-desktop.jpg | 새 Netlify 배포의 실제 화면 | 1440×960 / 구현 원격 |

외부 preview shell은 실제 iframe 폭을 표시하며 1440px를 화면에 맞춰 축소한다. 변경 전 데스크톱 캡처의 외부 이미지 크기는 1363×936, 나머지는 1348×926이다. 사이트 iframe은 전후 같은 1440×960/390×844를 사용했다. 전체 문서 스크롤 캡처가 아닌 선택한 장면의 viewport 캡처다.

## 남은 검수·결정

- NOT RUN: 최종 실제 사진·영상의 권리·인물 동의·장면 적합성·최종 인코딩/디코딩·느린 실제 네트워크. 현재 포스터 대안은 동작한다.
- TEST FIXTURE PASS, 최종 자산 NOT RUN: 영상 정상/거부/404/종료/재재생, 모션 감소·visibility. OS 자체 reduced-motion, 물리적 배경 탭 전환, save-data 기기 설정은 별도 실기기 검수 필요.
- NOT RUN: 실제 iPhone/Android·센서·스크린리더·브라우저 자체 200% zoom·외부 메일 앱/SMTP. 가상 IME 이벤트 검사는 실제 한글 키보드 입력 사용성 검사를 대체하지 않는다.
- NOT RUN: Lighthouse/Core Web Vitals, 실사용 성능·사용자 5초/10초 이해도·전환율. 자산 파일 크기와 화면 검수만 보고한다.
- 검토 필요: 최종 문안·CI·가격 트랙 선택·VAT·기간/범위·공개 승인. 이번 구현은 승인을 대신하지 않는다.
- noindex는 유지했으며 접근 제어를 뜻하지 않는다. 운영 배포 차단을 해제하지 않았다.

## 피드백과 Weplace 영향

| ID | 위치·환경 | 사용자 표현 | 원인 가설 | 수정안 | 상태·근거 | 재검수 |
|---|---|---|---|---|---|---|
| F01 | 작성 대기 | — | — | — | 사용자 피드백 미수신 | NOT RUN |

피드백은 `화면 / 데스크톱·모바일 / 첫 느낌 / 유지할 것 / 걸리는 부분`으로 받는다. P0 사실·문의·공개범위·동작, P1 이해·가독성, P2 정서·리듬 순으로 수정한다.

Weplace 독립 사이트·문의 경로·운영 데이터에는 변경이 없다. Mashcore 안의 협업 설명과 자료 순서만 정리했다. Weplace에는 화면의 질문→기여→근거 순서를 참고할 수 있으나 최종 자산·가격·CI나 성과를 자동 이관하지 않는다.
