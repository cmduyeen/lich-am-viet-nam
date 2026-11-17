import json
import unittest
from src.maintenance import maintain

class FakeGitHub:
    def __init__(self,year=2026,state='active',coverage=2026,publish='true',running=False,ready=True):
        self.year=year;self.state=state;self.coverage=coverage;self.publish=publish
        self.running=running;self.ready=ready;self.writes=[]
    def api(self,path):
        if path.endswith('main.yml'):return {'state':self.state}
        if 'variables/' in path:return {'value':self.publish}
        if '/runs?' in path:return {'workflow_runs':[{'status':'in_progress','html_url':'https://github.com/run/1'}] if self.running else []}
        raise AssertionError(path)
    def content(self,repo,path):
        if path.endswith('main.yml'):return 'python3 src/release_state.py --check' if self.ready else 'old workflow'
        if path=='output/index.json':
            return json.dumps([{'file':f'{code}_latest.ics','countries':[code],'start_year':self.coverage,'end_year':self.coverage+1} for code in ('VN','CN','TW','HK','MO','KR','SG','MY')])
        raise AssertionError(path)
    def enable(self,repo):self.writes.append('enable')
    def dispatch(self,repo):self.writes.append('dispatch')

class MaintenanceTests(unittest.TestCase):
    def test_current_year_uses_no_write_or_dispatch(self):
        client=FakeGitHub();result=maintain('owner/repo',client,2026)
        self.assertEqual(result['status'],'current');self.assertEqual(client.writes,[])
    def test_stale_year_dispatches_once(self):
        client=FakeGitHub(coverage=2025)
        self.assertEqual(maintain('owner/repo',client,2026)['status'],'dispatched')
        self.assertEqual(client.writes,['dispatch'])
    def test_inactivity_is_recovered_before_dispatch(self):
        client=FakeGitHub(coverage=2025,state='disabled_inactivity')
        maintain('owner/repo',client,2026)
        self.assertEqual(client.writes,['enable','dispatch'])
    def test_fresh_inactive_workflow_only_needs_reenabling(self):
        client=FakeGitHub(state='disabled_inactivity')
        self.assertEqual(maintain('owner/repo',client,2026)['status'],'current')
        self.assertEqual(client.writes,['enable'])
    def test_running_build_is_not_duplicated(self):
        client=FakeGitHub(coverage=2025,running=True)
        self.assertEqual(maintain('owner/repo',client,2026)['status'],'already-running')
        self.assertEqual(client.writes,[])
    def test_dry_run_performs_no_mutation(self):
        client=FakeGitHub(coverage=2025,state='disabled_inactivity')
        result=maintain('owner/repo',client,2026,dry_run=True)
        self.assertEqual(result['actions'],['enable-workflow','dispatch-workflow'])
        self.assertEqual(client.writes,[])
    def test_disabled_publication_or_manual_optout_is_respected(self):
        for client in (FakeGitHub(coverage=2025,publish='false'),FakeGitHub(state='disabled_manually')):
            with self.assertRaises(ValueError):maintain('owner/repo',client,2026)
            self.assertEqual(client.writes,[])
    def test_old_workflow_and_invalid_repo_are_not_run(self):
        for repo,client in [('owner/repo',FakeGitHub(ready=False)),('owner/repo --bad',FakeGitHub())]:
            with self.assertRaises(ValueError):maintain(repo,client,2026)
            self.assertEqual(client.writes,[])
