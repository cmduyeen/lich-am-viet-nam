# Vietnamese lunar calendar release checklist

Public scope: Vietnamese lunar dates, displayed in Vietnamese and English. Only `viet_lunar_latest.ics`, `viet_lunar_en_latest.ics`, `viet_lunar_minimal_latest.ics`, and `viet_lunar_en_minimal_latest.ics` are published by default. Stable UIDs and the existing subscription URLs are preserved.

- Run the Python regression suite, including Vietnamese date reference fixtures, private custom dates and rollback.
- Parse both feed inventories independently and verify matching dates, unique UIDs, checksums and all-day boundaries.
- Check both root READMEs and the shared cover at desktop and mobile sizes.
- Confirm current and next year coverage, and no standard foreign feeds in output.
- Require GitHub CI on the pushed commit before merging.
- Live Google Calendar, Apple Calendar and Outlook subscription/refresh checks still require separate acceptance testing.

Local consumer checks write current results into ignored tests/e2e/artifacts. The two root READMEs link to the author's actual Google Calendar screen recordings under assets/videos, with language-specific screenshots under assets/screenshots.

Final local verification: 108 Python tests passed, including corrupt-inventory repair and an automatic 2026-to-2027 rollover with stable overlapping UIDs. Independent browser/ICAL.js checks passed for both 2026-2027 (1,460 events) and 2027-2028 (1,462 events), 16 checks per run. The Windows recovery task command was syntax-checked, including paths with apostrophes; it must be installed once under the owner's Windows account. The author's screenshots and recordings are preserved as supplied. Dependency installation and live GitHub execution cannot be verified from this network-restricted session.
