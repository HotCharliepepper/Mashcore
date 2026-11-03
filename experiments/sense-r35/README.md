# MASHCORE R3.5 SENSE EXPERIENCE

독립 실험. 운영 홈의 대체본 또는 검증된 고객 성과가 아니다.

## 실행

저장소 루트에서 Node 22 이상으로 실행한다.

```sh
node qa/r35/serve.mjs
```

브라우저에서 `http://127.0.0.1:8350/sense-r35/`를 연다. 실제 원본은 `experiments/sense-r35/`에 있다. 사이트 루트의 기존 자산과 상세 경로를 재사용하므로 HTTP 서버로 실행한다.

Netlify에서는 Deploy Preview의 `/sense-r35/`에서만 제공된다. `production`과 `branch-deploy`의 패키징에는 포함되지 않는다. main 병합·운영 배포·DNS 변경을 하지 않는다.

## 검수 재실행

```sh
npm ci --prefix qa/r35 --ignore-scripts
cd qa/r35
npx playwright install chromium webkit
cd ../..
node qa/r35/browser.mjs
```

Windows 로컬 검수는 설치된 Chrome을 사용한다. CI에서는 Playwright Chromium과 WebKit을 사용한다. 다른 서버를 검사하려면 `R35_URL`, WebKit을 선택하려면 `R35_BROWSER=webkit`을 설정한다. 캡처와 JSON은 `evidence/r35/`에 저장된다. 실기기 및 실제 스크린리더 사용자 검수와는 구분한다.

## 동작

- Origin: 질문·서비스 링크·정지 포스터. 영상은 명시적 클릭 후 한 번 재생한다. 화면 밖 이동, 탭 숨김, 동작 줄이기 설정 변경 시 멈춘다.
- Second Look: 세 가설 중 하나를 선택하고 다음 확인과 반례를 읽는다. 선택은 정답·유형·점수로 해석하지 않는다.
- Sense OS: S31 / 04 시선 경로(배치 비교), 25 예측가능성(과정 펼치기), 26 통제감(안내 길이 선택·초기화).
- JS 미작동: 가설 전체 본문, CSS 배치 비교, native details, 안내 길이 선택·reset, 내부 링크가 남는다. GSAP만 실패해도 번호 예시는 정적으로 작동한다.
- 저장·분석·전송·계정·예약·결제 기능은 없다.

## 자산

`/assets/r31/origin.webp`, `/assets/r31/origin.mp4`, `/assets/r31/gsap.min.js`를 변경 없이 참조한다. Runway 생성 연출 장면이라는 기존 고지를 유지한다. 기존 자산의 재사용은 현재 실험 범위이며 새로운 초상권·상업적 라이선스 검증을 주장하지 않는다.

고운바탕은 기존 브랜드 서체를 본문에 사용한 글자로 subset하여 로컬 WOFF2(47,796 bytes)로 저장했다. `fonts/OFL.txt`를 동봉한다. 재생성 도구는 `qa/r35/fetch-font.mjs`이며 글자를 추가할 때 다시 실행한다. 본문은 OS 한국어 산세리프를 사용한다. 외부 폰트 요청은 없다.

상세 비교, 결정과 검수 범위: [`docs/R35_SENSE_EXPERIENCE.md`](../../docs/R35_SENSE_EXPERIENCE.md).
