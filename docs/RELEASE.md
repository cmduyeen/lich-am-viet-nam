# Release checklist

Automated generation creates candidate artifacts. It is not an independent review or live application subscription test. New subscription URLs become live only after publication to the main branch.

- [x] All automated tests pass in a clean project Python environment (86 tests; Python 3.12 local, Python 3.11 CI checked separately).
- [ ] Reference fixtures and sources reviewed independently, including UTC+7/UTC+8/Korean differences and the 2033 leap month.
- [ ] Native-language review completed for vi, zh-Hans, zh-Hant, ko and ms; English reviewed as the reference guide.
- [ ] Google Calendar: subscribe by URL, confirm all-day boundaries, then update one event under the same UID and confirm no duplication.
- [ ] Apple Calendar: repeat the same subscription and update test.
- [ ] Outlook: repeat the same subscription and update test.
- [ ] Verify merged and component subscriptions separately; document overlapping subscriptions.
- [ ] Confirm that the generated inventory, README URLs, date bounds and checksums agree.
- [ ] Record application versions, test date, reviewer and feed URLs in this file. No live-app test has been performed yet.

After recording successful checks, set the repository Actions variable `PUBLISH_LUNAR_FEEDS` to `true`. Until then the workflow uploads candidates for review and does not commit new feed files automatically. This also applies to forks: their owner enables publication after checking their chosen feed.

For custom automatic subscriptions on a fork, commit `my-calendar.json`, set `CUSTOM_CONFIG` to that path, enable Actions and write permissions, and enable `PUBLISH_LUNAR_FEEDS` after review. A manual workflow input overrides the repository variable for that run only. The generator prints the exact file name. Use your own repository's raw main/output URL; `--year` generates a snapshot, not a rolling subscription.

Annual runs regenerate with pinned data. Dependency/source updates are reviewed changes: pin the new version and hashes, check the upstream release notes, rerun reference tests and inspect event changes before publishing. A calculated future festival is not official confirmation of a work or leave schedule.

US residence review: compare Vietnamese/Chinese/Korean feeds against their original profiles, verify that all-day dates remain unchanged across US timezones, and confirm that no US federal/state public-holiday schedule is implied. Traditional Chinese display for the US Chinese profile must retain the CN festival rules. Test a source feed and its US counterpart separately to avoid overlapping subscriptions.


## Small annual rolling window

The default feed covers the current Gregorian year and the next year (two years total). On year rollover, the previous year leaves the subscribed feed; keep snapshots separately if history matters. Explicit --start/--end or JSON years still allow a custom range. The same resolve_year_range helper controls CLI and batch defaults, with source-calendar year bounds enforced.

The standard batch writes only *_latest.ics and index.json. It retires dated ICS/ZIP exports only for active managed non-custom prefixes, after all new files pass validation, with rollback on failure. Unrelated files and custom exports are preserved. Use --split --output-dir exports for permanent snapshots outside managed output/.

The annual GitHub schedule targets January 1, 00:17 UTC (07:17 Vietnam time); execution can be delayed. Code/data pushes and workflow_dispatch still allow immediate corrections. Public repositories can have scheduled workflows disabled after 60 inactive days: maintain repository activity and monitor the workflow, or arrange an external scheduler that enables the workflow when needed and then calls workflow_dispatch. An annual cron alone is not a guarantee of unattended operation on an inactive public repository. See [GitHub's documented limit](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). New feeds still require release review and publication before the URLs work.

## Automated evidence for this release

The committed [evidence gallery](evidence/README.md) records the tested artifacts, native-browser screenshots and independent-consumer results. These checks cover actual generated ICS and real CLI updates; they do not replace the named application's acceptance checkbox above. The scheduled freshness preflight and `--if-needed` path are tested against year rollover, changed inputs, changed/missing output and conflicting writers.

The annual schedule now targets January 1 at 00:17 UTC (07:17 Vietnam time). GitHub can still disable schedules for inactive public repositories. An external annual guard can enable the workflow and dispatch it only when coverage is stale; it must not generate dummy commits or run a polling loop. The included `src/maintenance.py` guard runs directly under Task Scheduler or cron with an authenticated GitHub CLI. It requires the machine/network to be available; Windows catch-up runs missed tasks when available. No ChatGPT process is involved.
