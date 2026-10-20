import contextlib
from dataclasses import replace
from datetime import date, timedelta
import io
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from icalendar import Calendar

from main import cleanup_past_files, main
from src.config import (
    CALENDAR_DESCRIPTION_EN, CALENDAR_NAME_EN, EARTHLY_BRANCHES_EN,
    HEAVENLY_STEMS_EN, PRODID_EN,
    MINIMAL_CALENDAR_DESCRIPTION_EN, MINIMAL_CALENDAR_NAME_EN,
    MINIMAL_CALENDAR_DESCRIPTION, MINIMAL_CALENDAR_NAME, FULL_MOON_NOTE, PRODID,
)
from src.holidays import FIXED_LUNAR_HOLIDAYS, FIXED_SOLAR_HOLIDAYS, GIAO_THUA, HolidayInfo
from src.ics_generator import LunarCalendarGenerator, _build_event_for_day
from src.lunar_converter import DIA_CHI, THIEN_CAN, to_lunar


ROOT = Path(__file__).resolve().parents[1]


def without_timestamps(calendar):
    result = Calendar.from_ical(calendar.to_ical())
    for event in result.walk('VEVENT'):
        del event['DTSTAMP']
    return result.to_ical()


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.solar = date(2026, 1, 2)
        self.lunar = to_lunar(self.solar)

    def test_every_holiday_has_english_event_text(self):
        for (month, day), holiday in FIXED_LUNAR_HOLIDAYS.items():
            with self.subTest(holiday=holiday.name_en):
                lunar = replace(self.lunar, lunar_month=month, lunar_day=day)
                self.assert_holiday(self.solar, lunar, holiday)
        for (month, day), holiday in FIXED_SOLAR_HOLIDAYS.items():
            with self.subTest(holiday=holiday.name_en):
                self.assert_holiday(date(2026, month, day), self.lunar, holiday)

    def assert_holiday(self, solar, lunar, holiday):
        with patch('src.ics_generator.is_last_day_of_lunar_month', return_value=False):
            event = _build_event_for_day(solar, lunar, 'en')
        self.assertTrue(str(event['SUMMARY']).endswith(holiday.name_en))
        self.assertIn(f'{holiday.name_en}: {holiday.description_en}', str(event['DESCRIPTION']))
        self.assertTrue(holiday.name_en.isascii())
        self.assertTrue(holiday.description_en.isascii())
        self.assertEqual('X-MICROSOFT-CDO-IMPORTANCE' in event, holiday.is_public_holiday)

    def test_actual_lunar_new_year_and_eve(self):
        for solar, holiday in (
            (date(2026, 2, 16), GIAO_THUA),
            (date(2026, 2, 17), FIXED_LUNAR_HOLIDAYS[(1, 1)]),
        ):
            with self.subTest(date=solar):
                event = _build_event_for_day(solar, to_lunar(solar), 'en')
                self.assertTrue(str(event['SUMMARY']).endswith(holiday.name_en))
                self.assertIn(holiday.description_en, str(event['DESCRIPTION']))

    def test_ordinary_first_and_full_moon_days(self):
        for day, label in ((7, ''), (1, 'First Day of Lunar Month'), (15, 'Full Moon')):
            with self.subTest(day=day):
                lunar = replace(self.lunar, lunar_month=6, lunar_day=day)
                event = _build_event_for_day(self.solar, lunar, 'en')
                expected = f'Lunar {day}/6' + (f' \u2022 {label}' if label else '')
                self.assertEqual(str(event['SUMMARY']), expected)
                self.assertEqual(str(event['DESCRIPTION']), f'Lunar day {day}, month 6 (Yin Wood Snake year)')

    def test_actual_leap_month_markers(self):
        solar = date(2025, 7, 25)
        lunar = to_lunar(solar)
        self.assertTrue(lunar.is_leap_month)
        self.assertEqual(lunar.lunar_month, -6)
        event = _build_event_for_day(solar, lunar, 'en')
        self.assertEqual(str(event['SUMMARY']), 'Lunar 1/6 (leap month) \u2022 First Day of Lunar Month')
        self.assertIn('leap month 6', str(event['DESCRIPTION']))
        self.assertNotIn('(leap month)', str(_build_event_for_day(solar, lunar)['SUMMARY']))

    def test_year_translation_covers_all_stems_and_branches(self):
        self.assertEqual(set(HEAVENLY_STEMS_EN), set(THIEN_CAN.values()))
        self.assertEqual(set(EARTHLY_BRANCHES_EN), set(DIA_CHI.values()))
        for stem, stem_en in HEAVENLY_STEMS_EN.items():
            for branch, branch_en in EARTHLY_BRANCHES_EN.items():
                lunar = replace(self.lunar, can_chi_year=f'{stem} {branch}')
                event = _build_event_for_day(self.solar, lunar, 'en')
                self.assertIn(f'{stem_en} {branch_en} year', str(event['DESCRIPTION']))
        self.assertIn('Cat', EARTHLY_BRANCHES_EN.values())
        self.assertIn('Buffalo', EARTHLY_BRANCHES_EN.values())

    def test_missing_translation_fails_instead_of_publishing_partial_english(self):
        untranslated = {(self.lunar.lunar_month_abs, self.lunar.lunar_day): HolidayInfo('Untranslated')}
        with patch.dict(FIXED_LUNAR_HOLIDAYS, untranslated), \
                patch('src.ics_generator.to_lunar', return_value=self.lunar):
            with self.assertRaisesRegex(RuntimeError, 'Failed to generate English event'):
                LunarCalendarGenerator('en').generate_year(2026)

    def test_invalid_language_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported calendar language'):
            LunarCalendarGenerator('fr')


class FeedRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved_vi = Calendar.from_ical((ROOT / 'output' / 'viet_lunar_latest.ics').read_bytes())
        saved_events = cls.saved_vi.walk('VEVENT')
        cls.start = saved_events[0].decoded('DTSTART')
        cls.end = saved_events[-1].decoded('DTSTART')
        cls.vi = LunarCalendarGenerator().generate_range(cls.start.year, cls.end.year)
        cls.en = LunarCalendarGenerator('en').generate_range(cls.start.year, cls.end.year)

    def test_existing_vietnamese_feed_is_unchanged_except_timestamps(self):
        self.assertEqual(without_timestamps(self.vi), without_timestamps(self.saved_vi))

    def test_dates_styles_and_stable_separate_identifiers(self):
        vi_events = self.vi.walk('VEVENT')
        en_events = self.en.walk('VEVENT')
        self.assertEqual(len(en_events), (self.end - self.start).days + 1)
        self.assertEqual(len(vi_events), len(en_events))
        self.assertEqual(len({str(event['UID']) for event in en_events}), len(en_events))
        for offset, (vi, en) in enumerate(zip(vi_events, en_events)):
            solar = self.start + timedelta(days=offset)
            with self.subTest(date=solar):
                self.assertEqual(en.decoded('DTSTART'), solar)
                self.assertEqual(en.decoded('DTEND'), solar + timedelta(days=1))
                self.assertEqual(str(en['UID']), f'vnlunar-en-{solar:%Y%m%d}@cmduyeen')
                self.assertNotEqual(vi['UID'], en['UID'])
                for key in ('DTSTART', 'DTEND', 'COLOR', 'X-MICROSOFT-CDO-IMPORTANCE'):
                    self.assertEqual(vi.get(key), en.get(key))
                self.assertTrue(str(en['SUMMARY']).startswith('Lunar '))
                self.assertTrue(str(en['SUMMARY']).replace('\u2022', '').isascii())
                self.assertTrue(str(en['DESCRIPTION']).isascii())

    def test_english_metadata_and_published_artifacts(self):
        self.assertEqual(str(self.en['PRODID']), PRODID_EN)
        self.assertEqual(str(self.en['X-WR-CALDESC']), CALENDAR_DESCRIPTION_EN)
        self.assertEqual(str(self.en['X-WR-CALNAME']), f'{CALENDAR_NAME_EN} {self.start.year}\u2013{self.end.year}')
        output = ROOT / 'output'
        latest = (output / 'viet_lunar_en_latest.ics').read_bytes()
        combined = output / f'viet_lunar_en_{self.start.year}_{self.end.year}.ics'
        self.assertEqual(latest, combined.read_bytes())
        self.assertEqual(without_timestamps(Calendar.from_ical(latest)), without_timestamps(self.en))
        archive = output / f'viet_lunar_en_yearly_{self.start.year}_{self.end.year}.zip'
        with zipfile.ZipFile(archive) as zipped:
            expected_names = [f'viet_lunar_en_{year}.ics' for year in range(self.start.year, self.end.year + 1)]
            self.assertEqual(zipped.namelist(), expected_names)
            for year, name in zip(range(self.start.year, self.end.year + 1), expected_names):
                yearly = (output / name).read_bytes()
                self.assertEqual(zipped.read(name), yearly)
                calendar = Calendar.from_ical(yearly)
                self.assertEqual(str(calendar['X-WR-CALNAME']), f'{CALENDAR_NAME_EN} {year}')
                expected = [event for event in self.en.walk('VEVENT') if event.decoded('DTSTART').year == year]
                actual = calendar.walk('VEVENT')
                self.assertEqual(len(actual), len(expected))
                for saved, generated in zip(actual, expected):
                    for key in ('SUMMARY', 'DESCRIPTION', 'DTSTART', 'DTEND', 'UID', 'COLOR'):
                        self.assertEqual(saved[key], generated[key])

    def test_english_icalendar_wire_format(self):
        for path in (ROOT / 'output').glob('viet_lunar_en_*.ics'):
            with self.subTest(file=path.name):
                raw = path.read_bytes()
                self.assertTrue(raw.endswith(b'\r\n'))
                self.assertNotIn(b'\n', raw.replace(b'\r\n', b''))
                self.assertTrue(all(len(line) <= 75 for line in raw.split(b'\r\n')))


class MinimalFeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = Calendar.from_ical((ROOT / 'output' / 'viet_lunar_en_latest.ics').read_bytes())
        events = cls.full.walk('VEVENT')
        cls.start_year = events[0].decoded('DTSTART').year
        cls.end_year = events[-1].decoded('DTSTART').year
        cls.minimal = LunarCalendarGenerator('en', minimal=True).generate_range(cls.start_year, cls.end_year)
        cls.minimal_vi = LunarCalendarGenerator(minimal=True).generate_range(cls.start_year, cls.end_year)

    def test_exact_selection_titles_and_distinct_stable_identifiers(self):
        expected = {}
        for event in self.full.walk('VEVENT'):
            match = re.match(r'Lunar day (\d+), (leap )?month (\d+) ', str(event['DESCRIPTION']))
            self.assertIsNotNone(match)
            day, leap, month = match.groups()
            if day == '15':
                expected[event.decoded('DTSTART')] = 'Full Moon'
            elif day == '1' and month == '1' and not leap:
                expected[event.decoded('DTSTART')] = 'Lunar New Year'
        actual = self.minimal.walk('VEVENT')
        self.assertEqual(len(actual), len(expected))
        self.assertEqual(len({str(event['UID']) for event in actual}), len(actual))
        self.assertEqual({event.decoded('DTSTART'): str(event['SUMMARY']) for event in actual}, expected)
        for event in actual:
            solar = event.decoded('DTSTART')
            self.assertEqual(event.decoded('DTEND'), solar + timedelta(days=1))
            self.assertEqual(str(event['UID']), f'vnlunar-en-minimal-{solar:%Y%m%d}@cmduyeen')
            self.assertTrue(str(event['DESCRIPTION']).isascii())

    def test_minimal_metadata_and_checked_in_artifacts(self):
        self.assertEqual(str(self.minimal['X-WR-CALDESC']), MINIMAL_CALENDAR_DESCRIPTION_EN)
        self.assertEqual(
            str(self.minimal['X-WR-CALNAME']),
            f'{MINIMAL_CALENDAR_NAME_EN} {self.start_year}\u2013{self.end_year}',
        )
        output = ROOT / 'output'
        latest = (output / 'viet_lunar_en_minimal_latest.ics').read_bytes()
        self.assertEqual(latest, (output / f'viet_lunar_en_minimal_{self.start_year}_{self.end_year}.ics').read_bytes())
        self.assertEqual(without_timestamps(Calendar.from_ical(latest)), without_timestamps(self.minimal))
        with zipfile.ZipFile(output / f'viet_lunar_en_minimal_yearly_{self.start_year}_{self.end_year}.zip') as archive:
            names = [f'viet_lunar_en_minimal_{year}.ics' for year in range(self.start_year, self.end_year + 1)]
            self.assertEqual(archive.namelist(), names)
            for year, name in zip(range(self.start_year, self.end_year + 1), names):
                raw = (output / name).read_bytes()
                self.assertEqual(archive.read(name), raw)
                generated = LunarCalendarGenerator('en', minimal=True).generate_year(year)
                self.assertEqual(without_timestamps(Calendar.from_ical(raw)), without_timestamps(generated))

    def test_full_moon_titles_ignore_holiday_collisions(self):
        solar = date(2026, 1, 1)
        base = to_lunar(solar)
        for month in (1, 4, 7, 8):
            with self.subTest(month=month):
                lunar = replace(base, lunar_month=month, lunar_day=15, is_leap_month=False)
                event = _build_event_for_day(solar, lunar, 'en', minimal=True)
                self.assertEqual(str(event['SUMMARY']), 'Full Moon')
                self.assertIn('not an exact astronomical full moon time', str(event['DESCRIPTION']))
                self.assertNotIn(FIXED_LUNAR_HOLIDAYS[(month, 15)].name_en, str(event['DESCRIPTION']))
                self.assertNotIn('X-MICROSOFT-CDO-IMPORTANCE', event)
                self.assertEqual(str(event['COLOR']), '#FB8C00')

    def test_filter_includes_leap_full_moons_but_not_leap_new_year(self):
        solar = date(2026, 2, 17)
        base = to_lunar(solar)
        generator = LunarCalendarGenerator('en', minimal=True)
        for month, day, expected in (
            (1, 1, 'Lunar New Year'), (-1, 1, None), (-1, 15, 'Full Moon'),
            (-6, 15, 'Full Moon'), (1, 2, None), (1, 3, None),
            (12, 29, None), (12, 30, None), (6, 1, None), (6, 7, None),
        ):
            with self.subTest(month=month, day=day):
                lunar = replace(base, lunar_month=month, lunar_day=day, is_leap_month=month < 0)
                calendar = generator._make_calendar()
                with patch('src.ics_generator.to_lunar', return_value=lunar):
                    generator._fill_calendar(calendar, solar, solar)
                self.assertEqual(
                    [str(event['SUMMARY']) for event in calendar.walk('VEVENT')],
                    [expected] if expected else [],
                )

    def test_minimal_supports_both_languages_and_full_is_default(self):
        self.assertFalse(LunarCalendarGenerator('en').minimal)
        self.assertFalse(LunarCalendarGenerator().minimal)
        default = LunarCalendarGenerator(minimal=True)
        explicit = LunarCalendarGenerator('vi', minimal=True)
        self.assertEqual(default.language, 'vi')
        self.assertEqual(default.calendar_name, explicit.calendar_name)
        self.assertEqual(default.calendar_description, explicit.calendar_description)
        self.assertEqual(default.calendar_name, MINIMAL_CALENDAR_NAME)

    def test_vietnamese_minimal_matches_english_and_checked_in_artifacts(self):
        self.assertEqual(str(self.minimal_vi['PRODID']), PRODID)
        self.assertEqual(str(self.minimal_vi['X-WR-CALDESC']), MINIMAL_CALENDAR_DESCRIPTION)
        self.assertEqual(
            str(self.minimal_vi['X-WR-CALNAME']),
            f'{MINIMAL_CALENDAR_NAME} {self.start_year}\u2013{self.end_year}',
        )
        vi_events = self.minimal_vi.walk('VEVENT')
        en_events = self.minimal.walk('VEVENT')
        self.assertEqual(len(vi_events), len(en_events))
        self.assertEqual(len({str(event['UID']) for event in vi_events}), len(vi_events))
        titles = {'Full Moon': 'R\u1eb1m', 'Lunar New Year': 'T\u1ebft Nguy\u00ean \u0110\u00e1n'}
        for vi, en in zip(vi_events, en_events):
            self.assertEqual(str(vi['SUMMARY']), titles[str(en['SUMMARY'])])
            self.assertEqual(str(vi['UID']), f"vnlunar-minimal-{vi.decoded('DTSTART'):%Y%m%d}@cmduyeen")
            self.assertNotEqual(vi['UID'], en['UID'])
            for key in ('DTSTART', 'DTEND', 'COLOR', 'X-MICROSOFT-CDO-IMPORTANCE'):
                self.assertEqual(vi.get(key), en.get(key))
        output = ROOT / 'output'
        latest = (output / 'viet_lunar_minimal_latest.ics').read_bytes()
        self.assertEqual(latest, (output / f'viet_lunar_minimal_{self.start_year}_{self.end_year}.ics').read_bytes())
        self.assertEqual(without_timestamps(Calendar.from_ical(latest)), without_timestamps(self.minimal_vi))
        with zipfile.ZipFile(output / f'viet_lunar_minimal_yearly_{self.start_year}_{self.end_year}.zip') as archive:
            names = [f'viet_lunar_minimal_{year}.ics' for year in range(self.start_year, self.end_year + 1)]
            self.assertEqual(archive.namelist(), names)
            for year, name in zip(range(self.start_year, self.end_year + 1), names):
                raw = (output / name).read_bytes()
                self.assertEqual(archive.read(name), raw)
                self.assertTrue(raw.endswith(b'\r\n'))
                self.assertNotIn(b'\n', raw.replace(b'\r\n', b''))
                self.assertTrue(all(len(line) <= 75 for line in raw.split(b'\r\n')))
                generated = LunarCalendarGenerator(minimal=True).generate_year(year)
                self.assertEqual(without_timestamps(Calendar.from_ical(raw)), without_timestamps(generated))

    def test_vietnamese_full_moon_collisions_and_leap_markers(self):
        solar = date(2026, 1, 1)
        base = to_lunar(solar)
        for month in (1, 4, 7, 8, -1, -6):
            with self.subTest(month=month):
                lunar = replace(base, lunar_month=month, lunar_day=15, is_leap_month=month < 0)
                event = _build_event_for_day(solar, lunar, minimal=True)
                self.assertEqual(str(event['SUMMARY']), 'R\u1eb1m')
                self.assertIn(FULL_MOON_NOTE, str(event['DESCRIPTION']))
                self.assertEqual(' nhu\u1eadn ' in str(event['DESCRIPTION']), month < 0)
                self.assertNotIn('X-MICROSOFT-CDO-IMPORTANCE', event)
        lunar = replace(base, lunar_month=-1, lunar_day=1, is_leap_month=True)
        generator = LunarCalendarGenerator(minimal=True)
        calendar = generator._make_calendar()
        with patch('src.ics_generator.to_lunar', return_value=lunar):
            generator._fill_calendar(calendar, solar, solar)
        self.assertEqual(calendar.walk('VEVENT'), [])

    def test_vietnamese_minimal_errors_do_not_publish_partial_calendars(self):
        with patch('src.ics_generator.to_lunar', side_effect=ValueError('Conversion failed')):
            with self.assertRaisesRegex(RuntimeError, 'Failed to generate Vietnamese event'):
                LunarCalendarGenerator(minimal=True).generate_year(2026)


class CommandLineTests(unittest.TestCase):
    def run_main(self, *arguments):
        with patch('sys.argv', ['main.py', *arguments]), patch('main.HAS_TQDM', False), \
                contextlib.redirect_stdout(io.StringIO()):
            main()

    def test_split_and_single_year_outputs_do_not_overwrite_other_language(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            vi_latest = output / 'viet_lunar_latest.ics'
            vi_latest.write_bytes(b'Existing Vietnamese subscription')
            self.run_main('--language', 'en', '--start', '2026', '--end', '2027', '--split', '--output-dir', directory)
            en_latest = output / 'viet_lunar_en_latest.ics'
            saved_latest = en_latest.read_bytes()
            self.assertEqual(saved_latest, (output / 'viet_lunar_en_2026_2027.ics').read_bytes())
            self.assertEqual(vi_latest.read_bytes(), b'Existing Vietnamese subscription')
            with zipfile.ZipFile(output / 'viet_lunar_en_yearly_2026_2027.zip') as archive:
                self.assertEqual(archive.namelist(), ['viet_lunar_en_2026.ics', 'viet_lunar_en_2027.ics'])
            self.run_main('--language', 'en', '--year', '2028', '--output-dir', directory)
            self.assertEqual(en_latest.read_bytes(), saved_latest)
            self.assertEqual(len(Calendar.from_ical((output / 'viet_lunar_en_2028.ics').read_bytes()).walk('VEVENT')), 366)
            self.run_main('--year', '2028', '--output-dir', directory)
            self.assertTrue((output / 'viet_lunar_2028.ics').is_file())
            self.assertEqual(en_latest.read_bytes(), saved_latest)
            self.assertEqual(vi_latest.read_bytes(), b'Existing Vietnamese subscription')

    def test_cleanup_is_language_specific_and_keeps_latest(self):
        for language, prefix, other_prefix in (
            ('vi', 'viet_lunar', 'viet_lunar_en'),
            ('en', 'viet_lunar_en', 'viet_lunar'),
        ):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                expired = [f'{prefix}_2025.ics', f'{prefix}_2025_2035.ics', f'{prefix}_yearly_2025_2035.zip']
                keep = [f'{prefix}_latest.ics', f'{prefix}_2026.ics', f'{prefix}_2026_2036.ics',
                        f'{prefix}_yearly_2026_2036.zip', f'{other_prefix}_2025.ics',
                        f'{other_prefix}_2025_2035.ics', f'{other_prefix}_yearly_2025_2035.zip', 'notes.txt']
                for name in expired + keep:
                    (output / name).touch()
                self.assertEqual(set(cleanup_past_files(output, 2026, language)), set(expired))
                self.assertEqual({path.name for path in output.iterdir()}, set(keep))

    def test_invalid_language_exits_before_writing(self):
        with patch('sys.argv', ['main.py', '--language', 'fr']), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main()
        self.assertEqual(error.exception.code, 2)

    def test_minimal_cli_outputs_preserve_full_feeds_and_latest_on_year_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            full_names = ['viet_lunar_latest.ics', 'viet_lunar_en_latest.ics',
                          'viet_lunar_en_2025.ics', 'viet_lunar_minimal_latest.ics']
            for name in full_names:
                (output / name).write_bytes(b'Existing full feed')
            self.run_main('--language', 'en', '--minimal', '--start', '2026', '--end', '2027',
                          '--split', '--output-dir', directory)
            latest = (output / 'viet_lunar_en_minimal_latest.ics').read_bytes()
            self.assertEqual(latest, (output / 'viet_lunar_en_minimal_2026_2027.ics').read_bytes())
            with zipfile.ZipFile(output / 'viet_lunar_en_minimal_yearly_2026_2027.zip') as archive:
                self.assertEqual(archive.namelist(), ['viet_lunar_en_minimal_2026.ics', 'viet_lunar_en_minimal_2027.ics'])
            self.run_main('--language', 'en', '--minimal', '--year', '2028', '--output-dir', directory)
            self.assertTrue((output / 'viet_lunar_en_minimal_2028.ics').is_file())
            self.assertEqual((output / 'viet_lunar_en_minimal_latest.ics').read_bytes(), latest)
            for name in full_names:
                self.assertEqual((output / name).read_bytes(), b'Existing full feed')

    def test_cleanup_is_isolated_between_all_four_feeds(self):
        variants = [('vi', False, 'viet_lunar'), ('en', False, 'viet_lunar_en'),
                    ('vi', True, 'viet_lunar_minimal'), ('en', True, 'viet_lunar_en_minimal')]
        for language, minimal, prefix in variants:
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                names = {f'{p}_{suffix}' for _, _, p in variants for suffix in (
                    '2025.ics', '2025_2035.ics', 'yearly_2025_2035.zip', 'latest.ics', '2026.ics',
                )}
                for name in names:
                    (output / name).touch()
                expired = {f'{prefix}_{suffix}' for suffix in ('2025.ics', '2025_2035.ics', 'yearly_2025_2035.zip')}
                self.assertEqual(set(cleanup_past_files(output, 2026, language, minimal)), expired)
                self.assertEqual({path.name for path in output.iterdir()}, names - expired)

    def test_default_and_explicit_vietnamese_minimal_cli_preserve_other_feeds(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            other_names = ['viet_lunar_latest.ics', 'viet_lunar_en_latest.ics',
                           'viet_lunar_en_minimal_latest.ics', 'viet_lunar_2025.ics']
            for name in other_names:
                (output / name).write_bytes(b'Existing feed')
            self.run_main('--minimal', '--start', '2026', '--end', '2027', '--split', '--output-dir', directory)
            latest = (output / 'viet_lunar_minimal_latest.ics').read_bytes()
            self.assertEqual(latest, (output / 'viet_lunar_minimal_2026_2027.ics').read_bytes())
            with zipfile.ZipFile(output / 'viet_lunar_minimal_yearly_2026_2027.zip') as archive:
                self.assertEqual(archive.namelist(), ['viet_lunar_minimal_2026.ics', 'viet_lunar_minimal_2027.ics'])
            self.run_main('--minimal', '--year', '2028', '--output-dir', directory)
            default = Calendar.from_ical((output / 'viet_lunar_minimal_2028.ics').read_bytes())
            self.run_main('--language', 'vi', '--minimal', '--year', '2028', '--output-dir', directory)
            explicit = Calendar.from_ical((output / 'viet_lunar_minimal_2028.ics').read_bytes())
            self.assertEqual(without_timestamps(default), without_timestamps(explicit))
            self.assertEqual((output / 'viet_lunar_minimal_latest.ics').read_bytes(), latest)
            for name in other_names:
                self.assertEqual((output / name).read_bytes(), b'Existing feed')


if __name__ == '__main__':
    unittest.main()
