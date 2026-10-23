# Mashcore 리뉴얼 — 구현 검토 기록

2026-10-23 설계 기준 · 상태: 검토용 구현 / 신규 문안·배치·모션 PROPOSED

홈 네 장면에서 서비스·연구·소개·Weplace 협업 상세·독립 문의까지 실제로 탐색하는 검토본을 만들었다. 문서 보드를 홈페이지로 복사하지 않고, 08의 화면 순서와 콘텐츠를 기존 PR 생성기에 적용했다. 새 CI·가격 확정·main 병합·운영 공개의 완료 기록이 아니다.

## 1. 검토 위치와 실제 구현 범위

| 위치 | 상태·용도 |
|---|---|
| 격리된 작업 사본 | `/workspace/scratch/4af8868c2e72/mashcore-review` |
| 최종 화면 대상 | 위 작업 사본의 `dist/`; 루트 입력 HTML과 구분 |
| 내부 브라우저 QA | `http://terminal.local:4173/`에서 생성된 결과 검사. 사용자에게 제공하는 외부 호스팅 주소가 아님 |
| 새 Draft PR | [Draft PR #6](https://github.com/HotCharliepepper/Mashcore/pull/6), open / Draft / unmerged; 현재 main과 병합 충돌 없음 |
| 이번 검토 Preview | [검토 홈](https://deploy-preview-6--mashcore.netlify.app/) · [화면 비교](https://deploy-preview-6--mashcore.netlify.app/preview/); 기존 Netlify mashcore의 deploy-preview, 12개 경로 HTTP 200 확인 |
| 실제 화면 캡처 | `docs/screenshots/`의 실제 Chromium 캡처 4장; 이번 dist에서 촬영 |

구현 범위는 홈·모바일·서비스·소개·연구 허브·Chore to Play·Market Interpretation·연구 로그·Explore·Weplace 협업·환불·화면 비교의 12개 HTML 경로다. 모든 검토 페이지에 noindex를 유지하고, 내부 명세·content·scripts·docs·qa·Git 데이터는 배포 산출물에서 제외한다. noindex는 접근 제어가 아니다.

## 2. 실제 ref와 보존·통합

| 대상 | 기준 문서의 고정 기록 | 착수 시 실제 확인 | 이후 차이 |
|---|---|---|---|
| main | `b31a55cea32cd83113624f9cdc27bd8d8bc36926` | 동일 HEAD | 없음 |
| PR #2 | `9e857fdca62b66bd7d81ecc3492940124a02c08a` | 동일 HEAD, open / Draft / not merged | 없음 |
| PR #2 브랜치 | `feature/mashcore-weplace-portfolio-20261019` | 기존 작업 유지 | 닫기·reset·force push 없음 |
| 후속 작업 ref | — | `review/mashcore-renewal-20261023` | PR #2 HEAD에서 분기한 격리 작업 사본. 최신 main을 이 검토 브랜치 안으로 병합해 두 계보를 함께 보존(main 자체 변경 없음) |
| 후속 최종 커밋 | — | 화면 구현 커밋 `36516abcd7a3375d10645a3a7d547e299f5e3719`; 이후 기록 갱신 HEAD는 Draft PR #6에서 확인 | 운영 반영과 별개 |

일반 Git push는 셸 인증 부재로 실패했다. 연결된 GitHub 기능으로 로컬 검수본과 동일한 tree `c8617cbce7a705081245ebff7cf24c2eaf05acd2`를 등록하고 두 기준 SHA를 부모로 하는 커밋을 만들었다. 파일 tree 일치를 확인한 뒤 그 원격 ref를 현재 작업 사본으로 가져왔다. 원래 로컬 두 커밋은 `local/mashcore-renewal-20261023`에 보존했다. reset·force push·기존 PR 변경은 하지 않았다.

PR 메타데이터의 base SHA `45bba47…`는 현재 main SHA와 다르므로 main의 현재 상태로 사용하지 않았다. 두 기준 이후 신규 커밋은 없었지만, 서로 다른 계보 사이에 존재하던 운영 정보·생성 방식·화면 차이는 아래와 같이 통합했다.

| 항목 | 보존·통합 내용 |
|---|---|
| 철학·역할 | PR의 ‘함께 하여 강화한다’, 현장 경험·전략·브랜드·디지털 설계·프로젝트별 전문성 유지 |
| 홈 | origin/research/field/invitation 유지; 홈에는 PR 세 관점 A/B를 배치 |
| 연구 | 여섯 동시 관점·3D·가설 수정·원문·로그·직접 경로 유지. PR의 3D 소스는 main과 동일했으므로 불필요하게 다시 만들지 않음 |
| 협업 | PR의 Weplace 상세를 이어 질문·선택 이유·자료 상태·다음 연결 보강 |
| 사업자·문의 | main 최신 값을 strict JSON 설정에 이관; BASE/EMAIL·동작·mailto·canonical/OG·검사 기대값 일치 |
| 정책 | main 환불 원문과 스타일을 이관하고 실제 dist·서비스·공통 푸터에 포함 |
| 가격 | PR JSON 원문 그대로 + main 가격 카드 원문 별도 트랙. 판매 승인 플래그 변경 없음 |
| 생성 방식 | PR `build_public.py → dist`만 사용. 모바일은 같은 홈 원본에서 생성; 생성 결과 수동 수정 없음 |

## 3. 페이지별 보존·수정·추가·보류

| 실제 경로 | 처리 | 구현 내용·주 CTA | 주요 적용 파일 |
|---|---|---|---|
| `/` | 보존·수정 | 네 장면, 역할 구성 예시, 원문 A/B, Field 설명도, 독립 문의. Origin → `/services/`, Research → `/research/chore-to-play/`, Field → `/work/weplace/` | `scripts/review_home.py`, `scripts/build_public.py`, `content/strategy.json`, `assets/css/renewal.css` |
| `/mobile/` | 보존·수정 | 홈과 같은 내용·행동을 한 생성 경로로 출력 | `scripts/build_public.py` |
| `/services/` | 보존·수정·추가 | 여섯 설명 축·산출물 예시·과정·별도 가격 트랙·SOW·환불. 주 CTA → `/#invitation` | `scripts/review_details.py`, `content/services-main-review.html`, 기존 `content/services-prototype.json` |
| `/about/` | 보존·수정 | 규현의 역할·판단 방식·남기는 결과물·프로젝트별 협업·Lab/Weplace/Mashcore34. 주 CTA → `/services/` | `scripts/review_details.py` |
| `/research/` | 보존·수정·추가 | 기존 허브에 Lab/Market 편집 입구; 원문은 한 벌 유지. 주 CTA → Chore 상세 | `research/index.html`, `assets/css/research-review.css` |
| `/research/chore-to-play/` | 보존·수정 | 여섯 동시 관점·기존 3D·정지 목록·선택·초기화·키보드/버튼 대안, 원문·수정 이력 유지 | `research/chore-to-play/index.html`, `assets/js/chore-spatial.js`, `assets/css/chore-spatial.css` |
| `/research/market-interpretation/` | 보존·수정 | 첫 설명·자료 시점/시간축 안내·로그 연결; 기존 교육·연구 성격과 본문 보존 | `research/market-interpretation/index.html` |
| `/research/log/` | 보존·수정 | 첫 설명·연구 연결; 실제 원문 날짜와 수정 기록 보존 | `research/log/index.html` |
| `/explore/` | 보존·제한 수정 | 기존 주제·글·질문·anchor·탐색 유지; 연구 허브와 관계 설명 | `explore/index.html` |
| `/work/weplace/` | PR 보존·수정 | 질문→선택 이유→기여 범위→자료 상태→다음 연결. Weplace 공식 홈과 Mashcore 문의 구분 | `work/weplace/index.html` |
| `/policies/refund/` | main 보존·통합 | 정책 원문·메일 유지, 공통 정적 푸터. 새로운 환불률·기한 추가 없음 | `policies/refund/index.html`, `assets/css/commerce.css`, 생성기 |
| `/preview/` | 보존·수정 | desktop/mobile 비교와 실제 검토 경로; 공통 제품 메뉴에는 노출하지 않음 | `preview/index.html`, `assets/js/preview.js`, `assets/css/preview.css` |
| 분류별 새 URL·Else·새 노트·CI·영상·CMS | 보류 | 공개할 원문·자산·운영 필요가 준비된 뒤 별도 결정 | 이번에 생성하지 않음 |

공통 메뉴는 서비스 / 연구 / 생각 읽기 / 소개와 ‘내 상황 이야기하기’로 정리했다. 가격·사업자정보·정책·주 CTA는 애니메이션이나 펼침 완료를 기다리지 않는다. 로고/파비콘은 기존 웹 표현을 유지했다.

### 조작과 상태

- A/B: 손의 움직임 / 읽는 순서 / 결정의 조건의 원문·정보·A/B 설명을 보존했다. 선택 상태와 배치가 함께 바뀌며, JavaScript가 없거나 초기화되지 않으면 세 관점의 A와 B 대안을 정적으로 읽는다. 실제 반응·전환율 검증으로 소개하지 않는다.
- 문의: 원문을 자동으로 자르지 않는다. 카운터와 검증은 같은 문자 계산을 사용하고 한글 조합 중 내용을 바꾸지 않는다. 1,000자 초과 시 메일·자동 복사 행동을 제한하고, 원문·직접 선택·이메일을 남긴다.
- 빈 메일은 수신자·제목만, 빈 복사는 입력 안내를 제공한다. 메일 앱 열기·복사 결과·수동 복사 대안을 구분한다. 서버 접수·저장·CRM·전송·결제 완료 UI는 없다.
- 모바일 메뉴는 Escape로 닫고 열기 버튼으로 초점을 돌린다. 3D는 드래그·센서 외에 읽기 목록·선택·초기화·방향 버튼·키보드 대안을 제공한다.

관련 동작 파일: `assets/js/site.js`, `assets/js/observations.js`, `assets/js/chore-spatial.js`. 기존 condition-lab·Explore의 동작도 보존했다.

## 4. 자산의 종류·출처·공개 범위

| 자산 | 종류·출처 | 이번 처리·한계 |
|---|---|---|
| 기존 워드마크·파비콘 | PR 코드의 실제 웹 자산 | 유지. 새 승인 벡터 CI 또는 운영 로고 교체가 아님 |
| 세 관점 A/B | PR 루트 입력 HTML·observations.js의 설명용 가상 화면 | 원문 보존. 실제 고객 화면·실험 성과가 아님 |
| 여섯 관점·3D | 기존 연구 HTML/CSS/JS | 연구 모형과 정지 대안 보존. 사람의 등급·점수·성장 단계가 아님 |
| Origin 역할 구성 | 이번 HTML/CSS 구성 예시 | 역할을 연결하는 설명. 실적·인력 상시 배정의 증거가 아님 |
| 서비스 결과물 4칸 | 이번 설명용 구성 예시 | 질문/확인할 자료/선택한 방향/다음 실행. 완성된 고객 납품물로 표시하지 않음 |
| Weplace 4질문 구성 | 08의 설명용 재구성 | ‘정보 흐름을 요약한 구성’ 및 실제 운영 화면·성과가 아님을 인접 표시 |
| 로컬 웹폰트 | Gowun Batang 400, Noto Sans KR 400/600; WOFF2 변환·OFL 포함 | 동일 출처 로딩·fallback·font-display:swap. 출처·라이선스·해시·글리프 검증은 `docs/REVIEW_FONT_SOURCES.md` |
| 실제 인물·현장 사진·영상·성과 수치 | 이번에 새 확보·제작하지 않음 | 공개 원본·기여·사용 허락 확인 후 추가 가능 |

외부 폰트 CDN 의존을 없앴고, 첨부 검토 HTML의 불완전한 글자 subset을 재사용하지 않았다. EB Garamond는 신규 포함하지 않고 기존 serif fallback을 사용한다. 사용자·고객 개인정보와 내부 FLOW/CRM·계약·보수·원문 문서는 dist에 넣지 않았다.

## 5. 실제 실행한 검수와 한계

검수 환경은 격리된 Linux 작업 사본, Python/Node 및 CUA 클라우드 브라우저다. 아래 브라우저 결과는 이번 실제 검수 기록이며 과거 PR 본문의 검수 수치를 재사용한 것이 아니다.

| 명령·검사 | 결과 | 검증 범위·한계 |
|---|---|---|
| `python3 scripts/build_public.py --context deploy-preview` | PASS: HTML 12개, 공통 정적 푸터 11개 | 실제 dist 생성. preview 비교 페이지는 제품 푸터 대상에서 제외 |
| `python3 scripts/check_public.py` | PASS: 로컬 참조 341개, 두 가격 트랙·사업자·ARIA·메타·원문·모바일·산출 제외 검사 | 정적 검수. `dist/__review/build.json`에 근거 기록 |
| `node scripts/check_review_interactions.cjs` | PASS: Node VM 9개 점검 | 문의·상태·이벤트의 실행 검사. 실제 브라우저·클립보드·기기 검증을 대신하지 않음 |
| `NODE_PATH=/tmp/mashcore-review-qa/node_modules node scripts/check_spatial.cjs` | PASS: 실제 dist 대상 Node/linkedom 9개 묶음 | 선택·키보드·초기화·센서 오류/거절·모션 감소·터치 흐름 시뮬레이션. 실제 기기·센서 시험이 아님. QA 의존성은 repo 밖 임시 설치 |
| `python3 scripts/build_public.py --context production` | EXPECTED BLOCK | 상품 범위·과금 기준·VAT 명시 승인 필요. 배포 명령이 아니며 운영 변경 없음 |
| 차단 점검 후 deploy-preview 재생성 | PASS | 최종 검토 결과는 검토 컨텍스트로 복원 |
| 11개 제품 경로 × 320/390/768/1440px | PASS: 44개 페이지·폭 조합 | 실제 브라우저 iframe의 CSS viewport 폭 검사. 세로 스크롤바가 있는 콘텐츠 가용 폭은 설정 폭보다 15px 작을 수 있음 |
| 390px, 10개 경로의 글자 200% 강제 확대 | PASS | 텍스트 확대 검사이며 브라우저 자체 200% 줌 시험은 아님 |
| 실제 A/B | PASS: 읽는 순서 B 선택·정보 순서/상태 확인 | 전환율·고객 이해도 시험 아님 |
| 실제 문의 | PASS: URI, 1,001자 원문 보존·행동 차단, 빈 복사 안내 | 외부 메일 앱·SMTP 발송 없음 |
| 실제 메뉴·3D | PASS: 메뉴 Escape/초점 복귀, 3D 선택·초기화·방향 버튼·키보드 | 물리 터치·센서 시험 아님 |
| Netlify 이번 Preview | READY, 12 HTML 경로와 JS/CSS/폰트 8개 HTTP 200 | 자산 8개는 dist와 바이트 일치. HTML은 Netlify가 삽입한 동일한 Preview toolbar 블록 하나만 제외하면 dist와 일치. 원격 렌더 브라우저 재검사는 아님 |
| 비공개 산출 제외 HTTP | content 2개·docs·scripts·.git 경로 5개 모두 404 | noindex와 별도로 실제 공개 경로 제외를 확인 |
| 외부 CTA/정책 참조 HTTP | Weplace 공식 홈 200; 국가법령정보센터 기존 참조는 이 환경에서 503 | Weplace HTTP 접근만 확인. 법령 링크의 최종 내용/운영 접근은 NEED_VERIFY; 원문 링크는 임의 변경하지 않음 |
| JavaScript 비활성 sandbox | PASS: A 3개+B 3개 정적 대안·이메일 경로 | 실제 스크립트 비활성 렌더 확인 |
| 실제 브라우저 클립보드 API 결과 | PASS: iframe 거절 시 실패 안내·원문 전체 선택·직접 복사 대안 | 성공 오표시 없음. 실제 clipboard 성공은 NOT RUN; 성공 분기는 Node VM에서 확인 |

**NOT RUN / NEED_VERIFY:** 실제 iPhone/Android·소프트 키보드·물리 센서·스크린리더·외부 메일 앱 실행·메일 송수신/SMTP·등록증 대조·PG 심사/개통·사용자 이해도·운영 URL의 이번 변경 바이트 일치·브라우저 자체 200% 확대·브라우저 모션 감소 설정·폰트/이미지 네트워크 강제 실패. 소스의 fallback·reduced-motion 처리는 존재하지만 해당 브라우저 실패 상태 시험 완료로 기록하지 않는다.

main 전용 동기화·검수 스크립트로 dist를 만들거나 검증하지 않았다. 이력 통합 후 legacy 스크립트에는 생성기 프로젝트에서 실행을 중단하는 안내를 추가했다. 실제 산출물 검수는 `build_public.py`·`check_public.py`·두 런타임 검사로 수행했다. 자동 이메일 발송도 하지 않았다.

원격 근거: `docs/qa/remote-preview-20261023.json`. 배포 ID `6adb79ffba2a561ec0faebc8`, context `deploy-preview`, 구현 커밋 `36516abcd7a3375d10645a3a7d547e299f5e3719`. main은 `b31a55c`, 기존 운영 배포 ID는 `6adb113e296767181eb98f02`로 그대로다.

브라우저 폭/글자 확대의 원시 결과: `docs/qa/browser-layout-20261023.json`. 캡처는 홈 데스크톱, 홈 390px, 모바일 복사 실패 대안, 여섯 관점 선택 화면이다. 폰트·색상은 로딩 후 대표 화면에서 확인했으며 모든 상태의 자동 대비 인증을 주장하지 않는다.

## 6. 문의·가격·사업자 현재 상태와 남은 결정

| 항목 | 현재 구현·상태 | 남은 결정·확인 |
|---|---|---|
| 메일 | `weplacehyun@naver.com`, 제목 `[Mashcore] 함께할 일 문의`; 사용자 직접 전송 | 실제 앱 실행·송수신 |
| 본문 | 최대 1,000자는 스크립트 행동 기준. 초과 원문 보존·직접 복사 대안 | 다양한 실제 기기/IME·메일 앱 URI 길이 |
| PR 상품 | 사업 방향·실행 설계 400만 / 고객·매출 분석과 개선 250만 / 한 가지 문제 집중 설계 150만 / 우리 사업 첫 점검 50만 | 이름·범위·기간·횟수·1회 과금은 제안, VAT 미확정 |
| main 상품 | 첫 진단 99,000원 / 집중 진단 50만 / 전략 설계 100만 / 전략과 실행 150만 | 원문별 제안가·공급가액 가안·VAT/범위 조건 유지 |
| 승인 플래그 | `production_approved=false`, `status=PROPOSED`, `basis_status=PROPOSED`, `vat_status=NEED_VERIFY` | 공식 상품·조건 선택 후 별도 승인과 구현 |
| 사업자 | Mashcore / 최규현 / 247-02-04104 / 서울특별시 영등포구 선유로9길 10, 812호 Mashcore | 등록증상 정확 표기 대조 |
| 도메인 | `https://mashcore.co.kr/` canonical/OG 기준 | 현재 운영 변경 반영을 뜻하지 않음 |
| 전화·결제 | 전화 공란 유지, 결제 개통·구매 버튼 없음 | 별도 확인 |
| 새 문안·배치·모션·자산 | 실제 검토 코드 존재, 모두 PROPOSED | 최종 화면·문안 선택, 실제 자산 공개 범위 |

## 7. 다음 구현 묶음과 Weplace 인계

1. 이번 검토 화면을 확인해 홈 문안·A/B/3D 배치·상세 읽기 흐름을 선택한다.
2. 운영 공개 전에 가격 트랙·범위·VAT·상품별 문의와 정책을 함께 확정한다. 플래그만 바꾸어 출시하지 않는다.
3. 실제 기기·메일 앱·접근성·모션 감소·자산 실패 검수의 미실시 항목을 진행한다.
4. 공개 가능한 협업 원자료 한 건을 확보하고, 재구성과 실제 기여·운영 화면을 구분해 보강한다.
5. Weplace는 해당 프로젝트에서 최신 소스·독립 문의·서비스/업종/작업실/고객 공간을 상세 설계한다. Mashcore의 문의·사업자·CRM을 복제하지 않는다.

07 추가 델타의 반영 순서는 기준/상태 → 구현 계보 → 관계 설명 → 실제 경로 → 공동 사례 자료 → 문의·가격·사업자/데이터 경계 → Weplace 상세설계 → 양쪽 최종 연결 검수다. 제공된 파일은 `07_WEPLACE_HANDOFF_DELTA_20261023.md`이며 원래 `07_WEPLACE_HANDOFF.md` 본문은 제공되지 않았다. 기존 07을 수정 완료했다고 보고하지 않는다.

## 8. 공개 단계

필요한 코드와 가역적인 검토 작업을 먼저 완성한 상태다. main 병합·운영 배포는 01·06 및 기존 PR의 최종 확인 조건을 유지한다. 문서 보관·구현 요청·과거 승인/배포 이력은 이번 가격·문안·CI·운영 공개의 승인으로 승계하지 않는다. 이번 보고에서 로컬 코드, 실제 dist, 검토 Preview, 운영 확인은 각각 별도 상태로 남긴다.
