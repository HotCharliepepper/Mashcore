# MASHCORE R3.4 — Homepage Journey / Phase 2

기준일: 2026-10-31 KST  
상태: Draft 구현 · 운영 미반영 · 검수 결과는 현재 PR CI와 연결해 별도 판정

## 기준 버전과 변경 경계

- Repository: `HotCharliepepper/Mashcore`
- 기준 부모: R3.4 IA Draft #17, `158da502072c82f144a37928e045a7897928585c`
- 계보: R3.1 운영 `a8dae1c4` → R3.2 Draft #15 → R3.3 Draft #16 → R3.4 IA Draft #17 → 이 Phase 2
- 이 PR은 누적 Draft이므로 기존 PR들과 **독립적으로 main에 병합하지 않는다**.
- 기존 R3.3의 2.2초/0.90초 SplitText, native proximity, 고정 Origin 영상과 역할·문의·사업자정보·검색 메타데이터, 4장면 ID 및 현재 서비스/상세 경로는 변경하지 않는다.
- GitHub main, Netlify production, DNS, DB, 결제, 실고객 데이터 및 PR #14~#17은 변경하지 않는다.

## 사용자 의도 → 구현

메인에서는 **발견 → 빠른 업무 이해 → 비교 가능한 근거 → 상세 선택 → 문의**를 돕고, 선택한 상세에서는 근거와 반례로 깊어지는 구조를 만든다.

### 1. LAB / NOTES / SIGNAL STUDIO 진입

- 기존 흩어진 LAB/NOTES/Studio 입구를 하나의 세 카드로 통합.
- LAB → `/research/lab/`: 관찰/근거/반례/판단 방법.
- NOTES → `/research/notes/`: 기존 공개 원문과 날짜·출처. 가짜 신규 발행·CMS·실시간 시장지표를 만들지 않음.
- SIGNAL STUDIO → `/signal-studio/`: Owner-First R2.1 로컬 Gate 0 소개. 실결제/자동게시/외부 생성 API 완료로 표현하지 않음.
- 내부 네 번째 책임인 LEDGER는 공개 링크·카드·소스에 넣지 않음.
- Weplace는 Mashcore의 하위 부문/자회사가 아닌 독립적인 현장 실행 협업 경로 `/work/weplace/`.

### 2. Chore to Play의 홈 경험 조정

- 기존 여섯 동시 관점/공간모형을 삭제하지 않고 네이티브 `<details>`의 사용자 선택 뒤에 둔다.
- 기존 `#chore-research` 앵커는 요약 진입으로 유지한다.
- `/research/chore-to-play/`의 원문 및 동일한 여섯 관점의 상세 모델은 수정하지 않는다.
- 첫 방문자는 긴 철학적 연구를 지나지 않고 `field`로 이동할 수 있다. 펼친 경우 기존 기능과 모션 감소/키보드 기준을 보존한다.

### 3. Field에서 설명하는 실제 일의 구조

- 실제 고객 실적을 만들거나 재구성해서 성과처럼 보여주지 않는다.
- 정보의 **순서**만 비교하는 가상 매장 Before/After를 네이티브 라디오와 CSS로 제공한다.
- 실제/가정의 구분과 제한을 비교 UI 바로 옆에서 읽을 수 있게 표기한다.
- Mashcore의 해석·설계 / Weplace의 별도 현장 적용을 구분하여 서비스·협업 상세로 연결한다.

## 적용 파일

- `index.html`: 공통 메인 원본
- `mobile/index.html`: 동일 내용, 모바일 title만 구분
- `assets/css/r34-home.css`: 위 세 구역에 한정된 디자인
- `qa/r34_home_journey.py`: 실제 Draft Preview 반응형/키보드·네이티브 비교·JS-off·200% CSS zoom 검사
- `.github/workflows/r34-home-journey.yml`: 소스·빌드 3 context·기존 기능·브라우저 QA

## 통과 게이트

1. 기존 `scripts/check_site.py`, `scripts/check_release.py`, `scripts/check_r32.py`, `scripts/test_r31_boundary.py` 재검수.
2. `scripts/check_interactions.cjs`와 `scripts/check_spatial.cjs`에서 기존 문의·연구 기능 보존 확인.
3. Chromium 320/390/768/1440과 WebKit 390, 홈과 `/mobile/` 각각: 세 카드, Before/After 라디오, Chore 열기, 이동, overflow, 원래 Hero CTA.
4. Javascript 없는 기본 문서에서도 카드 링크, 네이티브 라디오, details가 동작.
5. 200% CSS zoom은 실제 브라우저 UI 확대/물리 기기와 구분. 모바일 iOS/Android·실사용자·운영 Core Web Vitals·전환효과는 별도 검증.
6. Draft noindex와 R3.4 IA review 경로의 production/branch exclusion 확인.

## 공개/인계 상태

이 구현은 신규 공개 승인/실적 검증이나 운영 배포가 아니다. 승인된 Preview에서 사용자 이해도와 실제 전환 경로를 검토한 뒤 최종 문안·실제 사례/권리·운영 적용을 별도 결정한다. 위 변경은 Weplace 소유·운영 정보 및 고객 자료를 변경하지 않는다.
