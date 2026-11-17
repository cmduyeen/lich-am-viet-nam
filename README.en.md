# Vietnamese and Global Lunar Calendars

![Lunar calendar cover](assets/lunar-calendar-cover.png)

Choose your region in the [calendar directory](README.md), or open the Vietnamese calendar guides in [English](vietnam/README.md) or [Vietnamese](vietnam/README.vi.md).

Existing subscriptions remain available at `output/viet_lunar_latest.ics` and `output/viet_lunar_en_latest.ics`. Each contains one event per civil day with lunar dates and the bilingual observances documented in [HOLIDAYS](docs/HOLIDAYS.md).

The default rolling window is now the current year and next year. Dated files and ZIPs are optional snapshots: `python main.py --split --output-dir exports`. Previously downloaded snapshots remain static.

## Personal calendars

The holiday-selection and personal-date commands remain supported:

```powershell
python main.py --language en --holidays mid-autumn
python main.py --language vi --custom-holidays .local/holidays.json
python main.py --list-holidays
```

Customized daily calendars default to `.local/output`, which Git ignores. Do not place personal data in committed files. See [examples/holidays.json](examples/holidays.json) for fictional input.

Use `--country`, `--countries`, `--residence` or `--config` for the shared multi-country pipeline; these options use the country-guide configuration format. Holiday-selection commands use the daily Vietnamese format and cannot be combined with profile options.

[Automation](docs/AUTOMATION.md) describes the annual schedule, checksum preflight and optional external maintenance. [Security](SECURITY.md) covers private data and secret reporting.

The screenshots in `assets/screenshots/` are retained historical Vietnamese/English previews. They do not verify subscription refresh for the new multi-country feeds. Current consumer evidence and remaining release checks are documented in [docs/RELEASE.md](docs/RELEASE.md).
