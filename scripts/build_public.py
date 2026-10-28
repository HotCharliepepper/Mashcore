#!/usr/bin/env python3
"""Generate static Mashcore review pages. Python standard library only.

The v5 index/research files remain the baseline. Shared content renders into
'dist', never into production source pages. Unapproved offers block production.
"""
from __future__ import annotations
import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlencode
from review_home import hero as review_hero, observation as review_observation, field as review_field, invitation as review_invitation, flow_figure
from review_details import render_services, render_about
from review_r2 import hero as r2_hero, situations, judgment, outputs_process, home_faq
from media_assets import verify_media
from review_seo import apply_seo
from review_integrated import render_review_pages, research_bridge, field_bridge

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://mashcore.co.kr'
EMAIL = 'weplacehyun@naver.com'  # Latest main configuration; inbox delivery not tested.
E = html.escape


def read_json(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(obj, dict):
        raise ValueError(f'{path}: an object is required')
    return obj


def catalog_guard(catalog: dict, context: str) -> None:
    products = catalog.get('products', [])
    if [p.get('amount') for p in products] != [4000000, 2500000, 1500000, 500000]:
        raise ValueError('Preserve all four owner-specified KRW amounts and their order.')
    if len({p['id'] for p in products}) != 4:
        raise ValueError('Four unique product IDs are required.')
    for p in products:
        if p['amount_label'] != f"{p['amount']//10000}만원":
            raise ValueError('Display price and numeric price disagree.')
        for key in ('for','scope','period','meetings','data','deliverables','revision','not_included'):
            if not p.get(key):
                raise ValueError(f"{p['id']}: missing {key}")
    if context == 'production' and not (
        catalog.get('production_approved') is True
        and catalog.get('status') == 'APPROVED'
        and catalog.get('basis_status') == 'APPROVED'
        and catalog.get('vat_status') == 'CONFIRMED'
    ):
        raise ValueError('PRODUCTION BLOCKED: prototype scope, billing basis and VAT need explicit approval. The current published site is not changed.')


def business_config(root: Path) -> dict:
    raw = (root / 'assets/js/site-config.js').read_text(encoding='utf-8')
    match = re.search(r'Object\.freeze\((\{.*?\})\)\s*;', raw, re.S)
    if not match:
        raise ValueError('Expected JSON in the shared business configuration.')
    return json.loads(match.group(1))


def business_rows(b: dict) -> str:
    labels = {'companyName':'상호','representative':'대표자','registrationNumber':'사업자등록번호','address':'사업장 주소','phone':'전화','email':'이메일'}
    items = ''.join(f'<div><dt>{label}</dt><dd>{E(str(b[key]))}</dd></div>' for key,label in labels.items() if b.get(key))
    items=items.replace('<dd>'+E(str(b.get('email','')))+'</dd>', '<dd><a href="mailto:'+E(str(b.get('email','')))+'">'+E(str(b.get('email','')))+'</a></dd>')
    return '<dl class="business-info" data-business-info="">' + items + '</dl>'


def header() -> str:
    return '<header class="site-header core-header"><div class="core-wrap header-inner"><a class="brand core-brand" href="/" aria-label="Mashcore 홈">Mashcore</a><nav id="main-nav" class="desktop-nav" aria-label="주요 메뉴"><a href="/services/">함께할 일</a><a href="/research/">연구·노트</a><a href="/work/weplace/">현장 협업</a><a href="/signal-studio/">Signal Studio</a><a href="/about/">소개</a><a class="mobile-inquiry" href="/#invitation">내 상황 이야기하기 ↗</a></nav><a class="header-cta" href="/#invitation">내 상황 이야기하기 <span aria-hidden="true">↗</span></a><button class="menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="메뉴 열기">메뉴</button></div></header>'


def footer(b: dict) -> str:
    return f'''<footer class="core-footer"><div class="core-wrap"><div class="core-footer-grid"><div><a class="core-footer-brand" href="/">Mashcore</a><p>함께 하여 강화한다.<br>서로의 강점을 모아 사업의 다음 선택을 설계합니다.</p></div><nav aria-label="하단 메뉴"><a href="/services/">서비스</a><a href="/research/">연구</a><a href="/research/notes/">노트</a><a href="/research/log/">연구 기록</a><a href="/signal-studio/">Signal Studio</a><a href="/explore/">생각 읽기</a><a href="/about/">소개</a><a href="/policies/refund/">취소·환불 정책</a></nav></div><section class="footer-legal" aria-labelledby="footer-business-title"><h2 id="footer-business-title">사업자 정보</h2>{business_rows(b)}</section><div class="core-footer-bottom"><span>© 2026 Mashcore</span><span>전략·브랜드·디지털 설계</span><a href="#main">위로 ↑</a></div></div></footer>'''


def page(path: str, title: str, description: str, main: str, b: dict, *, home: bool = False, review: bool = True) -> str:
    data = {'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'url':BASE+path,'inLanguage':'ko'}
    schema = json.dumps(data, ensure_ascii=False).replace('<','\\u003c')
    robots = '<meta name="robots" content="noindex,nofollow">' if review else ''
    scripts = '<script defer src="/assets/js/site-config.js"></script><script defer src="/assets/js/site.js"></script>'
    if home:
        scripts += '<script defer src="/assets/js/hero-media.js"></script><script defer src="/assets/js/hero-reverse.js"></script><script defer src="/assets/js/observations.js"></script><script defer src="/assets/js/chapters.js"></script>'
    body_class = 'landing-page core-page' if home else 'document-page core-page'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{E(title)}</title><meta name="description" content="{E(description,quote=True)}"><meta name="theme-color" content="#202124"><link rel="canonical" href="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title,quote=True)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{BASE}{path}">{robots}<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23121A14'/%3E%3Cpath d='M8 22V10h2.4l3.1 7 3.1-7H22v12h-2.2v-7.8l-2.9 6.4h-1.8l-2.9-6.4V22z' fill='%23A6885A'/%3E%3C/svg%3E"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&amp;family=Noto+Sans+KR:wght@400;500;600&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/css/strategy.css"><script type="application/ld+json">{schema}</script>{scripts}</head><body class="{body_class}"><a class="core-skip" href="#main">본문으로 바로 가기</a>{header()}<main id="main">{main}</main>{footer(b)}</body></html>'''


def people(s: dict, ident: str = 'together') -> str:
    cards = ''.join(f'''<article class="core-person"><span class="core-person-number">0{i}</span><p class="core-overline">{E(p['role'])}</p><h3>{E(p['name'])}</h3><p>{E(p['description'])}</p><p class="core-result"><span>함께 남기는 것</span>{E(p['output'])}</p></article>''' for i,p in enumerate(s['people'],1))
    return f'''<section class="core-band core-together" id="{ident}" aria-labelledby="{ident}-title"><div class="core-wrap"><div class="core-section-heading"><div><p class="core-overline">Mashcore가 하는 일</p><h2 id="{ident}-title">혼자 보던 문제를,<br>함께 더 정확하게.</h2></div><p class="core-lead">{E(s['combined_description'])}</p></div><div class="core-people">{cards}</div><div class="core-center"><p class="core-overline">Mash + Core</p><h3>함께 모은 강점이,<br class="core-small-break"> 전략의 중심이 됩니다.</h3><p>{E(s['combined_title'])}</p></div><details class="core-boundary"><summary>경험과 자료는 어떻게 다루나요?</summary><p>{E(s['privacy_note'])}</p><p>분석에 필요한 자료의 범위와 전달 방법은 먼저 합의합니다. 이 홈페이지에 고객정보나 매출 원본을 올리는 기능은 없습니다.</p></details></div></section>'''


def example(s: dict) -> str:
    x=s['example']
    steps=''.join(f'<article><span class="core-step-number">0{i}</span><h3>{E(p["title"])}</h3><p>{E(p["text"])}</p></article>' for i,p in enumerate(x['steps'],1))
    return f'''<section class="core-band core-example"><div class="core-wrap"><p class="core-overline">{E(x['label'])}</p><h2>{E(x['title'])}</h2><div class="core-steps">{steps}</div><p class="core-note">자료에서 나타난 차이가 곧 원인이라는 뜻은 아닙니다. 확인한 사실과 아직 살펴볼 가능성을 구분합니다.</p></div></section>'''


def product(p: dict, c: dict) -> str:
    subject=f"[Mashcore 상품 상담] {p['name']} · {p['amount_label']} 검토안"
    body=f"관심 있는 구성: {p['name']}\n금액: {p['amount_label']} (정식 요금 아님)\n{c['basis_label']} / {c['vat_label']}\n\n사업 또는 매장 이름:\n함께 살펴보고 싶은 문제:\n답변받을 연락 방법:\n\n상담을 위한 메일이며 계약·결제 신청이 아닙니다.\n고객 개인정보나 매출 원본은 첨부하지 마세요."
    href='mailto:'+EMAIL+'?'+urlencode({'subject':subject,'body':body})
    outputs=''.join(f'<li>{E(v)}</li>' for v in p['deliverables'])
    return f'''<article class="core-product" id="product-{p['id']}" aria-labelledby="product-title-{p['id']}"><p class="core-overline">상품 구성 검토안</p><h3 id="product-title-{p['id']}">{E(p['name'])}</h3><p class="core-for">{E(p['for'])}</p><p class="core-price"><strong>{E(p['amount_label'])}</strong><span>{E(c['basis_label'])}</span></p><p class="core-tax">{E(c['vat_label'])} · 정식 판매가 아님</p><p class="core-promise">{E(p['promise'])}</p><p class="core-includes"><span>함께 만드는 것</span>{E(p['summary'])}</p><p class="core-period">진행 기간: {E(p['period'])}</p><details class="core-product-details"><summary>포함 범위·결과물·별도 비용 보기</summary><div class="core-detail-body"><dl><div><dt>대상 범위</dt><dd>{E(p['scope'])}</dd></div><div><dt>대화·검토</dt><dd>{E(p['meetings'])}</dd></div><div><dt>살펴볼 자료</dt><dd>{E(p['data'])}</dd></div></dl><h4>받게 되는 결과물 · 제안</h4><ul>{outputs}</ul><h4>담당 역할</h4><p>{E(p['analysis'])}</p><h4>수정·확인 범위</h4><p>{E(p['revision'])}</p><h4>포함하지 않는 것</h4><p>{E(p['not_included'])}</p><p>광고비·촬영·출장·인쇄·서버·구독료 등 실비는 별도 협의합니다.</p></div></details><a class="core-button" data-product-contact="{p['id']}" href="{E(href,quote=True)}">이 구성으로 문의 메일 작성 <span aria-hidden="true">↗</span><span class="sr-only"> — {E(p['name'])}</span></a><p class="core-mail-note">메일 앱에서 확인한 뒤 직접 보내주세요.</p></article>'''


def services(c: dict, heading: str = 'h2') -> str:
    cards=''.join(product(p,c) for p in c['products'])
    exclusions=''.join(f'<li>{E(x)}</li>' for x in c['common_exclusions'])
    return f'''<section class="core-band core-services" id="services" aria-labelledby="services-title"><div class="core-wrap"><p class="core-overline">함께 시작하는 네 가지 방법</p><{heading} id="services-title">지금 필요한 만큼,<br>함께 시작합니다.</{heading}><p class="core-lead">처음 방향을 찾는 일부터, 자료 분석과 실행 설계까지.<br>지금 필요한 도움과 결과물을 먼저 살펴보세요.</p><aside class="core-review-notice" aria-label="상품 검토안 안내"><strong>현재는 상품 구성 검토 단계입니다.</strong><p>{E(c['common_notice'])}</p></aside><div class="core-product-grid">{cards}</div><div class="core-common"><h3>모든 구성에서 먼저 합의할 내용</h3><p>{E(c['common_scope'])}</p><details><summary>공통 별도 항목과 계약 범위 보기</summary><ul>{exclusions}</ul><p>자료 전달 방식, 실제 투입 인력, 변경·취소·해지 조건, 결과물의 사용 범위는 계약 전에 정합니다. 특정 매출·검색 순위·계약 건수를 보장하지 않습니다.</p></details></div><p class="core-final-question">어떤 구성이 맞는지 아직 모르셔도 괜찮습니다.<br><a href="/#invitation">지금 상황부터 이야기하기 →</a></p></div></section>'''


def extract_sections(source: str) -> tuple[str,str,str]:
    markers=['<section aria-labelledby="observation-title"','<section aria-labelledby="connection-title"','<section aria-labelledby="invite-title"']
    pos=[]
    for marker in markers:
        if source.count(marker)!=1:
            raise ValueError('Baseline changed; review the home markers before proceeding: '+marker)
        pos.append(source.index(marker))
    end=source.index('</main>',pos[2])
    return source[pos[0]:pos[1]],source[pos[1]:pos[2]],source[pos[2]:end]


def about_main(s: dict) -> str:
    content=f'''<section class="core-about-hero"><div class="core-wrap"><p class="core-overline">{E(s['principle'])}</p><h1>서로의 강점을 모아,<br>더 나은 선택을.</h1><p class="core-lead">{E(s['hero_description'])}</p><p>Mash는 서로 다른 경험과 능력을 모으는 일,<br>Core는 그 힘으로 사업의 중심을 잡는 일을 뜻합니다.</p><a class="core-text-link" href="/services/">함께 시작할 수 있는 일 보기 →</a></div></section>'''
    content+=people(s,'people')+example(s)
    content+='''<section class="core-band" id="weplace"><div class="core-wrap"><p class="core-overline">생각을 현장으로 연결하는 방식</p><h2>역할을 분명히 하고,<br>필요한 일을 연결합니다.</h2><div class="core-two-columns"><article><h3>Mashcore</h3><p>사업의 강점과 고객의 질문을 읽고, 자료를 분석해 방향과 실행 기준을 설계합니다. 브랜드·상품·디지털 화면·업무 방식에 필요한 안을 만듭니다.</p></article><article><h3>Weplace</h3><p>별도로 협의한 범위에서 로컬 매장의 홈페이지·지도 정보·사진·안내 등 고객 접점을 개선하는 실행 브랜드입니다. 전략·디지털 설계 협업을 포트폴리오에서 살펴볼 수 있습니다.</p><a href="/work/weplace/">Weplace 적용 사례 보기 →</a></article></div><p class="core-note">담당자·납품 범위·자료 접근 권한은 프로젝트별로 정합니다. 두 사업자의 계약과 고객정보를 자동으로 합치지 않습니다.</p></div></section><section class="core-band core-research-band" id="mashcore34"><div class="core-wrap"><p class="core-overline">배운 것을 오래 쓰는 기준으로</p><h2>한 번의 답을 넘어,<br>다음에도 쓸 수 있게.</h2><p class="core-lead">Mashcore Lab에서는 관찰한 일과 확인한 자료, 선택한 이유를 연구합니다. 현장에서 배운 기준은 방법론과 Mashcore34의 집필 자료로 쌓아갑니다.</p><p>Chore to Play는 같은 일을 여섯 관점에서 살펴보는 진행 중인 연구입니다. 사람의 등급이나 성장 순서를 정하는 검사가 아닙니다.</p><div class="core-research-links"><a href="/research/chore-to-play/">Chore to Play 연구</a><a href="/research/market-interpretation/">판단의 기준을 다루는 연구</a><a href="/research/log/">연구 기록</a><a href="/explore/">생각 읽기</a></div></div></section>'''
    return content


def render_new_pages(output: Path, s: dict, c: dict, b: dict, context: str) -> None:
    for route,title,desc,body in [
        ('about','소개 — Mashcore',s['description'],render_about(s)),
        ('services','하는 일 — Mashcore','사업의 방향, 고객에게 건네는 말, 홈페이지와 상담의 흐름을 함께 설계합니다. 상품 구성과 조건은 검토 중입니다.',render_services(c, product, services))
    ]:
        (output/route).mkdir(parents=True,exist_ok=True)
        (output/route/'index.html').write_text(page('/'+route+'/',title,desc,body,b,review=context!='production' or route=='services'),encoding='utf-8')


def build(root: Path, output: Path, context: str) -> dict:
    s=read_json(root/'content/strategy.json');c=read_json(root/'content/services-prototype.json');b=business_config(root)
    if b.get('email') != EMAIL or b.get('siteUrl','').rstrip('/') != BASE:
        raise ValueError('Business config, BASE and EMAIL must match.')
    effective_context='production' if os.environ.get('CONTEXT')=='production' else context
    catalog_guard(c,effective_context)
    source=(root/'index.html').read_text(encoding='utf-8')
    observed,portfolio,invitation=extract_sections(source)
    if output.resolve()!=root.resolve()/'dist' or output.is_symlink():
        raise ValueError('Only the dedicated repo/dist directory may be replaced.')
    if output.exists():shutil.rmtree(output)
    output.mkdir()
    for name in ('assets','mobile','preview','explore','research','about','work','policies'):
        if (root/name).is_dir():
            shutil.copytree(root/name,output/name,ignore=shutil.ignore_patterns('*.md','*.map','.DS_Store','node_modules','__pycache__'))
    for name in ('robots.txt','sitemap.xml','_redirects','_headers','mashcore-profile.jpg'):
        if (root/name).is_file():shutil.copy2(root/name,output/name)
    media=read_json(root/'content/hero-media.json')
    observed=review_observation(observed,s)
    portfolio=review_field(s)
    invitation=review_invitation(EMAIL,s)
    origin='<section id="origin" aria-labelledby="opening-title" data-chapter="">'+r2_hero(s,media)+situations()+'</section>'
    observed=observed.rsplit('</section>',1)[0]+judgment()+research_bridge()+'</section>'
    portfolio=portfolio.rsplit('</section>',1)[0]+outputs_process()+field_bridge()+'</section>'
    invitation=invitation.replace('<div class="chapter-inner invitation-layout">',home_faq()+'<div class="chapter-inner invitation-layout">',1)
    main=origin+observed+portfolio+invitation
    home=page('/',s['title'],s['description'],main,b,home=True,review=context!='production')
    (output/'index.html').write_text(home,encoding='utf-8')
    (output/'mobile').mkdir(exist_ok=True)
    mobile=home.replace('class="landing-page core-page"','class="landing-page core-page mobile-edition"',1).replace('<title>Mashcore —','<title>Mashcore 모바일 —',1)
    (output/'mobile/index.html').write_text(mobile,encoding='utf-8')
    render_new_pages(output,s,c,b,context)
    render_review_pages(output,b,page,review=context!='production')
    count=0
    for path in sorted(output.rglob('*.html')):
        text=path.read_text(encoding='utf-8').replace('https://mashcore.netlify.app',BASE).replace('weplace25@gmail.com',EMAIL)
        if path.relative_to(output).as_posix()!='preview/index.html':
            text=re.sub(r'<header class="site-header[^>]*>.*?</header>',lambda _:header(),text,count=1,flags=re.S)
            text=re.sub(r'<footer\b.*?</footer>',lambda _:footer(b),text,count=1,flags=re.S)
            count+=1
            if '/assets/css/strategy.css' not in text:
                text=text.replace('</head>','<link rel="stylesheet" href="/assets/css/strategy.css"></head>',1)
        text=re.sub(r'<link[^>]+(?:fonts.googleapis.com|fonts.gstatic.com)[^>]*>','',text)
        # Establish the existing progressive-enhancement class before first paint.
        # If site.js fails, restore the readable navigation fallback.
        if path.relative_to(output).as_posix()!='preview/index.html':
            text=text.replace('<head>','<head><script>document.documentElement.classList.add("js");addEventListener("error",e=>{if((e.target?.src||e.filename||"").split("?")[0].endsWith("/site.js"))document.documentElement.classList.remove("js")},true)</script>',1)
        text=text.replace('</head>','<link rel="stylesheet" href="/assets/css/fonts.css"><link rel="stylesheet" href="/assets/css/renewal.css"><link rel="stylesheet" href="/assets/css/experience-r2.css"><link rel="stylesheet" href="/assets/css/review-integrated.css"></head>',1)
        if path.relative_to(output).as_posix() in ('index.html', 'mobile/index.html'):
            text=text.replace('</head>','<link rel="stylesheet" href="/assets/css/hero-reverse.css"></head>',1)
            # Select the requested layout before first paint. With scripts
            # blocked, the server-rendered A remains the readable fallback.
            text=text.replace('<head>', '<head><script>document.documentElement.dataset.heroInitialMode=new URLSearchParams(location.search).get("hero")==="reverse"?"reverse":"default";addEventListener("error",e=>{if((e.target?.src||e.filename||"").split("?")[0].endsWith("/hero-reverse.js"))delete document.documentElement.dataset.heroInitialMode},true)</script>', 1)
            # The deployed review iframe exposed an unstyled first paint.
            # Inline the authored CSS in its existing order on these two entry
            # pages only. No second hand-maintained critical stylesheet.
            for css_name in ('strategy.css','fonts.css','renewal.css','experience-r2.css','hero-reverse.css','review-integrated.css'):
                css_path='/assets/css/'+css_name
                link='<link rel="stylesheet" href="'+css_path+'">'
                style='<style data-source="'+css_path+'">'+(root/css_path.lstrip('/')).read_text(encoding='utf-8')+'</style>'
                text=text.replace(link,style,1)
        text=apply_seo(text,path.relative_to(output).as_posix(),root,b)
        if context!='production' and not re.search(r'<meta\b[^>]*\bname=[\'"]robots[\'"]',text):
            text=text.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>',1)
        path.write_text(text,encoding='utf-8')
    sitemap=output/'sitemap.xml'
    if sitemap.exists():
        text=sitemap.read_text(encoding='utf-8').replace('https://mashcore.netlify.app',BASE)
        for route in ('/services/','/research/lab/','/research/notes/','/signal-studio/'):
            if BASE+route not in text:
                text=text.replace('</urlset>',f'<url><loc>{BASE}{route}</loc></url></urlset>')
        sitemap.write_text(text,encoding='utf-8')
    if context!='production':
        (output/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
        h=output/'_headers';existing=h.read_text(encoding='utf-8') if h.exists() else ''
        h.write_text(existing+'\n/*\n  X-Robots-Tag: noindex, nofollow\n',encoding='utf-8')
    verify_media(root,output)
    result={'context':context,'html_pages':len(list(output.rglob('*.html'))),'business_footers':count,'products':len(c['products'])}
    print(json.dumps(result,ensure_ascii=False));return result


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--context',default=os.environ.get('CONTEXT','local-review'))
    args=parser.parse_args()
    try:build(ROOT,ROOT/'dist',args.context)
    except (ValueError,OSError,json.JSONDecodeError) as exc:raise SystemExit(str(exc)) from exc

if __name__=='__main__':main()
