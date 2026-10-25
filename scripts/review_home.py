"""Renewal home compositions. New copy/layout remain PROPOSED; no customer data."""
import re
from html.parser import HTMLParser
from html import escape
from urllib.parse import quote

class Children(HTMLParser):
    """Split direct HTML children without rewriting their original text."""
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source=source;self.depth=0;self.start=0;self.parts=[]
        self.lines=[0]
        for m in re.finditer('\n',source):self.lines.append(m.end())
        self.feed(source)
    def source_offset(self):
        line,col=self.getpos();return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        if self.depth==0:self.start=self.source_offset()
        if tag not in ('br','img','hr','input','meta','link','wbr'):self.depth+=1
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        self.depth-=1
        if self.depth==0:
            end=self.source.index('>',self.source_offset())+1
            self.parts.append(self.source[self.start:end])

STUDIES={
 'hand':(['intro','context','action'],'배치 B · 내용을 읽은 뒤 안내를 열 수 있습니다.'),
 'reading':(['intro','price','included','context'],'배치 B · 요금 바로 다음에 포함 항목이 놓여 있습니다.'),
 'decision':(['intro','conditions','action'],'배치 B · 이용 조건을 확인한 뒤 예약 방법을 살펴봅니다.')}

def observation(source, s):
    c=s["home"]
    source=re.sub(r'<h2 id="observation-title">.*?</h2>','<h2 id="observation-title">'+lines(c['research_title'])+'</h2>',source,flags=re.S)
    source=re.sub(r'<p class="chapter-deck">.*?</p>','<p class="chapter-deck">'+escape(c['research_description'])+'</p>',source,count=1,flags=re.S)
    source=source.replace('02 / SMALL THINGS, REAL QUESTIONS','02 / 관찰 · 읽히는 순서')
    for key,(order,caption) in STUDIES.items():
        pattern=r'(<section\b[^>]*data-layout-study="'+key+r'".*?</section>)'
        m=re.search(pattern,source,re.S)
        if not m:raise ValueError('Missing study '+key)
        panel=m.group(1)
        surface=re.search(r'<div class="study-surface"[^>]*>(.*?)</div>\s*<figcaption>',panel,re.S)
        if not surface:raise ValueError('Missing surface '+key)
        # surface includes its own closing div, but the pattern consumes the final one.
        nodes=Children(surface.group(1)).parts
        blocks={re.search(r'data-layout-block="([^"]+)"',n).group(1):n for n in nodes}
        if set(order)!=set(blocks):raise ValueError('Study blocks changed: '+key)
        fallback='<figure class="study-phone static-layout" data-layout-fallback data-static-layout="b" data-study="'+key+'"><div class="phone-topline">배치 B · 같은 정보</div><div class="study-surface">'+''.join(blocks[k] for k in order)+'</div><figcaption>'+caption+'</figcaption></figure>'
        panel=panel.replace('</section>',fallback+'</section>')
        source=source[:m.start()]+panel+source[m.end():]
    source=source.replace('<p class="observation-principle">무엇을 바꿀지는, 실제 고객의 반응을 보며 정합니다.</p>','<p class="observation-principle">'+escape(c['research_limit'])+'</p>')
    source=re.sub(r'<div class="research-foot">.*?</div>', '<div class="research-foot"><a class="core-button" href="/research/chore-to-play/">일을 보는 여섯 관점 <span aria-hidden="true">↗</span></a><a class="chapter-link" href="/research/market-interpretation/">판단의 근거를 확인하는 연구 →</a></div>',source,flags=re.S)
    source=re.sub(r'<dl class="study-reason">.*?</dl>', lambda m: '<details class="study-question"><summary>이 장면에서 묻는 것</summary>'+m.group()+'</details>', source, flags=re.S)
    return source

def lines(parts):
    return '<br>'.join(escape(part) for part in parts)


def hero(s, media):
    """Initial HTML is complete. Media configuration has one source, no guessed src."""
    import json
    poster=media['poster']; ui=media['ui']; video=media['video']
    next_label=ui['next_label'].removesuffix(' ↓')
    source=video.get('mobile') or video.get('desktop')
    video_html='<video data-hero-video muted playsinline preload="none" aria-label="문 앞의 장면" hidden></video>' if source else ''
    config=json.dumps(media, ensure_ascii=False).replace('<','\\u003c')
    return f'''<div class="r1-origin core-wrap">
<div class="origin-stage" data-hero-media data-media-state="poster_only">
  <figure class="origin-media">
    <picture><source media="(max-width: 900px)" srcset="{escape(poster['mobile'], quote=True)}"><img data-hero-poster src="{escape(poster['desktop'], quote=True)}" alt="{escape(poster['alt'], quote=True)}" width="1600" height="900" fetchpriority="high" loading="eager"></picture>
    {video_html}
    <figcaption>{escape(media['provenance']['review_label'])}</figcaption>
  </figure>
  <div class="hero-copy"><p class="core-overline">{escape(s['hero_role'])}</p><h1 id="opening-title">{lines(s['hero_title'])}</h1><p class="core-hero-description">{escape(s['hero_description'])}</p></div>
  <div class="hero-media-controls" hidden data-hero-controls><button type="button" data-hero-toggle>{escape(ui['play_label'])}</button><span data-hero-status role="status" aria-live="polite"></span></div>
  <script type="application/json" data-hero-config>{config}</script>
</div>
<div class="origin-navigation"><a class="origin-next" href="{escape(ui['next_anchor'], quote=True)}"><span>{escape(next_label)}</span><span aria-hidden="true">↓</span></a><a class="origin-services" href="{escape(ui['services_href'], quote=True)}">{escape(ui['services_label'])} <span aria-hidden="true">↗</span></a></div>
</div>'''

def flow_figure():
    pairs=[('나와 관련 있나','내 상황을 알아볼 질문'),('무엇을 함께하나','맡길 일과 함께할 범위'),('어떤 근거가 있나','확인할 자료와 선택 이유'),('어떻게 이야기하나','예상할 수 있는 다음 행동')]
    return '<figure class="review-flow"><div class="flow-heading"><span>Weplace</span><small>고객이 읽는 순서</small></div><ol>'+''.join(f'<li><span>0{i}</span><div><strong>{a}</strong><p>{b}</p></div></li>' for i,(a,b) in enumerate(pairs,1))+'</ol><figcaption>정보 흐름을 요약한 구성 · 설명용 재구성<br>실제 운영 화면이나 성과 자료가 아닙니다.</figcaption></figure>'

def field(s):
    c=s['home']
    return f'''<section aria-labelledby="connection-title" class="chapter portfolio-chapter" data-chapter="" id="field"><div class="chapter-inner"><p class="chapter-kicker">03 / 현장과 작업</p><div class="field-heading"><h2 id="connection-title">{lines(c['field_title'])}</h2><p class="chapter-deck">{escape(c['field_description'])}</p></div><div class="field-grid"><div><p class="portfolio-relation">현장 실행 브랜드 · 전략·디지털 설계 협업</p><h3>{escape(c['field_project'])}</h3><p class="chapter-deck">{escape(c['field_work'])}</p><dl class="portfolio-focus"><div><dt>함께 다루는 질문</dt><dd>고객은 무엇을 먼저 확인하고, 어디에서 다시 묻게 될까요?</dd></div><div><dt>선택의 이유</dt><dd>자기 상황과 맡길 일을 이해한 뒤, 근거와 연락 방법을 확인하도록.</dd></div></dl><div class="portfolio-actions"><a class="core-button" href="/work/weplace/">작업과 선택의 이유 보기 ↗</a><a class="chapter-link" href="https://withweplace.kr/">Weplace 홈페이지 보기 ↗</a></div></div>'''+flow_figure()+'''</div></div></section>'''

def invitation(email, s):
    c=s["home"]
    subject=quote('[Mashcore] 함께할 일 문의')
    return f'''<section aria-labelledby="invite-title" class="chapter invitation-chapter" data-chapter="" id="invitation"><div class="chapter-inner invitation-layout"><div><p class="chapter-kicker">04 / 대화 · 지금의 선택</p><h2 id="invite-title">{lines(c["invitation_title"])}</h2><p class="chapter-deck">{escape(c["invitation_description"])}</p><p class="invitation-note">{escape(c["invitation_help"])}</p></div><div class="question-form"><label for="question">함께 이야기할 상황 <span>선택 입력</span></label><textarea aria-describedby="question-help question-count question-error" id="question" placeholder="잘하고 있는 일인데, 처음 보는 고객에게 어떻게 전해야 할지 모르겠습니다." rows="5"></textarea><div class="form-meta"><span id="question-help">메일·복사에 사용할 내용은 1,000자 이내</span><span id="question-count">0 / 1,000</span></div><p id="question-error" class="question-error" aria-live="polite"></p><div class="form-actions"><a class="btn" href="mailto:{email}?subject={subject}" id="email-question">메일 앱 열기 <span aria-hidden="true">↗</span></a><button class="text-link" id="copy-question" type="button" hidden>질문 복사</button><button class="text-link" id="select-question" type="button" hidden>내용 직접 선택</button></div><p aria-live="polite" class="copy-status" id="copy-status" role="status"></p><div class="direct-contact"><a href="mailto:{email}">{email}</a><p>메일 앱에서 내용을 확인한 뒤 직접 보내주세요.</p><p>{escape(c["invitation_notice"])}</p><noscript><p>작성한 내용을 직접 선택·복사해 이메일에 붙여 넣어 주세요.</p></noscript></div></div></div></section>'''
