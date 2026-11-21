import json
import unittest
from src.maintenance import maintain, coverage_current

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
            return json.dumps([
                {'file': name, 'countries': ['VN'], 'language': language, 'start_year': self.coverage, 'end_year': self.coverage + 1}
                for name, language in (
                    ('viet_lunar_latest.ics', 'vi'),
                    ('viet_lunar_en_latest.ics', 'en'),
                    ('viet_lunar_minimal_latest.ics', 'vi'),
                    ('viet_lunar_en_minimal_latest.ics', 'en'),
                )
            ])
        raise AssertionError(path)
    def enable(self,repo):self.writes.append('enable')
    def dispatch(self,repo):self.writes.append('dispatch')

class MaintenanceTests(unittest.TestCase):
    def test_corrupt_incomplete_and_duplicate_inventory_requests_recovery(self):
        valid = json.loads(FakeGitHub().content('owner/repo', 'output/index.json'))
        invalid = [None, {}, [None], valid[:1], [valid[0], valid[0]],
                   [{**valid[0], 'end_year': True}, valid[1]],
                   [{**valid[0], 'countries': ['CN']}, valid[1]]]
        for inventory in invalid:
            with self.subTest(inventory=inventory):
                self.assertFalse(coverage_current(inventory, 2026))
        client = FakeGitHub()
        original = client.content
        client.content = lambda repo, path: '{broken' if path == 'output/index.json' else original(repo, path)
        self.assertEqual(maintain('owner/repo', client, 2026)['status'], 'dispatched')
        self.assertEqual(client.writes, ['dispatch'])

    def test_transient_read_failure_is_not_treated_as_missing_calendar(self):
        client = FakeGitHub()
        original = client.content
        def failing(repo, path):
            if path == 'output/index.json':
                raise ValueError('HTTP 503 service unavailable')
            return original(repo, path)
        client.content = failing
        with self.assertRaisesRegex(ValueError, '503'):
            maintain('owner/repo', client, 2026)
        self.assertEqual(client.writes, [])

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
