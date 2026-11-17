"""Protect main-branch daily feeds when shared profiles are enabled."""
from datetime import date
import unittest

from src.ics_generator import LunarCalendarGenerator
from src.user_config import CalendarOptions


class MergeCompatibilityTests(unittest.TestCase):
    def test_default_published_daily_feed_retains_main_observances_and_uids(self):
        generator = LunarCalendarGenerator()
        direct = generator.generate_year(2026)
        published = generator.generate_year(2026, CalendarOptions())
        before = {e.decoded('dtstart'): e for e in direct.walk('VEVENT')}
        after = {e.decoded('dtstart'): e for e in published.walk('VEVENT')}
        self.assertEqual(len(after), 365)
        for day in before:
            self.assertEqual(str(before[day]['uid']), str(after[day]['uid']))
            self.assertEqual(str(before[day]['summary']), str(after[day]['summary']))
            self.assertIsInstance(after[day]['x-lunar-color'], str)
        self.assertEqual(str(after[date(2026, 1, 1)]['x-lunar-color']), '#E53935')
        from src.lunar_converter import to_lunar
        for day, event in after.items():
            if to_lunar(day).lunar_day in (1, 15) and 'x-microsoft-cdo-importance' not in event:
                self.assertEqual(str(event['x-lunar-color']), '#FB8C00')

    def test_profile_generation_remains_independent_of_daily_customization(self):
        generator = LunarCalendarGenerator('en', 'none')
        profile = generator.generate_year(2026, CalendarOptions(country='KR', language='en'))
        identities = {str(e['x-lunar-event-id']) for e in profile.walk('VEVENT')}
        self.assertIn('chuseok', identities)
        self.assertIn('chuseok_eve', identities)
        self.assertIn('chuseok_day_2', identities)
