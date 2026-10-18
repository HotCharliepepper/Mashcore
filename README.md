# Mashcore

고객의 작은 행동과 화면의 구조를 연구해, 대표님의 일이 더 잘 전해지도록 돕는 전략 파트너의 공개 홈페이지.

## Small observations & Weplace portfolio v5

2026-10-19 KST 프리뷰 검토본. 네 장면 안에 관찰 체험·Weplace 포트폴리오·사용자 확정 사업자번호를 담는다. 최종 운영 반영은 프리뷰·QA 결과를 확인한 뒤 승인한다.

| 경로 | 내용 |
|---|---|
| / | 보다 → 다르게 보다 → 현장에 놓다 → 함께 묻다 |
| /mobile/ | 동일 콘텐츠의 모바일 전용 세로 구성 |
| /work/weplace/ | Weplace 공개 홈페이지의 전략·경험 설계 협업 |
| /preview/?view=desktop | 1440px 데스크톱 비교 |
| /preview/?view=mobile | 390px 모바일 비교 |
| /explore/ | 기존 관점·주제·글 보존 |
| /research/ | 연구 전체 |
| /research/chore-to-play/ | 여섯 동시 관점 입체 모형·조건 탐색·기울기 선택 사용 |
| /research/market-interpretation/ | 판단력 교육 R&D |
| /research/log/ | 공개 연구 기록 |
| /about/ | Mashcore Lab·Weplace·Mashcore34 소개 |

빌드 없는 HTML/CSS/JavaScript. 운영 호스트 https://mashcore.netlify.app/ 와 기존 GitHub main → Netlify Git CD를 유지한다. mashcore.kr은 DNS·TLS 확인 후 별도 전환한다.

- [DESIGN.md](DESIGN.md): 현재 화면과 동작 기준.
- [DECISIONS](docs/DECISIONS.md), [CLAIMS](docs/CLAIMS.md), [RELEASE_NOTES](docs/RELEASE_NOTES.md): 판단·근거·검수·배포 상태.
- [도메인·사업자정보 운영](docs/DOMAIN_AND_OPERATIONS.md).
- [v4 설계 이력](docs/DESIGN_v4_archive.md).

### 수정 후 동기화

```sh
python3 scripts/sync_mobile.py
python3 scripts/sync_business.py
python3 scripts/check_site.py
node --check assets/js/site.js
node --check assets/js/chapters.js
node --check assets/js/observations.js
node --check assets/js/chore-spatial.js
node --check assets/js/preview.js
```

사업자정보의 단일 원본은 assets/js/site-config.js다. 사용자 확인 사업자번호 **247-02-04104**만 반영했고 다른 필드는 비어 있다. sync_business.py는 정적 HTML도 갱신해 JavaScript 없이 번호를 읽을 수 있게 한다.

### 상호작용 검사

개발 환경에만 linkedom을 설치한 뒤 실행한다. 운영 사이트에는 외부 JavaScript 의존성이 없다.

```sh
node scripts/check_interactions.cjs
node scripts/check_observations.cjs
node scripts/check_spatial.cjs
```

DOM 검사는 실제 브라우저 줄바꿈·가로 넘침·센서 검사가 아니다. 실기기·브라우저 검수 상태는 RELEASE_NOTES에 별도로 기록한다.

A/B는 같은 가상 안내의 배치를 비교하는 체험이다. 실제 실험 결과·국적별 비율·전환율 우위를 주장하지 않는다. 체험과 질문 입력은 자동 저장·전송하지 않는다. 사용자가 복사하거나 메일 앱에서 직접 보낸다.
