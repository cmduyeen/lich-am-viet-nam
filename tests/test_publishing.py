from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from src.ics import write_calendar, validate_bytes, publish_staged
from src.ics_generator import LunarCalendarGenerator
from src.user_config import CalendarOptions

ROOT=Path(__file__).resolve().parents[1]


class PublishingTests(unittest.TestCase):
    def calendar(self):
        return LunarCalendarGenerator().generate_year(2026,CalendarOptions(country='VN',language='vi',content='festivals'))

    def test_unchanged_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'calendar.ics'
            write_calendar(self.calendar(),path)
            first=path.read_bytes()
            mtime=path.stat().st_mtime_ns
            write_calendar(self.calendar(),path)
            self.assertEqual(path.read_bytes(),first)
            self.assertEqual(path.stat().st_mtime_ns,mtime)

    def test_invalid_revision_timestamp_is_repaired(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'calendar.ics'
            calendar=self.calendar()
            raw=calendar.to_ical().replace(b'DTSTAMP:20261114T000000Z',b'DTSTAMP:2026-11-14 00:00:00+00:00')
            path.write_bytes(raw)
            write_calendar(calendar,path)
            parsed=validate_bytes(path.read_bytes())
            self.assertEqual(len(parsed.walk('VEVENT')),len(calendar.walk('VEVENT')))

    def test_latest_only_build_and_deterministic_zip(self):
        from src.build import build_files
        from src.ics import create_zip
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            stage=folder/'stage'
            stage.mkdir()
            options=CalendarOptions(country='KR',language='ko',content='festivals')
            calendar,files=build_files(options,2026,2027,stage,folder/'out',latest_only=True)
            self.assertEqual(len(files),1)
            self.assertTrue(files[0].name.endswith('_latest.ics'))
            create_zip(files,folder/'a.zip')
            create_zip(files,folder/'b.zip')
            self.assertEqual((folder/'a.zip').read_bytes(),(folder/'b.zip').read_bytes())

    def test_changed_event_keeps_uid_and_advances_only_its_revision(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'calendar.ics'
            original=self.calendar()
            write_calendar(original,path)
            old={str(e['uid']):e.to_ical() for e in original.walk('VEVENT')}
            modified=deepcopy(original)
            target=modified.walk('VEVENT')[0]
            uid=str(target['uid'])
            target['summary']='Đã cập nhật'
            write_calendar(modified,path)
            parsed=validate_bytes(path.read_bytes())
            for event in parsed.walk('VEVENT'):
                if str(event['uid'])==uid:
                    self.assertEqual(int(event['sequence']),1)
                    self.assertEqual(str(event['summary']),'Đã cập nhật')
                else:
                    self.assertEqual(event.to_ical(),old[str(event['uid'])])

    def test_failed_local_publish_rolls_back_previous_output(self):
        import src.ics as ics
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            staging,output=base/'stage',base/'out'
            staging.mkdir(); output.mkdir()
            (staging/'a.ics').write_bytes(b'new-a')
            (staging/'b.ics').write_bytes(b'new-b')
            (output/'a.ics').write_bytes(b'old-a')
            real=ics.atomic_write
            state={'failed':False}
            def fail_once(path,raw):
                if Path(path).name=='b.ics' and not state['failed']:
                    state['failed']=True
                    raise OSError('simulated interrupted write')
                return real(path,raw)
            with patch('src.ics.atomic_write',side_effect=fail_once):
                with self.assertRaises(OSError): publish_staged(staging,output)
            self.assertEqual((output/'a.ics').read_bytes(),b'old-a')
            self.assertFalse((output/'b.ics').exists())

    def test_wire_format_all_locales(self):
        from src.profiles import PROFILES
        for p in PROFILES.values():
            for language in p.languages:
                cal=LunarCalendarGenerator().generate_year(2026,CalendarOptions(country=p.code,tradition=p.tradition,language=language,content='observances'))
                validate_bytes(cal.to_ical())


class CliTests(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(ROOT/'main.py'),*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')

    def test_config_cli_override_all_disables_previous_filter(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            config=folder/'custom.json'
            config.write_text(json.dumps(dict(country='KR',language='ko',content='daily',start_year=2027,end_year=2027,lunar_days=[1],holiday_types=[])),encoding='utf-8')
            result=self.run_cli('--config',config,'--lunar-days','all','--language','en','--output-dir',folder/'output')
            self.assertEqual(result.returncode,0,result.stderr)
            latest,=(folder/'output').glob('*latest.ics')
            self.assertEqual(len(validate_bytes(latest.read_bytes()).walk('VEVENT')),365)

    def test_none_is_not_confused_with_missing_override(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            config=folder/'custom.json'
            config.write_text(json.dumps(dict(country='VN',language='vi',content='daily',lunar_days=[1,15])),encoding='utf-8')
            result=self.run_cli('--config',config,'--year','2026','--lunar-days','none','--holiday-types','none','--output-dir',folder/'out')
            self.assertEqual(result.returncode,0,result.stderr)
            file,=(folder/'out').glob('*.ics')
            self.assertEqual(len(validate_bytes(file.read_bytes()).walk('VEVENT')),0)

    def test_invalid_profile_does_not_touch_output(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            previous=folder/'existing.ics'
            previous.write_bytes(b'keep')
            result=self.run_cli('--country','KR','--year','2051','--output-dir',folder)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(previous.read_bytes(),b'keep')
            self.assertEqual(len(list(folder.iterdir())),1)

    def test_list_only_implemented_profiles(self):
        result=self.run_cli('--list-countries')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('KR | korean',result.stdout)
        self.assertNotIn('JP |',result.stdout)
