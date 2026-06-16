# 04_MASHCORE_LAB_LINK_MAP_v0.1

- 문서 상태: `IMPLEMENTED DRAFT`
- 목적: 다섯 HTML이 커스텀 도메인과 GitHub 프로젝트 페이지에서 모두 이동 가능하도록 연결
- 구현 원칙: 루트 절대경로(`/research/`) 대신 페이지별 상대경로 사용

---

## 1. 페이지 구조

```text
/
├─ index.html
├─ research/
│  ├─ index.html
│  ├─ chore-to-play/
│  │  └─ index.html
│  └─ log/
│     └─ index.html
└─ about/
   └─ index.html
```

---

## 2. 공용 내비게이션 라벨

```text
MASHCORE LAB
연구
연구 기록
소개
```

| 라벨 | 목적지 |
|---|---|
| MASHCORE LAB | Home |
| 연구 | Research Index |
| 연구 기록 | Selected Research Log |
| 소개 | About |

현재 페이지는 `aria-current="page"`로 표시한다.

---

## 3. 페이지별 상대경로

### Home `/index.html`

| 목적지 | 경로 |
|---|---|
| Home | `./` |
| Research | `./research/` |
| Chore to Play | `./research/chore-to-play/` |
| Research Log | `./research/log/` |
| About | `./about/` |
| Mashcore34 설명 | `./about/#mashcore34` |
| Weplace 설명 | `./about/#weplace` |

### Research Index `/research/index.html`

| 목적지 | 경로 |
|---|---|
| Home | `../` |
| Research | `./` |
| Chore to Play | `./chore-to-play/` |
| Research Log | `./log/` |
| About | `../about/` |
| Mashcore34 설명 | `../about/#mashcore34` |
| Weplace 설명 | `../about/#weplace` |

### Chore to Play `/research/chore-to-play/index.html`

| 목적지 | 경로 |
|---|---|
| Home | `../../` |
| Research | `../` |
| Chore to Play | `./` |
| Research Log | `../log/` |
| About | `../../about/` |
| Mashcore34 설명 | `../../about/#mashcore34` |
| Weplace 설명 | `../../about/#weplace` |

### Research Log `/research/log/index.html`

| 목적지 | 경로 |
|---|---|
| Home | `../../` |
| Research | `../` |
| Chore to Play | `../chore-to-play/` |
| Research Log | `./` |
| About | `../../about/` |
| Mashcore34 설명 | `../../about/#mashcore34` |
| Weplace 설명 | `../../about/#weplace` |

### About `/about/index.html`

| 목적지 | 경로 |
|---|---|
| Home | `../` |
| Research | `../research/` |
| Chore to Play | `../research/chore-to-play/` |
| Research Log | `../research/log/` |
| About | `./` |
| Mashcore34 설명 | `#mashcore34` |
| Weplace 설명 | `#weplace` |

---

## 4. 본문 브리지

### Home 끝

- `연구 전체 지도` → Research Index
- `Mashcore Lab 소개` → About

### Research Index 끝

- `Chore to Play` → 상세 연구
- `연구 변경 기록` → Research Log

### Chore to Play 끝

- `이 연구의 변경 기록` → Research Log
- `연구 전체 지도로 돌아가기` → Research Index

### Research Log 끝

- `현재 연구 지도에서 다시 읽기` → Chore to Play
- `다른 연구 질문 보기` → Research Index

### About 끝

- `현재 진행 중인 연구` → Research Index
- `첫 번째 연구 바로 읽기` → Chore to Play

---

## 5. About 내부 앵커

```text
/about/#weplace
/about/#mashcore34
```

- Weplace와 Mashcore34의 외부 URL이 확정되기 전에는 About의 역할 설명으로 연결한다.
- 외부 URL 확정 후 Footer 링크만 교체하고 본문 내부 앵커는 유지한다.

---

## 6. 아직 확정되지 않은 연결

| 항목 | 현재 처리 | 최종 필요 |
|---|---|---|
| 내 사례 남기기 | About로 이동 | Google Form 또는 자체 폼 URL |
| 반례 제보하기 | About로 이동 | Form endpoint |
| 연구 인터뷰 참여 | About로 이동 | 예약 또는 이메일 URL |
| Weplace | About 내부 설명 | 공식 외부 URL |
| Mashcore34 | About 내부 설명 | 출간·프로젝트 페이지 URL |
| Contact | 공용 Footer에서 임시 제거 | 대표 이메일 또는 연결 페이지 |

가짜 주소나 빈 `href="#"`를 사용하지 않는다.

---

## 7. GitHub Pages 호환 규칙

1. 상대경로를 사용해 `username.github.io/repository/`에서도 작동하도록 한다.
2. 디렉터리 링크는 끝에 `/`를 붙인다.
3. 로컬 검수는 파일 직접 열기보다 간단한 HTTP 서버로 수행한다.
4. 커스텀 도메인 연결 후에도 상대경로를 유지한다.
5. 향후 빌드 시스템 도입 시 `<base>` 태그를 임의로 추가하지 않는다.

로컬 검수 예:

```bash
python -m http.server 8080
```

---

## 8. 구현 상태

이 문서와 함께 제공되는 `mashcore-lab-p2` HTML에는 다음이 반영되어 있다.

- 다섯 페이지 공용 내비게이션 목적지
- 로고 Home 링크
- 핵심 CTA 실제 경로
- 페이지 하단 `다음 읽기` 브리지
- About의 Weplace / Mashcore34 내부 앵커
- Footer의 내부 연결
- `href="#"` 제거 또는 실제 섹션 앵커로 교체

텍스트·타이포·사진의 전면 통합은 다음 단계에서 진행한다.
