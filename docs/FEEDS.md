# Public feeds

The standard publisher exports four Vietnamese lunar calendars (daily and minimal, in Vietnamese and English):

| Language | Scope | File |
| --- | --- | --- |
| Vietnamese | Daily (all lunar dates + holidays) | `viet_lunar_latest.ics` |
| English | Daily (all lunar dates + holidays) | `viet_lunar_en_latest.ics` |
| Vietnamese | Minimal (holidays, Tet, 1st & 15th) | `viet_lunar_minimal_latest.ics` |
| English | Minimal (holidays, Tet, 1st & 15th) | `viet_lunar_en_minimal_latest.ics` |

The daily feeds contain one all-day event per civil date, while the minimal feeds contain only Vietnamese lunar/solar holidays, Lunar New Year, and the 1st & 15th of each lunar month. All feeds retain the current year and next year with Vietnamese UTC+7 lunar dates. Each feed has its own stable UID namespace. Choose one subscription to avoid seeing duplicate events.

Copy complete subscription URLs from the [Vietnamese](../README.md) or [English](../README.en.md) guide. Changes become public after publication to main; calendar applications control their refresh interval. Imported ICS files remain snapshots.

`output/index.json` records the four feed filenames, languages, coverage, event counts and checksums. `output/.build-state.json` supports freshness checks. CI artifacts and publication use an explicit public-file allowlist. An inventory containing personal or additional custom feeds is rejected before staging.

Keep personal dates in `.local/` and generate customized calendars locally with `--custom-holidays`. Custom output is ignored by Git and is not part of the public publisher. Optional historical snapshots belong in `exports/`, using `--split --output-dir exports`.
