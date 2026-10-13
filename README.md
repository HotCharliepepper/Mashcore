# Mashcore Lab

사람·브랜드·공간·관계·기술의 신호를 읽는 공개 연구 홈페이지.

## Editorial Research v3

`Mashcore_Editorial_Review_v2`의 편집 디자인과 기존 저장소의 연구 콘텐츠를 통합한 검토 버전입니다. 디자인 결정·근거·검수 한계는 [DESIGN.md](DESIGN.md), 기존 Figma 파일과의 인계는 [FIGMA_HANDOFF_v3.md](docs/FIGMA_HANDOFF_v3.md)에 기록합니다.

| 경로 | 내용 |
|---|---|
| `/` | 관점 탐색·현재 연구·글 초안·질문 정리 |
| `/research/` | 연구 전체와 방법·열린 질문 |
| `/research/chore-to-play/` | 일의 상태와 조건 탐색 |
| `/research/market-interpretation/` | 판단력 교육 R&D |
| `/research/log/` | 공개된 연구 변경 기록 |
| `/about/` | Mashcore Lab·Weplace·Mashcore34의 역할 |

빌드가 필요 없는 HTML/CSS/JavaScript입니다. 모든 공개 페이지는 상대 경로를 사용합니다. 현재 운영 호스트는 `https://mashcore.netlify.app/`이며, Netlify에 연결된 `main` 병합이 운영 배포 경로입니다.

```sh
python3 scripts/check_site.py
node --check assets/js/site.js
```

외부 JavaScript 런타임과 Tailwind Play CDN을 사용하지 않습니다. Google Fonts가 차단되어도 시스템 폰트로 읽을 수 있습니다. 질문 작성은 브라우저 로컬에서만 처리하며, 복사 또는 사용자 메일 앱을 통한 직접 전송을 선택합니다.

`docs/01`–`05`는 이전 디자인·구현 이력이며 현재 구현 기준은 루트 `DESIGN.md`입니다.
