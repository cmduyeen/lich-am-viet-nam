# Operations and maintenance

The shared pipeline and its current operating instructions are in [AUTOMATION.md](AUTOMATION.md). The former monthly two-language workflow has been replaced by annual generation on January 1 at 00:17 UTC (07:17 Vietnam time), code/data triggers and manual dispatch. Unchanged scheduled runs skip generation and do not write keep-alive commits or monthly status timestamps.

The default window is the current year and next year. Dated exports are retired from managed `output/`; save snapshots with `--split --output-dir exports`. Existing Vietnamese/English latest subscription URLs remain stable. Other country feeds become public when the reviewed outputs reach main.

Private daily-calendar input and output remain in ignored `.local/` by default. `--holidays` and `--custom-holidays` retain the Vietnamese daily customization API; see [README.en.md](../README.en.md). Shared profile customizations use the separate `--config` format described in the country guides. Publishing a shared custom config is an explicit public-data action: never put private dates or credentials in that file.

The prior `output/update-status.json` is historical, not the current build health signal. Check GitHub Actions and `output/.build-state.json` instead. Successful unchanged runs do not update timestamps. Public GitHub repository schedules may be disabled after inactivity; the optional maintenance helper is documented in AUTOMATION.md.

Dependabot, secret scanning, private-file ignore rules and the bilingual daily-calendar regression suite are retained from main. Release review still requires the outstanding checks in [RELEASE.md](RELEASE.md).
