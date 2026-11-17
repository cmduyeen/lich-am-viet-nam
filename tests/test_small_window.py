from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo
from src.config import resolve_year_range
from src.ics import obsolete_exports, publish_staged, validate_bytes, write_calendar
from src.ics_generator import LunarCalendarGenerator
from src.user_config import CalendarOptions

ROOT=Path(__file__).resolve().parents[1]


class SmallWindowTests(unittest.TestCase):
    def test_default_window_and_rollover(self):
        self.assertEqual(resolve_year_range(2026),(2026,2027))
        self.assertEqual(resolve_year_range(2027),(2027,2028))
        self.assertEqual(resolve_year_range(2026,start_year=2030),(2030,2031))
        self.assertEqual(resolve_year_range(2049,last_year=2050),(2049,2050))
        self.assertEqual(resolve_year_range(2050,last_year=2050),(2050,2050))

    def test_explicit_range_still_works(self):
        self.assertEqual(resolve_year_range(2026,2026,2036),(2026,2036))
        with self.assertRaises(ValueError): resolve_year_range(2026,2028,2027)

    def test_overlapping_year_keeps_same_event_identities_and_revisions(self):
        generator=LunarCalendarGenerator()
        options=CalendarOptions(country='VN',content='festivals',language='vi')
        first=generator.generate_range(2026,2027,options)
        second=generator.generate_range(2027,2028,options)
        before={str(e['uid']):e.to_ical() for e in first.walk('VEVENT') if e.decoded('dtstart').year==2027}
        after={str(e['uid']):e.to_ical() for e in second.walk('VEVENT') if e.decoded('dtstart').year==2027}
        self.assertEqual(before,after)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'feed.ics'
            write_calendar(first,path)
            write_calendar(second,path)
            self.assertEqual({e.decoded('dtstart').year for e in validate_bytes(path.read_bytes()).walk('VEVENT')},{2027,2028})

    def test_default_cli_outputs_only_a_two_year_latest_file(self):
        with tempfile.TemporaryDirectory() as temp:
            result=subprocess.run([sys.executable,str(ROOT/'main.py'),'--country','VN','--output-dir',temp],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            files=list(Path(temp).iterdir())
            self.assertEqual(len(files),1)
            self.assertTrue(files[0].name.endswith('_latest.ics'))
            year=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).year
            self.assertEqual({e.decoded('dtstart').year for e in validate_bytes(files[0].read_bytes()).walk('VEVENT')},{year,year+1})

    def test_cli_country_can_replace_merged_json_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            config=folder/'merged.json'
            config.write_text(json.dumps({'countries':['VN','CN'],'language':'en','content':'festivals'}),encoding='utf-8')
            result=subprocess.run([sys.executable,str(ROOT/'main.py'),'--config',str(config),'--country','VN','--language','en','--year','2027','--output-dir',str(folder/'out')],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            path,=(folder/'out').glob('*.ics')
            self.assertTrue(all(str(e['x-countries'])=='VN' for e in validate_bytes(path.read_bytes()).walk('VEVENT')))

    def test_json_numbers_are_validated_before_deduplication(self):
        for days in ([1,True],[True,1],[1,1.0],[False],['1']):
            with self.subTest(days=days),self.assertRaises(ValueError):
                CalendarOptions.from_mapping({'lunar_days':days})

    def test_pruning_is_scoped_and_custom_snapshots_survive(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'out';output.mkdir()
            staging=Path(temp)/'stage';staging.mkdir()
            names=['viet_lunar_2026_2036.ics','viet_lunar_2028.ics','viet_lunar_yearly_2026_2036.zip',
                   'viet_lunar_latest.ics','personal.ics','other_2026.ics','viet_lunar_custom_1234abcd_2026.ics']
            for name in names:(output/name).write_bytes(b'old')
            (staging/'viet_lunar_latest.ics').write_bytes(b'new')
            stale=obsolete_exports(output,staging,[{'file':'viet_lunar_latest.ics'}])
            self.assertEqual(set(stale),set(names[:3]))
            publish_staged(staging,output,obsolete=stale)
            self.assertTrue(all(not (output/name).exists() for name in names[:3]))
            self.assertTrue(all((output/name).exists() for name in names[3:]))

    def test_removed_exports_are_restored_on_publish_failure(self):
        import src.ics as ics
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);output=folder/'out';staging=folder/'stage'
            output.mkdir();staging.mkdir()
            (output/'old.ics').write_bytes(b'original')
            (staging/'new.ics').write_bytes(b'new')
            (staging/'index.json').write_bytes(b'index')
            real=ics.atomic_write
            def fail_index(path,raw):
                if Path(path).name=='index.json':raise OSError('simulated failure after pruning')
                return real(path,raw)
            with patch('src.ics.atomic_write',side_effect=fail_index):
                with self.assertRaises(OSError):publish_staged(staging,output,obsolete=['old.ics'])
            self.assertEqual((output/'old.ics').read_bytes(),b'original')
            self.assertFalse((output/'new.ics').exists())

    def test_pruning_cannot_escape_the_output_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);output=root/'out';staging=root/'stage'
            output.mkdir();staging.mkdir()
            outside=root/'keep.txt';outside.write_text('keep')
            with self.assertRaises(ValueError):publish_staged(staging,output,obsolete=['../keep.txt'])
            self.assertEqual(outside.read_text(),'keep')
