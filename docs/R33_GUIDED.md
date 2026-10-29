# R3.3 guided reading — review only

Base: R3.2 `3da474ecf7783464d9cc3d9c9ee9e0d2ba07365f`.
Remote main checked immediately before work: `a8dae1c4b6e69cd02e24b5e28bc9600f5a756fcf`.
PRs 14 and 15 remain open Draft; no existing R3.3 branch was found.
Branch: `codex/r33-guided-experience-20261029`; separate worktree.

## Behavior

Three semantic phrases preserve the original H1, em, breaks and spaces. Default
starts/ends: 0–2.2, .9–3.1, 1.8–4.0 seconds. Comparison: 0–1.85,
.7–2.55, 1.4–3.25. Initial text remains visible; only y=14px and color animate.
SplitText's temporary delimiter/wrappers are removed on completion/interruption.
Explicit replay, immediate skip; no automatic replay after scroll/background.
Core app, media, detail pages, SEO and six Chore-to-Play perspectives are retained.

`?motion=slow` (default), `?motion=calm` (comparison), `?motion=still`;
`?scroll=free` and `?scroll=proximity`; all also work on `/mobile/`.
System reduced motion/data saving override motion selection.

Native CSS proximity is used because it does not intercept input. Only Origin
and Research can be targets, and only while both fit below the header. Short,
landscape, zoomed and long Research layouts fall back to ordinary scrolling.
The mode also disables on hashes, reduced motion, data saving and after leaving
the transition. Field/Invitation and the retained deeper research never snap.
No pin, scroll lock or delayed CTA. Preview controls are excluded in production
packaging, as before. This branch is not authorized for production publication.

## Media and rights

The same previously approved homepage `assets/r31/origin.webp` and `origin.mp4`
are retained unchanged; no new media or broader usage is introduced. Existing
allowlists and master-file exclusions remain. The visible hero label moves to
an accessible native footer disclosure: main video is AI concept staging,
not real customer footage/evidence. Poster alt still identifies the generated
scene. R3.2 docs and packaging record prior approval; no independent new legal
rights determination is made here.

## Validation and review criteria

Existing source/detail/SEO/mobile invariants and preview packaging pass locally.
Chromium and WebKit measured three phrase targets, default 4.0s and comparison
3.25s timelines, actual CTA navigation during motion, direct invitation without
snap, skip, scroll interruption, and 200% CSS zoom with no horizontal overflow.
Screenshots and measured JSON are in `qa/r33-evidence/` (not published).
`qa/r32_phase1.py` retains the prior regression matrix, adds 390x667 and landscape;
`qa/r33_guided.py` adds measured R3.3 checks. The CI runs both on the exact preview
commit and uploads evidence. Local Windows symlink boundary case cannot run
without symlink privilege; Linux CI must verify it. Do not interpret old R3.2 CI
as R3.3 validation.

NOT RUN: physical iPhone/Android, screen-reader user session, browser native
200% zoom (CSS zoom is tested), field CWV, actual conversion outcomes, mail
delivery or server submission. No real customer information or messages sent.

Review: choose 2.2/.90 vs 1.85/.70 and whether fitting-screen proximity adds value.
If wrapping/CTA reachability, motion preference, anchor escape or inquiry regresses,
keep Draft and fix forward/revert R3.3 in a new commit. No reset/force push,
main merge, production restore/deploy, DNS, database or payment changes.
