#!/usr/bin/env python3
"""Validate generated review output. These checks do not claim browser or device QA."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote, parse_qs
import hashlib
import json
import os
import re

from build_public import catalog_guard, read_json, business_config

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE = 'https://mashcore.co.kr'
EMAIL = 'weplacehyun@naver.com'
EXPECTED_ROUTES = {
    'index.html', 'mobile/index.html', 'services/index.html', 'about/index.html',
    'research/index.html', 'research/chore-to-play/index.html',
    'research/market-interpretation/index.html', 'research/log/index.html',
    'explore/index.html', 'work/weplace/index.html', 'policies/refund/index.html',
    'preview/index.html',
}
BUSINESS = {
    'companyName': 'Mashcore', 'representative': '최규현',
    'registrationNumber': '247-02-04104',
    'address': '서울특별시 영등포구 선유로9길 10, 812호 Mashcore',
    'email': EMAIL, 'phone': '',
}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


def compact(value: str) -> str:
    return re.sub(r'\s+', '', value)


@dataclass
class Node:
    tag: str
    attrs: dict
    children: list = field(default_factory=list)

    def text(self) -> str:
        return ''.join(child if isinstance(child, str) else child.text() for child in self.children)

    def descendants(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.descendants()


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.root = Node('document', {})
        self.stack = [self.root]
        self.nodes = []
        self.feed(text)
        self.ids = [n.attrs['id'] for n in self.nodes if n.attrs.get('id')]
        self.refs = [n.attrs[k] for n in self.nodes for k in ('href', 'src') if n.attrs.get(k)]
        self.aria = [ident for n in self.nodes for key in ('aria-controls', 'aria-labelledby', 'aria-describedby') for ident in n.attrs.get(key, '').split()]
        self.product_links = [n for n in self.nodes if 'data-product-contact' in n.attrs]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.nodes.append(node)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def where(self, attr, value=None):
        return [n for n in self.nodes if attr in n.attrs and (value is None or n.attrs[attr] == value)]

    def one(self, attr, value=None):
        found = self.where(attr, value)
        assert len(found) == 1, f'Expected one [{attr}={value}], found {len(found)}'
        return found[0]


def check_business(page: Page, rel: str):
    footers = [node for node in page.nodes if node.tag == 'footer']
    assert len(footers) == 1, f'Expected one static footer: {rel}'
    footer = footers[0]
    text = compact(footer.text())
    for key, value in BUSINESS.items():
        if value:
            assert compact(value) in text, f'Missing current {key} in static footer: {rel}'
    lists = [n for n in footer.descendants() if 'data-business-info' in n.attrs]
    assert len(lists) == 1, f'Expected static business block: {rel}'
    for key in ('companyName', 'representative', 'registrationNumber', 'address'):
        assert compact(BUSINESS[key]) in compact(lists[0].text()), f'Incomplete static business details: {rel} {key}'
    assert any(n.attrs.get('href') == '/policies/refund/' for n in footer.descendants()), f'No refund footer link: {rel}'
    assert any(n.attrs.get('href') == 'mailto:' + EMAIL for n in footer.descendants()), f'No direct email footer link: {rel}'
    assert not any(n.tag == 'details' for n in footer.descendants()), f'Business information must not be collapsed: {rel}'


def check_products(page: Page):
    catalog = read_json(ROOT / 'content/services-prototype.json')
    assert catalog['production_approved'] is False
    assert catalog['status'] == 'PROPOSED' and catalog['basis_status'] == 'PROPOSED'
    assert catalog['vat_status'] == 'NEED_VERIFY'
    expected = [(4000000, '사업 방향·실행 설계'), (2500000, '고객·매출 분석과 개선'), (1500000, '한 가지 문제 집중 설계'), (500000, '우리 사업 첫 점검')]
    assert [(p['amount'], p['name']) for p in catalog['products']] == expected, 'PR product names/amounts changed'
    assert len(page.product_links) == 4, 'Four distinct prototype inquiry links are required on services'
    for product, link in zip(catalog['products'], page.product_links):
        card = page.one('id', 'product-' + product['id'])
        card_text = compact(card.text())
        for key in ('name', 'amount_label', 'for', 'scope', 'period', 'meetings', 'data', 'revision', 'not_included'):
            assert compact(product[key]) in card_text, f"Missing prototype term: {product['id']} {key}"
        for item in product['deliverables']:
            assert compact(item) in card_text, f"Missing deliverable: {product['id']}"
        for value in (catalog['basis_label'], catalog['vat_label'], '정식 판매가 아님'):
            assert compact(value) in card_text, f"Missing review condition: {product['id']} {value}"
        uri = urlparse(link.attrs.get('href', '')); query = parse_qs(uri.query)
        assert uri.scheme == 'mailto' and uri.path == EMAIL
        assert product['name'] in query.get('subject', [''])[0]
        assert catalog['vat_label'] in query.get('body', [''])[0]
        assert '계약·결제 신청이 아닙니다' in query.get('body', [''])[0]
    # The main track remains a separate comparison. Matching amounts do not merge products.
    main_track = page.one('id', 'main-price-track')
    main_text = compact(main_track.text())
    for value in ('첫 진단', '99,000원', '제안가', '집중 진단', '50만 원', '전략 설계', '100만 원', '전략과 실행', '150만 원', '공급가액 가안', '진행 시간·결과물·VAT 포함 여부는 출시 전에 확정합니다.', '확정 견적 및 VAT는 계약 전 별도 안내합니다.', '진행기간과 납품물은 개별 제안서로 결정합니다.', '작업 항목·횟수·검수 방식은 계약서에 명시합니다.'):
        assert compact(value) in main_text, f'Main price track condition lost: {value}'
    assert not any('data-product-contact' in n.attrs for n in main_track.descendants()), 'Price tracks merged'
    axis_terms = (
        ('신호 해석', '무엇이 달라졌고, 무엇을 더 확인해야 할까요?', '관찰한 장면·근거·가능한 설명·우선 확인할 질문'),
        ('사업 구조', '누구에게 어떤 가치를 어떤 흐름으로 제공할까요?', '고객·가치·제공 방식·실행 우선순위'),
        ('고객 분석', '고객은 어디에서 망설이고, 무엇을 다시 묻나요?', '고객 질문·접점 지도·확인할 자료와 방법'),
        ('영업 설계', '무엇을 어떤 순서로 이해하면 다음 행동이 자연스러울까요?', '상담 질문·제안 순서·후속 대화 기준'),
        ('디지털 요구사항', '홈페이지와 업무 흐름에 무엇이 먼저 필요할까요?', '페이지·기능 지도, 정보 순서, 완료 판단 기준'),
        ('학습과 회고', '실행 뒤 무엇을 유지하고 바꿀까요?', '결정 기록·다른 설명·다음 확인 계획'),
    )
    axes = page.one('id', 'service-axes')
    for terms in axis_terms:
        for value in terms:
            assert compact(value) in compact(axes.text()), f'Service explanation question/output missing: {value}'
    assert '유료 패키지가 아닙니다' in axes.text(), 'Service axes must remain explanation categories'
    assert '/policies/refund/' in page.refs
    try:
        catalog_guard(catalog, 'production')
    except ValueError as error:
        assert 'PRODUCTION BLOCKED' in str(error)
    else:
        raise AssertionError('Unapproved production must be blocked during prototype review.')
    return catalog


def check_observation(home: Page):
    source = Page((ROOT / 'index.html').read_text(encoding='utf-8'))
    source_lab = source.one('data-observation-lab')
    lab = home.one('data-observation-lab')
    actual = compact(lab.text())
    # Individual original text fragments permit layout/ARIA changes while protecting the copy.
    def fragments(node):
        for child in node.children:
            if isinstance(child, str):
                if len(compact(child)) >= 4:
                    yield compact(child)
            else:
                yield from fragments(child)
    for text in fragments(source_lab):
        assert text in actual, 'Original A/B information/copy lost: ' + text[:80]
    assert [n.attrs['data-layout-study'] for n in home.where('data-layout-study')] == ['hand', 'reading', 'decision']
    for caption in ('배치 B · 내용을 읽은 뒤 안내를 열 수 있습니다.', '배치 B · 요금 바로 다음에 포함 항목이 놓여 있습니다.', '배치 B · 이용 조건을 확인한 뒤 예약 방법을 살펴봅니다.'):
        assert compact(caption) in actual, 'Static B fallback caption missing: ' + caption
    expected_b_orders = {
        'hand': ['intro', 'context', 'action'],
        'reading': ['intro', 'price', 'included', 'context'],
        'decision': ['intro', 'conditions', 'action'],
    }
    for key, order in expected_b_orders.items():
        source_panel = source.one('data-layout-study', key)
        source_blocks = {n.attrs['data-layout-block']: compact(n.text()) for n in source_panel.descendants() if 'data-layout-block' in n.attrs}
        fallback = home.one('data-study', key)
        assert fallback.attrs.get('data-static-layout') == 'b' and 'hidden' not in fallback.attrs, 'Static B must remain readable when JS fails'
        fallback_blocks = [n for n in fallback.descendants() if 'data-layout-block' in n.attrs]
        assert [n.attrs['data-layout-block'] for n in fallback_blocks] == order, 'Static B order drifted: ' + key
        assert {n.attrs['data-layout-block']: compact(n.text()) for n in fallback_blocks} == source_blocks, 'A/B must contain exactly the same information: ' + key
    for node in home.where('data-layout-controls'):
        assert 'hidden' in node.attrs, 'A/B control should be enabled only after initialization'
    return True


def check_contact(home: Page):
    question = home.one('id', 'question')
    assert question.tag == 'textarea' and 'maxlength' not in question.attrs, 'Long pasted input must not be truncated'
    assert any(n.tag == 'label' and n.attrs.get('for') == 'question' for n in home.nodes), 'Inquiry needs a permanent label'
    uri = urlparse(home.one('id', 'email-question').attrs.get('href', ''))
    query = parse_qs(uri.query)
    assert uri.scheme == 'mailto' and uri.path == EMAIL
    assert query.get('subject') == ['[Mashcore] 함께할 일 문의'] and 'body' not in query, 'Empty inquiry opens recipient/subject only'
    assert home.one('id', 'copy-question').tag == 'button'
    status = home.one('id', 'copy-status')
    assert status.attrs.get('role') == 'status' or status.attrs.get('aria-live') == 'polite'
    assert 'mailto:' + EMAIL in home.refs, 'Manual direct email path missing'
    assert '저장' in home.root.text() and '직접' in home.root.text()
    for name in ('site.js', 'observations.js'):
        js = (DIST / 'assets/js' / name).read_text(encoding='utf-8')
        assert not re.search(r'\b(?:localStorage|sessionStorage|sendBeacon|XMLHttpRequest)\b|\bfetch\s*\(', js), f'Unexpected inquiry/network persistence in {name}'


def main():
    paths = sorted(DIST.rglob('*.html'))
    actual_routes = {path.relative_to(DIST).as_posix() for path in paths}
    assert actual_routes == EXPECTED_ROUTES, f'Route mismatch: missing={EXPECTED_ROUTES-actual_routes}, extra={actual_routes-EXPECTED_ROUTES}'
    parsed = {path: Page(path.read_text(encoding='utf-8')) for path in paths}
    references = 0
    for path, page in parsed.items():
        rel = path.relative_to(DIST).as_posix()
        raw = path.read_text(encoding='utf-8')
        assert len(page.ids) == len(set(page.ids)), f'Duplicate ID: {rel}'
        for ident in page.aria:
            assert ident in page.ids, f'Broken ARIA ref: {rel} #{ident}'
        for node in page.nodes:
            if node.tag == 'script' and node.attrs.get('type') == 'application/ld+json':
                data = json.loads(node.text())
                assert not re.search(r'"@type"\s*:\s*"(?:Offer|AggregateOffer)"', node.text()), 'Draft offers must not be purchase metadata'
                assert 'mashcore.netlify.app' not in node.text(), f'Old schema domain: {rel}'
        for ref in page.refs:
            parts = urlparse(ref)
            if parts.scheme == 'mailto':
                assert parts.path == EMAIL, f'Stale mail recipient: {rel} {parts.path}'
            if parts.scheme or ref.startswith('//'):
                continue
            resolved = urlparse(urljoin('https://local/' + rel, ref))
            target = DIST / unquote(resolved.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'Missing asset/route: {rel} {ref}'
            references += 1
            if resolved.fragment and target.suffix == '.html':
                assert unquote(resolved.fragment) in parsed[target].ids, f'Broken anchor: {rel} {ref}'
        if rel != 'preview/index.html':
            assert len([n for n in page.nodes if n.tag == 'h1']) == 1, f'H1 count: {rel}'
            check_business(page, rel)
            nav = page.one('id', 'main-nav')
            nav_links = [n for n in nav.descendants() if n.tag == 'a']
            core_links = [n for n in nav_links if 'mobile-inquiry' not in n.attrs.get('class', '').split()]
            mobile_links = [n for n in nav_links if 'mobile-inquiry' in n.attrs.get('class', '').split()]
            assert [n.attrs.get('href') for n in core_links] == ['/services/', '/research/', '/explore/', '/about/'], f'Common navigation mismatch: {rel}'
            assert len(mobile_links) <= 1, f'Duplicate mobile inquiry link: {rel}'
            if mobile_links:
                assert mobile_links[0].attrs.get('href') == '/#invitation', f'Mobile inquiry destination mismatch: {rel}'
                assert '내 상황 이야기하기' in mobile_links[0].text(), f'Mobile inquiry label mismatch: {rel}'
            expected_url = BASE + ('/' if rel in ('index.html', 'mobile/index.html') else '/' + rel.removesuffix('index.html'))
            canonical = [n.attrs.get('href') for n in page.nodes if n.tag == 'link' and n.attrs.get('rel') == 'canonical']
            og = [n.attrs.get('content') for n in page.nodes if n.tag == 'meta' and n.attrs.get('property') == 'og:url']
            assert canonical == [expected_url], f'Canonical mismatch: {rel} {canonical}'
            assert og == [expected_url], f'OG URL mismatch: {rel} {og}'
        if os.environ.get('CONTEXT') != 'production':
            robots = [n.attrs.get('content', '').lower() for n in page.nodes if n.tag == 'meta' and n.attrs.get('name', '').lower() == 'robots']
            assert len(robots) == 1 and 'noindex' in robots[0], f'Robots noindex missing: {rel}'
        assert 'weplace25@gmail.com' not in raw, f'Stale email: {rel}'
        assert '기존 관점 1' not in raw and '기존 관점 2' not in raw and '기존 관점 3' not in raw, f'Placeholder content: {rel}'
    configured = business_config(ROOT)
    assert all(configured.get(key) == value for key, value in BUSINESS.items()), 'Business source values drifted'
    catalog = check_products(parsed[DIST / 'services/index.html'])
    home_raw = (DIST / 'index.html').read_text(encoding='utf-8')
    mobile_raw = (DIST / 'mobile/index.html').read_text(encoding='utf-8')
    assert mobile_raw.replace('class="landing-page core-page mobile-edition"', 'class="landing-page core-page"', 1).replace('<title>Mashcore 모바일 —', '<title>Mashcore —', 1) == home_raw, 'Mobile is not generated from the same source'
    home = parsed[DIST / 'index.html']
    assert [n.attrs.get('id') for n in home.where('data-chapter')] == ['origin', 'research', 'field', 'invitation'], 'Home scene IDs/order changed'
    assert not home.product_links, 'Home must lead to service details, not duplicate product terms'
    check_observation(home)
    check_contact(home)
    chore = parsed[DIST / 'research/chore-to-play/index.html']
    assert [n.attrs['data-spatial-select'] for n in chore.where('data-spatial-select')] == ['action', 'obligation', 'economy', 'relation', 'practice', 'meaning'], 'Six concurrent perspectives changed'
    for attr in ('data-spatial-reset', 'data-spatial-sensor-button', 'data-spatial-stage', 'data-spatial-description'):
        chore.one(attr)
    assert len(chore.where('data-spatial-turn')) == 2, '3D needs direction-button alternatives'
    assert '/assets/js/chore-spatial.js' in chore.refs
    assert '/work/weplace/' in home.refs and '/research/chore-to-play/' in home.refs
    refund_source = Page((ROOT / 'policies/refund/index.html').read_text(encoding='utf-8'))
    refund = parsed[DIST / 'policies/refund/index.html']
    assert compact(refund_source.one('id', 'main').text()) == compact(refund.one('id', 'main').text()), 'Refund terms must be preserved from the selected main source'
    if os.environ.get('CONTEXT') != 'production':
        assert 'Disallow: /' in (DIST / 'robots.txt').read_text(encoding='utf-8')
        assert 'X-Robots-Tag: noindex' in (DIST / '_headers').read_text(encoding='utf-8')
    work = parsed[DIST / 'work/weplace/index.html']
    assert 'https://withweplace.kr/' in work.refs and '/#invitation' in work.refs
    assert '정보 흐름을 요약한 구성' in work.root.text(), 'Reconstruction asset needs an adjacent label'
    forbidden = {'docs', 'content', 'scripts', '.git', 'node_modules', 'qa', 'project_sources', 'upload', '.openai'}
    for path in DIST.rglob('*'):
        rel = path.relative_to(DIST)
        assert not forbidden.intersection(rel.parts), f'Private/source directory in output: {rel}'
        assert path.name not in {'README.md', 'DESIGN.md', 'netlify.toml', 'AGENTS.md'}, f'Private/source file in output: {rel}'
        assert path.suffix not in {'.md', '.py', '.env', '.map', '.zip', '.pem', '.key'}, f'Unexpected source/archive in output: {rel}'
        assert not path.name.startswith('.env'), f'Environment file in output: {rel}'
        if path.suffix == '.json':
            assert rel.as_posix() == '__review/build.json', f'Unapproved data/metadata file in output: {rel}'
        if path.is_file() and path.suffix in {'.html', '.js', '.xml'}:
            assert 'weplace25@gmail.com' not in path.read_text(encoding='utf-8'), f'Stale runtime mail recipient: {rel}'
    assert not any((DIST / 'research' / name).exists() for name in ('else', 'lab', 'market', 'notes')), 'Empty proposed research routes must not be published'
    result = {
        'static_validation': 'PASS', 'html_pages': len(paths), 'expected_routes': sorted(EXPECTED_ROUTES),
        'local_references': references, 'business_footers': len(EXPECTED_ROUTES) - 1,
        'prototype_products': len(catalog['products']), 'main_price_track': 'separate review',
        'production_guard': 'blocked as expected', 'baseline_observation_copy_preserved': True,
        'mobile_sync_exact': True, 'browser_device_mail_validation': 'not covered by this static checker',
        'runtime_js_sha256': {name: hashlib.sha256((DIST / 'assets/js' / name).read_bytes()).hexdigest() for name in ('site.js', 'observations.js', 'chapters.js', 'chore-spatial.js')},
    }
    print(json.dumps(result, ensure_ascii=False))
    if os.environ.get('CONTEXT') != 'production':
        (DIST / '__review').mkdir(exist_ok=True)
        (DIST / '__review/build.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
