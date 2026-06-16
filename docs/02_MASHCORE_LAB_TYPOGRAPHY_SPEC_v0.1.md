# 02_MASHCORE_LAB_TYPOGRAPHY_SPEC_v0.1

- 문서 상태: `DESIGN SYSTEM DRAFT`
- 목표: 다섯 페이지의 문장 위계와 읽는 호흡을 하나로 통일
- 상위 기준: `03_LAB_DESIGN_DNA.md`

---

## 1. 타이포의 역할

Mashcore Lab의 타이포는 꾸미는 장치가 아니라 **사유의 속도를 조절하는 구조**다.

- Serif — 생각, 질문, 여운
- Sans-serif — 이해, 이동, 상태 정보
- Garamond italic — 버전, 주석, 편집적 표식

---

## 2. 권장 폰트 스택

```css
:root{
  --font-serif:'Gowun Batang','Nanum Myeongjo','AppleMyungjo','Batang',serif;
  --font-sans:'Pretendard Variable','Pretendard',-apple-system,'Apple SD Gothic Neo','Noto Sans KR',system-ui,sans-serif;
  --font-editorial:'EB Garamond','Cormorant Garamond',Georgia,serif;
}
```

### 역할

| 역할 | 폰트 | 사용처 |
|---|---|---|
| 국문 디스플레이 | Gowun Batang | Hero, 큰 질문, 파치먼트 선언 |
| 국문 본문 | Pretendard | 설명 문단, 정의, 사례, UI |
| 국문 인용·짧은 사유 | Gowun Batang | 인용, 연결 문장 |
| 라틴 라벨·버전 | EB Garamond 또는 Pretendard | Research 번호, 버전, 날짜 |
| 내비게이션·버튼 | Pretendard | 이동과 조작 |

Hanken Grotesk는 Pretendard와 역할이 겹치므로 최종 빌드에서는 제거 가능하다.

---

## 3. 타입 스케일

```css
:root{
  --type-display:clamp(2.55rem,5.2vw,4.25rem);
  --type-h1:clamp(2.15rem,4.2vw,3.5rem);
  --type-h2:clamp(1.75rem,3vw,2.65rem);
  --type-h3:clamp(1.35rem,2vw,1.85rem);
  --type-question:clamp(1.55rem,2.6vw,2.35rem);
  --type-body-lg:clamp(1.08rem,1.35vw,1.2rem);
  --type-body:clamp(1rem,1.05vw,1.08rem);
  --type-small:.875rem;
  --type-label:.75rem;
}
```

| 토큰 | Desktop 기준 | Mobile 기준 | 용도 |
|---|---:|---:|---|
| Display | 56–68px | 38–44px | Hero |
| H1 | 46–56px | 34–40px | 페이지 제목 |
| H2 | 36–44px | 28–32px | 주요 섹션 |
| H3 | 24–30px | 21–25px | 개념·카드 제목 |
| Question | 30–38px | 24–29px | 열린 질문 |
| Body Large | 18–20px | 17–18px | 서문·핵심 설명 |
| Body | 16.5–18px | 16–17px | 일반 설명 |
| Small | 13–14px | 13px | 캡션·보조 |
| Label | 11–12px | 11px | 영문 라벨·버전 |

---

## 4. 행간과 폭

```css
.prose{
  max-width:42.5rem;
  font-family:var(--font-sans);
  font-size:var(--type-body);
  line-height:1.85;
  letter-spacing:-.012em;
  word-break:keep-all;
  overflow-wrap:anywhere;
}

.display,
.question{
  font-family:var(--font-serif);
  word-break:keep-all;
  text-wrap:balance;
}
```

- 긴 본문 최대 폭: 640–680px
- 선언·질문 최대 폭: 760–900px
- 한 문단은 데스크톱 기준 3–7행을 권장
- 긴 영어 개념어가 모바일에서 넘치지 않도록 `overflow-wrap:anywhere`

---

## 5. 굵기

- Gowun Batang 400 — 기본 헤드라인·인용
- Gowun Batang 700 — Hero의 제한적 강조
- Pretendard 400 — 본문
- Pretendard 500–600 — UI·소제목·정의 라벨
- 영문 라벨에 과도한 700–800 금지

한 화면에서 굵기 단계는 최대 세 개만 쓴다.

---

## 6. 언어 위계

### 한국어

- 생각과 설명의 주언어
- 큰 제목·본문·질문 모두 한국어 우선

### 영어

- `[RESEARCH IN PROGRESS]`
- `Research 01`
- `Revision · L1`
- `Selected Research Log`

처럼 짧은 편집 표식에만 쓴다. 긴 영어 본문은 사용하지 않는다.

---

## 7. 페이지별 타이포 적용

### Home

- Hero: Serif Display
- 다섯 연구 주제 제목: Serif H3
- 주제 설명: Sans Body
- 파치먼트 선언: Serif H2 / 넓은 행간

### Research Index

- 연구명: Serif H1
- 연구 상태·레벨: Sans Label
- 연구 방식: 번호는 Garamond, 설명은 Sans

### Chore to Play

- 원래 가설: Serif
- 개념 정의: 제목 Serif + 설명 Sans
- 매트릭스 축·상태: Sans
- 열린 질문: Serif Question

### Research Log

- 날짜·유형·레벨: Garamond/Sans Label
- 제목: Serif H2
- 이전 생각: Serif Italic 또는 일반 Serif
- 이유·현재 판단: Sans Body

### About

- `읽다.`: Serif Display
- 역할 설명: Sans Body
- `Mashcore Lab / Weplace / Mashcore34`: Serif H3
- 인물 소개: Sans Body + 짧은 Serif 문장

---

## 8. 접근성·성능

1. 본문 최소 16px 유지
2. 다크 배경 위 보조 텍스트 대비를 지나치게 낮추지 않는다
3. 폰트 로딩 전에도 레이아웃이 크게 흔들리지 않는 폴백을 지정한다
4. `font-display:swap` 사용
5. 최종 공개는 CDN 의존도를 줄이고, 사용 권한이 확인된 방식으로 로드한다
6. 폰트 파일 자체는 저장소 공유 산출물에 포함하지 않는다
7. `prefers-reduced-motion`과 무관하게 텍스트는 즉시 읽을 수 있어야 한다

---

## 9. 금지

- 모든 본문을 명조체로 처리
- 영어 대문자 라벨의 과도한 자간
- 작은 글자를 고급스러움으로 착각하는 것
- 모바일에서 강제 `<br>`로 문장 조각내기
- 문단마다 다른 글꼴 또는 이탤릭 사용
- 본문 중앙 정렬 남발

---

## 10. 다음 구현

Claude 통합 단계에서 공통 파일로 분리한다.

```text
/assets/css/tokens.css
/assets/css/typography.css
/assets/css/components.css
```
