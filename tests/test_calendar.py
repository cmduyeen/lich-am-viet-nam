import subprocess
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.ics import validate_bytes
from src.ics_generator import LunarCalendarGenerator, _build_event_for_day
from src.lunar_converter import to_lunar
from main import create_zip_archive
from src.calendar_options import HOLIDAYS, load_custom_holidays


class CalendarTests(unittest.TestCase):
    def test_languages_have_same_dates_and_english_text(self):
        vi = LunarCalendarGenerator().generate_year(2026).walk('VEVENT')
        en = LunarCalendarGenerator('en').generate_year(2026).walk('VEVENT')
        self.assertEqual([e.decoded('dtstart') for e in vi], [e.decoded('dtstart') for e in en])
        self.assertEqual(len(en), 365)
        self.assertEqual(len({str(e['uid']) for e in en + vi}), 730)
        tet = next(e for e in en if e.decoded('dtstart') == date(2026, 2, 17))
        self.assertEqual(str(tet['summary']), '1/1 • Lunar New Year — Day 1')
        self.assertIn('Lunar day 1, month 1, year 2026', str(tet['description']))
        self.assertEqual(tet['summary'].params['LANGUAGE'], 'en')
        for rule in HOLIDAYS.values():
            self.assertTrue(rule.name_vi and rule.name_en and rule.description_en)

    def test_selection_keeps_every_day_and_only_selected_holidays(self):
        events = LunarCalendarGenerator('en', 'mid-autumn').generate_year(2026).walk('VEVENT')
        self.assertEqual(len(events), 365)
        titles = [str(e['summary']) for e in events]
        self.assertEqual(sum('Mid-Autumn Festival' in title for title in titles), 1)
        self.assertFalse(any('Lunar New Year' in title for title in titles))
        none = LunarCalendarGenerator('en', 'none').generate_year(2026).walk('VEVENT')
        self.assertEqual(str(none[0]['summary']), '13/11')

    def test_personal_dates_and_collisions_share_one_event(self):
        custom = load_custom_holidays(Path('examples/holidays.json'))
        events = LunarCalendarGenerator('en', 'none', custom).generate_year(2026).walk('VEVENT')
        birthday = next(e for e in events if e.decoded('dtstart') == date(2026, 6, 15))
        self.assertIn('Birthday', str(birthday['summary']))
        self.assertTrue(any('Family memorial day' in str(e['summary']) for e in events))
        # National Day and Vu Lan fall on the same date in 2058.
        events = LunarCalendarGenerator('en').generate_year(2058).walk('VEVENT')
        collision = next(e for e in events if e.decoded('dtstart') == date(2058, 9, 2))
        self.assertIn("National Day", str(collision['summary']))
        self.assertIn("Vu Lan", str(collision['summary']))

    def test_custom_cli_isolated_from_public_feeds_and_rejects_bad_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            latest = Path(folder) / 'viet_lunar_latest.ics'
            latest.write_bytes(b'existing')
            args = [sys.executable, 'main.py', '--language', 'en', '--start', '2026',
                    '--end', '2026', '--output-dir', folder, '--holidays']
            result = subprocess.run(args + ['mid-autumn'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            custom = Path(folder) / 'viet_lunar_custom_en_latest.ics'
            self.assertEqual(len(validate_bytes(custom.read_bytes()).walk('VEVENT')), 365)
            before = custom.read_bytes()
            bad = subprocess.run(args + ['typo'], capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(custom.read_bytes(), before)
            self.assertEqual(latest.read_bytes(), b'existing')

    def test_invalid_personal_dates_are_rejected(self):
        valid = {'calendar': 'lunar', 'month': 3, 'day': 12,
                 'name': {'vi': 'Ngày riêng', 'en': 'Personal date'}}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'holidays.json'
            for changes in ({'calendar': 'unknown'}, {'month': 13}, {'day': 31},
                            {'day': True}, {'name': {'vi': 'Thiếu tiếng Anh'}},
                            {'calendar': 'solar', 'month': 2, 'day': 30}):
                with self.subTest(changes=changes):
                    path.write_text(json.dumps([{**valid, **changes}]), encoding='utf-8')
                    with self.assertRaises(ValueError):
                        load_custom_holidays(path)

    def test_vietnamese_new_year_boundaries(self):
        for year, month, day in [(1968, 1, 29), (1985, 1, 21), (2007, 2, 17), (2026, 2, 17)]:
            lunar = to_lunar(date(year, month, day))
            self.assertEqual((lunar.lunar_year, lunar.lunar_month, lunar.lunar_day), (year, 1, 1))

    def test_leap_month_does_not_repeat_festival(self):
        from datetime import datetime, timezone
        lunar = to_lunar(date(2020, 6, 6))
        self.assertEqual((lunar.lunar_month, lunar.lunar_day), (-4, 15))
        event = _build_event_for_day(lunar.solar_date, lunar, datetime.now(timezone.utc))
        self.assertIn('nhuận', str(event['summary']))
        self.assertNotIn('Phật Đản', str(event['summary']))

    def test_wire_compatibility_and_stable_revisions(self):
        generator = LunarCalendarGenerator()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'calendar.ics'
            generator.save(generator.generate_year(2026), path)
            first = path.read_bytes()
            parsed = validate_bytes(first)
            events = parsed.walk('VEVENT')
            self.assertEqual(len(events), 365)
            self.assertEqual(str(events[0]['uid']), 'vnlunar-20260101@cmduyeen')
            generator.save(generator.generate_year(2026), path)
            self.assertEqual(path.read_bytes(), first)
            changed = generator.generate_year(2026)
            changed.walk('VEVENT')[0]['SUMMARY'] = 'Updated'
            generator.save(changed, path)
            event = validate_bytes(path.read_bytes()).walk('VEVENT')[0]
            self.assertEqual(str(event['uid']), str(events[0]['uid']))
            self.assertEqual(int(event['sequence']), 1)
            archive = Path(folder) / 'calendar.zip'
            create_zip_archive([path], archive)
            first_zip = archive.read_bytes()
            create_zip_archive([path], archive)
            self.assertEqual(archive.read_bytes(), first_zip)

    def test_invalid_range_keeps_existing_subscription(self):
        with tempfile.TemporaryDirectory() as folder:
            latest = Path(folder) / 'viet_lunar_latest.ics'
            latest.write_bytes(b'existing')
            result = subprocess.run(
                [sys.executable, 'main.py', '--start', '2100', '--output-dir', folder],
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(latest.read_bytes(), b'existing')


if __name__ == '__main__':
    unittest.main()
