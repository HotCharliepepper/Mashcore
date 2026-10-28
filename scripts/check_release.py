#!/usr/bin/env python3
"""Production/Preview release boundary and generated static-link validation."""
from __future__ import annotations
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
from prepare_public import R31_FILES, R31_ROUTE, R31_PUBLIC_FILES

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"dist"
EXPECTED={
 "index.html","mobile/index.html","services/index.html","about/index.html",
 "explore/index.html","research/index.html","research/lab/index.html",
 "research/notes/index.html","research/log/index.html",
 "research/chore-to-play/index.html","research/market-interpretation/index.html",
 "work/weplace/index.html","signal-studio/index.html","policies/refund/index.html"
}
CANON="https://mashcore.co.kr"
BUSINESS=("247-02-04104","최규현","weplacehyun@naver.com")
FORBIDDEN={"docs","content","scripts","qa",".git",".github","source-media","project_sources","upload","experiments"}
VOID={"br","img","input","link","meta","source","track","hr","wbr","area"}


class Scan(HTMLParser):
    def __init__(self, data):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.ids=[]
        self.h1=0
        self.titles=0
        self.desc=[]
        self.canon=[]
        self.robots=[]
        self.source_commits=[]
        self.chapters=[]
        self.nav=[]
        self.errors=[]
        self._in_head=False
        self.feed(data)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='head':self._in_head=True
        if "id" in a:self.ids.append(a["id"])
        if tag=="section" and "data-chapter" in a:self.chapters.append(a.get("id"))
        if tag=="h1":self.h1+=1
        if tag=="title" and self._in_head:self.titles+=1
        if tag=="meta" and a.get("name")=="description":self.desc.append(a.get("content",""))
        if tag=="meta" and a.get("name")=="robots":self.robots.append(a.get("content",""))
        if tag=="meta" and a.get("name")=="r31-commit":self.source_commits.append(a.get("content",""))
        if tag=="link" and a.get("rel")=="canonical":self.canon.append(a.get("href",""))
        if tag=="img" and "alt" not in a:self.errors.append("Missing img alt")
        for k in ("href","src","poster","data-src"):
            if a.get(k):self.links.append(a[k])
        if tag=="a" and a.get("href") in ("/services/","/research/","/work/weplace/","/signal-studio/","/about/"):
            self.nav.append(a["href"])

    def handle_endtag(self,tag):
        if tag=='head':self._in_head=False


def run(context):
    assert context in ("production","deploy-preview","branch-deploy")
    preview_enabled = context == "deploy-preview"
    expected_pages = EXPECTED | ({R31_ROUTE+"/index.html"} if preview_enabled else set())
    actual={p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html")}
    assert actual==expected_pages, f"Unexpected/missing route: extra={actual-expected_pages}, missing={expected_pages-actual}"
    preview_root = OUT / R31_ROUTE
    if preview_enabled:
        actual_preview = {p.relative_to(preview_root).as_posix() for p in preview_root.rglob("*") if p.is_file()}
        assert actual_preview == set(R31_FILES), f"R3.1 file allowlist mismatch: {actual_preview ^ set(R31_FILES)}"
        assert (preview_root/"assets/origin.mp4").stat().st_size < 3_000_000, "Web video budget exceeded; do not deploy master"
    else:
        assert not preview_root.exists(), "R3.1 is only allowed in deploy-preview"
    public_media = OUT / "assets/r31"
    actual_media = {p.relative_to(public_media).as_posix() for p in public_media.rglob("*") if p.is_file()}
    assert actual_media == set(R31_PUBLIC_FILES), "Public R3.1 asset allowlist mismatch"
    assert (public_media / "origin.mp4").stat().st_size < 3_000_000, "Public video budget exceeded; do not deploy master"
    allowed_videos = {"assets/r31/origin.mp4"} | ({"r31-review/assets/origin.mp4"} if preview_enabled else set())
    assert {p.relative_to(OUT).as_posix() for p in OUT.rglob("*.mp4")} == allowed_videos, "Unapproved video in release"
    pages={rel:Scan((OUT/rel).read_text(encoding="utf-8")) for rel in expected_pages}
    checks=0
    for rel,page in pages.items():
        assert page.h1==1 and page.titles==1 and len(page.desc)==1 and page.desc[0], f"{rel}: title/H1/description"
        expected=CANON+("/" if rel in ("index.html","mobile/index.html",R31_ROUTE+"/index.html") else "/"+rel.removesuffix("index.html"))
        assert page.canon==[expected], f"{rel}: canonical {page.canon} vs {expected}"
        assert len(page.ids)==len(set(page.ids)), f"{rel}: duplicate IDs"
        assert not page.errors, f"{rel}: {page.errors}"
        if rel in ("index.html", "mobile/index.html", R31_ROUTE+"/index.html"):
            assert len(page.source_commits)==1 and re.fullmatch(r"[0-9a-f]{40}", page.source_commits[0]), "R3.1 source commit marker missing or invalid"
        source=(OUT/rel).read_text(encoding="utf-8")
        for value in BUSINESS:
            assert value in source, f"{rel}: visible business details missing: {value[:3]}"
        assert "footer-legal" in source and "business-info" in source, f"{rel}: legal footer not visible"
        assert "href=\"/preview/\"" not in source, f"{rel}: internal preview link leaked"
        assert set(("/services/","/research/","/work/weplace/","/signal-studio/","/about/")).issubset(set(page.nav)), f"{rel}: common nav missing"
        if context=="production":
            assert not page.robots or not any("noindex" in x.lower() for x in page.robots), f"{rel}: unintended production noindex"
        else:
            assert len(page.robots)==1 and "noindex" in page.robots[0], f"{rel}: review noindex missing"
        for ref in page.links:
            url=urlsplit(ref)
            if url.scheme or url.netloc or ref.startswith("//"):continue
            target=OUT/unquote(url.path).lstrip("/") if url.path.startswith("/") else (OUT/rel).parent/unquote(url.path)
            if not url.path:target=OUT/rel
            target=target.resolve()
            assert target.is_relative_to(OUT.resolve()), f"{rel}: link leaves public root: {ref}"
            if target.is_dir():target=target/"index.html"
            assert target.is_file(), f"{rel}: broken local path {ref}"
            if url.fragment and target.suffix==".html":
                dest=target.relative_to(OUT.resolve()).as_posix()
                assert dest in pages and unquote(url.fragment) in pages[dest].ids, f"{rel}: broken fragment {ref}"
        checks+=1
    home=(OUT/"index.html").read_text(encoding="utf-8")
    assert pages["index.html"].chapters==["origin","research","field","invitation"],"Four scene IDs"
    assert 'id="opening-title"' in home and "왜 잠시 멈췄을까요?" in " ".join(re.sub(r"<[^>]+>", " ", home).split()) and 'href="/services/"' in home
    for rel in ("index.html", "mobile/index.html"):
        source=(OUT/rel).read_text(encoding="utf-8")
        assert "DESIGN PREVIEW" not in source and "검토본</title>" not in source, "Review label in public homepage"
        assert '/assets/r31/origin.mp4' in source and '/assets/r31/origin.webp' in source
        assert 'id="origin-video"' in source and 'data-research-step="next"' in source
    notes=(OUT/"research/notes/index.html").read_text(encoding="utf-8")
    studio=(OUT/"signal-studio/index.html").read_text(encoding="utf-8")
    assert "2026.05.11" in notes and "https://mashcore-market-notes.netlify.app/" in notes
    assert "Gate 0" in studio and "Mock" in studio and "미검증" in studio
    assert (OUT/"research/index.html").read_text(encoding="utf-8").count('id="research-public-paths"')==1
    assert all("LEDGER" not in (OUT/x).read_text(encoding="utf-8").upper() for x in expected_pages)
    assert not any(x.name.startswith("hero-desktop") or x.name.startswith("hero-mobile") for x in OUT.rglob("*")),"Unapproved generated hero found"
    assert not (OUT/"preview").exists()
    for path in OUT.rglob("*"):
        rel=path.relative_to(OUT)
        assert not FORBIDDEN.intersection(rel.parts), f"Private/source directory published: {rel}"
        assert not path.name.startswith("."), f"Dotfile published: {rel}"
        if path.is_file(): assert path.suffix not in (".py",".md",".env",".zip",".map",".pem",".key"), f"Source artifact published: {rel}"
    xml=ET.parse(OUT/"sitemap.xml")
    locs=[e.text for e in xml.iter() if e.tag.endswith("loc")]
    robots=(OUT/"robots.txt").read_text(encoding="utf-8")
    if context=="production":
        assert len(locs)==13 and all(str(v).startswith(CANON+"/") for v in locs),"Production sitemap URLs"
        assert all((OUT/(v.removeprefix(CANON).lstrip("/") or "index.html")).is_file() or
                   (OUT/(v.removeprefix(CANON).lstrip("/"))/"index.html").is_file() for v in locs),"Production sitemap missing pages"
        assert "Allow: /" in robots and "Disallow: /" not in robots
        assert not (OUT/"_headers").exists(),"Review noindex headers leaked into production"
    else:
        assert not locs,"Draft sitemap must be empty"
        assert "Allow: /" in robots and "Disallow: /" not in robots
        assert "X-Robots-Tag: noindex" in (OUT/"_headers").read_text(encoding="utf-8"),"Draft header noindex missing"
    print(json.dumps({"result":"PASS","context":context,"pages":len(expected_pages),"checked_page_shells":checks,
         "sitemap_urls":len(locs),"r31_preview_included":preview_enabled,
         "r31_allowlisted_files":len(R31_FILES) if preview_enabled else 0,
         "approved_public_r31_assets":len(R31_PUBLIC_FILES),
         "legacy_preview_excluded":True},ensure_ascii=False))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--context",required=True,choices=("production","deploy-preview","branch-deploy"))
    args=parser.parse_args()
    run(args.context)
