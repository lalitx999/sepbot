# Vendored front-end libraries (self-hosted, no CDN)

| Library | Version | License | Files |
|---|---|---|---|
| Bootstrap | 5.3.8 | MIT | `bootstrap/` |
| Bootstrap Icons | 1.13.1 | MIT | `bootstrap-icons/` |
| Sarabun (via @fontsource) | 5.3.0 | OFL-1.1 | `fonts/sarabun-*` |
| Noto Serif Thai (via @fontsource) | 5.3.0 | OFL-1.1 | `fonts/noto-serif-thai-*` |
| SweetAlert2 | 11.26.25 | MIT | `sweetalert2/` |
| Chart.js | 4.6.1 | MIT | `chartjs/` |
| Quill | 2.0.2 | BSD-3-Clause | `quill/` |
| mammoth | 1.6.0 | BSD-2-Clause | `mammoth/` |
| page-flip | 2.0.7 | MIT | `page-flip/` |

`sourceMappingURL` comments were removed so `ManifestStaticFilesStorage` does not look for `.map` files.
To upgrade a library: `npm pack <pkg>@<version>`, copy the same files, strip the sourceMappingURL comment, update this table.

Not vendored: the LINE LIFF SDK (`static.line-scdn.net/liff/edge/2/sdk.js`) must be loaded from LINE.
