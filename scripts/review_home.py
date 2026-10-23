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

def observation(source):
    source=re.sub(r'<h2 id="observation-title">.*?</h2>','<h2 id="observation-title">같은 정보도, 놓인 순서에 따라 다르게 읽힙니다.</h2>',source,flags=re.S)
    source=re.sub(r'<p class="chapter-deck">.*?</p>','<p class="chapter-deck">먼저 눈에 들어오는 것과 다시 찾게 되는 것을 비교해 보세요. 같은 정보를 어떻게 놓을지 살피는 관찰 예시입니다.</p>',source,count=1,flags=re.S)
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
    source=source.replace('<p class="observation-principle">무엇을 바꿀지는, 실제 고객의 반응을 보며 정합니다.</p>','<p class="observation-principle">같은 정보의 배치를 비교하는 예시입니다. 고객 반응이나 전환율을 측정한 결과는 아닙니다.</p>')
    source=re.sub(r'<div class="research-foot">.*?</div>', '<div class="research-foot"><a class="core-button" href="/research/chore-to-play/">일을 보는 여섯 관점 <span aria-hidden="true">↗</span></a><a class="chapter-link" href="/research/market-interpretation/">판단을 다시 확인하는 연구 →</a></div>',source,flags=re.S)
    return source

def hero(s):
    return '''<div class="core-hero"><div class="core-wrap core-hero-grid"><div class="hero-copy"><p class="core-overline">함께 하여 강화한다.</p><h1 id="opening-title">각자의 강점을 모아,<br class="hero-break"> 사업의 다음 길을 만듭니다.</h1><p class="core-hero-description">대표님의 현장 경험과 전략·브랜드·디지털 설계를 연결해, 지금 선택할 방향과 다음 실행을 정리합니다.</p><div class="core-hero-actions"><a class="core-button" href="/services/">함께할 수 있는 일 보기 <span aria-hidden="true">↗</span></a><a class="core-hero-secondary" href="#research">관점 살펴보기 ↓</a></div></div><figure class="role-composition"><figcaption>서로 다른 강점을 연결하는 구성 예시</figcaption><div class="role-slab"><span>01</span><strong>현장 경험</strong><small>지켜야 할 강점과 지금의 질문</small></div><div class="role-slab"><span>02</span><strong>전략·브랜드·디지털 설계</strong><small>자료를 읽고 선택할 기준</small></div><div class="role-slab"><span>03</span><strong>프로젝트에 필요한 전문성</strong><small>합의한 범위에 맞춰 함께할 역할</small></div><div class="role-outcome"><span>지금 결정할 일</span><span aria-hidden="true">→</span><strong>다음 실행</strong></div></figure></div><div class="core-wrap core-hero-floor"><span>경험을 듣고, 자료로 확인하고, 실행할 순서를 정합니다.</span><span class="hero-edition">MASH + CORE</span></div></div>'''

def flow_figure():
    pairs=[('나와 관련 있나','내 상황을 알아볼 질문'),('무엇을 함께하나','맡길 일과 함께할 범위'),('어떤 근거가 있나','확인할 자료와 선택 이유'),('어떻게 이야기하나','예상할 수 있는 다음 행동')]
    return '<figure class="review-flow"><div class="flow-heading"><span>Weplace</span><small>고객이 읽는 순서</small></div><ol>'+''.join(f'<li><span>0{i}</span><div><strong>{a}</strong><p>{b}</p></div></li>' for i,(a,b) in enumerate(pairs,1))+'</ol><figcaption>정보 흐름을 요약한 구성 · 설명용 재구성<br>실제 운영 화면이나 성과 자료가 아닙니다.</figcaption></figure>'

def field():
    return '''<section aria-labelledby="connection-title" class="chapter portfolio-chapter" data-chapter="" id="field"><div class="chapter-inner"><p class="chapter-kicker">03 / 현장 · 질문에서 설계로</p><div class="field-grid"><div><p class="portfolio-relation">현장 실행 브랜드 · 전략·디지털 설계 협업</p><h2 id="connection-title">현장의 질문을,<br>고객이 읽는 순서로.</h2><p class="chapter-deck">Weplace와 고객이 정보를 발견하고 이해한 뒤 상담으로 이어지는 흐름을 함께 설계합니다.</p><dl class="portfolio-focus"><div><dt>함께 다루는 질문</dt><dd>고객은 무엇을 먼저 확인하고, 어디에서 다시 묻게 될까요?</dd></div><div><dt>선택의 이유</dt><dd>자기 상황과 맡길 일을 이해한 뒤, 근거와 연락 방법을 확인하도록.</dd></div></dl><div class="portfolio-actions"><a class="core-button" href="/work/weplace/">협업의 질문과 설계 보기 ↗</a><a class="chapter-link" href="https://withweplace.kr/">Weplace 홈페이지 보기 ↗</a></div></div>'''+flow_figure()+'''</div></div></section>'''

def invitation(email):
    subject=quote('[Mashcore] 함께할 일 문의')
    return f'''<section aria-labelledby="invite-title" class="chapter invitation-chapter" data-chapter="" id="invitation"><div class="chapter-inner invitation-layout"><div><p class="chapter-kicker">04 / 대화 · 지금의 선택</p><h2 id="invite-title">지금, 어떤 선택 앞에 서 있나요?</h2><p class="chapter-deck">지금 하는 일, 마음에 걸리는 점, 함께 확인하고 싶은 것을 편하게 적어주세요.</p><p class="invitation-note">완성된 계획이 없어도 괜찮습니다.<br>지금 가장 마음에 걸리는 한 가지부터.</p></div><div class="question-form"><label for="question">함께 이야기할 상황 <span>선택 입력</span></label><textarea aria-describedby="question-help question-count question-error" id="question" placeholder="잘하고 있는 일인데, 처음 보는 고객에게 어떻게 전해야 할지 모르겠습니다." rows="5"></textarea><div class="form-meta"><span id="question-help">메일·복사에 사용할 내용은 1,000자 이내</span><span id="question-count">0 / 1,000</span></div><p id="question-error" class="question-error" aria-live="polite"></p><div class="form-actions"><a class="btn" href="mailto:{email}?subject={subject}" id="email-question">메일 앱 열기 <span aria-hidden="true">↗</span></a><button class="text-link" id="copy-question" type="button" hidden>질문 복사</button><button class="text-link" id="select-question" type="button" hidden>내용 직접 선택</button></div><p aria-live="polite" class="copy-status" id="copy-status" role="status"></p><div class="direct-contact"><a href="mailto:{email}">{email}</a><p>메일 앱에서 내용을 확인한 뒤 직접 보내주세요.</p><p>작성한 내용은 이 사이트에 저장되거나 자동 접수되지 않습니다. 나가기 전에 필요한 내용을 복사해 주세요.</p><noscript><p>작성한 내용을 직접 선택·복사해 이메일에 붙여 넣어 주세요.</p></noscript></div></div></div></section>'''
