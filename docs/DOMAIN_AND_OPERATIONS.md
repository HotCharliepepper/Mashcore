# 도메인·사업자 정보 운영

## 현재 상태

- 운영 대상: https://mashcore.netlify.app
- 계획 도메인: https://mashcore.kr
- 2026-10-14 KST 공개 DNS 조회에서 mashcore.kr은 NXDOMAIN. 도메인 등록·소유권 여부는 확인하지 못했다.
- 현재 연결된 Netlify 도구에는 custom domain/DNS 변경 기능이 없다. 도메인 설정·구매·HTTPS 발급은 완료하지 않았다.
- GitHub main 병합 → 기존 Netlify Git CD. 별도 수동 운영 배포로 연결을 바꾸지 않는다.

## 도메인 연결 순서

1. 등록업체에서 mashcore.kr이 본인 소유로 등록되었는지 확인한다.
2. Netlify mashcore → Domain management → Add a domain → Add a domain you already own → mashcore.kr.
3. Netlify가 보여주는 해당 도메인의 Pending DNS verification 안내를 우선 적용한다.
4. 외부 DNS를 쓸 때 일반적인 레코드는 아래와 같다. 기존 메일용 MX/TXT를 변경하지 않는다.

| 이름 | 방식 | 대상 |
|---|---|---|
| @ | ALIAS / ANAME / flattened CNAME 지원 시 | apex-loadbalancer.netlify.com |
| @ | 위 방식이 없을 때 A | 75.2.60.5 |
| www | CNAME | mashcore.netlify.app |

@ 레코드는 두 방식 중 지원되는 하나를 선택한다. DNS 전파와 Netlify HTTPS 인증서가 완료된 뒤 최종 primary domain을 mashcore.kr로 설정하고 www 리디렉션을 확인한다.

5. mashcore.kr에서 홈·연구·모바일·자산이 HTTPS로 정상 응답하는지 확인한 후, 저장소 HTML의 canonical/og:url/JSON-LD URL과 sitemap.xml/robots.txt의 호스트를 https://mashcore.kr로 변경한다. `/mobile/`은 루트 canonical을 계속 공유한다. `/preview/`는 noindex를 유지한다.
6. 정적 검사 후 커밋·배포하고 실제 리디렉션·canonical을 확인한다.

공식 문서 (확인 2026-10-14 KST):
- https://docs.netlify.com/manage/domains/manage-domains/assign-a-domain-to-your-site-app/
- https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/

## 사업자 정보 바로 입력

`assets/js/site-config.js`의 `companyName`, `representative`, `registrationNumber`, `address`, `phone`을 실제 등록 내용으로 채운다. 현재는 모두 빈 문자열이다. 푸터가 이 파일을 공유하므로 페이지별로 다시 입력할 필요가 없다. 빈 필드는 표시하지 않고, 입력값은 HTML 실행 없이 텍스트로 표시한다. 공개 정보만 넣고 비밀키·주민번호 등은 넣지 않는다.

## 운영 확인

- 센서: 휴대폰에서 `/mobile/#research`를 직접 열고 “기울기로 살펴보기”를 눌러 허용한다. 기울기는 시점만 바꾸며 실제 중력 물리 시뮬레이션이나 진단이 아니다.
- 비교: `/preview/?view=desktop`, `/preview/?view=mobile`. 비교 iframe은 화면 구성 확인용이며 센서는 새 창에서 검토한다.
- 문의: 자동 서버 전송 기능이 없다. 이메일 앱에서 초안을 확인하고 사용자가 직접 보낸다. 기존 연락처 weplace25@gmail.com을 유지했다.
- 기록: 실제 반응, 읽기/문의에서 막힌 부분, 모션 피로 여부를 DESIGN.md에 근거와 함께 축적한다. 미측정 성과를 수치로 기록하지 않는다.

## 2026-10-23 확인 및 결제심사 준비

- Netlify `mashcore` 프로젝트가 보고한 **현재 primarySiteUrl은 `https://mashcore.co.kr`**. 위 2026-10-14의 `mashcore.kr` 계획은 과거 기록이며 운영 주소로 해석하지 않는다.
- 현재 홈페이지 연락 이메일은 `weplace25@gmail.com`이고, Mashcore 전용 주소의 유효 여부는 NEED VERIFY.
- `assets/js/site-config.js`의 상호·대표자·사업자등록번호·주소·전화가 비어 있으므로 실제 서류 확인 후 공개할 것. 값을 임의로 채우지 않는다.
- `/policies/refund/`와 `/services/`는 정책과 상품 안내 경로이다. 결제창 기능은 아직 구축·개통 전이며, PG 심사에 상품 제공 기간·VAT·범위·상품별 상세정보와 결제 테스트 경로가 추가로 필요하다.
- 진행 중 카드사 심사가 있다면 푸터 사업자 정보, 상품 분류와 결제 경로를 잦게 변경하기 전에 토스페이먼츠 담당자와 확인한다.
