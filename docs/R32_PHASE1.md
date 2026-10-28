# R3.2 Phase 1 — mobile observation and word motion

Baseline main: `a8dae1c4b6e69cd02e24b5e28bc9600f5a756fcf`.
PR #14 reference: `5b87eec9a2d4181865444548b2e41f2fcbf62091`.
Branch: `codex/r32-phase1-20261029`. Existing Drafts and both local R3.1
worktrees remain unchanged. No main merge, production deployment or DNS action.

## Implemented experience

The Origin question, role, CTA and approved Runway scene remain the same. At
mobile/tablet widths, an observation frame is visually placed just before the
question; forest background, ivory copy and gold accents continue below it.
The media keeps an explicit size and poster so video failure or delayed loading
cannot collapse the layout. The original DOM reading sequence and links remain.
The primary CTA, complete media frame and question are tested within the first
viewport at 320/390/768. Desktop retains the R3.1 cinematic composition.

PR #14's optional SplitText/Timeline/ScrollTrigger implementation was adapted
into `assets/r32/word-motion.js`. Default slow is 1.4s per word; calm is 1.25s,
both with 0.18s stagger and 8px settle plus sequential color emphasis. No word
starts hidden or clipped. Research playback remains one-time on entry. All
temporary wrappers are reverted after completion or width/preference changes.
GSAP core and both plugins are 3.15.0. The existing core and R3.1 app/style bytes
are unchanged. No global timeline clearing, scroll hijack or second core.

## Review controls

The preview packaging inserts a small disclosure after Origin. Its links are:

- `?layout=before` — R3.1 layout and no added word motion.
- `?motion=calm` — 1.25s word motion.
- `?motion=slow` — 1.4s word motion (default).
- `?motion=still` — stop the added word motion; existing video controls remain.

Actual OS reduced-motion and saveData always win and skip plugin requests.
An explicit replay button restarts only this module, preserving app.js state.
These controls are included in preview/branch artifacts and omitted from the
production packaging. No-JS retains the poster, all copy, CTA and native links;
the replay button stays disabled. The original JS-off navigation fallback is
given its own row to keep it away from the question.

## Preserved contracts

Four chapter IDs, Research selection, six-lens spatial model, inquiry draft,
business information, all detail pages, canonical/OG/JSON-LD and mobile route
remain. `scripts/check_r32.py` checks those invariants against main and the
generated output. `sync_mobile.py` uses explicit UTF-8. R3.1's five-file media
allowlist is unchanged; R3.2 has a separate exact four-file allowlist. Docs,
QA, source and private files remain outside dist. Preview stays noindex.

## QA and evidence

Local work uses `prepare_public.py --context deploy-preview` followed by the
release and R3.2 checks. The dedicated PR workflow additionally exercises the
temporary packaging boundary tests and existing inquiry/spatial regressions.
It checks the exact Preview commit before Chromium 320/390/768/1440 on `/` and
`/mobile/`, plus WebKit 390. It captures same-viewport Before/After screenshots,
mid-animation transforms/colors, 1.25/1.4/still modes, reduced-motion/saveData,
JS/core/plugin/video failures, real video pause/play and CTA navigation. It
records CLS, resource timings, Korean font status and existing inquiry/research
state without sending any form or email. Artifacts remain in CI, not dist.

Actual results/Preview/artifact links are recorded in the Draft PR after CI.
NOT RUN by this suite: physical iPhone/Android, screen-reader user sessions,
field Core Web Vitals, Lighthouse or controlled throttling scores. One CI
sample does not establish usability, conversion uplift or production speed.
