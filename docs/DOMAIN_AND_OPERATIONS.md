# Mashcore — 운영 도메인·사업자 정보 (2026-10-23)

## 현재 운영 정보

- 운영 도메인 (Netlify primarySiteUrl): https://mashcore.co.kr
- GitHub: `HotCharliepepper/Mashcore`, `main` 브랜치 병합 → Netlify 자동 배포
- 공개 사업자 정보: `assets/js/site-config.js`
- 현재 이메일: `weplacehyun@naver.com`
- 사용자 제공 등록번호: `247-02-04104`
- 사용자 제공 대표자: 최규현
- 사용자 제공 주소: 서울특별시 영등포구 선유로9길 10, 812호 Mashcore
- 사용자 제공 영문 상호 표시: Mashcore
- 전화번호: **NEED VERIFY — 미제공, 공개 안 함**
- 법정 상호 표기 및 주소는 **사업자등록증과 최종 대조 필요**
- Netlify 원래 서브도메인과 이전 `mashcore.kr` 계획은 과거 자료이다. 신규 설정에서 무조건 적용하지 않는다.

## 사업자 정보 수정 SOP

1. `assets/js/site-config.js`만 기준 정보로 업데이트한다. 등록증·실제 연락처와 일치하도록 한다.
2. `python3 scripts/sync_mobile.py` — 메인 레이아웃 자체가 바뀌었을 때만 실행한다.
3. `python3 scripts/sync_business_info.py` — 모든 HTML 푸터에 사업자 정보를 사전 렌더링한다. PG 심사/검색 엔진에서 JavaScript 실행 없이도 정보를 읽을 수 있다.
4. `python3 scripts/check_site.py`, `node --check assets/js/site.js` 검사 후 PR → 미리보기 → main 병합 → Netlify 운영 배포 확인.
5. 전화번호는 공식 심사에 요구되므로 실제 사업용 연락처를 확인한 뒤 추가한다. 임의 번호 생성 금지.
6. 이메일 주소는 각 페이지 고객문의·취소/환불 mailto 링크도 함께 확인한다.

## 토스페이먼츠

- 서비스 목록 `/services/`, 취소·환불 정책 `/policies/refund/`은 게시됨.
- 99,000원/50만/100만/150만 등 서비스는 **출시 전 가안**: 구매 가능한 확정 상품이 아니며 결제창은 아직 없다.
- PG 심사 전 실제 상품명·포함 VAT·제공기간·납품물·상품이미지·취소 조건·비회원 주문 흐름을 확정한다.
- 결제창은 토스페이먼츠 테스트 키로 먼저 연동할 수 있지만, 실결제 개통은 PG/카드사 승인 후 가능하다.
- 2026-10-23 사용자 발언: 토스페이먼츠 신청 뒤 '탑재 불가' 메시지 확인. 구체적 사유 및 신용관련 여부 **NEED VERIFY**. 토스 공식 지원팀에 거절 사유와 재심사 가능 조건을 문의한다.
- 라이브 PG 키, 주민등록번호, 결제 비밀번호, 개인 신용 정보 등은 GitHub에 커밋하지 않는다.

## 변경에서 제외

- Chore to Play 모델, 화면 진입 애니메이션, 모바일 인터랙션 재설계는 이번 사업자 정보 수정과 무관. 이후 Work에서 별도 기획·검증한다.

## 공식 가이드

- https://docs.tosspayments.com/guides/v2/get-started/payment-products
- https://docs.netlify.com/manage/domains/manage-domains/assign-a-domain-to-your-site-app/
