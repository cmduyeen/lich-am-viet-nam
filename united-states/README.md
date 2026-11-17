# United States — community lunar calendars

English is the main guide language here. Choose the tradition and community language you use. These calendars keep original festival dates; they are not US federal/state holiday schedules.

## Choose a community

- **Vietnamese** — [English](vietnamese/README.md) · [Tiếng Việt](vietnamese/README.vi.md)
- **Chinese · Simplified** — [English](chinese/README.md) · [简体中文](chinese/README.zh-Hans.md)
- **Chinese · Traditional** — [English](chinese-traditional/README.md) · [繁體中文](chinese-traditional/README.zh-Hant.md)
- **Korean** — [English](korean/README.md) · [한국어](korean/README.ko.md)

## Custom generation

```powershell
python main.py --country US --tradition vietnamese --language vi
python main.py --country US --tradition chinese --language zh-Hant
python main.py --country US --tradition korean --language ko
```

US feeds use English by default. A tradition is required; the source calendars remain distinct. All-day dates do not move to a previous date because of US timezones. Do not subscribe to both the original and US counterpart unless you want overlapping events.

[All countries](../README.md) · [Sources and release checks](../docs/RELEASE.md)
