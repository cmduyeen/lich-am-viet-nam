# 🌙 Vietnamese Lunar Calendar (Google Calendar, Apple Calendar, Outlook)

[Tiếng Việt](README.md) · [English](README.en.md)

[![Update Lunar Calendars](https://github.com/cmduyeen/lich-am-viet-nam/actions/workflows/main.yml/badge.svg)](https://github.com/cmduyeen/lich-am-viet-nam/actions/workflows/main.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

![Vietnamese lunar calendar](assets/lunar-calendar-cover.png)

A **free, open-source Vietnamese Lunar Calendar (.ics)** calculated in **GMT+7 (UTC+7)** and available in **Vietnamese or English**. **No extra apps or third-party software required** — use the **[interactive Web Studio](https://cmduyeen.github.io/lich-am-viet-nam/)** to customize holidays, lunar birthdays, and personal events in your browser, or paste **one `.ics` URL** directly into **Google Calendar, Apple Calendar, or Microsoft Outlook** for automatic yearly updates.

> 🌐 **Try Web Studio:** **[cmduyeen.github.io/lich-am-viet-nam](https://cmduyeen.github.io/lich-am-viet-nam/)** · More tools at **[Blog & Tools](https://cmduyeen.github.io/en/tools/)**

## Table of Contents

- [Customize Online (Web Studio)](#customize-online-web-studio)
- [Subscribe via URL (No App Required — Just Paste & Go)](#subscribe-via-url-no-app-required--just-paste--go)
- [Quick Setup Guides](#quick-setup-guides)
- [Key Features](#key-features)
- [Generate & Customize with Python (Optional for Developers)](#generate--customize-with-python-optional-for-developers)
- [Maintenance & Automation](#maintenance--automation)
- [FAQ](#faq)

## Customize Online (Web Studio)

Open **[Vietnamese Lunar Calendar Studio](https://cmduyeen.github.io/lich-am-viet-nam/)** in your browser without installing Python:

- **Choose your detail level:** Major festivals only, Festivals + New Moon & Full Moon (1st & 15th), or full daily lunar dates.
- **Add personal events:** Add lunar birthdays, family anniversaries, or custom solar/lunar reminders.
- **Instant Solar ↔ Lunar lookup:** Check any date's lunar equivalent and Sexagenary cycle (Can Chi) in GMT+7.
- **Export `.ics` or JSON/CLI:** Download a ready-to-import `.ics` file or copy the config for Python CLI.

## Subscribe via URL (No App Required — Just Paste & Go)

You **don't need to download any files, install Python, or use third-party calendar apps**. Simply copy **one** of the `.ics` subscription URLs below and paste it into your existing calendar app (all feeds share the exact same GMT+7 lunar dates):

**Full Daily Feed (all lunar dates + holidays)**

* Vietnamese:
```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```
* English:
```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

**Minimal Feed (Lunar & Solar Holidays, Lunar New Year, 1st & 15th only)**

* Vietnamese:
```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_minimal_latest.ics
```
* English:
```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_minimal_latest.ics
```

> **Note:** Subscribe to **one language only** to avoid duplicate daily events. Always use **Add calendar from URL / Subscribe** rather than downloading and importing a static `.ics` file, as imported snapshots will not receive automatic yearly updates.

## Quick Setup Guides

### 1. Google Calendar (Android, iPhone, Web)

1. Copy the **Vietnamese or English** `.ics` feed URL above.
2. Open [Google Calendar](https://calendar.google.com/) in a desktop browser.
3. In the left sidebar next to **Other calendars**, click **+ → From URL**.
4. Paste the URL and click **Add calendar**. The calendar will sync automatically to the Google Calendar mobile app under the same account.

![Vietnamese lunar dates in English in Google Calendar](assets/screenshots/google-calendar-en.png)

**Google Calendar screen recording:**

https://github.com/user-attachments/assets/37bef49a-dff3-42a1-b842-bd1d1a16d44e

See [Google's official instructions](https://support.google.com/calendar/answer/37100?hl=en) for more details.

### 2. Apple Calendar (iPhone, iPad, Mac)

- **On iPhone / iPad:** Open the **Calendar** app → tap **Calendars** at the bottom → **Add Calendar** → **Add Subscription Calendar** → paste the `.ics` URL and tap **Subscribe**.
- **On macOS:** Open **Calendar** → select **File → New Calendar Subscription...** → paste the `.ics` URL → click **Subscribe**.

### 3. Microsoft Outlook

- Open [Outlook on the web](https://outlook.live.com/calendar/) → click **Add calendar** → **Subscribe from web** → paste the `.ics` URL, name your calendar, and click **Import**.

## Key Features

- **Zero Extra Software Needed:** Just paste one `.ics` URL into Google Calendar, Apple Calendar, or Outlook already on your phone or computer — no bloated apps, no ads, no tracking.
- **Accurate Vietnamese Astronomy (GMT+7 / UTC+7):** Computed directly from astronomical new moons and solar terms in UTC+7. This avoids off-by-one-day discrepancies that occur when using Chinese lunar calendars (UTC+8).
- **Rolling 2-Year Coverage, Permanent URL:** Public feeds always cover the **current year and next year**, rolling forward automatically at the turn of the year without changing your subscription URL. The underlying engine supports **1900–2099**.
- **27 Curated Vietnamese Observances:** Includes Tet (Lunar New Year), Hung Kings' Commemoration Day, Buddha's Birthday, Vu Lan, Mid-Autumn Festival, Kitchen Gods Day, and Gregorian public holidays in Vietnam. See the full [holiday catalog](docs/HOLIDAYS.md).
- **Minimal & Private:** One clean all-day event per day, zero notification spam, zero ads, and MIT-licensed open source.

## Generate & Customize with Python (Optional for Developers)

> Regular users **do not** need to run any code — simply subscribe using the `.ics` URL above.

If you want to run the generator locally with **Python 3.11+** to build custom feeds (e.g., personal lunar anniversaries, family memorials, or annual snapshots):

```powershell
python -m pip install --require-hashes -r requirements.txt
python generate_all.py
```

This publishes the two standard Vietnamese/English feeds into `output/`. To skip rebuilding when inputs and checksums are unchanged:

```powershell
python generate_all.py --if-needed
```

Generate a single language or export annual snapshots:

```powershell
python main.py --language vi
python main.py --language en
python main.py --language vi --split --output-dir exports
```

### Filter Holidays & Add Personal Dates

```powershell
python main.py --language en --list-holidays
python main.py --language en --holidays mid-autumn
python main.py --language vi --custom-holidays .local/holidays.json
```

Use the [fictional JSON example](examples/holidays.json) as a template for personal dates. Customized calendars default to `.local/output/`, which is ignored by Git so private data stays out of the public repository.

> **Note:** Observances in this feed represent traditional and public commemorative dates—not statutory leave or substitute-day schedules. See the [holiday catalog](docs/HOLIDAYS.md).

## Maintenance & Automation

- **Daily Automated Checks:** GitHub Actions checks for updates daily and rebuilds the feeds only when source files or dates change.
- **Permanent Subscription URLs:** Coverage automatically rolls forward to the current and next year without changing any subscription links.
- **Technical Docs:** See the [automation guide](docs/AUTOMATION.md), [operations](docs/OPERATIONS.md), and [release checks](docs/RELEASE.md).

## FAQ

**1. Will the lunar calendar update automatically on my phone?**  
Yes, as long as you subscribe via URL rather than importing a static file. Your calendar app (Google Calendar, Apple Calendar, or Outlook) controls the refresh interval.

**2. Why does the Vietnamese lunar calendar sometimes differ from the Chinese lunar calendar?**  
Because of the 1-hour timezone difference between Vietnam (**UTC+7**) and China (**UTC+8**). When an astronomical new moon falls between 23:00 and 23:59 in Vietnam (00:00–00:59 the next day in China), the lunar month starts on a different civil date. This project computes everything in **UTC+7**.

**3. Does it include compensatory days off or swapped workdays?**  
No. It lists lunar dates and 27 standard observances. Statutory leave swaps and extended Tet holiday schedules depend on annual government announcements.

**4. How can I report an issue or contribute?**  
Feel free to open an [Issue](https://github.com/cmduyeen/lich-am-viet-nam/issues) or submit a Pull Request. If you find this project helpful, please consider giving it a **Star ⭐**!

## Contributors

- [@cmduyeen](https://github.com/cmduyeen) — Creator & Maintainer
- [@DevSecNinja](https://github.com/DevSecNinja) — Suggested and helped shape the English & minimal subscription feeds

## Support the Project ☕

This project is completely free and open-source. If it helps you or your family keep track of Vietnamese lunar dates, you can optionally buy me a coffee at **[Ko-fi (ko-fi.com/cmduyeen)](https://ko-fi.com/cmduyeen)**!

---

[MIT License](LICENSE) · Maintained by [cmduyeen](https://github.com/cmduyeen)
