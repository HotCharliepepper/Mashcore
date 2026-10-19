# Mashcore — 함께 하여 강화한다 / v6.1 review

여러 현장의 경험과 최규현의 전략·브랜드·디지털 설계, 만덕의 데이터 분석을 연결하는 전략 파트너의 홈페이지 검토안.

## Source and deployment

- 기존 PR #2와 `feature/mashcore-weplace-portfolio-20261019`를 이어간다. 기준 HEAD: `e79629da7a2775d19e8d0fb79de4453bbcdb180f`.
- 기존 `main` / Netlify Production은 이 작업의 변경 대상이 아니다.
- `content/strategy.json`: 철학·역할·소개 문안.
- `content/services-prototype.json`: 400/250/150/50만원, 대상·수량·범위·제외·수정·기간·VAT·승인 상태의 단일 원본.
- `assets/js/site-config.js`: 사용자 제공 사업자 공개 정보. 대표 최규현 / 247-02-04104 / 선유로9길 10. 등록상호·층/호수·전화는 임의 입력하지 않음.
- `scripts/build_public.py`: 기존 v5 홈페이지의 관찰/포트폴리오/질문 DOM을 가져와 새 철학·역할·상품과 결합하고, 전체 공개 파일을 `dist/`에 생성.
- 루트 `index.html`, `mobile/index.html`, `about/index.html`은 이전 v5 입력/이력이다. 현재 배포될 HTML의 기준은 **빌드 후 `dist/`**다. 루트 HTML을 그대로 수동 배포하지 말 것.
- 공개 주소·canonical은 기존 Netlify 호스트 유지. DNS 변경 없음.

## Build and check

```sh
python3 scripts/build_public.py --context deploy-preview
python3 scripts/check_public.py
# 아래는 의도적으로 실패해야 함: 실제 배포가 아닌 로컬 승인 차단 검사
python3 scripts/build_public.py --context production
```

Python 표준 라이브러리만 사용. Netlify가 실제 저장소 전체를 대상으로 빌드 후 정적/링크/ARIA/메일/VAT/모바일 동기화/프로덕션 차단을 검사한다. 공개되는 것은 `dist/`뿐이고 `content/`, `docs/`, `scripts/`, `qa/`는 제외한다.

## Routes

홈과 `/mobile/`은 같은 문안. `/about/`은 철학·하는 일·역할 소개. `/services/`는 네 상품의 상세 비교. `/work/weplace/`, `/explore/`, `/research/`, `/research/chore-to-play/`, `/research/market-interpretation/`, `/research/log/`, `/preview/` 유지.

## Review boundary

금액은 사용자 지정. 1회 프로젝트 기준, 상품명·범위·기간·수정 횟수는 제안이며 VAT 포함 여부는 미정. 실제 결제·접수·예약·자료 업로드·개인정보 공유·매출 보장 없음. 메일 앱 초안 작성과 수동 복사만 제공한다. 운영 배포는 가격/조건 및 공개 정보 검토, QA와 사용자 최종 승인 후 별도 변경으로 진행한다. 현재 프로덕션 빌드는 차단된다.
