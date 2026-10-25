# R2 검수 재현

```sh
python scripts/build_public.py
python scripts/check_public.py
python scripts/check_r2.py
node scripts/check_review_interactions.cjs
NODE_PATH=/path/to/linkedom/node_modules node scripts/check_spatial.cjs
python qa/r2/prepare.py
```

기존 `scripts/check_r1.py`는 R1의 null 영상·SVG 자산 스냅샷 검사로 보존합니다. R2에는 `check_r2.py`를 사용합니다. `check_public.py`는 공통 회귀 검사입니다. R2의 `/mobile/` 메타데이터는 별도이지만 body는 홈과 같아야 합니다.

`qa/r2/site`를 로컬 검토 서버로 열고 `/qa/browser.html`에서 실제 iframe을 검사합니다. layout matrix는 11경로×4폭, 글자 200% 11경로, JS 차단 3경로입니다. interaction tests는 실제 미디어·A/B·문의·모션 감소·환경 복구·회전 시 사용자 정지/종료 상태를 확인합니다. 테스트 클립은 2.5초 색상 막대이며 실제 R2 자산 시험과 구분합니다. 권한 거절·모션 선호·visibility·save-data는 명시적 주입입니다.

`/qa/performance.html`은 실제 홈 HTML에 로컬 PerformanceObserver를 넣은 진단 페이지입니다. LCP와 관찰한 layout-shift 합계를 기록합니다. 네트워크·CPU 제한, 실기기, CrUX, 세션 전체 INP 계산은 수행하지 않습니다. 수치가 운영 성능 보장은 아닙니다. `performance.js`는 dist에 포함하지 않습니다.

화면 비교의 `페이지 전체`는 iframe을 문서 높이로 펼쳐 전체 홈 캡처를 돕습니다. 글자 200%는 브라우저 zoom을 대체하지 않습니다. 320/390/1440 프레임 높이는 844/844/960px, 768은 1024px이며 자동 matrix의 태블릿 높이는 960px입니다. OS 스크롤바 영역은 별도로 차지합니다.

원격 검증:

```sh
python qa/r2/check_preview.py --url https://VERIFIED_DEPLOY_URL --deploy-id VERIFIED_DEPLOY_ID
```

동일한 dist와 HTTP 내용을 비교합니다. 해당 deploy ID의 Netlify preview toolbar만 제외합니다. HTML·미디어·JS·CSS와 noindex, 내부 소스의 404를 검사합니다. URI·HTTP 검사가 실제 메일 발송/수신이나 운영 승인을 대신하지 않습니다.
