from dataclasses import replace
from datetime import date
import unittest
from src.ics_generator import LunarCalendarGenerator
from src.profiles import PROFILES, get_profile
from src.user_config import CalendarOptions
from src.localization import validate_translations, LOCALES, title


class ProfilePipelineTests(unittest.TestCase):
    def setUp(self): self.gen=LunarCalendarGenerator()

    def test_all_profile_languages_have_same_semantics_and_uids(self):
        validate_translations()
        for profile in PROFILES.values():
            expected=None
            for language in profile.languages:
                options=CalendarOptions(country=profile.code,tradition=profile.tradition,language=language,content='festivals')
                calendar=self.gen.generate_year(2026,options)
                actual={(e.decoded('dtstart'),str(e['x-lunar-event-id']),str(e['uid'])) for e in calendar.walk('VEVENT')}
                if expected is None: expected=actual
                self.assertEqual(actual,expected,profile.code)
                self.assertIn(LOCALES[language]['calendar'],str(calendar['x-wr-calname']))
                for event in calendar.walk('VEVENT'):
                    self.assertIn(LOCALES[language]['notice'],str(event['description']))
                    self.assertEqual(event.decoded('dtend').toordinal(),event.decoded('dtstart').toordinal()+1)

    def test_new_default_differs_from_legacy_without_replacing_it(self):
        self.assertTrue(CalendarOptions().legacy)
        new=CalendarOptions.from_mapping({'country':'VN'})
        self.assertEqual(new.content,'festivals')
        events=self.gen.generate_year(2026,new).walk('VEVENT')
        self.assertLess(len(events),30)
        self.assertNotIn(date(2026,1,1),{e.decoded('dtstart') for e in events})
        self.assertTrue(all(str(e['x-event-category'])=='lunar' for e in events))

    def test_multi_tradition_profiles_are_explicit(self):
        for code in ('SG','MY'):
            with self.assertRaisesRegex(ValueError,'tradition chinese'):
                CalendarOptions(country=code,language='en')
            self.assertEqual(CalendarOptions(country=code,tradition='chinese',language='en').content,'festivals')

    def test_unsupported_profiles_and_languages_fail(self):
        with self.assertRaises(ValueError): get_profile('JP')
        with self.assertRaises(ValueError): CalendarOptions(country='KR',language='zh-Hans')
        with self.assertRaises(ValueError): CalendarOptions(countries=('CN','KR'),language='native')
        with self.assertRaises(ValueError): CalendarOptions(content='festivals',minimal=True)

    def test_native_alias_is_deterministic(self):
        self.assertEqual(CalendarOptions(country='TW',language='native').language,'zh-Hant')
        self.assertEqual(CalendarOptions(country='KR',language='native').language,'ko')

    def test_merge_is_semantic_and_country_order_independent(self):
        options=CalendarOptions(countries=('VN','CN','KR'),language='en',content='festivals')
        first=self.gen.generate_year(2026,options)
        second=self.gen.generate_year(2026,replace(options,countries=('KR','VN','CN')))
        self.assertEqual(first.to_ical(),second.to_ical())
        events=first.walk('VEVENT')
        new_year=[e for e in events if str(e['x-lunar-event-id'])=='lunar_new_year']
        self.assertEqual(len(new_year),1)
        self.assertEqual(str(new_year[0]['x-countries']),'CN,KR,VN')
        mid=[e for e in events if e.decoded('dtstart')==date(2026,9,25)]
        ids={str(e['x-lunar-event-id']) for e in mid}
        self.assertIn('chuseok',ids)
        self.assertIn('mid_autumn',ids)
        changed=self.gen.generate_year(2030,options)
        days={e.decoded('dtstart') for e in changed.walk('VEVENT') if str(e['x-lunar-event-id'])=='lunar_new_year'}
        self.assertIn(date(2030,2,2),days)
        self.assertIn(date(2030,2,3),days)

    def test_leap_months_do_not_repeat_festivals(self):
        options=CalendarOptions(country='KR',language='en',content='festivals')
        calendar=self.gen.generate_year(2017,options)
        self.assertNotIn(date(2017,6,28),{e.decoded('dtstart') for e in calendar.walk('VEVENT') if str(e['x-lunar-event-id'])=='dano'})

    def test_filters_are_independent_and_can_be_disabled(self):
        options=CalendarOptions(country='CN',language='en',content='daily',lunar_days=frozenset(),holiday_types=frozenset())
        self.assertEqual(len(self.gen.generate_year(2026,options).walk('VEVENT')),0)
        options=replace(options,lunar_days=frozenset({15}))
        self.assertIn(len(self.gen.generate_year(2026,options).walk('VEVENT')),(12,13))

    def test_solar_terms_are_opt_in_and_not_misclassified(self):
        base=CalendarOptions(country='CN',language='en',content='festivals')
        self.assertNotIn('qingming',{str(e['x-lunar-event-id']) for e in self.gen.generate_year(2026,base).walk('VEVENT')})
        all_types=replace(base,holiday_types=frozenset({'solar','lunar'}))
        event=next(e for e in self.gen.generate_year(2026,all_types).walk('VEVENT') if str(e['x-lunar-event-id'])=='qingming')
        self.assertEqual(str(event['x-event-category']),'solar_term')

    def test_local_names_do_not_change_shared_identity(self):
        self.assertNotEqual(title('TW','zh-Hant','lunar_new_year'),title('HK','zh-Hant','lunar_new_year'))
        self.assertEqual(set(PROFILES),{'VN','CN','TW','HK','MO','KR','SG','MY'})

    def test_corrected_festival_date_retains_occurrence_uid(self):
        from unittest.mock import patch
        from src.pipeline import Occurrence, generate
        from src.models import LunarDay
        options=CalendarOptions(country='VN',language='en',content='festivals')
        lunar=LunarDay(date(2026,2,17),2026,1,1)
        item=Occurrence('VN','lunar_new_year',lunar,'lunar')
        with patch('src.pipeline.occurrences',return_value={(date(2026,2,17),'lunar_new_year'):[item]}):
            first=generate(2026,2026,options).walk('VEVENT')[0]
        with patch('src.pipeline.occurrences',return_value={(date(2026,2,18),'lunar_new_year'):[item]}):
            corrected=generate(2026,2026,options).walk('VEVENT')[0]
        self.assertEqual(first['uid'],corrected['uid'])
        self.assertNotEqual(first.decoded('dtstart'),corrected.decoded('dtstart'))

    def test_configuration_round_trip(self):
        for options in (CalendarOptions(),CalendarOptions(countries=('VN','CN'),language='en',content='observances')):
            self.assertEqual(CalendarOptions.from_mapping(options.to_dict()),options)

    def test_merged_profiles_keep_their_own_traditions(self):
        options=CalendarOptions(countries=('VN','CN','SG','MY','KR'),language='en',content='festivals')
        events=self.gen.generate_year(2026,options).walk('VEVENT')
        event=next(e for e in events if str(e['x-lunar-event-id'])=='lunar_new_year')
        self.assertEqual(str(event['x-countries']),'CN,KR,MY,SG,VN')
        self.assertEqual(len({str(e['uid']) for e in events}),len(events))
