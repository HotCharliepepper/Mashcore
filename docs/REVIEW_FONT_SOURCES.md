# Review fonts — source and verification

Status: review implementation. These fonts do not establish a new corporate identity.

## Selected assets

- `assets/fonts/NotoSansKR-Regular.woff2`: Noto Sans KR, normal 400.
- `assets/fonts/NotoSansKR-SemiBold.woff2`: Noto Sans KR, normal 600.
- `assets/fonts/GowunBatang-Regular.woff2`: Gowun Batang, normal 400.
- `assets/css/fonts.css`: same-origin `@font-face` declarations, `font-display: swap`.

All three files were converted with fontTools from available full TTF originals, without subsetting. Character mappings and glyph order are compared before and after conversion. Original copyright and license name-table entries are retained. Original Noto files contain 23,174 Unicode mappings; Gowun contains 12,494. Both families include all 11,172 modern Hangul syllables and 94 compatibility Jamo in U+3131–U+318E. Embedded subsets from the attached screen-review HTML were inspected but are not reused: they contain only 590 Unicode mappings, which is insufficient for the complete site and arbitrary Korean input.

The original source directory available in this work session was `/workspace/scratch/8c32783663cb/output/mashcore_anchor/fonts/`. This is a provenance record, not a build dependency. Delivered WOFF2 files are tracked repository assets and require no external font server to load. No runtime package or frontend build dependency was added.

## License provenance

The full license files were obtained from the official Google Fonts repository through the GitHub connector. Each original font also contains a SIL Open Font License 1.1 statement in its name table.

| Family | License file included with assets | Official source | Retrieved Git blob |
|---|---|---|---|
| Noto Sans KR | `assets/fonts/OFL-NotoSansKR.txt` | https://github.com/google/fonts/blob/main/ofl/notosanskr/OFL.txt | `1c9f43281b8f216c5461fe9ac729afbade7724e4` |
| Gowun Batang | `assets/fonts/OFL-GowunBatang.txt` | https://github.com/google/fonts/blob/main/ofl/gowunbatang/OFL.txt | `638ca4da3c4df267261e9cd34eb9458b4513fe0c` |

Noto copyright: 2014–2021 Adobe, reserved font name “Source”. Gowun copyright: 2021 The Gowun Batang Project Authors. The converted family names do not use “Source”. Copyright and complete OFL files accompany the distributed fonts.

## Fallback and verification boundary

Conversion and round-trip verification completed successfully:

| Output | Bytes | Unicode mappings / glyphs | WOFF2 SHA-256 |
|---|---:|---:|---|
| NotoSansKR-Regular.woff2 | 2,071,988 | 23,174 / 24,964 | `b5b2630fbfd805032cd6ef046b889f1862ea8b96f7b351a4ef74f605ead73d81` |
| NotoSansKR-SemiBold.woff2 | 2,105,828 | 23,174 / 24,964 | `c12839e5c9589225432a98a1634355ad0736034afd9daa153294ecb6719945ec` |
| GowunBatang-Regular.woff2 | 536,760 | 12,494 / 12,550 | `333ec20c81cebe1d20793beaceaa7d1cd524daf2a043df40f1ee4b4d0b40a573` |

TTF input SHA-256 values, respectively: `0e04e6e4e4987b09d6c2be2c991c7a5f729fb7ff046da7fd676adfe72df6845c`, `fcd255effdf666f7ea35245b30c1394c96f506023c1bc74dff61824ddc08311d`, and `466c593e7147412e748af4856d5ad14709b5a860bdf62b9c2546f2c5874e9849`.

The existing Google stylesheet referenced Gowun Batang, Noto Sans KR and EB Garamond, while the original editorial CSS selected Noto Serif KR as its heading family. The review should explicitly select Gowun Batang for headings. EB Garamond is not bundled; Latin text may use the existing Georgia/serif fallback. Korean body fallback should include Apple SD Gothic Neo, Malgun Gothic and a generic sans-serif; headings should retain a Korean serif and generic serif fallback.

Source inspection and font-file validation do not prove browser loading. Same-origin HTTP responses, actual browser font readiness, failed-font rendering and viewport checks belong to the final review QA. The executor reported no system Korean fonts via `fc-list :lang=ko`; this does not describe every user's device or the separate browser environment.
