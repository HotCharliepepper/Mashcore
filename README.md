# Mashcore

사람의 망설임과 브랜드의 신호를 읽고, 연구와 현장을 연결하는 공개 홈페이지.

## Scene & Spatial v4

짧은 철학과 네 장면, Chore to Play의 여섯 관점 입체 모형, 휴대폰 기울기 선택 사용, 모바일 전용 구성과 화면 비교를 추가했다. Editorial Review v2와 기존 GitHub 연구를 이어 받은 v3 내용은 `/explore/`에 보존한다.

| 경로 | 내용 |
|---|---|
| `/` | 네 장면 랜딩, 반응형 기본 화면 |
| `/mobile/` | 같은 콘텐츠의 모바일 전용 세로 구성 |
| `/preview/?view=desktop` | 1440px 데스크톱 비교 |
| `/preview/?view=mobile` | 390px 모바일 비교 |
| `/explore/` | 기존 관점·주제 탭, 글 초안, 질문 정리 |
| `/research/` | 연구 전체 |
| `/research/chore-to-play/` | 입체 모형·일의 조건 탐색·연구 이력 |
| `/research/market-interpretation/` | 판단력 교육 R&D |
| `/research/log/` | 공개 연구 변경 기록 |
| `/about/` | Mashcore Lab·Weplace·Mashcore34 역할 |

빌드 없는 HTML/CSS/JavaScript. 운영 주소는 Netlify 프로젝트에서 확인한 `https://mashcore.co.kr/`이다(2026-10-23 확인). `main` 병합 시 Git 기반 배포가 이루어진다. 기존 `mashcore.netlify.app`은 Netlify 기본 호스트이며, 다른 도메인 `mashcore.kr`은 별도 확인 대상이다.

- [DESIGN.md](DESIGN.md): 근거 상태, A–F 설계·Stitch 프롬프트·검수
- [FIGMA_HANDOFF_v4.md](docs/FIGMA_HANDOFF_v4.md): 기존 Figma와의 인계. 이번에 캔버스 동기화는 하지 않음
- [DOMAIN_AND_OPERATIONS.md](docs/DOMAIN_AND_OPERATIONS.md): 도메인 연결·사업자 정보 입력
- `assets/js/site-config.js`: 공개 사업자 정보의 원본 (2026-10-23 사용자 제공값 반영, 전화번호·등록증 표기 대조는 미완료)

홈 내용 수정 후 모바일을 동기화한다:

```sh
python3 scripts/sync_mobile.py
python3 scripts/sync_business_info.py
python3 scripts/check_site.py
node --check assets/js/site.js
node --check assets/js/chapters.js
node --check assets/js/chore-spatial.js
node --check assets/js/preview.js
```

추가 DOM 회귀 검사(운영 런타임 의존성 없음): 개발 환경에 `linkedom` 설치 후 `node scripts/check_interactions.cjs`, `node scripts/check_spatial.cjs`. 실제 렌더링·센서 검사가 아니므로 iPhone/Android의 직접 확인을 대체하지 않는다.

외부 JavaScript 라이브러리 없이 작동한다. 외부 폰트가 차단되어도 시스템 폰트를 쓴다. 센서 값과 입력한 질문은 자동 저장·전송하지 않는다. 입력은 복사하거나 메일 앱에서 직접 전송한다. `docs/01`–`05`와 v3 archive는 과거 이력이며 현재 구현 기준은 루트 DESIGN.md다.

## Service & policy readiness (2026-10-23)

- `/services/`: 서비스와 가격 검토안 및 문의 흐름. **아직 실제 카드결제 불가.**
- `/policies/refund/`: 공개 취소·환불 기준 및 연락 방법.
- 모든 공개 페이지 상단의 서비스 안내, 하단 환불정책 링크를 유지한다.
- 상품별 확정 제공 범위·기간·부가세는 확인 후 업데이트한다. 사업자 정보는 표시하되 실제 사업자등록증과 법정 상호·주소를 최종 대조하고 사업용 전화번호를 추가해야 한다.
- 토스페이먼츠 정식 심사·라이브 결제 구현은 **미완료**. 사이트 정책 게시를 결제 개통으로 간주하면 안 된다.
- 링크 검사: `python3 scripts/check_site.py` · 모바일 동기화: `python3 scripts/sync_mobile.py` (홈 원본 수정 시)

## 2026-10-23 Business contact patch

- 이메일 `weplacehyun@naver.com`, 등록번호 `247-02-04104`, 대표자 최규현, 사용자 제공 사업장 주소를 정적 푸터에 표시.
- 실제 사업자등록증 상호/주소 표기와 전화번호 **NEED VERIFY**.
- 기존 인터랙션/애니메이션 기능은 보존했으며 Work 후속 작업 범위로 분리함.
- PG '탑재 불가' 표시 원인은 미확인. 심사기관 답변 없이 개인 신용 사유로 단정하지 않음.
