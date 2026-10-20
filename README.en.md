# Vietnamese Lunar Calendar

[Vietnamese](README.md) | English

A minimalist Vietnamese lunar calendar for Google Calendar, Apple Calendar and
Outlook. Subscribe in your existing calendar app without installing another app.

- Daily lunar dates, first days of lunar months, full moons and major holidays.
- English event titles, descriptions, calendar name and calendar description.
- A rolling calendar from the current year through ten years ahead, inclusive.
- Automatic annual regeneration, with separate English and Vietnamese feeds.
- Free and open source under the [MIT License](LICENSE).

## Subscribe

Choose an English subscription:

- [Full daily calendar](output/viet_lunar_en_latest.ics): lunar dates and all included holidays.
- [Minimal calendar](output/viet_lunar_en_minimal_latest.ics): only **Full Moon** and **Lunar New Year**.

Open the chosen file, select
**Raw**, and copy the resulting URL into your calendar app. The raw URL identifies
the repository and branch you are viewing: when trying this change in a fork,
use that fork's branch, not upstream `main` until the English file is available
there. Keep using the `latest` file rather than a year-specific download for
automatic updates.

The existing Vietnamese subscription is unchanged:

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

The [Vietnamese minimal subscription](output/viet_lunar_minimal_latest.ics)
uses translated titles and descriptions for the same dates as minimal English.

Choose one feed to avoid duplicate events. All four feeds have their own stable
identifiers, so full/minimal English and Vietnamese do not overwrite one another.

### Minimal calendar

Both minimal feeds contain only these two event kinds (English titles shown):

- **Full Moon**: the traditional **15th day of every lunar month**, including leap
  months. This follows the existing lunar calendar convention, **not the exact
  astronomical full moon instant or date**. Festival names such as Mid-Autumn
  Festival do not replace the Full Moon title.
- **Lunar New Year**: day 1 of **non-leap lunar month 1** only. New Year's Eve,
  days 2 and 3, and day 1 of a leap month are excluded.

Both are all-day events. Descriptions retain the lunar date and leap-month marker
where applicable. No new astronomical calculations or dependencies are involved.

### Set up your calendar app

- **Apple Calendar (iPhone / iPad):** Open Calendar, choose **Calendars**,
  **Add Calendar**, then **Add Subscription Calendar** and paste the URL.
  On older iOS versions, use **Settings > Calendar > Accounts > Add Account >
  Other > Add Subscribed Calendar**.
- **Apple Calendar (Mac):** Choose **File > New Calendar Subscription**, paste
  the URL and select an automatic refresh interval.
- **Google Calendar (Web / Android):** In [Google Calendar](https://calendar.google.com)
  on the web, choose **+** next to **Other calendars**, then **From URL**, and
  paste the URL. Enable the subscribed calendar on your Android device.
- **Outlook on the web:** Choose **Add calendar > Subscribe from web**, paste the
  URL, give the calendar a name and select **Import**.

Subscribe by URL rather than importing a downloaded file: a one-time file import
does not receive future updates. Refresh timing is controlled by your calendar app.

## What the events mean

The full daily feed's titles use **lunar day/month**, not the Gregorian date. Examples:

| Event | English title |
| --- | --- |
| Ordinary lunar day | `Lunar 14/11` |
| First day of a lunar month | `Lunar 1/6` &bull; `First Day of Lunar Month` |
| Full moon day | `Lunar 15/6` &bull; `Full Moon` |
| Lunar New Year | `Lunar 1/1` &bull; `Lunar New Year - Day 1` |
| A day in a leap lunar month | `Lunar 7/6 (leap month)` |

Descriptions translate the traditional stem-and-branch year into
English, for example **Yang Fire Horse year**. Vietnamese zodiac conventions,
including the **Cat** and **Buffalo**, are retained.

The full English feed uses the same date calculations, holiday precedence, all-day
event boundaries and colours as the Vietnamese feed. It adds an explicit
**leap month** label to English titles and descriptions; the Vietnamese feed
keeps its existing formatting. This translation does not change the underlying
calendar algorithm or holiday rules.

## Included holidays (full daily feed)

### Public holidays

| Holiday | Date |
| --- | --- |
| New Year's Day | January 1, Gregorian calendar |
| Lunar New Year's Eve | Last day of lunar month 12 |
| Lunar New Year - Days 1, 2 and 3 | Days 1-3 of lunar month 1 |
| Hung Kings Commemoration Day | Day 10 of lunar month 3 |
| Reunification Day | April 30, Gregorian calendar |
| International Labour Day | May 1, Gregorian calendar |
| National Day | September 2, Gregorian calendar |

### Traditional festivals

| Festival | Lunar date (day/month) |
| --- | --- |
| Kitchen Gods Day | 23/12 |
| God of Wealth Day | 10/1 |
| First Full Moon Festival | 15/1 |
| Buddha's Birthday | 15/4 |
| Double Fifth Festival | 5/5 |
| Filial Piety Festival | 15/7 |
| Mid-Autumn Festival | 15/8 |

These are the existing calendar's holiday dates, not a complete schedule of
government-announced days off or substitute holidays.

## Generate calendars locally

Use Python 3.11 or newer and install the existing dependencies:

```sh
python -m pip install -r requirements.txt
```

The default remains Vietnamese. Add `--language en` to generate English files
without overwriting Vietnamese files:

```sh
python main.py --split
python main.py --language en --split
python main.py --language en --start 2026 --end 2036
python main.py --language en --year 2027
python main.py --minimal --split
python main.py --language vi --minimal --split
python main.py --language en --minimal --split
```

Generation status messages remain in Vietnamese. On Windows terminals that do
not default to UTF-8, set `$env:PYTHONUTF8 = '1'` in PowerShell before running.

Full English files in `output` are:

- `viet_lunar_en_latest.ics`: rolling subscription feed.
- `viet_lunar_en_<start>_<end>.ics`: combined calendar for the requested years.
- `viet_lunar_en_<year>.ics`: single-year calendar (`--split` or `--year`).
- `viet_lunar_en_yearly_<start>_<end>.zip`: yearly calendars (`--split`, multiple years).

`--minimal` works with both languages: Vietnamese is the default, or select
`--language vi` explicitly; use `--language en` for English. Minimal files use
`viet_lunar_minimal` (Vietnamese) or `viet_lunar_en_minimal` (English) with the
same rolling, year-range, single-year and ZIP filename patterns. Their subscription
files are `viet_lunar_minimal_latest.ics` and `viet_lunar_en_minimal_latest.ics`.
For example, `python main.py --language en --minimal --year 2027` only writes
`viet_lunar_en_minimal_2027.ics`. Omitting `--minimal` preserves the full feed.

`--year` only writes a single-year file and does not replace the `latest` feed.
`--output-dir` selects a different output directory. Cleanup removes past-year
files only for the selected language and mode, leaving all other feeds untouched.

The GitHub Actions workflow generates full and minimal feeds in both languages
on pushes to `main`, on January 1 each year and on manual runs. It retains the
existing rolling range.
Scheduled workflows may need to be enabled in a fork before automatic updates run.

Run the regression tests with:

```sh
python -m unittest discover -s tests -v
```

## License and attribution

[MIT License](LICENSE). Copyright (c) 2026
[cmduyeen](https://github.com/cmduyeen) - Pinkie Suite.

<p align="center">
  <img src="assets/signature.svg" alt="cmduyeen" width="400" />
</p>
