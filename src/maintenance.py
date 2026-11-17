"""Annual GitHub maintenance guard. Standard library + authenticated gh CLI only.

Can run from Windows Task Scheduler or cron without ChatGPT or a running editor.
"""
import argparse
import base64
import json
import re
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

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
        inventory=json.loads(github.content(repo,'output/index.json'))
    except ValueError as exc:
        if '404' not in str(exc):raise
        inventory=[]
    managed=[e for e in inventory if not e['file'].startswith('custom_') and '_custom_' not in e['file']]
    covered={code for e in managed for code in e['countries']}
    current=bool(managed) and covered>={'VN','CN','TW','HK','MO','KR','SG','MY'} and all(
        e['start_year']==year and e['end_year']>=min(year+1,e.get('supported_end_year',year+1)) for e in managed)
    if current:return dict(status='current',actions=actions,year=year)
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
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--log-file',type=Path)
    args=parser.parse_args(argv)
    now=datetime.now(timezone(timedelta(hours=7)))
    try:
        result=maintain(args.repo,GitHub(args.gh),now.year,args.dry_run)
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
