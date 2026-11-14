"""Public compatibility facade; new profiles all use the shared pipeline."""
from .legacy_generator import LunarCalendarGenerator as LegacyGenerator
from .user_config import CalendarOptions
from .pipeline import generate, validate_range


class LunarCalendarGenerator(LegacyGenerator):
    def generate_range(self,start_year,end_year,options=None):
        options=options or CalendarOptions()
        validate_range(start_year,end_year,options)
        if options.legacy:
            return super().generate_range(start_year,end_year,options)
        return generate(start_year,end_year,options)

    def generate_year(self,year,options=None):
        options=options or CalendarOptions()
        validate_range(year,year,options)
        if options.legacy:
            return super().generate_year(year,options)
        return generate(year,year,options)

    @staticmethod
    def save(calendar,filepath):
        from .ics import write_calendar
        write_calendar(calendar,filepath)
