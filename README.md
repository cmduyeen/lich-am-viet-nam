# 🌙 Global Lunar Calendars

Choose a region, then open a country guide. Each guide has an English version, a native-language version and a copyable calendar URL.

## 1. Choose your calendar

<details>
<summary><strong>East Asia</strong></summary>

- **China** — [English](china/README.md) · [简体中文](china/README.zh-Hans.md)
- **Taiwan** — [English](taiwan/README.md) · [繁體中文](taiwan/README.zh-Hant.md)
- **Hong Kong** — [English](hong-kong/README.md) · [繁體中文](hong-kong/README.zh-Hant.md)
- **Macao** — [English](macao/README.md) · [繁體中文](macao/README.zh-Hant.md)
- **South Korea** — [English](south-korea/README.md) · [한국어](south-korea/README.ko.md)

</details>

<details>
<summary><strong>Southeast Asia</strong></summary>

- **Vietnam** — [English](vietnam/README.md) · [Tiếng Việt](vietnam/README.vi.md)
- **Singapore** — [English](singapore/README.md) · [简体中文](singapore/README.zh-Hans.md)
- **Malaysia** — [English](malaysia/README.md) · [Bahasa Melayu](malaysia/README.ms.md)

</details>

<details>
<summary><strong>North America</strong></summary>

- **[United States](united-states/README.md)** — choose Vietnamese, Chinese or Korean tradition.

</details>

## 2. Customize with Python

One shared generator; no separate country applications. Run from this root folder after installing Python 3.11+ and requirements.txt:

```powershell
python main.py --config vietnam/calendar.config.json
python main.py --country US --tradition vietnamese --language en
```

Configurations live next to each country’s two guides. Generated calendars stay in output/ so existing subscription URLs remain stable. Defaults cover the current year and next year; scheduled generation is annual, with immediate rebuilds for fixes. Yearly files and ZIPs are optional via --split --output-dir exports. A local folder rename does not rename the GitHub repository or publish new URLs.

## Status and development

New feeds require publication to main before subscription. Native-language review and live calendar-app checks are still pending. Nigeria, Egypt, Brazil and Mexico are roadmap markets, not supported calendar profiles.

[Development](docs/DEVELOPMENT.md) · [Automation](docs/AUTOMATION.md) · [Feed inventory](output/index.json) · [Release checklist](docs/RELEASE.md) · [MIT](LICENSE)

[cmduyeen](https://github.com/cmduyeen)
