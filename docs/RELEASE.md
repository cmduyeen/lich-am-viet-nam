# Vietnamese lunar calendar release checklist

Public scope: Vietnamese lunar dates, displayed in Vietnamese and English. Only `viet_lunar_latest.ics` and `viet_lunar_en_latest.ics` are published by default. Stable UIDs and the existing subscription URLs are preserved.

- Run the Python regression suite, including Vietnamese date reference fixtures, private custom dates and rollback.
- Parse both feed inventories independently and verify matching dates, unique UIDs, checksums and all-day boundaries.
- Check both root READMEs and the shared cover at desktop and mobile sizes.
- Confirm current and next year coverage, and no standard foreign feeds in output.
- Require GitHub CI on the pushed commit before merging.
- Live Google Calendar, Apple Calendar and Outlook subscription/refresh checks still require separate acceptance testing.

Historical multi-country evidence under docs/evidence predates this scope reduction; it is not current product documentation. Local consumer checks write current results into ignored tests/e2e/artifacts.

Local verification after scope reduction: 104 Python tests passed; independent browser/ICAL.js consumer passed 16 checks on 2 feeds and 1,460 daily events for 2026-2027. Dependency installation and GitHub CI were not rerun in this network-restricted session.
