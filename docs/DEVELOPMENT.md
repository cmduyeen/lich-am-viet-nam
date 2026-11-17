# Development

The public product is the Vietnamese lunar calendar, with Vietnamese and English display languages. `main.py` generates one selected language; `generate_all.py` publishes the two default daily feeds. Personal holiday selection uses `src/daily_cli.py` and `src/daily_generator.py`. Both default languages share the same Vietnamese UTC+7 date conversion.

`src/ics_generator.py` preserves the existing daily constructor and options-based compatibility. `src/ics.py` validates wire format, reconciles stable UIDs/revisions and publishes staged changes with rollback. `src/release_state.py` fingerprints source inputs and verifies output checksums before expensive work. `src/maintenance.py` checks the Vietnamese inventory before dispatching a stale build.

Internal reference profiles and engines remain for astronomy regression tests and comparison fixtures. They do not define additional public subscriptions. Adding countries back to the standard publisher requires a separate product scope decision.

Validation:

```powershell
python -m unittest discover -s tests -v
python generate_all.py
python generate_all.py --if-needed
npm ci --prefix tests/e2e --ignore-scripts --no-fund
cd tests/e2e
npm test
```

Browser checks parse both actual feeds independently, render both languages and READMEs, check mobile layout, HTTP refresh, stable UIDs and all-day dates in several timezones. They do not certify Google/Apple/Outlook refresh behavior.
