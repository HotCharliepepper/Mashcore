# Release notes — Mashcore v5 preview

기록일: 2026-10-19 KST.
대상: feature/mashcore-weplace-portfolio-20261019의 이 기록을 포함한 커밋.
단계: 프리뷰 검토. 최종 main 병합·production 반영 승인 대기.

## 변경

히어로의 역할 구체화, 세 관점의 가상 화면 A/B, Weplace 홈 카드와 /work/weplace/ 상세, 사용자 제공 사업자번호 247-02-04104의 공통·정적 푸터 반영, 홈·모바일 동기화, 탐색·메타·사이트맵·운영 문서를 갱신했다.

기존 연구 경로·Chore to Play 입체 모형·문의 작성과 복사를 유지한다.

## 완료한 검수

| 검수 | 결과 | 범위 |
|---|---|---|
| scripts/check_site.py | PASS | HTML 10개 경로의 링크·자산·ID·ARIA·한국어·H1·메타·JSON-LD |
| scripts/check_interactions.cjs | PASS | 메뉴·Escape·문의 초안·복사·수동 대안·기존 탭/조건·사업자 표시·HTML 삽입 방지·비교 경로 |
| scripts/check_observations.cjs | PASS | 홈/모바일의 세 관점·키보드·A/B 실순서·동일 정보·details 상태·no-JS·정적 번호·정확한 동기화 |
| scripts/check_spatial.cjs | PASS | 연구 모형의 선택·회전·센서 권한/실패/미지원/지연·모션 감소·정리 시뮬레이션 |
| JS/CSS 구문 | PASS | JS 6개·CSS 7개 구문 분석 |
| 독립 코드·문안 검토 | PASS | 가상 A/B 표현·협업 범위·no-JS·반응형 CSS 구조에서 수정 필요 문제 발견 없음 |

검수 환경은 정적 분석과 Node DOM 시뮬레이션이다. 개발 전용 임시 환경에 linkedom 0.18.12와 css-tree 3.1.0을 사용했으며 운영 의존성은 추가하지 않았다.

## 남은 확인

- NEED VERIFY: 320/390/768/1440px 실제 브라우저 렌더링·가로 넘침·줄바꿈·200% 확대.
- NEED VERIFY: iPhone/Android 실기기·VoiceOver/TalkBack·실제 메일 앱·물리 센서.
- 관리 환경에 허용된 control-browser가 없어 브라우저 렌더링 QA를 수행하지 않았다. 정적 CSS 구간 확인을 실기기 완료로 보고하지 않는다.
- 실제 프리뷰 URL·배포 완료 상태는 이 변경의 GitHub PR·Netlify 체크에서 확인한다. URL 생성만으로 배포 완료라고 처리하지 않는다.

## 운영 반영과 복구

출발 main: 45bba47cee6e59e64fd74ea50e3779a9e4865208.
출발 production: 6acea31aa6b6223a8eaafa43, ready, 위 커밋과 일치.

첨부 05_CHANGE_AND_QA_PROTOCOL.md의 branch → preview → QA → 승인 → main → production 순서를 따른다. 검토 가능한 결과를 제시한 뒤 최종 운영 반영을 승인받는다.

프리뷰 오류는 같은 브랜치에서 수정한다. 운영 반영 후 되돌려야 하면 변경을 되돌리는 새 커밋을 검토·병합하여 기존 Git CD로 배포한다. 과거 배포를 임의로 재발행하거나 DNS·호스팅 경로를 바꾸지 않는다.
