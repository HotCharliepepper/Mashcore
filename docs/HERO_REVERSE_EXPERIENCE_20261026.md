# MASHCORE HERO REVERSE EXPERIENCE · R3 Review · 2026-10-26

Status: PROPOSED / DRAFT REVIEW ONLY. Child branch of Experience R2 PR #6 HEAD b0aeca2946701b25a32c34a66f58eac412b1b416. PR #2 is kept open separately. Do not merge main or deploy production without approval.

## A/B experience (NOT a validated conversion test)
A retains the R2 hero, text, film, role, and service CTA. B keeps the same core information and actions while displaying a right-to-left SVG trace from the fictional person toward the explanation, plus a supplementary annotation. Korean is read normally. Comparison buttons have aria-pressed and a live status, with shareable ?hero=reverse URL state. This is distinct from the three-perspective Research section A/B.

## Reverse design from final action
Actual action: /services/ or invitation. Reassurance: scope, actual or clearly-labeled reconstructed work examples, independent inquiry. Self-discovery: customers pausing or re-checking missing information. First scene: a fictional person near a door. Trace symbolizes inquiry, not evidence of the fictional person's thoughts.

## Motion and fallback
The poster, H1, description, and CTA are visible from first paint. SVG runs in ~1.15 seconds once per B selection; only the supplementary question reveals from right to left. No new video autoplay or fixed delay. At <=900px the trace is omitted for a compact annotation. Reduced motion and save-data get a static B. No JS means original A and no inert controls. Existing hero-media.js independently handles all video lifecycle cases.

## Files
Modified: scripts/review_r2.py, scripts/build_public.py, netlify.toml.
New: assets/css/hero-reverse.css, assets/js/hero-reverse.js, scripts/check_hero_reverse.py, docs/HERO_REVERSE_EXPERIENCE_20261026.md.
Untouched: R2 media files/config, research/observations, six-perspective 3D, inquiry, service JSON, refund policy, business values.

## QA
In an isolated repo: python3 scripts/build_public.py --context deploy-preview && python3 scripts/check_public.py && python3 scripts/check_hero_reverse.py. Test the new Draft Preview at / (A) and /?hero=reverse (B). Verify 320/390/768/1440, keyboard Tab/Enter, title/CTA immediate visibility, JS off, reduced motion, video fallback, old Research A/B, inquiry and six-perspective 3D. Structural build checks are not eye-tracking, browser performance or conversion evidence.

## Status and remaining decisions
Code review and Netlify build results must be recorded separately. Physical mobile, screen reader, live user 5-second comprehension, actual footage rights, slow network, Core Web Vitals, Figma Motion edit, live email send and production deploy are NOT RUN until evidenced. No Weplace code, independent inquiry, DB, DNS or deployment changed.
