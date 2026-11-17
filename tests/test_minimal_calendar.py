import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from icalendar import Calendar
from main import cleanup_past_files
from src.ics_generator import LunarCalendarGenerator
from src.lunar_converter import to_lunar
from src.user_config import CalendarOptions

ROOT = Path(__file__).resolve().parents[1]


class MinimalCalendarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calendars = {
            language: LunarCalendarGenerator().generate_range(2026, 2036, CalendarOptions(language=language, minimal=True))
            for language in ('vi', 'en')
        }

    def test_selection_titles_boundaries_and_leap_months(self):
        expected = set()
        current = date(2026, 1, 1)
        while current <= date(2036, 12, 31):
            lunar = to_lunar(current)
            if lunar.lunar_day == 15 or (lunar.lunar_day == 1 and lunar.lunar_month_abs == 1 and not lunar.is_leap_month):
                expected.add(current)
            current += timedelta(days=1)
        for language, calendar in self.calendars.items():
            events = calendar.walk('VEVENT')
            self.assertEqual(len(events), 148)
            self.assertEqual({e.decoded('dtstart') for e in events}, expected)
            full_moons = leap_moons = new_years = 0
            for event in events:
                start = event.decoded('dtstart')
                lunar = to_lunar(start)
                self.assertIs(type(start), date)
                self.assertEqual(event.decoded('dtend'), start + timedelta(days=1))
                self.assertIn('-minimal-', str(event['uid']))
                if lunar.lunar_day == 15:
                    full_moons += 1
                    leap_moons += lunar.is_leap_month
                    self.assertEqual(str(event['summary']), 'Rằm' if language == 'vi' else 'Full Moon')
                    if lunar.is_leap_month:
                        self.assertIn('nhuận' if language == 'vi' else 'leap', str(event['description']))
                else:
                    new_years += 1
                    self.assertEqual(str(event['summary']), 'Tết Nguyên Đán' if language == 'vi' else 'Lunar New Year')
                    self.assertEqual(str(event['x-lunar-color']), '#E53935')
            self.assertEqual((full_moons, leap_moons, new_years), (137, 4, 11))

    def test_wire_format_and_round_trip(self):
        for calendar in self.calendars.values():
            raw = calendar.to_ical()
            self.assertNotIn(b'\n', raw.replace(b'\r\n', b''))
            self.assertTrue(all(len(line) <= 75 for line in raw.split(b'\r\n')))
            self.assertEqual(len(Calendar.from_ical(raw).walk('VEVENT')), 148)

    def test_modes_have_distinct_stable_uids(self):
        gen = LunarCalendarGenerator()
        uid_sets = []
        for language in ('vi', 'en'):
            for minimal in (False, True):
                options = CalendarOptions(language=language, minimal=minimal)
                cal = gen.generate_year(2026, options)
                ids = {str(e['uid']) for e in cal.walk('VEVENT')}
                self.assertEqual(ids, {str(e['uid']) for e in gen.generate_year(2026, options).walk('VEVENT')})
                for previous in uid_sets:
                    self.assertTrue(ids.isdisjoint(previous))
                uid_sets.append(ids)

    def test_minimal_overrides_content_filters(self):
        cal = LunarCalendarGenerator().generate_year(2026, CalendarOptions(minimal=True, lunar_days=frozenset(), holiday_types=frozenset()))
        self.assertEqual(len(cal.walk('VEVENT')), 14)

    def test_cleanup_is_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            names = ['viet_lunar_2025.ics', 'viet_lunar_en_2025.ics', 'viet_lunar_minimal_2025.ics', 'viet_lunar_minimal_yearly_2025_2035.zip', 'viet_lunar_minimal_latest.ics']
            for name in names:
                (folder / name).touch()
            removed = cleanup_past_files(folder, 2026, 'viet_lunar_minimal')
            self.assertEqual(set(removed), set(names[2:4]))
            self.assertTrue(all((folder / name).exists() for name in (names[0], names[1], names[4])))

    def test_json_validates_minimal(self):
        self.assertTrue(CalendarOptions.from_mapping({'minimal': True}).minimal)
        with self.assertRaises(ValueError):
            CalendarOptions.from_mapping({'minimal': 'false'})

    def test_cli_split_and_zip(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(ROOT / 'main.py'), '--minimal', '--split', '--output-dir', tmp], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            folder = Path(tmp)
            latest = folder / 'viet_lunar_minimal_latest.ics'
            self.assertTrue(latest.exists())
            archive, = folder.glob('*.zip')
            with zipfile.ZipFile(archive) as z:
                self.assertEqual(len(z.namelist()), 2)
                for name in z.namelist():
                    self.assertEqual(z.read(name), (folder / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
