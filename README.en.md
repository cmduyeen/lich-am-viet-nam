[Tiếng Việt](README.md) · **English**

<h1 align="center">🌙 Vietnamese Lunar Calendar</h1>

<p align="center">
  Vietnamese lunar dates and festivals, synced to your favorite calendar app with one link.
</p>

<p align="center">
  <img width="900" alt="Vietnamese Lunar Calendar preview" src="https://github.com/user-attachments/assets/64fc3e3d-d883-4504-84a3-e5f797dbb7e2" />
</p>

---

## 1. Subscribe quickly by URL

Copy the link below and choose **Add calendar from URL** or **Subscribe to calendar by URL** in your calendar app:

**English**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

**Tiếng Việt**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

Paste the link and save. Subscribe by URL to receive updates automatically. Compatible with Google Calendar, Apple Calendar, Outlook, and other apps that support iCalendar.

Choose one language. For example: `15/8 • Mid-Autumn Festival` or `15/8 • Tết Trung Thu`. The existing Vietnamese subscription URL is unchanged.

### Calendar contents

- Lunar dates for every Gregorian day.
- The first and fifteenth days of each lunar month, and Lunar New Year's Eve.
- Major holidays: New Year's Day, Tết (Vietnamese Lunar New Year), Hùng Kings' Commemoration Day, Reunification Day, International Workers' Day, and National Day.
- Traditional observances: Kitchen Gods' Day, God of Wealth Day, First Full Moon Festival, Buddha's Birthday, Đoan Ngọ Festival, Vu Lan Festival, and Mid-Autumn Festival.

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

Copy and edit [examples/holidays.json](examples/holidays.json) to add memorial dates, birthdays, or anniversaries. Each entry has a `calendar` of `lunar` or `solar`, a `month`, a `day`, and names in both `vi` and `en`:

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
python main.py --language en --holidays tet-1,mid-autumn --custom-holidays examples/holidays.json
```

Personal dates are added to the selected holidays. Lunar holidays occur only in regular months; day 30 appears only in months with 30 days, and February 29 only in leap years. Holidays sharing a date appear together in **one** event.

</details>

Files are saved in `output/`: `viet_lunar_en_latest.ics` (English) or `viet_lunar_latest.ics` (Vietnamese) by default. Selecting holidays or adding personal dates produces `viet_lunar_custom_en_latest.ics` or `viet_lunar_custom_vi_latest.ics`, separate from the quick subscription feeds.

Add `--year 2027` for a single year, `--start 2026 --end 2036` for a range, `--split` for yearly files and a ZIP, or `--output-dir my-calendar` to choose a folder. With `--year`, the filename contains the year instead of `latest`.

Import the generated `.ics` file into your calendar app. To subscribe to a custom calendar by URL, host the file at a fixed public URL and rerun Python when you want to update it. The quick subscription feeds above are updated automatically each month by this repository.

---

<p align="center">
  Open-source software under the <a href="LICENSE">MIT</a> license.
</p>
