# Feeds

Default subscriptions contain lunar festivals. The country guides provide English and native-language instructions; these additional modes use the same naming convention:

| Content | Meaning | Example |
| --- | --- | --- |
| festivals | Traditional lunar festivals | `lunar_vn_vietnamese_vi_festivals_latest.ics` |
| observances | Festivals plus lunar days 1 and 15 | `lunar_vn_vietnamese_vi_observances_latest.ics` |
| daily | Every lunar day plus festivals | `lunar_vn_vietnamese_vi_daily_latest.ics` |

Prefix the filename with `https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/` to subscribe. New files are not live until published to main. `output/index.json` is the authoritative generated inventory. Each record includes dates, sources, language, content, SHA256 and live-app test status.

Country and tradition prefixes are `vn_vietnamese`, `cn_chinese`, `tw_chinese`, `hk_chinese`, `mo_chinese`, `kr_korean`, `sg_chinese`, `my_chinese`. Use only a language listed for that profile in the README. The default merged example is `lunar_cn-kr-vn_merged_en_festivals_latest.ics`.

Existing subscriptions:

- `viet_lunar_latest.ics`: full Vietnamese calendar.
- `viet_lunar_en_latest.ics`: full English Vietnamese calendar.
- `viet_lunar_minimal_latest.ics`: Vietnamese Full Moon and Lunar New Year.
- `viet_lunar_en_minimal_latest.ics`: English Full Moon and Lunar New Year.

Legacy modes retain one event per selected civil date and existing UID format. Calendar corrections retain the date-based UID format; new semantic feeds have separate identifiers. This is why users should choose one feed version instead of subscribing to overlapping feeds.

Solar-term events such as Qingming are excluded from lunar-only festival feeds. To include available solar and solar-term rules, generate a custom feed with `--holiday-types all`. No workday, substitute-day or government leave schedule is implied.

The separate Chinese repository's old URL cannot redirect subscribers automatically. Move subscriptions to this repository when the new feed has passed the release checklist. Do not delete the old repository as part of the migration.


## United States community subscriptions

US residence profiles reuse the Vietnamese, Chinese or Korean source calendar without changing its civil dates. They are not US public-holiday schedules. From the main README open North America → United States, then choose the community folder and its English or native-language guide. Copy the complete URL from its text block.

| Tradition | Source calendar | Languages |
| --- | --- | --- |
| vietnamese | VN, UTC+7 rules | en, vi |
| chinese | CN, UTC+8 rules | en, zh-Hans, zh-Hant |
| korean | KR, Korean table through 2050 | en, ko |

Files follow `lunar_us_{tradition}_{language}_{content}_latest.ics`; content is festivals, observances or daily. Example: `lunar_us_vietnamese_vi_festivals_latest.ics`. Use the same raw main/output URL prefix documented above. New links only become available after publication.

```powershell
python main.py --country US --tradition vietnamese --language vi
python main.py --country US --tradition chinese --language zh-Hant
python main.py --country US --tradition korean --language ko
python main.py --country VN --residence US --language vi
python main.py --countries VN,CN,KR --residence US --language en
```

For JSON customization, set country to US and provide tradition, language and optional content/filters. Or use a source country with residence US. These forms share canonical configuration and naming. US source-calendar dates stay all-day dates even in New York, Los Angeles or Honolulu; changing a host timezone must not shift Tết or Seollal to the previous day. Choose either the source feed or the US residence feed to avoid overlapping subscriptions.


## Small annual rolling window

The default feed covers the current Gregorian year and the next year (two years total). On year rollover, the previous year leaves the subscribed feed; keep snapshots separately if history matters. Explicit --start/--end or JSON years still allow a custom range. The same resolve_year_range helper controls CLI and batch defaults, with source-calendar year bounds enforced.

The standard batch writes only *_latest.ics and index.json. It retires dated ICS/ZIP exports only for active managed non-custom prefixes, after all new files pass validation, with rollback on failure. Unrelated files and custom exports are preserved. Use --split --output-dir exports for permanent snapshots outside managed output/.

The annual GitHub schedule targets January 1, 00:00 UTC (07:00 Vietnam time); execution can be delayed. Code/data pushes and workflow_dispatch still allow immediate corrections. Public repositories can have scheduled workflows disabled after 60 inactive days: maintain repository activity and monitor the workflow, or arrange an external scheduler that enables the workflow when needed and then calls workflow_dispatch. An annual cron alone is not a guarantee of unattended operation on an inactive public repository. See [GitHub's documented limit](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). New feeds still require release review and publication before the URLs work.
