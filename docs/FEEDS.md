# Public feeds

The standard publisher exports exactly two Vietnamese lunar calendars:

| Language | File |
| --- | --- |
| Vietnamese | `viet_lunar_latest.ics` |
| English | `viet_lunar_en_latest.ics` |

Both contain one all-day event per civil date, with Vietnamese UTC+7 lunar dates and selected observances. They retain the current year and next year. The language changes the text, while both use the same dates. Each language has its own stable UID namespace. Choose one subscription to avoid seeing both sets of events.

Copy complete subscription URLs from the [Vietnamese](../README.md) or [English](../README.en.md) guide. Changes become public after publication to main; calendar applications control their refresh interval. Imported ICS files remain snapshots.

`output/index.json` records the two feed filenames, languages, coverage, event counts and checksums. `output/.build-state.json` supports freshness checks. CI artifacts and publication use an explicit public-file allowlist. An inventory containing personal or additional custom feeds is rejected before staging.

Keep personal dates in `.local/` and generate customized calendars locally with `--custom-holidays`. Custom output is ignored by Git and is not part of the public publisher. Optional historical snapshots belong in `exports/`, using `--split --output-dir exports`.
