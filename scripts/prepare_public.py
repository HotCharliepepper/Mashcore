#!/usr/bin/env python3
"""Copy the confirmed public static site into a deploy-only allowlist.

The production main remains a static HTML/CSS/JS source. This reproducible
packaging step prevents docs, staging drafts, PR9 generated concept media and
internal assets from being uploaded as public web files.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "dist"
PUBLIC_DIRS = (
    "assets", "about", "explore", "mobile", "policies",
    "research", "services", "signal-studio", "work",
)
PUBLIC_FILES = ("index.html", "robots.txt", "sitemap.xml", "mashcore-profile.jpg")
FORBIDDEN_ROOTS = {"docs", "content", "scripts", "qa", ".git", ".github", "source-media", "project_sources"}


def prepare(context: str) -> None:
    if context not in ("production", "deploy-preview", "branch-deploy"):
        raise ValueError("Unsupported public packaging context")
    if DEST.resolve() != ROOT.resolve() / "dist" or DEST.is_symlink():
        raise ValueError("Only the dedicated dist directory may be regenerated")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
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
            if '<meta name="robots"' not in text and '<meta content="noindex' not in text:
                text = text.replace("</head>", '<meta name="robots" content="noindex,nofollow"></head>', 1)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--context", required=True, choices=("production", "deploy-preview", "branch-deploy"))
    args = cli.parse_args()
    prepare(args.context)
    print("Public site packaged; context="+args.context)
