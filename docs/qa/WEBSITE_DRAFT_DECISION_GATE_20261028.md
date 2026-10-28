# MASHCORE Website Draft · Decision Gate / 2026-10-28

**Purpose:** Present an explicit next-choice recommendation after the actually implemented PR #9 and Chromium browser review. This document does not approve a public launch.

## Version and evidence

- Implementation SHA tested: ea2ba5887f9e1eb3257d0da7e94637d1ad8af691.
- Browser Run: https://github.com/HotCharliepepper/Mashcore/actions/runs/40638511881
- Result: 114 PASS, 0 FAIL, screenshots + result.json uploaded to artifact 12794851680.
- Draft PR: https://github.com/HotCharliepepper/Mashcore/pull/9
- Preview: https://deploy-preview-9--mashcore.netlify.app/?hero=reverse
- Existing main and production deploy unchanged during this work.

## Decisions by scope

| Gate | Evidence status | Decision for this Draft | Still needs approval/evidence |
|---|---|---|---|
| R01 · Existing Hero A vs Reverse B | Both have actual code; B screenshot 1440/390 and A/B switching passed browser test. No measured human comprehension or conversion evidence. | **KEEP BOTH.** B is the preferred comparative Preview link; A remains original default and rollback baseline. | Final public choice after human first-understanding test, actual scene asset rights and mobile editorial review. |
| R02 · Motion tools and speed | Existing SVG/CSS/JS worked in tested screenshots/controls and reduced-motion simulation. | **KEEP EXISTING IMPLEMENTATION.** No GSAP migration. | Motion-duration experiment only if visual review identifies a real comprehension problem. |
| R03 · Visual system | Figma 02 System and P01 reviewed; new panels use scoped paper/forest/brass editorial layers, no existing tokens replaced. | **KEEP scoped CSS** pending final CI/asset approval. | Final brand typography, CI asset provenance, 200% native zoom, physical device QA. |
| R04 · LAB/NOTES public entries | New routes and old research hub links return 200 and pass navigation/metadata checks. Market original is dated 2026-05-11. | **KEEP separate LAB and NOTES pages.** Preserve existing study originals and market URL; do not migrate. | Approval of first new original note and publication date/source record. |
| R05 · Signal Studio page | R2.1 described accurately as local Gate 0; current Mock/API/manual posting boundaries visible. | **KEEP informational introduction**, no signup/payment/autopost CTA. | Real pilot, authentication/files, rights and operating support before public product claims. |
| R06 · GEO/search surface | Current Draft noindex HTTP and meta confirmed, robots now permits reading noindex, draft sitemap empty, canonical source mapped. | **KEEP review noindex**; new paths are candidate public pages only, not yet published production pages. | At release, site production sitemap/links/canonical and Search Console inspection, no guaranteed AI citations. |
| R07 · Inquiry and prices | Mail draft/copied message works. No mail delivered; two historical price tracks remain review-only, VAT/terms not approved. | **KEEP email/copy**; do not add an untested server form or payments. | User-approved recipient/delivery test, scope/VAT/contracts/rights before sales launch. |
| R08 · Weplace responsibility | Collaboration and independent external destination remain; no shared CRM/account behavior introduced. | **KEEP independent relationship** and separate inquiry/commercial ownership. | Any actual case and photos require proof of contribution and separate public permission. |
| R09 · Generated hero and other imagery | Concept poster is visibly labeled AI; rights_verified=false and public_use_approved=false in source. | **KEEP FOR DRAFT REVIEW ONLY.** Do not promote permission flags. | Use independently licensed/consented real scenes or separately approved assets before production. |
| R10 · Mobile page length | Full Chrome screenshot at 390px is about 13,716px tall. This is a layout measurement, not a human behavior outcome. | **EDITORIAL HYPOTHESIS:** make a comparative condensed cut after the user reviews this working version. Preserve all source/long-form routes. | Decide which repeated home explanations to consolidate through visual comparison; no conversion claim. |

## User review sequence (recommended)

1. Compare [B desktop/mobile visual evidence](https://github.com/HotCharliepepper/Mashcore/actions/runs/40638511881/artifacts/12794851680) and inspect home A vs B in the live Draft. Mark the first question, role, CTA and first scroll point for copy adjustments. Do not choose a winner from code existence alone.
2. Read LAB, NOTES, Studio and services as a stranger: Is each page a clear answer to a business owner's question, and does its next action match what the app can actually do?
3. Decide asset/public-rights and service terms before requesting a production proposal. Preserve PR #9 as a rollback-capable review baseline.

## Unperformed and protected boundaries

- No genuine physical device/screen reader test, real browser Ctrl+plus zoom, live network/CPU throttling, production RUM/Core Web Vitals, 5-second human comprehension study, SEO indexing confirmation.
- No main merge, production publish, DNS, real DB/auth permission changes, payments, client data migration, actual social posting, email sending, Search Console/GBP write or Figma original edits.
- The Graphical browser/CI pass is not user approval of final copy, hero imagery, client example, license, fee or results.

## Weplace handoff

The new homepage bridge identifies Mashcore's judgment/design role, Weplace's independent on-site execution role and Studio's local prototype. Weplace's operating homepage and customer records were not changed. A future joint example requires exact roles, source and public permission; this review does not authorize one.
