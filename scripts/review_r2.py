"""R2 sales flow, extending the four established scenes without changing their IDs."""
import json
from html import escape as E


def hero(s, media):
    poster=media['poster']; ui=media['ui']
    title='<br>'.join(E(x) for x in s['hero_title'])
    mobile_title='<br>'.join(E(x) for x in s['hero_title_mobile'])
    config=json.dumps(media,ensure_ascii=False).replace('<','\\u003c')
    video='<video data-hero-video muted playsinline preload="none" aria-label="AI 콘셉트 정지 이미지의 느린 모션 시안" hidden></video>' if any(media['video'].get(k) for k in ('desktop','mobile')) else ''
    return f'''<div class="r1-origin r2-origin core-wrap" data-hero-experience data-hero-mode="default">
<div class="hero-variant-bar" data-hero-mode-controls hidden aria-label="히어로 화면 구성 비교">
 <div class="hero-variant-heading"><span>REVIEW / HERO EXPERIENCE</span><small>같은 문안·같은 행동, 다른 시선 동선</small></div>
 <div class="hero-variant-buttons" role="group" aria-label="히어로 구성 선택">
  <button type="button" data-hero-mode-choice="default" aria-pressed="true">A · 기존 R2</button>
  <button type="button" data-hero-mode-choice="reverse" aria-pressed="false">B · 역방향 탐색</button>
 </div>
 <p class="hero-variant-feedback" data-hero-variant-status role="status" aria-live="polite">기존 R2 구성을 보고 있습니다.</p>
</div>
<div class="origin-stage" data-hero-media data-media-state="poster_only" data-media-has-source="{str(bool(video)).lower()}">
 <figure class="origin-media"><picture><source media="(max-width: 700px)" srcset="{E(poster['mobile'],quote=True)}" width="780" height="1040"><img data-hero-poster src="{E(poster['desktop'],quote=True)}" alt="{E(poster['alt'],quote=True)}" width="1600" height="900" fetchpriority="high" loading="eager"></picture>{video}
 <div class="hero-reverse-layer" data-hero-reverse-layer aria-hidden="true">
  <svg class="hero-reverse-svg" viewBox="0 0 1200 650" preserveAspectRatio="none" focusable="false">
   <defs><linearGradient id="hero-reverse-stroke" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fcf8ec"/><stop offset=".44" stop-color="#d9bd87"/><stop offset="1" stop-color="#8b623d"/></linearGradient></defs>
   <path class="hero-reverse-halo" d="M 1022 264 C 925 250 866 311 799 394 S 636 514 460 548" fill="none" stroke="#fcf8ec" stroke-opacity=".74" stroke-width="8" stroke-linecap="round" pathLength="100"/>
   <path class="hero-reverse-trace" d="M 1022 264 C 925 250 866 311 799 394 S 636 514 460 548" fill="none" stroke="url(#hero-reverse-stroke)" stroke-width="2.8" stroke-linecap="round" pathLength="100"/>
   <circle class="hero-reverse-ring" cx="1022" cy="264" r="29" fill="none" stroke="#fcf8ec" stroke-width="2" stroke-opacity=".92"/>
   <circle class="hero-reverse-source" cx="1022" cy="264" r="5" fill="#fdf9ef"/>
   <path class="hero-reverse-arrow" d="M 476 534 L 454 548 L 481 555" fill="none" stroke="#8b623d" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"/>
  </svg>
  <div class="hero-reverse-question"><span>OBSERVATION / 01</span><strong>어디서, 왜<br>멈추었을까?</strong></div>
 </div><figcaption>{E(media['provenance']['review_label'])}</figcaption></figure>
 <div class="hero-copy"><p class="core-overline"><span class="r2-desktop-copy">MASHCORE / {E(s['hero_role'])}</span><span class="r2-mobile-copy">MASHCORE / {E(s['hero_role_mobile'])}</span></p><h1 id="opening-title"><span class="r2-desktop-copy">{title}</span><span class="r2-mobile-copy">{mobile_title}</span></h1><p class="core-hero-description">{E(s['hero_description'])}</p><a class="core-button hero-primary" href="/services/"><span class="r2-desktop-copy">{E(ui['services_label'])}</span><span class="r2-mobile-copy">{E(ui['services_label_mobile'])}</span><span aria-hidden="true">↗</span></a></div>
 <div class="hero-controls-slot"><div class="hero-media-controls" hidden data-hero-controls><button type="button" data-hero-toggle>{E(ui['play_label'])}</button><span data-hero-status role="status" aria-live="polite"></span></div></div>
 <script type="application/json" data-hero-config>{config}</script>
</div><div class="origin-navigation"><a class="origin-next" href="#research"><span>같은 정보, 다른 순서. 직접 살펴보기</span><span aria-hidden="true">↓</span></a><span class="origin-footnote">사람을 이해하는 일에서 시작합니다.</span></div>
</div>'''


def situations():
    cards=[('전해지는 강점','잘하는데, 왜 잘 전해지지 않을까?','소개말과 사진, 고객이 만나는 첫 화면을 함께 살펴봅니다.','/services/#axis-4','전달하는 말과 순서'),('고객의 다음 질문','고객은 어디서 다시 확인할까?','찾아오는 길부터 조건과 문의까지, 다시 묻게 되는 지점을 찾습니다.','/services/#axis-3','고객의 질문과 접점'),('실행의 우선순위','무엇부터 바꾸면 좋을까?','지금 가진 경험과 자료에서 먼저 확인하고 바꿀 일을 정합니다.','/services/#axis-2','사업의 방향과 선택')]
    return '''<div class="r2-situations core-wrap" aria-labelledby="situations-title"><div class="r2-section-intro"><p class="core-overline">마음에 걸리는 장면이 있나요?</p><h2 id="situations-title">지금의 질문에서<br>함께할 일을 찾습니다.</h2></div><div class="r2-situation-grid">'''+''.join(f'''<article><div class="situation-index"><span>0{i}</span><small>{E(eyebrow)}</small></div><h3>{E(title)}</h3><p>{E(desc)}</p><a href="{href}">{E(link)} <span aria-hidden="true">↗</span></a></article>''' for i,(eyebrow,title,desc,href,link) in enumerate(cards,1))+'''</div></div>'''


def judgment():
    return '''<div class="r2-judgment chapter-inner" aria-labelledby="home-judgment-title"><div><p class="core-overline">Mash + Core / 함께 하여 강화한다</p><h2 id="home-judgment-title">서로 다른 경험을 연결하면,<br>다음 선택이 보입니다.</h2><p>대표님이 아는 현장에 고객의 관점과 자료를 더합니다. 하나의 답으로 서두르지 않고, 지금 선택할 이유와 다음에 확인할 것을 정합니다.</p><a class="core-text-link" href="/about/#judgment">어떻게 판단하는지 보기 ↗</a></div><figure class="r2-judgment-map"><div class="judgment-inputs"><span>현장의 경험</span><span>고객의 질문</span><span>확인한 자료</span></div><div class="judgment-core"><small>MASHCORE</small><strong>연결하고, 비교하고,<br>순서를 정합니다.</strong></div><p class="judgment-output">함께 결정할 방향 <span aria-hidden="true">→</span> 다음 실행</p><figcaption>판단 방식을 설명하는 구성</figcaption></figure></div>'''


def worksheet():
    return '''<figure class="r2-worksheet"><div class="sheet-heading"><span>M / DECISION NOTE</span><span>01</span></div><h3>고객이 다시 묻는 지점은?</h3><dl><div><dt>질문</dt><dd>처음 방문하는 사람에게 무엇이 부족할까?</dd></div><div><dt>확인 자료</dt><dd>공개된 안내 · 반복되는 질문 · 이용 조건</dd></div><div><dt>선택 방향</dt><dd>필요한 조건을 다음 행동 가까이에 둡니다.</dd></div><div><dt>다음 실행</dt><dd>안내를 바꾼 뒤, 다시 들어오는 질문을 살핍니다.</dd></div></dl><figcaption>결과물 구성 예시 · 실제 고객 자료나 납품물이 아닙니다.</figcaption></figure>'''


def outputs_process():
    return '''<div class="r2-outputs chapter-inner" aria-labelledby="home-outputs-title"><div class="r2-output-intro"><div><p class="core-overline">함께 만들고 남기는 것</p><h2 id="home-outputs-title">생각에서 멈추지 않도록.</h2><p>방향을 정하고, 전할 말과 화면으로 옮기고, 다음 실행에서 다시 확인합니다.</p><a class="core-text-link" href="/services/#service-axes">여섯 가지 업무와 결과물 보기 ↗</a></div>'''+worksheet()+'''</div><div class="r2-output-categories"><article><span>01 / 방향과 기준</span><h3>무엇을 먼저 할지</h3><p>사업의 방향, 고객의 질문, 실행 우선순위</p></article><article><span>02 / 전달되는 경험</span><h3>어떻게 전할지</h3><p>소개말, 제안의 순서, 화면과 업무의 구조</p></article><article><span>03 / 다음 실행과 학습</span><h3>무엇을 다시 볼지</h3><p>완료 기준, 관찰 결과, 다음 선택의 기록</p></article></div><div class="r2-process"><div><p class="core-overline">함께 일하는 과정</p><h2>범위를 맞추고,<br>하나씩 움직입니다.</h2><a href="/services/#process-title">자세한 과정과 범위 보기 →</a></div><ol><li><span>01</span><div><h3>상황과 자료를 살핍니다.</h3><p>하고 있는 일과 마음에 걸리는 장면을 듣습니다.</p></div></li><li><span>02</span><div><h3>함께할 범위를 정합니다.</h3><p>맡을 일, 결과물, 일정과 비용을 먼저 맞춥니다.</p></div></li><li><span>03</span><div><h3>설계하고 적용합니다.</h3><p>말과 화면, 실제로 쓸 실행 기준으로 옮깁니다.</p></div></li><li><span>04</span><div><h3>반응을 함께 확인합니다.</h3><p>유지할 것과 다음에 바꿀 것을 정리합니다.</p></div></li></ol></div><div class="r2-detail-links"><a href="/services/#price-tracks-title">상품 구성과 가격 검토안 ↗</a><a href="/research/">판단의 근거를 쌓는 연구 ↗</a></div></div>'''


def home_faq():
    return '''<div class="r2-home-faq chapter-inner" aria-labelledby="home-faq-title"><div><p class="core-overline">대화를 시작하기 전에</p><h2 id="home-faq-title">지금 가진 질문이면<br>충분합니다.</h2></div><div><details class="service-faq"><summary>아직 무엇이 문제인지 명확하지 않아도 되나요?</summary><p>지금 하는 일과 반복해서 마음에 걸리는 장면부터 들려주세요. 먼저 확인할 질문을 함께 정리합니다.</p></details><details class="service-faq"><summary>광고 운영도 맡길 수 있나요?</summary><p>무엇을 바꾸고 어떤 순서로 실행할지 먼저 정합니다. 광고 집행이나 제작이 필요하면 맡을 일과 협업 범위를 구분해 제안합니다.</p></details><details class="service-faq"><summary>홈페이지 제작도 함께하나요?</summary><p>문구·정보 구조·디지털 요구사항을 설계합니다. 실제 개발·게시·운영은 프로젝트에서 합의한 범위에 따라 진행합니다.</p></details></div></div>'''
