#!/usr/bin/env python3
"""Exercise R3.1 packaging in temporary repositories, including negative cases.

Uses real source files without modifying the checkout's dist/ or experiment.
Run after the R3.1 source and its six review assets are present.
"""
from contextlib import redirect_stdout
from io import StringIO
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import prepare_public as pack
import check_release as release

SOURCE = Path(__file__).resolve().parents[1]
REVIEW_FILES = {"index.html", "styles.css", "app.js", "assets/origin.mp4",
                "assets/origin.webp", "assets/gsap.min.js"}


class PreviewBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mashcore-r31-boundary-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in pack.PUBLIC_DIRS:
            shutil.copytree(SOURCE / name, self.root / name)
        for name in pack.PUBLIC_FILES:
            shutil.copy2(SOURCE / name, self.root / name)
        shutil.copytree(SOURCE / pack.R31_SOURCE, self.root / pack.R31_SOURCE)
        self.out = self.root / "dist"
        for module, key, value in ((pack, "ROOT", self.root), (pack, "DEST", self.out),
                                    (release, "ROOT", self.root), (release, "OUT", self.out)):
            p = patch.object(module, key, value)
            p.start()
            self.addCleanup(p.stop)
        p = patch.dict(os.environ, {"COMMIT_REF": "a" * 40})
        p.start()
        self.addCleanup(p.stop)

    def checked_build(self, context):
        pack.prepare(context)
        with redirect_stdout(StringIO()):
            release.run(context)

    def test_contexts_and_clean_rebuild(self):
        # Preview followed by production must remove every previous review byte.
        for context in ("deploy-preview", "production", "branch-deploy"):
            with self.subTest(context=context):
                self.checked_build(context)
                review = self.out / "r31-review"
                self.assertEqual(review.exists(), context == "deploy-preview")
                self.assertEqual(len(list(self.out.rglob("*.html"))),
                                 15 if context == "deploy-preview" else 14)
                if context == "deploy-preview":
                    self.assertEqual({p.relative_to(review).as_posix()
                                      for p in review.rglob("*") if p.is_file()}, REVIEW_FILES)
                    self.assertIn('name="r31-commit" content="' + "a" * 40,
                                  (review / "index.html").read_text())
                if context == "production":
                    for name in pack.PUBLIC_FILES:
                        self.assertEqual((self.out / name).read_bytes(), (self.root / name).read_bytes())
                    for directory in pack.PUBLIC_DIRS:
                        for source in (self.root / directory).rglob("*.html"):
                            self.assertEqual(source.read_bytes(),
                                             (self.out / source.relative_to(self.root)).read_bytes())

    def test_unlisted_experiment_files_never_copy(self):
        source = self.root / pack.R31_SOURCE
        for name in ("master.mp4", "working-notes.txt", "private.json", "source.zip"):
            (source / name).write_text("not approved for deployment")
        self.checked_build("deploy-preview")
        self.assertFalse(any(p.name in {"master.mp4", "working-notes.txt", "private.json", "source.zip"}
                             for p in self.out.rglob("*")))

    def test_missing_asset_blocks_only_preview(self):
        (self.root / pack.R31_SOURCE / "assets/origin.mp4").unlink()
        with self.assertRaisesRegex(ValueError, "Missing allowlisted"):
            pack.prepare("deploy-preview")
        self.checked_build("production")
        self.checked_build("branch-deploy")

    def test_symlink_asset_rejected(self):
        target = self.root / pack.R31_SOURCE / "assets/origin.mp4"
        target.unlink()
        target.symlink_to(self.root / "index.html")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            pack.prepare("deploy-preview")

    def test_extra_review_output_rejected(self):
        self.checked_build("deploy-preview")
        (self.out / "r31-review/private.json").write_text("{}")
        with self.assertRaisesRegex(AssertionError, "allowlist mismatch"):
            release.run("deploy-preview")

    def test_oversize_master_rejected(self):
        self.checked_build("deploy-preview")
        with (self.out / "r31-review/assets/origin.mp4").open("wb") as f:
            f.truncate(3_000_000)
        with self.assertRaisesRegex(AssertionError, "budget exceeded"):
            release.run("deploy-preview")

    def test_review_leak_rejected_in_production_and_branch(self):
        for context in ("production", "branch-deploy"):
            with self.subTest(context=context):
                self.checked_build(context)
                leak = self.out / "r31-review"
                leak.mkdir()
                (leak / "styles.css").write_text("/* leaked experiment */")
                with self.assertRaisesRegex(AssertionError, "only allowed in deploy-preview"):
                    release.run(context)


if __name__ == "__main__":
    unittest.main(verbosity=2)
