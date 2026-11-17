import json
from datetime import date
from pathlib import Path
import re
import unittest
from src.engines import ENGINES, chinese, korean, vietnamese
from src.user_config import CalendarOptions
from src.ics_generator import LunarCalendarGenerator

FIXTURES=Path(__file__).parent/'fixtures'


class ReferenceDateTests(unittest.TestCase):
    def test_independently_recorded_dates(self):
        for item in json.loads((FIXTURES/'reference_dates.json').read_text(encoding='utf-8')):
            with self.subTest(item=item):
                actual=ENGINES[item['engine']](date.fromisoformat(item['solar']))
                self.assertEqual([actual.year,actual.month,actual.day,actual.leap],item['lunar'])
                self.assertTrue(item['source'].startswith('https://'))

    def test_hko_complete_reference_tables(self):
        checked=0
        previous=None
        for path in sorted(FIXTURES.glob('hko-*.txt')):
            rows=[]
            for line in path.read_text(encoding='utf-8-sig').splitlines():
                match=re.match(r'^(\d{4})/(\d{1,2})/(\d{1,2})\s+(.+?)\s{2,}',line)
                if match:
                    y,m,d,label=match.groups()
                    rows.append((date(int(y),int(m),int(d)),label.strip()))
            first_marker=next(int(re.match(r'(\d+)',label).group()) for _,label in rows if 'Lunar Month' in label)
            month=(first_marker-2)%12+1
            year=rows[0][0].year-1
            leap=False
            if previous and previous[0].toordinal()+1==rows[0][0].toordinal():
                _,year,month,leap=previous
            for solar,label in rows:
                if 'Lunar Month' in label:
                    following=int(re.match(r'(\d+)',label).group())
                    leap=following==month
                    month=following
                    day=1
                    if month==1 and not leap: year=solar.year
                else: day=int(label)
                actual=chinese(solar)
                self.assertEqual((actual.year,actual.month,actual.day,actual.leap),(year,month,day,leap),(path.name,solar))
                checked+=1
                previous=(solar,year,month,leap)
        self.assertEqual(checked,1825)

    def test_three_engines_do_not_substitute_for_each_other(self):
        self.assertEqual(vietnamese(date(2030,2,2)).day,1)
        self.assertEqual(chinese(date(2030,2,2)).day,30)
        self.assertEqual(chinese(date(2027,2,6)).day,1)
        self.assertEqual(korean(date(2027,2,6)).day,30)
        self.assertEqual(korean(date(2027,2,7)).day,1)

    def test_vietnamese_months_are_continuous_29_or_30_days(self):
        from datetime import timedelta
        first,last=date(2026,1,1),date(2036,12,31)
        previous=vietnamese(first)
        for offset in range(1,(last-first).days+1):
            current=vietnamese(first+timedelta(days=offset))
            if current.day==1:
                self.assertIn(previous.day,(29,30))
            else:
                self.assertEqual(current.day,previous.day+1)
                self.assertEqual((current.year,current.month,current.leap),(previous.year,previous.month,previous.leap))
            previous=current

    def test_year_bounds_are_enforced_by_public_api(self):
        generator=LunarCalendarGenerator()
        for code,year in [('KR',2051),('VN',2100),('CN',1900)]:
            with self.assertRaises(ValueError):
                generator.generate_year(year,CalendarOptions(country=code,language='en',content='festivals'))

    def test_second_language_reuses_engine_results(self):
        generator=LunarCalendarGenerator()
        generator.generate_year(2028,CalendarOptions(country='CN',language='en',content='daily'))
        before=chinese.cache_info().misses
        generator.generate_year(2028,CalendarOptions(country='CN',language='zh-Hans',content='daily'))
        self.assertEqual(chinese.cache_info().misses,before)
