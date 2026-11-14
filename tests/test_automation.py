from pathlib import Path
import json
import tempfile
import subprocess
import sys
import os
import unittest
from unittest.mock import patch
from dataclasses import replace
from datetime import date
from src.release_state import fingerprint, is_current, write_state, digest
from src.output_lock import output_lock
from src.pipeline import occurrences, _collect_occurrences
from src.user_config import CalendarOptions
from src.ics_generator import LunarCalendarGenerator
from src.profiles import RULES

class AutomationTests(unittest.TestCase):
    def test_freshness_checks_year_config_sources_and_every_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'src').mkdir();(root/'out').mkdir()
            for name in ('main.py','generate_all.py','requirements.txt','src/a.py','src/data.json'):
                (root/name).write_text('data',encoding='utf-8')
            config=root/'custom.json';config.write_text('{}')
            first=fingerprint(root,2026,[config])
            self.assertEqual(first,fingerprint(root,2026,[config]))
            self.assertNotEqual(first,fingerprint(root,2027,[config]))
            config.write_text('{"feed_name":"family"}')
            self.assertNotEqual(first,fingerprint(root,2026,[config]))
            (root/'src/a.py').write_text('changed')
            self.assertNotEqual(first,fingerprint(root,2026,[]))
            out=root/'out';(out/'test.ics').write_bytes(b'calendar')
            (out/'index.json').write_text(json.dumps([{'file':'test.ics','sha256':digest(b'calendar')}]))
            write_state(out,first)
            self.assertTrue(is_current(out,first))
            self.assertFalse(is_current(out,'different'))
            (out/'test.ics').write_bytes(b'corrupt')
            self.assertFalse(is_current(out,first))
            (out/'test.ics').unlink()
            self.assertFalse(is_current(out,first))

    def test_invalid_state_and_path_escape_never_skip_build(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)
            for raw in ('{','[]',json.dumps({'schema':1,'fingerprint':'x','files':{'../outside':'x','index.json':'x'}})):
                (out/'.build-state.json').write_text(raw)
                self.assertFalse(is_current(out,'x'))

    def test_output_lock_is_exclusive_and_released_after_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'output'
            with self.assertRaisesRegex(RuntimeError,'simulated'):
                with output_lock(out):
                    with self.assertRaisesRegex(ValueError,'Another generator'):
                        with output_lock(out):self.fail('must not enter')
                    raise RuntimeError('simulated')
            with output_lock(out):pass

    def test_semantic_cache_ignores_language_colors_and_residence(self):
        _collect_occurrences.cache_clear()
        base=CalendarOptions(country='CN',language='en',content='festivals')
        first=occurrences(2026,2026,base)
        misses=_collect_occurrences.cache_info().misses
        second=occurrences(2026,2026,replace(base,language='zh-Hans',holiday_color='#123ABC'))
        third=occurrences(2026,2026,CalendarOptions(country='US',tradition='chinese',language='zh-Hant',content='festivals'))
        self.assertIs(first,second);self.assertIs(first,third)
        self.assertEqual(_collect_occurrences.cache_info().misses,misses)
        with self.assertRaises(TypeError):first[date(2026,1,1),'bad']=()

    def test_multiple_festivals_on_same_day_are_retained(self):
        events=LunarCalendarGenerator().generate_year(2026,CalendarOptions(country='HK',content='festivals',language='zh-Hant')).walk('VEVENT')
        selected=[e for e in events if e.decoded('dtstart')==date(2026,5,24)]
        self.assertEqual({str(e['x-lunar-event-id']) for e in selected},{'buddha_east','tam_kung'})
        self.assertEqual(len({str(e['uid']) for e in selected}),2)

    def test_added_korean_festival_days_match_official_2026_dates(self):
        # Korea Tourism Organization: Seollal Feb 16-18, Chuseok Sep 24-26.
        events=LunarCalendarGenerator().generate_year(2026,CalendarOptions(country='KR',content='festivals',language='ko')).walk('VEVENT')
        actual={str(e['x-lunar-event-id']):e.decoded('dtstart').isoformat() for e in events}
        for identity,expected in {'new_year_eve':'2026-02-16','lunar_new_year':'2026-02-17','seollal_day_2':'2026-02-18','chuseok_eve':'2026-09-24','chuseok':'2026-09-25','chuseok_day_2':'2026-09-26'}.items():
            self.assertEqual(actual[identity],expected)

    def test_added_macau_days_match_tourism_office_2026_dates(self):
        # MGTO A-Ma 2026/5/9; Feast of Na Tcha 2026/7/2.
        events=LunarCalendarGenerator().generate_year(2026,CalendarOptions(country='MO',content='festivals',language='en')).walk('VEVENT')
        actual={str(e['x-lunar-event-id']):e.decoded('dtstart').isoformat() for e in events}
        self.assertEqual(actual['mazu'],'2026-05-09')
        self.assertEqual(actual['na_tcha'],'2026-07-02')

    def test_new_holidays_do_not_repeat_in_2028_leap_fifth_month(self):
        events=LunarCalendarGenerator().generate_year(2028,CalendarOptions(country='MO',content='festivals',language='en')).walk('VEVENT')
        self.assertEqual(sum(str(e['x-lunar-event-id'])=='na_tcha' for e in events),1)
        self.assertEqual(sum(str(e['x-lunar-event-id'])=='dragon_boat' for e in events),1)

    def test_process_lock_releases_after_actual_process_termination(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'out'
            script="import sys,time; from src.output_lock import output_lock; "+"\nwith output_lock(sys.argv[1]):\n print('locked',flush=True)\n time.sleep(30)"
            child=subprocess.Popen([sys.executable,'-u','-c',script,str(output)],
                cwd=Path(__file__).resolve().parents[1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            try:
                self.assertEqual(child.stdout.readline().strip(),'locked')
                with self.assertRaisesRegex(ValueError,'Another generator'):
                    with output_lock(output):self.fail('must not acquire')
            finally:
                child.terminate();child.communicate(timeout=5)
            with output_lock(output):pass

    def test_bad_json_types_and_windows_bom_are_handled(self):
        from src.user_config import load_calendar_options
        for data in ({'countries':None},{'countries':False},{'country':'US','tradition':{}},{'country':'US','tradition':[]}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                CalendarOptions.from_mapping(data)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'calendar.json'
            path.write_text('{"country":"VN","language":"vi"}',encoding='utf-8-sig')
            self.assertEqual(load_calendar_options(path).language,'vi')

    def test_fresh_batch_does_not_invoke_any_generator(self):
        from generate_all import main
        with tempfile.TemporaryDirectory() as temp:
            with patch('generate_all.is_current',return_value=True), patch('generate_all.build_files',side_effect=AssertionError('unnecessary build')):
                self.assertEqual(main(['--if-needed','--output-dir',str(Path(temp)/'out')]),0)
