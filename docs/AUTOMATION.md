# Automation without ChatGPT

Generation and maintenance are ordinary code. No chat, AI subscription, production server or paid calendar API is required.

## Normal operation: GitHub Actions

Merge the reviewed PR, then set the repository Actions variable `PUBLISH_LUNAR_FEEDS` to `true`. The workflow runs on January 1 at 07:17 Vietnam time, relevant main-branch changes and manual dispatch. A two-year feed rolls forward to the current year plus next year at the same URL. Runtime dependencies are hash-pinned.

Before installing dependencies, the workflow checks input fingerprints and every recorded output checksum. An unchanged scheduled run skips installation, generation, browser tests, artifacts and commits. A build that actually runs writes only changed bytes. Runs are serialized, have a 15-minute limit, and do not retry indefinitely. Browser checks are reserved for PRs or explicit manual verification; review artifacts expire after three days.

## Annual recovery guard: code, Task Scheduler or cron

GitHub can disable scheduled workflows after 60 days without repository activity. `src/maintenance.py` checks actual published coverage, recovers only inactivity-disabled workflows, avoids duplicate dispatch when a run already exists, and invokes the same workflow only when a new year needs coverage. A manually disabled workflow stays disabled. There are no dummy commits, keep-alive polling or loops.

Windows setup from the project root:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --require-hashes -r requirements.txt
gh auth status
.venv\Scripts\python.exe src/maintenance.py --repo cmduyeen/lich-am-viet-nam --dry-run
powershell -NoProfile -File src/install_annual_task.ps1
```

The task runs once a year on January 1 at 07:35 Vietnam time. It uses the current Windows user's existing GitHub CLI login, stores no password/token, requires network access, ignores overlapping starts and catches up a missed run when the machine/user becomes available. Logs go to ignored `.maintenance.log`. Use `-Repo your-name/your-fork` when installing for a fork. It can be managed or removed normally in Windows Task Scheduler. No ChatGPT process or browser needs to be open. A powered-off machine cannot execute code; catch-up runs when available.

On an existing always-on Linux machine, use the same standard-library script with authenticated `gh` and a cron entry (this example assumes UTC):

```cron
35 0 1 1 * cd /path/to/lunar-calender && /usr/bin/python3 src/maintenance.py --repo owner/repo --log-file .maintenance.log
```

Only one guard is needed. This is a small annual request, not a background daemon. Provider quotas and the machine's ordinary operating costs still apply; this project provisions no paid services.

## Local generation

```powershell
.venv\Scripts\python.exe generate_all.py --if-needed
.venv\Scripts\python.exe main.py --config vietnam/calendar.config.json --feed-name family
```

Use `--if-needed` for unattended batch runs. Omit it to exercise a full rebuild; identical output must still produce zero changed files. A cross-process OS lock prevents two local writers from reconciling revisions simultaneously and releases on process termination. Publication uses staging, validation, atomic replacement and rollback. GitHub publishes the complete generated set in one commit.
