# Development

One project, one Python source folder (`src/`). The two root Python files are thin CLI entry points. Documentation, tests and generated artifacts stay outside source. No country-specific application copies or web service are needed.

The pipeline consumes validated immutable options, resolves profiles, uses a cached engine, selects semantic festival identities, merges equal identities on equal local dates, localizes, then serializes. Country codes do not identify an engine or a language. Single-country SG/MY commands require an explicit Chinese tradition. A merged selection uses each registered profile’s stated tradition, so Vietnamese/Korean feeds can be combined with the Chinese-tradition SG/MY profiles without forcing one tradition on every country.

`src/profiles.py` is the registry and rule catalog; `src/engines.py` owns the cached Vietnamese, Chinese and Korean engines; `src/locales.json` and `src/localization.py` contain strict locale lookup. `src/pipeline.py` has common selection/merge logic. `src/build.py` and `src/ics.py` handle reuse, revisions, validation and publication. The original Vietnamese implementation stays behind a compatibility facade while new feeds use the common pipeline.

## Add a country

1. Reuse an engine only if calendar rules really agree. Otherwise add a new function to the engine module with explicit year bounds and a cache independent of language.
2. Add a profile, official reference sources, native language, supported languages and explicit tradition. Modern time-zone rules are not a historical calendar reconstruction.
3. Add stable festival identities and date rules. Reuse an identity only when it is the same observance; Dano, Chuseok and Vietnamese Vu Lan retain distinct identities. Never classify holidays by searching translated strings.
4. Add complete display strings and any local-name overrides. Do not silently fall back to another language. Include local descriptions, month labels, leap-month labels and calendar metadata. Obtain independent native-language review before release.
5. Add independent, source-attributed fixtures for New Year, major festivals, leap months and divergence from existing engines. Upstream regression fixtures supplement, but do not replace, official independent data.
6. Update the English/native pair for each affected country together. Add the language to the selector only once its guide is complete. Run tests and build candidates; finish the release checklist before enabling publication.

## Roadmap

Stage 1: VN, CN, TW, HK, MO, KR, and Chinese-tradition SG/MY. Stage 2: Thai, Khmer, Lao, Myanmar and Sri Lankan Buddhist profiles, each with its own verified rules. They are not published lunar profiles today. Other calendars follow only when sources and regional variations can be represented accurately. The experimental 51-country holiday list is not a lunar-support claim.

## Verify and benchmark

```powershell
python -m unittest discover -s tests -v
python generate_all.py
python generate_all.py --split
python -m src.benchmark
```

Generation is offline. Only test-fixture maintenance and dependency updates need a network. The benchmark reports cold/warm generation and verifies a second language does not add conversions. Compare on the same runner; do not promise machine-independent latency. The static ICS download is served by GitHub; application refresh delays are outside the generator's control.

Generation stages every file and validates it before output replacement. On local failure the publisher restores previous output bytes; on GitHub, a single commit publishes the validated set. There are no destructive cleanup operations across unrelated feed prefixes. The index is written last. Repeated runs retain unchanged event timestamps, sequences and deterministic ZIP metadata.

The annual build publishes only the rolling latest files for new profiles. Yearly files, dated aggregate copies and ZIPs are optional via --split. Default builds retain only rolling latest files, including legacy subscriptions. This avoids storing duplicate multi-year daily feeds for every locale.

Astronomical calculations use the pinned lunar-python ephemeris (MIT); Korean dates use korean-lunar-calendar (MIT). These dependency licenses remain with their distributions.


## Residence and worldwide expansion

The US is the first supported residence outside Asia. A residence describes the audience and available traditions; it is not a new lunar engine or national-holiday catalog. `--country US --tradition vietnamese` resolves to the VN source profile with `residence=US`; `--country VN --residence US` is the equivalent explicit form. Both produce the same canonical options and filenames. Traditions vietnamese/chinese/korean map to VN/CN/KR. Default/native display language for US feeds is English. Chinese US feeds additionally support traditional Chinese as a display locale, retaining the CN festival catalog rather than silently substituting TW/HK/MO rules.

US feeds use `lunar_us_{tradition}_{language}_{content}_latest.ics` and separate residence-scoped UIDs. Manifest records retain their source countries and add residence, residence sources and the source-calendar civil-date policy. Calendar/event metadata distinguishes residence from source tradition. All-day `DATE` boundaries are preserved; no single timezone is assigned to the multi-timezone US. These feeds cover the original cultural festival dates, not US federal/state holidays or individually chosen local celebration dates. Do not subscribe to both a source feed and its US counterpart unless you want overlapping events.

For a new residence reusing these engines, add its tradition mapping and supported locales, translated country name and residence note, tests comparing all-day dates against the original profile, and localized copyable README links. The batch generator iterates the registry automatically. For a different calendar such as Hijri, first implement and independently validate local rules and confirmed-versus-estimated date handling.

Next outside-Asia markets are Nigeria and Egypt for Islamic traditions, then Brazil and Mexico if national holidays enter scope. These are roadmap entries, not working calendar profiles. Do not publish placeholder feeds for them. The Buddhist expansion remains an independent roadmap track. No population statistics are embedded in the generator.


## Country folders and documentation

The project root is lunar-calender. Country folders are vietnam, china, taiwan, hong-kong, macao, south-korea, singapore and malaysia. Each holds README.md (English), exactly one README.<native-locale>.md and calendar.config.json. English is also the US main language, so united-states/README.md is a community index; its vietnamese, chinese, chinese-traditional and korean subfolders each contain the same English/native pair plus configuration. Separate Chinese script folders preserve the two-file language convention.

Runtime code stays in src/, with a single main.py and generate_all.py at the root. Country folders contain configuration and documentation, not cloned generator applications. Generated ICS stays in output/; moving local folders does not change subscription URLs. Repository publishing remains a separate step.

Run `python -m src.documentation` to regenerate the country guides and root index. Translated template copy lives in src/documentation.py; locale names and calendar descriptions remain in src/locales.json. Update a country's English/native copy together and review native wording before release. PUBLIC_FEED_BASE_URL in src/config.py is the shared subscription origin. It intentionally preserves the original GitHub URL; change it only when actually publishing to a new repository, then regenerate guides and check every link.

This folder structure provides separate country/language pages for a future website. It does not by itself deploy a site, configure hreflang/canonical URLs, or guarantee search rankings. A future publishing layer should assign canonical country/language URLs and use the existing paired pages as input.


## Small annual rolling window

The default feed covers the current Gregorian year and the next year (two years total). On year rollover, the previous year leaves the subscribed feed; keep snapshots separately if history matters. Explicit --start/--end or JSON years still allow a custom range. The same resolve_year_range helper controls CLI and batch defaults, with source-calendar year bounds enforced.

The standard batch writes only *_latest.ics and index.json. It retires dated ICS/ZIP exports only for active managed non-custom prefixes, after all new files pass validation, with rollback on failure. Unrelated files and custom exports are preserved. Use --split --output-dir exports for permanent snapshots outside managed output/.

The annual GitHub schedule targets January 1, 00:00 UTC (07:00 Vietnam time); execution can be delayed. Code/data pushes and workflow_dispatch still allow immediate corrections. Public repositories can have scheduled workflows disabled after 60 inactive days: maintain repository activity and monitor the workflow, or arrange an external scheduler that enables the workflow when needed and then calls workflow_dispatch. An annual cron alone is not a guarantee of unattended operation on an inactive public repository. See [GitHub's documented limit](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). New feeds still require release review and publication before the URLs work.

## Stable custom subscriptions

Set `"feed_name": "family"` in JSON, or pass `--feed-name family`, before subscribing. This writes `custom_family_latest.ics` independently of filters, colors or years. Keep the name unique and unchanged for that subscription. The batch builder rejects conflicting configurations sharing a name before publication. Unnamed configurations keep the existing hash-based naming behavior.

Event COLOR uses the nearest CSS named color from a small built-in palette, as required by RFC 7986. X-LUNAR-COLOR retains the exact requested RGB; X-APPLE-CALENDAR-COLOR retains calendar-level RGB. Client color rendering remains client controlled.

## Resource-aware automation

`python generate_all.py --if-needed` verifies an input fingerprint, the calendar year, custom JSON and every recorded output checksum before skipping. A new year, source/config change, missing file or changed output triggers a full validated build. `python src/release_state.py --check` is a standard-library-only preflight and works before dependency installation. Builds without `--if-needed` still exercise generation and must produce zero changes for identical inputs.

`src/output_lock.py` prevents concurrent CLI/batch writers from reconciling against stale revisions. The OS releases this lock after a process exits, including crashes; the small persistent lock file is ignored by Git. Staging, validation, rollback and manifest publication remain one shared implementation. Semantic occurrences are cached independently of display language/color/residence, with bounded caches; no network is used during generation.

The workflow checks freshness before setup/install, caps its runtime at 15 minutes, serializes runs per branch, runs browser checks only for PRs or explicit manual requests, and retains review artifacts for three days. Scheduled unchanged runs create no artifact, commit or dependency download. Publication requires `PUBLISH_LUNAR_FEEDS=true` and a change in output bytes. No application server or paid API is required; hosting and Actions remain subject to the account/provider's quotas.

See [browser consumer test instructions](../tests/e2e/README.md) and [festival data sources](FESTIVALS.md).
