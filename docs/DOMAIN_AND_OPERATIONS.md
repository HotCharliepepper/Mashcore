# Mashcore — 도메인·사업자·생성 운영 기준

2026-10-23 리뉴얼 검토 브랜치 기준. 이전 main의 운영 정보 수정 이력을 보존하면서, 실행 절차는 PR의 `build_public.py → dist` 구조에 맞췄습니다. 이 문서는 새 운영 배포·등록증 대조·메일 송수신·PG 승인의 완료 기록이 아닙니다.

## 현재 기준 값

| 항목 | 값·상태 |
|---|---|
| 공식 도메인 | `https://mashcore.co.kr/` — main 및 Netlify primarySiteUrl 확인 기록 |
| 저장소 | `HotCharliepepper/Mashcore` |
| 공개 상호 | Mashcore |
| 대표자 | 최규현 |
| 사업자등록번호 | `247-02-04104` |
| 주소 | 서울특별시 영등포구 선유로9길 10, 812호 Mashcore |
| 이메일 | `weplacehyun@naver.com` |
| 전화 | 미제공·공개하지 않음 |
| 등록증 대조 | 법정 상호·주소 최종 대조 NEED_VERIFY |
| 메일 | 실제 송수신 NOT RUN |

원본은 `assets/js/site-config.js`입니다. PR 생성기는 `Object.freeze` 안의 객체를 strict JSON으로 읽습니다. main의 일반 JS 객체 파일을 통째 덮어쓰지 않고, 값과 파싱 형식을 함께 맞춥니다. Weplace의 사업자·문의·고객정보와 합치지 않습니다.

`mashcore.netlify.app`은 기존 Netlify 기본 호스트이며, `mashcore.kr`은 과거 계획 기록입니다. 현재 도메인으로 자동 되돌리지 않습니다. 이번 구현에서 DNS·SSL·리디렉션을 변경하지 않습니다. 운영 URL의 실제 제공 바이트와 브라우저 상태는 별도 확인 대상입니다.

## 이 브랜치의 수정 절차

1. `assets/js/site-config.js`의 공개 값을 근거에 맞게 수정합니다. 전화나 누락된 등록 정보를 추정하지 않습니다.
2. 생성기의 `BASE/EMAIL`, 문의 런타임, 정책·상품 mailto, canonical/OG/JSON-LD, sitemap과 검사 기대값의 일치를 확인합니다.
3. `python3 scripts/build_public.py --context deploy-preview`로 `dist`를 재생성합니다. 사업자 정적 푸터와 모바일은 이 경로에서 함께 생성합니다.
4. `python3 scripts/check_public.py`와 `node scripts/check_review_interactions.cjs`를 실행합니다. 3D 관련 변경은 개발 의존성이 준비된 환경에서 `node scripts/check_spatial.cjs`로 확인합니다.
5. 실제 `dist`를 렌더하여 경로·모바일·확대·초점·모션 감소·실패 대안을 확인하고, 수행하지 않은 항목은 그대로 기록합니다.
6. 검토 가능한 변경과 결과를 제시한 뒤, 필요한 main 병합·운영 공개의 최종 확인을 받습니다. 과거 승인·배포 이력을 새 변경의 승인으로 승계하지 않습니다.

현재 Netlify 설정은 `dist`만 게시합니다. 운영 context는 미승인 상품을 차단합니다. 운영 차단의 예상 실패를 시험한 뒤에는 검토 출력을 다시 생성합니다. 생성된 모바일·푸터만 수동 수정하지 않습니다.

## 이전 구조의 명령을 혼용하지 않기

`sync_mobile.py`, `sync_business.py`, `sync_business_info.py`, `check_site.py`, `check_interactions.cjs`는 이전 구조의 원본문을 보존한 이력입니다. 이 생성기 프로젝트에서는 안전하게 중단하고 현재 명령을 안내합니다.

main의 `sync_business_info.py`와 `check_site.py`는 single-quoted 일반 JS 객체를 전제로 했습니다. strict JSON 설정을 읽지 못한 채 실행하면 사업자 값을 공란으로 해석하거나 검증을 놓칠 수 있습니다. 이전 푸터 동기화는 저장소를 재귀적으로 수정하므로 `dist`까지 덮을 수 있습니다. 이 브랜치에서는 위의 단일 생성 절차를 사용합니다.

## 서비스·환불·문의의 경계

- `/services/`의 여섯 축은 업무 설명 분류입니다. 실제 개발·배포·DB·보안·대규모 제작은 별도 합의 범위입니다.
- main의 첫 진단 99,000원·집중 진단 50만원·전략 설계 100만원·전략과 실행 150만원은 원문 검토 상태를 유지합니다.
- PR의 400/250/150/50만원 프로토타입은 원본 JSON의 상품명·범위·기간·수량·VAT·승인 상태를 유지합니다. 같은 금액을 같은 상품으로 합치지 않습니다.
- `/policies/refund/`는 main의 정책 본문을 보존합니다. 이번 통합에서 새 환불률·기한이나 법률 검토 완료를 추가하지 않습니다.
- 공통 푸터는 ‘사업자 정보’ 제목 아래 전체 너비의 정적 영역으로 표시합니다. JS가 실패해도 상호·대표·번호·전체 주소·이메일·정책을 읽을 수 있어야 합니다.
- 문의는 메일 앱 열기와 질문 복사입니다. 실제 발송은 사용자가 합니다. 서버 접수·저장·CRM·결제 완료로 표시하지 않습니다.
- 입력 원문과 센서 값을 자동 저장·전송하지 않습니다. noindex는 접근 제어가 아니므로 비공개 원문·내부 명세·고객 자료는 산출물 자체에서 제외합니다.

## 결제와 남은 확인

카드결제·자동결제는 미개통 상태입니다. 2026-10-23 이전 기록의 PG ‘탑재 불가’ 사유는 미확인이고, 개인 신용 사유로 단정하지 않습니다. 상품·VAT·납품물·제공기간·결제 방식·취소 조건·사업자 정보를 확인하고 PG/카드사의 실제 승인이 필요한 단계는 별도로 진행합니다. 라이브 키·주민등록번호·결제 비밀번호·개인 신용 정보는 저장소에 넣지 않습니다.

공식 참고 링크는 기존 기록으로 남깁니다. 이 구현에서 새로운 법률·PG 심사 검증을 수행했다는 뜻은 아닙니다.

- https://docs.tosspayments.com/guides/v2/get-started/payment-products
- https://docs.netlify.com/manage/domains/manage-domains/assign-a-domain-to-your-site-app/

## 검토 기록과 실제 운영 확인

[리뉴얼 검토 기록](RENEWAL_REVIEW_20261023.md)에 작업 ref, 실제 검사, 확인된 검토 주소와 NOT RUN 항목을 분리합니다. main은 기존 운영 배포 경로이며, 이 작업 브랜치에 main을 통합하는 것은 main 병합·운영 배포가 아닙니다.

3D는 `/research/chore-to-play/`에서 직접 접근합니다. 센서는 명시적 opt-in이고 시점만 바꾸며 진단이나 점수가 아닙니다. `/preview/`는 비교용 화면이며 실제 기기·센서·외부 메일 앱을 대체하지 않습니다.
