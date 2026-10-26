# PR #6 — R2 시작 전 본문 보존

HEAD `4cd7504878f3118e876beb179f490a141a0e5b61`, Draft/open, main `b31a55cea32cd83113624f9cdc27bd8d8bc36926`.

홈 첫 화면을 사람의 멈춤과 현장 질문에서 시작하는 Experience R1으로 구현했습니다. 포스터를 첫 HTML에서 즉시 표시하고 얇은 가로선·↓로 연구에 이어지며, 홈·서비스·소개·연구·Weplace 협업 상세의 문안과 정보 밀도를 v0.2 기준으로 정리했습니다.

최종 영상은 미제공입니다. 기존 문 앞 인물 SVG를 편집한 포스터에 “히어로 구도 시안 · 실제 촬영 아님”을 표시하고, 미승인 자산 상태를 설정에 남겼습니다. 영상 경로는 null이며 빈 플레이어가 생성되지 않습니다. 실제 영상이 연결되면 playing 이후 전환, 수동 정지, 환경 정지, 종료/다시 보기, 오류와 모션 감소 상태를 처리합니다.

## 검토 위치와 정확한 커밋

- 화면 검토: https://deploy-preview-6--mashcore.netlify.app/preview/?view=desktop&page=%2F
- 최종 검토 HEAD: `4cd7504878f3118e876beb179f490a141a0e5b61`
- R1 구현 커밋: `2585b11b5d59c1b6ef43d49b9b55523242e5f365`
- 변경 전 PR #6: `a3c81d821f4bcbe542bb0aee332a1803fd8ae8a4`
- 최종 Netlify deploy: `6ade094f2dddd1db23a7c889` — ready / deploy-preview / commit_ref가 최종 HEAD와 일치 / published_at null.
- 구현 커밋 고정 배포: https://6ade057424cd7fdda7398c2e--mashcore.netlify.app/
- [검토 기록과 미실시 항목](https://github.com/HotCharliepepper/Mashcore/blob/4cd7504878f3118e876beb179f490a141a0e5b61/docs/EXPERIENCE_R1_REVIEW_20261025.md)
- [원본 캡처 13장·커밋/viewport/해시 목록](https://chatgpt.com/library?file_id=libfile_80b476cd86b88191ae8033d966581340&account_id=personal)

최종 HEAD는 구현 커밋에 검수 자료와 재현용 검사만 추가합니다. assets/content/scripts/research/work/netlify.toml의 변경은 없습니다. GitHub 연결의 tree/commit/ref API로 기존 HEAD를 부모로 보존하고 force:false로 갱신했습니다.

## 검수 결과

- 정적 검사: 12 HTML, 11 사업자 푸터, 362 로컬 참조 PASS. R1 단일 원본·포스터·공개 산출물 제외 검사 PASS.
- 기존 문의/A·B 9개 묶음 + 3D 9개 묶음 PASS (Node VM/linkedom).
- 실제 Chromium: 11경로×4폭 44개 + 390px 글자 200% 11개 + JS 비활성 3개 = 58/58 PASS.
- 실제 Chromium 미디어·문의·A/B: 21/21 PASS. 영상은 별도 TEST FIXTURE이며 자동재생 거부·모션 선호·visibility는 명시적 주입입니다. 종료 후 준비 상태를 기다리지 못하던 재재생 결함을 수정하고 재검수했습니다.
- 실제 키보드 메뉴 Enter/Escape·초점 복귀, A/B Space, ↓와 서비스 앵커, Field→협업 상세→서비스, 복사 실패 대안·메일 URI 확인.
- 원격: 12 HTML + 7 자산 HTTP 200/내용 일치, 내부 5경로 404 = 24개 PASS. 정확한 Netlify preview toolbar만 제외해 비교했습니다. 최종 배포의 홈도 같은 검수 출력과 일치합니다.
- 원격 화면에서 홈·↓·A/B·서비스를 조작하고 캡처했습니다. 상세 로그: `docs/qa/r1/`.

## 보존과 남은 검토

기존 A/B 원문·노드, 여섯 동시 관점/3D와 정지 대안, 문의·1,001자 원문 보존, 사업자·정책·두 가격 트랙·PROPOSED/VAT 미정 상태를 보존했습니다. 기존 JS 5개와 상품 JSON은 기준 커밋과 바이트가 같습니다.

최종 영상·권리/동의, 실기기/센서/스크린리더, 실제 OS 모션 감소·save-data·배경 탭, 느린 네트워크/최종 영상 디코딩, 브라우저 자체 200% zoom, 외부 메일 앱/SMTP, 사용자 인상·전환율 검사는 NOT RUN입니다. 글자 확대와 브라우저 zoom, 테스트 클립과 최종 자산을 구분합니다.

PR #2는 그대로 open Draft이며 열린 후속 PR을 재확인했습니다. main은 `b31a55cea32cd83113624f9cdc27bd8d8bc36926`, 운영 deploy는 `6adb113e296767181eb98f02`로 유지됩니다. main 병합·운영 배포·DNS·DB·Weplace 독립 사이트 변경은 하지 않았습니다. noindex와 미승인 production 차단을 유지합니다. 문안·CI·가격·공개 승인으로 간주하지 않으며 화면 피드백에 따라 이 Draft에서 수정합니다.
