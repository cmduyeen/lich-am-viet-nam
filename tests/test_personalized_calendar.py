import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from icalendar import Calendar

from src.ics_generator import LunarCalendarGenerator
from src.user_config import CalendarOptions, load_calendar_options


class CalendarOptionsTests(unittest.TestCase):
    def test_loads_personal_options_from_json(self) -> None:
        settings = {
            "language": "en",
            "start_year": 2026,
            "end_year": 2027,
            "lunar_days": [1, 15],
            "holiday_types": ["lunar"],
            "colors": {"holiday": "#123abc"},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "calendar.json"
            path.write_text(json.dumps(settings), encoding="utf-8")

            options = load_calendar_options(path)

        self.assertEqual(options.language, "en")
        self.assertEqual(options.lunar_days, frozenset({1, 15}))
        self.assertEqual(options.holiday_types, frozenset({"lunar"}))
        self.assertEqual(options.holiday_color, "#123ABC")

    def test_rejects_invalid_colors_and_unknown_settings(self) -> None:
        with self.assertRaisesRegex(ValueError, "six-digit hex color"):
            CalendarOptions(holiday_color="red")
        with self.assertRaisesRegex(ValueError, "unknown configuration key"):
            CalendarOptions.from_mapping({"langauge": "en"})


class PersonalizedCalendarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = LunarCalendarGenerator()

    def _events_by_date(self, calendar: Calendar) -> dict[date, object]:
        return {
            component.decoded("dtstart"): component
            for component in calendar.walk("VEVENT")
        }

    def test_english_output_localizes_metadata_and_event(self) -> None:
        options = CalendarOptions(
            language="en",
            start_year=2026,
            end_year=2026,
            lunar_days=frozenset(),
            holiday_types=frozenset({"lunar"}),
            holiday_color="#123ABC",
        )
        calendar = self.generator.generate_year(2026, options)
        events = self._events_by_date(calendar)
        new_year = events[date(2026, 2, 17)]

        self.assertEqual(str(calendar.get("x-wr-calname")), "Vietnamese Lunar Calendar 2026")
        self.assertIn("Lunar New Year", str(new_year.get("summary")))
        self.assertIn("Year of the Fire Horse", str(new_year.get("description")))
        self.assertEqual(str(new_year.get("x-lunar-color")), "#123ABC")
        self.assertIn("-en-", str(new_year.get("uid")))
        self.assertNotIn(date(2026, 1, 1), events)

    def test_lunar_day_filter_and_holiday_filter_are_independent(self) -> None:
        options = CalendarOptions(
            language="en",
            lunar_days=frozenset({1}),
            holiday_types=frozenset(),
        )
        events = self._events_by_date(self.generator.generate_year(2026, options))

        self.assertIn(date(2026, 2, 17), events)
        self.assertNotIn(date(2026, 2, 18), events)
        self.assertNotIn(date(2026, 9, 2), events)


if __name__ == "__main__":
    unittest.main()
