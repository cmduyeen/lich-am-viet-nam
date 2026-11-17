# Automatic updates and recovery

The generator is ordinary Python code. No editor, production web server, or paid calendar service is required.

## GitHub Actions: daily health check

The workflow checks every day at 00:17 UTC (07:17 Vietnam time), on source changes and on manual dispatch. It checks source fingerprints, the current year and all recorded checksums before installing dependencies. Healthy scheduled runs skip dependency setup, generation, browser tests, artifacts and commits. A failed or dropped run can be retried by the next daily invocation.

When inputs or coverage change, it builds the two Vietnamese/English feeds in staging, validates them and publishes only changed public files. UIDs remain stable for overlapping years. Invalid inventory metadata is rebuilt without deleting unknown private files. There are no dummy commits to keep GitHub active.

Set `PUBLISH_LUNAR_FEEDS=true` once; main-branch maintenance fails visibly if publication is disabled. Repository rules must allow the workflow token to update generated output on main. GitHub notification settings determine whether the owner receives failure emails.

## Recover GitHub inactivity disablement

GitHub can disable scheduled workflows in public repositories after 60 days without repository activity. A daily cron inside that same disabled workflow cannot re-enable itself. See [GitHub's documented behavior](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).

Install the existing maintenance helper once on a computer you regularly use:

```powershell
gh auth status
gh variable set PUBLISH_LUNAR_FEEDS --body true --repo cmduyeen/lich-am-viet-nam
python src/maintenance.py --repo cmduyeen/lich-am-viet-nam --dry-run
python src/maintenance.py --repo cmduyeen/lich-am-viet-nam --install-task
```

The Windows task runs at 07:35 local time and when the same user logs in. It uses Python 3.11+ and that user's existing GitHub CLI login; no project virtual environment, password or new token is required. It recovers only inactivity-disabled workflows, dispatches when the two feeds need coverage or inventory repair, and avoids duplicate runs. Manually disabled workflows remain disabled.

It catches up after missed schedules, ignores overlapping starts and retries failed requests up to three times at 30-minute intervals. Logs stay in ignored `.maintenance.log`. It runs under the current user with limited privileges, so that user must be logged in and the computer/network must be available. It cannot execute while the machine is powered off; the logon trigger catches up when you return. The helper does not claim permanent operation if the computer is abandoned or its GitHub login is revoked.

Verify after setup:

```powershell
Get-ScheduledTaskInfo -TaskName VietnameseLunarCalendarMaintenance
Get-Content .maintenance.log -Tail 5
```

If an older `LunarCalendarsAnnual` task was installed, it is redundant; it can be removed in Task Scheduler after verifying the new task. The installer does not delete other tasks.

On an existing always-on Linux machine, use the same standard-library guard with authenticated `gh` (UTC example):

```cron
35 0 * * * cd /path/to/lich-am-viet-nam && /usr/bin/python3 src/maintenance.py --repo owner/repo --log-file .maintenance.log
```

Only one external guard is needed. If you require recovery while your personal computer is always off, run it on an always-on machine or an independently configured external scheduler.

## Local generation and supported scope

```powershell
python generate_all.py --if-needed
python main.py --language vi --custom-holidays .local/holidays.json
```

Default coverage is the current year plus next year, within the verified Vietnamese engine range of 1901–2099. This is not an unlimited-year guarantee. Source changes, dependency updates, platform policy changes and new official observances may still require maintenance. The Google/Apple/Outlook application controls its URL refresh interval independently of generation.
