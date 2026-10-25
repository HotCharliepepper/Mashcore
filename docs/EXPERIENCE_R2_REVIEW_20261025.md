# Mashcore Experience R2 — 구현·화면 검수 결과

기존 사이트와 Draft PR #6에 R2를 이어 구현했습니다. 실제 홈·상세페이지·A/B·문의·3D를 탐색하는 검토본입니다. R1 코드·기록·캡처와 PR #2를 보존했으며 main 병합·운영 배포·GBP 변경은 하지 않았습니다.

## 정확한 검토 위치

| 구분 | 값 |
|---|---|
| 이어 작업한 원격 브랜치 | `review/mashcore-renewal-20261023` |
| Draft PR | https://github.com/HotCharliepepper/Mashcore/pull/6 |
| R1 기준 HEAD | `4cd7504878f3118e876beb179f490a141a0e5b61` |
| R2 본 구현 | `f2d51d8d3701fc7d8245e4b1603211c98b78d020` |
| R2 최종 화면 코드 | `d5179086661cdd7b1c08e0231f11a6e216cc185f` — 문의 FAQ 소제목 대비 보정 포함 |
| 코드에 대응하는 고정 배포 | `6ade289eeba0b597dafdfbb5` — ready / deploy-preview / published_at null |
| 고정 사이트 | https://6ade289eeba0b597dafdfbb5--mashcore.netlify.app/ |
| PC·모바일 화면 비교 | https://6ade289eeba0b597dafdfbb5--mashcore.netlify.app/preview/?view=desktop&page=%2F |
| 계속 수정되는 PR Preview | https://deploy-preview-6--mashcore.netlify.app/ |

최종 증거 커밋의 HEAD는 PR 본문에 별도로 기록합니다. 이 문서·원격 검수·캡처 링크 추가는 위 화면 코드를 바꾸지 않습니다. Git 연결의 tree/commit/ref API로 부모를 유지했고 `expected_sha`와 `force:false`로 갱신했습니다. 이전 로컬 체크포인트도 삭제하지 않았습니다.

## 화면에서 달라진 것

| 위치 | 구현과 이유 | 적용 원본 |
|---|---|---|
| 첫 화면 | 가상의 인물이 문 앞 안내를 살피는 AI 콘셉트. 포스터를 즉시 표시하고 6.5초 무음 모션 시안이 준비되면 전환. 실제 업무 한 문장과 서비스 CTA를 첫 화면에 배치 | `scripts/review_r2.py`, `content/strategy.json`, `content/hero-media.json`, `assets/media/hero-*` |
| PC·모바일 | PC는 왼쪽 문안·오른쪽 인물. 320/390은 이미지와 문안을 분리하고 H1 두 줄·48px CTA. 768은 세로 이미지가 머리·손을 자르지 않도록 가로 자산 사용 | `assets/css/experience-r2.css`, `assets/js/hero-media.js` |
| 홈 흐름 | 관심 → 세 상황 질문 → 기존 A/B → 판단 방식 → Weplace 작업 → 결과물 한 장 → 업무 범위·과정 → FAQ·문의 | `scripts/review_r2.py`, `scripts/build_public.py` |
| 깊은 설명 | 기존 여섯 서비스축·두 가격안·소개·연구·협업 상세로 실제 링크. 서비스 결과물 예시를 읽을 수 있는 한 장으로 보강 | `scripts/review_details.py`, `/services/`, `/about/`, `/research/`, `/work/weplace/` |
| 자산 경계 | AI 콘셉트, 정지 이미지 모션, 결과물 예시·Weplace 재구성을 화면에서 구분. 실제 증거로 오인될 자료 제목을 수정 | `content/assets-r2.json`, `work/weplace/index.html` |
| 미디어 상태 | 포스터 우선, 실제 playing 후 표시, 사용자 정지·종료 존중, 회전 시 자산 교체, 모션 감소·save-data·실패 대안 | `assets/js/hero-media.js` |
| 안정성 | 모바일 메뉴 초기화의 큰 화면 이동 제거. site.js 실패 시 펼쳐진 메뉴 대안 복원. 영상 조작 영역의 자리 확보 | `scripts/build_public.py`, `assets/css/experience-r2.css` |
| 검색 정보 | 페이지별 title/description/canonical/OG, 홈·소개 Organization과 본문 일치. LocalBusiness·미확인 전화/시간/평점/Offer 없음 | `content/seo.json`, `scripts/review_seo.py` |
| 검토 도구 | 기존 화면 비교에 ‘페이지 전체’ 추가. 내부 QA·소스는 dist에서 제외, 미디어 바이트 검증 | `assets/js/preview.js`, `scripts/media_assets.py`, `qa/r2/` |

PC H1은 “그 사람은, / 왜 잠시 멈췄을까요?”, 모바일 H1은 “왜 잠시 / 멈췄을까요?”입니다. 역할 문장은 “현장과 고객을 살펴, 사업의 방향과 브랜드의 말, 홈페이지와 상담의 흐름을 설계합니다.”입니다. 주 CTA는 PC “함께할 수 있는 일 보기 ↗”, 모바일 “함께할 일 보기 ↗”이며 모두 실제 `/services/`로 이동합니다. 얇은 가로선과 ↓는 기존 `#research`에 연결됩니다.

## 실제 검수

| 환경·범위 | 결과 | 증거 |
|---|---|---|
| Python 정적 검사 | 12 HTML / 11 사업자 footer / 390 로컬 참조 PASS. 가격 승인·정책·문의·A/B 원문·연구·noindex·production 차단 보존 | `docs/qa/r2/static.json`, `r2-static.json` |
| Node VM·linkedom | 문의/A·B 9개 묶음 + 3D 9개 묶음 PASS | `interactions-node.json`, `spatial-node.json` |
| 실제 Chrome 렌더 | 11경로×320/390/768/1440 44개 + 글자 200% 11개 + JS 차단 3개 = **58/58 PASS** | `browser-layout.json` |
| 실제 Chrome 기능·미디어 | **31/31 PASS**. 실제 PC·모바일 6.5초 영상, 거절 후 재생, 일시정지·종료·재재생, 404, 모션 감소, save-data, 화면 회전 후 정지·종료 보존, site.js 404 메뉴 대안 | `browser-interactions.json` |
| 키보드 수동 검수 | 서비스 앵커, 메뉴 Enter·Escape·초점 복귀, 소개 이동, 여섯 관점 Space 선택, 문의 URI, FAQ 펼침 확인 | `manual-ui.json` |
| 실제 원격 Preview | HTML·자산 26개 HTTP 200 및 로컬 출력 일치, 내부 8경로 404. noindex 확인. 원격 홈·영상·↓·A/B Space·서비스 CTA 직접 조작 | `remote-http.json`, `deploy.json`, 원격 캡처 |
| 문안·크롭 | 320/390 제목 두 줄, 인물 시선·손과 문안 분리. 주 CTA 하단 위치 약 595/679px, 높이 48px | 기능 로그 first viewport, 변경 전후 캡처 |
| 대비 보정 | 문의 FAQ 본문 10.89:1, 소제목 9.17:1 | `faq-contrast.json`, 최종 FAQ 화면 |

58/31 전체 브라우저 검사는 본 구현 커밋의 기능·구조에서 실행했습니다. 이후 최종 코드 변경은 FAQ 소제목 색상 한 선언이며 정적 검사와 해당 대비를 다시 확인했습니다. 미디어·문의·3D·레이아웃 구조는 같고, 최종 배포의 모든 대상 파일은 새 dist와 다시 대조했습니다. 두 검수 시점은 캡처 manifest에서 구분합니다.

모션 선호·save-data·visibility·자동재생 거절·복사 거절은 테스트 페이지의 명시적 주입입니다. 영상 오류와 스크립트 오류는 실제 404로, 일반 재생은 실제 미디어로 확인했습니다. 테스트용 색상 막대와 배포된 콘셉트 영상은 구분합니다. 가로 넘침은 OS 스크롤바를 뺀 실제 clientWidth와 대조했습니다.

로컬 실탐색 PerformanceObserver 표본은 PC LCP **728ms / 관찰한 layout-shift 합계 0**, 모바일 **388ms / 0**입니다. 네트워크·CPU 제한 없이 캐시 영향을 받는 검토 환경의 단일 표본입니다. 처음 모바일에서 관찰한 0.108의 이동은 메뉴 초기화 보정 후 해소됐습니다. 이 수치는 운영 Core Web Vitals나 전환 성과가 아니며 **INP·CrUX·느린 네트워크·실기기 측정은 NOT RUN**입니다. 파일 크기는 포스터 PC 146,030B / 모바일 97,192B, 영상 PC 362,892B / 모바일 196,263B, OG 26,586B입니다.

실제 방문자의 5초 이해도 응답, 브라우저 자체 200% zoom, 스크린리더, 실제 터치 기기·센서·OS 모션 설정, 메일 앱·발송·수신, Google Rich Results Test·Search Console·GBP 관리자 화면은 NOT RUN입니다. 수행한 글자 확대·DOM/키보드·스키마 파싱과 구분합니다.

## GEO·GBP와 자산

[정보 대조표](R2_GEO_GBP_20261025.md)에 사업 정보·검색 의도·키워드 후보·URL·구조화 데이터와 미확인 항목을 기록했습니다. GBP 기존 프로필·등록 자격·관리 권한·공개 전화·영업시간은 NEED_VERIFY입니다. 프로필 생성·수정, 상호 키워드 삽입, 허구의 운영정보 입력은 하지 않았습니다.

[자산 목록](R2_ASSETS_20261025.md)과 `content/assets-r2.json`은 실제/AI/재구성을 구분합니다. 현재 영상은 **AI 정지 이미지의 느린 확대 시안**입니다. 실제 현장 원본, 실제 Weplace 화면·성과 자료, 공개 허락, 최종 인물·영상·문안·CI 선택은 남아 있습니다. seed.ai 인물·제일기획 작품·이상한마케팅 성과를 복제하지 않았습니다.

## 보존 및 남은 판단

사업자 설정, 기존 site.js/observations.js/chapters.js/chore-spatial.js, 두 가격안 원본, 정책은 R1과 바이트가 같습니다. 문의는 mailto·복사만 제공하며 자동 접수·저장·결제 기능을 만들지 않았습니다. origin/research/field/invitation과 여섯 동시 관점·정적 읽기·3D 센서 선택권을 보존했습니다. Weplace 독립 사이트·DB·DNS는 변경하지 않았습니다.

종료 확인에서 열린 항목은 Draft PR #2·#6이며 별도 열린 issue는 없었습니다. PR #2 HEAD는 `9e857fdca62b66bd7d81ecc3492940124a02c08a`, main은 `b31a55cea32cd83113624f9cdc27bd8d8bc36926`, 운영 deploy는 `6adb113e296767181eb98f02`입니다. 화면·자산·가격·GBP·main 병합·운영 배포 승인을 이번 구현으로 대체하지 않습니다.

다음 검토는 첫 인물 장면과 PC/모바일 문안, 결과물 예시의 밀도, 공개 가능한 실제 작업 자료의 선택입니다. 이 Draft와 고정 Preview를 기준으로 수정할 수 있습니다.

## 변경 전후 캡처

[원본 캡처 32장과 manifest ZIP](https://chatgpt.com/library?file_id=libfile_cd72eef427f08191ad10ba9a74384202&account_id=personal). R1 320·390·768·1440, R2 첫 화면·전체 홈·서비스·소개·연구·협업·문의와 원격 조작 화면을 포함합니다.

`before-*`는 R1 기준, `after-*`는 구현 중 로컬 작업 화면, `remote-*`는 f2d51d8 고정 배포, `final-*`는 d517908 고정 배포입니다. 개별 트리를 커밋하지 않은 로컬 중간 캡처에는 확정 커밋을 가장하지 않고 대응 구현만 표시했습니다. 최종 판단에는 `final-home-full-1440.jpg`, `final-home-full-390.jpg`, `final-home-390-frame.jpg`, `final-faq-open-390.jpg`를 사용해 주세요. manifest에는 실제 CSS 폭·이미지 크기·출처·시각·해시가 있습니다.
