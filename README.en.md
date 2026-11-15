[Tiếng Việt](README.md) · **English**

<h1 align="center">🌙 Vietnamese Lunar Calendar</h1>

<p align="center">
  Vietnamese lunar dates and holidays, synced to Google Calendar, Apple Calendar, and Microsoft Outlook with a single URL link (.ics). Automatically updated monthly, free, and ad-free.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-FFD1DC?style=flat" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Updates-Monthly-FFF0F5?style=flat" alt="Monthly Updates" />
  <img src="https://img.shields.io/badge/Coverage-Next_10_Years-FFD1DC?style=flat" alt="Next 10 Years" />
  <img src="https://img.shields.io/badge/Format-iCalendar_(.ics)-FFF0F5?style=flat" alt="iCalendar format" />
</p>

<p align="center">
  <a href="assets/screenshots/google-calendar-en.png"><img width="1100" alt="Daily lunar dates with lunar and Gregorian holidays in Google Calendar" src="assets/screenshots/google-calendar-en.png" /></a>
  <br /><em>Vietnam Calendar · EN — Google Calendar, November 2026.</em>
</p>

### Highlights

- 🔄 **Automatic Sync**: Subscribe once via URL; your calendar refreshes automatically each month, maintaining a 10-year rolling window.
- 📅 **Every Lunar Day**: Displays daily lunar dates (e.g. `15/8`) for all 365/366 days of the year, alongside the 1st and 15th lunar days and Lunar New Year's Eve.
- 🎋 **Comprehensive Holidays**: Combines Vietnamese traditional lunar festivals, major national holidays, and widely celebrated Gregorian observances.
- 📱 **Cross-Platform**: Seamlessly works with Google Calendar (Android, iOS, Web), Apple Calendar (iPhone, iPad, Mac), and Microsoft Outlook.
- 🌏 **Diaspora & Global Friendly**: Formatted as All-Day events aligned with Vietnam astronomical time (UTC+7). Overseas Vietnamese in the US, Europe, Australia, or Japan stay aligned with Vietnam dates without timezone day-shifts.
- 🛡️ **Privacy & Ad-Free**: 100% open-source, zero advertising, zero tracking, safe for personal calendars.

---

## 1. Subscribe quickly by URL

Copy the link below and choose **Add calendar from URL** or **Subscribe to calendar by URL** in your calendar app:

**English — Vietnam Calendar · EN**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

**Tiếng Việt — Lịch Việt Nam · VI**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

Paste the link and save. Subscribe by URL to receive updates automatically without downloading or manually importing `.ics` files. Compatible with Google Calendar, Apple Calendar, Outlook, and other apps supporting iCalendar.

Choose **one** language. For example: `15/8 • Mid-Autumn Festival` or `15/8 • Tết Trung Thu`. The existing Vietnamese subscription URL remains active.

<details>
<summary><strong>Step-by-step instructions for major calendar apps</strong></summary>

#### Google Calendar (Web, Android, and iOS)
1. Open [Google Calendar](https://calendar.google.com/) in a desktop web browser.
2. In the left sidebar, next to **Other calendars**, click the **+** icon and select **From URL**.
3. Paste the `.ics` link above into the **URL of calendar** field and click **Add calendar**.
4. On your mobile phone, open the Google Calendar app: go to **Settings** -> tap your Google account -> ensure the new calendar is checked and turn on **Sync**.

#### Apple Calendar (iPhone, iPad, and macOS)
- **On iPhone / iPad (iOS)**:
  1. Go to **Settings** -> scroll down to **Calendar** -> tap **Calendar Accounts** (or **Accounts** -> **Add Account**).
  2. Tap **Other** -> tap **Add Subscribed Calendar**.
  3. Paste the `.ics` link into the **Server** field -> tap **Next** -> tap **Save**.
- **On Mac (macOS)**:
  1. Open the **Calendar** app.
  2. In the top menu bar, choose **File** -> **New Calendar Subscription...**
  3. Paste the `.ics` link -> click **Subscribe** -> set Auto-refresh frequency to **Every day** -> click **OK**.

#### Microsoft Outlook (Web & Desktop App)
- **Outlook Web Browser**:
  1. Go to [Outlook Calendar](https://outlook.live.com/calendar/) -> click **Add calendar**.
  2. Select **Subscribe from web** -> paste the `.ics` link -> name the calendar and click **Import**.
- **Outlook Desktop App**:
  1. Switch to Calendar view -> click **Add Calendar** on the ribbon -> choose **From Internet...**
  2. Paste the `.ics` link -> click **OK** -> confirm the subscription.

</details>

### One calendar for everything

- **Every daily lunar date**, with lunar and Gregorian holidays in the same event.
- The first and fifteenth days of each lunar month, and Lunar New Year's Eve.
- Major holidays: New Year's Day, Tết (Vietnamese Lunar New Year), Hùng Kings' Commemoration Day, Reunification Day, International Workers' Day, and National Day.
- Traditional observances: Kitchen Gods Day, God of Wealth Day, First Full Moon Festival, Han Thuc, Buddha's Birthday, Doan Ngo, Vu Lan, Mid-Autumn and Ha Nguyen.
- Gregorian observances: Valentine's Day, International Women's Day, Children's Day, Vietnamese Family Day, Vietnamese Women's Day, Vietnamese Teachers' Day, Vietnam Culture Day (from 2026), Christmas Eve and Christmas.

For example: `12/10 • Vietnamese Teachers' Day`. Holidays sharing a date remain in **one** event. [Catalog and sources](docs/HOLIDAYS.md). This is a calendar of festivals and observances; compensatory leave and workday swaps depend on annual announcements.

Dates follow Vietnam time (GMT+7). The calendar refreshes automatically at 07:17 Vietnam time on the first day of each month, covering the current year and the next ten years. Leap months are labeled, and annual lunar festivals occur in regular months.


## 2. Create a custom calendar with Python

Use Python 3.11 or later. Download the source and install dependencies:

```sh
git clone https://github.com/cmduyeen/lich-am-viet-nam.git
cd lich-am-viet-nam
python -m pip install -r requirements.txt
```

**Choose a language**, with all holidays included by default:

```sh
python main.py --language en
python main.py --language vi
```

**Choose which holidays** to annotate, for example Lunar New Year and Mid-Autumn Festival:

```sh
python main.py --language en --holidays tet-1,tet-2,tet-3,mid-autumn
```

Change `en` to `vi` for Vietnamese. Use `--holidays none` for lunar dates and first/fifteenth lunar day labels only. Every selection still includes **every day**.

<details>
<summary>Holiday IDs and personal dates</summary>

List all available holiday IDs:

```sh
python main.py --list-holidays --language en
```

| ID | Holiday |
| --- | --- |
| `tet-1`, `tet-2`, `tet-3` | Lunar New Year, days 1–3 |
| `new-year-eve` | Lunar New Year's Eve |
| `god-of-wealth` | God of Wealth Day |
| `first-full-moon` | First Full Moon Festival |
| `hung-kings` | Hung Kings' Commemoration Day |
| `buddha-birthday` | Buddha's Birthday |
| `doan-ngo` | Doan Ngo Festival |
| `vu-lan` | Vu Lan Festival |
| `mid-autumn` | Mid-Autumn Festival |
| `kitchen-gods` | Kitchen Gods Day |
| `new-year` | New Year's Day |
| `reunification` | Reunification Day |
| `labour-day` | International Workers' Day |
| `national-day` | National Day |
| `valentine` | Valentine's Day |
| `international-women` | International Women's Day |
| `children` | Children's Day |
| `family` | Vietnamese Family Day |
| `vietnamese-women` | Vietnamese Women's Day |
| `teachers` | Vietnamese Teachers' Day |
| `culture` | Vietnam Culture Day (from 2026) |
| `christmas-eve`, `christmas` | Christmas Eve, Christmas |
| `han-thuc`, `ha-nguyen` | Han Thuc, Ha Nguyen |

Copy [examples/holidays.json](examples/holidays.json) to `.local/holidays.json` and edit it to add private family memorials, birthdays, or anniversaries. Each entry accepts a `calendar` type (`lunar` or `solar`), `month`, `day`, and names in `vi`/`en`:

```json
[
  {
    "calendar": "lunar",
    "month": 3,
    "day": 12,
    "name": {"vi": "Ngày giỗ gia đình", "en": "Family memorial day"}
  }
]
```

```sh
python main.py --language en --holidays tet-1,mid-autumn --custom-holidays .local/holidays.json
```

Custom dates are merged with your chosen holidays. Lunar dates only apply to standard months; day 30 applies only to full lunar months, and February 29 applies only to leap solar years. Overlapping events on the same day are consolidated into **one** event.

</details>

Standard feeds are generated in `output/`: `viet_lunar_latest.ics` (Vietnamese) and `viet_lunar_en_latest.ics` (English). When selecting specific holidays or supplying personal dates, files are written to `.local/output/` (ignored by Git) under names such as `viet_lunar_custom_en_latest.ics`, keeping private files separate from quick subscription feeds.

Add `--year 2027` to export for 2027 only, `--start 2026 --end 2036` to specify a year span, `--split` to output separate annual files alongside ZIP archives, or `--output-dir my-calendar` to specify a custom folder.

Import your generated `.ics` file into your calendar app. If you want a customized calendar to auto-sync, host the file at a persistent public URL and re-run the generator when updating; the standard subscription URLs above update automatically every month. Any personal dates in a public calendar will be visible to others; keep private calendars in `.local/` to avoid publishing them.


## 3. Frequently Asked Questions (FAQ)

<details>
<summary><strong>Why should I subscribe via URL instead of downloading and importing the .ics file?</strong></summary>

Subscribing via URL establishes a live subscription link with the repository. Your calendar automatically syncs monthly updates (covering a continuous 10-year rolling window and any newly gazetted holidays). If you download and import a `.ics` file, events become static entries that never update automatically, leading to event duplication when re-importing later.
</details>

<details>
<summary><strong>Will the lunar dates shift incorrectly if I live overseas (US, Australia, Japan, etc.)?</strong></summary>

No. All events are configured as standard **All-Day events** anchored to astronomical Vietnam Time (UTC+7). Regardless of whether your local device is set to US Pacific, Eastern, Central European, or Australian time, the event remains bound to the correct calendar day corresponding to Vietnam's schedule. This ensures overseas Vietnamese can accurately track memorial days, full moons, and traditional Tết celebrations.
</details>

<details>
<summary><strong>What algorithm is used to calculate the lunar dates?</strong></summary>

Dates are computed using the canonical astronomical algorithms developed by Dr. Ho Ngoc Duc (Institute of Information Technology, Vietnam), calibrated to the UTC+7 (Hanoi) reference meridian. Holiday schedules strictly reference the Vietnamese Labor Code (Law No. 45/2019/QH14) and relevant national resolutions (details in [docs/HOLIDAYS.md](docs/HOLIDAYS.md)).
</details>

<details>
<summary><strong>Does this calendar show compensatory days off or swapped workdays?</strong></summary>

This calendar tracks astronomical lunar dates, traditional festivals, and national cultural observances. Compensatory days off and swapped working schedules vary annually based on official government announcements; the project preserves the authentic holiday dates without presuming unannounced administrative swaps.
</details>

<details>
<summary><strong>Does the project collect any user data or contain ads?</strong></summary>

None whatsoever. This project is 100% open-source and non-commercial. It contains no tracking, no telemetry, and no advertisements. When building personal calendars with private memorial dates via Python, data is kept strictly on your local machine under `.local/` (which is excluded from Git tracking).
</details>

---

[Operations and maintenance](docs/OPERATIONS.md) · [Security and privacy](SECURITY.md)

<p align="center">
  Open source under the <a href="LICENSE">MIT License</a>.
</p>
