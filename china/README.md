[English](README.md) · [简体中文](README.zh-Hans.md) · [All countries](../README.md)

# 🌙 China — Lunar calendar

Copy the URL below and subscribe in your calendar app.

## 1. Subscribe by URL

Lunar festivals only

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_cn_chinese_en_festivals_latest.ics
```

Paste it into Subscribe by URL in Google Calendar, Apple Calendar or Outlook, then save. Downloading and importing an ICS file does not receive automatic updates.

> New links become available after these files are published to main.

<details>
<summary>Other calendars: lunar days 1 and 15 / every lunar day</summary>

**Festivals + lunar days 1 and 15**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_cn_chinese_en_observances_latest.ics
```

**Every lunar day + festivals**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_cn_chinese_en_daily_latest.ics
```

</details>

<details>
<summary>Included lunar festivals</summary>

| Lunar date (day/month) | Festival |
| --- | --- |
| 1/1 | Lunar New Year |
| 2/1 | Lunar New Year — Day 2 |
| 3/1 | Lunar New Year — Day 3 |
| 15/1 | Lantern Festival |
| 2/2 | Dragon Heads-raising Day |
| 5/5 | Double Fifth / Dragon Boat Festival |
| 7/7 | Qixi Festival |
| 15/7 | Ghost Festival |
| 15/8 | Mid-Autumn Festival |
| 9/9 | Double Ninth Festival |
| 8/12 | Laba Festival |
| 23/12 | Little New Year — Northern China |
| 24/12 | Little New Year — Southern China |
| Last day of lunar year | Lunar New Year's Eve |

[Sources and festival rules](../docs/FESTIVALS.md)

</details>

## 2. Customize with Python

Run commands from the project root: [lunar-calender](../README.md).

<details>
<summary>First time? Set up Python 3.11+</summary>

Download the repository, open the root folder containing main.py, and create a virtual environment. Activate it before installing the pinned dependencies.

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
```

</details>

```powershell
python main.py --config china/calendar.config.json --language en
```

<details>
<summary>Edit your configuration</summary>

Use this folder’s calendar.config.json. CLI options override JSON. The English command below explicitly selects English; the stored configuration uses the native display language.

Set feed_name to a stable name such as family in your JSON before subscribing. The URL stays custom_family_latest.ics when settings change; keep this name unique.

```json
{
  "country": "CN",
  "tradition": "chinese",
  "language": "en",
  "content": "festivals"
}
```

Use --year or --start/--end for dates, --lunar-days all/none/1,15 for background days, --holiday-types lunar/solar/all/none for categories, --split for yearly files and ZIP, and --output-dir for another folder. Colors accept #RRGGBB via --calendar-color, --holiday-color, --lunar-day-color and --ordinary-color.

```powershell
python main.py --config china/calendar.config.json --language en --year 2027 --split --output-dir exports
python main.py --config china/calendar.config.json --language en --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>Automatic updates on your fork</summary>

1. Fork the repository and commit your configuration.
2. Enable Actions and allow the workflow to write repository contents.
3. Set CUSTOM_CONFIG to the configuration path shown below.
4. Complete the release checklist, then set PUBLISH_LUNAR_FEEDS to true. Run Update Lunar Calendars; custom_config can override the path for a manual run.
5. Use the printed filename with your own fork’s raw main/output URL. Annual runs reuse CUSTOM_CONFIG.

Scheduled generation is annual, January 1 at 00:00 UTC; code/data changes and manual runs can rebuild immediately. Public GitHub repositories can have schedules disabled after 60 inactive days. Keep the workflow enabled and monitored, or use an external scheduler that enables the workflow when needed and calls workflow_dispatch.

```text
china/calendar.config.json
```

</details>

## Coverage and help

Traditional observance; not an official public-holiday or substitute-day schedule.

The rolling subscription retains the current year and next year. Older years leave the feed when it rolls forward. Keep historical snapshots with --split --output-dir exports; output/ is managed and dated exports there are retired by the next standard batch build.

Supported years: 1901–2099. The default rolling calendar covers 2 consecutive years starting with the current year, within these limits.

Calendar rules: chinese; reference timezone: Asia/Shanghai. Traditional day 15 is not the exact astronomical full moon. Leap months do not repeat festivals.

Independent native-language review and live Google/Apple/Outlook subscription tests remain pending. These are candidate feeds until the release checks are complete.

<details>
<summary>FAQ</summary>

If a URL is unavailable, confirm the file is on main in the correct repository. App refresh intervals vary. Unsupported options raise an error; color support depends on the app.

</details>

**Shared technical documentation**

[Feeds](../docs/FEEDS.md) · [Development](../docs/DEVELOPMENT.md) · [Automation](../docs/AUTOMATION.md) · [Release](../docs/RELEASE.md) · [Sources](../tests/fixtures/README.md) · [index.json](../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../LICENSE)
