import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.ics import validate_bytes
from src.ics_generator import LunarCalendarGenerator, _build_event_for_day
from src.lunar_converter import to_lunar
from main import create_zip_archive


class CalendarTests(unittest.TestCase):
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
