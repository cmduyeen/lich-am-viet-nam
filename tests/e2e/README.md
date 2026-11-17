# Actual-artifact browser checks

These development-only checks read `output/*.ics` through an independent ICAL.js parser, serve the exact bytes over a temporary loopback HTTP endpoint, and render them in FullCalendar with a real headless browser. They also render the actual country READMEs. They do not add a production website, paid service, runtime dependency or background server.

```sh
python generate_all.py --if-needed
npm ci --prefix tests/e2e --ignore-scripts --no-fund
cd tests/e2e
npx playwright install chromium
npm test
```

Use `PYTHON` to select a virtual-environment interpreter and `BROWSER_EXECUTABLE` to use an already installed Chrome/Edge executable instead of downloading Chromium. Set `EVIDENCE_DIR` to keep screenshots elsewhere. Default output is ignored `tests/e2e/artifacts/`. Images are native browser screenshots with no desktop chrome, mouse pointer or simulated cursor overlay.

Coverage: exactly two Vietnamese daily feeds in vi/en; inventory checksums, event counts, unique UIDs, all-day boundaries and year range; both root READMEs, the shared cover and 390px mobile layout; localized Tet events in both languages; HTTP 304; actual CLI regeneration followed by refresh without duplicate events; four timezone contexts. Temporary files and the loopback server are cleaned up on success or failure.

This is evidence for this consumer and parser. It must not be labeled as a Google Calendar, Apple Calendar or Outlook subscription test. Those applications control their own refresh intervals and require separate live acceptance checks.
