# MASHCORE current release provenance

This candidate packages the reviewed local **R069 VALUE FLOW R1** site with the official repository's deterministic static release contract. The old A20 commit is a deployment baseline, not the latest design source.

## Baseline and current source

- Official repository baseline: `5625881ece956b0133e8466cc7f708390e54de2a` (A20).
- Latest reviewed local artifact: `r069-value-flow-r1-20261120/preview`.
- Editable authoring source remains separately preserved as `source/frontend5207` in the release workspace, together with its build manifests and prior versions. It is not a public website route or a wholesale new public-repository upload.
- The public HTML, CSS, JS, media and font-license files at this repository's root are the canonical reviewed static source for the current release. `scripts/public_manifest.txt` declares the complete publication boundary.
- The new Git commit binds these public files, the release policy, and `scripts/release_lock.json`. The old local development HEAD is not used as the new candidate's commit identity.

## Reviewed module ownership

| Runtime module | Authoring/build owner | Reviewed SHA256 |
|---|---|---|
| `assets/home-a23-Byn7jaxj.js` | R066 source-module build, `becomes-home-entry.js`, existing 21 home modules | `809d860b53397148e7e378b64df706d00acb725de8ee0bbf56592d934e7f7dd7` |
| `assets/interlude-r1-D7l2aCxP.js` | R068 `interlude-r1.js`, bounded Vite build | `96f56f1763a8d88269039125eceaa171e7c0c4e34f6161fe09cd082b3ba4747f` |
| `assets/value-flow-r1-CNEfV0ww.js` | R069 `value-flow-r1.js`, bounded Vite build | `c373b60e9f06b35b33e52f25bf420c2f422aa8d599e8438e9ec550a212c9ce52` |

The unbundled `assets/why-resonance-controller.js`, `assets/why-resonance.js` and `assets/trust-project-media.js` exactly match the latest frontend root-owned source files. The historical source tree also has an obsolete duplicate controller under its asset directory; it is not the current runtime owner. Future authoring should follow the recorded bounded build/assembly mapping rather than running the historical generic Vite config and reviving that duplicate.

The runtime bundles are not edited by the release packaging scripts. They remain the exact reviewed R069 bytes. An intentional future motion fix must change its owning editable source, regenerate and review its specific output, and update the provenance and lock explicitly.

## Bounded release preparation

The candidate preserves the existing HERO, QUESTION, EGG, HUMAN, FIELD, THINK, collaboration cards, inquiry mechanisms, LINEN and closing sequence. The local review alternatives `hero-10.html`, `hero-30.html` and `question-a0.html` are excluded from the public file manifest. Private release evidence, source archives and local review galleries are not published.

Release-only changes cover search metadata/indexing policy and repaired legal-footer markup on existing detail pages. The latter reuses the unchanged existing A20 stylesheet `assets/legal-footer-detail.css`; no new visual system is introduced. Current business details and policy links remain in the document body.

Public examples remain labelled as hypothetical or MASHCORE's own production records. A working external URL is not evidence of customer outcomes, ownership, a shared business entity, or broader project responsibilities. No such claims or customer data are added by this release.

On 2026-11-20, the user explicitly approved public display of the ARVO & 마장동 사천 card's **current name, text and link**. This is bounded approval of the existing text-only card; it does not authorize a new logo, new role or ownership claim, broader project materials, or performance claims. The source payload did not change after that confirmation, so the sealed public bytes remain the reviewed candidate.

## Deterministic build and lock

After completing candidate-source review, an authorized maintainer explicitly runs:

```sh
python3 scripts/release_lock.py --seal
```

This records SHA256 for every public source file and every expected output file in production, deploy-preview and branch-deploy contexts, together with canonical tree digests. It does not deploy and is never invoked automatically by CI or Netlify. Any subsequent source or packaging-behavior change fails the lock and requires an explicit new seal and affected QA; builds cannot silently accept new bytes.

Normal build/check commands are:

```sh
python3 scripts/prepare_public.py --context production
python3 scripts/check_release.py --context production
python3 scripts/release_lock.py --check --context production
```

Netlify uses that same production packaging contract. `prepare_public.py` validates the resolved repository-local `dist` path before replacing it, copies only the manifest, applies deterministic context policy, and verifies the output against the lock. It does not compile, minify or replace the reviewed runtime modules.

Production contains exactly 19 HTML routes and 17 indexable sitemap URLs; `/mobile/` and `/research/method/` retain their dedicated noindex policy. Draft and branch outputs have a full noindex policy and empty sitemap. These intentional search-policy differences are recorded in separate locked context maps. Public Git attributes preserve exact file bytes across Windows checkout and Linux CI.

CI retains the 19-route A20 browser smoke test and adds the current Interlude, VALUE FLOW, HUMAN, FIELD and inquiry interaction test. The old test alone cannot certify the current experience. All contexts must pass strict static checks; production output is restored and checked before browser QA. The release record associates the tested Git SHA, locked production tree, Draft QA and actual production deployment ID.

Sealing is a technical identity checkpoint, not permission to publish. If a required functional, public-scope, accessibility or deployment gate fails, the previous production site remains in place until the issue is resolved.
