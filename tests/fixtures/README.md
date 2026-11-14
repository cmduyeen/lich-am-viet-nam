# Reference fixtures

The HKO text tables are downloaded reference datasets from the Hong Kong Observatory, not output from our engines:

- https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2026e.txt
- https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2027e.txt
- https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2030e.txt
- https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2033e.txt
- https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2034e.txt

Retrieved 2026-11-14. Each fixture retains its original text. Tests reconstruct month boundaries and repeated leap months directly from the table. These test Chinese-calendar dates; they must not be used as Vietnamese or Korean answers.

`reference_dates.json` records separately sourced Vietnamese/Korean examples. Vietnamese 2007 is based on an interview with the State Calendar Board; the 1985 historical example is secondary reporting. Korean 2026 Chuseok and Buddha birthday use government/tourism sources. The upstream Korean leap-month fixture is explicitly marked supplementary and is not an independent official check.

These fixtures are regression evidence, not exhaustive certification of all profiles or all years. Historical examples use the stated modern civil-calendar convention and do not certify every historical regional calendar. Source data remains attributed to its publisher; check its reuse terms when redistributing datasets beyond this project.
