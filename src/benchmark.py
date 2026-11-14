"""Small reproducible cache benchmark; run with python -m src.benchmark."""
from time import perf_counter
from .engines import ENGINES
from .ics_generator import LunarCalendarGenerator
from .user_config import CalendarOptions


def main():
    engine=ENGINES['chinese']
    engine.cache_clear()
    generator=LunarCalendarGenerator()
    start=perf_counter()
    first=generator.generate_year(2027,CalendarOptions(country='CN',language='en',content='daily'))
    cold=perf_counter()-start
    misses=engine.cache_info().misses
    start=perf_counter()
    second=generator.generate_year(2027,CalendarOptions(country='CN',language='zh-Hans',content='daily'))
    warm=perf_counter()-start
    extra=engine.cache_info().misses-misses
    if extra: raise RuntimeError('Language generation repeated lunar conversion')
    print(f'CN 2027: cold={cold:.3f}s; second-language={warm:.3f}s; extra conversions={extra}; events={len(first.walk("VEVENT"))}/{len(second.walk("VEVENT"))}')


if __name__=='__main__': main()
