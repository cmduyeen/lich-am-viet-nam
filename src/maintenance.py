"""Lightweight GitHub recovery guard. Standard library + authenticated gh CLI only.

Can run from Windows Task Scheduler or cron without ChatGPT or a running editor.
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def task_script(repo, python, gh, script_path, log_path, project_root):
    """Build a fixed least-privilege task; quote values as PowerShell literals."""
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('repo must be owner/repository')
    def literal(value):
        return "'" + str(value).replace("'", "''") + "'"
    assignments = '\n'.join(f'${name} = {literal(value)}' for name, value in (
        ('repo', repo), ('pythonPath', python), ('ghPath', gh),
        ('scriptPath', script_path), ('logPath', log_path), ('projectRoot', project_root)))
    return assignments + r'''
$ErrorActionPreference = 'Stop'
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskName = 'VietnameseLunarCalendarMaintenance'
$taskAction = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`" --repo $repo --gh `"$ghPath`" --log-file `"$logPath`"" -WorkingDirectory $projectRoot
$taskTriggers = @(
    (New-ScheduledTaskTrigger -Daily -At '07:35'),
    (New-ScheduledTaskTrigger -AtLogOn -User $currentUser)
)
$taskSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 30) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $currentUser -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $taskTriggers -Settings $taskSettings -Principal $taskPrincipal -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
'''


def install_task(repo, gh='gh'):
    if os.name != 'nt':
        raise ValueError('Task Scheduler installation requires Windows; use cron on Linux')
    gh_path = shutil.which(gh)
    if not gh_path:
        raise ValueError('GitHub CLI is not installed')
    root = Path(__file__).resolve().parents[1]
    script = task_script(repo, sys.executable, gh_path, Path(__file__).resolve(),
                         root / '.maintenance.log', root)
    GitHub(gh_path).run('auth', 'status', '--hostname', 'github.com')
    encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
    try:
        result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive',
                                 '-EncodedCommand', encoded],
                                capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError('Could not install the Windows maintenance task') from exc
    if result.returncode:
        raise ValueError('Task installation failed; run from your Windows account with Task Scheduler access')
    return dict(status='installed', task='VietnameseLunarCalendarMaintenance',
                schedule='Daily 07:35 local time and user logon; initial check started')

class GitHub:
    def __init__(self, executable='gh'):self.executable=executable
    def run(self,*args):
        try:
            result=subprocess.run([self.executable,*args],capture_output=True,text=True,encoding='utf-8',timeout=45)
        except (OSError,subprocess.TimeoutExpired) as exc:
            raise ValueError('GitHub CLI unavailable or timed out; check gh authentication and network') from exc
        if result.returncode:
            raise ValueError(result.stderr.strip() or 'GitHub request failed')
        return result.stdout
    def api(self,path):return json.loads(self.run('api',path))
    def content(self,repo,path):
        result=self.api(f'repos/{repo}/contents/{path}?ref=main')
        return base64.b64decode(result['content']).decode('utf-8-sig')
    def enable(self,repo):self.run('workflow','enable','main.yml','--repo',repo)
    def dispatch(self,repo):self.run('workflow','run','main.yml','--repo',repo,'--ref','main')

def coverage_current(inventory, year):
    """Treat incomplete/corrupt metadata as stale, never as a permanent crash."""
    expected = {'viet_lunar_latest.ics': 'vi', 'viet_lunar_en_latest.ics': 'en'}
    if not isinstance(inventory, list):
        return False
    managed = [entry for entry in inventory
               if isinstance(entry, dict) and isinstance(entry.get('file'), str)
               and entry['file'] in expected]
    if len(managed) != 2 or {entry['file'] for entry in managed} != set(expected):
        return False
    for entry in managed:
        start, end = entry.get('start_year'), entry.get('end_year')
        limit = entry.get('supported_end_year', year + 1)
        if (any(type(value) is not int for value in (start, end, limit))
                or entry.get('countries') != ['VN']
                or entry.get('language') != expected[entry['file']]
                or start != year or end < min(year + 1, limit) or end < start):
            return False
    return True


def maintain(repo, github, year, dry_run=False):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):
        raise ValueError('repo must be owner/repository')
    workflow=github.api(f'repos/{repo}/actions/workflows/main.yml')
    source=github.content(repo,'.github/workflows/main.yml')
    if 'src/release_state.py' not in source:
        raise ValueError('The resource-aware release workflow is not on main yet; merge the reviewed release first')
    actions=[]
    if workflow['state']=='disabled_inactivity':
        actions.append('enable-workflow')
        if not dry_run:github.enable(repo)
    elif workflow['state']!='active':
        raise ValueError('Workflow is disabled manually or not initialized; no automatic override')
    try:
        inventory_raw=github.content(repo,'output/index.json')
    except ValueError as exc:
        if '404' not in str(exc):raise
        inventory_raw='[]'
    try:
        inventory=json.loads(inventory_raw)
    except (ValueError, TypeError):
        inventory=[]
    if coverage_current(inventory, year):return dict(status='current',actions=actions,year=year)
    variables=github.api(f'repos/{repo}/actions/variables/PUBLISH_LUNAR_FEEDS')
    if variables.get('value')!='true':
        raise ValueError('Automatic publication is disabled: set PUBLISH_LUNAR_FEEDS=true after reviewing the release')
    runs=github.api(f'repos/{repo}/actions/workflows/main.yml/runs?branch=main&per_page=10')
    active=[run for run in runs.get('workflow_runs',[]) if run['status'] in ('queued','in_progress','waiting','pending','requested')]
    if active:return dict(status='already-running',actions=actions,run_url=active[0]['html_url'],year=year)
    actions.append('dispatch-workflow')
    if not dry_run:github.dispatch(repo)
    return dict(status='dry-run' if dry_run else 'dispatched',actions=actions,year=year)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True)
    parser.add_argument('--gh',default='gh')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run',action='store_true')
    mode.add_argument('--install-task',action='store_true',help='Install daily Windows recovery for the current user')
    parser.add_argument('--log-file',type=Path)
    args=parser.parse_args(argv)
    now=datetime.now(timezone(timedelta(hours=7)))
    try:
        result=(install_task(args.repo,args.gh) if args.install_task
                else maintain(args.repo,GitHub(args.gh),now.year,args.dry_run))
        code=0
    except (ValueError,KeyError,TypeError) as exc:
        result=dict(status='error',message=str(exc));code=1
    result['checked_at']=now.isoformat(timespec='seconds')
    raw=json.dumps(result,ensure_ascii=False)
    print(raw)
    if args.log_file:
        args.log_file.parent.mkdir(parents=True,exist_ok=True)
        with args.log_file.open('a',encoding='utf-8') as file:file.write(raw+'\n')
    return code

if __name__=='__main__':raise SystemExit(main())
