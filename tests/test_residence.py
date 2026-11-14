"""Residence is independent of calendar rules, host timezone and display language."""
from dataclasses import replace
from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from src.engines import ENGINES
from src.ics import validate_bytes, write_calendar
from src.ics_generator import LunarCalendarGenerator
from src.localization import validate_translations, LOCALES
from src.naming import output_prefix
from src.profiles import PROFILES, RESIDENCES, residence_languages
from src.user_config import CalendarOptions

ROOT=Path(__file__).resolve().parents[1]


class ResidenceTests(unittest.TestCase):
    def setUp(self): self.generator=LunarCalendarGenerator()

    def signature(self, calendar):
        return {(e.decoded('dtstart'),e.decoded('dtend'),str(e['x-lunar-event-id'])) for e in calendar.walk('VEVENT')}

    def test_country_alias_and_explicit_residence_are_equivalent(self):
        for tradition,source in RESIDENCES['US'].traditions:
            alias=CalendarOptions(country='US',tradition=tradition)
            explicit=CalendarOptions(country=source,residence='US')
            self.assertEqual(alias,explicit)
            self.assertFalse(alias.legacy)
            self.assertEqual(alias.content,'festivals')
            self.assertEqual(alias.language,'en')
            self.assertEqual(output_prefix(alias),f'lunar_us_{tradition}_en_festivals')
            self.assertEqual(CalendarOptions.from_mapping(alias.to_dict()),alias)
            settings=CalendarOptions.from_mapping({'country':'US','tradition':tradition,'start_year':2027,'end_year':2027})
            self.assertEqual(output_prefix(settings),output_prefix(replace(explicit,start_year=2027,end_year=2027)))

    def test_us_requires_a_supported_tradition(self):
        for kwargs in ({'country':'US'}, {'country':'US','tradition':'islamic'},
                       {'country':'US','tradition':'vietnamese','residence':'CA'},
                       {'country':'VN','residence':'CA'},
                       {'country':'TW','residence':'US'},
                       {'country':'US','tradition':'korean','language':'vi'},
                       {'country':'US','tradition':'chinese','minimal':True}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                CalendarOptions(**kwargs)

    def test_every_us_locale_preserves_source_dates_and_identities(self):
        validate_translations()
        for tradition,source in RESIDENCES['US'].traditions:
            profile=PROFILES[source]
            home=self.generator.generate_year(2027,CalendarOptions(country=source,language='en',content='festivals'))
            expected=self.signature(home)
            ids=None
            for language in residence_languages('US',profile):
                options=CalendarOptions(country='US',tradition=tradition,language=language)
                calendar=self.generator.generate_year(2027,options)
                self.assertEqual(self.signature(calendar),expected)
                self.assertIn(LOCALES[language]['country_names']['US'],str(calendar['x-wr-calname']))
                self.assertNotIn('x-wr-timezone',calendar)
                actual={str(e['uid']) for e in calendar.walk('VEVENT')}
                if ids is None: ids=actual
                self.assertEqual(actual,ids)
                self.assertTrue(actual.isdisjoint({str(e['uid']) for e in home.walk('VEVENT')}))
                for event in calendar.walk('VEVENT'):
                    self.assertEqual(str(event['x-residence']),'US')
                    self.assertEqual(str(event['x-countries']),source)
                    self.assertIn(LOCALES[language]['residence_note'],str(event['description']))
                validate_bytes(calendar.to_ical())

    def test_calendar_divergences_are_preserved_for_us_communities(self):
        expected={('vietnamese',2030):date(2030,2,2),('chinese',2030):date(2030,2,3),
                  ('chinese',2027):date(2027,2,6),('korean',2027):date(2027,2,7)}
        for (tradition,year),day in expected.items():
            calendar=self.generator.generate_year(year,CalendarOptions(country='US',tradition=tradition))
            events=[e for e in calendar.walk('VEVENT') if str(e['x-lunar-event-id'])=='lunar_new_year']
            self.assertEqual([e.decoded('dtstart') for e in events],[day])

    def test_host_timezone_and_dst_do_not_move_all_day_dates(self):
        options=CalendarOptions(country='US',tradition='vietnamese',content='daily')
        reference=self.generator.generate_year(2027,options).to_ical()
        from unittest.mock import patch
        for timezone in ('America/New_York','America/Los_Angeles','Pacific/Honolulu'):
            with patch.dict(os.environ,{'TZ':timezone}):
                self.assertEqual(self.generator.generate_year(2027,options).to_ical(),reference)
        events={e.decoded('dtstart') for e in validate_bytes(reference).walk('VEVENT')}
        self.assertIn(date(2027,3,14),events)
        self.assertIn(date(2027,11,7),events)
        self.assertEqual(len(events),365)

    def test_residence_reuses_cached_conversion(self):
        home=CalendarOptions(country='KR',language='en',content='daily')
        self.generator.generate_year(2028,home)
        before=ENGINES['korean'].cache_info().misses
        self.generator.generate_year(2028,CalendarOptions(country='US',tradition='korean',language='ko',content='daily'))
        self.assertEqual(ENGINES['korean'].cache_info().misses,before)

    def test_merged_residence_remains_semantic_and_order_independent(self):
        options=CalendarOptions(countries=('VN','CN','KR'),residence='US',language='en',content='festivals')
        first=self.generator.generate_year(2030,options)
        second=self.generator.generate_year(2030,replace(options,countries=('KR','CN','VN')))
        self.assertEqual(first.to_ical(),second.to_ical())
        new_years=[e for e in first.walk('VEVENT') if str(e['x-lunar-event-id'])=='lunar_new_year']
        self.assertIn(date(2030,2,2),{e.decoded('dtstart') for e in new_years})
        self.assertIn(date(2030,2,3),{e.decoded('dtstart') for e in new_years})
        self.assertEqual(output_prefix(options),'lunar_us-cn-kr-vn_merged_en_festivals')
        validate_bytes(first.to_ical())

    def test_us_feed_regeneration_is_stable(self):
        options=CalendarOptions(country='US',tradition='chinese',language='zh-Hant')
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'feed.ics'
            write_calendar(self.generator.generate_year(2027,options),path)
            initial=path.read_bytes()
            write_calendar(self.generator.generate_year(2027,options),path)
            self.assertEqual(path.read_bytes(),initial)

    def test_json_cli_generates_a_custom_us_subscription(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            config=folder/'us.json'
            config.write_text(json.dumps({'country':'US','tradition':'korean','language':'ko','start_year':2027,'end_year':2027}),encoding='utf-8')
            result=subprocess.run([sys.executable,str(ROOT/'main.py'),'--config',str(config),'--output-dir',str(folder/'out')],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            latest,=(folder/'out').glob('*latest.ics')
            calendar=validate_bytes(latest.read_bytes())
            self.assertEqual(str(calendar['x-residence']),'US')
            self.assertIn('lunar_us_korean_ko_festivals_custom_',latest.name)

    def test_invalid_cli_never_creates_an_output_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'out'
            result=subprocess.run([sys.executable,str(ROOT/'main.py'),'--country','US','--output-dir',str(target)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('--tradition',result.stderr)
            self.assertFalse(target.exists())
