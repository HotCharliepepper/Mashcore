#!/usr/bin/env python3
"""Copy the confirmed public static site into a deploy-only allowlist.

The production main remains a static HTML/CSS/JS source. This reproducible
packaging step prevents docs, staging drafts, PR9 generated concept media and
internal assets from being uploaded as public web files.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "dist"
PUBLIC_DIRS = (
    "assets", "about", "explore", "mobile", "policies",
    "research", "services", "signal-studio", "work",
)
PUBLIC_FILES = ("index.html", "robots.txt", "sitemap.xml", "mashcore-profile.jpg")
R31_SOURCE = "experiments/r31-origin-research"
R31_ROUTE = "r31-review"
# Deliberate file-by-file boundary: never copy the experiments tree, source ZIP,
# master video, working notes, or new files merely because they share a folder.
R31_FILES = (
    "index.html", "styles.css", "app.js", "assets/origin.mp4",
    "assets/origin.webp", "assets/gsap.min.js",
)
# Approved for the public homepage by the user's 2026-10-28 deployment request.
# The historical experiment remains independently isolated to Deploy Previews.
R31_PUBLIC_FILES = ("styles.css", "app.js", "origin.mp4", "origin.webp", "gsap.min.js")
R32_PUBLIC_FILES = ("styles.css", "word-motion.js", "SplitText.min.js", "ScrollTrigger.min.js")
R32_REVIEW_TOOLS = '''<details class="r32-review" id="r32-review"><summary>R3.2 화면·워드 모션 비교</summary>
<nav aria-label="R3.2 비교 선택"><a href="?layout=before" data-r32-motion-choice="before">R3.1 기준</a>
<a href="?motion=calm" data-r32-motion-choice="calm">일반 · 1.25초</a>
<a href="?motion=slow" data-r32-motion-choice="slow">일반 · 1.4초</a>
<a href="?motion=still" data-r32-motion-choice="still">워드 정지</a>
<button type="button" data-r32-replay disabled>워드 다시 보기</button></nav>
<p data-r32-motion-status role="status">기기의 모션 감소·데이터 절약 설정을 우선합니다.</p></details>'''
FORBIDDEN_ROOTS = {"docs", "content", "scripts", "qa", ".git", ".github", "source-media", "project_sources", "experiments"}


def prepare(context: str) -> None:
    if context not in ("production", "deploy-preview", "branch-deploy"):
        raise ValueError("Unsupported public packaging context")
    if DEST.resolve() != ROOT.resolve() / "dist" or DEST.is_symlink():
        raise ValueError("Only the dedicated dist directory may be regenerated")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    public_media = ROOT / "assets/r31"
    if any(p.is_symlink() for p in (public_media, *public_media.parents, *public_media.rglob("*"))):
        raise ValueError("Symlink in public R3.1 assets")
    if {p.relative_to(public_media).as_posix() for p in public_media.rglob("*") if p.is_file()} != set(R31_PUBLIC_FILES):
        raise ValueError("Public R3.1 assets must match the approved allowlist")
    r32 = ROOT / "assets/r32"
    if any(p.is_symlink() for p in (r32, *r32.parents, *r32.rglob("*"))):
        raise ValueError("Symlink in R3.2 assets")
    if {p.relative_to(r32).as_posix() for p in r32.rglob("*") if p.is_file()} != set(R32_PUBLIC_FILES):
        raise ValueError("R3.2 assets must match the explicit allowlist")
    for name in PUBLIC_DIRS:
        src = ROOT / name
        if not src.is_dir():
            raise ValueError("Expected public source directory: " + name)
        shutil.copytree(src, DEST / name,
                        ignore=shutil.ignore_patterns("*.map", "*.md", ".DS_Store", "__pycache__", "node_modules"))
    for name in PUBLIC_FILES:
        src = ROOT / name
        if not src.is_file():
            raise ValueError("Expected public source file: " + name)
        shutil.copy2(src, DEST / name)

    if context == "deploy-preview":
        preview_source = ROOT / R31_SOURCE
        for name in R31_FILES:
            src = preview_source / name
            # Reject symlinks in every path component, including the source root.
            if any(part.is_symlink() for part in (src, *src.parents)):
                raise ValueError("Symlink in R3.1 source: " + name)
            if not src.is_file():
                raise ValueError("Missing allowlisted R3.1 source: " + name)
            target = DEST / R31_ROUTE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    commit = os.environ.get("COMMIT_REF") or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("R3.1 requires a full source commit SHA")
    marked_pages = [DEST / "index.html", DEST / "mobile/index.html"]
    if context == "deploy-preview":
        marked_pages.append(DEST / R31_ROUTE / "index.html")
    for page in marked_pages:
        html = page.read_text(encoding="utf-8")
        html = html.replace("</head>", f'<meta name="r31-commit" content="{commit}"></head>', 1)
        page.write_text(html, encoding="utf-8")

    # /preview/ is an internal review tool, not a public destination.
    assert not (DEST / "preview").exists()
    for path in DEST.rglob("*"):
        rel = path.relative_to(DEST)
        if FORBIDDEN_ROOTS.intersection(rel.parts) or path.name.startswith("."):
            raise ValueError("Source/private data in release: " + str(rel))
        if path.is_file() and path.suffix in (".md", ".py", ".zip", ".env", ".map", ".key", ".pem"):
            raise ValueError("Non-public source file: " + str(rel))

    if context != "production":
        # noindex must remain readable, not blocked by robots.txt.
        (DEST / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
        (DEST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n',
            encoding="utf-8")
        (DEST / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")
        for path in DEST.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            text = text.replace("<!-- R32_REVIEW_TOOLS -->", R32_REVIEW_TOOLS)
            if '<meta name="robots"' not in text and '<meta content="noindex' not in text:
                text = text.replace("</head>", '<meta name="robots" content="noindex,nofollow"></head>', 1)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--context", required=True, choices=("production", "deploy-preview", "branch-deploy"))
    args = cli.parse_args()
    prepare(args.context)
    print("Public site packaged; context="+args.context)
