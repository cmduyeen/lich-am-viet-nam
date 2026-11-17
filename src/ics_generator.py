"""Public compatibility facade; new profiles all use the shared pipeline."""
from .legacy_generator import LunarCalendarGenerator as LegacyGenerator
from .user_config import CalendarOptions
from .pipeline import generate, validate_range
from .daily_generator import LunarCalendarGenerator as DailyGenerator, _build_event_for_day


class LunarCalendarGenerator(LegacyGenerator):
    def __init__(self, language='vi', holidays='all', custom_holidays=()):
        self.daily = DailyGenerator(language, holidays, custom_holidays)

    def _daily_calendar(self, start, end, options):
        from .colors import add_event_color
        calendar = DailyGenerator(options.language).generate_range(start, end)
        calendar['x-apple-calendar-color'] = options.calendar_color
        for event in calendar.walk('VEVENT'):
            event.pop('color')
            rgb = str(event.pop('x-lunar-color'))
            if 'x-microsoft-cdo-importance' in event:
                rgb = options.holiday_color or options.calendar_color
            elif rgb == '#FB8C00':
                rgb = options.lunar_day_color
            else:
                rgb = options.ordinary_color
            add_event_color(event, rgb)
        return calendar

    @staticmethod
    def _plain_daily(options, end):
        return (options.legacy and not options.minimal and options.lunar_days is None
                and options.holiday_types == frozenset({'solar', 'lunar'}) and end <= 2098)

    def generate_range(self,start_year,end_year,options=None):
        if options is None:
            return self.daily.generate_range(start_year,end_year)
        validate_range(start_year,end_year,options)
        if self._plain_daily(options, end_year):
            return self._daily_calendar(start_year, end_year, options)
        if options.legacy:
            return super().generate_range(start_year,end_year,options)
        return generate(start_year,end_year,options)

    def generate_year(self,year,options=None):
        if options is None:
            return self.daily.generate_year(year)
        validate_range(year,year,options)
        if self._plain_daily(options, year):
            return self._daily_calendar(year, year, options)
        if options.legacy:
            return super().generate_year(year,options)
        return generate(year,year,options)

    @staticmethod
    def save(calendar,filepath):
        from .ics import write_calendar
        write_calendar(calendar,filepath)
