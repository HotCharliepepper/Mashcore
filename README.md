# Mashcore — interactive renewal review

‘함께 하여 강화한다’를 중심으로 홈 네 장면, 서비스·소개·연구·Weplace 협업·독립 문의를 탐색하는 검토본입니다. 새 문안·배치·모션은 **PROPOSED**, 두 가격 트랙은 검토 상태입니다. main 병합·운영 공개·가격 확정·결제 개통은 별도 단계입니다.

## 구현 계보

- 작업 ref: `review/mashcore-renewal-20261023`.
- 기존 Draft PR #2 HEAD `9e857fdca62b66bd7d81ecc3492940124a02c08a`에서 이어갑니다. PR #2를 폐기하거나 과거 SHA로 reset하지 않습니다.
- 비교 main: `b31a55cea32cd83113624f9cdc27bd8d8bc36926`. 최신 사업자정보·정적 푸터·환불·서비스 검토안을 통합합니다.
- 첫 리뉴얼 구현 커밋: `d97499f89297f522d1703ff8668ace11662b3cf0`. main의 변경을 이 검토 브랜치로 가져오는 통합은 **main으로 병합하는 작업이 아닙니다**.
- 최신 커밋·검토 주소·실제 검수 결과는 [리뉴얼 검토 기록](docs/RENEWAL_REVIEW_20261023.md)에 기록합니다. 과거 Preview를 이번 결과로 취급하지 않습니다.

## 원본과 산출물

이 브랜치는 **`scripts/build_public.py → dist/`** 한 생성 경로를 사용합니다. Netlify 게시 디렉터리도 `dist/`입니다. 루트 HTML을 그대로 배포하거나 생성된 HTML만 직접 고치지 않습니다.

| 파일 | 역할 |
|---|---|
| `index.html` | PR 관찰 A/B의 입력 원문과 추출 마커 |
| `content/strategy.json` | 철학·문안의 검토 기준, PROPOSED 상태 |
| `content/services-prototype.json` | PR 네 상품의 금액·범위·기간·VAT·승인 상태 원본 |
| `content/services-main-review.html` | main의 별도 가격 검토 카드 원문 |
| `assets/js/site-config.js` | 최신 공개 사업자 값, `Object.freeze` 안 strict JSON |
| `scripts/review_home.py`, `scripts/review_details.py` | 08의 홈·서비스·소개 검토 구성을 생성 |
| `research/`, `explore/`, `work/weplace/`, `policies/refund/` | 보존·편집할 상세 원본 |
| `assets/css/renewal.css`, `assets/css/research-review.css` | 검토본 시각 구성 |
| `dist/` | 실제 화면·링크·상태의 최종 검수 대상 |

모바일은 같은 홈 결과에서 생성합니다. `content/`, `docs/`, `scripts/`, `qa/`, Git 데이터와 비공개 원문은 `dist/`에 포함하지 않습니다. `noindex`는 검색 제외 요청이며 접근 제어가 아닙니다.

## 생성과 검사

Python 표준 라이브러리를 사용하는 생성기입니다. 저장소 루트에서 실행합니다.

```sh
python3 scripts/build_public.py --context deploy-preview
python3 scripts/check_public.py
node scripts/check_review_interactions.cjs
node scripts/check_spatial.cjs
```

- `check_public.py`: 실제 `dist`의 경로·링크·메타데이터·정적 푸터·정책·가격 상태·A/B 원문·모바일 동기화·공개 범위를 검사합니다.
- `check_review_interactions.cjs`: 실제 런타임 코드의 문의·메뉴·A/B 상태를 Node VM 이벤트 모형에서 검사합니다.
- `check_spatial.cjs`: 실제 `dist`의 3D 원문과 런타임을 DOM 모형에서 검사합니다. 개발 검사 의존성 `linkedom`이 필요합니다. 설치되지 않은 환경에서는 실행 불가를 기록하며, 성공으로 처리하지 않습니다.
- 위 검사는 렌더 브라우저·물리 기기·센서·외부 메일 앱·SMTP 검증을 대신하지 않습니다.

미승인 상품의 운영 차단을 확인하는 다음 명령은 **실패가 기대 결과**입니다. 배포 명령이 아닙니다. 확인 후 검토용 산출물을 다시 생성합니다.

```sh
python3 scripts/build_public.py --context production
python3 scripts/build_public.py --context deploy-preview
python3 scripts/check_public.py
```

`production_approved`, `status`, `basis_status`, `vat_status`를 플래그만 바꿔 출시하지 않습니다. `CONTEXT=production`이 설정된 환경에서는 명령 인자와 별개로 운영 차단이 적용됩니다.

기존 `sync_mobile.py`, `sync_business.py`, `sync_business_info.py`, `check_site.py`, `check_interactions.cjs`는 이전 빌드 없는 구조의 이력입니다. 본문은 보존하되 이 생성기 프로젝트에서는 명시적으로 중단하도록 했습니다. 이 명령을 위 생성·검사 명령과 혼용하지 않습니다.

## 검토 경로

| 경로 | 내용 |
|---|---|
| `/`, `/mobile/` | 네 장면·원문 A/B·협업·문의 |
| `/services/` | 여섯 설명 축, 산출물 예시, 진행 방식, 두 가격 검토 트랙 |
| `/about/` | 규현의 역할·판단 방식·프로젝트별 협업 |
| `/research/` | Lab/Market 편집 입구와 기존 원문 연결 |
| `/research/chore-to-play/` | 여섯 동시 관점·3D·정지 목록·조건 탐색·수정 이력 |
| `/research/market-interpretation/`, `/research/log/` | 판단 연구와 기존 날짜의 변경 기록 |
| `/explore/` | 기존 관점·주제·글·질문 |
| `/work/weplace/` | 협업의 질문·선택 이유·자료 상태·독립 문의·Weplace 공식 홈 연결 |
| `/policies/refund/` | main에서 보존한 취소·환불 안내 |
| `/preview/` | 화면 폭·페이지 선택·글자 확대·스크립트 차단 비교. 실제 브라우저 줌/실기기와 구분 |

## 문의·판매·운영 정보

- 공식 도메인·canonical: `https://mashcore.co.kr/`. 기존 `mashcore.netlify.app`은 Netlify 기본 호스트이며 DNS를 변경한 작업이 아닙니다.
- 공개 설정: Mashcore / 최규현 / `247-02-04104` / 서울특별시 영등포구 선유로9길 10, 812호 Mashcore / `weplacehyun@naver.com`.
- 전화번호는 미제공이며 만들지 않습니다. 등록증의 상호·주소 대조와 실제 메일 송수신은 별도 확인 사항입니다.
- 문의는 메일 앱의 작성창 열기 또는 질문 복사입니다. 사용자가 메일 앱에서 직접 보냅니다. 서버 접수·저장·CRM 등록이 없습니다.
- 1,000자 초과 원문은 남겨 두고 메일·자동 복사만 제한합니다. 직접 선택·복사·이메일 경로를 제공합니다.
- PR의 400/250/150/50만원 프로토타입과 main의 99,000원/50만/100만/150만원 검토안은 서로 다른 상품입니다. 공식 가격·범위·VAT가 확정된 판매 페이지가 아닙니다.
- 실제 카드결제·자동결제는 미개통 상태입니다. 정책 게시를 PG 승인이나 결제 개통으로 설명하지 않습니다.

## 관련 기록

- [구현·검수·미실시·남은 결정](docs/RENEWAL_REVIEW_20261023.md)
- [운영 정보와 이 브랜치의 수정 절차](docs/DOMAIN_AND_OPERATIONS.md)
- [Weplace 인계 추가 델타](docs/07_WEPLACE_HANDOFF_DELTA_20261023.md)
- [폰트 출처·라이선스·대안](docs/REVIEW_FONT_SOURCES.md)

과거 `DESIGN.md`, v3/v5/v6 문서는 이력이며 이번 실행 명령을 대체하지 않습니다. 연구·현장 설명의 실제/재구성/검토 상태를 유지하고, 사용자 최종 확인 전 main 병합·운영 공개를 진행하지 않습니다.
