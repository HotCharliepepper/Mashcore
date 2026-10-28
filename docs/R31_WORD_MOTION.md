# R3.1 Word Motion integration

Base: `a8dae1c4b6e69cd02e24b5e28bc9600f5a756fcf` (main observed 2026-10-28 KST).
Work branch: `codex/r31-word-motion-20261028`. No main merge or production deployment.

## Behavior

The existing Origin H1, role paragraph, CTA, and Research H2 are unchanged. Two
data attributes opt those headings into a new, independent `word-motion.js`.
The original `assets/r31/app.js` and `gsap.min.js` bytes are unchanged: existing
signal-line, research-panel and video state management remain their owners.

Default experiment: duration **0.85s**, word stagger **0.18s**, vertical offset
**8px**, power2.out. These values are grouped in one immutable configuration.
Origin starts as readable static HTML, followed by a small word settle and color
emphasis. Research runs once on viewport entry, without pre-splitting content
below the viewport. No opacity-zero, visibility-hidden, masks, pinning, scrub,
or forced scrolling is applied. Every word remains readable during playback.
Colors differ between the ivory mobile Origin and dark sections.

The earlier local `mashcore-motion-lab-retry` exercise and backup were accessible.
Its Timeline/SplitText sequencing principle was inspected. This is a new module
adapted to the current official markup, not a claim that the old code was copied.
It uses **words**, rather than the historical chars/words mismatch.

## Dependencies and lifecycle

Existing GSAP core, vendored SplitText and ScrollTrigger are all **3.15.0**.
Vendor files came from the installed GSAP 3.15.0 distribution, with copyright and
license headers retained. The module loads only the two required plugins, from
same-origin files, after checking reduced-motion and saveData. It does not load
a second core or a remote CDN. Version mismatch, core/plugin failure, timeout,
or font-readiness timeout leaves the original static copy intact.

Only this module's timelines, split wrappers and ScrollTrigger are cleaned up.
It never calls killAll, clears the global timeline, or changes app.js state.
Split wrappers are reverted after completion, width changes, preference changes,
page hiding and navigation. Korean spaces, explicit br/em markup, heading roles
and the accessible name are preserved. No added word wrapper is a focus target.

## Source versus publish output

- `index.html` is the source. `scripts/sync_mobile.py` regenerates the mobile URL
  with the existing mobile title and root canonical. Explicit UTF-8 I/O was added.
- `prepare_public.py` extends the existing strict public R3.1 asset allowlist by
  exactly four files: word-motion.js, word-motion.css, SplitText.min.js,
  ScrollTrigger.min.js. Unlisted files still fail packaging.
- The historical `experiments/r31-origin-research` and its six-file preview-only
  route are unchanged. Docs, QA source/evidence and private files never enter dist.
- Existing production, branch-deploy, and deploy-preview boundaries, commit
  markers and noindex rules remain in effect.

## Validation and evidence

Local checks: source link/semantic checks; all three release contexts; immutable
app/core hashes; exact copy/CTA and mobile synchronization; source/dist hooks;
JavaScript/Python syntax. The packaging boundary suite passed 9 tests locally;
the symlink-negative test could not create its symlink on Windows (WinError
1314). The CI Linux run exercises all ten tests without changing OS privileges.

The dedicated PR workflow checks the exact Netlify Preview commit before browser
testing. `qa/r31_word_motion.py` covers homepage and `/mobile/` at 320/390/768/1440,
Korean copy/wrapping, initial and final CTA readability/position, CLS versus a
module-disabled baseline, resource timing, one-time Research playback, keyboard,
menu, research panels, inquiry draft, existing video UI, reduced-motion/saveData,
mid-motion resize/preference changes, JS/core/module/plugin failure and a WebKit
390px sample. It never sends an inquiry or clicks mailto. Screenshots, metrics,
checks and summary are retained in a GitHub Actions artifact, outside public dist.
Actual results and exact-commit Preview/Actions links belong in the Draft PR.

NOT RUN by this suite: physical iPhone/Android, a screen-reader user session,
field Core Web Vitals, Lighthouse/throttled lab score. Browser emulation, measured
CLS/resource timings and a WebKit sample do not establish those outcomes.

Technical references: [SplitText](https://gsap.com/docs/v3/Plugins/SplitText/),
[ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/).
