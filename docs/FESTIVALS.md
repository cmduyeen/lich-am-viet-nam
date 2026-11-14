# Lunar festival scope and sources

All events are traditional observances on source-calendar civil dates. Public-holiday entitlement, compensation days and event/parade schedules are separate and are not inferred. A holiday is not repeated in a leap month. Different identities on one day remain separate; for example, Vu Lan and Trung Nguyên in Vietnam, and Buddha’s Birthday and Tam Kung’s Birthday in Hong Kong.

The English/native country guides show each profile’s complete list in a collapsed section. `src/profiles.py` defines the date rules; `src/locales.json` defines display names; `src/festival_sources.json` records sources for this expansion. US residence feeds inherit their selected source profile’s observances without shifting all-day dates.

| Profile | Additions in this release | Rule/source |
| --- | --- | --- |
| Vietnam | Khai Hạ (1/7), Hàn Thực (3/3), Trung Nguyên (7/15, distinct from Vu Lan) | [Vietnamese Embassy / Vietnam News Agency](https://vietnamembassy-usa.org/node/665); dates in month/day order in this table |
| Taiwan | Second day of New Year, Mazu’s birthday (3/23), Qixi (7/7) | [Travel Tainan: religious festivals](https://www.twtainan.net/en/statics/religion/) |
| Hong Kong | Second/third days of New Year, Tin Hau (3/23), Tam Kung (4/8) | [Chinese Temples Committee](https://www.ctc.org.hk/en/festival/); [2026 government New Year dates](https://www.info.gov.hk/gia/general/202505/16/P2025051300353.htm) |
| Macao | Second day of New Year, A-Ma (3/23), Na Tcha (5/18) | [Cultural Affairs Bureau](https://www.culture.gov.mo/en/News/detail/12051); [MGTO 2026 Na Tcha date](https://www.macaotourism.gov.mo/en/events/whatson/13374?type=1) |
| South Korea | Day after Seollal; day before/after Chuseok; localized Seollal Eve | [Korea Tourism Organization, 2026 dates](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140038) |
| Singapore | Second day of Chinese New Year | [Ministry of Manpower: 2026 dates](https://www.mom.gov.sg/newsroom/press-releases/2025/0616-public-holidays-for-2026) |
| Malaysia | Second day of Chinese New Year | [Tourism Malaysia: Chinese New Year season](https://www.tourism.gov.my/media/view/chinese-new-year) |
| China | Existing regional Little New Year, Qixi, Laba, Double Ninth and core festivals retained | [Chinese date conversion references](https://www.hko.gov.hk/en/gts/time/conversion.htm) |

The last day of the lunar year is calculated by checking the next date, so New Year’s Eve works in both 29-day and 30-day final months. In Korea, the eve, Seollal and the following day are three separate all-day events. Chuseok uses lunar 8/14, 8/15 and 8/16. These dates never imply a substitute holiday.

Qingming is a solar-term festival, not a fixed lunar date. Existing profiles expose it only with `--holiday-types all` or `solar`; default lunar-only links retain their stated scope. Buddhist traditions in Thailand, Cambodia, Laos, Myanmar and Sri Lanka require separate engines/rules and are not inferred from the Chinese Buddha birthday.

New festival data is added to new profile feeds. Previously released Vietnamese compatibility feeds retain their original selection and UID format. Use the country-specific festival/daily link for the expanded catalog.
