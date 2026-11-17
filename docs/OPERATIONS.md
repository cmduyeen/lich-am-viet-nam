# Operations

This repository publishes Vietnamese lunar dates in Vietnamese and English only. Default outputs are `viet_lunar_latest.ics` and `viet_lunar_en_latest.ics`, plus the inventory and checksum state. Both retain the current year and next year. Existing URLs and UIDs remain stable.

Run `python generate_all.py --if-needed` for checksum-aware generation. The workflow runs annually, on relevant source changes and on manual dispatch. Unchanged runs do not write keep-alive commits. Historical `output/update-status.json` is no longer a build health signal.

Personal daily calendar inputs and outputs remain in ignored `.local/` by default. See the two root READMEs for holiday selection and custom JSON dates. Never commit private calendar data.

The shared engine still contains internal reference profiles for cross-calendar regression tests. Those profiles are not published by the standard build and have no country selector in the public documentation. Previously indexed standard multi-country feeds are retired atomically during the next build; unrelated files and private custom outputs are preserved.

See [AUTOMATION.md](AUTOMATION.md) for schedule recovery and [RELEASE.md](RELEASE.md) for acceptance checks.
