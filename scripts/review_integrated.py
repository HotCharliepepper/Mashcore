"""Public review-only content for LAB, NOTES and SIGNAL STUDIO.

Do not add customer originals, Ledger details, internal research files, or
unapproved media. Editorial labels describe current evidence, not results.
"""
from pathlib import Path

MARKET_ORIGINAL = "https://mashcore-market-notes.netlify.app/"


def research_bridge():
    return """
<div class="mc-bridge mc-bridge--research chapter-inner" aria-labelledby="mc-research-title">
  <div class="mc-bridge-heading"><p class="core-overline">MASHCORE / LAB &amp; NOTES</p>
    <h2 id="mc-research-title">멈춘 장면 하나에서,<br>판단의 근거까지.</h2>
    <p>무엇을 보았고, 무엇은 아직 모르는지. 관찰과 해석, 다른 설명을 구분하면 다음에 확인할 질문이 남습니다.</p>
  </div>
  <div class="mc-bridge-links">
    <a class="mc-feature-link" href="/research/lab/"><span>01 / LAB · 판단 방법</span><strong>고객은 왜 같은 정보를 다시 확인할까요?</strong><small>관찰 → 근거 → 해석 → 반례 → 다음 판단</small><em>연구 방법 살펴보기 ↗</em></a>
    <a class="mc-feature-link" href="/research/notes/"><span>02 / NOTES · 공개 원문</span><strong>하나의 질문을 끝까지 읽습니다.</strong><small>연구 원문과 작성 시점이 표시된 Market Notes</small><em>노트와 원문 보기 ↗</em></a>
  </div>
  <p class="mc-bridge-caution">관찰 A/B는 정보 배치를 비교하는 화면입니다. 사람의 성격·전환 효과를 판정한 실험 결과가 아닙니다.</p>
</div>"""


def field_bridge():
    return """
<div class="mc-bridge mc-bridge--field chapter-inner" aria-labelledby="mc-field-title">
  <div class="mc-bridge-heading"><p class="core-overline">FROM SIGNAL TO SURFACE</p>
    <h2 id="mc-field-title">판단의 이유가,<br>실제로 쓸 결과물이 되도록.</h2>
    <p>설계와 실행, 제품 지원의 책임을 구분합니다. 무엇을 바꾸는지뿐 아니라 왜 그 순서인지 설명합니다.</p>
  </div>
  <div class="mc-path-grid">
    <article><span>01 / MASHCORE</span><h3>고객의 질문을 읽고</h3><p>고객이 다시 확인하는 지점과 필요한 정보의 순서를 살펴, 문안·홈페이지 구조·실행 기준으로 설계합니다.</p><a href="/services/#service-axes">설계 범위 보기 ↗</a></article>
    <article><span>02 / WEPLACE</span><h3>현장의 접점을 정리하고</h3><p>별도 협업 범위에서 지도 정보, 사진, FAQ, 홈페이지 등 실제 고객이 만나는 표면에 적용합니다.</p><a href="/work/weplace/">독립적인 현장 협업 보기 ↗</a></article>
    <article><span>03 / SIGNAL STUDIO</span><h3>첫 콘텐츠를 준비합니다</h3><p>대표의 가게 설명과 실제 사진으로 글·사진 기반 영상·게시 안내를 만드는 로컬 검토 도구입니다.</p><a href="/signal-studio/">제작 과정과 현재 상태 보기 ↗</a></article>
  </div>
  <p class="mc-bridge-caution">위 흐름은 업무의 관계를 설명합니다. 한 회사·통합 계약·공통 고객 DB 또는 검증된 매출 성과를 뜻하지 않습니다.</p>
</div>"""


LAB = """
<section class="core-about-hero mc-detail-hero" aria-labelledby="lab-title"><div class="core-wrap">
  <p class="core-overline">MASHCORE LAB / 관찰과 해석</p>
  <h1 id="lab-title">무엇을 보고,<br>어떻게 판단하는가.</h1>
  <p class="core-lead">고객은 언제 다시 검색하고, 어떤 정보에서 멈출까요? 하나의 장면을 결론으로 단정하기보다, 근거와 반대 설명을 함께 살펴봅니다.</p>
  <nav class="mc-inline-nav" aria-label="연구 탐색"><a href="#method">판단의 순서 ↓</a><a href="#example">하나의 장면 ↓</a><a href="/research/notes/">노트 읽기 ↗</a></nav>
</div></section>
<section class="core-band mc-detail-section" id="method" aria-labelledby="lab-method-title"><div class="core-wrap">
  <p class="core-overline">A METHOD IN REVIEW</p><h2 id="lab-method-title">한 번의 관찰을,<br>다음 선택의 기준으로.</h2>
  <p class="core-lead">아래는 MASHCORE가 연구를 기록하는 방법입니다. 특정 고객 행동의 원인이나 전환율을 이미 검증했다는 뜻은 아닙니다.</p>
  <ol class="mc-method-steps">
    <li><span>01 / 관찰</span><h3>실제로 보인 것은?</h3><p>질문·화면·동선·말·시점을 기록하고 재구성과 구분합니다.</p></li>
    <li><span>02 / 근거</span><h3>어디에서 확인할 수 있나?</h3><p>원문, 운영 조건, 반복 질문 등 확인 가능한 자료를 찾습니다.</p></li>
    <li><span>03 / 해석</span><h3>어떤 설명이 가능한가?</h3><p>가능한 원인을 가설로 적고, 사실처럼 확정하지 않습니다.</p></li>
    <li><span>04 / 반례</span><h3>다른 이유는 없을까?</h3><p>조건·시점·선택권 등 다른 설명과 생각을 바꿀 조건을 남깁니다.</p></li>
    <li><span>05 / 다음 판단</span><h3>무엇을 작게 바꿀까?</h3><p>정보·문장·운영 방식을 조정하고 실제 반응을 다시 확인합니다.</p></li>
  </ol>
</div></section>
<section class="core-band mc-example-band" id="example" aria-labelledby="lab-example-title"><div class="core-wrap mc-split">
  <div><p class="core-overline">재구성한 설명 예시</p><h2 id="lab-example-title">“주차는 어디에 하나요?”</h2><p class="core-lead">방문 전 주차를 다시 확인한다면, 안내가 찾기 어려운 걸까요? 주차 여건이 불확실한 걸까요?</p><p>같은 질문에도 가능한 이유는 여럿입니다. 실제 안내·주차 조건·반복되는 문의를 대조한 뒤 문구와 위치를 바꿀지 판단합니다.</p><p class="core-note">실제 고객 사례·관측 수치가 아닌 가상 상황 설명입니다.</p></div>
  <dl class="mc-evidence-card"><div><dt>관찰할 신호</dt><dd>방문 전 반복되는 주차 문의</dd></div><div><dt>가설</dt><dd>안내 정보가 눈에 띄지 않거나 조건이 이해되지 않을 수 있음</dd></div><div><dt>반대 설명</dt><dd>정보가 충분해도 실시간 주차 가능 여부를 확인하려 할 수 있음</dd></div><div><dt>다음 확인</dt><dd>안내 변경 전후의 질문 종류와 실제 이용 조건 비교</dd></div></dl>
</div></section>
<section class="core-band mc-detail-section" aria-labelledby="lab-model-title"><div class="core-wrap">
 <p class="core-overline">연구 참고 / 아직 검증 전</p><h2 id="lab-model-title">이론을 빌리되,<br>판단은 현장에서 다시 묻습니다.</h2>
 <p class="core-lead">한스-게오르크 호이젤의 Limbic® 접근은 연구 참고입니다. Mashcore는 안심을 위해 확인하는 것, 선택하고 싶은 것, 더 알아보고 싶은 것을 현장 질문으로 살펴보는 독자 모델 v0.1을 검토 중입니다.</p>
 <p class="core-note">이 질문들은 원전의 표준 검사 문항이나 검증된 성격 분류·동기 예측기가 아닙니다. 색·표정·체류만으로 사람의 마음을 판정하지 않습니다. 자료와 반례에 따라 기준을 갱신합니다.</p>
 <div class="mc-related"><a href="/research/chore-to-play/">Chore to Play · 여섯 동시 관점 ↗</a><a href="/research/market-interpretation/">Market Interpretation · 판단의 조건 ↗</a><a href="/research/log/">연구 변경 기록 ↗</a><a href="/research/notes/">공개 노트 ↗</a></div>
</div></section>
<section class="core-band mc-detail-end"><div class="core-wrap"><h2>어떤 장면이 반복되나요?</h2><p>확인해야 할 질문과 다음에 바꿀 표면을 함께 정할 수 있습니다.</p><a class="core-button" href="/#invitation">내 상황 이야기하기 ↗</a></div></section>
"""

NOTES = """
<section class="core-about-hero mc-detail-hero" aria-labelledby="notes-title"><div class="core-wrap">
 <p class="core-overline">MASHCORE NOTES / 읽히는 연구</p>
 <h1 id="notes-title">질문을 남기고,<br>근거를 잇습니다.</h1>
 <p class="core-lead">관찰과 해석은 다릅니다. 언제 무엇을 보았는지, 어떤 설명이 가능한지, 무엇이 나오면 판단을 바꿀지 원문과 함께 읽습니다.</p>
 <nav class="mc-inline-nav" aria-label="노트 목록"><a href="#market-note">시장 노트 ↓</a><a href="#research-reading">공개 연구 ↓</a><a href="/research/lab/">LAB 방법 ↗</a></nav>
</div></section>
<section class="core-band mc-detail-section" id="market-note" aria-labelledby="market-notes-title"><div class="core-wrap">
 <p class="core-overline">MARKET NOTES / 과거 원문 연결</p><h2 id="market-notes-title">시장 신호를 읽은 기록.</h2>
 <p class="core-lead">기존 Market Notes 원문은 독립 사이트에 보존합니다. 여기에는 작성 시점과 주제를 안내하며, 현재 시장 데이터나 매매 판단으로 갱신한 것처럼 표시하지 않습니다.</p>
 <article class="mc-editorial-card"><div><span class="mc-card-kind">2026.05.11 · 기존 정적 리포트</span><h3>NEAR 시나리오 리포트 — BTC가 신고가일 때 NEAR는 어디 있었나</h3><p>해당 시점의 시장 시나리오를 다룬 보존 원문입니다. 현재 가격·전망의 정확성은 이번 홈페이지 작업에서 재검증하지 않았습니다.</p><a class="core-text-link" href="https://mashcore-market-notes.netlify.app/" rel="noopener noreferrer">기존 Market Notes 원문 읽기 ↗</a></div><p class="mc-card-label">ORIGINAL / 외부 원문</p></article>
</div></section>
<section class="core-band mc-example-band" id="research-reading" aria-labelledby="notes-reading-title"><div class="core-wrap">
 <p class="core-overline">READ THE SOURCE</p><h2 id="notes-reading-title">이미 공개된 연구에서<br>더 깊이 읽습니다.</h2>
 <div class="mc-reading-grid">
  <article><span>RESEARCH / 진행 중</span><h3>Chore to Play</h3><p>일을 여섯 관점에서 동시에 봅니다. 능력 등급이나 성장 순서를 측정하는 검사가 아닙니다.</p><a href="/research/chore-to-play/">여섯 관점과 정적 설명 읽기 ↗</a></article>
  <article><span>RESEARCH / 방법론</span><h3>Market Interpretation</h3><p>시장 신호를 어떻게 해석하고, 어떤 근거가 바뀌면 기존 판단을 수정할지 살펴봅니다.</p><a href="/research/market-interpretation/">판단 방법 읽기 ↗</a></article>
  <article><span>LOG / 변경 기록</span><h3>연구 기록</h3><p>언제 무엇을 바꾸고 어떤 질문이 남았는지. 현재 공개된 기록을 따라 읽습니다.</p><a href="/research/log/">변경 이력 보기 ↗</a></article>
 </div>
 <p class="core-note">새로운 다중 노트 CMS나 자동 발행·실시간 뉴스 기능이 만들어졌다는 뜻이 아닙니다.</p>
</div></section>
<section class="core-band mc-detail-section"><div class="core-wrap mc-split">
 <div><p class="core-overline">NOTE EDITORIAL RULE</p><h2>주장 하나마다,<br>확인할 자리를 남깁니다.</h2><p class="core-lead">관찰 → 해석 → 출처·시점 → 반대 설명 → 생각을 바꿀 조건 → 지금 할 질문. 공개 허락을 받은 내용만 노트로 편집합니다.</p></div>
 <div class="mc-related mc-related--stack"><a href="/research/lab/">LAB 연구 방법 보기 ↗</a><a href="/explore/">기존 생각 기록 읽기 ↗</a><a href="/services/">함께할 수 있는 일 ↗</a><a href="/#invitation">질문 이야기하기 ↗</a></div>
</div></section>
"""

STUDIO = """
<section class="core-about-hero mc-detail-hero" aria-labelledby="studio-title"><div class="core-wrap">
 <p class="core-overline">MASHCORE SIGNAL STUDIO / OWNER FIRST</p>
 <h1 id="studio-title">가게 이야기에서,<br>첫 게시까지.</h1>
 <p class="core-lead">마케팅 도구를 배울 시간보다, 오늘 손님에게 전할 말이 먼저인 대표를 위한 콘텐츠 제작 흐름을 검토하고 있습니다.</p>
 <nav class="mc-inline-nav" aria-label="제품 소개 탐색"><a href="#studio-process">어떻게 만드나요? ↓</a><a href="#studio-status">현재 지원 범위 ↓</a><a href="/#invitation">제품에 관해 문의 ↗</a></nav>
</div></section>
<section class="core-band mc-detail-section" id="studio-process" aria-labelledby="studio-process-title"><div class="core-wrap">
 <p class="core-overline">ONE SHOP / ONE QUESTION / ONE POST</p><h2 id="studio-process-title">대표가 확인할 것은<br>가게의 실제 이야기입니다.</h2>
 <p class="core-lead">현재 R2.1 로컬 검토 흐름은 세탁업의 고객 질문 하나를 중심으로 글과 네 장면, 사진 기반 영상을 준비합니다. 실제 매장 파일은 이 공개 페이지에 받지 않습니다.</p>
 <ol class="mc-method-steps mc-studio-steps">
  <li><span>01 / 설명</span><h3>가게를 들려주세요.</h3><p>누구를 돕고, 어떤 서비스를 제공하는지 대표가 설명합니다.</p></li>
  <li><span>02 / 사실 확인</span><h3>맞는 말과 사진인가요?</h3><p>실제 사진의 출처와 안내할 사실을 확인합니다.</p></li>
  <li><span>03 / 초안</span><h3>손님의 질문에 답합니다.</h3><p>게시 글과 네 장면의 설명을 만들고 문구를 수정합니다.</p></li>
  <li><span>04 / 영상</span><h3>사진에 흐름을 더합니다.</h3><p>실사진 크롭·움직임과 한글 조판으로 사진 기반 MP4를 렌더합니다.</p></li>
  <li><span>05 / 게시 안내</span><h3>대표가 직접 확인합니다.</h3><p>현재 버전을 승인·내보내고, 직접 게시할 때 필요한 안내를 받습니다.</p></li>
 </ol>
</div></section>
<section class="core-band mc-example-band" id="studio-status" aria-labelledby="studio-status-title"><div class="core-wrap mc-split">
 <div><p class="core-overline">IMPLEMENTATION STATUS / 검토 단계</p><h2 id="studio-status-title">작동하는 부분과,<br>아직 검증할 부분.</h2><p class="core-lead">R2.1은 로컬 Gate 0 검토 구현입니다. 실제 사진 기반 샘플 MP4와 로컬 인증·저장·워커 코드가 있지만, 공개 유료 서비스나 원격 파일럿이 검증된 것은 아닙니다.</p><p class="core-note">현재 구현 기준: 세탁업 질문 1개, Instagram 릴스 1채널, 고정 템플릿, 로컬 MP4 렌더. 요식업·정육업 등은 확장 방향입니다.</p></div>
 <dl class="mc-evidence-card"><div><dt>확인된 범위</dt><dd>대표 설명·사실 확인·글·네 장면·수정·렌더·승인·내보내기 로컬 코드</dd></div><div><dt>결제</dt><dd>Mock 상태. 검수 금액은 실제 판매가가 아닙니다.</dd></div><div><dt>외부 생성 AI</dt><dd>유료 생성 영상·LLM·TTS API 미연결 또는 비활성</dd></div><div><dt>실제 SNS 게시</dt><dd>자동 게시 미구현. 실고객의 게시 완료·반복 사용은 미검증</dd></div></dl>
</div></section>
<section class="core-band mc-detail-section"><div class="core-wrap">
 <p class="core-overline">THE PURPOSE</p><h2>첫 게시에 필요한 질문을,<br>복잡한 편집보다 먼저.</h2>
 <p class="core-lead">대표가 확인해야 할 사실과 문구를 분명히 하고, 콘텐츠 제작에 필요한 단계를 줄이는 것이 목표입니다. 공개 페이지의 버튼은 실제 계정 생성·체험 시작·결제·게시 완료를 수행하지 않습니다.</p>
 <div class="mc-related"><a href="/research/lab/">LAB · 고객 질문의 판단 기준 ↗</a><a href="/research/notes/">NOTES · 공개 기록 ↗</a><a href="/work/weplace/">Weplace · 현장 접점 협업 ↗</a><a href="/services/">Mashcore 업무 범위 ↗</a></div>
 <a class="core-button mc-standalone-cta" href="/#invitation">제품 검토 의견 또는 제작 상황 이야기하기 ↗</a>
</div></section>
"""


PAGE_ITEMS = (
    ("research/lab", "Mashcore Lab — 관찰과 판단의 방법 | MASHCORE",
     "현장의 질문을 관찰하고 근거·해석·반례와 다음 판단을 구분하는 Mashcore Lab의 연구 방법을 소개합니다.", LAB),
    ("research/notes", "Mashcore Notes — 질문과 근거가 이어지는 기록 | MASHCORE",
     "공개된 연구와 작성일이 있는 Market Notes 원문을 연결합니다. 관찰·해석·출처·한계를 나누어 읽어보세요.", NOTES),
    ("signal-studio", "Signal Studio — 가게 설명에서 첫 게시 준비까지 | MASHCORE",
     "실제 가게 설명과 사진으로 게시 글·사진 기반 영상·게시 안내를 준비하는 Signal Studio R2.1 로컬 검토 흐름과 한계.", STUDIO),
)


def render_review_pages(output: Path, business: dict, page, review: bool = True):
    """Generate only public editorial review HTML, never customer workspaces."""
    for segment, title, description, body in PAGE_ITEMS:
        dest = output / segment / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page("/" + segment + "/", title, description, body, business, review=review), encoding="utf-8")
