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

빌드 없는 HTML/CSS/JavaScript. 운영 호스트 `https://mashcore.netlify.app/`; main 병합이 기존 Netlify 배포 경로다. 예상 도메인 mashcore.kr은 DNS·HTTPS 확인 후 전환한다. 루트 경로를 기준으로 서비스한다.

- [DESIGN.md](DESIGN.md): 근거 상태, A–F 설계·Stitch 프롬프트·검수
- [FIGMA_HANDOFF_v4.md](docs/FIGMA_HANDOFF_v4.md): 기존 Figma와의 인계. 이번에 캔버스 동기화는 하지 않음
- [DOMAIN_AND_OPERATIONS.md](docs/DOMAIN_AND_OPERATIONS.md): 도메인 연결·사업자 정보 입력
- `assets/js/site-config.js`: 실제 사업자 등록 후 채울 공란

홈 내용 수정 후 모바일을 동기화한다:

```sh
python3 scripts/sync_mobile.py
python3 scripts/check_site.py
node --check assets/js/site.js
node --check assets/js/chapters.js
node --check assets/js/chore-spatial.js
node --check assets/js/preview.js
```

추가 DOM 회귀 검사(운영 런타임 의존성 없음): 개발 환경에 `linkedom` 설치 후 `node scripts/check_interactions.cjs`, `node scripts/check_spatial.cjs`. 실제 렌더링·센서 검사가 아니므로 iPhone/Android의 직접 확인을 대체하지 않는다.

외부 JavaScript 라이브러리 없이 작동한다. 외부 폰트가 차단되어도 시스템 폰트를 쓴다. 센서 값과 입력한 질문은 자동 저장·전송하지 않는다. 입력은 복사하거나 메일 앱에서 직접 전송한다. `docs/01`–`05`와 v3 archive는 과거 이력이며 현재 구현 기준은 루트 DESIGN.md다.
