# MASHCORE Website Draft · 2026-10-28 QA & Handoff

> **Follow-up available:** The initial NOT RUN items below are historical. The later 2026-10-28 automated Chromium run #40638511881 checked the specified browser items; physical devices, native 200% zoom, actual user comprehension and mail delivery remain NOT RUN. Details at the end.

**Status:** CODE PRESENT / DRAFT PREVIEW READY / PRODUCTION NOT APPLIED  
**Scope:** Follow-up to PR #8 on an independent branch. Not a production release or content-rights approval.

## Source / deployment evidence

- Original #8 HEAD: `7fdb37aee8d49f9d61111c3a503d22fc839abed0`.
- Implementation HEAD tested by Netlify: `d8486a5cb514c14b9f9c78ae3258a226bd8eefba`.
- Follow-up branch: `review/mashcore-website-draft-20261028`; new Draft PR #9: https://github.com/HotCharliepepper/Mashcore/pull/9.
- Netlify deploy ID: `6ae17e4ddc4f7e9fd1baf351`; context `deploy-preview`; state `ready`; `published_at=null`; matching `commit_ref`.
- Aliased preview: https://deploy-preview-9--mashcore.netlify.app/
- Immutable implementation preview: https://6ae17e4ddc4f7e9fd1baf351--mashcore.netlify.app/
- GitHub combined status: `netlify/mashcore/deploy-preview: success`.
- Existing production Netlify deploy remained `6adb113e296767181eb98f02` at last read; main remains `b31a55cea32cd83113624f9cdc27bd8d8bc36926`.
- Prior original Draft PR #2/#6/#7/#8 and their branches were not modified.

## New code relative to exact PR #8 HEAD

| File | Change |
|---|---|
| `scripts/review_integrated.py` | New LAB, NOTES, Studio standalone page HTML and home research/field content bridges. |
| `assets/css/review-integrated.css` | Existing editorial system-compatible responsive styling, static accessibility and reduced-motion handling. |
| `scripts/build_public.py` | Wire new content into original four home scene IDs, generate routes, shared navigation/footer, CSS and sitemap. |
| `content/seo.json` | Unique title, meta description and search-intent candidates for each new page. |
| `scripts/check_public.py` | Enforce 15 generated routes, navigation/links, original Market URL/date, local Studio limitations, inquiry and no Ledger public description. |

**No changes to:** `content/strategy.json`, `content/hero-media.json`, existing Hero CSS/JS, research 3D controls, services pricing, policy body, business configuration, source photos/video.

## Tests and what they actually establish

| Dimension | This run's evidence | Status |
|---|---|---|
| Build `scripts/build_public.py --context deploy-preview` | New Netlify deploy ready, no build error, reported 15 generated pages | PASS (remote build) |
| Static page validator `scripts/check_public.py` | Included unchanged in Netlify deploy-preview build command; deploy completed successfully | PASS (remote build) |
| Reverse hero contract `scripts/check_hero_reverse.py` | Included unchanged in Netlify deploy-preview build command; deploy completed successfully | PASS (remote build) |
| New routes generated | Netlify deploy summary mentions new routes; source generator creates three concrete pages | CONFIRMED in deploy |
| Preview indexing guard | Build script writes draft robots.txt disallow, site-wide X-Robots-Tag noindex and page meta; source inspected | CODE VERIFIED; direct HTTP headers NOT RUN |
| Rights guard | `content/hero-media.json`: `rights_verified=false`, `public_use_approved=false`, explicit AI concept label | CODE VERIFIED; not public use approval |
| Secrets | Netlify deploy validation scanned 180 files, zero secret scan matches | SCANNER RESULT; not an exhaustive privacy audit |
| Market Notes | Date label 2026-05-11, original external URL in generated review content | CODE VERIFIED; source report not revalidated as current analysis |
| Signal Studio | Local Gate 0, mock/disabled services and manual posting are expressly stated | CODE VERIFIED; no customer pilot |
| 320/390/768/1440 browser layout, H1 and CTA visual fold | No remote graphical browser available this run | NOT RUN |
| Keyboard, focus order, menu Escape, 200% zoom | Browser/assistive technology test unavailable | NOT RUN |
| JS disabled, video/poster failure, OS reduced-motion and save-data | New live failure simulations unavailable; inherited earlier #8 QA is not this run | NOT RUN |
| Lighthouse / INP / real device | No actual measurements or devices in this run | NOT RUN |
| Inquiry email delivery | Neither mail sent nor server endpoint added | NOT RUN / not implemented |

## Figma mapping (read only)

- Existing Design file: https://www.figma.com/design/e2C0JjYTRiwiW9Fxh3f8X7
- `02 — System & Handoff` start node `3:136`: paper `#f4efe6`, forest `#18241c`, brass `#a6885a`, ink `#20261f`; Gowun Batang heading / Noto Sans KR body. These inform a separate scoped CSS layer without replacing original code tokens.
- `06 — HERO REVERSE` and `P01 — Motion Card` node `57:179`: original CSS/SVG motion and poster/stop/failure logic retained. No Figma files or variables edited.

## Reader path and content boundaries

- Four home scenes preserve their IDs: `origin/research/field/invitation`.
- `/research/lab/`: observation, evidence, interpretation, counterexample, next decision; hypothetical scene explicitly labeled; Limbic® as research reference, no inferred brain state/validated conversion score.
- `/research/notes/`: existing research and 2026-05-11 historical Market Notes external original; no fabricated CMS/current market facts.
- `/signal-studio/`: Owner-First R2.1 documented local prototype, not a live SaaS or auto-post service.
- `/services/`, `/research/`, `/about/`, `/work/weplace/`, refund/policy, six Chore to Play lenses, original A/B and independent inquiry remain.
- No Ledger pages, private source bundles, client uploads or real financial records added to public build.
- Inquiry mail-app open and copy actions must not be described as verified message delivery.
- Relative source-generated canonical/sitemap paths target the eventual official hostname but do not mean new routes are published on production; draft remains noindex.

## Pending decisions / next checks

1. Use a real graphical browser for screenshot and interaction QA at 320/390/768/1440, 200% zoom, keyboard, reduced motion, media errors; record actual URL/OS/test and fix regressions before public approval.
2. Review language/CI and replace generated concept hero or third-party references only with cleared assets; retain current `public_use_approved=false`. Select final Hero A/B only after actual comprehension tests.
3. Validate prices/VAT/service scope, approved notes, Studio external pilot status and contact delivery; plan a *separately approved* public release with canonical/sitemap and Search Console review.

## Weplace handoff

The `/work/weplace/` page and existing external link to https://withweplace.kr/ remain intact. New home bridge explains independent strategic-design versus field-execution responsibilities; no shared identity, account, CRM, payment, customer records or actual Weplace code change. Continue to require project-specific rights/role verification.

**Guardrail:** No main merge, production deploy, DNS, PG, real database, customer data migration or social posting was performed.


## Live Chromium follow-up — 2026-10-28

This section supplements and preserves the initial report above.

- Branch: review/mashcore-website-draft-20261028 (Draft PR #9).
- Exact code SHA tested: ea2ba5887f9e1eb3257d0da7e94637d1ad8af691.
- [GitHub Actions run #40638511881](https://github.com/HotCharliepepper/Mashcore/actions/runs/40638511881) concluded success.
- [114-check JSON and screenshots, artifact ID 12794851680](https://github.com/HotCharliepepper/Mashcore/actions/runs/40638511881/artifacts/12794851680).
- Automated result: **114 PASS / 0 FAIL** in headless Chromium 143, Ubuntu 24.04, Playwright 1.57.0.
- Tested actual Draft: https://deploy-preview-9--mashcore.netlify.app/ (not production).
- That code commit's netlify/mashcore/deploy-preview status was success; production code/deploy not changed.

### Verified browser behavior

| Group | This run |
|---|---|
| Home 320/390/768/1440 CSS px | HTTP 200, one H1, visible service CTA, four scene IDs, LAB/NOTES/Studio paths, no horizontal overflow, no runtime page errors |
| Navigation | At 320/390 the menu opens and Escape closes; 768 displays the authored desktop navigation rather than a menu. |
| Hero | A/B switches in the desktop browser, preserving role/CTA. Mobile B question/CTA precedes concept image. |
| Detail routes | LAB / NOTES / Studio / services / research / about / work-Weplace / refund all returned 200, single H1, canonical matching future public URL, and Draft noindex meta + header. |
| Research | Three observation situations, switching to B, and all six Chore-to-Play perspectives work. |
| Inquiry | Typed message updates mailto draft; copy feedback explicitly confirms no message was sent. Email sending was not triggered. |
| Alternate modes | JS disabled, media request failure, reduced-motion emulation and touch mobile preserve H1 and CTA. |
| 200% reflow proxy | 400 CSS-px viewport / doubled device-pixel ratio approximates responsive reflow; no overflow. Not genuine browser-native zoom. |
| Preview search boundaries | Draft robots permits crawler access to the noindex directive, Draft sitemap contains no unapproved URL, and X-Robots-Tag noindex is present. |
| Content provenance | Existing 2026-05-11 Market Notes original linked; Studio Gate 0 and Mock limits shown; no payment CTA added. |

### Real screenshot review

- Desktop 1440 B: readable question, role, CTA and separate generated-concept label.
- Mobile 390 B: clear question -> role -> CTA -> image order, no horizontal overflow.
- LAB/NOTES/Studio: consistent editorial palette and type, meaningful HTML explanations, visible dates/limitations.
- **Editorial review candidate:** full mobile home screenshot is about 13,716 px high. Consider consolidating repeated explanations in a subsequent copy/layout revision. This is a screen-density observation, not measured reader fatigue or conversion decline.

### Remaining untested or unapproved

- Actual physical iOS/Android devices, screen readers, keyboard accessibility with assistive technology, native browser Ctrl+plus zoom, real OS preference switching.
- Slow CPU/network, production Core Web Vitals field measurement (75th percentile), actual 5-second comprehension or A/B conversion test.
- Message delivery, server-side inquiry receipt, purchases, real customer data, live social posting.
- Commercial public rights for the existing AI concept hero are not approved. In source: rights_verified=false and public_use_approved=false.
- Brand copy, customer/field photographs, price basis and VAT, Notes publication, Studio external pilot, final Hero choice and operating release remain OPEN.

### Follow-up changes

- Connected old research index directly to new LAB and NOTES, leaving original research intact.
- Updated Draft robots/noindex interaction based on [Google's official noindex guidance](https://developers.google.com/search/docs/crawling-indexing/block-indexing); Draft sitemap excludes unapproved routes.
- Added isolated PR #9-only Chromium QA workflow and script, collecting screenshots/JSON but no customer actions.
- The first Chromium run was **100/102** due to a wrong assumed menu breakpoint and an invalid document CSS zoom simulation. QA logic was corrected, and the later run passed **114/114**. Initial failures remain in the run history and are not mislabeled as site bugs.

**Final meaning:** Code present + successfully deployed review Preview + automated Chromium QA passed. Not a merged/published website or customer-validated public release.
