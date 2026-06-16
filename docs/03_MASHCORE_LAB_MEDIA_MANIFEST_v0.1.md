# 03_MASHCORE_LAB_MEDIA_MANIFEST_v0.1

- 문서 상태: `MEDIA PLANNING`
- 목표: 사진을 장식이 아니라 호흡·증거·기록으로 사용
- 1차 공개 권장 수량: 4장, 선택 1장

---

## 1. 프레임 유형

### Editorial Window

- 역할: 사유의 호흡과 장면 전환
- 비율: Desktop 16:10 / Mobile 4:3
- 사용처: Home, Reading, About
- 스타일: 모서리 최소, 얇은 황동선, 과한 그림자 없음

### Field Evidence

- 역할: 실제 현장과 관찰의 증거
- 비율: 4:3 또는 1:1 고정
- 사용처: Cases, Chore to Play 실제 사례
- 스타일: 동일 크롭·동일 밝기, 사실을 바꾸는 생성형 편집 금지

### Research Artifact

- 역할: 메모·스케치·문서·구버전 도식
- 비율: 원본 유지
- 사용처: Research Log, 연구 상태 직전
- 스타일: 파치먼트 매트, `object-fit:contain`, 날짜·버전 표기

---

## 2. 슬롯 목록

| ID | 페이지 | 위치 | 프레임 | 상태 | 필요한 이미지 |
|---|---|---|---|---|---|
| HOME-01 | Home | Lab이 읽는 것 다음 | Editorial Window | REQUIRED | 실제 작업대·메모·기록하는 손 |
| CTP-01 | Chore to Play | 식당 매니저 사례 다음 | Field Evidence | REQUIRED | 운영·예약·마감 등 다중 역할이 보이는 실제 장면 |
| CTP-02 | Chore to Play | Three Models 다음 | Research Artifact | REQUIRED | 최초 8단계 메모 또는 Audit 문서 일부 |
| ABOUT-01 | About | 최규현 소개 옆 | Editorial Portrait | REQUIRED | 4:5 작업·관찰 장면 |
| RESEARCH-01 | Research Index | Current Research 전후 | Editorial Window | OPTIONAL | 여러 연구 문서가 놓인 조용한 장면 |
| LOG-XX | Research Log | 개별 로그 펼침 | Research Artifact | CONDITIONAL | 해당 변경을 증명하는 실제 메모·문서 |

---

## 3. 파일명

```text
mcl-[page]-[subject]-[frame]-[number]-[width].webp
```

### 제안 파일명

```text
assets/images/home/mcl-home-research-desk-editorial-01-640.webp
assets/images/home/mcl-home-research-desk-editorial-01-960.webp
assets/images/home/mcl-home-research-desk-editorial-01-1600.webp

assets/images/research/chore-to-play/mcl-ctp-restaurant-manager-evidence-01-1200.webp
assets/images/research/chore-to-play/mcl-ctp-original-model-artifact-01-1200.webp

assets/images/about/mcl-about-mashcore-working-portrait-01-1200.webp

assets/images/og/og-home-1200x630.jpg
assets/images/og/og-chore-to-play-1200x630.jpg
assets/images/og/og-research-log-1200x630.jpg
```

---

## 4. 사이즈

| 용도 | 폭 |
|---|---:|
| Mobile source | 640px |
| Tablet / normal content | 960px |
| Wide editorial | 1600px |
| OG | 1200×630 |

- 기본 포맷: WebP
- 사진 폴백: JPEG
- 투명 자료·문서 캡처: PNG 또는 WebP lossless
- 원본 고해상도 및 고객 비공개 자료는 공개 GitHub에 넣지 않는다

---

## 5. Alt text 초안

### HOME-01

> 어두운 작업대 위에 Chore to Play의 단어와 수정 메모가 펼쳐져 있다.

### CTP-01

> 식당 운영자가 예약과 현장 상황을 확인하며 여러 업무를 동시에 조율하는 장면.

실제 사진이 정해지면 보이는 사실만 다시 적는다. 사진에 없는 철학을 alt에 넣지 않는다.

### CTP-02

> Chore에서 Play까지 여덟 단어를 한 줄로 배열했던 초기 연구 메모.

### ABOUT-01

> 최규현이 작업대에서 문서와 화면을 함께 보며 기록을 수정하는 장면.

---

## 6. 캡션 초안

### HOME-01

```text
OBSERVATION 01
처음의 순서가 무너진 자리에서 다음 질문이 시작됐습니다.
```

### CTP-01

```text
FIELD NOTE
한 사람의 하루 안에서 Job, Role, Duty와 Responsibility는 동시에 움직입니다.
```

### CTP-02

```text
RESEARCH ARTIFACT · v0.1
한 줄로 세웠던 최초 가설. 현재는 원전으로 보존합니다.
```

### ABOUT-01

캡션 없이 사용할 수 있다. 필요하다면:

```text
읽고, 구조화하고, 현장에 놓고, 다시 수정합니다.
```

---

## 7. 보정 규칙

### Editorial

- 채도 소폭 감소
- 따뜻한 암부 통일
- 약한 필름 입자 가능
- 인위적인 주황·청록 색보정 금지

### Evidence

- 수평·밝기·색온도만 정리
- 개인정보 가림 허용
- 없던 물건 추가, 전후 차이 과장 금지

### Artifact

- 원문 가독성 우선
- 문서 가장자리를 지나치게 자르지 않음
- 날짜·버전·출처를 캡션에 기록

---

## 8. GitHub 공개 기준

공개 저장소에 넣는 것:

- 리사이즈·최적화 완료본
- 공개 허가 확인본
- 개인정보 제거본
- 실제 페이지에서 사용되는 파일

넣지 않는 것:

- RAW 원본
- 고객 개인정보
- 비공개 연구 원전
- 생성 과정의 전체 후보
- 사용하지 않는 대용량 이미지

---

## 9. 현재 필요한 사용자 입력

1. About 4:5 작업 장면 후보
2. Home 작업대·메모 사진 후보
3. Chore to Play 현장 사진을 실제 사례로 할지 연출 사진으로 할지 결정
4. 최초 8단계 메모를 이미지로 만들 원본 선택
5. 외부 공개가 가능한지 각 사진 권리 확인
