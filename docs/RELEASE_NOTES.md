# v6.1 review — implementation and QA

작성일: 2026-10-19. 이 문서는 구현/검토 상태이며 Production 배포 완료 보고가 아니다.

## Baseline and change

PR #2 / feature/mashcore-weplace-portfolio-20261019 / 시작 HEAD e79629da7a2775d19e8d0fb79de4453bbcdb180f.
이전 중단된 작업의 Git tree는 커밋·브랜치·배포가 아니었다. 해당 초안을 보완해 같은 PR에 안전한 fast-forward로 연결한다.

새 철학/역할, 네 가격대 상품 프로토타입, 대표·주소·번호 공통 표기, /about/·/services/, 정적 생성/검수/승인 게이트 추가. 이전 HTML 입력/연구 경로와 런타임 JS는 유지. 새 홈은 공통 strategy.css로 조판해 누적 스타일 충돌을 피함. 기존 연구/포트폴리오에서는 푸터 범위만 별도 CSS로 개선.

## Local verification actually performed

Python 생성기/검수기 구문 검사, JSON 읽기·금액 매칭, 미승인 production 차단 확인.
오프라인 실제 Chromium set_content로 홈/모바일/소개/상품 검수본의 320/390/768/1440 폭, 4상품 details, 메뉴/Escape, 기존 3관점 A/B, 방향키 탭 이동, 메일 URI 인코딩, 복사 수동 대안, 390폭 글자 2배 강제 확대, no-JS, reduced-motion: 28개 점검 통과, page error 0.

중요한 한계: 컨테이너 외부 Git DNS와 브라우저 localhost 이동은 환경에서 차단됐다. 네트워크 정책을 바꾸지 않고, 생성한 HTML/CSS/JS를 메모리에 넣어 실제 Chromium으로 렌더링했다. 홈 로컬 입력은 PR에서 읽은 세 섹션으로 만든 integration fixture이며 원격 v5 index 원본을 대체하지 않는다. site.js·observations.js·chapters.js는 원격 Git blob SHA와 정확히 일치한다. 실제 배포본의 전체 링크·ARIA·모바일 동기화는 Netlify가 전체 저장소에서 실행하는 scripts/check_public.py로 별도 검증한다.

외부 Google 폰트 네트워크 대신 시스템 한국어 fallback으로 로컬 확인. 실물 iPhone/Android·센서·스크린리더·60대 사용자 이해도·실제 메일 앱/수신은 미실시. 로컬 검수를 배포 도메인의 종단 브라우저 검수로 표현하지 않는다.

## Deploy boundary and recovery

Netlify는 dist만 게시하며 docs/content/qa/script 미게시, preview noindex. 미승인 상품의 production build는 실패하도록 구성. 현재 운영 main/배포/도메인/DB는 수정하지 않음.
완료 후 최신 커밋·Netlify deploy ID·ready 상태·검수 결과는 PR #2에 기록한다.
복구는 v6 변경을 되돌리는 새 커밋으로 PR을 갱신하는 방식. Production에는 아직 변경된 것이 없어 되돌릴 운영 배포가 없다. git reset --hard/force push/Netlify restore를 사용하지 않는다.
