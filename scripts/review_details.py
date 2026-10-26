"""Review-only page compositions from 08. Copy/layout remain PROPOSED.

Catalog amounts, scope and approval flags are rendered by the existing public
generator. Main's separate price text is preserved in a source-only fragment.
"""
from html import escape
from pathlib import Path
from review_r2 import worksheet

ROOT = Path(__file__).resolve().parents[1]


def render_services(c: dict, product_renderer, services_renderer) -> str:
    """Return the services main body; product_renderer is kept for integration."""
    axes = [
        ('신호 해석', '무엇이 달라졌고, 무엇을 더 확인해야 할까요?', '관찰 기록, 가능한 설명, 우선 확인 질문'),
        ('사업 구조', '누구에게 어떤 가치를 제공할까요?', '고객·가치·제공 방식과 실행 우선순위'),
        ('고객 분석', '고객은 무엇을 다시 확인하고 있나요?', '고객 질문, 접점 지도, 확인 계획'),
        ('영업 설계', '다음 대화로 이어지려면 무엇을 먼저 말해야 할까요?', '상담 질문, 제안 순서, 후속 대화 기준'),
        ('디지털 요구사항', '화면과 업무에 무엇이 먼저 필요할까요?', '정보 구조, 기능 요구사항, 완료 판단 기준'),
        ('학습과 회고', '바꾼 뒤 무엇을 유지하고 고칠까요?', '결정 기록, 관찰 결과, 다음 실행'),
    ]
    axis_html = ''.join(f'''<article class="review-axis" id="axis-{i}"><p class="core-overline">0{i} / {escape(name)}</p><h3>{escape(question)}</h3><p class="core-result"><span>남기는 것의 예시</span>{escape(output)}</p></article>''' for i, (name, question, output) in enumerate(axes, 1))
    process = ['상황 듣기', '자료와 질문 정리', '함께할 범위 합의', '설계·실행', '함께 확인']
    process_html = ''.join(f'<li><span>0{i}</span><p>{step}</p></li>' for i, step in enumerate(process, 1))
    main_prices = (ROOT / 'content/services-main-review.html').read_text(encoding='utf-8')
    prototype = services_renderer(c)
    return f'''
<section class="core-about-hero review-detail-hero" aria-labelledby="services-hero-title"><div class="core-wrap">
  <p class="core-overline">함께할 수 있는 일</p>
  <h1 id="services-hero-title">무엇부터 바꿀지,<br>함께 정합니다.</h1>
  <p class="core-lead">사업의 방향, 고객에게 건네는 말, 홈페이지와 상담의 흐름. 지금 가진 경험과 자료를 살펴, 필요한 일과 남길 결과물을 정합니다.</p>
  <div class="core-hero-actions"><a class="core-button core-button-light" href="/#invitation">함께할 범위 이야기하기 <span aria-hidden="true">↗</span></a><a class="core-hero-secondary" href="#service-axes">어떤 일을 함께하나요? ↓</a></div>
  <ul class="review-situations"><li><a href="#axis-2">방향을 정하고 싶습니다. <span aria-hidden="true">↓</span></a></li><li><a href="#axis-3">좋은 점이 더 잘 전해졌으면 합니다. <span aria-hidden="true">↓</span></a></li><li><a href="#axis-5">실행할 기준이 필요합니다. <span aria-hidden="true">↓</span></a></li></ul>
</div></section>
<section class="core-band" id="service-axes" aria-labelledby="service-axes-title"><div class="core-wrap">
  <div class="core-section-heading"><div><p class="core-overline">질문과 남기는 것</p><h2 id="service-axes-title">지금의 질문에서,<br>필요한 일을 찾습니다.</h2></div><p class="core-lead">여섯 가지는 함께 다룰 일을 설명하는 분류입니다. 상황에 맞는 축을 연결하고, 실제 범위와 결과물을 정합니다.</p></div>
  <div class="review-axes">{axis_html}</div>
  <p class="core-note">위 결과물은 설명을 위한 예시입니다. 모든 계약에 전부 포함되는 목록이나 여섯 개의 유료 패키지가 아닙니다.</p>
</div></section>
<section class="core-band core-example" aria-labelledby="outputs-title"><div class="core-wrap">
  <p class="core-overline">무엇이 남나요?</p><h2 id="outputs-title">다음 선택에 다시 꺼내 볼 기준.</h2>
  <p class="core-lead">질문·확인 자료·선택 방향·다음 실행을 한 장에서 다시 볼 수 있게 정리합니다.</p>
  {worksheet()}
</div></section>
<section class="core-band" aria-labelledby="process-title"><div class="core-wrap"><p class="core-overline">함께 일하는 과정</p><h2 id="process-title">기대와 범위를 맞춘 뒤 시작합니다.</h2><ol class="review-process">{process_html}</ol><p class="core-note">기간·회차·수정 횟수·담당 역할은 필요한 일과 자료를 확인한 뒤 합의합니다.</p></div></section>
<section class="core-band review-pricing-intro" aria-labelledby="price-tracks-title"><div class="core-wrap"><p class="core-overline">상품 구성 검토</p><h2 id="price-tracks-title">두 상품안을 비교 중입니다.</h2><p class="core-lead">금액과 범위는 아래 검토 상태를 함께 확인해 주세요. 같은 금액이어도 서로 다른 상품이며, 정식 판매 조건은 아직 확정하지 않았습니다.</p><p class="core-note">실제 개발·배포·DB·보안·대규모 제작은 별도 범위를 합의합니다. 이 페이지에서는 결제나 계약이 진행되지 않습니다.</p><nav class="review-price-nav" aria-label="가격 검토안"><a href="#prototype-price-track">프로젝트별 구성안 ↓</a><a href="#main-price-track">진단·실행 구성안 ↓</a></nav></div></section>
<div id="prototype-price-track" aria-label="프로젝트별 구성안"><div class="core-wrap review-track-heading"><p class="core-overline">구성안 A · 프로젝트별 협업</p></div>{prototype}</div>
<section class="core-band core-example" id="main-price-track" aria-labelledby="main-price-title"><div class="core-wrap"><p class="core-overline">구성안 B · 진단에서 실행까지</p><h2 id="main-price-title">문제의 크기에 따라 시작하는 구성.</h2><p class="core-lead">아래 가격·구성은 출시 전 검토안입니다. 실제 판매 시 서비스 범위, 제공기간, 부가세 및 환불 조건을 개별 상품 페이지에서 확정해 안내합니다.</p>{main_prices}<p class="core-note">Mashcore의 첫 진단 99,000원은 Weplace 홈페이지 최초 생성 99,000원 가안과 다른 상품입니다. 서로의 범위와 운영 조건을 합치지 않습니다.</p></div></section>
<section class="core-band" aria-labelledby="faq-title"><div class="core-wrap"><p class="core-overline">먼저 궁금할 이야기</p><h2 id="faq-title">시작하기 전에.</h2>
<details class="service-faq"><summary>광고를 대신 운영하는 곳인가요?</summary><p>Mashcore는 먼저 무엇을 바꾸고 어떤 순서로 실행할지 정합니다. 광고 집행이나 제작이 필요하다면, 맡을 일과 협업할 범위를 구분해 제안합니다.</p></details>
<details class="service-faq"><summary>아직 문제가 명확하지 않아도 이야기할 수 있나요?</summary><p>지금 하는 일과 반복해서 마음에 걸리는 장면부터 들려주세요. 먼저 확인해야 할 질문을 함께 정리합니다.</p></details>
<details class="service-faq"><summary>홈페이지 제작도 함께하나요?</summary><p>방문자의 질문에 맞춘 문구·정보 구조·디지털 요구사항을 설계합니다. 실제 개발·게시·운영은 프로젝트에서 합의한 업무 범위에 따라 진행합니다.</p></details></div></section>
<section class="core-band" aria-labelledby="scope-title"><div class="core-wrap"><div class="core-section-heading"><div><p class="core-overline">범위와 연락 방법</p><h2 id="scope-title">무엇을 함께할지,<br>먼저 분명하게.</h2></div><p class="core-lead">전략·문구·정보 구조·요구사항을 정하는 일과 실제 개발·배포·DB·보안·대규모 제작은 필요한 범위를 나누어 합의합니다. 광고비·촬영·출장·인쇄·서버·구독료 등 실비도 별도 협의합니다.</p></div><p>현재는 일반 카드결제·자동결제 모두 개통 전입니다. 문의 메일 작성은 계약·결제 신청이나 서버 접수가 아닙니다.</p><div class="core-hero-actions"><a class="core-button" href="/#invitation">함께할 범위 이야기하기 <span aria-hidden="true">↗</span></a><a class="core-text-link" href="/policies/refund/">취소·환불 정책 읽기 →</a></div><div class="core-research-links"><a href="/about/">어떤 방식으로 판단하나요?</a><a href="/work/weplace/">현장 협업의 질문과 설계</a></div></div></section>'''


def render_about(s: dict) -> str:
    privacy = escape(s['privacy_note'])
    return f'''
<section class="core-about-hero review-detail-hero" aria-labelledby="about-title"><div class="core-wrap"><p class="core-overline">최규현 · 전략·브랜드·디지털 설계</p><h1 id="about-title">현장을 아는 사람과,<br>다음 길을 함께 만듭니다.</h1><p class="core-lead">대표님은 현장에서 무엇이 잘되는지, 어디가 어려운지 알고 있습니다. 저는 그 경험에 고객의 관점과 브랜드·디지털 설계를 연결합니다.</p><div class="core-hero-actions"><a class="core-button core-button-light" href="/services/">함께할 수 있는 일 보기 <span aria-hidden="true">↗</span></a><a class="core-hero-secondary" href="#judgment">판단하는 방식 살펴보기 ↓</a></div></div></section>
<section class="core-band" id="judgment" aria-labelledby="judgment-title"><div class="core-wrap"><p class="core-overline">무엇을 살피고, 어떻게 판단하는가</p><h2 id="judgment-title">보이는 것 너머,<br>사람의 이유를 봅니다.</h2><p class="core-lead">하나의 장면을 바로 결론으로 만들지 않습니다. 실제 자료와 다른 설명을 함께 살펴보고, 지금 선택할 일과 다음 실행의 기준을 정합니다.</p><div class="core-steps">
<article><span class="core-step-number">01</span><h3>관찰한 질문</h3><p>현장과 고객 접점에서 반복되는 질문을 찾습니다. 보인 사실과 아직 확인하지 못한 부분을 나눕니다.</p></article>
<article><span class="core-step-number">02</span><h3>비교한 설명</h3><p>자료에 나타난 차이와 가능한 이유를 비교합니다. 어떤 근거가 더 필요하고, 무엇이 달라지면 생각을 바꿀지도 적습니다.</p></article>
<article><span class="core-step-number">03</span><h3>선택한 구조</h3><p>지금 정할 방향과 다음 실행의 순서를 만듭니다. 실제 반응을 확인한 뒤 유지할 것과 고칠 것을 다시 정합니다.</p></article>
</div><p class="core-note">이 구성은 작업 방식을 설명합니다. 특정 프로젝트의 성과나 검증된 효과를 나타내는 사례가 아닙니다.</p></div></section>
<section class="core-band core-example" aria-labelledby="leave-title"><div class="core-wrap"><p class="core-overline">무엇을 남기는가</p><h2 id="leave-title">생각에서 멈추지 않도록.</h2><div class="core-two-columns"><article><h3>같이 판단할 기준</h3><p>사업의 방향, 고객의 질문, 살펴볼 근거와 실행 우선순위를 정리합니다. 선택한 이유가 남아 다음 판단에서도 꺼내 볼 수 있게 합니다.</p></article><article><h3>실제로 쓸 문장과 구조</h3><p>강점이 전해지는 소개말, 제안 순서, 홈페이지의 정보 구성, 디지털 기능의 요구사항과 완료 판단 기준으로 옮깁니다.</p></article></div><a class="core-text-link" href="/services/#service-axes">질문과 산출물의 예시 보기 →</a></div></section>
<section class="core-band" id="people" aria-labelledby="people-title"><div class="core-wrap"><p class="core-overline">함께 하여 강화한다</p><h2 id="people-title">각자의 강점을,<br>하나의 다음 선택으로.</h2><p class="core-lead">Mashcore의 중심에는 ‘함께 하여 강화한다’가 있습니다. 서로 다른 경험과 전문성을 연결하되, 누가 어떤 역할을 맡는지는 분명히 합니다.</p><div class="core-people">
<article class="core-person"><span class="core-person-number">01</span><p class="core-overline">현장에서 쌓아온 강점</p><h3>대표님의 경험</h3><p>누가 찾아오는지, 무엇을 잘하는지, 운영하면서 어디가 어려운지. 대표님이 가장 잘 아는 현장에서 출발합니다.</p><p class="core-result"><span>함께 남기는 것</span>현재 상황과 지켜야 할 강점</p></article>
<article class="core-person"><span class="core-person-number">02</span><p class="core-overline">전략·브랜드·디지털 설계</p><h3>최규현</h3><p>사람과 공간, 고객의 망설임을 읽습니다. 강점이 전해질 소개말과 정보의 순서, 홈페이지와 상담·업무의 흐름을 설계합니다.</p><p class="core-result"><span>함께 남기는 것</span>사업의 방향과 실제로 쓸 문장·화면·실행 순서</p></article>
<article class="core-person"><span class="core-person-number">03</span><p class="core-overline">프로젝트에 필요한 전문성</p><h3>분석과 제작의 협업</h3><p>필요한 자료 분석이나 제작이 있을 때 실제 참여자와 맡을 범위를 정합니다. 참여자의 전문성이 필요한 판단과 결과물에 연결되도록 협업합니다.</p><p class="core-result"><span>함께 남기는 것</span>자료에서 확인할 기준과 합의한 결과물</p></article>
</div><p class="core-note">담당자·참여 범위·자료 접근 권한은 프로젝트마다 합의합니다. 이 소개가 상시 배정 인력이나 모든 계약의 포함 범위를 뜻하지는 않습니다.</p><details class="core-boundary"><summary>경험과 자료는 어떻게 다루나요?</summary><p>{privacy}</p><p>분석에 필요한 자료와 전달 방법은 먼저 합의합니다. 이 홈페이지에 고객정보나 매출 원본을 올리는 기능은 없습니다.</p></details></div></section>
<section class="core-band core-research-band" aria-labelledby="connections-title"><div class="core-wrap"><p class="core-overline">연구·현장·기록으로 이어지는 일</p><h2 id="connections-title">배운 것을,<br>다음에도 쓸 수 있게.</h2><div class="core-steps">
<article id="lab"><p class="core-overline">질문과 근거</p><h3>Mashcore Lab</h3><p>관찰한 질문과 가설, 다른 설명, 생각을 바꾼 이유를 연구로 남깁니다.</p><a class="core-text-link" href="/research/">연구 읽기 →</a></article>
<article id="weplace"><p class="core-overline">현장 실행 브랜드 · 전략·디지털 설계 협업</p><h3>Weplace</h3><p>고객이 정보를 읽고 자기 상황에 대입한 뒤 상담으로 이어지는 흐름을 함께 설계합니다. 두 브랜드가 각자 판단하고 실행하는 관계를 유지합니다.</p><a class="core-text-link" href="/work/weplace/">협업의 질문과 설계 보기 →</a></article>
<article id="mashcore34"><p class="core-overline">개인 기록과 표현</p><h3>Mashcore34</h3><p>사람·브랜드·공간·관계를 관찰하며 얻은 질문과 기준을 기록하고, 글로 이어갑니다.</p><a class="core-text-link" href="/explore/">공개된 생각 읽기 →</a></article>
</div></div></section>
<section class="core-band" aria-labelledby="about-invitation-title"><div class="core-wrap"><p class="core-overline">다음 이야기는, 대표님의 상황에서</p><h2 id="about-invitation-title">지금, 어떤 선택 앞에 서 있나요?</h2><p class="core-lead">완성된 계획이 없어도 괜찮습니다. 지금 하는 일과 마음에 걸리는 점부터 이야기해 주세요.</p><div class="core-hero-actions"><a class="core-button" href="/#invitation">내 상황 이야기하기 <span aria-hidden="true">↗</span></a><a class="core-text-link" href="/research/chore-to-play/">일을 보는 여섯 관점 읽기 →</a></div></div></section>'''
